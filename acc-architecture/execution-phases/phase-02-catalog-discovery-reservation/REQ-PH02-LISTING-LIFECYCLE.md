# REQ-PH02-LISTING-LIFECYCLE — Listing update and withdrawal

**Document ID:** REQ-PH02-LISTING-LIFECYCLE  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-LISTING-LIFECYCLE |
| Phase ID | PH-02 |
| Title | Listing update and withdrawal |
| Statement | Published listings can be updated and withdrawn with versioned history, and a withdrawn listing is hidden from new buyers without altering history. |
| Actors | ACT-INST-EMPLOYEE |
| Locations | SYS-ACCORE, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACR-PRODUCTMASTER, CNT-ACC-CATALOG, CNT-ACR-CONNECTOR, CNT-ACC-SEARCH |
| Related function/use case | FN-INT-PUBLISH |
| Status | DRAFT |
| Evidence | FR-010; CMP-CAT-LISTING; dynamic-publication-flow.md §3 |

## 2. Scope boundary and phase handoffs

- Effects on in-flight orders belong to PH-03: order records retain immutable snapshots (FR-010 A1).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-LCY-001 | REQ-PH02-LISTING-LIFECYCLE | An update to a published product increments the listing version and applies once per version. | Employee modifies a published product. | A new listing version is current. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-PRODUCTMASTER, CNT-ACC-CATALOG, CNT-ACR-CONNECTOR | AC-PH02-LCY-001-01 | TEST (planned): update test | DRAFT | PUB-001, PUB-006 |
| SREQ-PH02-LCY-002 | REQ-PH02-LISTING-LIFECYCLE | Withdrawing a listing marks it withdrawn or inactive and retains its history. | Employee withdraws a listing. | The listing is inactive with history preserved. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-PRODUCTMASTER, CNT-ACC-CATALOG | AC-PH02-LCY-002-01 | TEST (planned): withdrawal test | DRAFT | PUB-006 |
| SREQ-PH02-LCY-003 | REQ-PH02-LISTING-LIFECYCLE | A withdrawn listing is excluded from results shown to new buyers. | A buyer searches or browses after withdrawal. | The listing is absent. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-SEARCH | AC-PH02-LCY-003-01 | TEST (planned): visibility test | DRAFT | PUB-006 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-LCY-001 | Versioned update | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-010 |
| SREQ-PH02-LCY-002 | Withdrawal retains history | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-010 |
| SREQ-PH02-LCY-003 | Withdrawn listings not shown | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-010 AC2 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-LCY-001-01 | SREQ-PH02-LCY-001 | Version increments on every published update; duplicate update events cause no conflicting state. | IF-ACR-PUBLISH-EVENT §8.4.1; §8.6 | FR-010 AC1/AC4 | FR-010 |
| AC-PH02-LCY-002-01 | SREQ-PH02-LCY-002 | A withdrawn listing is not deleted; its version chain remains. | IF-ACR-PUBLISH-EVENT §8.4.1 | FR-010; CMP-INT-PUBLICATION §3.3 | FR-010 |
| AC-PH02-LCY-003-01 | SREQ-PH02-LCY-003 | Search and detail views exclude withdrawn listings for new buyers. | IF-ACC-CATALOG-QUERY §1.4 | FR-010 AC2 | FR-010 AC2 |

## 5. Alternate paths, failure, exception and uncertainty handling

- A version lower than current has no listing-state effect under `FN-INT-PUBLISH` §3 P4 and `SREQ-PH02-ING-008`. A higher version arriving while an intermediate update may be missing is a different case; payload completeness and safe recovery remain open under `PUB-001`.
- Update payloads may remain distinct contract modes: a complete permitted projection can supersede a missing intermediate version only when completeness is guaranteed; `changed_fields` updates cannot be assumed complete and need contract-defined ordering or authoritative reconciliation before applying across a gap. The event/schema must identify the mode for each update; no global mode is selected.
- WITHDRAWN vs REMOVED state/event mapping is open (PUB-006).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| PUB-001 | Safe handling of a forward version gap (e.g. current v1 receives v3 while v2 may be missing). FN-INT-PUBLISH §4 and interface-contracts.md §8.3 describe `listing_data`; dynamic-publication-flow.md §3.1 describes `changed_fields`. No source establishes whether each update payload is complete or how a partial update is recovered. If v3 is a partial update applied across the gap, Catalog may miss fields changed only in v2. Distinct complete-projection and partial-update modes can coexist only when event/schema semantics make completeness explicit; no global choice is made. | SREQ-PH02-LCY-001 |
| PUB-006 | Mapping of publication/update/withdrawal events to Catalog states; rejected-update visibility and search effect. | SREQ-PH02-LCY-001, SREQ-PH02-LCY-002, SREQ-PH02-LCY-003 |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-010
- supporting-views/dynamic-publication-flow.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
