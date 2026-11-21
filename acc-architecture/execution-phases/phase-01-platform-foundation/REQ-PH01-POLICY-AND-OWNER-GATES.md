# REQ-PH01-POLICY-AND-OWNER-GATES — Policy registry and owner-gate mechanism

**Document ID:** REQ-PH01-POLICY-AND-OWNER-GATES  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-POLICY-AND-OWNER-GATES |
| Phase ID | PH-01 |
| Title | Policy registry and owner-gate mechanism |
| Statement | Unresolved operational, provider, security and governance choices are held as versioned owner-approved policy values with fail-closed defaults so capabilities cannot be activated on unapproved values. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH01-007) |
| Status | DRAFT |
| Evidence | ADR-017; ADR-022; policy-and-gates.md; execution-phases/README.md §7; decisions/ADR-STAKEHOLDER-REVIEW-GATE.md |

## 2. Scope boundary and phase handoffs

- This document creates no policy value and approves no gate; it requires the mechanism only.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-POL-001 | REQ-PH01-POLICY-AND-OWNER-GATES | Thresholds, durations and policy values are read from a versioned policy store and are never hard-coded. | A service needs a threshold. | The value comes from the store. | SYS-ACCSYSTEM | CNT-ACC-INSTREG | AC-PH01-POL-001-01 | TEST (planned): policy change test | DRAFT | ADR-022-GATE |
| SREQ-PH01-POL-002 | REQ-PH01-POLICY-AND-OWNER-GATES | A capability whose required policy value is missing or lacks an owner approval record is not activated. | Production activation is attempted. | Activation is blocked. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN | AC-PH01-POL-002-01 | TEST (planned): onboarding gate test | DRAFT | ADR-017-GATE |
| SREQ-PH01-POL-003 | REQ-PH01-POLICY-AND-OWNER-GATES | Approved policy snapshots are immutable and consumers record the snapshot version they used. | A policy value is approved or consumed. | History is unaltered. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-AUDIT | AC-PH01-POL-003-01 | TEST (planned): snapshot immutability test | DRAFT | ADR-022-GATE |
| SREQ-PH01-POL-004 | REQ-PH01-POLICY-AND-OWNER-GATES | Each unresolved decision has a named owner function, activation condition and approval record, and stays visible rather than converted to success. | A gated decision is pending. | It is listed with owner and condition. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN | AC-PH01-POL-004-01 | REVIEW (planned): gate register review | OWNER_REVIEW | GATE-STAKEHOLDER |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-POL-001 | Externalized thresholds | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-007) | ADR-022 |
| SREQ-PH01-POL-002 | Fail-closed activation | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-007) | ADR-017; ADR-022 |
| SREQ-PH01-POL-003 | Immutable policy snapshots | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-007) | ADR-017 |
| SREQ-PH01-POL-004 | Visible owner gates | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-007) | policy-and-gates.md |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-POL-001-01 | SREQ-PH01-POL-001 | Changing an approved value needs no code change; each threshold names an owner function. | RGAP-PH01-007 | ADR-022 §3 | ADR-022 |
| AC-PH01-POL-002-01 | SREQ-PH01-POL-002 | Activation without an approved value is blocked. | RGAP-PH01-007 | ADR-022 §6; ADR-017 | ADR-017; ADR-022 |
| AC-PH01-POL-003-01 | SREQ-PH01-POL-003 | Later edits create new versions; earlier use remains traceable. | RGAP-PH01-007 | ADR-017; ADR-022 | ADR-017 |
| AC-PH01-POL-004-01 | SREQ-PH01-POL-004 | Gate register lists owner and condition; no gate is shown resolved without an approval record. | RGAP-PH01-007 | policy-and-gates.md; GATE-STAKEHOLDER | policy-and-gates.md |

## 5. Alternate paths, failure, exception and uncertainty handling

- Many owners are OWNER_UNASSIGNED in the source; assignment is an owner action outside this draft.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-POL-001, SREQ-PH01-POL-003 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH01-POL-002 |
| GATE-STAKEHOLDER | decisions/ADR-STAKEHOLDER-REVIEW-GATE.md: all ADRs PROPOSED; sign-off pending; no stakeholder approval recorded. | SREQ-PH01-POL-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-007 | Policy store has no registered interface; ADR-022 §8 only names CNT-ACC-INSTREG as the policy-store container; approval-record mechanism unspecified. | Recorded here; route: technical ADR if implementation deviates (ADR-022 §4). |

## 7. Traceability sources

- decisions/ADR-017.md, ADR-022.md
- supporting-views/policy-and-gates.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
