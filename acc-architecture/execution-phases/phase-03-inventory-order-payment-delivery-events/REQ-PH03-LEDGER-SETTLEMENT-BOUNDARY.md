# REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY — Payment ledger and settlement boundary

**Document ID:** REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY |
| Phase ID | PH-03 |
| Title | Payment ledger and settlement boundary |
| Statement | Platform payment facts are kept in an append-only ledger distinct from seller credit, commission and settlement, while ownership of settlement remains an unresolved owner gate. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-PAYMENT, CNT-ACC-AUDIT, CNT-ACC-INSTREG |
| Related function/use case | TBD (RGAP-PH03-004) |
| Status | DRAFT |
| Evidence | financial-ledger-and-settlement.md; ADR-016; ODEC-006; UNKN-005; CNT-ACC-PAYMENT |

## 2. Scope boundary and phase handoffs

- No settlement, payout, commission or seller-credit requirement is created because the source assigns no owner or policy (RGAP-PH03-004).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-LDG-001 | REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY | Payment facts (authorization, capture, void, refund, provider references) are recorded in append-only ledger entries with a reason. | A payment event occurs. | An entry is appended. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-AUDIT | AC-PH03-LDG-001-01 | REVIEW (planned): ledger design review | OWNER_REVIEW | ADR-016-GATE |
| SREQ-PH03-LDG-002 | REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY | Capture creates no automatic seller credit; any credit or settlement state follows only an approved policy. | A payment is captured. | No implied credit. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-LDG-002-01 | REVIEW (planned): finance owner review | OWNER_REVIEW | UNKN-005, ODEC-006, ADR-016-GATE |
| SREQ-PH03-LDG-003 | REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY | A payment completed outside the platform is recorded as RecordedOutsidePlatform only by an authorized actor under approved controls and is never presented as platform-captured. | An authorized actor records an external payment. | Distinct, auditable record. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-AUDIT | AC-PH03-LDG-003-01 | REVIEW (planned): control review | OWNER_REVIEW | ADR-016-GATE |
| SREQ-PH03-LDG-004 | REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY | Settlement and commission domain decisions remain visible open gates and block activation of dependent behavior. | A dependent capability is activated. | Blocked until approved. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-INSTREG | AC-PH03-LDG-004-01 | REVIEW (planned): gate review | OWNER_REVIEW | UNKN-005, ODEC-006, ADR-017-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-LDG-001 | Append-only payment facts | ACT-PLATFORM-ADMIN | TBD (RGAP-PH03-004) | financial-ledger-and-settlement.md |
| SREQ-PH03-LDG-002 | Seller credit separate from capture | ACT-PLATFORM-ADMIN | FN-PAY-AUTHORIZE | FN-PAY-AUTHORIZE; ADR-016; ODEC-006 |
| SREQ-PH03-LDG-003 | Manual or external payment recorded | ACT-PLATFORM-ADMIN | TBD (RGAP-PH03-004) | ADR-016 |
| SREQ-PH03-LDG-004 | Unresolved settlement visible | ACT-PLATFORM-ADMIN | TBD (RGAP-PH03-004) | ADR-017 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-LDG-001-01 | SREQ-PH03-LDG-001 | Entries are not updated or deleted; corrections are reversing entries. | NOT SPECIFIED (source reference gap: RGAP-PH03-004) | financial-ledger-and-settlement.md | financial-ledger-and-settlement.md |
| AC-PH03-LDG-002-01 | SREQ-PH03-LDG-002 | No credit or payout is created by capture alone. | NOT SPECIFIED (no seller-credit API/event contract is specified) | FN-PAY-AUTHORIZE § Flow step 3 | FN-PAY-AUTHORIZE § Flow step 3; ADR-016; ODEC-006 |
| AC-PH03-LDG-003-01 | SREQ-PH03-LDG-003 | The record is distinct from captured payments and audited with actor and approval. | NOT SPECIFIED (source reference gap: RGAP-PH03-010) | ADR-016 | ADR-016 |
| AC-PH03-LDG-004-01 | SREQ-PH03-LDG-004 | No settlement-dependent behavior is activated without approved owner values. | NOT SPECIFIED (source reference gap: RGAP-PH01-007) | ADR-017; policy-and-gates.md | ADR-017 |

## 5. Alternate paths, failure, exception and uncertainty handling

- The source lists a Settlement boundary as proposed with unassigned owner; this draft does not create it.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-016-GATE | ADR-016 provider capabilities, commission/settlement policy, manual-payment approval flow are owner/finance/legal gates. | SREQ-PH03-LDG-001, SREQ-PH03-LDG-002, SREQ-PH03-LDG-003 |
| UNKN-005 | Settlement/commission model for platform transactions not defined. | SREQ-PH03-LDG-002, SREQ-PH03-LDG-004 |
| ODEC-006 | Settlement/commission domain scope. | SREQ-PH03-LDG-002, SREQ-PH03-LDG-004 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH03-LDG-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-004 | FN-PAY-AUTHORIZE establishes that capture does not itself mean seller credit or settlement, but no canonical function, registered container or assigned owner covers ledger entries, seller credit, commission or settlement; CNT-ACC-PAYMENT remains interim reconciliation only. | Owner gate recorded here. CNT-ACC-PAYMENT is used as the interim container for evidence matching only; no ownership of seller credit or commission is implied. |
| RGAP-PH03-010 | No interface defines manual/externally completed payment recording (RecordedOutsidePlatform) or its approval workflow. | Recorded here; ADR-016 gate. |
| RGAP-PH01-007 | Policy store has no registered interface; ADR-022 §8 only names CNT-ACC-INSTREG as the policy-store container; approval-record mechanism unspecified. | Recorded here; route: technical ADR if implementation deviates (ADR-022 §4). |

## 7. Traceability sources

- supporting-views/financial-ledger-and-settlement.md
- decisions/ADR-016.md
- functions/specs/FN-PAY-AUTHORIZE.md — §Flow step 3 (capture is not seller credit/settlement)

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
