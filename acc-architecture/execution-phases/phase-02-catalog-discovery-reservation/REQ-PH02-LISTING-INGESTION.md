# REQ-PH02-LISTING-INGESTION — Listing admission, validation and creation at ACCSystem

**Document ID:** REQ-PH02-LISTING-INGESTION  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-LISTING-INGESTION |
| Phase ID | PH-02 |
| Title | Listing admission, validation and creation at ACCSystem |
| Statement | ACCSystem admits publication submissions only for active authenticated institutions, validates them, and creates or updates the Catalog-owned marketplace listing idempotently without treating it as the source of truth. |
| Actors | ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-INTEGRATION, CNT-ACC-INSTREG, CNT-ACC-CATALOG, CNT-ACC-SOFTCAT, CNT-ACR-CONNECTOR, CNT-ACC-AUDIT |
| Related function/use case | FN-INT-PUBLISH |
| Status | DRAFT |
| Evidence | FR-001; FN-INT-PUBLISH §4-§7; ADR-004; CMP-INT-PUBLICATION; CMP-CAT-LISTING; CMP-CAT-VALIDATION |

## 2. Scope boundary and phase handoffs

- Acceptance receipt is not proof of listing creation or indexing (FN-INT-PUBLISH §4 step 8).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-ING-001 | REQ-PH02-LISTING-INGESTION | The gateway admits a submission only when the institution is registered and Active, authenticated, and the payload is well-formed. | A publication submission arrives. | Admitted or rejected before any listing effect. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION, CNT-ACC-INSTREG | AC-PH02-ING-001-01, AC-PH02-ING-001-02 | TEST (planned): admission test | DRAFT | none recorded |
| SREQ-PH02-ING-002 | REQ-PH02-LISTING-INGESTION | A definitive pre-admission rejection records the rejected attempt with its reason and creates or mutates no listing. | Validation or permission fails. | Structured non-success and recorded attempt. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION, CNT-ACC-CATALOG | AC-PH02-ING-002-01 | TEST (planned): rejection test | DRAFT | PUB-005 |
| SREQ-PH02-ING-003 | REQ-PH02-LISTING-INGESTION | Catalog validates the publication against content policy rules and returns a verdict with reasons before a listing is written. | Accepted work reaches Catalog. | PASS or FAIL with violations. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-SOFTCAT | AC-PH02-ING-003-01 | TEST (planned): validation rule test | DRAFT | PUB-004, PUB-006 |
| SREQ-PH02-ING-004 | REQ-PH02-LISTING-INGESTION | Catalog creates or updates the listing once per institution/product/version; completed duplicates return the recorded outcome and stale versions are ignored. | A validated publication or its duplicate is processed. | One listing effect; stable listing_id. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-INTEGRATION | AC-PH02-ING-004-01, AC-PH02-ING-004-02 | TEST (planned): duplicate/version test | RETIRED | PUB-001, PUB-005 |
| SREQ-PH02-ING-005 | REQ-PH02-LISTING-INGESTION | A Catalog-owned listing_id is retained stably across updates and reported to ACCore under the approved receipt contract. | A publication is accepted. | ACCore can learn the listing_id. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-CATALOG, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH02-ING-005-01 | REVIEW (planned): receipt contract review | OWNER_REVIEW | PUB-005 |
| SREQ-PH02-ING-006 | REQ-PH02-LISTING-INGESTION | Approved and rejected publication admissions are audited. | An admission decision is made. | An audit record exists. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION, CNT-ACC-AUDIT | AC-PH02-ING-006-01 | TEST (planned): audit test | DRAFT | none recorded |
| SREQ-PH02-ING-007 | REQ-PH02-LISTING-INGESTION | Catalog creates or updates a listing once per institution/product/version; a completed duplicate returns its recorded outcome. | A validated publication or its completed duplicate is processed. | There is one listing effect per institution/product/version and a completed duplicate returns its recorded outcome. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-INTEGRATION | AC-PH02-ING-007-01 | TEST (planned): duplicate listing idempotency test | DRAFT | PUB-005 |
| SREQ-PH02-ING-008 | REQ-PH02-LISTING-INGESTION | Catalog ignores a publication version lower than the current listing version. | Catalog receives a publication with a version lower than the current listing version. | The stale publication does not change the current listing. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-INTEGRATION | AC-PH02-ING-008-01 | TEST (planned): stale listing version test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-ING-001 | Admission checks | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FN-INT-PUBLISH; FR-012 AC2 |
| SREQ-PH02-ING-002 | Pre-admission rejection leaves no listing | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-001 A1; FN-INT-PUBLISH §5 |
| SREQ-PH02-ING-003 | Content validation | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | CMP-CAT-VALIDATION |
| SREQ-PH02-ING-004 | Idempotent listing creation | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-001 AC3; FN-INT-PUBLISH §6.2 |
| SREQ-PH02-ING-005 | Listing identifier and receipt | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-001 AC1; FN-INT-PUBLISH §4 step 8 |
| SREQ-PH02-ING-006 | Audit of admission decisions | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | NFR-009; FN-INT-PUBLISH §8 |
| SREQ-PH02-ING-007 | Idempotent listing application | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-001 AC3; FN-INT-PUBLISH §6.2; IF-ACR-PUBLISH-EVENT §8.6 |
| SREQ-PH02-ING-008 | Ignore stale listing versions | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FN-INT-PUBLISH §3 P4; IF-ACR-PUBLISH-EVENT §8.4.1 |

## 4. Acceptance criteria

### Cycle 4 preservation and decomposition record

`SREQ-PH02-ING-004` and its two original criteria remain unchanged as a `RETIRED` source record. `ING-007` covers same-key duplicate listing outcome; `ING-008` covers the specified no-effect rule for a version below current (`FN-INT-PUBLISH` §3 P4). `PUB-005` remains open for receipt/duplicate-response representation. `PUB-001` remains open only for a higher version arriving while an intermediate update may be missing: the artifacts describe `listing_data` and `changed_fields` without establishing snapshot completeness. Its active lifecycle impact is mapped to `REQ-PH02-LISTING-LIFECYCLE` / `SREQ-PH02-LCY-001`. No response schema or global ordering policy is added.


| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-ING-001-01 | SREQ-PH02-ING-001 | Unknown or non-Active institution yields 403; malformed payload yields 400/422. | IF-ACR-PUBLISH-EVENT §8.7 | FN-INT-PUBLISH §3 P1-P2 | FN-INT-PUBLISH; FR-012 AC2 |
| AC-PH02-ING-001-02 | SREQ-PH02-ING-001 | Payload institution_id must match the authenticated binding. | IF-ACR-PUBLISH-EVENT §8.8 | FN-INT-PUBLISH §8 | FN-INT-PUBLISH; FR-012 AC2 |
| AC-PH02-ING-002-01 | SREQ-PH02-ING-002 | No listing is created or changed; a structured reason code is returned and ACCore can correct and resubmit. | IF-ACR-PUBLISH-EVENT §8.7 | FR-001 A1/AC5 | FR-001 A1; FN-INT-PUBLISH §5 |
| AC-PH02-ING-003-01 | SREQ-PH02-ING-003 | Violations are listed by rule; text fields are sanitized. | NOT SPECIFIED (source reference gap: RGAP-PH02-001) | CMP-CAT-VALIDATION §3; FN-INT-PUBLISH §8 | CMP-CAT-VALIDATION |
| AC-PH02-ING-004-01 | SREQ-PH02-ING-004 | A duplicate event with the same key creates no duplicate listing. | IF-ACR-PUBLISH-EVENT §8.6 | FR-001 AC3 | FR-001 AC3; FN-INT-PUBLISH §6.2 |
| AC-PH02-ING-004-02 | SREQ-PH02-ING-004 | A lower version than current is silently ignored. | IF-ACR-PUBLISH-EVENT §8.4.1 | FN-INT-PUBLISH §3 P4 | FR-001 AC3; FN-INT-PUBLISH §6.2 |
| AC-PH02-ING-005-01 | SREQ-PH02-ING-005 | listing_id is unchanged across updates. | IF-ACR-PUBLISH-EVENT §8.4.1 | FR-001 AC1 | FR-001 AC1; FN-INT-PUBLISH §4 step 8 |
| AC-PH02-ING-006-01 | SREQ-PH02-ING-006 | Each approved and rejected publication has an audit entry. | NOT SPECIFIED (source reference gap: RGAP-PH01-004) | FN-INT-PUBLISH §8 | NFR-009; FN-INT-PUBLISH §8 |
| AC-PH02-ING-007-01 | SREQ-PH02-ING-007 | A duplicate event with the same key creates no duplicate listing; a completed duplicate returns its recorded outcome. | IF-ACR-PUBLISH-EVENT §8.6 | FR-001 AC3; FN-INT-PUBLISH §6.2 | FR-001 AC3; FN-INT-PUBLISH §6.2 |
| AC-PH02-ING-008-01 | SREQ-PH02-ING-008 | A publication version lower than the current listing version is ignored without changing the current listing. | IF-ACR-PUBLISH-EVENT §8.4.1 | FN-INT-PUBLISH §3 P4 | FR-001 AC3; FN-INT-PUBLISH §6.2 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Catalog moderation rejection and its effect on a previous ACTIVE version are open (PUB-006).
- Search sync failure leaves the listing ACTIVE but not searchable (see REQ-PH02-PUBLICATION-RECOVERY).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| PUB-005 | Acceptance receipt vs queued Catalog-owned listing_id, in-progress duplicate response, rejected-attempt representation. | SREQ-PH02-ING-002, SREQ-PH02-ING-004 (historical), SREQ-PH02-ING-007, SREQ-PH02-ING-005 |
| PUB-004 | Which listing fields are permitted for publication is not defined. | SREQ-PH02-ING-003 |
| PUB-006 | Mapping of publication/update/withdrawal events to Catalog states; rejected-update visibility and search effect. | SREQ-PH02-ING-003 |
| PUB-001 | Safe handling of a higher version arriving while an intermediate update may be missing; event-payload completeness is unresolved. | SREQ-PH02-ING-004 (historical); active lifecycle impact: REQ-PH02-LISTING-LIFECYCLE / SREQ-PH02-LCY-001 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-001 | functions/function-catalog.md has no FN-* for browsing, search, offer presentation or cart preparation (only FN-INT-PUBLISH, FN-ORD-CHECKOUT, FN-ORD-RESERVE exist). | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH01-004 | No registered IF-* contract or AuditEvent schema for audit write/query. | Recorded in this document; CNT-ACC-AUDIT lists no interface. Route: API Governance (IC-002). |

## 7. Traceability sources

- functions/specs/FN-INT-PUBLISH.md
- c3-components/CNT-ACC-INTEGRATION/CMP-INT-PUBLICATION.md
- c3-components/CNT-ACC-CATALOG/

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
