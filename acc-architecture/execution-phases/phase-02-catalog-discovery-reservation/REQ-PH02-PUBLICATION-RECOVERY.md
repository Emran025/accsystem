# REQ-PH02-PUBLICATION-RECOVERY — Publication and search-sync recovery

**Document ID:** REQ-PH02-PUBLICATION-RECOVERY  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-PUBLICATION-RECOVERY |
| Phase ID | PH-02 |
| Title | Publication and search-sync recovery |
| Statement | Failures between ACCore, Catalog and the derived search index are retried and reconciled without duplicating listing effects or claiming completion that did not occur. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-CATALOG, CNT-ACC-SEARCH, CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION, CNT-ACR-OUTBOX, CNT-ACR-CONNECTOR |
| Related function/use case | FN-INT-PUBLISH |
| Status | DRAFT |
| Evidence | FN-INT-PUBLISH §7; CMP-CAT-SEARCHSYNC; CNT-ACC-SEARCH §6; resilience-observability.md §4 |

## 2. Scope boundary and phase handoffs

- Operations roles and runbook ownership are open (see REQ-PH01-OBSERVABILITY-AND-RECOVERY).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-REC-001 | REQ-PH02-PUBLICATION-RECOVERY | Search index updates are applied asynchronously from approved Catalog state, retried on failure and tracked per listing version. | A listing event requires an index update. | Index converges to Catalog state. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-SEARCH | AC-PH02-REC-001-01 | TEST (planned): sync failure test | DRAFT | none recorded |
| SREQ-PH02-REC-002 | REQ-PH02-PUBLICATION-RECOVERY | A committed Catalog write whose event relay fails is retried or reconciled without claiming downstream completion. | Event relay fails after commit. | Intent is retained and retried. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION | AC-PH02-REC-002-01 | TEST (planned): relay recovery test | DRAFT | IC-004 |
| SREQ-PH02-REC-003 | REQ-PH02-PUBLICATION-RECOVERY | The search index can be rebuilt from Catalog data and verified against it. | Index inconsistency is detected. | Index matches Catalog source. | SYS-ACCSYSTEM | CNT-ACC-SEARCH, CNT-ACC-CATALOG | AC-PH02-REC-003-01 | TEST (planned): reindex test (acceptance-test-plan.md item 12) | OWNER_REVIEW | none recorded |
| SREQ-PH02-REC-004 | REQ-PH02-PUBLICATION-RECOVERY | Rejected and failed publications remain visible to operations and to ACCore for correction and resubmission. | A publication is rejected or fails. | Failure is recorded and visible. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-OUTBOX, CNT-ACR-CONNECTOR | AC-PH02-REC-004-01 | TEST (planned): resubmission test | DRAFT | PUB-005 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-REC-001 | Search sync retry | ACT-PLATFORM-ADMIN | FN-INT-PUBLISH | FN-INT-PUBLISH §7 |
| SREQ-PH02-REC-002 | Relay recovery | ACT-PLATFORM-ADMIN | FN-INT-PUBLISH | FN-INT-PUBLISH §6.1 |
| SREQ-PH02-REC-003 | Index rebuild | ACT-PLATFORM-ADMIN | FN-INT-PUBLISH | CNT-ACC-SEARCH §1 |
| SREQ-PH02-REC-004 | Failed publication visibility | ACT-PLATFORM-ADMIN | FN-INT-PUBLISH | FN-INT-PUBLISH §7 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-REC-001-01 | SREQ-PH02-REC-001 | A sync failure leaves the listing ACTIVE but unsearchable and is retried. | RGAP-PH02-006 | FN-INT-PUBLISH §7; CMP-CAT-SEARCHSYNC §3 | FN-INT-PUBLISH §7 |
| AC-PH02-REC-002-01 | SREQ-PH02-REC-002 | The durable event intent survives restart; retries/DLQ do not duplicate listing effects. | IF-ACC-EVENT-ENVELOPE §5.6 | FN-INT-PUBLISH §7 | FN-INT-PUBLISH §6.1 |
| AC-PH02-REC-003-01 | SREQ-PH02-REC-003 | Replaying source events with idempotency restores the index. | RGAP-PH02-006 | resilience-observability.md §4; CNT-ACC-SEARCH §1 | CNT-ACC-SEARCH §1 |
| AC-PH02-REC-004-01 | SREQ-PH02-REC-004 | A FAILED outbox state exists for definitive errors and allows resubmission. | IF-ACR-PUBLISH-EVENT §8.7 | FN-INT-PUBLISH §4 step 9 | FN-INT-PUBLISH §7 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Institution notification of rejection is an ASSUMPTION in the source.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| IC-004 | Message-broker technology, topics, partitioning, retention and ACL design unspecified. | SREQ-PH02-REC-002 |
| PUB-005 | Acceptance receipt vs queued Catalog-owned listing_id, in-progress duplicate response, rejected-attempt representation. | SREQ-PH02-REC-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-006 | The search API (GET /v1/catalog/products) is not a registered IF-*; relation to IF-ACC-CATALOG-QUERY is an OPEN separate spec (interface-contracts.md §1.9). | Recorded here; route: API Governance. |

## 7. Traceability sources

- functions/specs/FN-INT-PUBLISH.md §7
- supporting-views/resilience-observability.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
