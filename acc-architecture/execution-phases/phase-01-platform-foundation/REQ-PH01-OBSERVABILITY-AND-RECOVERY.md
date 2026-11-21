# REQ-PH01-OBSERVABILITY-AND-RECOVERY — Baseline observability, recovery ownership and data boundaries

**Document ID:** REQ-PH01-OBSERVABILITY-AND-RECOVERY  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-OBSERVABILITY-AND-RECOVERY |
| Phase ID | PH-01 |
| Title | Baseline observability, recovery ownership and data boundaries |
| Statement | The foundation exposes baseline health and metrics, names recovery ownership per domain without inventing objectives, and enforces schema ownership and secret handling needed by later phases. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-INTEGRATION, CNT-ACC-IDENTITY, CNT-ACC-AUDIT, CNT-ACC-EVENTBUS, CNT-ACC-INSTREG, CNT-ACC-LICENSE |
| Related function/use case | TBD (RGAP-PH01-010) |
| Status | DRAFT |
| Evidence | NFR-010; NFR-011; NFR-012; CON-012; ADR-012; resilience-observability.md; deployment-view.md |

## 2. Scope boundary and phase handoffs

- No numeric SLO, RTO or RPO is asserted.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-OBS-001 | REQ-PH01-OBSERVABILITY-AND-RECOVERY | Foundation services expose the named operational signals (integration last-sync, failed messages, ACCore latency, auth success, outbox/DLQ depth) with thresholds held as policy keys. | A foundation service runs. | Signals are measurable. | SYS-ACCSYSTEM | CNT-ACC-INTEGRATION, CNT-ACC-IDENTITY, CNT-ACC-AUDIT, CNT-ACC-EVENTBUS | AC-PH01-OBS-001-01 | TEST (planned): metrics presence test | DRAFT | ADR-022-GATE |
| SREQ-PH01-OBS-002 | REQ-PH01-OBSERVABILITY-AND-RECOVERY | Each domain has a named owner and defined RPO/RTO with backup-restore testing before production activation. | A domain approaches activation. | Objectives and owner are recorded. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-INTEGRATION | AC-PH01-OBS-002-01 | REVIEW (planned): DR readiness review | OWNER_REVIEW | UNKN-001, RP-15 |
| SREQ-PH01-OBS-003 | REQ-PH01-OBSERVABILITY-AND-RECOVERY | Each bounded context owns its schema and no service accesses another context's database, including in co-hosted deployment units; a single service can deploy without coordinated deployment of others. | A service is deployed or queries data. | Boundaries hold. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-INSTREG, CNT-ACC-INTEGRATION | AC-PH01-OBS-003-01, AC-PH01-OBS-003-02 | TEST (planned): independent deployment test | DRAFT | RP-14 |
| SREQ-PH01-OBS-004 | REQ-PH01-OBSERVABILITY-AND-RECOVERY | Signing keys, credentials and secrets are kept out of source code and client bundles and support rotation. | Secrets are provisioned or rotated. | No secret resides in code or bundles. | SYS-ACCSYSTEM | CNT-ACC-LICENSE, CNT-ACC-IDENTITY, CNT-ACC-INSTREG | AC-PH01-OBS-004-01 | REVIEW (planned): secret handling review | DRAFT | RP-16 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-OBS-001 | Baseline metrics | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-010) | resilience-observability.md §2 |
| SREQ-PH01-OBS-002 | Recovery objectives owned | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-010) | NFR-012; RP-15 |
| SREQ-PH01-OBS-003 | Schema ownership and deployability | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-010) | NFR-011; ADR-012 |
| SREQ-PH01-OBS-004 | Secrets outside code | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-010) | security-view §2.2 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-OBS-001-01 | SREQ-PH01-OBS-001 | Each signal family is observable; no threshold number is hard-coded. | RGAP-PH01-010 | resilience-observability.md §2; CNT-ACC-INTEGRATION §8 | resilience-observability.md §2 |
| AC-PH01-OBS-002-01 | SREQ-PH01-OBS-002 | No domain is activated without recorded owner and objectives; none are asserted here. | RGAP-PH01-010 | NFR-012 | NFR-012; RP-15 |
| AC-PH01-OBS-003-01 | SREQ-PH01-OBS-003 | No cross-context database access exists. | RGAP-PH01-010 | ADR-012; deployment-view §1 | NFR-011; ADR-012 |
| AC-PH01-OBS-003-02 | SREQ-PH01-OBS-003 | Deploying one service does not require coordinated deployment of others. | RGAP-PH01-010 | NFR-011; CON-012 | NFR-011; ADR-012 |
| AC-PH01-OBS-004-01 | SREQ-PH01-OBS-004 | Review finds no embedded secrets; rotation works without code change. | RGAP-PH01-010 | CMP-LIC-OFFLINE §6; security-view §2.2 | security-view §2.2 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Recovery procedures in the source are INCOMPLETE PROPOSALS (stuck saga, reindex, reconnection); owners and runbooks remain to be assigned.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-OBS-001 |
| UNKN-001 | SLA/availability targets per domain not defined (discovery-report.md). | SREQ-PH01-OBS-002 |
| RP-15 | Workload, SLO, RPO/RTO and reconciliation targets unknown/proposed. | SREQ-PH01-OBS-002 |
| RP-14 | Independent deployability evidence for NFR-011/CON-012 not yet available. | SREQ-PH01-OBS-003 |
| RP-16 | Institutional auth mode, executable API/event schemas, key lifecycle and replay tests not ratified. | SREQ-PH01-OBS-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-010 | No registered contract for health/readiness endpoints or metric names; probe format is "to be selected" (resilience-observability.md §2). | Recorded here; route: platform review / SRE. |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md NFR-010..012, CON-012
- supporting-views/resilience-observability.md
- supporting-views/deployment-view.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
