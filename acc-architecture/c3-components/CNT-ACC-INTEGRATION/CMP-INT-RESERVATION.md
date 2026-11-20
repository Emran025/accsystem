# CMP-INT-RESERVATION — Reservation Relay

**Purpose:** Relay versioned reservation/release commands between the Parent Saga Coordinator and seller ACCore instances. It does not own inventory decisions.

## Contract and state
Every command contains `parent_order_id`, `seller_order_id`, `reservation_id`, `seller_id`, items, price/currency snapshot reference, correlation ID, and idempotency key. The relay persists `REQUESTED`, `ACCEPTED`, `REJECTED`, `UNKNOWN`, `RELEASE_REQUESTED`, `RELEASED`, `EXPIRED`, and `CONSUMED/COMMITTED` states.

## Behavior
The relay writes an Outbox entry before sending. Responses are Inbox-deduplicated. A timeout, channel interruption, circuit-open result, or lost response becomes `UNKNOWN`; retries first query ACCore by reservation ID/idempotency key. It never emits `REJECTED` or sends a release merely because a timeout elapsed. Definitive rejection is emitted only from ACCore evidence. Release commands are separate idempotent commands and are reconciled if their result is unknown.

## Failure handling
| Condition | Result |
|---|---|
| ACCore accepted | Persist `ACCEPTED`; notify parent saga. |
| ACCore definitively rejected | Persist `REJECTED`; notify parent saga. |
| Timeout/disconnection | Persist `UNKNOWN`; retry/query/reconcile; payment remains blocked. |
| Accepted hold, known payment/order failure | Send `RELEASE_REQUESTED`; release only that known hold. |
| Release timeout | Persist release `UNKNOWN`; query/reconcile; do not repeat blindly. |
| Duplicate command/event | Return stored result; no duplicate side effect. |

Authentication uses the method selected by ADR-015 policy. Numeric retry, timeout, hold, and deduplication values are deployment configuration owned by operations and must be consistent with reconciliation coverage.

## Interfaces and collaborators
- Consumes `IF-ACC-RESERVE-SAGA` from the Order Saga and relays to ACCore through `CMP-CON-RESERVATION`.
- Returns outcomes through `IF-ACR-RESERVATION-RESP`; exact delivery modality remains open under ADR-015.

## Verification references
Existing acceptance scenarios in `FN-ORD-RESERVE` and `validation/acceptance-test-plan.md` cover accepted/rejected/unknown outcomes, query-before-retry, and idempotent release. These are documented scenarios, not executed-test results.
