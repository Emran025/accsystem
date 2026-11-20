# Financial Ledger and Settlement View

## State model

Where a selected provider supports and policy enables payment-code lookup, an illustrative branch is `PaymentIntentCreated` → `CodeIssued` → `ProviderLookupVerified` → `Authorized`/`Captured`/`UNKNOWN`/`Declined`. Other approved supported provider paths need not issue or look up a code; see `CMP-PAY-ORCHESTRATOR`. In all branches, seller credit/transfer is tracked separately as `Pending`, `Credited`, `Failed`, `Reversed`, or `Reconciled`. Commission is a separate payable record linked to the SellerOrder and ledger postings. A manual payment is `RecordedOutsidePlatform` and never masquerades as a provider capture.

Every record carries `order_id`, `seller_order_id`, `payment_attempt_id`, provider/external reference when available, currency, amount, exchange-rate source and timestamp when conversion occurs, actor/source, correlation ID, idempotency key, policy snapshot ID, and immutable timestamps. Unknown, duplicate, reversal, and unmatched records enter reconciliation queues; no timeout is treated as a negative result.

## Controls

Ledger postings are append-only, balanced by currency, and idempotent. Corrections use reversal/adjustment postings rather than mutation. Raw PAN/CVV/expiry are never stored. Provider webhooks, polling, settlement files, and manual evidence are adapter inputs. Manual-payment and commission-policy permissions are institution-scoped and approval-controlled. Reporting separates gross product price, tax lines, delivery charges, commission, provider fees, seller credit, and settlement status.

## External gates

The selected provider must be tested for payment-code lookup, seller accounts/wallets, direct credit or split payment, webhook/reversal/refund support, reconciliation files, and legal/finance suitability. Tax liability, commission basis, settlement timing, and accounting recognition require finance/legal approval; no value is invented here.
