# CNT-ACC-NOTIFICATIONS — Notifications

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-NOTIFICATIONS |
| **Purpose** | Dispatches notifications to users across configured channels (in-app, push, email, SMS — channels: UNKNOWN) in response to domain events such as order status changes, payment updates, and license events. |
| **Scope Boundary** | Owns notification templates, delivery state, and channel configurations. Does NOT own the events that trigger notifications. |

CONFIRMED (idea.md §3.1): "Notifications — إرسال إشعارات داخل التطبيق ورسائل القنوات المفعلة."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-EVENTBUS | Inbound | Subscribes to domain events (OrderConfirmed, PaymentFailed, ShipmentDelivered, LicenseExpiring, etc.) |
| External notification channels | Outbound | Dispatches messages via configured providers (UNKNOWN: specific providers) |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Channels | UNKNOWN | In-app, push, email, SMS — not all confirmed. OWNER_UNASSIGNED. |
| Provider | UNKNOWN | Third-party notification provider not specified |

---

## 4. Data Owned

- Notification templates per event type
- Delivery status per notification
- User channel preferences (ASSUMPTION)

---

## 5. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Channel provider unavailable | Retry with backoff; DLQ for undelivered notifications |
| Template not found for event | Log error; skip notification; alert ops |

---

## 6. Security

- No sensitive business data in notification payloads — ASSUMPTION
- Channel credentials stored securely, not in code

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| Availability | Non-critical path; notifications are informational, not transactional |
| SLI | Notification delivery rate. Targets: UNKNOWN |

---

## 8. C3 Disposition

**EXCEPTION:** Notification dispatch service; complexity low relative to other domains. C3 deferred to Phase 4+ planning. Revisit trigger: when multi-channel orchestration, preference management, or templating complexity grows.
