# REQ-PH03-EXTERNAL-DELIVERY-EVENTS — External and institution-owned delivery event intake

**Document ID:** REQ-PH03-EXTERNAL-DELIVERY-EVENTS  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-EXTERNAL-DELIVERY-EVENTS |
| Phase ID | PH-03 |
| Title | External and institution-owned delivery event intake |
| Statement | Shipment and tracking events from external or institution-owned delivery systems are accepted, normalized to a common vocabulary and mapped to the correct order scope idempotently without presuming ACCMared. |
| Actors | ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-DELIVERY, CNT-ACC-ORDERS, CNT-ACC-INTEGRATION |
| Related function/use case | TBD (RGAP-PH03-002) |
| Status | DRAFT |
| Evidence | execution-phases/README.md §5; ODEC-010; UNKN-004; ASSUM-006; traceability-24-topics.md topic 8; CNT-ACC-DELIVERY |

## 2. Scope boundary and phase handoffs

- Owner gate RGAP-PH03-002: no interface, schema or function exists for this intake; statements below follow the PH-03 boundary only.
- Internal ACCMared dispatch is PH-04; the common vocabulary here must not presume it.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-EXD-001 | REQ-PH03-EXTERNAL-DELIVERY-EVENTS | ACCSystem accepts shipment and tracking events from an authorized institution or external delivery source under the connector contract rules. | An authorized source reports a delivery event. | Event accepted or rejected. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS, CNT-ACC-INTEGRATION | AC-PH03-EXD-001-01 | TEST (planned): intake auth test | OWNER_REVIEW | ODEC-010, UNKN-004 |
| SREQ-PH03-EXD-002 | REQ-PH03-EXTERNAL-DELIVERY-EVENTS | Events map to a delivery vocabulary independent of whether delivery is performed by ACCMared or an external party. | An external event arrives. | Normalized status recorded. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY | AC-PH03-EXD-002-01 | REVIEW (planned): vocabulary review | OWNER_REVIEW | ADR-008-GATE |
| SREQ-PH03-EXD-003 | REQ-PH03-EXTERNAL-DELIVERY-EVENTS | Each external shipment has a stable identity within order scope and duplicate events cause no duplicate effect. | An event is replayed. | One effect. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS | AC-PH03-EXD-003-01 | TEST (planned): duplicate delivery event test | OWNER_REVIEW | none recorded |
| SREQ-PH03-EXD-004 | REQ-PH03-EXTERNAL-DELIVERY-EVENTS | A confirmed order lacking shipment information shows a pending-delivery state without blocking order confirmation. | No delivery event has arrived. | Pending delivery shown. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-DELIVERY | AC-PH03-EXD-004-01 | TEST (planned): pending delivery test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-EXD-001 | Accept external delivery events | ACT-INST-EMPLOYEE | TBD (RGAP-PH03-002) | execution-phases/README.md §5 |
| SREQ-PH03-EXD-002 | Normalize to common vocabulary | ACT-INST-EMPLOYEE | TBD (RGAP-PH03-002) | ADR-008; ASSUM-006 |
| SREQ-PH03-EXD-003 | Stable shipment identity and idempotency | ACT-INST-EMPLOYEE | TBD (RGAP-PH03-002) | CON-003; execution-phases/README.md §5 |
| SREQ-PH03-EXD-004 | Pending delivery visibility | ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FN-ORD-CONFIRM; ADR-013 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-EXD-001-01 | SREQ-PH03-EXD-001 | Unauthorized sources are rejected. | NOT SPECIFIED (source reference gap: RGAP-PH03-002) | execution-phases/README.md §5 | execution-phases/README.md §5 |
| AC-PH03-EXD-002-01 | SREQ-PH03-EXD-002 | Unmapped statuses are retained and flagged rather than discarded. | NOT SPECIFIED (source reference gap: RGAP-PH03-002) | ADR-008 | ADR-008; ASSUM-006 |
| AC-PH03-EXD-003-01 | SREQ-PH03-EXD-003 | A replayed event does not change delivery state again; events cannot be applied to the wrong SellerOrder. | NOT SPECIFIED (source reference gap: RGAP-PH03-002) | CON-003 | CON-003; execution-phases/README.md §5 |
| AC-PH03-EXD-004-01 | SREQ-PH03-EXD-004 | Confirmation never depends on delivery events. | NOT SPECIFIED (no external-intake contract is required for this invariant) | FN-ORD-CONFIRM; ADR-013 | FN-ORD-CONFIRM; ADR-013 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Whether ACCMared coexists with external delivery per institution is open (ASSUM-006, UNKN-004).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ODEC-010 | ACCMared delivery scope: platform fleet only or external logistics provider integration. | SREQ-PH03-EXD-001 |
| UNKN-004 | ACCMared delivery scope: platform fleet only vs external logistics provider integration. | SREQ-PH03-EXD-001 |
| ADR-008-GATE | ADR-008 offline courier strategy and delivery provider scope unknown. | SREQ-PH03-EXD-002 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-002 | For SREQ-PH03-EXD-004, FN-ORD-CONFIRM covers the internal post-confirmation delivery attempt and pending-delivery outcome; it does not define intake/normalization of shipment or tracking events from external or institution-owned systems, for which no interface, function spec or event schema exists. | Recorded here; route: API Governance and the delivery-provider owner decision (UNKN-004, ODEC-010). |

## 7. Traceability sources

- execution-phases/README.md §5
- functions/specs/FN-ORD-CONFIRM.md — §4 steps 5, §7 shipment-creation failure
- validation/traceability-24-topics.md topic 8

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
