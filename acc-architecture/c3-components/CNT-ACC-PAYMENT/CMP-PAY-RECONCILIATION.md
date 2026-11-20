# CMP-PAY-RECONCILIATION — Reconciliation Engine

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-PAY-RECONCILIATION |
| **Parent Container** | CNT-ACC-PAYMENT (Payment Orchestration — ACCSystem) |
| **Purpose** | Periodically reconciles internal payment transaction records against settlement reports received from EXT-PAYMENT-PROVIDER. Flags discrepancies as operational alerts for human review or automated correction. |
| **Scope Boundary** | Owns reconciliation run records and discrepancy alerts. Does NOT authorize payments, process refunds, or directly modify payment transaction state — it raises alerts that trigger corrective action via CMP-PAY-ORCHESTRATOR or CMP-PAY-REFUND. |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CMP-PAY-ORCHESTRATOR | Inbound (reads) | Reads internal payment transaction records for comparison |
| EXT-PAYMENT-PROVIDER | Inbound (ingests) | Source of settlement report data |
| CNT-ACC-AUDIT | Outbound | Publishes reconciliation run results and discrepancy audit events |
| Operational alerting (CNT-ACC-AUDIT / monitoring) | Outbound | Emits alerts for discrepancies requiring action |

---

## 3. Behavior, Rules, and State

### 3.1 Reconciliation Process

| Step | Action |
|---|---|
| **1 — Ingest** | Receive/pull settlement report from EXT-PAYMENT-PROVIDER for a given settlement period |
| **2 — Normalize** | Parse provider-specific report format into internal settlement line items |
| **3 — Match** | Match each settlement line item through the durable scoped mapping of provider transaction/reference, `payment_attempt_id`, `seller_order_id`, and `allocation_id`. One aggregate provider transaction may reconcile to multiple provider allocation references and internal allocations; never infer scope from `order_id` alone. |
| **4 — Compare** | Compare the provider line or aggregate against the internal allocation-level reconciliation basis: gross, fee, commission, net, currency, status, and relevant operation timestamps. Aggregate totals may be compared only after all constituent allocations and provider references are mapped. |
| **5 — Flag** | Record unmatched, over-settled, under-settled, or status-mismatched items as `DiscrepancyRecord` |
| **6 — Alert** | Emit operational alert for any discrepancy requiring action; publish `ReconciliationCompleted` audit event |

### 3.2 Reconciliation Triggers

- **Scheduled:** periodic run on a configurable schedule. ASSUMPTION — frequency expected to match provider settlement cadence.
- **Manual:** triggered by operational team for ad hoc period re-reconciliation.

### 3.3 Discrepancy Classification

| Category | Description | Action |
|---|---|---|
| `UNMATCHED_INTERNAL` | Settlement line has no matching internal transaction | Alert; investigate potential duplicate payment or data gap |
| `UNMATCHED_PROVIDER` | Internal transaction has no matching settlement line | Alert; payment may not have settled — investigate with provider |
| `AMOUNT_MISMATCH` | Provider gross, fee, commission, or net differs from the allocation-level reconciliation basis; an aggregate mismatch is decomposed before classification | Alert; possible fee deduction, split-mapping gap, or error |
| `STATUS_MISMATCH` | Internal status is `CAPTURED` but provider shows `REFUNDED` or vice versa | Alert; trigger corrective state sync via CMP-PAY-ORCHESTRATOR |
| `CURRENCY_MISMATCH` | Currencies differ | Alert; high severity |

> [!WARNING] Settlement report format and delivery frequency are **UNKNOWN** — open decision (idea.md §12 — settlement/commissions). Consequence: reconciliation scheduling, ingest pipeline, and normalization logic cannot be finalized. Resolution evidence: provider contract / settlement API specification. Owner: OWNER_UNASSIGNED. Revisit trigger: provider selection (Phase 3).

---

## 4. Data Owned

| Entity | Owned By | Schema Shape |
|---|---|---|
| `ReconciliationRun` | CMP-PAY-RECONCILIATION | `{run_id, period_start, period_end, status, total_lines, matched, unmatched, discrepancies, completed_at}` |
| `DiscrepancyRecord` | CMP-PAY-RECONCILIATION | `{discrepancy_id, run_id, type, payment_attempt_id?, seller_order_id?, allocation_id?, aggregate_transaction_id?, provider_transaction_reference?, provider_allocation_reference?, internal_gross?, internal_fee?, internal_commission?, internal_net?, provider_gross?, provider_fee?, provider_commission?, provider_net?, currency?, internal_status, provider_status, flagged_at, resolved_at, resolution_note}` |
| Ingested settlement report (raw) | CMP-PAY-RECONCILIATION | Stored as blob/JSONB per run for audit; retention policy UNKNOWN |

**NOT owned:**
- `PaymentTransaction` records (owned by CMP-PAY-ORCHESTRATOR — read-only access here)
- Refund execution (owned by CMP-PAY-REFUND)

---

## 5. Failure Modes and Resilience

| Failure | Response Strategy |
|---|---|
| Settlement report unavailable / delivery failure | Retry ingestion; alert if report not received within expected window; run is marked `PARTIAL` |
| Provider report format changes without notice | Parse failure; alert operations team; run marked `FAILED`; manual review required |
| Reconciliation run fails midway | Re-runnable from last checkpoint using `run_id`; idempotent match results |
| Discrepancy alert delivery fails | Alert is persisted in `DiscrepancyRecord`; operational dashboard must surface unresolved records |
| Large settlement volume causing timeout | Batch processing per configurable page size. PROPOSAL |

---

## 6. Security Responsibilities

| Concern | Responsibility |
|---|---|
| Settlement report source authentication | UNKNOWN — depends on provider delivery mechanism (SFTP, webhook, API pull); must be verified. Owner: OWNER_UNASSIGNED |
| Access to raw settlement data | Restricted to CMP-PAY-RECONCILIATION process; not exposed via API |
| Audit trail | Every reconciliation run and every discrepancy record written to Audit & Observability |
| Data retention | Settlement reports and discrepancy records must follow financial data retention policy. UNKNOWN — policy not defined |

---

## 7. Operational Concerns

### 7.1 SLIs

| Indicator | Target (PROPOSAL) |
|---|---|
| Reconciliation run completion within schedule | > 99% (excluding provider report non-delivery) |
| Discrepancy detection latency | Within one settlement cycle of occurrence |
| Unresolved discrepancies beyond the configured escalation age | Alert operational team; age is a controlled policy value, not an asserted duration |

### 7.2 Scaling

- Batch job execution; scaling is bounded by settlement volume, not user traffic.
- Settlement volume at scale is UNKNOWN; horizontal partition by settlement period is PROPOSAL.

### 7.3 Known Risks

| Risk | Consequence | Mitigation |
|---|---|---|
| Settlement report format entirely unknown | Cannot build ingest pipeline | Highest risk item for Phase 3; unblock by provider selection |
| Commission/fee logic complexity | UNKNOWN — if platform takes a cut, settlement amounts will differ from order amounts | Design fee model before Phase 3 (idea.md §12 — settlement/commissions) |
| Multi-currency settlement | Reconciliation requires exchange rate reference | UNKNOWN — multi-currency open decision (idea.md §12) |

---

## 8. Unknowns, Traceability, and ADR References

| Item | Status | Owner / Action |
|---|---|---|
| Settlement report format | UNKNOWN — idea.md §12 open decision | OWNER_UNASSIGNED; resolve during Phase 3 provider onboarding |
| Settlement report delivery frequency and mechanism | UNKNOWN | Provider contract; define before Phase 3 |
| Commission / platform fee deduction model | UNKNOWN — idea.md §12 | Finance / product team; define before Phase 3 |
| Financial data retention period | UNKNOWN | Legal / compliance; define before Phase 3 |

**ADR References:** ADR-005, ADR-007

**Requirement References:** §7.5 (partial failure — "Payment Reconciliation"), §11 (monitoring — "Payment Reconciliation"), §12 (open decisions)


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Daily settlement file matching | Provider settlement file received | Transactions matched against local payment records; status `SETTLED` |
| Missing settlement record | Local payment record missing corresponding settlement entry | Discrepancy logged; flagged for financial operations review |
| Amount discrepancy | Provider settled amount differs from authorized amount | Discrepancy record created; automated alert dispatched to finance team |
