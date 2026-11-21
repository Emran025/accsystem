# REQ-PH04-PROOF-OF-DELIVERY — Proof of delivery capture and integrity

**Document ID:** REQ-PH04-PROOF-OF-DELIVERY  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-PROOF-OF-DELIVERY |
| Phase ID | PH-04 |
| Title | Proof of delivery capture and integrity |
| Statement | A delivery is completed with a tamper-evident proof-of-delivery record whose fields and handling follow an approved definition. |
| Actors | ACT-COURIER, ACT-DELIVERY-SUPERVISOR |
| Locations | SYS-ACCSYSTEM, SYS-ACCMARED-COU |
| Primary C4 containers | CNT-ACC-DELIVERY, CNT-AMD-COURIER, CNT-ACC-AUDIT, CNT-ACC-IDENTITY |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-ACC-DELIVERY §4, §6; CNT-AMD-COURIER §6; UNKN-002 |

## 2. Scope boundary and phase handoffs

- Exact fields are UNKNOWN (RGAP-PH04-004); only photo, signature reference and geolocation are named.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-POD-001 | REQ-PH04-PROOF-OF-DELIVERY | A shipment is marked delivered only with the proof-of-delivery record required by the approved definition. | A courier marks a shipment delivered. | Delivered only with the required POD. | SYS-ACCSYSTEM, SYS-ACCMARED-COU | CNT-ACC-DELIVERY, CNT-AMD-COURIER | AC-PH04-POD-001-01 | TEST (planned): POD requirement test | OWNER_REVIEW | UNKN-002, ADR-008-GATE |
| SREQ-PH04-POD-002 | REQ-PH04-PROOF-OF-DELIVERY | Proof-of-delivery records are tamper-evident and not editable after submission. | A POD is stored. | Alteration is detectable. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-AUDIT | AC-PH04-POD-002-01 | REVIEW (planned): storage review | DRAFT | none recorded |
| SREQ-PH04-POD-003 | REQ-PH04-PROOF-OF-DELIVERY | Photo, signature and geolocation data are handled under the approved privacy and retention rules and exposed only to authorized parties. | POD data is stored or read. | Access is limited. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-IDENTITY | AC-PH04-POD-003-01 | REVIEW (planned): privacy review | OWNER_REVIEW | UNKN-002 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-POD-001 | POD required to complete | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §4 |
| SREQ-PH04-POD-002 | Tamper-evident POD | ACT-COURIER, ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §6 |
| SREQ-PH04-POD-003 | POD data protection | ACT-COURIER, ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | UNKN-002; CNT-ACC-DELIVERY §4 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-POD-001-01 | SREQ-PH04-POD-001 | Delivered without the required proof is rejected; the required set is an approved policy value. | RGAP-PH04-004 | CNT-ACC-DELIVERY §4 | CNT-ACC-DELIVERY §4 |
| AC-PH04-POD-002-01 | SREQ-PH04-POD-002 | No edit path exists for a stored POD; integrity check detects change. | RGAP-PH04-004 | CNT-ACC-DELIVERY §6 (ASSUMPTION) | CNT-ACC-DELIVERY §6 |
| AC-PH04-POD-003-01 | SREQ-PH04-POD-003 | Unauthorized roles cannot read POD data; retention follows approved policy (none asserted). | RGAP-PH04-004 | UNKN-002 | UNKN-002; CNT-ACC-DELIVERY §4 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Disputed deliveries depend on the deferred returns/disputes design (ODEC-007).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-002 | Compliance/data-residency/retention framework (PCI-DSS, privacy, audit retention) not defined. | SREQ-PH04-POD-001, SREQ-PH04-POD-003 |
| ADR-008-GATE | ADR-008 offline courier strategy and delivery provider scope unknown. | SREQ-PH04-POD-001 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-004 | Exact proof-of-delivery fields, retention and privacy handling are UNKNOWN (photo, signature reference, geolocation named only). | Recorded here; UNKN-002 owner gate. |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-DELIVERY.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
