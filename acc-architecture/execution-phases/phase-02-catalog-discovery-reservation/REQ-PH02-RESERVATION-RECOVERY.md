# REQ-PH02-RESERVATION-RECOVERY — Unknown outcomes, expiry, safe release and reconciliation

**Document ID:** REQ-PH02-RESERVATION-RECOVERY  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-RESERVATION-RECOVERY |
| Phase ID | PH-02 |
| Title | Unknown outcomes, expiry, safe release and reconciliation |
| Statement | Reservation outcomes that cannot be established stay UNKNOWN until reconciled, expiry is authoritative, and release happens only for eligible known holds after reconciliation. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-INTEGRATION, CNT-ACC-ORDERS, CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY |
| Related function/use case | FN-ORD-RESERVE |
| Status | DRAFT |
| Evidence | FN-ORD-RESERVE; ADR-018; ADR-006 §3; resilience-observability.md §1.2-1.3; RP-01; acceptance-test-plan.md items 1, 3 |

## 2. Scope boundary and phase handoffs

- Release after payment failure is a PH-03 consumer of this capability.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-RRC-001 | REQ-PH02-RESERVATION-RECOVERY | A timeout, lost response or interruption after possible dispatch records the reservation as UNKNOWN, not rejected. | No response is received. | Reservation state UNKNOWN. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION, CNT-ACC-ORDERS | AC-PH02-RRC-001-01 | TEST (planned): unknown test (acceptance-test-plan.md item 3) | DRAFT | RP-01, ADR-018-GATE |
| SREQ-PH02-RRC-002 | REQ-PH02-RESERVATION-RECOVERY | An UNKNOWN reservation is reconciled by known reservation ID or stable key through an agreed channel, otherwise the system waits and escalates without repeating a possible effect. | An UNKNOWN reservation exists. | Resolved to ACCEPTED, REJECTED or EXPIRED, or escalated. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH02-RRC-002-01, AC-PH02-RRC-002-02 | TEST (planned): reconciliation test | OWNER_REVIEW | RP-03, IC-006 |
| SREQ-PH02-RRC-003 | REQ-PH02-RESERVATION-RECOVERY | A hold is EXPIRED only on authoritative ACCore evidence, not elapsed local time. | A hold may have lapsed. | EXPIRED only with evidence. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY, CNT-ACC-INTEGRATION | AC-PH02-RRC-003-01 | TEST (planned): expiry test | DRAFT | ADR-006-GATE, ADR-018-GATE |
| SREQ-PH02-RRC-004 | REQ-PH02-RESERVATION-RECOVERY | After a definitive peer failure and reconciliation, only confirmed ACCEPTED holds not consumed or linked to a confirmed order are released, idempotently. | A seller reservation is definitively rejected or expired. | Eligible peer holds released. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY | AC-PH02-RRC-004-01, AC-PH02-RRC-004-02 | TEST (planned): release guard test (acceptance-test-plan.md item 1) | DRAFT | RP-01 |
| SREQ-PH02-RRC-005 | REQ-PH02-RESERVATION-RECOVERY | A release whose outcome is unknown is reconciled before another release is attempted. | Release response is lost. | Release state UNKNOWN then resolved. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH02-RRC-005-01 | TEST (planned): release timeout test | DRAFT | RP-01 |
| SREQ-PH02-RRC-006 | REQ-PH02-RESERVATION-RECOVERY | An UNKNOWN reservation unresolved beyond the policy window is escalated for review with its evidence retained. | Reconciliation window is exceeded. | Escalated, still UNKNOWN. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-INTEGRATION | AC-PH02-RRC-006-01 | REVIEW (planned): operations runbook review | OWNER_REVIEW | ADR-022-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-RRC-001 | Timeout is UNKNOWN | ACT-PLATFORM-ADMIN | FN-ORD-RESERVE | ADR-018; FN-ORD-RESERVE |
| SREQ-PH02-RRC-002 | Reconcile by key | ACT-PLATFORM-ADMIN | FN-ORD-RESERVE | FN-ORD-RESERVE |
| SREQ-PH02-RRC-003 | Authoritative expiry only | ACT-PLATFORM-ADMIN | FN-ORD-RESERVE | ADR-018 |
| SREQ-PH02-RRC-004 | Safe release of eligible holds | ACT-PLATFORM-ADMIN | FN-ORD-RESERVE | ADR-018; FN-ORD-CHECKOUT |
| SREQ-PH02-RRC-005 | Unknown release reconciled | ACT-PLATFORM-ADMIN | FN-ORD-RESERVE | FN-ORD-CHECKOUT |
| SREQ-PH02-RRC-006 | Escalation to review | ACT-PLATFORM-ADMIN | FN-ORD-RESERVE | ADR-022; CMP-ORD-STATEMACHINE |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-RRC-001-01 | SREQ-PH02-RRC-001 | Timeout never yields REJECTED, and payment progression is blocked. | IF-ACC-RESERVE-SAGA §3.6 | ADR-018 | ADR-018; FN-ORD-RESERVE |
| AC-PH02-RRC-002-01 | SREQ-PH02-RRC-002 | A lost accepted response is resolved by query with no duplicate hold. | NOT SPECIFIED (source reference gap: RGAP-PH02-007) | FN-ORD-RESERVE | FN-ORD-RESERVE |
| AC-PH02-RRC-002-02 | SREQ-PH02-RRC-002 | Without a query channel the system waits and escalates. | NOT SPECIFIED (source reference gap: RGAP-PH02-007) | FN-ORD-RESERVE §Execution 5 | FN-ORD-RESERVE |
| AC-PH02-RRC-003-01 | SREQ-PH02-RRC-003 | Elapsed local time alone never marks a hold expired. | IF-ACR-RESERVATION-RESP §9.5 | ADR-018 | ADR-018 |
| AC-PH02-RRC-004-01 | SREQ-PH02-RRC-004 | Release is never issued solely on timeout; unknown peers are reconciled first. | NOT SPECIFIED (source reference gap: RGAP-PH02-008) | FN-ORD-RESERVE; ADR-018 | ADR-018; FN-ORD-CHECKOUT |
| AC-PH02-RRC-004-02 | SREQ-PH02-RRC-004 | A consumed or committed reservation cannot be released. | NOT SPECIFIED (source reference gap: RGAP-PH02-008) | FN-ORD-RESERVE | ADR-018; FN-ORD-CHECKOUT |
| AC-PH02-RRC-005-01 | SREQ-PH02-RRC-005 | A second release is not sent blindly. | NOT SPECIFIED (source reference gap: RGAP-PH02-008) | FN-ORD-CHECKOUT acceptance | FN-ORD-CHECKOUT |
| AC-PH02-RRC-006-01 | SREQ-PH02-RRC-006 | Escalation does not infer an outcome; window is policy value. | NOT SPECIFIED (source reference gap: RGAP-PH02-007) | ADR-022 saga.reconciliation_window_seconds | ADR-022; CMP-ORD-STATEMACHINE |

## 5. Alternate paths, failure, exception and uncertainty handling

- Circuit-open after possible dispatch is UNKNOWN unless durable evidence shows no command was sent.
- Deduplication retention covers reconciliation; duration is a policy value.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| RP-01 | Reservation timeout/UNKNOWN contradiction: technical alignment recorded, versioned institutional contract and executable evidence open. | SREQ-PH02-RRC-001, SREQ-PH02-RRC-004, SREQ-PH02-RRC-005 |
| ADR-018-GATE | ADR-018 reservation TTL values and async-callback mode require per-institution approval. | SREQ-PH02-RRC-001, SREQ-PH02-RRC-003 |
| RP-03 | Reservation response vocabulary and delivery-mode contract gate open. | SREQ-PH02-RRC-002 |
| IC-006 | Reservation response delivery mode (sync vs async callback) not confirmed (partially resolved by ADR-018). | SREQ-PH02-RRC-002 |
| ADR-022-GATE | ADR-022 governs the configurable reconciliation window, not the reservation query/delivery channel. | SREQ-PH02-RRC-006 |
| ADR-006-GATE | ADR-006 reservation hold TTL unknown (policy:reservation.hold_ttl_seconds, ADR-022). | SREQ-PH02-RRC-003 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-007 | Existence of an ACCore reservation query endpoint is an assumption pending institution agreement (FN-ORD-RESERVE). | Recorded here; institution/API gate (IC-006, RP-03). |
| RGAP-PH02-008 | Reservation release/cancel command has no schema in IF-ACC-RESERVE-SAGA §3.4 (only request/response bodies). | Recorded here; route: API Governance (RP-03). |

## 7. Traceability sources

- decisions/ADR-018.md
- functions/specs/FN-ORD-RESERVE.md
- validation/c4-microservices-remediation-plan.md RP-01

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
