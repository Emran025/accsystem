# CMP-PAY-ADAPTER — Provider Adapter

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-PAY-ADAPTER |
| **Parent Container** | CNT-ACC-PAYMENT (Payment Orchestration — ACCSystem) |
| **Purpose** | Adapts calls from CMP-PAY-ORCHESTRATOR and CMP-PAY-REFUND to the external payment provider's API. Handles all provider-specific request/response translation, signature validation for inbound webhooks, and circuit breaking for outbound provider calls. |
| **Scope Boundary** | Owns provider-API translation logic only. Does NOT store payment transaction state (CMP-PAY-ORCHESTRATOR does), does NOT make business decisions about whether to authorize or capture, and does NOT publish domain events. |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CMP-PAY-ORCHESTRATOR | Inbound (called by) | Requests authorization, capture, void operations |
| CMP-PAY-REFUND | Inbound (called by) | Requests refund operations |
| EXT-PAYMENT-PROVIDER | Outbound (calls) | Sends API requests; receives synchronous responses and inbound webhooks |
| CMP-PAY-ORCHESTRATOR (webhook relay) | Outbound (relays) | Forwards validated and translated webhook payloads back to Orchestrator |

**Interface involved:** `IF-ACC-PAYMENT-WEBHOOK` — CMP-PAY-ADAPTER is the first receiver of inbound webhook calls from EXT-PAYMENT-PROVIDER. It validates provider signatures before passing the payload onward. CONFIRMED (idea.md §9 — "Webhooks")

---

## 3. Behavior, Rules, and State

### 3.1 Operations Provided

| Operation | Input | Output |
|---|---|---|
| `authorize(order_id, amount, currency, payment_method_ref, idempotency_key)` | Internal domain request | `{provider_auth_id, status, raw_response}` |
| `capture(provider_auth_id, amount, idempotency_key)` | Internal domain request | `{provider_capture_id, status, raw_response}` |
| `void(provider_auth_id, idempotency_key)` | Internal domain request | `{status, raw_response}` |
| `refund(provider_capture_id, amount, idempotency_key)` | Internal domain request | `{provider_refund_id, status, raw_response}` |
| `validateWebhook(headers, body)` | Raw HTTP webhook | `{valid: bool, translated_event}` |

### 3.2 Translation Rules

- Provider-specific field mapping is encapsulated in this component; callers use only the internal domain model.
- All provider error codes are translated to a canonical set: `DECLINED`, `INSUFFICIENT_FUNDS`, `PROVIDER_ERROR`, `TIMEOUT`, `INVALID_CARD`, `FRAUD_SUSPECTED`.
- PROPOSAL: A `ProviderProfile` configuration record (per supported provider) holds base URLs, authentication scheme, webhook secret, and field mapping rules. Switching provider requires updating the profile, not code.

### 3.3 Circuit Breaker

- A per-provider circuit breaker (PROPOSAL: half-open/open/closed states) wraps all outbound API calls.
- Open threshold: configurable policy key `payment.cb.open_policy`, owned by Operations/SRE and calibrated with provider availability/recovery evidence; no initial count is asserted.
- When open: fail fast with `PROVIDER_CIRCUIT_OPEN`; the orchestrator records an operational/provider-unavailable or UNKNOWN outcome according to whether provider state is known, and never treats circuit state alone as proof that no financial effect exists.
- Metrics: circuit state transitions exposed as operational metrics. PROPOSAL.

### 3.4 Idempotency at Provider Level

- Provider idempotency keys are derived from the internal idempotency key passed by callers.
- If the provider returns an idempotent response for a repeated request, the adapter returns the same translated result.

---

## 4. Data Owned

**CMP-PAY-ADAPTER does NOT own or persist payment state.** It is a stateless translation layer with one exception:

| Item | Purpose | Lifetime |
|---|---|---|
| In-memory / short-lived circuit breaker state | Tracks provider health | Process lifetime; not persisted |
| Provider profile config | Mapping rules, secrets references | Loaded from config store; not in component DB |

**NOT owned:** payment transactions, refund records, outbox entries — all owned by other components.

---

## 5. Failure Modes and Resilience

| Failure | Response Strategy |
|---|---|
| Provider API timeout | Return `TIMEOUT`/UNKNOWN with provider reference status; circuit policy records health, but the orchestrator reconciles before retry, void, capture, or release |
| Provider returns 5xx | Return `PROVIDER_ERROR` with outcome UNKNOWN if a financial effect may have occurred; circuit breaker records health. Reconcile provider state before any financial retry, void, capture or dependent release; locally proven non-dispatch is distinct. |
| Webhook signature invalid | Return `{valid: false}`; CMP-PAY-ORCHESTRATOR discards; security alert emitted |
| Provider returns ambiguous status | Return `PROVIDER_ERROR` with UNKNOWN outcome; record appropriately protected evidence and have CMP-PAY-RECONCILIATION resolve before repeating effects |
| Circuit breaker open | No new network call; callers receive `PROVIDER_CIRCUIT_OPEN`. The orchestrator records local non-dispatch only when durable evidence proves no command was sent; otherwise it records UNKNOWN and reconciles. |
| Provider credential expiry | UNKNOWN — secret rotation mechanism not defined; consequence: all provider calls fail. Owner: OWNER_UNASSIGNED; revisit trigger: secret management design |

---

## 6. Security Responsibilities

| Concern | Responsibility |
|---|---|
| Webhook signature validation | Validates provider HMAC/signature on every inbound webhook before any state mutation downstream |
| Credential isolation | Provider API keys referenced via external secret store; never logged or embedded in payloads |
| TLS enforcement | All outbound calls to EXT-PAYMENT-PROVIDER over TLS. CONFIRMED (idea.md §9) |
| PCI scope | Adapter never receives or stores raw card numbers; uses provider-issued tokens/references |
| Replay protection on webhooks | Passes `provider_event_id` to CMP-PAY-ORCHESTRATOR, which durably records receipt/claim state. A webhook is ACKed only after atomic effect-and-dedup completion or durable acceptance with owned crash recovery; in-progress, completed duplicate, and conflicting records remain distinct and provider retry behavior is contract-gated. |

---

## 7. Operational Concerns

### 7.1 SLIs

| Indicator | Target (PROPOSAL) |
|---|---|
| Provider call success rate (excluding declined) | `provider.sli.success_rate`; target requires provider/SRE evidence |
| Outbound latency | `provider.sli.latency`; target requires provider/SRE evidence |
| Circuit breaker open frequency | `provider.alert.cb_frequency`; threshold requires SRE baseline evidence |

### 7.2 Scaling

- Stateless; horizontal scaling. PROPOSAL.
- Provider rate limits must be respected; UNKNOWN: specific rate-limit values depend on provider contract. Owner: OWNER_UNASSIGNED.

### 7.3 Known Risks

| Risk | Consequence | Mitigation |
|---|---|---|
| Provider API changes | Mapping rules break silently | Contract test suite per provider profile; alert on unexpected response shape |
| Single provider assumed | No fallback if provider is down | Phase 6 scope: multi-provider adapter profiles |
| Webhook HMAC secret rotation | Brief validation failures during rotation | Support dual-secret validation window (new + old secret). PROPOSAL |

---

## 8. Unknowns, Traceability, and ADR References

| Item | Status | Owner / Action |
|---|---|---|
| Supported payment provider(s) identity | UNKNOWN — provider selection is an open decision (idea.md §12) | Product/commercial team; define before Phase 3 |
| Provider-specific rate limits | UNKNOWN | Confirm during provider onboarding |
| Circuit breaker thresholds | Configurable policy keys | Operations/SRE; approve after provider and recovery evidence before production |

**ADR References:** ADR-005, ADR-007

**Requirement References:** §7.2, §7.5, §9, §12 (payment model open decision)
