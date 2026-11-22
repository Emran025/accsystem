# REQ-PH03-PAYMENT-RECONCILIATION — Payment reconciliation

**Document ID:** REQ-PH03-PAYMENT-RECONCILIATION  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-PAYMENT-RECONCILIATION |
| Phase ID | PH-03 |
| Title | Payment reconciliation |
| Statement | Payment records are reconciled against provider evidence at allocation level so UNKNOWN outcomes are resolved and discrepancies are raised for corrective action. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-PAYMENT, CNT-ACC-ORDERS, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH03-001) |
| Status | DRAFT |
| Evidence | CMP-PAY-RECONCILIATION; ADR-016; acceptance-test-plan.md items 4-6; financial-ledger-and-settlement.md |

## 2. Scope boundary and phase handoffs

- Reconciliation alerts and read internal records; corrective commands belong to the owning payment component.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-PRC-001 | REQ-PH03-PAYMENT-RECONCILIATION | Reconciliation resolves an UNKNOWN payment operation from authoritative provider evidence before any retry, void or release. | A payment is UNKNOWN. | One definitive state or continued UNKNOWN. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-ORDERS | AC-PH03-PRC-001-01 | TEST (planned): unknown resolution test | DRAFT | IC-003 |
| SREQ-PH03-PRC-002 | REQ-PH03-PAYMENT-RECONCILIATION | Provider lines are matched to internal allocations using scoped mapping and compared on gross, fee, commission, net, currency and status. | A reconciliation run executes. | Matches and discrepancies recorded. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PRC-002-01 | TEST (planned): matching test | DRAFT | UNKN-005 |
| SREQ-PH03-PRC-003 | REQ-PH03-PAYMENT-RECONCILIATION | Unmatched, amount, status and currency mismatches are recorded as discrepancy records and alerted without mutating payment state. | A mismatch is found. | Discrepancy record and alert exist. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-AUDIT | AC-PH03-PRC-003-01 | TEST (planned): discrepancy test | DRAFT | none recorded |
| SREQ-PH03-PRC-004 | REQ-PH03-PAYMENT-RECONCILIATION | Provider settlement reports are ingested when a report contract exists and incomplete runs are marked PARTIAL or FAILED. | A settlement report is available. | Run recorded. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PRC-004-01 | TEST (planned): ingestion test | OWNER_REVIEW | UNKN-005, ADR-016-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-PRC-001 | Resolve UNKNOWN | ACT-PLATFORM-ADMIN | FN-PAY-AUTHORIZE | FN-PAY-AUTHORIZE; ADR-013 |
| SREQ-PH03-PRC-002 | Allocation-level matching | ACT-PLATFORM-ADMIN | TBD (RGAP-PH03-001) | CMP-PAY-RECONCILIATION |
| SREQ-PH03-PRC-003 | Discrepancy classification | ACT-PLATFORM-ADMIN | TBD (RGAP-PH03-001) | CMP-PAY-RECONCILIATION |
| SREQ-PH03-PRC-004 | Settlement evidence ingestion | ACT-PLATFORM-ADMIN | TBD (RGAP-PH03-001) | CMP-PAY-RECONCILIATION |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-PRC-001-01 | SREQ-PH03-PRC-001 | Later definitive evidence drives exactly one transition. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | acceptance-test-plan.md item 4 | FN-PAY-AUTHORIZE; ADR-013 |
| AC-PH03-PRC-002-01 | SREQ-PH03-PRC-002 | An aggregate provider transaction is decomposed to allocations before comparison. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | CMP-PAY-RECONCILIATION §3.1 | CMP-PAY-RECONCILIATION |
| AC-PH03-PRC-003-01 | SREQ-PH03-PRC-003 | Each mismatch type is classified; no state is changed by reconciliation itself. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | CMP-PAY-RECONCILIATION §3.3, §1 | CMP-PAY-RECONCILIATION |
| AC-PH03-PRC-004-01 | SREQ-PH03-PRC-004 | Report absence or format change fails the run visibly and allows rerun. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | CMP-PAY-RECONCILIATION §5 | CMP-PAY-RECONCILIATION |

## 5. Alternate paths, failure, exception and uncertainty handling

- Report format and frequency are UNKNOWN until provider selection.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| IC-003 | Payment-provider webhook schema is provider-defined and may differ per provider; this does not define a settlement-report contract. | SREQ-PH03-PRC-001 |
| UNKN-005 | Settlement/commission model for platform transactions not defined. | SREQ-PH03-PRC-002, SREQ-PH03-PRC-004 |
| ADR-016-GATE | ADR-016 provider capabilities, commission/settlement policy, manual-payment approval flow are owner/finance/legal gates. | SREQ-PH03-PRC-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-001 | FN-ORD-CONFIRM covers inventory/stock commitment. FN-PAY-AUTHORIZE is linked for UNKNOWN-outcome resolution, but does not define reconciliation runs and allocation matching, discrepancy handling, settlement-report ingestion, or ledger/settlement. No canonical function covers cancellation/return coordination or refund/void. | Recorded in registry for the remaining uncovered behaviors; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH03-003 | Payment operations (authorize, capture, void, refund) are internal adapter/orchestrator commands in CMP-PAY-ADAPTER; no registered IF-* covers them; the webhook interface is provider-defined (IC-003). | Recorded here; route: provider selection and API Governance. |

## 7. Traceability sources

- c3-components/CNT-ACC-PAYMENT/CMP-PAY-RECONCILIATION.md
- functions/specs/FN-PAY-AUTHORIZE.md — §Flow step 4, §States (UNKNOWN outcome only)

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
