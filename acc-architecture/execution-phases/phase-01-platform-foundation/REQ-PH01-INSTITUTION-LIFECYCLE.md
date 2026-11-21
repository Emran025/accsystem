# REQ-PH01-INSTITUTION-LIFECYCLE — Institution identity, lifecycle and integration configuration

**Document ID:** REQ-PH01-INSTITUTION-LIFECYCLE  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-INSTITUTION-LIFECYCLE |
| Phase ID | PH-01 |
| Title | Institution identity, lifecycle and integration configuration |
| Statement | ACCSystem keeps a canonical registry of participating institutions with stable platform identifiers, an explicit activation lifecycle and managed integration configuration so later-phase capabilities can be gated on institution status. |
| Actors | ACT-PLATFORM-ADMIN, ACT-INST-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN, CNT-ACC-INTEGRATION, CNT-ACC-IDENTITY |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | FR-012; CNT-ACC-INSTREG; ADR-011; ADR-015; ADR-022 §8 |

## 2. Scope boundary and phase handoffs

- In scope: institution record, activation lifecycle, integration configuration and credential lifecycle at registry level.
- Out of scope: product publication gated on Active status is enabled in PH-02; this document only requires the registry to provide the status.
- ACCore hosting/packaging (ODEC-001) is undecided; the registry is agnostic to it.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-INST-001 | REQ-PH01-INSTITUTION-LIFECYCLE | On registration of a contracted institution the Institution Registry assigns one unique platform_institution_id that is never reassigned. | Platform administrator creates an institution record. | An institution record with a unique stable platform_institution_id exists. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN | AC-PH01-INST-001-01, AC-PH01-INST-001-02 | TEST (planned): registry uniqueness/stability test | DRAFT | none recorded |
| SREQ-PH01-INST-002 | REQ-PH01-INSTITUTION-LIFECYCLE | An institution has an explicit onboarding/activation status and is Active only after an authorized activation step. | Onboarding initiated for a new institution. | Status reflects the lifecycle step; only activation yields Active. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-PLATFORMADMIN | AC-PH01-INST-002-01, AC-PH01-INST-002-02 | TEST (planned): lifecycle transition test | DRAFT | ADR-017-GATE |
| SREQ-PH01-INST-003 | REQ-PH01-INSTITUTION-LIFECYCLE | The registry provides institution status and integration configuration to authorized platform services, and dependent flows do not proceed on an unknown status when the registry is unavailable. | A platform service needs institution status or configuration. | Authorized caller receives status/config; unavailability pauses dependent flows. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-INTEGRATION, CNT-ACC-IDENTITY | AC-PH01-INST-003-01, AC-PH01-INST-003-02 | TEST (planned): registry outage test | DRAFT | ADR-022-GATE, IC-002 |
| SREQ-PH01-INST-004 | REQ-PH01-INSTITUTION-LIFECYCLE | On onboarding, integration configuration (connector references, allowed event types, credential or certificate references) is created for the institution under the authentication method selected by policy. | Institution is onboarded to platform connectivity. | The institution has a configured connector identity. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-INTEGRATION, CNT-ACC-PLATFORMADMIN | AC-PH01-INST-004-01, AC-PH01-INST-004-02 | REVIEW (planned): security review of credential handling | DRAFT | ADR-015-GATE, RP-16 |
| SREQ-PH01-INST-005 | REQ-PH01-INSTITUTION-LIFECYCLE | Integration credentials or certificates can be rotated and revoked without interrupting service for the institution. | Rotation or revocation is requested or triggered by lifecycle. | New credential is in force; revoked credential is rejected. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-INTEGRATION | AC-PH01-INST-005-01 | TEST (planned): credential rotation/revocation test | RETIRED | ADR-015-GATE, RP-16 |
| SREQ-PH01-INST-006 | REQ-PH01-INSTITUTION-LIFECYCLE | Deactivating an institution removes its membership-based access and blocks capability-gated operations while retaining its records. | Authorized deactivation is performed. | Institutional access is removed; records retained. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN | AC-PH01-INST-006-01, AC-PH01-INST-006-02 | TEST (planned): deactivation access test | OWNER_REVIEW | ADR-011-GATE |
| SREQ-PH01-INST-009 | REQ-PH01-INSTITUTION-LIFECYCLE | Integration credentials or certificates can be rotated under the approved transition policy: both the old and new credentials are accepted during the transition, then only the new credential is accepted; no duration or uninterrupted-service policy is asserted. | Credential or certificate rotation is requested or triggered by lifecycle. | During the approved transition both credentials are accepted; after it only the new credential is accepted. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-INTEGRATION | AC-PH01-INST-009-01 | TEST (planned): credential rotation transition test | DRAFT | ADR-015-GATE, RP-16 |
| SREQ-PH01-INST-010 | REQ-PH01-INSTITUTION-LIFECYCLE | After an integration credential or certificate is revoked, authentication using that credential is rejected. | An integration credential or certificate is revoked. | Authentication using the revoked credential is rejected. | SYS-ACCSYSTEM | CNT-ACC-INSTREG, CNT-ACC-INTEGRATION | AC-PH01-INST-010-01 | TEST (planned): revoked credential rejection test | DRAFT | ADR-015-GATE, RP-16 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-INST-001 | Unique stable institution ID | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-012 AC1 |
| SREQ-PH01-INST-002 | Activation status | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-012 AC2; FN-INT-PUBLISH P1 |
| SREQ-PH01-INST-003 | Institution lookup for platform services | ACT-PLATFORM-ADMIN, ACT-INST-ADMIN | TBD (RGAP-PH01-005) | CNT-ACC-INSTREG §5-§6 |
| SREQ-PH01-INST-004 | Integration configuration and credential issuance | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-012; ADR-015 |
| SREQ-PH01-INST-005 | Credential rotation without disruption | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-012 AC3; ADR-015 |
| SREQ-PH01-INST-006 | Institution deactivation | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CMP-IDN-TENANCY; ADR-011 |
| SREQ-PH01-INST-009 | Credential rotation transition | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-012 AC3; ADR-015 |
| SREQ-PH01-INST-010 | Revoked credential rejection | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-012 AC3; ADR-015 |

## 4. Acceptance criteria

### Cycle 4 preservation and decomposition record

`SREQ-PH01-INST-005` and its original criterion remain unchanged as a `RETIRED` source record; `INST-009` and `INST-010` separate the evidence-backed rotation transition and revoked-credential rejection. The source's broader “without interrupting service” claim is not proven beyond the stated transition criterion. No transition duration, authentication mode, or revocation-availability mechanism is selected. `ADR-015-GATE`, `RP-16`, and `RGAP-PH01-006` remain open.


| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-INST-001-01 | SREQ-PH01-INST-001 | Two registrations never receive the same platform_institution_id. | RGAP-PH01-001 | Institution record {platform_institution_id, name, status, activation_date, contact_points} — CNT-ACC-INSTREG §4 | FR-012 AC1 |
| AC-PH01-INST-001-02 | SREQ-PH01-INST-001 | The identifier is unchanged across updates, suspension and deactivation. | RGAP-PH01-001 | CNT-ACC-INSTREG §4 | FR-012 AC1 |
| AC-PH01-INST-002-01 | SREQ-PH01-INST-002 | A non-Active institution is reported as non-Active to every status lookup. | RGAP-PH01-001 | Registry status — CNT-ACC-INSTREG §4 | FR-012 AC2; FN-INT-PUBLISH P1 |
| AC-PH01-INST-002-02 | SREQ-PH01-INST-002 | Each status transition is recorded as an audit event with actor and timestamp. | RGAP-PH01-004 | CNT-ACC-AUDIT | FR-012 AC2; FN-INT-PUBLISH P1 |
| AC-PH01-INST-003-01 | SREQ-PH01-INST-003 | Lookup is limited to authorized platform services. | RGAP-PH01-001 | Consumers: Identity, Integration — CNT-ACC-INSTREG §2 | CNT-ACC-INSTREG §5-§6 |
| AC-PH01-INST-003-02 | SREQ-PH01-INST-003 | With the registry unavailable, integration flows pause; staleness of cached config is bounded by a policy value, not an asserted number. | RGAP-PH01-001 | CNT-ACC-INSTREG §6; policy store RGAP-PH01-007 | CNT-ACC-INSTREG §5-§6 |
| AC-PH01-INST-004-01 | SREQ-PH01-INST-004 | Configuration exists per institution and is retrievable only by authorized services. | RGAP-PH01-001 | Integration configuration — CNT-ACC-INSTREG §4 | FR-012; ADR-015 |
| AC-PH01-INST-004-02 | SREQ-PH01-INST-004 | Secret material is stored protected and is not returned by lookup operations. | RGAP-PH01-001 | CNT-ACC-INSTREG §7 (ASSUMPTION in source) | FR-012; ADR-015 |
| AC-PH01-INST-005-01 | SREQ-PH01-INST-005 | During the approved transition policy both old and new credentials are accepted; after it only the new one; a revoked credential is rejected. | RGAP-PH01-006 | ADR-015 lifecycle; transition policy deployment-specific (FN-INT-PUBLISH §8) | FR-012 AC3; ADR-015 |
| AC-PH01-INST-006-01 | SREQ-PH01-INST-006 | After deactivation membership lookups return no institutional scope and tokens carry no institutional claims. | RGAP-PH01-001 | CMP-IDN-TENANCY §8 | CMP-IDN-TENANCY; ADR-011 |
| AC-PH01-INST-006-02 | SREQ-PH01-INST-006 | Deactivation requires the approval mandated by policy (HIGH_RISK operation; flow not defined). | RGAP-PH01-003 | ADR-011 §3 | CMP-IDN-TENANCY; ADR-011 |
| AC-PH01-INST-009-01 | SREQ-PH01-INST-009 | During the approved transition policy both old and new credentials are accepted; after it only the new credential is accepted. | RGAP-PH01-006 | ADR-015 lifecycle; transition policy deployment-specific (FN-INT-PUBLISH §8) | FR-012 AC3; ADR-015 |
| AC-PH01-INST-010-01 | SREQ-PH01-INST-010 | A revoked credential is rejected. | RGAP-PH01-006 | ADR-015 lifecycle; no revocation-availability policy is inferred | FR-012 AC3; ADR-015 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Institution not found or not Active: dependent flows (PH-02 publication) must treat it as unauthorized (FN-INT-PUBLISH P1).
- Registry unavailable: dependent flows pause; stale-config TTL is UNKNOWN.
- Plan/tier structure of the institution record is UNKNOWN (CNT-ACC-INSTREG §4).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH01-INST-002 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-INST-003 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH01-INST-003 |
| ADR-015-GATE | ADR-015 per-institution auth mode, connectivity mode and release trust are proposed baselines pending owner/security approval. | SREQ-PH01-INST-004, SREQ-PH01-INST-005 (historical), SREQ-PH01-INST-009, SREQ-PH01-INST-010 |
| RP-16 | Institutional auth mode, executable API/event schemas, key lifecycle and replay tests not ratified. | SREQ-PH01-INST-004, SREQ-PH01-INST-005 (historical), SREQ-PH01-INST-009, SREQ-PH01-INST-010 |
| ADR-011-GATE | ADR-011 approval flow (4-eyes) and session TTL policy keys not defined; assumption only. | SREQ-PH01-INST-006 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-001 | No registered IF-* contract for Institution Registry operations (registration, activation, lookup, integration-config/credential issuance); event catalogue §5.5 has no institution lifecycle event. | Recorded in this document; CNT-ACC-INSTREG §5 lists operations without an interface ID. Route: API Governance (ADR-021, IC-002). |
| RGAP-PH01-004 | No registered IF-* contract or AuditEvent schema for audit write/query. | Recorded in this document; CNT-ACC-AUDIT lists no interface. Route: API Governance (IC-002). |
| RGAP-PH01-007 | Policy store has no registered interface; ADR-022 §8 only names CNT-ACC-INSTREG as the policy-store container; approval-record mechanism unspecified. | Recorded here; route: technical ADR if implementation deviates (ADR-022 §4). |
| RGAP-PH01-006 | Concrete version/schema mapping of the single logical ACCore connector contract is not defined. | ADR-015 and ADR-021 defer it to API Governance; recorded here. |
| RGAP-PH01-003 | No registered IF-* contract for platform user lifecycle, role grant/revoke or support-session operations; PlatformRoleGranted/SupportAccessGranted are named in FR-006 but absent from the §5.5 event catalogue. | Recorded in this document; CNT-ACC-PLATFORMADMIN §2/§5. Route: API Governance (IC-002). |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-012
- c2-containers/accsystem/CNT-ACC-INSTREG.md
- decisions/ADR-011.md, ADR-015.md, ADR-022.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
