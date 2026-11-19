# CMP-ORD-CANCEL — Cancellation & Return Coordinator

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-ORD-CANCEL |
| **Parent Container** | CNT-ACC-ORDERS (Order Management Domain — ACCSystem) |
| **Purpose** | Receives cancellation or return requests, validates that the order state allows the transition, and coordinates compensation across the reservation, payment, and delivery domains. Supports partial compensation when individual steps fail. |
| **Scope Boundary** | Owns the cancellation/return coordination flow. Does NOT own reservation cancellation logic (ACCore), payment void/refund logic (CMP-PAY-REFUND), or delivery halt logic (CNT-ACC-DELIVERY). |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| Order Management API / User | Inbound (called by) | Buyer or authorized actor submits cancellation/return request |
| CMP-ORD-STATEMACHINE | Outbound (calls) | Checks if cancellation/return transition is allowed; requests state transition |
| CMP-INT-RESERVATION | Outbound (calls) | Sends reservation release/cancel to ACCore seller |
| CMP-PAY-REFUND | Outbound (calls) | Triggers void (pre-capture) or refund (post-capture) |
| CNT-ACC-DELIVERY | Outbound (calls) | Requests shipment halt or return initiation |
| Event Bus | Outbound | Publishes `OrderCancelled`, `ReturnRequested` events |
| Outbox Table | Outbound | Guarantees event publication |

---

## 3. Behavior, Rules, and State

### 3.1 Cancellation Flow

1. Receive cancellation request (`order_id`, `reason`, `requester`).
2. Check with CMP-ORD-STATEMACHINE: is transition to `CancellationPending` allowed?
   - If not allowed (e.g., order already `Completed`, `Cancelled`, `Returned`) → reject with reason.
3. Transition order state to `CancellationPending`.
4. Execute compensation steps (order independent, can run in parallel):
   - **Step A:** Release/cancel reservation at ACCore seller via CMP-INT-RESERVATION.
   - **Step B:** Void or refund payment via CMP-PAY-REFUND.
   - **Step C:** Halt or return shipment via CNT-ACC-DELIVERY.
5. Record outcome of each step (success / failed / skipped).
6. When all steps are settled (or max retries reached):
   - If all succeeded (or not applicable) → transition to `Cancelled`.
   - If some steps failed → remain in `CancellationPending` with operational alert; retry strategy applies.
7. Publish `OrderCancelled` event with `correlation_id`.

### 3.2 Return Flow

1. Receive return request (`seller_order_id` or `order_id`, `return_reason`, `line_items`).
2. Check transition to `ReturnPending` is allowed (must be in `Delivered` or `Completed`).
3. Transition to `ReturnPending`.
4. Coordinate:
   - Initiate delivery return/collection via CNT-ACC-DELIVERY.
   - Trigger refund via CMP-PAY-REFUND (after delivery return confirmed, or immediately — per policy (OPEN: see idea.md §12, OWNER_UNASSIGNED)).
5. On completion → transition to `Returned`.
6. Publish `ReturnRequested` and subsequently `OrderReturned`.

### 3.3 Business Rules (§7.4)

- Cancellation is **not** deletion. It is a state transition with full audit trail.
- Each compensation step has an **independent outcome**. A failure in one step does not automatically fail or block others.
- **Partial compensation** is supported: if delivery halt fails (shipment already dispatched), cancellation can still proceed for reservation and payment, with an operational flag raised for manual delivery handling.
- The coordinator must track each step's result and persist it.
- Cancellation of an order in `PendingReservation` or `PendingPayment` is handled by CMP-ORD-SAGA compensation; CMP-ORD-CANCEL handles post-`Confirmed` cancellations.

### 3.4 Compensation Decision Table (§7.5)

| Order State at Cancel Request | Reservation Action | Payment Action | Delivery Action |
|---|---|---|---|
| PendingReservation / PendingPayment | Via saga compensation | Via saga compensation | N/A |
| Confirmed (before dispatch) | Release reservation | Void (pre-capture) or Refund | Cancel shipment creation |
| Processing / Dispatched | Release reservation (if still held) | Refund (post-capture) | Request delivery return |
| Delivered | N/A | Refund | N/A (already delivered) |

---

## 4. Data and Side Effects

| Data Item | Owned By | Description |
|---|---|---|
| Cancellation / Return record | CMP-ORD-CANCEL | `{order_id, request_type, requester, reason, step_outcomes[], final_state, created_at}` |
| Step outcome records | CMP-ORD-CANCEL | Per-step result: `{step, status, attempt_count, last_error}` |
| `OrderCancelled` / `ReturnRequested` events | Outbox → Event Bus | Published on final state transition |

- **Transaction boundary:** Cancellation record creation + order state transition to `CancellationPending` are atomic. Each compensation step outcome is written independently as it completes.
- **Idempotency:** If a cancellation/return record already exists for the same `order_id`, return the existing record's status.

---

## 5. Failure, Security, and Operations

### 5.1 Failure Modes

| Failure | Response |
|---|---|
| State machine rejects cancellation (invalid transition) | Return rejection error with current state and reason |
| ACCore seller unreachable during reservation release | Retry with backoff; after max retries → flag for manual handling; allow payment/delivery steps to proceed |
| Payment refund fails | Retry; after max retries → operational alert for manual reconciliation |
| Delivery halt fails (shipment already moving) | Log failure; alert operations team; cancellation of order and payment proceeds |
| Coordinator crashes mid-flow | On restart, re-read step_outcomes; resume from incomplete steps |

### 5.2 Timeouts and Circuit Breaking

- Each outbound compensation call has a configured timeout.
- Circuit breaker for ACCore delivery calls (may be physically unavailable).
- Max retry policy with dead-letter for each step is a configurable Operations/SRE policy; calibration requires recovery and audit evidence before production.

### 5.3 Security

- Cancellation requests require authenticated user with appropriate role (buyer for own orders; institution admin for seller orders; platform support with scoped access).
- Return requests similarly scoped — buyers can request returns for their orders within policy window.
- Internal compensation calls (reservation, payment, delivery) are service-to-service only.

### 5.4 Audit Events

| Event | Trigger |
|---|---|
| `CancellationRequested` | Request received and validated |
| `OrderCancellationStepCompleted` | Each compensation step completes |
| `OrderCancelled` | Final Cancelled state reached |
| `ReturnRequested` | Return request validated and initiated |
| `OrderReturned` | Final Returned state reached |

---

## 6. Verification and Tests

| Scenario | Expected Outcome |
|---|---|
| Cancel order in `Confirmed` state | Reservation released, payment voided, delivery cancelled, order → Cancelled |
| Cancel order in `Dispatched` state | Payment refunded, delivery return initiated, order → Cancelled |
| Cancel already-Cancelled order | Rejection with `InvalidStateTransition` |
| Payment refund fails during cancellation | Operational alert raised; order stays CancellationPending; retry scheduled |
| Delivery return fails | Log + alert; cancellation proceeds for other steps |
| Idempotent cancellation request | Existing cancellation record returned; no duplicate steps executed |
| Return request on `Delivered` order | Delivery return initiated, refund triggered, order → Returned |

### 6.1 Partial Refund Edge Case

> [!WARNING]
> Partial refunds are marked **UNKNOWN** — business rules not yet defined (§12). The coordinator must support partial refund amounts when the business rule is established. Until then, all refunds are for the full order/seller-order amount.

---

## 7. Unknowns, Traceability, and ADR References

| Item | Status | Owner / Action |
|---|---|---|
| Partial refund rules | UNKNOWN | Product/Finance team; define before Phase 6 |
| Return eligibility window (time limit from delivery) | UNKNOWN | Product team; define before Phase 4 |
| Refund trigger: on return request or on delivery return confirmation? | UNKNOWN | Business decision; before Phase 6 |
| Max retry counts per compensation step | UNKNOWN — config decision | Architecture team; before Phase 3 |

**ADR References:** ADR-005, ADR-006, ADR-007

**Requirement References:** §7.4 (cancellation/returns), §7.5 (partial failure handling), §12 (open decisions on returns/disputes)
