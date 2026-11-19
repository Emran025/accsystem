# DF-BOOKING-001 — Shipment booking and outcome persistence

## Purpose, scope and participants

This illustrative dynamic/data flow traces a merchant operator's shipment request through `CNT-WEB`, `CNT-API`, external `EXT-CARRIER`, and persistence `CNT-DB`. It describes the known high-level path only. It does not claim that the carrier protocol, transaction model, status lifecycle, or synchronous/asynchronous behavior has been confirmed.

Participants: `ACT-MERCHANT`, `CNT-WEB`, `CNT-API`, `CMP-API-VALIDATION`, `CMP-API-BOOKING`, `CMP-API-REPOSITORY`, `EXT-CARRIER`, and `CNT-DB`. Related function: `FN-ORDER-001`; integration: `IF-CARRIER-001`.

## Normal path (sample behavior)

1. The merchant operator enters origin, destination and parcel dimensions in `CNT-WEB` and submits the request. **Open:** request ID, authentication context, field units and client-side validation are not defined.
2. `CNT-WEB` sends the shipment data to `CNT-API`. **Proposed:** use HTTPS/JSON as shown in the sample context. **Open:** versioning, authorization, payload schema, correlation ID and duplicate-submit behavior.
3. `CMP-API-VALIDATION` applies `FN-ORDER-001`. Missing required origin/destination or non-positive dimensions produce field-specific validation errors. On this path the API must not call the carrier or persist a booking.
4. If validation succeeds, `CMP-API-BOOKING` requests a booking from `EXT-CARRIER` using `IF-CARRIER-001`. **Open:** provider authentication, carrier-specific field mapping, idempotency token, timeout, retry policy, rate limit and response/error schema.
5. On an unambiguous carrier success, the API receives a provider booking reference and, if supplied, a label or label reference. **Open:** synchronous response vs callback/polling, label storage location, privacy classification and provider version.
6. `CMP-API-REPOSITORY` writes the booking state to `CNT-DB`. **Open:** schema, transaction boundary, durable commit point and handling when the carrier succeeds but persistence fails.
7. `CNT-API` returns a booking outcome to `CNT-WEB`; the operator sees the state and can retrieve the label when available. **Open:** response codes, polling/callback behavior, authorization and user-visible terminal states.

## Alternate and failure paths

| Condition | Required externally visible behavior | Side effects/recovery | Current status |
|---|---|---|---|
| Invalid input | Field-specific validation failure; no carrier call and no booking write | Correct request and resubmit | Rule evidenced by `FN-ORDER-001`; error envelope still open |
| Carrier rejects request | Do not present success; preserve actionable failure category | Persisting the rejection vs. no record is a product decision | `UNKNOWN`; define contract and tests |
| Carrier timeout before response | Return/record a non-success or pending/unknown result; do not blindly create another booking | Reconcile with provider or retry only when idempotency semantics allow | `UNRESOLVED`; critical integration decision |
| Carrier success but DB write fails | Do not lose the provider booking reference; do not claim durable completion | Retry persistence, reconcile by idempotency/reference, or provide manual recovery | `UNRESOLVED`; critical consistency/compensation design |
| DB commit succeeds but client response is lost | A repeated client request must not silently create a second carrier booking | Return same result using durable idempotency/correlation state | `UNRESOLVED`; key scope/retention not defined |
| Label unavailable after booking | Distinguish booked from label-ready; make retrieval/retry state visible | Poll/event/manual support path according to carrier contract | `UNKNOWN`; lifecycle missing |

These are design obligations and failure cases, not claims that the sample already implements them. No compensation protocol is specified. A distributed transaction spanning carrier and local database must not be assumed.

## Data and consistency effects

Candidate data includes origin/destination, parcel dimensions, local booking state, provider reference, error/status metadata and label content/reference. The authoritative source, exact schema, sensitive-data classification, data minimization, retention/deletion, encryption and audit rules remain unresolved. The flow should avoid logging addresses, credentials or label contents. Consistency between provider booking and `CNT-DB` is not guaranteed by the current sample; explicitly model `PENDING`, `SUCCEEDED`, `FAILED`, or `UNKNOWN` states only after product/provider semantics are confirmed.

## Verification scenarios

- Invalid/missing origin, destination, zero/negative dimensions: validation error, zero carrier calls, zero booking writes.
- Valid request with carrier success: correlate request/provider reference, persist outcome and expose status/label reference.
- Carrier rejection, timeout, rate-limit response and malformed provider response: deterministic status/error with no false success.
- Retry after timeout and duplicate client submission: prove idempotency or block automatic retry until reconciliation.
- Carrier success followed by DB failure; DB commit followed by lost HTTP response; label delay: verify recovery and no duplicate booking.
- Authorization/tenant boundary, PII redaction and audit behavior: add once the identity/data policy is defined.

## Open decisions

| Decision/unknown | Impact | Required evidence | Owner/action | Revisit trigger |
|---|---|---|---|---|
| Synchronous vs asynchronous booking lifecycle | API contract, user experience, retry and persistence model | Carrier SLA/callback behavior and product workflow | `OWNER_UNASSIGNED` — appoint product/integration owner | Before API contract approval |
| Idempotency and reconciliation semantics | Duplicate bookings and financial/support exposure | Provider contract and fault-injection test | `OWNER_UNASSIGNED` — appoint integration owner | Before enabling retries |
| Data/label retention and ownership | Privacy, security and recovery | Data classification and retention policy | `OWNER_UNASSIGNED` — appoint data/privacy owner | Before production storage |

Flow disposition: `PARTIAL` — happy path and important failure obligations are documented, while implementation-specific contracts and acceptance remain open.
