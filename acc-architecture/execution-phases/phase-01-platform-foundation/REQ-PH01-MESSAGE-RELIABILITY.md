# REQ-PH01-MESSAGE-RELIABILITY — Outbox/Inbox and at-least-once delivery

**Document ID:** REQ-PH01-MESSAGE-RELIABILITY  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-MESSAGE-RELIABILITY |
| Phase ID | PH-01 |
| Title | Outbox/Inbox and at-least-once delivery |
| Statement | Cross-system commands and events use durable local intent, idempotent receipt and at-least-once delivery so retries and duplicates do not repeat business effects and unknown outcomes stay recoverable. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCORE, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACR-OUTBOX, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-EVENTBUS |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | CON-003; CON-009; NFR-003; NFR-007; ADR-005; IF-ACC-EVENT-ENVELOPE; resilience-observability.md §1 |

## 2. Scope boundary and phase handoffs

- Function-specific idempotency keys are defined in the phases that own the function.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-MSG-001 | REQ-PH01-MESSAGE-RELIABILITY | A business state change and its outbound event intent commit in the same local transaction. | A business operation emits an event. | Both persist together or neither does. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-OUTBOX, CNT-ACC-INTEGRATION | AC-PH01-MSG-001-01 | TEST (planned): crash recovery test (acceptance-test-plan.md item 12) | DRAFT | none recorded |
| SREQ-PH01-MSG-002 | REQ-PH01-MESSAGE-RELIABILITY | A receiver records receipt before processing and applies each business effect at most once per scoped key; a redelivered completed effect returns the recorded outcome. | A duplicate or redelivered message arrives. | No second effect occurs. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-OUTBOX, CNT-ACR-CONNECTOR, CNT-ACC-INTEGRATION | AC-PH01-MSG-002-01 | TEST (planned): duplicate delivery test | DRAFT | ADR-022-GATE |
| SREQ-PH01-MSG-003 | REQ-PH01-MESSAGE-RELIABILITY | Failed deliveries are retried under policy with the same key, and dead-lettering records a delivery condition, not a business rejection or completion. | Delivery retries are exhausted. | Message is preserved in dead-letter state for recovery. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION, CNT-ACR-OUTBOX | AC-PH01-MSG-003-01 | TEST (planned): DLQ replay test | DRAFT | IC-004, ADR-022-GATE |
| SREQ-PH01-MSG-004 | REQ-PH01-MESSAGE-RELIABILITY | Events needing order are applied in order per partition key where configured, and consumers detect out-of-order delivery by version or ordering key. | Events arrive out of order. | Stale or early events are detected. | SYS-ACCSYSTEM | CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION | AC-PH01-MSG-004-01 | TEST (planned): ordering test | DRAFT | IC-004 |
| SREQ-PH01-MSG-005 | REQ-PH01-MESSAGE-RELIABILITY | Published events are immutable and corrections are new events. | A published event requires correction. | A new event is published. | SYS-ACCSYSTEM | CNT-ACC-EVENTBUS | AC-PH01-MSG-005-01 | REVIEW (planned): bus design review | DRAFT | none recorded |
| SREQ-PH01-MSG-006 | REQ-PH01-MESSAGE-RELIABILITY | Every event carries event_id, event_type, event_version, occurred_at, producer, institution_id, aggregate_id, correlation_id, causation_id and idempotency_key. | A service publishes an event. | The envelope is complete. | SYS-ACCSYSTEM | CNT-ACC-EVENTBUS | AC-PH01-MSG-006-01 | TEST (planned): contract test | DRAFT | IC-002, IC-004, ADR-021-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-MSG-001 | Atomic outbox | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CON-003; ADR-005 |
| SREQ-PH01-MSG-002 | Idempotent inbox | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | NFR-003; CON-003 |
| SREQ-PH01-MSG-003 | Retry and dead-letter semantics | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | ADR-005; resilience §1.4 |
| SREQ-PH01-MSG-004 | Per-key ordering | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | NFR-007 |
| SREQ-PH01-MSG-005 | Event immutability | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CON-009 |
| SREQ-PH01-MSG-006 | Common event envelope | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | IF-ACC-EVENT-ENVELOPE §5.4 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-MSG-001-01 | SREQ-PH01-MSG-001 | After a crash between commit and send the event is dispatched on restart; no event exists without committed state. | IF-ACC-EVENT-ENVELOPE §5.6 | CON-003; CNT-ACR-OUTBOX §1 | CON-003; ADR-005 |
| AC-PH01-MSG-002-01 | SREQ-PH01-MSG-002 | Duplicates yield no repeated effect; an in-progress duplicate is recovered, not re-executed. | IF-ACC-EVENT-ENVELOPE §5.6 | NFR-003 | NFR-003; CON-003 |
| AC-PH01-MSG-003-01 | SREQ-PH01-MSG-003 | A dead-lettered message is not treated as rejected or executed; before replay of a financial or reservation command the source of truth is queried by key. | IF-ACC-EVENT-ENVELOPE §5.6 | resilience-observability.md §1.4 | ADR-005; resilience §1.4 |
| AC-PH01-MSG-004-01 | SREQ-PH01-MSG-004 | An out-of-order event does not cause an invalid transition; global ordering is not implied. | IF-ACC-EVENT-ENVELOPE §5.6 | NFR-007 | NFR-007 |
| AC-PH01-MSG-005-01 | SREQ-PH01-MSG-005 | No update path exists for published events. | IF-ACC-EVENT-ENVELOPE §5.7 | CON-009 | CON-009 |
| AC-PH01-MSG-006-01 | SREQ-PH01-MSG-006 | Events missing envelope fields are rejected by the contract check. | IF-ACC-EVENT-ENVELOPE §5.4 | CNT-ACC-EVENTBUS §3 | IF-ACC-EVENT-ENVELOPE §5.4 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Event bus unavailable: producers hold events in their Outbox.
- Event schema evolution and broker technology are UNKNOWN (IC-004).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-MSG-002, SREQ-PH01-MSG-003 |
| IC-004 | Message-broker technology, topics, partitioning, retention and ACL design unspecified. | SREQ-PH01-MSG-003, SREQ-PH01-MSG-004, SREQ-PH01-MSG-006 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH01-MSG-006 |
| ADR-021-GATE | ADR-021 interface versioning is interim, approval-required. | SREQ-PH01-MSG-006 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |

## 7. Traceability sources

- decisions/ADR-005.md
- supporting-views/resilience-observability.md
- c2-containers/accore/CNT-ACR-OUTBOX.md, accsystem/CNT-ACC-EVENTBUS.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
