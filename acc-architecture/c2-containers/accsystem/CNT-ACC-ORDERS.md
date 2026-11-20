# CNT-ACC-ORDERS — Order Management

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-ORDERS |
| **Purpose** | Manages the full lifecycle of marketplace orders — creation, state transitions, multi-seller splitting, saga orchestration, commercial snapshot immutability, and cancellation/return coordination. |
| **Scope Boundary** | Owns the central order record and its lifecycle. Does NOT own payment logic (CNT-ACC-PAYMENT) or delivery logic (CNT-ACC-DELIVERY). Coordinates but does not execute those domains. |

CONFIRMED (idea.md §3.1): "Order Management — إنشاء الطلب، إدارة حالاته، تقسيمه حسب البائع عند الحاجة، تنسيق الأحداث."
CONFIRMED (idea.md §14, ADR-007): "Order Domain ينسق الدفع والتوصيل ولا يمتلك تفاصيل تنفيذهما."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-CART | Inbound | Triggers order creation on checkout completion |
| CNT-ACC-PAYMENT | Bidirectional (via Saga) | Saga triggers payment authorization; receives PaymentAuthorized/Failed events |
| CNT-ACC-INTEGRATION | Bidirectional | Sends reservation requests; receives ACCEPTED/REJECTED/UNKNOWN and authoritative EXPIRED outcomes; UNKNOWN is reconciled before payment or release |
| CNT-ACC-DELIVERY | Outbound | Triggers shipment creation after OrderConfirmed |
| CNT-ACC-LICENSE | Outbound (event) | OrderConfirmed event triggers license activation for software products |
| CNT-ACC-NOTIFICATIONS | Outbound | Publishes order status events for buyer/seller notification |
| CNT-ACC-EVENTBUS | Bidirectional | Publishes OrderConfirmed, OrderCancelled; subscribes to PaymentAuthorized/Failed |
| CNT-ACC-AUDIT | Outbound | Logs all order state transitions |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Data store | UNKNOWN | OWNER_UNASSIGNED |
| Saga implementation | CONFIRMED (idea.md §14, ADR-013) | Orchestration-based Saga pattern via CMP-ORD-SAGA |
| Outbox | CONFIRMED (idea.md §6.5) | Transactional Outbox for event publication atomicity |

---

## 4. Data Owned

- Parent Order: `{order_id, buyer_id, status, created_at, snapshot}`
- Seller Orders: `{seller_order_id, order_id, institution_id, items, status}`
- Order Lines: `{line_id, listing_id, quantity, unit_price_snapshot, description_snapshot}`
- Saga state records
- Cancellation/return records

CONFIRMED (idea.md §8.3): Immutable commercial snapshot written at order confirmation.
CONFIRMED (idea.md §5.2): Reference IDs — order_id, seller_order_id, correlation_id used in all events.

---

## 5. Interfaces

- **IF-ACC-ORDER-CREATE** (provider): Order creation API — consumers: CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE, CNT-ACC-APIGATEWAY
- Publishes: OrderConfirmed, OrderCancelled events via IF-ACC-EVENT-ENVELOPE

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| ACCore definitive reservation rejection | Release only confirmed accepted holds; no payment; order fails. Timeout/lost response/circuit-open after possible dispatch → `ReservationUnknown`; query/reconcile; no payment or release solely from elapsed time. |
| Payment definitive decline | Release only confirmed reservations; order fails. Timeout/lost response → `PaymentUnknown`; reconcile provider before retry, void, or release. |
| Confirmation write fails | Retry local commit if no commit; otherwise query local snapshot/outbox and external states, then resume or compensate only on definitive evidence; never blanket void/refund. |
| Delivery creation fails | Order remains Confirmed; delivery state → PendingDelivery; retry |

CONFIRMED (idea.md §7.5): Full failure mode table with responses.

---

## 7. Security

- Order access scoped to buyer_id and institution_id — CONFIRMED (idea.md §9)
- No cross-institution order data exposure — CONFIRMED (idea.md §9)
- All order state transitions logged in audit trail — CONFIRMED (idea.md §9)
- correlation_id propagated through all events — CONFIRMED (idea.md §11)

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "معدل نجاح Checkout، الطلبات المؤكدة، معدل فشل الحجز" |
| Risk | Multi-seller cart complexity (open decision §12) — OWNER_UNASSIGNED |
| Saga monitoring | Saga step durations and timeouts must be monitored for stuck sagas |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-ORD-SAGA — Order Saga Orchestrator
- CMP-ORD-STATEMACHINE — Order State Machine
- CMP-ORD-MULTISELLER — Multi-Seller Order Splitter
- CMP-ORD-SNAPSHOT — Commercial Snapshot Service
- CMP-ORD-CANCEL — Cancellation & Return Coordinator

See: `c3-components/CNT-ACC-ORDERS/`
