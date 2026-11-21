# REQ-PH04-OFFLINE-COURIER-SYNC — Offline courier queue and synchronization

**Document ID:** REQ-PH04-OFFLINE-COURIER-SYNC  
**Phase:** PH-04 — ACCMared Internal Delivery Operations  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH04-OFFLINE-COURIER-SYNC |
| Phase ID | PH-04 |
| Title | Offline courier queue and synchronization |
| Statement | Where offline operation is approved, courier updates queue in encrypted local storage and synchronize idempotently when connectivity returns. |
| Actors | ACT-COURIER |
| Locations | SYS-ACCMARED-COU, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-AMD-COURIER, CNT-ACC-DELIVERY |
| Related function/use case | TBD (RGAP-PH04-001) |
| Status | DRAFT |
| Evidence | CNT-AMD-COURIER §6-§7; ADR-008; CNT-ACC-DELIVERY §5 |

## 2. Scope boundary and phase handoffs

- Offline strategy is not approved (ADR-008-GATE); all sub-requirements are OWNER_REVIEW.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH04-OFS-001 | REQ-PH04-OFFLINE-COURIER-SYNC | Offline status submissions are stored in an encrypted local queue and survive process termination. | The courier is offline. | Updates are retained locally. | SYS-ACCMARED-COU | CNT-AMD-COURIER | AC-PH04-OFS-001-01 | TEST (planned): offline persistence test | OWNER_REVIEW | ADR-008-GATE |
| SREQ-PH04-OFS-002 | REQ-PH04-OFFLINE-COURIER-SYNC | On reconnection the queue syncs through idempotent submissions with exponential backoff and jitter. | Connectivity returns. | Entries are applied once. | SYS-ACCMARED-COU, SYS-ACCSYSTEM | CNT-AMD-COURIER, CNT-ACC-DELIVERY | AC-PH04-OFS-002-01 | TEST (planned): sync test | OWNER_REVIEW | ADR-008-GATE |
| SREQ-PH04-OFS-003 | REQ-PH04-OFFLINE-COURIER-SYNC | An offline update conflicting with the backend state is rejected with a visible result rather than overwriting it. | A queued update conflicts with current state. | Backend state wins; conflict visible. | SYS-ACCSYSTEM, SYS-ACCMARED-COU | CNT-ACC-DELIVERY, CNT-AMD-COURIER | AC-PH04-OFS-003-01 | TEST (planned): conflict test | OWNER_REVIEW | ADR-008-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH04-OFS-001 | Encrypted local queue | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-AMD-COURIER §7 |
| SREQ-PH04-OFS-002 | Idempotent sync with backoff | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-AMD-COURIER §6 |
| SREQ-PH04-OFS-003 | Stale offline update | ACT-COURIER | TBD (RGAP-PH04-001) | CNT-ACC-DELIVERY |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH04-OFS-001-01 | SREQ-PH04-OFS-001 | Queued entries persist across app restart; local storage is encrypted (key management UNKNOWN). | RGAP-PH04-002 | CNT-AMD-COURIER §7 | CNT-AMD-COURIER §7 |
| AC-PH04-OFS-002-01 | SREQ-PH04-OFS-002 | Replayed entries cause no duplicate state changes; fatal validation errors are shown to the courier. | RGAP-PH04-002 | CNT-AMD-COURIER §6-§7 | CNT-AMD-COURIER §6 |
| AC-PH04-OFS-003-01 | SREQ-PH04-OFS-003 | Conflicting updates are not silently applied. | RGAP-PH04-002 | CNT-ACC-DELIVERY §1 | CNT-ACC-DELIVERY |

## 5. Alternate paths, failure, exception and uncertainty handling

- Courier offline duration limits are UNKNOWN.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-008-GATE | ADR-008 offline courier strategy and delivery provider scope unknown. | SREQ-PH04-OFS-001, SREQ-PH04-OFS-002, SREQ-PH04-OFS-003 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH04-001 | functions/function-catalog.md has no FN-* for shipment creation, dispatch, courier updates, proof of delivery or delivery exceptions. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH04-002 | No registered IF-* or schema for delivery APIs; ShipmentCreated/Assigned/Delivered are named in CNT-ACC-DELIVERY §2 but absent from the §5.5 event catalogue; courier PATCH sync is described only in CNT-AMD-COURIER §6. | Recorded here; route: API Governance (IC-002). |

## 7. Traceability sources

- c2-containers/accmared/CNT-AMD-COURIER.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
