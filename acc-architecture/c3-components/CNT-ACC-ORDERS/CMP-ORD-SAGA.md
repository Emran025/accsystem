# CMP-ORD-SAGA — Parent Order Saga Coordinator

**Status:** PROPOSED MVP BASELINE — multi-seller checkout required; owner direction recorded in ADR-016.

## Responsibility
Coordinate one ParentOrder and its SellerOrders across ACCore reservations, payment allocations, confirmation, and post-confirmation effects. A local transaction never spans ACCSystem and ACCore.

## Steps
1. Validate cart and create ParentOrder/SellerOrders through the splitter.
2. Launch one reservation sub-operation per SellerOrder, concurrently where safe.
3. Wait for every required reservation. `ACCEPTED` for all proceeds. Any definitive `REJECTED` releases confirmed accepted holds and fails checkout. Any `UNKNOWN` blocks payment and enters reconciliation; it is not failure.
4. Create payment allocation records per SellerOrder. Use one aggregated buyer transaction only when all seller policies are compatible and the provider supports it; otherwise use separate payment attempts. Each operation has seller/order amount, currency, policy snapshot, and idempotency key.
5. Run the configured capture policy: authorize-then-capture or immediate/contract-defined capture. Seller policy cannot bypass platform, legal, risk, or provider controls.
6. Persist the immutable parent/seller order snapshot and `CONFIRMED` transition with `OrderConfirmed` in the same local transaction via Outbox. If publication fails after commit, the durable outbox relay retries; the order is not rolled back by an absent delivery.

## Compensation and unknowns
| Condition | Action |
|---|---|
| Definitive reservation rejection | Release confirmed accepted holds; no payment. |
| Reservation unknown | Query/reconcile; no payment or release solely due to timeout. |
| Definitive payment failure | Release confirmed holds; fail checkout. |
| Payment unknown | Preserve payment/reservation unknown states; reconcile; no duplicate financial action. |
| Confirmation write failure before commit | Retry local transaction; no confirmed order. |
| Outbox delivery failure after commit | Retry outbox; order remains committed and visible. |
| Capture failure after confirmation | Keep order confirmed with payment exception; retry/reconcile/void/refund according to policy. |

All steps are at-least-once and idempotent. Saga state is persisted and recovery resumes from the last known state. Numeric retry/timeout/expiry values are configuration, not asserted targets.

## Verification references
Existing scenarios in `FN-ORD-CHECKOUT`, `FN-ORD-RESERVE`, `FN-PAY-AUTHORIZE`, and `validation/acceptance-test-plan.md` cover reservation-before-payment, UNKNOWN blocking, idempotent confirmation, and outbox recovery. These references do not claim runtime execution.
