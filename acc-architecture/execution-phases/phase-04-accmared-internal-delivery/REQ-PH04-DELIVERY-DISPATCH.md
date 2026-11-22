# REQ-PH04-DELIVERY-DISPATCH — Supervisor dispatch and assignment

**Document ID:** REQ-PH04-DELIVERY-DISPATCH  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-DELIVERY-DISPATCH |
| Phase ID | PH-04 |
| Title | Supervisor dispatch and assignment |
| Statement | Delivery supervisors see unassigned shipments for their fleet and assign or reassign couriers with auditable records. |
| Actors | ACT-DELIVERY-SUPERVISOR |
| Locations | SYS-ACCMARED-SUP, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-AMD-SUPERVISOR, CNT-ACC-DELIVERY, CNT-ACC-APIGATEWAY, CNT-ACC-EVENTBUS, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-AMD-SUPERVISOR; CNT-ACC-DELIVERY §2, §6; idea §2.1 |

## 2. Scope boundary and phase handoffs

- Prioritization, courier accept/reject and reassignment criteria have no source definition (RGAP-PH04-006).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-DSP-001 | REQ-PH04-DELIVERY-DISPATCH | A supervisor can list unassigned and in-progress shipments of their own fleet. | A supervisor opens the dispatch view. | Scoped shipments are listed. | SYS-ACCMARED-SUP, SYS-ACCSYSTEM | CNT-AMD-SUPERVISOR, CNT-ACC-DELIVERY, CNT-ACC-APIGATEWAY | AC-PH04-DSP-001-01 | TEST (planned): scope test | OWNER_REVIEW | none recorded |
| SREQ-PH04-DSP-002 | REQ-PH04-DELIVERY-DISPATCH | A supervisor assigns a courier to a shipment and the assignment is recorded and published. | Supervisor assigns a courier. | Assignment recorded with event. | SYS-ACCSYSTEM, SYS-ACCMARED-SUP | CNT-ACC-DELIVERY, CNT-AMD-SUPERVISOR, CNT-ACC-EVENTBUS, CNT-ACC-AUDIT | AC-PH04-DSP-002-01 | TEST (planned): assignment test | DRAFT | none recorded |
| SREQ-PH04-DSP-003 | REQ-PH04-DELIVERY-DISPATCH | A shipment can be reassigned while undelivered without losing history. | Supervisor reassigns. | New assignee with preserved history. | SYS-ACCSYSTEM, SYS-ACCMARED-SUP | CNT-ACC-DELIVERY, CNT-AMD-SUPERVISOR, CNT-ACC-AUDIT | AC-PH04-DSP-003-01 | TEST (planned): reassignment test | OWNER_REVIEW | none recorded |
| SREQ-PH04-DSP-004 | REQ-PH04-DELIVERY-DISPATCH | The supervisor app holds no delivery business logic; all decisions are made by Delivery Management. | Any supervisor action. | Decision made by the backend. | SYS-ACCMARED-SUP, SYS-ACCSYSTEM | CNT-AMD-SUPERVISOR, CNT-ACC-DELIVERY | AC-PH04-DSP-004-01 | REVIEW (planned): client design review | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-DSP-001 | Unassigned queue | ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | CNT-AMD-SUPERVISOR; CNT-ACC-DELIVERY §6 |
| SREQ-PH04-DSP-002 | Courier assignment | ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §2 |
| SREQ-PH04-DSP-003 | Reassignment | ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY |
| SREQ-PH04-DSP-004 | Thin client | ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | ADR-008 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-DSP-001-01 | SREQ-PH04-DSP-001 | Only the supervisor's fleet shipments are returned. | NOT SPECIFIED (source reference gap: RGAP-PH04-002) | CNT-ACC-DELIVERY §6 (ASSUMPTION) | CNT-AMD-SUPERVISOR; CNT-ACC-DELIVERY §6 |
| AC-PH04-DSP-002-01 | SREQ-PH04-DSP-002 | ShipmentAssigned is published and the assignment is audited with supervisor and courier. | NOT SPECIFIED (source reference gap: RGAP-PH04-002) | CNT-ACC-DELIVERY §2 | CNT-ACC-DELIVERY §2 |
| AC-PH04-DSP-003-01 | SREQ-PH04-DSP-003 | The previous assignment remains in history. | NOT SPECIFIED (source reference gap: RGAP-PH04-002) | CNT-ACC-DELIVERY §4 | CNT-ACC-DELIVERY |
| AC-PH04-DSP-004-01 | SREQ-PH04-DSP-004 | The app performs presentation only; rules reside in CNT-ACC-DELIVERY. | NOT SPECIFIED (source reference gap: RGAP-PH04-003) | CNT-AMD-SUPERVISOR; ADR-008 | ADR-008 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Assignment conflict (two supervisors): rule not defined in sources.

## 6. Open decisions and documented gaps

No `ADR-011-GATE` is assigned here: ADR-011 §1 and §3 cover platform-administrator and support access, and its second-approver rule applies only to operations later classified `HIGH_RISK`; the sources do not classify supervisor listing, assignment or reassignment that way. Supervisor-conflict and prioritization behavior remains unspecified as noted in §2; no approval policy is inferred.

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-002 | No registered IF-* or schema for delivery APIs; ShipmentCreated/Assigned/Delivered are named in CNT-ACC-DELIVERY §2 but absent from the §5.5 event catalogue; courier PATCH sync is described only in CNT-AMD-COURIER §6. | Recorded here; route: API Governance (IC-002). |
| RGAP-PH04-003 | C3 decomposition of CNT-ACC-DELIVERY and the ACCMared apps is an EXCEPTION deferred until the delivery provider model is defined. | Recorded here; CNT-ACC-DELIVERY §8; no C3 component references are used. |

## 7. Traceability sources

- c2-containers/accmared/CNT-AMD-SUPERVISOR.md
- c2-containers/accsystem/CNT-ACC-DELIVERY.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
