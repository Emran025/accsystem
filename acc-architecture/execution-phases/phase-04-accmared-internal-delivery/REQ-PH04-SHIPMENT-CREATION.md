# REQ-PH04-SHIPMENT-CREATION — Shipment creation from confirmed orders

**Document ID:** REQ-PH04-SHIPMENT-CREATION  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-SHIPMENT-CREATION |
| Phase ID | PH-04 |
| Title | Shipment creation from confirmed orders |
| Statement | A confirmed order with physical items triggers idempotent shipment creation, with software-only orders creating none and creation failure leaving the order confirmed in a retried Pending Delivery state. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-DELIVERY, CNT-ACC-ORDERS, CNT-ACC-EVENTBUS |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-ACC-DELIVERY §2, §5; FR-002; idea §7.5 via CNT-ACC-DELIVERY; ADR-013 |

## 2. Scope boundary and phase handoffs

- Delivery state never changes order confirmation (ADR-013).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-SHP-001 | REQ-PH04-SHIPMENT-CREATION | Delivery Management creates one or more shipments from OrderConfirmed for physical items, linked to order_id and seller_order_id. | OrderConfirmed with physical items is consumed. | Shipment records exist. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS, CNT-ACC-EVENTBUS | AC-PH04-SHP-001-01 | TEST (planned): shipment creation test | DRAFT | ADR-008-GATE |
| SREQ-PH04-SHP-002 | REQ-PH04-SHIPMENT-CREATION | A replayed OrderConfirmed does not create duplicate shipments. | The confirmation event is redelivered. | No extra shipment. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY | AC-PH04-SHP-002-01 | TEST (planned): duplicate event test | DRAFT | none recorded |
| SREQ-PH04-SHP-003 | REQ-PH04-SHIPMENT-CREATION | An order containing only licensed software creates no shipment. | OrderConfirmed has no physical lines. | No shipment. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY | AC-PH04-SHP-003-01 | TEST (planned): software-only test | DRAFT | none recorded |
| SREQ-PH04-SHP-004 | REQ-PH04-SHIPMENT-CREATION | If shipment creation fails after confirmation the order stays confirmed with Pending Delivery and creation is retried. | Shipment creation fails. | Order stays confirmed; retry occurs. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS | AC-PH04-SHP-004-01 | TEST (planned): creation failure test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-SHP-001 | Create from OrderConfirmed | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §2, §4 |
| SREQ-PH04-SHP-002 | Idempotent creation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH04-001) | CON-003 |
| SREQ-PH04-SHP-003 | Software-only orders | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH04-001) | FN-LIC-ACTIVATE; CNT-ACC-DELIVERY |
| SREQ-PH04-SHP-004 | Pending Delivery with retry | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §5; ADR-013 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-SHP-001-01 | SREQ-PH04-SHP-001 | A shipment record holds {shipment_id, order_id, seller_order_id, courier_id, status, proof_of_delivery_ref, created_at}. | RGAP-PH04-002 | CNT-ACC-DELIVERY §4 | CNT-ACC-DELIVERY §2, §4 |
| AC-PH04-SHP-002-01 | SREQ-PH04-SHP-002 | Replay yields the same shipment set. | RGAP-PH04-002 | CON-003 | CON-003 |
| AC-PH04-SHP-003-01 | SREQ-PH04-SHP-003 | No shipment exists for software-only orders. | RGAP-PH04-002 | FR-005; FN-LIC-ACTIVATE | FN-LIC-ACTIVATE; CNT-ACC-DELIVERY |
| AC-PH04-SHP-004-01 | SREQ-PH04-SHP-004 | Order status remains confirmed and the retry is observable. | RGAP-PH04-002 | CNT-ACC-DELIVERY §5 | CNT-ACC-DELIVERY §5; ADR-013 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Delivery service unavailable: orders stay confirmed with Pending Delivery.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-008-GATE | ADR-008 offline courier strategy and delivery provider scope unknown. | SREQ-PH04-SHP-001 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-002 | No registered IF-* or schema for delivery APIs; ShipmentCreated/Assigned/Delivered are named in CNT-ACC-DELIVERY §2 but absent from the §5.5 event catalogue; courier PATCH sync is described only in CNT-AMD-COURIER §6. | Recorded here; route: API Governance (IC-002). |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-DELIVERY.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
