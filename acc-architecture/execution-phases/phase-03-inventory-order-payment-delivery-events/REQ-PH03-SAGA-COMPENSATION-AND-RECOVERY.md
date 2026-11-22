# REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY — Checkout saga persistence, compensation and recovery

**Document ID:** REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY |
| Phase ID | PH-03 |
| Title | Checkout saga persistence, compensation and recovery |
| Statement | The checkout/payment saga persists its state, resumes after failure and applies compensation only for confirmed effects, keeping unknown outcomes in explicit review states. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-ORDERS, CNT-ACR-OUTBOX, CNT-ACC-PAYMENT, CNT-ACC-INTEGRATION |
| Related function/use case | FN-ORD-CHECKOUT |
| Status | DRAFT |
| Evidence | FN-ORD-CHECKOUT; FR-009; ADR-006; ADR-018; CMP-ORD-STATEMACHINE; resilience-observability.md §1 |

## 2. Scope boundary and phase handoffs

- Release mechanics are the PH-02 reservation recovery capability; this document applies them to payment and confirmation failures.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-SAG-001 | REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY | Saga state is persisted before each external command so a restart resumes without repeating possible effects. | The orchestrator restarts mid-flow. | Flow resumes from persisted state. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-ORDERS, CNT-ACR-OUTBOX | AC-PH03-SAG-001-01 | TEST (planned): saga restart test (acceptance-test-plan.md item 12) | DRAFT | none recorded |
| SREQ-PH03-SAG-002 | REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY | Compensation (release, void, refund) is issued only for effects confirmed or reconciled, and never for unknown or ineligible ones. | A saga step fails. | Eligible compensation only. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-PAYMENT, CNT-ACC-INTEGRATION | AC-PH03-SAG-002-01 | TEST (planned): compensation guard test | DRAFT | RP-01, ADR-018-GATE |
| SREQ-PH03-SAG-003 | REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY | If the confirmation transaction fails after successful payment steps, no partial order exists and the saga retries or escalates with possible effects preserved. | Confirmation commit fails. | No partial order; recovery path. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-PAYMENT | AC-PH03-SAG-003-01 | TEST (planned): commit failure test | DRAFT | none recorded |
| SREQ-PH03-SAG-004 | REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY | Operational reconciliation timeouts move work to review states and never infer success, failure or release. | A reconciliation window lapses. | PENDING_REVIEW with evidence. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-SAG-004-01 | REVIEW (planned): operations review | OWNER_REVIEW | ADR-022-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-SAG-001 | Durable saga state | ACT-PLATFORM-ADMIN | FN-ORD-CHECKOUT | FN-ORD-CHECKOUT |
| SREQ-PH03-SAG-002 | Compensation only for confirmed effects | ACT-PLATFORM-ADMIN | FN-ORD-CHECKOUT | FR-009 AC4 |
| SREQ-PH03-SAG-003 | Confirmation write failure | ACT-PLATFORM-ADMIN | FN-ORD-CHECKOUT | FN-ORD-CONFIRM §7 |
| SREQ-PH03-SAG-004 | Review state not inferred | ACT-PLATFORM-ADMIN | FN-ORD-CHECKOUT | ADR-022; CMP-ORD-STATEMACHINE |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-SAG-001-01 | SREQ-PH03-SAG-001 | After a crash the saga resumes and issues no duplicate command. | IF-ACC-RESERVE-SAGA §3.6 | FN-ORD-CHECKOUT | FN-ORD-CHECKOUT |
| AC-PH03-SAG-002-01 | SREQ-PH03-SAG-002 | Definitive payment failure releases only eligible confirmed holds after reconciliation. | NOT SPECIFIED (source reference gap: RGAP-PH02-008) | FN-ORD-CHECKOUT; FR-009 AC4 | FR-009 AC4 |
| AC-PH03-SAG-003-01 | SREQ-PH03-SAG-003 | A failed commit leaves no partial order; capture/auth state is reconciled before any reversal. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | FN-ORD-CONFIRM §7 | FN-ORD-CONFIRM §7 |
| AC-PH03-SAG-004-01 | SREQ-PH03-SAG-004 | The state stays UNKNOWN/review and an alert is raised; window is a policy value. | NOT SPECIFIED (source reference gap: RGAP-PH01-007) | ADR-022 saga.reconciliation_window_seconds | ADR-022; CMP-ORD-STATEMACHINE |

## 5. Alternate paths, failure, exception and uncertainty handling

- Owner of operational runbooks for stuck sagas is unassigned.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-018-GATE | ADR-018 reservation TTL values and async-callback mode require per-institution approval. | SREQ-PH03-SAG-002 |
| RP-01 | Reservation timeout/UNKNOWN contradiction: technical alignment recorded, versioned institutional contract and executable evidence open. | SREQ-PH03-SAG-002 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH03-SAG-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-008 | Reservation release/cancel command has no schema in IF-ACC-RESERVE-SAGA §3.4 (only request/response bodies). | Recorded here; route: API Governance (RP-03). |
| RGAP-PH03-003 | Payment operations (authorize, capture, void, refund) are internal adapter/orchestrator commands in CMP-PAY-ADAPTER; no registered IF-* covers them; the webhook interface is provider-defined (IC-003). | Recorded here; route: provider selection and API Governance. |
| RGAP-PH01-007 | Policy store has no registered interface; ADR-022 §8 only names CNT-ACC-INSTREG as the policy-store container; approval-record mechanism unspecified. | Recorded here; route: technical ADR if implementation deviates (ADR-022 §4). |

## 7. Traceability sources

- functions/specs/FN-ORD-CHECKOUT.md
- supporting-views/resilience-observability.md §1

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
