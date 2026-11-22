# FN-ORD-RESERVE — Inventory Reservation Function Specification

**Function ID:** FN-ORD-RESERVE  
**Status:** PROPOSED MVP BASELINE — configurable operational thresholds require review.

## Purpose
Reserve each SellerOrder's inventory at its seller's ACCore before any payment authorization. ACCore is the source of truth; ACCSystem stores only request/result state and an indicative projection.

## Execution
For each SellerOrder, the Parent Saga Coordinator persists a stable scoped request/idempotency key before dispatch. The resulting ACCore reservation ID is a distinct reference; its assignment and mapping conflict across current documents and require institution/API agreement. Requests may execute concurrently across sellers.

1. Persist `ReservationRequested` and an Outbox command in ACCSystem.
2. ACCore receives the command through the logical connector contract.
3. ACCore performs stock check and reservation in one local atomic transaction using a conditional update or suitable row lock. The transaction records the request result under the idempotency key.
4. If sufficient stock exists, return `ACCEPTED` with reservation ID, seller price confirmation, expiry policy reference, and quantity held. If insufficient, return `REJECTED` with a reason and no hold.
5. If the response is lost, persist `UNKNOWN`; use the stable request key to correlate/query where supported, including when the remote ID is not yet known. Query capability and endpoint are assumptions pending agreement; otherwise wait safely and escalate. Never infer rejection from timeout.
6. All required accepted holds and other guards permit payment. A definitive rejection or authoritative expiry blocks checkout; reconcile other UNKNOWN outcomes and compensate only eligible confirmed effects under ADR-018. Final closure waits for required compensation. Any unknown remains in reconciliation and blocks payment.

## States
`REQUESTED` → `ACCEPTED` | `REJECTED` | `UNKNOWN`;
`ACCEPTED` → `RELEASE_REQUESTED` → `RELEASED` | `UNKNOWN`;
`ACCEPTED` → `CONSUMED/COMMITTED`;
`ACCEPTED` → `EXPIRED` only on authoritative ACCore expiry evidence, not elapsed local time alone. An unknown request is queried before a retry where the institution contract provides a trusted query; otherwise the saga waits/escalates and does not repeat a possible effect. An unknown release is reconciled before any further release.

`RESERVED` is a deprecated legacy synonym for `ACCEPTED`, and `INSUFFICIENT` is a deprecated legacy synonym for `REJECTED`; neither is a current wire or state-machine token (ADR-018 §3.3).

## Idempotency and retention
The deduplication record is retained for a configurable operational period that covers retries and reconciliation and does not expire before the outcome is resolved or safely reconciled. No fixed duration is asserted. Duplicate requests return the original result. Release is idempotent and cannot release a consumed reservation or one linked to a confirmed order.

## Failure and security
A connector interruption creates `UNKNOWN`, not `REJECTED`. Release is not issued solely because a timeout elapsed. ACCore uses the authentication method enabled by the controlled policy in ADR-015 (OAuth 2.0 Client Credentials, mTLS, or another approved method); no API-key-or-mTLS ambiguity is embedded here. All commands/events use Outbox/Inbox, at-least-once delivery, correlation IDs, and idempotency keys.

## Acceptance tests

- Two concurrent requests for the last unit result in at most one `ACCEPTED` reservation.
- Duplicate request returns the original result without a second hold.
- Accepted response lost, then query by reservation ID returns `ACCEPTED`; no duplicate hold.
- Timeout before any known result remains `UNKNOWN`; no unsafe release.
- Definitive rejection compensates only confirmed accepted reservations from other sellers.
- Release retry is idempotent and cannot release `CONSUMED/COMMITTED` stock.
- Outbox publish failure is replayed without duplicate reservation.

**References:** ADR-015, ADR-016, ADR-017, CMP-INT-RESERVATION, CMP-CON-RESERVATION.

## Interfaces and collaborators
- Caller: `CMP-ORD-SAGA` within `CNT-ACC-ORDERS`.
- Command path: `IF-ACC-RESERVE-SAGA` → `CMP-INT-RESERVATION` → `CMP-CON-RESERVATION`.
- Outcome path: `IF-ACR-RESERVATION-RESP` → relay → parent saga. Exact schema/version and delivery modality remain contract gates.
