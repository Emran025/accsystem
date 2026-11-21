# REQ-PH04-COURIER-OPERATIONS — Courier task handling and status updates

**Document ID:** REQ-PH04-COURIER-OPERATIONS  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-COURIER-OPERATIONS |
| Phase ID | PH-04 |
| Title | Courier task handling and status updates |
| Statement | Couriers authenticate, see only their assigned shipments and submit pickup, transit and delivery status updates that the backend validates and applies idempotently. |
| Actors | ACT-COURIER |
| Locations | SYS-ACCMARED-COU, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-AMD-COURIER, CNT-ACC-DELIVERY, CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-AMD-COURIER; CNT-ACC-DELIVERY §2, §6; idea §9 via CNT-AMD-COURIER |

## 2. Scope boundary and phase handoffs

- Offline queueing is specified in REQ-PH04-OFFLINE-COURIER-SYNC.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-CRO-001 | REQ-PH04-COURIER-OPERATIONS | A courier authenticates with short-lived tokens and can access only shipments assigned to them. | A courier opens their tasks. | Only assigned shipments are visible. | SYS-ACCMARED-COU, SYS-ACCSYSTEM | CNT-AMD-COURIER, CNT-ACC-DELIVERY, CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH04-CRO-001-01, AC-PH04-CRO-001-02 | TEST (planned): courier scope and binary review | DRAFT | ADR-011-GATE |
| SREQ-PH04-CRO-002 | REQ-PH04-COURIER-OPERATIONS | Pickup, in-transit and delivered updates are validated against the shipment state by Delivery Management, and invalid transitions are rejected. | A courier submits a status update. | Accepted or rejected by the backend. | SYS-ACCMARED-COU, SYS-ACCSYSTEM | CNT-AMD-COURIER, CNT-ACC-DELIVERY | AC-PH04-CRO-002-01 | TEST (planned): transition test | DRAFT | none recorded |
| SREQ-PH04-CRO-003 | REQ-PH04-COURIER-OPERATIONS | Repeating an identical status submission causes no duplicate effect. | An update is resubmitted. | One effect. | SYS-ACCSYSTEM, SYS-ACCMARED-COU | CNT-ACC-DELIVERY, CNT-AMD-COURIER | AC-PH04-CRO-003-01 | TEST (planned): duplicate submission test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-CRO-001 | Scoped courier access | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-AMD-COURIER §4 |
| SREQ-PH04-CRO-002 | Status updates validated server-side | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY |
| SREQ-PH04-CRO-003 | Idempotent submission | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-AMD-COURIER §6; CON-003 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-CRO-001-01 | SREQ-PH04-CRO-001 | Access to another courier's shipment is denied. | RGAP-PH04-002 | CNT-ACC-DELIVERY §6 (ASSUMPTION) | CNT-AMD-COURIER §4 |
| AC-PH04-CRO-001-02 | SREQ-PH04-CRO-001 | No service secrets are embedded in the app binary; tokens are stored securely. | RGAP-PH04-002 | CNT-AMD-COURIER §4 | CNT-AMD-COURIER §4 |
| AC-PH04-CRO-002-01 | SREQ-PH04-CRO-002 | An update for an unassigned or already-delivered shipment is rejected. | RGAP-PH04-002 | CNT-ACC-DELIVERY §1; CNT-AMD-COURIER §1 | CNT-ACC-DELIVERY |
| AC-PH04-CRO-003-01 | SREQ-PH04-CRO-003 | A duplicate PATCH yields the same state. | RGAP-PH04-002 | CNT-AMD-COURIER §6 | CNT-AMD-COURIER §6; CON-003 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Courier accept/reject of assignments is not defined in sources.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-011-GATE | ADR-011 approval flow (4-eyes) and session TTL policy keys not defined; assumption only. | SREQ-PH04-CRO-001 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-002 | No registered IF-* or schema for delivery APIs; ShipmentCreated/Assigned/Delivered are named in CNT-ACC-DELIVERY §2 but absent from the §5.5 event catalogue; courier PATCH sync is described only in CNT-AMD-COURIER §6. | Recorded here; route: API Governance (IC-002). |

## 7. Traceability sources

- c2-containers/accmared/CNT-AMD-COURIER.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
