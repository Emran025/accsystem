# CNT-ACR-OUTBOX — Outbox / Inbox (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-OUTBOX |
| **Purpose** | Provides transactional outbox and inbox infrastructure within ACCore for recoverable at-least-once delivery attempts and idempotent business effects between ACCore and ACCSystem. Duplicate delivery is possible. |
| **Scope Boundary** | Infrastructure component — no business logic. Outbox: queues outbound events atomically in the same DB transaction as business state changes. Inbox: stores received events for idempotent processing. |

CONFIRMED (idea.md §4.1): "Outbox / Inbox — ضمان تسجيل الأحداث الصادرة ومعالجة الواردة بطريقة قابلة لإعادة المحاولة دون تكرار."
CONFIRMED (idea.md §6.5): "استخدم Transactional Outbox في ACCore وACCSystem لتجنب حفظ المعاملة دون نشر الحدث أو العكس."

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-CONNECTOR | Bidirectional | Connector reads Outbox; writes received events to Inbox |
| All ACCore modules | Inbound | Write outbound events to Outbox within their DB transactions |

---

## 3. Data Owned

- Outbox table: `{event_id, event_type, payload, status, created_at, attempt_count}`
- Inbox table: `{event_id, idempotency_key, processed_at}`

---

## 4. Failure Modes

| Failure | Response |
|---|---|
| ACCSystem unreachable | Events remain in Outbox; retried with backoff on reconnect — CONFIRMED (idea.md §4.2) |
| Duplicate incoming event | Inbox check by idempotency_key prevents double processing |

---

## 5. C3 Disposition

**EXCEPTION:** Transactional messaging infrastructure pattern. No business-logic components to decompose. Pattern documented in `supporting-views/resilience-observability.md`.


---

## 6. Security and Trust

- **Access Restriction:** Outbox table readable exclusively by authorized local dispatcher process; direct external network access blocked.
- **Payload Privacy:** Outbound event payloads containing sensitive institutional data are encrypted before persistence.

---

## 7. Technology Rationale and Decision Status

- **Architecture Pattern:** Transactional Outbox per proposed ADR-005 supports durable local intent and at-least-once delivery attempts without distributed 2PC. DLQ and unresolved recovery do not imply completed delivery.

---

## 8. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Dispatcher process crash | Unprocessed records with `PENDING` status picked up by replacement worker on startup |
| ACCSystem endpoint unreachable | Exponential backoff retry with jitter; records retained in outbox table until acknowledged |
| Poison pill message format | Routed to Dead-Letter Outbox table after max retry count; operational alert triggered |

---

## 9. Open Risks and Decisions

- Polling interval overhead vs Change Data Capture (Debezium/CDC) — `OPEN` (`OWNER_UNASSIGNED`). Action: evaluate DB transaction log volume.
