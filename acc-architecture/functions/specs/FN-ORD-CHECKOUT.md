# FN-ORD-CHECKOUT — Multi-Seller Checkout Function

**Function ID:** FN-ORD-CHECKOUT  
**Status:** PROPOSED MVP BASELINE — multi-seller carts are required; operational thresholds are configurable.

## Purpose and preconditions
Create one ParentOrder and one SellerOrder per seller, reserve inventory at every seller ACCore, then proceed to payment only after every required reservation is authoritatively `ACCEPTED`; definitive `REJECTED` fails checkout after conditional compensation, while `UNKNOWN` blocks payment and enters reconciliation. ACCore is the inventory source of truth. All commands/events use Outbox/Inbox, at-least-once delivery, correlation IDs, and idempotency keys.

## Executable flow

1. Validate buyer, cart, seller grouping, price/tax/delivery/currency snapshots, and policy versions.
2. Persist ParentOrder, SellerOrders, saga state, and outbox records atomically.
3. Start one reservation sub-operation per SellerOrder, concurrently where safe. Each has a stable scoped request/idempotency key; reservation-ID assignment and mapping remain an institution/API gate.
4. Wait for every required reservation:
   - all `ACCEPTED` → payment is eligible;
   - any definitive `REJECTED` or authoritative `EXPIRED` → block checkout; reconcile in-flight peers, then compensate eligible known holds under ADR-018 and close only after required outcomes resolve;
   - any `UNKNOWN` → enter `ReservationUnknown`, stop payment and unsafe release, reconcile by known reservation ID or stable key through an agreed available channel, or wait and escalate.
5. Create payment allocation records per SellerOrder. Use one aggregated buyer-facing provider transaction only when seller policies are compatible and provider capabilities support it; otherwise use separate payment attempts.
6. Apply the approved capture policy per seller/agreement: `AUTHORIZE_THEN_CAPTURE` or `IMMEDIATE_CAPTURE` when supported and permitted. Authorization is a hold, capture is collection, seller credit/transfer is separate, and settlement is reconciled later.
7. On definitive payment failure, block confirmation, reconcile other in-flight payment/reservation effects, and compensate eligible known effects only where the conservative UNKNOWN guard and policy permit. Any UNKNOWN remains pending/review without repeating a financial effect or unsafe release; final failure/expiry requires settled required compensation. Before confirmation re-establish that all required holds remain accepted and all required allocations have definitive success.
8. Persist immutable ParentOrder/SellerOrder snapshots, state transition, and `OrderConfirmed` outbox record in one local transaction. If local persistence fails before commit, no confirmation exists; retry safely. If an external command may already have executed, query/reconcile before retrying or compensating.
9. Post-confirmation inventory commit, capture, seller credit, settlement, and delivery are independent state machines with their own idempotent operations and reconciliation. They are not universal synchronous consequences of confirmation.

## Failure and recovery matrix

| Situation | Known/unknown classification | Required action |
|---|---|---|
| Local validation or write fails before an external command | Known local failure; no external side effect recorded | Roll back local transaction and retry; do not issue compensation for an unissued command. |
| Reservation definitively rejected or authoritatively expired | Known outcome for that hold, not proof of peer outcomes | Block payment; reconcile peers, compensate only eligible known holds under guards, and close only after required outcomes settle. |
| Reservation response lost/timeout/disconnection | Unknown | `ReservationUnknown`; query by reservation ID/key; no payment and no release solely due to timeout. |
| Payment definitively declined | Known outcome for that attempt, not proof of peer outcomes | Reconcile other attempts/holds, compensate only eligible known effects under guards; record results and keep pending until settled. |
| Payment response lost/timeout | Unknown | `PaymentUnknown`; query provider/reconcile; no duplicate authorization/capture and no unsafe release. |
| Authorization confirmed but local confirmation write fails | External effect may exist | Persist recovery task, query payment and reservation states, then resume or void/release only after definitive state evidence; never assume a void/release succeeded. |
| Outbox write/transaction fails | Known local failure if commit did not occur | Retry transaction. If order commit occurred, relay persisted outbox and reconcile delivery; do not create a second order. |
| Confirmed order downstream capture/commit fails | Post-confirmation exception | Keep explicit pending/failed/unknown state per domain; retry/reconcile/void/refund under policy; do not roll back the ParentOrder implicitly. |
| Saga operational timeout | Not a business outcome | Escalate and transition the affected sub-operation to `UNKNOWN`/review when an external result may exist. Compensate only after final state resolution. |
| Checkout session expires | Not proof that reservation is absent | Query ACCore states. Expiry/release follows configured ACCore safe-expiry policy only; unknown reservations remain protected and reconciling. |

## Testable acceptance criteria

- Multi-seller cart creates one ParentOrder and one SellerOrder per seller.
- Payment is not requested until all required reservations are definitively accepted.
- Timeout after a sent reservation request produces `UNKNOWN`, not rejection, and does not release a potentially existing hold.
- Lost `ReservationAccepted` response is resolved by query/idempotency key without a duplicate hold.
- Timeout during release remains release `UNKNOWN` and is reconciled before another release attempt.
- Definitive payment decline blocks confirmation; after required reconciliation, only eligible confirmed reservations may be released under the conservative UNKNOWN guard; unresolved peers or compensation prevent closure.
- Payment timeout produces `PaymentUnknown`; no duplicate financial effect occurs.
- Saga restart resumes persisted state without duplicate holds, payments, confirmations, or outbox events.
- Authorize-then-capture and immediate capture are separately testable; capture, seller credit, and settlement are distinct states.
- A confirmed authorization followed by local write failure enters recovery/reconciliation rather than blindly issuing void or marking failure.

**References:** FN-ORD-RESERVE, FN-ORD-CONFIRM, FN-PAY-AUTHORIZE, CMP-ORD-SAGA, ADR-016, ADR-017.
