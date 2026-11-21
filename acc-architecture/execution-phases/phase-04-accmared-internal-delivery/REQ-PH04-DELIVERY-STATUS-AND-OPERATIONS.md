# REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS — Delivery status propagation and operations

**Document ID:** REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS |
| Phase ID | PH-04 |
| Title | Delivery status propagation and operations |
| Statement | Delivery state changes are published, reflected to buyers and sellers and audited, with operational indicators named without asserting service-level targets. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE, ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-DELIVERY, CNT-ACC-EVENTBUS, CNT-ACC-NOTIFICATIONS, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-ACC-DELIVERY §2, §7; CNT-ACC-NOTIFICATIONS; NFR-009; NFR-010 |

## 2. Scope boundary and phase handoffs

- Buyer status display extends REQ-PH03-BUYER-ORDER-VISIBILITY.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-DOP-001 | REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS | Shipment created, assigned and delivered events are published with the common envelope and correlation. | A shipment changes state. | Event published. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-EVENTBUS | AC-PH04-DOP-001-01 | TEST (planned): event contract test | DRAFT | IC-004 |
| SREQ-PH04-DOP-002 | REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS | Delivery status events trigger notifications to the affected buyer and seller. | A delivery event is published. | Parties are notified. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-NOTIFICATIONS | AC-PH04-DOP-002-01 | TEST (planned): notification test | OWNER_REVIEW | UNKN-001 |
| SREQ-PH04-DOP-003 | REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS | Assignments, status changes and proof submissions are audited. | A delivery operation occurs. | Audit record exists. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-AUDIT | AC-PH04-DOP-003-01 | TEST (planned): audit test | DRAFT | none recorded |
| SREQ-PH04-DOP-004 | REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS | The platform exposes the indicators unassigned orders, late tasks, failed deliveries and proof-of-delivery completion. | Operations review delivery health. | Indicators are measurable. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-AUDIT | AC-PH04-DOP-004-01 | TEST (planned): indicator test | OWNER_REVIEW | UNKN-001, ADR-022-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-DOP-001 | Delivery events | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE, ACT-PLATFORM-ADMIN | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §2 |
| SREQ-PH04-DOP-002 | Notifications to parties | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE, ACT-PLATFORM-ADMIN | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §2 |
| SREQ-PH04-DOP-003 | Audit of delivery operations | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE, ACT-PLATFORM-ADMIN | TBD (RGAP-PH04-001) | NFR-009 |
| SREQ-PH04-DOP-004 | Operational indicators | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE, ACT-PLATFORM-ADMIN | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §7 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-DOP-001-01 | SREQ-PH04-DOP-001 | Events carry the common envelope fields; names are per CNT-ACC-DELIVERY (not in the §5.5 catalogue). | RGAP-PH04-002 | CNT-ACC-DELIVERY §2; IF-ACC-EVENT-ENVELOPE §5.4 | CNT-ACC-DELIVERY §2 |
| AC-PH04-DOP-002-01 | SREQ-PH04-DOP-002 | Notification failure does not alter delivery state. | RGAP-PH04-002 | CNT-ACC-DELIVERY §2 | CNT-ACC-DELIVERY §2 |
| AC-PH04-DOP-003-01 | SREQ-PH04-DOP-003 | Each operation has an audit entry with actor and timestamp. | RGAP-PH04-002 | CNT-ACC-DELIVERY §2; NFR-009 | NFR-009 |
| AC-PH04-DOP-004-01 | SREQ-PH04-DOP-004 | Each indicator is measurable; no target value is asserted. | RGAP-PH04-005 | CNT-ACC-DELIVERY §7 | CNT-ACC-DELIVERY §7 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Delivery SLA values are UNKNOWN (UNKN-001).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| IC-004 | Message-broker technology, topics, partitioning, retention and ACL design unspecified. | SREQ-PH04-DOP-001 |
| UNKN-001 | SLA/availability targets per domain not defined (discovery-report.md). | SREQ-PH04-DOP-002, SREQ-PH04-DOP-004 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH04-DOP-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-002 | No registered IF-* or schema for delivery APIs; ShipmentCreated/Assigned/Delivered are named in CNT-ACC-DELIVERY §2 but absent from the §5.5 event catalogue; courier PATCH sync is described only in CNT-AMD-COURIER §6. | Recorded here; route: API Governance (IC-002). |
| RGAP-PH04-005 | Delivery failure, re-attempt, return-to-sender and recipient-absent flows have no source definition; returns are deferred (ODEC-007). | Recorded here; no behavior beyond the documented Pending Delivery rule is asserted. |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-DELIVERY.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
