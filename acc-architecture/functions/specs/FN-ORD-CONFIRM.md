# FN-ORD-CONFIRM — Order Confirmation Function Specification

**Function ID:** FN-ORD-CONFIRM  
**Operation ID:** OP-ORDER-CONFIRM  
**Status:** DRAFT | Evidence: idea.md §8, ADR-007, ADR-013

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | FN-ORD-CONFIRM |
| **Name** | Order Confirmation |
| **Layer** | Saga Step 3 — sub-function of FN-ORD-CHECKOUT |
| **Triggering Component** | CMP-ORD-SAGA (after FN-PAY-AUTHORIZE success) |
| **Operation ID** | OP-ORDER-CONFIRM |

---

## 2. Trigger

- **Who:** CMP-ORD-SAGA (internal), after definitive payment success for the selected approved mode (authorization or supported immediate capture; FN-PAY-AUTHORIZE)
- **What:** Finalize the order: write commercial snapshot, transition state to CONFIRMED, publish OrderConfirmed event
- **How:** CMP-ORD-SAGA signals CMP-ORD-SNAPSHOT → CMP-ORD-STATEMACHINE → Outbox

---

## 3. Preconditions

| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | Order is `PendingPayment`, or `PaymentUnknown` has been authoritatively resolved to success | CMP-ORD-STATEMACHINE / saga | No invalid transition; reconcile first |
| P2 | Every required SellerOrder reservation remains authoritatively accepted and applicable guards hold | CMP-ORD-SAGA state | Cannot reach this step |
| P3 | Definitive `AUTHORIZED` for auth-then-capture, or `CAPTURED` for a supported and approved immediate-capture path | CMP-ORD-SAGA state | UNKNOWN or incomplete allocations block confirmation |
| P4 | No immutable confirmation record exists for this operation | CMP-ORD-STATEMACHINE / Orders DB | Return the stored confirmation result on replay, even after fulfillment advances |

---

## 4. Execution Flow

```
1. CMP-ORD-SAGA triggers Confirm step

2. CMP-ORD-SNAPSHOT writes commercial snapshot (immutable):
   {
     order_id,
     buyer_id,
     items: [{seller_id, seller_product_id, title_at_purchase,
              quantity, unit_price_at_purchase, currency}],
     total_at_purchase,
     payment_ref: aggregate buyer-facing reference when one provider transaction is used; otherwise a stable collection of SellerOrder/allocation references,
     snapshot_at: timestamp
   }
   → Stored in Orders DB, immutable after write

3. CMP-ORD-STATEMACHINE:
   Transition: PendingPayment → Confirmed, or PaymentUnknown → Confirmed after authoritative resolution
   Write: order state Confirmed, Order.confirmed_at = now()
   Idempotency: if an immutable confirmation record exists → return its stored result (no-op), independent of current fulfillment state

4. CNT-ACC-ORDERS Outbox:
   Write OrderConfirmed event to Outbox (abbreviated illustration only; not a wire schema):
   {
     event_type: "OrderConfirmed",
     order_id,
     buyer_id,
     institution_ids: [seller_id, ...],
     items: [...],
     total,
     payment_ref: aggregate reference plus allocation references when applicable,
     confirmed_at
   }

5. Event Bus delivers OrderConfirmed asynchronously via CNT-ACC-EVENTBUS:
   → CMP-INT-ORDERNOTIFY routes authorized institution-scoped handoffs via IF-ACC-ORDER-CONFIRM to CMP-CON-ORDERRECEIVER: seller sale/inventory and B2B buyer purchase-document paths are distinct; failures use retry/reconciliation, not saga rollback
   → CNT-ACC-LICENSE (triggers FN-LIC-ACTIVATE for software items)
   → CNT-ACC-NOTIFICATIONS (triggers buyer + seller notifications)
   → CNT-ACC-DELIVERY (triggers delivery job creation for physical items)
   → CNT-ACC-PAYMENT (evaluate each allocation and approved later-capture trigger; already captured allocations require no second capture; UNKNOWN requires reconciliation). Capture, void/refund, seller-credit, commission and settlement commands remain SellerOrder/allocation-scoped even when the buyer-facing reference is aggregated.

6. CMP-ORD-SAGA signals SUCCESS → checkout response returned to buyer:
   {order_id, status: "CONFIRMED", confirmed_at}
```

---

## 4.1 Commitment Point and Transaction Boundaries

This function defines the ACCSystem order commitment point, not a distributed atomic commit across ACCSystem, ACCore, and the payment provider.

| Domain | Local transaction boundary | What is guaranteed | What is not guaranteed |
|---|---|---|---|
| ACCSystem order | `Orders DB`: write snapshot + `Order.status = CONFIRMED` + Outbox event in the same DB transaction | Once the transaction commits, ACCSystem has a durable confirmed order and an event to publish | No guarantee that downstream consumers (ACCore, payment capture, delivery) have processed it yet |
| ACCore inventory | `ACCore` local DB: reservation accepted → later `OrderConfirmed` processing commits stock deduction and sales record | Inventory is reduced and a sales record is created only after receiving the event | No atomic rollback of the confirmed order if ACCore later fails to process |
| Payment provider | Provider auth/capture transaction | An authoritative outcome is recorded for each applicable operation when established | Delivery may be delayed or lost; timeout remains `UNKNOWN` unless reconciled |
| Event publication | Outbox send + retry loop | The event is retried with the same idempotency key until published or explicitly dead-lettered | No guarantee that all consumers receive and process it in order without duplicates |

### Required behavior for partial-success and unknown outcomes

- If the local state/snapshot/outbox transaction fails, it must not partially commit; if commit outcome is uncertain, establish it before retry. Once committed, a later relay failure does not undo the order: retain and retry or dead-letter/reconcile the durable outbox record under policy.
- If ACCore confirms reservation but later the event is not processed or the local sales record fails, the order remains in a reconciliation state rather than being silently rolled back.
- If the payment provider times out or returns no final answer, the payment state is `UNKNOWN`, not `FAILED`; no order confirmation is allowed to proceed and no reservation is released until the provider outcome is resolved.
- If ACCore never responds to `OrderConfirmed`, the order remains confirmed in ACCSystem and is retried or reconciled at the ACCore integration layer; the system does not assume the seller accepted or rejected the order without evidence.

> **Important:** `FN-ORD-CONFIRM` is the ACCSystem commitment point for the buyer-facing order. It is not a claim that ACCore inventory commit or any later-capture operation is already complete; an approved immediate-capture allocation may already be captured. Those are separate local states with explicit reconciliation.

## 5. Postconditions

| # | Postcondition |
|---|---|
| Q1 | Order.status = CONFIRMED in Orders DB |
| Q2 | Commercial snapshot immutably recorded (never modified) |
| Q3 | OrderConfirmed event durably recorded in the local Outbox |
| Q4 | Downstream delivery is attempted asynchronously; receipt and consumer effects are not implied by commit |

---

## 6. Idempotency

| Field | Value |
|---|---|
| **Key** | `order_id` |
| **Store** | Orders DB immutable confirmation record plus order state machine |
| **Mechanism** | Confirmation writes an immutable confirmation record keyed independently of current fulfillment state; re-execution returns that record without treating the whole order lifecycle as terminal |
| **Behavior on duplicate** | Return the stored `{order_id, status: CONFIRMED, confirmed_at}` result without re-writing the snapshot or re-publishing the event, even after later fulfillment transitions |

> [!IMPORTANT]
> The Outbox pattern targets at-least-once delivery of `OrderConfirmed`; duplicate deliveries remain possible. Receiver Inbox and scoped idempotency guard business effects, with `event_id` retained for tracing. Receipt and completed effects are distinct; see IF-ACC-ORDER-CONFIRM §2A.

---

## 7. Failure / Rollback

> [!IMPORTANT]
> **`CONFIRMED` is the saga terminal state.** Once `Order.status = CONFIRMED` is written, the saga is complete and no saga-level compensation is possible. Post-confirmation steps (inventory commit at ACCore, payment capture, shipment creation) are **async and non-compensating at the saga level** — their failures are handled by retry, reconciliation, and operations escalation, not by rolling back the confirmed order.

The table below distinguishes **pre-confirmation failures** (still within saga, compensation available) from **post-confirmation failures** (outside saga scope):

### Pre-Confirmation Failures (snapshot/state write has not yet succeeded)

| Failure Scenario | Mitigation | Compensation Available? |
|---|---|---|
| Snapshot write fails (DB error before state transition) | Retry idempotently under the configured local recovery policy; order remains PENDING. If an external effect may exist, query/reconcile before any void/release. | YES — only for confirmed effects after state resolution |
| State transition to CONFIRMED fails (DB error) | Retry idempotently; order remains PENDING during retry. If an external effect may exist, query/reconcile before any void/release; compensation is conditional and idempotent | YES — only after state resolution |
| Saga timeout before Confirm step begins | If all relevant outcomes are definitive, compensate confirmed effects; if any reservation/payment outcome is UNKNOWN, preserve UNKNOWN and reconcile before release/void. | Conditional — only after state resolution |

### Post-Confirmation Failures (order is CONFIRMED; saga is complete)

| Failure Scenario | Mitigation | Compensation? |
|---|---|---|
| Outbox write fails after CONFIRMED written | **Critical** — Outbox write must be in same DB transaction as state transition to prevent split-brain. If transaction atomically fails, order stays PENDING (pre-confirmation failure path). If order is CONFIRMED but event delivery stalls: ops alert + manual replay | NO saga compensation — order is confirmed; use reconciliation |
| ACCore inventory commit fails (post-event delivery) | Retain the confirmed order; record a separate pending fulfillment/inventory condition, reconcile UNKNOWN before repeating effects, and escalate per policy. Mapping to any order state is open. | NO saga rollback — inventory state may be uncertain |
| Payment capture fails (post-confirmation async) | CMP-PAY-RECONCILIATION handles; retry capture or flag for ops; order confirmed, payment pending capture | NO saga compensation; reconciliation path |
| Shipment creation fails (post-confirmation async) | Retain Confirmed and a separate pending-delivery condition; retry/reconcile and escalate per policy. Mapping to an order state is open. | NO saga compensation; retry path |

> [!CAUTION]
> The Outbox write and the CONFIRMED state transition **must be atomic** (single DB transaction). This is the only guarantee that prevents an order being marked CONFIRMED without the downstream event being deliverable. If this atomicity is violated, the system enters a split-brain state requiring manual intervention.

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Caller | Only CMP-ORD-SAGA (internal ACCSystem orchestration) |
| Snapshot immutability | Snapshot table is append-only; no UPDATE operations permitted on snapshot after write |
| Event authorization | Each handoff contains only recipient- and role-authorized data; no payment credentials. Buyer and seller scopes are distinct; see IF-ACC-ORDER-CONFIRM §2A |

---

## 9. Traceability

| Claim | Evidence |
|---|---|
| Commercial snapshot at confirmation | CONFIRMED (CMP-ORD-SNAPSHOT — idea.md §8.2) |
| OrderConfirmed triggers downstream activations | CONFIRMED (idea.md §7.3 — license activation; §4.3 — ACCore order receipt) |
| Outbox pattern for event delivery | CONFIRMED (ADR-005) |
| Financial commitment point | ADR-019 baseline: no universal financial trigger; institution Finance/Legal/Compliance approval remains required |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
