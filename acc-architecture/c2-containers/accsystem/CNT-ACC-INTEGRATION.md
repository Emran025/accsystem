# CNT-ACC-INTEGRATION — Institution Integration Gateway

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-INTEGRATION |
| **Purpose** | Manages all asynchronous and synchronous integration between ACCSystem and ACCore institution instances. Receives product publication events, routes reservation requests, dispatches order confirmation events, and ensures reliable at-least-once delivery with idempotency. |
| **Scope Boundary** | Owns integration state, message routing, sync status, and connector key mappings. Does NOT own product catalog data (CNT-ACC-CATALOG) or order state (CNT-ACC-ORDERS). |

CONFIRMED (idea.md §3.1): "Institution Integration — موصلات ACCore، استقبال الأحداث، التحقق من التوقيع، التسليم وإعادة المحاولة."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-CONNECTOR (via IF-ACR-PUBLISH-EVENT) | Inbound | Receives product publication events from ACCore institutions |
| CNT-ACR-CONNECTOR (via IF-ACR-RESERVATION-RESP) | Inbound | Receives reservation outcomes via response/trusted query or optional approved callback; statuses include ACCEPTED, REJECTED, UNKNOWN and authoritative EXPIRED |
| CNT-ACC-ORDERS / CMP-ORD-SAGA | Inbound (via IF-ACC-RESERVE-SAGA) | Receives reservation requests to relay to ACCore |
| CNT-ACC-CATALOG | Outbound | Sends validated product publication for listing processing |
| CNT-ACC-INSTREG | Outbound | Validates institution identity and integration configuration |
| CNT-ACC-EVENTBUS | Bidirectional | Publishes and subscribes to domain events |
| CNT-ACC-AUDIT | Outbound | Logs all integration events and failures |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Integration pattern | CONFIRMED (idea.md §6.5) | Outbox/Inbox pattern; at-least-once delivery; idempotency keys |
| Transport | CONFIRMED (idea.md §4.3) | HTTPS/TLS; service-to-service auth (OAuth 2.0) |
| Event format | CONFIRMED (idea.md §6.4) | Unified event envelope with event_id, event_type, correlation_id, idempotency_key |

---

## 4. Data Owned

- Integration sync state per institution per product
- Message dispatch log and retry counters
- Connector key mappings and ID translations (platform_institution_id ↔ ACCore institution identifier)
- Processed message store (Inbox) for deduplication

CONFIRMED (idea.md §3.1): "حالة المزامنة، سجلات الرسائل، مفاتيح الربط وخرائط المعرفات."

---

## 5. Interfaces

- **IF-ACR-PUBLISH-EVENT** (consumer): Receives publication events from CNT-ACR-CONNECTOR
- **IF-ACR-RESERVATION-RESP** (consumer): Receives reservation responses from CNT-ACR-CONNECTOR
- **IF-ACC-RESERVE-SAGA** (provider): Accepts reservation requests from CNT-ACC-ORDERS; relays to CNT-ACR-CONNECTOR
- **IF-ACC-ORDER-CONFIRM** (logical provider): Delivers recipient-scoped confirmations to the ACCore connector using the ADR-015 selected channel; other event schemas/channels remain open
- **IF-ACC-EVENT-ENVELOPE** (bidirectional): Publishes/subscribes via CNT-ACC-EVENTBUS

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| ACCore connector unavailable | Retry with configured backoff using the same idempotency_key; when the configured recovery policy is exhausted, preserve the message in DLQ and alert Operations. For a reservation command, query ACCore before replay or release. |
| Duplicate publication event received | Inbox check deduplicates; idempotent processing — CONFIRMED (idea.md §6.5) |
| Signature validation failure on incoming event | Reject and log security event; alert ops — CONFIRMED (idea.md §9) |
| Reservation response timeout | CMP-INT-RESERVATION records UNKNOWN after possible dispatch and reconciles by known reservation ID or stable request key using an agreed available channel; otherwise waits and escalates. Timeout is not a failure signal |

---

## 7. Security

- CONFIRMED (idea.md §9): Webhook signature verification on all inbound events from ACCore
- CONFIRMED (idea.md §4.3): TLS + service-to-service OAuth for all outbound calls to ACCore
- CONFIRMED (idea.md §9): Institution identity verified via platform_institution_id on every event
- CONFIRMED (idea.md §9): No direct database access to ACCore

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Event delivery success rate, reservation response latency, DLQ depth. Targets: UNKNOWN |
| Monitoring | CONFIRMED (idea.md §11): "Integration Health — آخر مزامنة لكل مؤسسة، الرسائل الفاشلة، زمن استجابة ACCore" |
| Risk | ACCore unavailability cascades to checkout flow; circuit breaker at CMP-INT-RESERVATION |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-INT-GATEWAY — Integration Gateway (inbound event routing, signature validation)
- CMP-INT-PUBLICATION — Product Publication Worker
- CMP-INT-RESERVATION — Reservation Relay
- CMP-INT-ORDERNOTIFY — Order Event Dispatcher

See: `c3-components/CNT-ACC-INTEGRATION/`
