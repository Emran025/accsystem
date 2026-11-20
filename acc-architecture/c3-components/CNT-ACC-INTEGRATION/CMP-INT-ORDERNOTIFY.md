# CMP-INT-ORDERNOTIFY — Order Event Dispatcher

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-INT-ORDERNOTIFY |
| **Parent Container** | CNT-ACC-INTEGRATION (Institution Integration Gateway — ACCSystem) |
| **Purpose** | Consumes OrderConfirmed and OrderCancelled events from the Event Bus and dispatches them to the relevant institution ACCore instances via CNT-ACR-CONNECTOR, ensuring the seller (and buyer for B2B) are notified of order outcomes. |
| **Scope Boundary** | Event routing and reliable dispatch only. Does NOT own order state or modify the order. |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-EVENTBUS | Inbound | Subscribes to OrderConfirmed, OrderCancelled, ReturnRequested events |
| CNT-ACR-CONNECTOR | Outbound | Sends order event to relevant institution ACCore via IF-ACC-ORDER-CONFIRM channel |
| CNT-ACC-INSTREG | Outbound | Looks up institution connector endpoint and auth credentials |
| CNT-ACC-AUDIT | Outbound | Logs dispatch attempts and results |

---

## 3. Behavior, Rules, and State

- For each OrderConfirmed event, identifies the seller institution (from order.institution_id) and sends the order notification
- For B2B orders, also notifies the buyer institution if present
- Delivery uses Outbox/Inbox pattern: dispatch logged atomically; retried until acknowledged
- Idempotency key: event_id + institution_id — same event not dispatched twice to same institution

**Business rules:**
- An institution is only notified of orders where it is seller or buyer — never shown cross-institution data
- Dispatch is non-blocking: failure does not roll back the order

---

## 4. Data and Side Effects

| Data Item | Owned By |
|---|---|
| Dispatch log record | CMP-INT-ORDERNOTIFY |
| Outbox entries for dispatch | Shared Outbox |

Does NOT own: Order records, institution records.

---

## 5. Failure Modes and Resilience

| Failure | Response |
|---|---|
| ACCore connector unavailable | Retry with configured backoff and the same idempotency key; when the configured recovery policy is exhausted, preserve the message in DLQ and alert Operations. |
| Duplicate OrderConfirmed event | Idempotency key check prevents double dispatch |
| Institution not found in registry | Log error; skip dispatch; alert ops |

---

## 6. Security

- CONFIRMED (idea.md §9): Institution isolation — only relevant institution receives its own order data
- Event payload must not expose other institution's data
- TLS + service-to-service auth for dispatch — CONFIRMED (idea.md §4.3)

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "Integration Health — الرسائل الفاشلة" monitored |
| Risk | ACCore unavailability delays seller notification; order remains Confirmed regardless |


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Order delivery notification | `OrderConfirmed` event received from Orders container | Outbound notification dispatched to seller institution webhook |
| Institution endpoint timeout | Seller endpoint unresponsive | Notification retried with exponential backoff (up to 5 attempts); queued in Outbox |
| Duplicate delivery event | Re-delivery of already dispatched notification event | Idempotency key prevents duplicate HTTP webhook dispatch to institution |
