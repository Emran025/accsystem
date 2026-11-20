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
| Settlement/Ledger boundary | Outbound (calls) | Reverses or holds seller credit, commission and settlement effects for each affected SellerOrder/allocation |
| CNT-ACC-DELIVERY | Outbound (calls) | Requests shipment halt or return initiation |
| Event Bus | Outbound | Publishes `OrderCancelled`, `ReturnRequested` events |
| Outbox Table | Outbound | Persists event intent for recoverable asynchronous publication |

---

## 3. Behavior, Rules, and State

### 3.1 Cancellation Flow

1. Receive cancellation request (`order_id`, `reason`, `requester`).
2. Check with CMP-ORD-STATEMACHINE: is transition to `CancellationPending` allowed?
   - If not allowed (e.g., order already `Completed`, `Cancelled`, `Returned`) → reject with reason.
3. Transition order state to `CancellationPending`.
4. Execute eligible compensation steps independently only where their guards and the conservative UNKNOWN rule permit:
   - **Step A:** Coordinate institution-owned stock handling. Do not release a consumed or confirmed-order-linked reservation; any post-confirmation reversal/return rule requires institutional and product approval.
   - **Step B:** Void or refund payment via CMP-PAY-REFUND.
   - **Step C:** Where capture or external payment has already produced a seller-credit, commission or settlement effect, request the policy-authorized hold/reversal/adjustment through the Settlement/Ledger boundary; do not infer reversal from a refund alone.
   - **Step D:** Halt or return shipment via CNT-ACC-DELIVERY.
5. Record each step as succeeded, failed, skipped/not applicable or UNKNOWN with evidence and stable operation identity. Reconcile a possibly dispatched stock/financial effect before repeating it.
6. Only when all required steps are definitively settled under policy transition to `Cancelled`; failure, UNKNOWN or exhausted retries remains pending with escalation.
7. Publish `OrderCancelled` with `correlation_id` only on the final transition.

### 3.2 Return Flow

1. Receive return request (`seller_order_id` or `order_id`, `return_reason`, `line_items`).
2. Check transition to `ReturnPending` and eligibility under policy: Delivered and Completed are documented paths; Dispatched eligibility and rejected-return restoration remain OPEN, not silently removed or universally authorized.
3. Transition to `ReturnPending`.
4. Coordinate:
   - Initiate delivery return/collection via CNT-ACC-DELIVERY.
   - Trigger refund via CMP-PAY-REFUND (after delivery return confirmed, or immediately — per policy (OPEN: see idea.md §12, OWNER_UNASSIGNED)).
   - Reconcile any seller-credit, commission or settlement reversal/hold for the affected allocation through the Settlement/Ledger boundary; retain `UNKNOWN` until authoritative provider/ledger evidence exists.
5. Track each applicable return/collection, stock and refund operation with stable identity, evidence and succeeded/failed/skipped/UNKNOWN outcome. Reconcile possible dispatch before repeating; respect ADR-018 and approved dependencies. Only when all required steps are definitively settled under policy transition to `Returned`; otherwise remain pending/review and escalate.
6. Preserve both `ReturnRequested` and `OrderReturned`; the audit table proposes request notification on validated initiation and final notification on completion. Event-contract owners must resolve the inconsistent request timing before implementation.

### 3.3 Business Rules (§7.4)

- Cancellation is **not** deletion. It is a state transition with full audit trail.
- Each compensation step has an **independent outcome**. Independently safe progress may continue only if it does not violate ADR-018's conservative UNKNOWN guard or a dependency.
- **Partial compensation** is supported: a delivery halt failure can be tracked separately while other eligible, evidenced steps proceed; unresolved steps keep the operation pending and visible.
- The coordinator must track each step's result and persist it.
- Cancellation of an order in `PendingReservation` or `PendingPayment` is handled by CMP-ORD-SAGA compensation; CMP-ORD-CANCEL handles authorized cancellation/return workflows after `Confirmed`. Return eligibility for `Delivered` or `Completed` is policy-gated and is not rejected merely because cancellation is no longer available.

### 3.5 Lifecycle boundary

| Situation | Owning workflow | Financial rule |
|---|---|---|
| Pre-confirmation saga failure | CMP-ORD-SAGA | Scoped void/refund compensation only after payment outcome resolution; `UNKNOWN` blocks unsafe repetition |
| Confirmed-order downstream failure | Order/payment recovery path | No saga rollback of the committed order; retain the order and reconcile the payment exception and any independent effects |
| Authorized cancellation after confirmation | CMP-ORD-CANCEL | Apply cancellation policy, then invoke CMP-PAY-REFUND and any Settlement/Ledger hold/reversal independently |
| Authorized return request | CMP-ORD-CANCEL return flow | Evaluate return eligibility separately from cancellation; delivery, refund timing, partial amount, and post-settlement adjustment remain policy-gated |

### 3.4 Compensation Decision Table (§7.5)

| Order State at Cancel Request | Reservation Action | Payment / credit / settlement action | Delivery Action |
|---|---|---|---|
| PendingReservation / PendingPayment | Via saga compensation | Via saga compensation, including any known credit/settlement effect | N/A |
| Confirmed (before dispatch) | Institution-approved post-confirmation handling; do not release confirmed-linked/consumed hold | Void (pre-capture) or refund where authorized and outcome known; hold/reverse any seller-credit or settlement effect per policy | Cancel shipment creation |
| Processing / Dispatched | Institution-approved cancellation/return handling; do not release confirmed-linked/consumed hold | Refund where authorized and outcome known; reconcile credit, commission and settlement reversal independently | Request delivery return where eligible |
| Delivered | N/A | Refund and any approved post-settlement adjustment | N/A (already delivered) |

---

## 4. Data and Side Effects

| Data Item | Owned By | Description |
|---|---|---|
| Cancellation / Return record | CMP-ORD-CANCEL | `{order_id, request_type, requester, reason, step_outcomes[], final_state, created_at}` |
| Step outcome records | CMP-ORD-CANCEL | Per-step result: `{step, status, attempt_count, last_error}` |
| `OrderCancelled` / `ReturnRequested` / `OrderReturned` events | Outbox → Event Bus | Final events on final transition; request-event timing is proposed at validated initiation and remains a contract decision |

- **Transaction boundary:** Cancellation record creation + order state transition to `CancellationPending` are atomic. Each compensation step outcome is written independently as it completes.
- **Idempotency:** Deduplicate the same authorized request/operation and applicable order/seller/line scope, without treating a distinct authorized cancellation or return as a duplicate. Exact request key and multi-return eligibility remain OPEN.

---

## 5. Failure, Security, and Operations

### 5.1 Failure Modes

| Failure | Response |
|---|---|
| State machine rejects cancellation (invalid transition) | Return rejection error with current state and reason |
| ACCore seller unreachable during an eligible stock operation | If possibly dispatched, preserve UNKNOWN and reconcile before retry; escalate per policy. Other work proceeds only if independently safe under ADR-018. |
| Payment refund fails or response is lost | Distinguish definitive failure from UNKNOWN; reconcile before repeating a possible financial effect and escalate per policy |
| Delivery halt fails (shipment already moving) | Log and alert; independently safe steps may proceed but unresolved required work prevents final cancellation |
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
| Cancel order in `Confirmed` state | Coordinate approved stock handling and eligible void/refund and delivery steps; only settled required steps permit Cancelled |
| Cancel order in `Dispatched` state | Coordinate eligible payment and delivery return under policy; no final Cancelled while required work is unresolved |
| Cancel already-Cancelled order | Rejection with `InvalidStateTransition` |
| Payment refund fails during cancellation | Operational alert raised; order stays CancellationPending; retry scheduled |
| Delivery return fails | Log + alert; cancellation proceeds for other steps |
| Idempotent cancellation request | Existing cancellation record returned; no duplicate steps executed |
| Return request on `Delivered` order | Coordinate policy-eligible return and refund; unresolved or UNKNOWN required steps remain pending/review, with `Returned` only after settlement |

### 6.1 Partial Refund Edge Case

> [!WARNING]
> Partial and full refund eligibility and amounts remain **UNKNOWN** (§12). Preserve both options for approved policy; do not assume an automatic full refund or execute an unapproved partial refund.

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
