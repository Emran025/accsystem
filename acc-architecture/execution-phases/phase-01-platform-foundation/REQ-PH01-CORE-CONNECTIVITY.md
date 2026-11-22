# REQ-PH01-CORE-CONNECTIVITY — ACCSystem–ACCore connector boundary and connectivity options

**Document ID:** REQ-PH01-CORE-CONNECTIVITY  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-CORE-CONNECTIVITY |
| Phase ID | PH-01 |
| Title | ACCSystem–ACCore connector boundary and connectivity options |
| Statement | ACCSystem and each institution's ACCore interoperate only through one logical authenticated connector contract with approved connectivity options, binding every message to an authenticated institution and preserving institutional ownership of ERP data. |
| Actors | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-INSTREG |
| Related function/use case | TBD (RGAP-PH01-006) |
| Status | DRAFT |
| Evidence | ADR-015; ADR-002; CON-001; CON-002; CMP-INT-GATEWAY; CNT-ACR-CONNECTOR |

## 2. Scope boundary and phase handoffs

- Message classes (publication, reservation, order confirmation) are specified in later phases and ride on this boundary.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-CONN-001 | REQ-PH01-CORE-CONNECTIVITY | The Integration Gateway is the only entry point for ACCore traffic and the Platform Connector is the only route from ACCore, with no direct database access in either direction. | Any ACCSystem–ACCore interaction. | It passes the connector contract. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH01-CONN-001-01 | REVIEW (planned): integration architecture review | DRAFT | ADR-021-GATE, IC-001, IC-002 |
| SREQ-PH01-CONN-002 | REQ-PH01-CORE-CONNECTIVITY | Outbound-initiated connectivity is the default for firewalled institutions and protected inbound mode is available only where approved, both using the same logical contract and semantics. | An institution is configured for connectivity. | The approved mode operates with identical contract behavior. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH01-CONN-002-01, AC-PH01-CONN-002-02 | TEST (planned): connectivity mode test | DRAFT | ADR-015-GATE, RP-02, ODEC-001 |
| SREQ-PH01-CONN-003 | REQ-PH01-CORE-CONNECTIVITY | The authentication method per institution (OAuth 2.0 Client Credentials and/or mTLS) is enabled by security/operations policy and verified on every inbound message. | An inbound message is received. | It is accepted only under the enabled method. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-INSTREG | AC-PH01-CONN-003-01 | TEST (planned): auth method test | DRAFT | ADR-015-GATE, RP-16 |
| SREQ-PH01-CONN-004 | REQ-PH01-CORE-CONNECTIVITY | The institution of an inbound message is derived from the authenticated principal and a mismatching institution identifier is rejected with 403. | A message carries an institution identifier. | Mismatch is rejected. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION, CNT-ACC-INSTREG | AC-PH01-CONN-004-01 | TEST (planned): binding test | DRAFT | RP-16 |
| SREQ-PH01-CONN-005 | REQ-PH01-CORE-CONNECTIVITY | Inbound events are validated for transport, signature (where applicable) and schema of the declared type, failing with structured machine-readable errors logged as security events. | An inbound event is received. | Valid events are routed; invalid are rejected structurally. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION | AC-PH01-CONN-005-01 | TEST (planned): validation test | DRAFT | IC-002 |
| SREQ-PH01-CONN-006 | REQ-PH01-CORE-CONNECTIVITY | ACCSystem records each institution's connectivity health (such as CONNECTIVITY_UNAVAILABLE) from connector health and last-sync information and exposes it to dependent capabilities, while ACCore local operations continue. | The connector is interrupted or recovers. | State is updated and available. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-INSTREG | AC-PH01-CONN-006-01, AC-PH01-CONN-006-02 | TEST (planned): connectivity loss test (acceptance-test-plan.md item 7) | DRAFT | RP-02, ADR-022-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-CONN-001 | Single logical contract | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-006) | ADR-015; CON-002 |
| SREQ-PH01-CONN-002 | Connectivity modes | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-006) | ADR-015; deployment-view §2 |
| SREQ-PH01-CONN-003 | Policy-selected authentication | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-006) | ADR-015; CMP-INT-GATEWAY |
| SREQ-PH01-CONN-004 | Institution identity binding | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-006) | CMP-INT-GATEWAY |
| SREQ-PH01-CONN-005 | Schema and signature validation | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-006) | CMP-INT-GATEWAY |
| SREQ-PH01-CONN-006 | Institution connectivity state | ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-006) | deployment-view §2 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-CONN-001-01 | SREQ-PH01-CONN-001 | No cross-system database access path exists; interactions use the connector contract. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | CON-001; CON-002; ADR-015 | ADR-015; CON-002 |
| AC-PH01-CONN-002-01 | SREQ-PH01-CONN-002 | Outbound polling or persistent channel works without inbound firewall exposure. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | ADR-015; deployment-view §2 | ADR-015; deployment-view §2 |
| AC-PH01-CONN-002-02 | SREQ-PH01-CONN-002 | Inbound mode is enabled only on approval and does not change logical direction. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | ADR-015 | ADR-015; deployment-view §2 |
| AC-PH01-CONN-003-01 | SREQ-PH01-CONN-003 | A method not enabled for the institution is refused; API keys are not implied. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | CMP-INT-GATEWAY §3.1 | ADR-015; CMP-INT-GATEWAY |
| AC-PH01-CONN-004-01 | SREQ-PH01-CONN-004 | Body/path institution differing from the principal binding yields 403. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | CMP-INT-GATEWAY §3.1; FN-INT-PUBLISH §8 | CMP-INT-GATEWAY |
| AC-PH01-CONN-005-01 | SREQ-PH01-CONN-005 | Schema failures return structured errors; signature failures are rejected and alerted. | NOT SPECIFIED (source reference gap: RGAP-PH01-006) | CMP-INT-GATEWAY §3; CNT-ACC-INTEGRATION §7 | CMP-INT-GATEWAY |
| AC-PH01-CONN-006-01 | SREQ-PH01-CONN-006 | An interrupted connector yields the unavailable state; recovery restores it. | NOT SPECIFIED (source reference gap: RGAP-PH01-010) | deployment-view §2; CNT-ACC-INTEGRATION §8 | deployment-view §2 |
| AC-PH01-CONN-006-02 | SREQ-PH01-CONN-006 | ACCore local ERP functions continue while interrupted. | NOT SPECIFIED (source reference gap: RGAP-PH01-010) | ADR-002; deployment-view §2 | deployment-view §2 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Connector interrupted: messages stay in the Outbox; nothing is treated as rejected.
- Concrete schema/version mapping is open (ADR-021).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-021-GATE | ADR-021 interface versioning is interim, approval-required. | SREQ-PH01-CONN-001 |
| IC-001 | No versioning/backward-compatibility strategy for interfaces (interim: ADR-021). | SREQ-PH01-CONN-001 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH01-CONN-001, SREQ-PH01-CONN-005 |
| ADR-015-GATE | ADR-015 per-institution auth mode, connectivity mode and release trust are proposed baselines pending owner/security approval. | SREQ-PH01-CONN-002, SREQ-PH01-CONN-003 |
| RP-02 | Inbound reachability vs outbound-initiated connectivity default; supported deployment modes await owner decision. | SREQ-PH01-CONN-002, SREQ-PH01-CONN-006 |
| ODEC-001 | ACCore hosting and packaging (institution-controlled; integrated or split). | SREQ-PH01-CONN-002 |
| RP-16 | Institutional auth mode, executable API/event schemas, key lifecycle and replay tests not ratified. | SREQ-PH01-CONN-003, SREQ-PH01-CONN-004 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-CONN-006 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-006 | Concrete version/schema mapping of the single logical ACCore connector contract is not defined. | ADR-015 and ADR-021 defer it to API Governance; recorded here. |
| RGAP-PH01-010 | No registered contract for health/readiness endpoints or metric names; probe format is "to be selected" (resilience-observability.md §2). | Recorded here; route: platform review / SRE. |

## 7. Traceability sources

- decisions/ADR-015.md
- c3-components/CNT-ACC-INTEGRATION/CMP-INT-GATEWAY.md
- supporting-views/deployment-view.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
