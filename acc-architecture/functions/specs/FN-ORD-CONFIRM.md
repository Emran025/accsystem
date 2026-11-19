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

- **Who:** CMP-ORD-SAGA (internal), after payment authorization succeeds (FN-PAY-AUTHORIZE)
- **What:** Finalize the order: write commercial snapshot, transition state to CONFIRMED, publish OrderConfirmed event
- **How:** CMP-ORD-SAGA signals CMP-ORD-SNAPSHOT → CMP-ORD-STATEMACHINE → Outbox

---

## 3. Preconditions

| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | Order status = PENDING | CMP-ORD-STATEMACHINE | Saga aborts (invalid transition) |
| P2 | FN-ORD-RESERVE completed successfully | CMP-ORD-SAGA state | Cannot reach this step |
| P3 | FN-PAY-AUTHORIZE returned AUTHORIZED | CMP-ORD-SAGA state | Cannot reach this step |
| P4 | order_id not already CONFIRMED | CMP-ORD-STATEMACHINE (idempotency) | Return existing CONFIRMED order |

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
     payment_ref,
     snapshot_at: timestamp
   }
   → Stored in Orders DB, immutable after write

3. CMP-ORD-STATEMACHINE:
   Transition: PENDING → CONFIRMED
   Write: Order.status = CONFIRMED, Order.confirmed_at = now()
   Idempotency: if already CONFIRMED → return existing order (no-op)

4. CNT-ACC-ORDERS Outbox:
   Write OrderConfirmed event to Outbox:
   {
     event_type: "OrderConfirmed",
     order_id,
     buyer_id,
     institution_ids: [seller_id, ...],
     items: [...],
     total,
     payment_ref,
     confirmed_at
   }

5. Event Bus delivers OrderConfirmed (async, via CNT-ACC-EVENTBUS):
   → CMP-CON-ORDERRECEIVER @ each seller's ACCore: triggers inventory commit (stock deduction) + local sales record creation — these are async, post-saga; failures handled by retry/ops escalation, not saga compensation
   → CNT-ACC-LICENSE (triggers FN-LIC-ACTIVATE for software items)
   → CNT-ACC-NOTIFICATIONS (triggers buyer + seller notifications)
   → CNT-ACC-DELIVERY (triggers delivery job creation for physical items)
   → CNT-ACC-PAYMENT (triggers payment capture — timing: OPEN per idea.md §12)

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
| Payment provider | Provider auth/capture transaction | Provider returns a definitive `AUTHORIZED` or `FAILED` result for the money hold | No guarantee of outcome delivery timing; timeout remains `UNKNOWN` unless provider confirms |
| Event publication | Outbox send + retry loop | The event is retried with the same idempotency key until published or explicitly dead-lettered | No guarantee that all consumers receive and process it in order without duplicates |

### Required behavior for partial-success and unknown outcomes

- If `Order.status = CONFIRMED` is written but the `OrderConfirmed` event cannot be published, the transaction is not complete and the state must be retried as a recoverable saga boundary; no silent success is allowed.
- If ACCore confirms reservation but later the event is not processed or the local sales record fails, the order remains in a reconciliation state rather than being silently rolled back.
- If the payment provider times out or returns no final answer, the payment state is `UNKNOWN`, not `FAILED`; no order confirmation is allowed to proceed and no reservation is released until the provider outcome is resolved.
- If ACCore never responds to `OrderConfirmed`, the order remains confirmed in ACCSystem and is retried or reconciled at the ACCore integration layer; the system does not assume the seller accepted or rejected the order without evidence.

> **Important:** `FN-ORD-CONFIRM` is the ACCSystem commitment point for the buyer-facing order. It is not a claim that ACCore inventory commit or payment capture are already complete. Those are separate local states with explicit reconciliation.

## 5. Postconditions

| # | Postcondition |
|---|---|
| Q1 | Order.status = CONFIRMED in Orders DB |
| Q2 | Commercial snapshot immutably recorded (never modified) |
| Q3 | OrderConfirmed event in Outbox (guaranteed delivery via event bus) |
| Q4 | Downstream systems notified asynchronously |

---

## 6. Idempotency

| Field | Value |
|---|---|
| **Key** | `order_id` |
| **Store** | Orders DB (order state machine) |
| **Mechanism** | CONFIRMED is a terminal state — re-execution returns existing order |
| **Behavior on duplicate** | Return `{order_id, status: CONFIRMED, confirmed_at}` without re-writing snapshot or re-publishing event |

> [!IMPORTANT]
> The Outbox pattern guarantees exactly-once delivery of `OrderConfirmed` to downstream consumers even if the saga step is retried — the Outbox record is deduplicated by order_id.

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
| ACCore inventory commit fails (post-event delivery) | Retry via CMP-CON-ORDERRECEIVER retry/backoff; ops escalation if persistent; order status → PendingFulfillment | NO — inventory state uncertain; escalate |
| Payment capture fails (post-confirmation async) | CMP-PAY-RECONCILIATION handles; retry capture or flag for ops; order confirmed, payment pending capture | NO saga compensation; reconciliation path |
| Shipment creation fails (post-confirmation async) | Retry; order status = Confirmed/PendingDelivery; ops escalation | NO saga compensation; retry path |

> [!CAUTION]
> The Outbox write and the CONFIRMED state transition **must be atomic** (single DB transaction). This is the only guarantee that prevents an order being marked CONFIRMED without the downstream event being deliverable. If this atomicity is violated, the system enters a split-brain state requiring manual intervention.

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Caller | Only CMP-ORD-SAGA (internal ACCSystem orchestration) |
| Snapshot immutability | Snapshot table is append-only; no UPDATE operations permitted on snapshot after write |
| Event authorization | OrderConfirmed event carries only buyer-scoped data; no payment credentials |

---

## 9. Traceability

| Claim | Evidence |
|---|---|
| Commercial snapshot at confirmation | CONFIRMED (CMP-ORD-SNAPSHOT — idea.md §8.2) |
| OrderConfirmed triggers downstream activations | CONFIRMED (idea.md §7.3 — license activation; §4.3 — ACCore order receipt) |
| Outbox pattern for event delivery | CONFIRMED (ADR-005) |
| Financial commitment point | ASSUMPTION — confirmation is the commitment point; payment capture timing UNKNOWN (idea.md §12) |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
