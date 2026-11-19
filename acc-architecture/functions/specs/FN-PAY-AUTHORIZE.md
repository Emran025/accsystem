# FN-PAY-AUTHORIZE — Payment Authorization and Capture Policy

**Function ID:** FN-PAY-AUTHORIZE  
**Status:** PROPOSED MVP BASELINE — seller/agreement policy is configurable and constrained by platform/provider/risk controls.

## Preconditions
All required SellerOrder reservations are `ACCEPTED/RESERVED`; no reservation is `UNKNOWN`. Every payment allocation has seller, SellerOrder, amount, currency, tax/delivery basis, policy snapshot, correlation ID, and idempotency key. Raw card data is absent.

## Flow
1. The Parent Saga creates one payment allocation per SellerOrder.
2. The policy resolver selects `AUTHORIZE_THEN_CAPTURE` or `IMMEDIATE_CAPTURE` for each seller/agreement. If a shared provider transaction would combine incompatible policies, split into separate attempts or reject checkout under policy; do not silently choose one.
3. The orchestrator sends an idempotent provider request. `AUTHORIZED` means a hold only; `CAPTURED` means collection; neither alone means seller settlement/credit.
4. On definitive decline/failure, release confirmed reservations. On timeout/lost response, persist `AUTHORIZATION_UNKNOWN` or `CAPTURE_UNKNOWN`, query/reconcile by provider reference/idempotency key, and do not repeat a financial effect or release a potentially existing hold solely due to elapsed time.
5. For authorize-then-capture, capture at the configured seller/agreement trigger after confirmation. For immediate capture, capture in the approved payment step. Capture failure after order confirmation becomes a visible payment exception requiring retry/reconciliation/void/refund policy.

## States
`PENDING_AUTHORIZATION`, `AUTHORIZING`, `AUTHORIZED`, `AUTHORIZATION_DECLINED`, `AUTHORIZATION_UNKNOWN`, `CAPTURE_REQUESTED`, `CAPTURED`, `CAPTURE_UNKNOWN`, `CAPTURE_FAILED`, `VOIDED`, `REFUNDED`, `RECONCILIATION_REQUIRED`.

## Verification
Test per-SellerOrder payment records, compatible aggregate transaction, incompatible policy split, authorize-then-capture, immediate capture, provider timeout, duplicate webhook, capture failure after confirmation, seller-credit mismatch, commission posting, and ledger reconciliation. No fixed timeout, expiry, percentage, or provider capability is asserted.
