# CNT-ACC-EVENTBUS — Event Bus / Message Broker

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-EVENTBUS |
| **Purpose** | Shared asynchronous messaging infrastructure for all ACCSystem bounded-context services. Provides durable, ordered, at-least-once event delivery with DLQ and retry policies. |
| **Scope Boundary** | Infrastructure component only — no business logic. Owned by the platform; accessed by all services via published contracts. |

CONFIRMED (idea.md §6.5, §10.1): "Message Broker / Event Bus — قنوات/Topics حسب المجال، مع DLQ وسياسات إعادة محاولة."

---

## 2. Collaborators

All ACCSystem domain services publish to and/or subscribe from the Event Bus. Key consumers:
- CNT-ACC-ORDERS, CNT-ACC-PAYMENT, CNT-ACC-DELIVERY, CNT-ACC-INTEGRATION, CNT-ACC-LICENSE, CNT-ACC-NOTIFICATIONS

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Broker technology | UNKNOWN | Kafka, RabbitMQ, cloud-native (SNS/SQS, Pub/Sub) — not specified. OWNER_UNASSIGNED. |
| Topic/channel model | CONFIRMED (idea.md §10.1) | Channels per domain with DLQ |
| Event format | CONFIRMED (idea.md §6.4) | Unified event envelope with event_id, event_type, occurred_at, producer, institution_id, aggregate_id, correlation_id, idempotency_key |

---

## 4. Data Owned

- Event messages (transient/durable per topic configuration)
- DLQ contents
- Consumer group offsets

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Event Bus unavailable | Outbox pattern at producer side holds events until bus recovers — CONFIRMED (idea.md §6.5) |
| Consumer lag | DLQ collects failed messages; consumer lag monitored — CONFIRMED (idea.md §11) |
| Message ordering violation | Partition key (order_id, seller_order_id) ensures order within partition — CONFIRMED (idea.md §6.5) |

---

## 6. Security

- CONFIRMED (idea.md §9): TLS for all connections; service-to-service auth for publish/subscribe access

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "تأخر الرسائل، حجم DLQ" monitored |

---

## 8. Interface

- **IF-ACC-EVENT-ENVELOPE** (provider): Event Bus interface. Consumers: CNT-ACC-ORDERS, CNT-ACC-PAYMENT, CNT-ACC-DELIVERY, CNT-ACC-INTEGRATION, CNT-ACC-LICENSE, CNT-ACC-NOTIFICATIONS

---

## 9. C3 Disposition

**EXCEPTION:** Shared messaging infrastructure — components are defined by the broker technology, not by business component decomposition. Cross-cutting patterns documented in `supporting-views/interface-contracts.md` and `supporting-views/resilience-observability.md`.
