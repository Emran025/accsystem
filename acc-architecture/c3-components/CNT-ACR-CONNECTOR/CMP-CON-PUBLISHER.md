# CMP-CON-PUBLISHER — Product Publication Client

**Component ID:** CMP-CON-PUBLISHER  
**Container:** CNT-ACR-CONNECTOR  
**System:** SYS-ACCORE (per-institution instance)  
**C4 Level:** C3 — Component  
**Status:** DRAFT | Evidence: idea.md §4.1, §4.3, ADR-005

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | CMP-CON-PUBLISHER |
| **Name** | Product Publication Client |
| **Container** | CNT-ACR-CONNECTOR |
| **Responsibility** | Reads product publication requests from ACCore's Outbox (CNT-ACR-OUTBOX), sends them to ACCSystem's Integration Layer (CNT-ACC-INTEGRATION) via IF-ACR-PUBLISH-EVENT, with retry and idempotency guarantees. Does NOT validate content — validation is CMP-CAT-VALIDATION's responsibility. |

---

## 2. Collaborators

| Collaborator | Direction | Interface / Event | Purpose |
|---|---|---|---|
| CNT-ACR-OUTBOX | Inbound read | Outbox poll / change-data-capture | Source of publication requests written by ACCore product management |
| CNT-ACR-PRODUCTMASTER | Inbound (indirect) | Via CNT-ACR-OUTBOX | Product data included in publication payload |
| CNT-ACC-INTEGRATION | Outbound | IF-ACR-PUBLISH-EVENT (HTTPS POST or message) | Delivers publication payload to ACCSystem |
| ACCore internal Outbox | Read/Write | Outbox pattern | Marks messages as SENT after successful delivery |

---

## 3. Data Owned

**No persistent entities owned beyond Outbox interaction.**

**Outbox Message (owned by CNT-ACR-OUTBOX, read by this component):**
```
outbox_id           UUID (PK)
message_type        string ("ProductPublication")
payload             JSON {
                      seller_product_id,
                      institution_id,
                      version,
                      title,
                      description,
                      price,
                      currency_code,
                      availability,
                      media_refs[],
                      category_id
                    }
status              enum {PENDING, SENT, FAILED}
created_at          timestamp
sent_at             timestamp (nullable)
retry_count         integer
```

---

## 4. Behavior / Rules / State

### Processing Loop
1. Poll CNT-ACR-OUTBOX for `PENDING` messages of type `ProductPublication` (or use CDC — ASSUMPTION: polling; CDC requires additional infrastructure)
2. For each message: prepare IF-ACR-PUBLISH-EVENT request
3. Send to CNT-ACC-INTEGRATION endpoint
4. On contract-valid HTTP 200/202 acceptance or recorded idempotent outcome: mark Outbox message as `SENT`; ID/receipt timing remains open per IF-ACR-PUBLISH-EVENT. Any 201 usage needs contract agreement.
5. On failure: increment retry_count; exponential backoff; mark `FAILED` after N retries

### Idempotency
- Idempotency key sent in HTTP header: `Idempotency-Key: {institution_id}:{seller_product_id}:{version}`
- ACCSystem must honor this key — duplicate requests with same key are no-ops
- Local: mark SENT only after a contract-valid ACK. A crash or lost ACK can cause resend with the same event ID and scoped key; receiver guards prevent repeated business effects, not physical resend.

### Does NOT:
- Validate product content (not its responsibility)
- Transform prices or currency codes
- Access ACCSystem internal state directly

---

## 5. Failure Modes

| Failure | Detection | Mitigation |
|---|---|---|
| CNT-ACC-INTEGRATION unreachable | Connection timeout | Retry with configured backoff; retain an explicit delivery state and reconcile after retry exhaustion. No fixed schedule or attempt count is asserted. |
| ACCSystem returns 4xx | HTTP 4xx | Definitive malformed/forbidden input is FAILED and corrected by the institution; 429 uses policy-governed backoff; permitted auth renewal is retried; dependency/unavailability remains retryable or UNKNOWN, not definitive rejection. |
| ACCSystem returns 5xx | HTTP 5xx | Retry (transient failure) |
| Duplicate send (crash after send, before SENT mark) | Idempotency key | ACCSystem ignores duplicate; Outbox remains PENDING → re-sent → idempotent |
| Outbox poll failure | DB connection error | Log error; resume under configured Operations-approved retry policy — Outbox is on local ACCore DB |
| ACCSystem version mismatch | 422 response | UNKNOWN — versioning policy between ACCore and ACCSystem not defined |

---

## 6. Security

| Concern | Control |
|---|---|
| Authentication to ACCSystem | Policy-selected OAuth 2.0 Client Credentials or mTLS under ADR-015; the authenticated principal is bound to the institution. Exact method is an onboarding/security gate. |
| Token renewal | If OAuth 2.0 Client Credentials is selected, CMP-CON-PUBLISHER caches the access token and refreshes it before expiry; mTLS mode follows its certificate lifecycle |
| Credential rotation | The selected credential/certificate is rotated through the approved onboarding and platform-security process; no code changes are implied |
| Payload integrity | HTTPS only; no HTTP fallback |
| Credential storage | Selected OAuth client secret or mTLS key/certificate reference is stored in ACCore secure configuration (ASSUMPTION — secret manager or equivalent); API keys are not a contract mechanism |
| Principle of least privilege | CMP-CON-PUBLISHER has read access to Outbox only; cannot write to ACCore product data |

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| Monitoring | Track Outbox queue depth, FAILED message count, retry rates — leading indicator of integration health |
| Manual replay | Admin command to re-process FAILED Outbox messages after root cause fix |
| Rate limiting | ACCSystem may impose rate limits on institution publication; exponential backoff absorbs burst |

---

## 8. Traceability

| Claim | Evidence |
|---|---|
| Outbox pattern for reliable integration | CONFIRMED (idea.md §4.3, ADR-005 — Outbox/Inbox + idempotency) |
| ACCore → ACCSystem via IF-ACR-PUBLISH-EVENT | CONFIRMED (interfaces.json — IF-ACR-PUBLISH-EVENT) |
| Validation at ACCSystem side only | CONFIRMED (ADR-004 — ACCSystem controls catalog quality) |
| Auth mechanism for inter-system calls | ASSUMPTION — not specified in idea.md §5 beyond "secure API" |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Institutional product publication | ACCore user publishes product | Outbox record read; OAuth 2.0 CC token obtained; payload posted to ACCSystem |
| Token expiry during publication | Access token expired | OAuth client refreshes token via client credentials grant and retries request |
| ACCSystem endpoint unreachable | ACCSystem returns HTTP 502/503 | Outbox record retried with exponential backoff; local product remains pending |
