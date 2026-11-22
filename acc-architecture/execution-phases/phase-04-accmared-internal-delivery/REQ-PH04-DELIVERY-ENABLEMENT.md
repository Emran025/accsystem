# REQ-PH04-DELIVERY-ENABLEMENT — ACCMared delivery enablement and coexistence

**Document ID:** REQ-PH04-DELIVERY-ENABLEMENT  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-DELIVERY-ENABLEMENT |
| Phase ID | PH-04 |
| Title | ACCMared delivery enablement and coexistence |
| Statement | ACCMared internal delivery is enabled per institution scope only on approved policy, behind a provider-agnostic delivery boundary that coexists with external delivery events without duplicating shipments. |
| Actors | ACT-PLATFORM-ADMIN, ACT-DELIVERY-SUPERVISOR |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-DELIVERY, CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN, CNT-ACC-ORDERS |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | ADR-008; ODEC-010; UNKN-004; ASSUM-006; execution-phases/README.md §6; traceability-24-topics.md topic 8 |

## 2. Scope boundary and phase handoffs

- Scope: the sources state internal platform fleet first with a provider interface and internal priority (topic 8); external provider integration remains open.
- C3 decomposition of the delivery container is deferred (RGAP-PH04-003).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-DEN-001 | REQ-PH04-DELIVERY-ENABLEMENT | ACCMared delivery for an institution scope is activated only after the delivery-scope decision is approved, otherwise the institution's orders use pending-delivery handling or external events. | Delivery enablement is requested. | Enabled only with approved scope. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN | AC-PH04-DEN-001-01 | REVIEW (planned): owner scope decision | OWNER_REVIEW | ODEC-010, UNKN-004, ASSUM-006, ADR-008-GATE |
| SREQ-PH04-DEN-002 | REQ-PH04-DELIVERY-ENABLEMENT | Delivery logic is accessed through a delivery boundary that does not hard-wire a single fleet, so an external provider can be added without changing order handling. | A shipment needs fulfilment. | Order logic is independent of the fulfilment party. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS | AC-PH04-DEN-002-01 | REVIEW (planned): interface review | OWNER_REVIEW | none recorded |
| SREQ-PH04-DEN-003 | REQ-PH04-DELIVERY-ENABLEMENT | A SellerOrder is fulfilled either through ACCMared or through external delivery events, and a shipment for the same SellerOrder is not created twice. | Both channels could apply to a SellerOrder. | One fulfilment channel. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS | AC-PH04-DEN-003-01 | TEST (planned): coexistence test | OWNER_REVIEW | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-DEN-001 | Policy-gated enablement | ACT-PLATFORM-ADMIN, ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | ADR-008; ODEC-010 |
| SREQ-PH04-DEN-002 | Provider-agnostic boundary | ACT-PLATFORM-ADMIN, ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | ADR-008 |
| SREQ-PH04-DEN-003 | No duplicate fulfilment per SellerOrder | ACT-PLATFORM-ADMIN, ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | execution-phases/README.md §6 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-DEN-001-01 | SREQ-PH04-DEN-001 | Activation without an approved delivery-scope value is blocked. | NOT SPECIFIED (source reference gap: RGAP-PH04-001) | ADR-017; ADR-022 §6 | ADR-008; ODEC-010 |
| AC-PH04-DEN-002-01 | SREQ-PH04-DEN-002 | Order handling references shipment identity and common statuses only. | NOT SPECIFIED (source reference gap: RGAP-PH04-002) | ADR-008; topic 8 | ADR-008 |
| AC-PH04-DEN-003-01 | SREQ-PH04-DEN-003 | The second channel is rejected or flagged for that SellerOrder. | NOT SPECIFIED (source reference gap: RGAP-PH04-002) | execution-phases/README.md §5-§6 | execution-phases/README.md §6 |

## 5. Alternate paths, failure, exception and uncertainty handling

- If the owner selects external providers only, PH-04 ACCMared requirements remain unactivated.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ODEC-010 | ACCMared delivery scope: platform fleet only or external logistics provider integration. | SREQ-PH04-DEN-001 |
| UNKN-004 | ACCMared delivery scope: platform fleet only vs external logistics provider integration. | SREQ-PH04-DEN-001 |
| ASSUM-006 | ACCMared covers platform-own fleet only at MVP (revisit before Phase 4). | SREQ-PH04-DEN-001 |
| ADR-008-GATE | ADR-008 offline courier strategy and delivery provider scope unknown. | SREQ-PH04-DEN-001 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-002 | No registered IF-* or schema for delivery APIs; ShipmentCreated/Assigned/Delivered are named in CNT-ACC-DELIVERY §2 but absent from the §5.5 event catalogue; courier PATCH sync is described only in CNT-AMD-COURIER §6. | Recorded here; route: API Governance (IC-002). |

## 7. Traceability sources

- decisions/ADR-008.md
- execution-phases/README.md §6

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
