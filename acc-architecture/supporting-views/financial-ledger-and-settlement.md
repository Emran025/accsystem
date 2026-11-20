# Financial Ledger and Settlement View

## State model

Where a selected provider supports and policy enables payment-code lookup, an illustrative branch is `PaymentIntentCreated` → `CodeIssued` → `ProviderLookupVerified` → `Authorized`/`Captured`/`UNKNOWN`/`Declined`. Other approved supported provider paths need not issue or look up a code; see `CMP-PAY-ORCHESTRATOR`. In all branches, seller credit/transfer is tracked separately as `Pending`, `Credited`, `Failed`, `Reversed`, or `Reconciled`. Commission is a separate payable record linked to the SellerOrder and ledger postings. A manual payment is `RecordedOutsidePlatform` and never masquerades as a provider capture.

Every record carries `order_id`, `seller_order_id`, `payment_attempt_id`, provider/external reference when available, currency, amount, exchange-rate source and timestamp when conversion occurs, actor/source, correlation ID, idempotency key, policy snapshot ID, and immutable timestamps. Unknown, duplicate, reversal, and unmatched records enter reconciliation queues; no timeout is treated as a negative result.

## Controls

Ledger postings are append-only, balanced by currency, and idempotent. Corrections use reversal/adjustment postings rather than mutation. Raw PAN/CVV/expiry are never stored. Provider webhooks, polling, settlement files, and manual evidence are adapter inputs. Manual-payment and commission-policy permissions are institution-scoped and approval-controlled. Reporting separates gross product price, tax lines, delivery charges, commission, provider fees, seller credit, and settlement status.

## Ownership and executable boundary

The payment domain owns payment-attempt, provider-operation, and allocation state. `CMP-PAY-RECONCILIATION` is the current payment/settlement-evidence matching capability: it ingests approved provider evidence, maintains reconciliation runs and discrepancy records, and raises corrective alerts; it does not post the ledger or mutate payment state directly. A future Settlement/Ledger boundary (owner to be assigned; PROPOSED) owns seller-credit/transfer, commission payable, settlement finality, and immutable ledger postings. It consumes `PaymentCaptured` or `RecordedOutsidePlatform` outcomes and emits allocation-scoped `SellerCreditPending`, `SellerCredited`, `SellerCreditUnknown`, `SettlementPending`, `SettlementReconciled`, and reversal/adjustment events through an outbox. `Confirmed` is not financial completion: each allocation independently progresses through `CAPTURED → CREDIT_PENDING → CREDITED/UNKNOWN → SETTLEMENT_PENDING → SETTLED/REVERSED`, subject to provider, institution, Finance and Legal policy.

### Responsibility matrix (interim and target)

| Responsibility | Current owner/status | Boundary rule |
|---|---|---|
| Payment-attempt and allocation state | Payment domain / CMP-PAY-ORCHESTRATOR | Owns capture/authorization facts and scoped operation identity; reconciliation is read-only for these records |
| Provider-operation and webhook outcome reconciliation | CMP-PAY-RECONCILIATION with CMP-PAY-ADAPTER/CMP-PAY-ORCHESTRATOR | Maps provider evidence to the scoped operation; unresolved mapping remains `UNKNOWN` |
| Settlement-report/evidence ingestion and discrepancy records | CMP-PAY-RECONCILIATION (interim) | Matches evidence and raises alerts; does not declare commercial settlement finality by itself |
| Seller credit, commission, settlement finality, and immutable ledger posting | Future Settlement/Ledger boundary (PROPOSED; owner unassigned) | Requires provider, institution, Finance, and Legal policy; no implementation owner is implied |
| Corrective financial command authority | Owning payment or future Settlement/Ledger component according to operation type (OPEN) | A discrepancy triggers an approved corrective command; it never authorizes an ad hoc mutation or retry |

Direct seller credit, platform-central collection followed by controlled settlement, separate provider attempts, and externally completed or manual payments remain supported alternatives. The selected route, commission basis, provider report contract, accounting trigger, and reversal authority are approval gates; this boundary does not choose among them.

## External gates

The selected provider must be tested for payment-code lookup, seller accounts/wallets, direct credit or split payment, webhook/reversal/refund support, reconciliation files, and legal/finance suitability. Tax liability, commission basis, settlement timing, and accounting recognition require finance/legal approval; no value is invented here.
