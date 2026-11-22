# REQ-PH03-VOID-AND-REFUND — Void and refund operations

**Document ID:** REQ-PH03-VOID-AND-REFUND  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-VOID-AND-REFUND |
| Phase ID | PH-03 |
| Title | Void and refund operations |
| Statement | A void applies only to an uncaptured authorization and a refund only to a captured payment, each as a scoped idempotent operation that never exceeds the eligible allocation. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-PAYMENT, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH03-001) |
| Status | DRAFT |
| Evidence | CMP-PAY-REFUND; ADR-016; FR-008; FR-009 |

## 2. Scope boundary and phase handoffs

- Partial-refund policy and return/dispute capabilities are deferred (ODEC-007) and are not completed here.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-VRF-001 | REQ-PH03-VOID-AND-REFUND | Void is used only for an authoritatively uncaptured authorization and refund only for authoritatively captured funds. | A reversal is requested. | Correct operation chosen or held. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-VRF-001-01 | TEST (planned): void/refund test | DRAFT | none recorded |
| SREQ-PH03-VRF-002 | REQ-PH03-VOID-AND-REFUND | Each void or refund has an immutable operation identity bound to payment, allocation, amount and currency, and conflicting reuse is rejected or reviewed. | A reversal is issued or retried. | One effect. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-VRF-002-01 | TEST (planned): operation key test | DRAFT | ADR-016-GATE |
| SREQ-PH03-VRF-003 | REQ-PH03-VOID-AND-REFUND | Concurrent refunds cannot exceed the eligible remaining captured allocation; amount and eligibility follow approved policy. | Two refunds race. | Total never exceeds eligible. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-VRF-003-01 | TEST (planned): concurrent refund test | OWNER_REVIEW | ODEC-007, ADR-016-GATE |
| SREQ-PH03-VRF-004 | REQ-PH03-VOID-AND-REFUND | A failed or unknown refund is recorded and escalated without marking the captured attempt failed or repeating the effect. | Refund fails or response is lost. | Refund record failed/UNKNOWN; alert. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-AUDIT | AC-PH03-VRF-004-01 | TEST (planned): refund failure test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-VRF-001 | Void vs refund distinction | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | CMP-PAY-REFUND §3 |
| SREQ-PH03-VRF-002 | Scoped idempotent operation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | CMP-PAY-REFUND |
| SREQ-PH03-VRF-003 | Refund within eligible amount | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | CMP-PAY-REFUND §8 |
| SREQ-PH03-VRF-004 | Refund failure handling | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | CMP-PAY-REFUND §5 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-VRF-001-01 | SREQ-PH03-VRF-001 | A captured payment is never voided; in-flight capture remains UNKNOWN and is reconciled first. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | CMP-PAY-REFUND §3 | CMP-PAY-REFUND §3 |
| AC-PH03-VRF-002-01 | SREQ-PH03-VRF-002 | Retry after lost response reuses the key and causes no second effect. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | CMP-PAY-REFUND §3-§4 | CMP-PAY-REFUND |
| AC-PH03-VRF-003-01 | SREQ-PH03-VRF-003 | Atomic claim of the remaining allocation prevents over-refund. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | CMP-PAY-REFUND §3, §8 | CMP-PAY-REFUND §8 |
| AC-PH03-VRF-004-01 | SREQ-PH03-VRF-004 | The captured PaymentAttempt stays captured; RefundFailed alerts operations. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | IF-ACC-PAYMENT-WEBHOOK §4.4 | CMP-PAY-REFUND §5 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Provider support for void/refund is a capability gate; unsupported paths are blocked.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ODEC-007 | Returns and disputes capability (deferred; design pending). | SREQ-PH03-VRF-003 |
| ADR-016-GATE | ADR-016 provider capabilities, commission/settlement policy, manual-payment approval flow are owner/finance/legal gates. | SREQ-PH03-VRF-002, SREQ-PH03-VRF-003 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-001 | FN-ORD-CONFIRM covers inventory/stock commitment. FN-PAY-AUTHORIZE is linked for UNKNOWN-outcome resolution, but does not define reconciliation runs and allocation matching, discrepancy handling, settlement-report ingestion, or ledger/settlement. No canonical function covers cancellation/return coordination or refund/void. | Recorded in registry for the remaining uncovered behaviors; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH03-003 | Payment operations (authorize, capture, void, refund) are internal adapter/orchestrator commands in CMP-PAY-ADAPTER; no registered IF-* covers them; the webhook interface is provider-defined (IC-003). | Recorded here; route: provider selection and API Governance. |

## 7. Traceability sources

- c3-components/CNT-ACC-PAYMENT/CMP-PAY-REFUND.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
