# REQ-PH04-DELIVERY-EXCEPTIONS — Delivery exceptions and cancellation interaction

**Document ID:** REQ-PH04-DELIVERY-EXCEPTIONS  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-DELIVERY-EXCEPTIONS |
| Phase ID | PH-04 |
| Title | Delivery exceptions and cancellation interaction |
| Statement | Delayed, stuck or failed deliveries are visible to operations, and order cancellation halts or coordinates delivery without inventing failure or return behavior the sources do not define. |
| Actors | ACT-DELIVERY-SUPERVISOR, ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCMARED-SUP |
| Primary C4 containers | CNT-ACC-DELIVERY, CNT-AMD-SUPERVISOR, CNT-ACC-ORDERS |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-ACC-DELIVERY §5, §7; FR-008; execution-phases/README.md §6; ODEC-007 |

## 2. Scope boundary and phase handoffs

- Failure, re-attempt and return flows are undefined (RGAP-PH04-005); only the documented rules are stated.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-DEX-001 | REQ-PH04-DELIVERY-EXCEPTIONS | Unassigned shipments, late tasks and stuck deliveries are visible to supervisors and operations. | A shipment exceeds expected handling. | It appears in an exception view. | SYS-ACCSYSTEM, SYS-ACCMARED-SUP | CNT-ACC-DELIVERY, CNT-AMD-SUPERVISOR | AC-PH04-DEX-001-01 | TEST (planned): exception view test | OWNER_REVIEW | UNKN-001, ADR-022-GATE |
| SREQ-PH04-DEX-002 | REQ-PH04-DELIVERY-EXCEPTIONS | An accepted order cancellation prevents further delivery progress for the affected shipment. | Cancellation is accepted for a shipment in progress. | Delivery does not progress. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY, CNT-ACC-ORDERS | AC-PH04-DEX-002-01 | TEST (planned): cancellation interaction test | OWNER_REVIEW | none recorded |
| SREQ-PH04-DEX-003 | REQ-PH04-DELIVERY-EXCEPTIONS | A missing courier update does not mark a delivery failed or delivered. | No status update arrives. | State stays as last confirmed. | SYS-ACCSYSTEM | CNT-ACC-DELIVERY | AC-PH04-DEX-003-01 | TEST (planned): absence test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-DEX-001 | Visible delivery exceptions | ACT-DELIVERY-SUPERVISOR | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY §7 |
| SREQ-PH04-DEX-002 | Cancellation halts delivery | ACT-DELIVERY-SUPERVISOR, ACT-PLATFORM-ADMIN | TBD (RGAP-PH04-001) | FR-008 |
| SREQ-PH04-DEX-003 | Failure not inferred | ACT-DELIVERY-SUPERVISOR, ACT-PLATFORM-ADMIN | TBD (RGAP-PH04-001) | ADR-013 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-DEX-001-01 | SREQ-PH04-DEX-001 | Unassigned, late and stuck shipments are retrievable; target thresholds are policy values. | NOT SPECIFIED (source reference gap: RGAP-PH04-005) | CNT-ACC-DELIVERY §7 (SLI) | CNT-ACC-DELIVERY §7 |
| AC-PH04-DEX-002-01 | SREQ-PH04-DEX-002 | A cancelled shipment accepts no further courier progress; handling of goods in transit is not asserted. | NOT SPECIFIED (source reference gap: RGAP-PH04-005) | FR-008 | FR-008 |
| AC-PH04-DEX-003-01 | SREQ-PH04-DEX-003 | Absence of updates changes no delivery state; a late indicator may be raised. | NOT SPECIFIED (source reference gap: RGAP-PH04-005) | ADR-013 | ADR-013 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Return-to-sender, re-attempt and recipient-absent flows are not specified.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-001 | SLA/availability targets per domain not defined (discovery-report.md). | SREQ-PH04-DEX-001 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH04-DEX-001 |
| ODEC-007 | Returns and disputes capability (deferred; design pending). | No defined delivery-exception sub-requirement; return/dispute behavior remains a parent-level deferred boundary. |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-005 | Delivery failure, re-attempt, return-to-sender and recipient-absent flows have no source definition; returns are deferred (ODEC-007). | Recorded here; no behavior beyond the documented Pending Delivery rule is asserted. |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-DELIVERY.md
- execution-phases/README.md §6

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
