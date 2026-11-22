# REQ-PH01-IDEMPOTENCY-AND-CORRELATION — Idempotency keys, correlation and identity mapping

**Document ID:** REQ-PH01-IDEMPOTENCY-AND-CORRELATION  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-IDEMPOTENCY-AND-CORRELATION |
| Phase ID | PH-01 |
| Title | Idempotency keys, correlation and identity mapping |
| Statement | Commands, events and operations carry stable scoped identities, a correlation identifier and institution identity mappings so duplicates, replays and cross-system flows can be recognized and traced. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACR-OUTBOX, CNT-ACC-APIGATEWAY, CNT-ACC-EVENTBUS |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | CON-003; NFR-003; NFR-010; CNT-ACC-INTEGRATION §4; CNT-ACR-CONNECTOR §4 |

## 2. Scope boundary and phase handoffs

- Flow-specific keys (checkout, reservation, publication, payment) are defined in later phases.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-IDEM-001 | REQ-PH01-IDEMPOTENCY-AND-CORRELATION | Every retryable command carries a stable idempotency key scoped to its business operation, reused unchanged on retry. | A command is sent or retried. | The key is identical across retries. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACR-OUTBOX | AC-PH01-IDEM-001-01 | TEST (planned): retry key test | DRAFT | none recorded |
| SREQ-PH01-IDEM-002 | REQ-PH01-IDEMPOTENCY-AND-CORRELATION | A correlation_id originating at the client request propagates through every service, message and integration call. | A client request begins a flow. | All hops carry the same correlation_id. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-APIGATEWAY, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-EVENTBUS | AC-PH01-IDEM-002-01 | TEST (planned): trace test | DRAFT | none recorded |
| SREQ-PH01-IDEM-003 | REQ-PH01-IDEMPOTENCY-AND-CORRELATION | The integration layer and connector map platform_institution_id to the ACCore-local institution reference consistently in both directions. | A message crosses the boundary. | Identifiers translate correctly. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH01-IDEM-003-01 | TEST (planned): mapping test | DRAFT | none recorded |
| SREQ-PH01-IDEM-004 | REQ-PH01-IDEMPOTENCY-AND-CORRELATION | Idempotency and deduplication records are retained at least as long as retries, reconciliation and audit require. | A deduplication record ages. | It is not purged while still needed. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-OUTBOX | AC-PH01-IDEM-004-01 | REVIEW (planned): retention policy review | OWNER_REVIEW | ADR-022-GATE, UNKN-002 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-IDEM-001 | Stable scoped keys | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CON-003; NFR-003 |
| SREQ-PH01-IDEM-002 | Correlation propagation | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | NFR-010 |
| SREQ-PH01-IDEM-003 | Institution identity mapping | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CNT-ACC-INTEGRATION §4 |
| SREQ-PH01-IDEM-004 | Retention covers reconciliation | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | resilience §1.5; ADR-022 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-IDEM-001-01 | SREQ-PH01-IDEM-001 | Retries reuse the same key; a new operation gets a new key. | IF-ACC-EVENT-ENVELOPE §5.4 | CON-003 | CON-003; NFR-003 |
| AC-PH01-IDEM-002-01 | SREQ-PH01-IDEM-002 | A trace query by one correlation_id spans gateway, integration, connector and bus. | IF-ACC-EVENT-ENVELOPE §5.4 | NFR-010 | NFR-010 |
| AC-PH01-IDEM-003-01 | SREQ-PH01-IDEM-003 | Round-trip mapping yields the original identifiers; unmapped ids are rejected. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | CNT-ACC-INTEGRATION §4; CNT-ACR-CONNECTOR §4 | CNT-ACC-INTEGRATION §4 |
| AC-PH01-IDEM-004-01 | SREQ-PH01-IDEM-004 | No record is purged before outcomes are resolved; duration is a policy value. | NOT SPECIFIED (source reference gap: RGAP-PH01-007) | ADR-022 idempotency.retention_days | resilience §1.5; ADR-022 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Reuse of a key with different parameters must be rejected or reviewed where the owning function defines it.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-IDEM-004 |
| UNKN-002 | Compliance/data-residency/retention framework (PCI-DSS, privacy, audit retention) not defined. | SREQ-PH01-IDEM-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-006 | Concrete version/schema mapping of the single logical ACCore connector contract is not defined. | ADR-015 and ADR-021 defer it to API Governance; recorded here. |
| RGAP-PH01-007 | Policy store has no registered interface; ADR-022 §8 only names CNT-ACC-INSTREG as the policy-store container; approval-record mechanism unspecified. | Recorded here; route: technical ADR if implementation deviates (ADR-022 §4). |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md CON-003, NFR-003, NFR-010
- supporting-views/resilience-observability.md §1.5

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
