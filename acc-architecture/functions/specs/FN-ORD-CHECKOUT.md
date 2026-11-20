# FN-ORD-CHECKOUT — Multi-Seller Checkout Function

**Function ID:** FN-ORD-CHECKOUT  
**Status:** PROPOSED MVP BASELINE — multi-seller carts are required; operational thresholds are configurable.

## Purpose and preconditions
Create one ParentOrder and one SellerOrder per seller, reserve inventory at every seller ACCore, then proceed to payment only after every required reservation has a definitive accepted or rejected outcome. ACCore is the inventory source of truth. All commands/events use Outbox/Inbox, at-least-once delivery, correlation IDs, and idempotency keys.

## Executable flow

1. Validate buyer, cart, seller grouping, price/tax/delivery/currency snapshots, and policy versions.
2. Persist ParentOrder, SellerOrders, saga state, and outbox records atomically.
3. Start one reservation sub-operation per SellerOrder, concurrently where safe. Each has a unique reservation ID and idempotency key.
4. Wait for every required reservation:
   - all `ACCEPTED` → payment is eligible;
   - any definitive `REJECTED` → release only reservations confirmed accepted, then fail checkout;
   - any `UNKNOWN` → enter `ReservationUnknown`, stop payment and unsafe release, query ACCore by reservation ID/key, and reconcile.
5. Create payment allocation records per SellerOrder. Use one aggregated buyer-facing provider transaction only when seller policies are compatible and provider capabilities support it; otherwise use separate payment attempts.
6. Apply the approved capture policy per seller/agreement: `AUTHORIZE_THEN_CAPTURE` or `IMMEDIATE_CAPTURE` when supported and permitted. Authorization is a hold, capture is collection, seller credit/transfer is separate, and settlement is reconciled later.
7. On definitive payment failure, release only confirmed reservations through idempotent release commands. If payment is `UNKNOWN`, stop dependent steps and reconcile without repeating a financial effect or releasing a potentially held reservation.
8. Persist immutable ParentOrder/SellerOrder snapshots, state transition, and `OrderConfirmed` outbox record in one local transaction. If local persistence fails before commit, no confirmation exists; retry safely. If an external command may already have executed, query/reconcile before retrying or compensating.
9. Post-confirmation inventory commit, capture, seller credit, settlement, and delivery are independent state machines with their own idempotent operations and reconciliation. They are not universal synchronous consequences of confirmation.

## Failure and recovery matrix

| Situation | Known/unknown classification | Required action |
|---|---|---|
| Local validation or write fails before an external command | Known local failure; no external side effect recorded | Roll back local transaction and retry; do not issue compensation for an unissued command. |
| Reservation definitively rejected | Known final outcome | Release only confirmed accepted holds; fail checkout; no payment. |
| Reservation response lost/timeout/disconnection | Unknown | `ReservationUnknown`; query by reservation ID/key; no payment and no release solely due to timeout. |
| Payment definitively declined | Known final outcome | Release only confirmed reservations using idempotent commands; record outcomes; fail checkout. |
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
- Definitive payment decline releases only confirmed reservations and never unknown reservations.
- Payment timeout produces `PaymentUnknown`; no duplicate financial effect occurs.
- Saga restart resumes persisted state without duplicate holds, payments, confirmations, or outbox events.
- Authorize-then-capture and immediate capture are separately testable; capture, seller credit, and settlement are distinct states.
- A confirmed authorization followed by local write failure enters recovery/reconciliation rather than blindly issuing void or marking failure.

**References:** FN-ORD-RESERVE, FN-ORD-CONFIRM, FN-PAY-AUTHORIZE, CMP-ORD-SAGA, ADR-016, ADR-017.
