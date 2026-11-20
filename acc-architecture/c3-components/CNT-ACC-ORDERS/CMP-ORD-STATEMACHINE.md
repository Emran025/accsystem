# CMP-ORD-STATEMACHINE — Order State Machine

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-ORD-STATEMACHINE |
| **Parent Container** | CNT-ACC-ORDERS (Order Management Domain — ACCSystem) |
| **Purpose** | Enforces valid state transitions for both Parent Orders and Seller Orders. Records every transition with actor, timestamp, and reason. Rejects invalid or out-of-sequence transitions. |
| **Scope Boundary** | Owns the order state record and transition history. Does NOT enforce business rules for payment, reservation, or delivery — those are owned by their respective domains. The state machine accepts or rejects transitions based on the allowed transition graph only. |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CMP-ORD-SAGA | Inbound (called by) | Requests state transitions at each saga step |
| CMP-ORD-CANCEL | Inbound (called by) | Requests CancellationPending, Cancelled, ReturnPending, Returned transitions |
| Event Bus | Outbound | Publishes `OrderStateChanged` event on every successful transition |
| Outbox Table | Outbound | Persists the event intent atomically with the state write; publication is a separate recoverable relay |
| Order Record (DB) | Read/Write | Owns `{order_id, current_state, state_history[], updated_at}` |

---

## 3. Behavior, Rules, and State

### 3.1 Order States (§7.6)

| State | Meaning |
|---|---|
| `PendingValidation` | Checkout received; validating buyer eligibility, items, and price |
| `PendingReservation` | Independent reservation requests sent to every seller ACCore |
| `PendingPayment` | All required reservations authoritatively accepted; awaiting the definitive payment outcome for the selected permitted capture mode |
| `ReservationUnknown` | A reservation outcome may have been dispatched but is not authoritative; non-terminal and payment-blocking |
| `PaymentUnknown` | Payment outcome may have been dispatched but is not authoritative; non-terminal and compensation-blocking |
| `PendingReview` | Non-terminal escalation of an unresolved reservation or payment operation; retain its originating state and evidence, and do not infer an outcome from escalation |
| `Confirmed` | Order commercially confirmed after definitive payment success for the approved mode (authorization, or immediate capture where supported) |
| `Processing` | Seller preparing order |
| `PartiallyFulfilled` | Partial shipment dispatched (multi-seller or multi-shipment) |
| `Dispatched` | Shipment handed to delivery |
| `Delivered` | Delivery confirmed with proof |
| `Completed` | All commercial and operational obligations met |
| `CancellationPending` | Cancellation request in-flight |
| `Cancelled` | Cancellation finalized only after all applicable stock, payment and delivery actions are settled under policy; confirmed-linked or consumed holds are not released as ordinary reservations |
| `ReturnPending` | Return request in-flight |
| `Returned` | Return and refund fully processed |
| `Failed` | Terminal failure (checkout expired, saga compensation complete) |
| `Expired` | An authoritative ACCore `EXPIRED` reservation outcome or approved expiry rule resolved before confirmation; elapsed time alone is insufficient |

### 3.2 Allowed Transition Graph

```
PendingValidation → PendingReservation
PendingValidation → Failed | Expired

PendingReservation → PendingPayment (only after every required SellerOrder reservation is authoritatively ACCEPTED)
PendingReservation → ReservationUnknown | Failed | Expired (failure/expiry only on authoritative evidence and after applicable compensation is resolved)
ReservationUnknown → PendingPayment (only after all required reservations resolve ACCEPTED)
ReservationUnknown → Failed | Expired (only from authoritative REJECTED/EXPIRED evidence and after relevant peer outcomes and required compensation are resolved)

PendingPayment → Confirmed (only after every required allocation is definitively successful, every required hold remains authoritatively accepted, and the confirmation commit guard succeeds)
PendingPayment → PaymentUnknown | Failed | Expired (failure/expiry only after relevant in-flight outcomes and applicable compensation are resolved)
PaymentUnknown → Confirmed (only after definitive success for every required payment allocation, all required holds remain authoritatively accepted, and confirmation commits)
PaymentUnknown → Failed | Expired (only after authoritative failure/expiry, reconciliation of all relevant effects and required compensation; exact disposition is policy-gated)
ReservationUnknown | PaymentUnknown → PendingReview (when policy escalation is required)
PendingReview → ReservationUnknown | PaymentUnknown (resume the originating reconciliation; subsequent transitions require their evidence and guards)

Confirmed → Processing | Dispatched | CancellationPending
Processing → PartiallyFulfilled | Dispatched | CancellationPending
PartiallyFulfilled → Dispatched | CancellationPending
Dispatched → Delivered | ReturnPending
Delivered → Completed | ReturnPending
Completed → ReturnPending

CancellationPending → Cancelled | Confirmed (revert only if explicitly rejected before irreversible compensation; otherwise remain pending/review)
ReturnPending → Returned | Delivered  (Returned only after required steps resolve under policy; a rejected return from Delivered may revert; restoration from other origins and Dispatched eligibility remain policy decisions)
```

> [!IMPORTANT]
> Any transition not listed above is **rejected** with an `InvalidStateTransition` error. The calling component (e.g., CMP-ORD-SAGA) is responsible for handling this rejection and deciding whether to retry or escalate.

### 3.3 Transition Record

Every successful transition records:

```json
{
  "order_id": "uuid",
  "from_state": "PendingPayment",
  "to_state": "Confirmed",
  "transitioned_at": "ISO-8601 UTC",
  "actor": "CMP-ORD-SAGA / system / user_id",
  "reason": "PaymentAuthorized",
  "correlation_id": "uuid"
}
```

### 3.4 Applies to Both Parent Order and Seller Orders

When an order is split (§8.2), each Seller Order has its own independent state machine instance. The Parent Order state is a **computed aggregation** of Seller Order states and is updated when any Seller Order transitions. The Parent Order state machine does NOT autonomously advance; it reflects the aggregate.

### 3.5 Business Rules

- State is the **single authoritative field** for order status. No component should infer order status from payment or delivery state directly.
- Transitions are **append-only** to the history log; past transitions are never modified.
- The state machine does not enforce business meaning (e.g., it does not know what "PaymentAuthorized" means) — it only enforces the graph.
- Unknown/review states are non-terminal and recoverable. `Failed`, `Expired`, `Cancelled` and `Returned` have no outgoing transitions in this graph. `Completed` ends ordinary fulfillment but retains the documented, policy-eligible `ReturnPending` path. `PENDING_REVIEW` and `PendingPaymentReview` occur in ADRs; their exact mapping to this order state remains an owner decision, not an assumed alias.

---

## 4. Data and Side Effects

| Data Item | Owned By | Description |
|---|---|---|
| Order state field | CMP-ORD-STATEMACHINE | Current state of `order_id` |
| Transition history | CMP-ORD-STATEMACHINE | Append-only log of all state transitions |
| `OrderStateChanged` event | Outbox → Event Bus | Published on every successful transition |

- **Transaction boundary:** State update + transition history append + outbox event write are committed in a single DB transaction.
- **Idempotency:** If requested transition matches the current state (already applied), return success without re-writing.
- **Concurrency:** Optimistic locking (`version` or `etag`) on the Order record prevents concurrent transition races.

---

## 5. Failure, Security, and Operations

### 5.1 Failure Modes

| Failure | Response |
|---|---|
| Invalid transition requested | Return `InvalidStateTransition` error; caller decides how to handle |
| DB write fails | Transaction rolled back; caller retries; idempotency prevents double-write |
| Outbox event not picked up | Outbox relay retries delivery; state is already written correctly |
| Concurrent transition conflict (optimistic lock) | Return conflict error; caller retries after re-reading current state |

### 5.2 Security

- Internal service only. Not exposed via any public or institution-facing API.
- Calls must originate from authorized internal services (CMP-ORD-SAGA, CMP-ORD-CANCEL).
- Audit: every `OrderStateChanged` event carries `actor` field indicating the system or user that triggered the transition.

### 5.3 Audit Events

| Event | Trigger |
|---|---|
| `OrderStateChanged` | Every successful state transition — published via Outbox |

---

## 6. Verification and Tests

| Scenario | Expected Outcome |
|---|---|
| Valid transition requested | State updated, history appended, `OrderStateChanged` published |
| Invalid transition (e.g., Confirmed → PendingPayment) | `InvalidStateTransition` error returned; no state change |
| Same transition requested twice (idempotent) | Second call returns success; no duplicate history entry |
| Concurrent transition attempt on same order | One succeeds; other receives conflict error and must retry |
| Unlisted terminal transition attempt | Rejected; a policy-eligible `Completed → ReturnPending` remains available |
| Seller Order state change triggers Parent Order recomputation | Parent Order state reflects updated aggregate |

---

## 7. Unknowns, Traceability, and ADR References

| Item | Status |
|---|---|
| PartiallyFulfilled logic for Parent Order aggregation | Needs product decision: how many Seller Orders must dispatch before parent moves? |
| Authoritative hold expiry during an unknown/successful payment | Orders, Finance, institution and provider owners must decide eligible Expired/Failed disposition and financial recovery after authoritative reconciliation; no confirmation while required holds are expired |
| ReturnPending restoration and Dispatched return eligibility | Product/Finance/Legal must define eligibility and how the prior state is restored, including a Completed origin |

**ADR References:** ADR-005, ADR-007

**Requirement References:** §7.6 (order states), §7.4 (cancellation/returns), §8.2 (multi-seller model), §11 (observability)
