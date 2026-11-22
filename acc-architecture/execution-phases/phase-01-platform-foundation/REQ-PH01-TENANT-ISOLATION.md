# REQ-PH01-TENANT-ISOLATION — Tenant context and cross-institution isolation

**Document ID:** REQ-PH01-TENANT-ISOLATION  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-TENANT-ISOLATION |
| Phase ID | PH-01 |
| Title | Tenant context and cross-institution isolation |
| Statement | Every request and query is bound to an authenticated institution context so one institution cannot read, write or infer another institution's data. |
| Actors | ACT-INST-EMPLOYEE, ACT-INST-ADMIN, ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY, CNT-ACC-INSTREG, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | NFR-004; CON-001; CON-002; CON-005; CMP-IDN-TENANCY |

## 2. Scope boundary and phase handoffs

- No shared database between institutions and API-only integration (CON-001, CON-002) are applied through the acceptance criteria below.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-TEN-001 | REQ-PH01-TENANT-ISOLATION | The institution context of a request is derived from the validated token, never from a client-supplied value alone. | An institution-scoped request arrives. | Context equals the token-bound institution. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-TEN-001-01 | TEST (planned): tenant mismatch test | DRAFT | none recorded |
| SREQ-PH01-TEN-002 | REQ-PH01-TENANT-ISOLATION | A valid credential of institution A cannot read, write or infer institution B data through any ACCSystem API, event or query path. | A cross-tenant access is attempted. | The attempt is denied and recorded. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY, CNT-ACC-INSTREG | AC-PH01-TEN-002-01, AC-PH01-TEN-002-02 | TEST (planned): automated isolation suite and penetration test (acceptance-test-plan.md item 11) | DRAFT | none recorded |
| SREQ-PH01-TEN-003 | REQ-PH01-TENANT-ISOLATION | Tokens of institutional users embed their active institution memberships; a user without active membership receives no institutional scope. | An institutional user authenticates. | Claims reflect only active memberships. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-INSTREG | AC-PH01-TEN-003-01 | TEST (planned): membership resolution test | DRAFT | none recorded |
| SREQ-PH01-TEN-004 | REQ-PH01-TENANT-ISOLATION | Platform administrator access that spans institutions is permitted only under the platform role and always emits an audit event. | A platform administrator accesses data across institutions. | Access succeeds only with the role and is audited. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-AUDIT | AC-PH01-TEN-004-01 | TEST (planned): super-tenant audit test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-TEN-001 | Tenant derived from credential | ACT-INST-EMPLOYEE, ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CON-005; CMP-IDN-TENANCY |
| SREQ-PH01-TEN-002 | Cross-tenant denial | ACT-INST-EMPLOYEE, ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | NFR-004; CON-001 |
| SREQ-PH01-TEN-003 | Membership claims | ACT-INST-EMPLOYEE, ACT-INST-ADMIN, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CMP-IDN-TENANCY |
| SREQ-PH01-TEN-004 | Audited platform-wide access | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CMP-IDN-TENANCY §8; ADR-011 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-TEN-001-01 | SREQ-PH01-TEN-001 | A request whose header/body institution differs from the token is rejected with 403 TENANT_MISMATCH and logged as a security event. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-TENANCY §8 | CON-005; CMP-IDN-TENANCY |
| AC-PH01-TEN-002-01 | SREQ-PH01-TEN-002 | Cross-tenant API calls with valid institution-A credentials return 403 or 404. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | NFR-004 measurement method | NFR-004; CON-001 |
| AC-PH01-TEN-002-02 | SREQ-PH01-TEN-002 | Unauthorized cross-tenant attempts appear in the audit log; no database is shared between institutions. | NOT SPECIFIED (source reference gap: RGAP-PH01-004) | CON-001 | NFR-004; CON-001 |
| AC-PH01-TEN-003-01 | SREQ-PH01-TEN-003 | Membership records {user, institution, role, status} drive the claims; deactivated institutions yield none. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-TENANCY §3-§4 | CMP-IDN-TENANCY |
| AC-PH01-TEN-004-01 | SREQ-PH01-TEN-004 | Cross-tenant access without the platform role is denied; with it, an audit event is always emitted. | NOT SPECIFIED (source reference gap: RGAP-PH01-004) | CMP-IDN-TENANCY §8 | CMP-IDN-TENANCY §8; ADR-011 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Whether employees can bypass the connector to reach ACCSystem directly is UNKNOWN.
- A multi-institution user (e.g. support) is an ASSUMPTION in CMP-IDN-TENANCY.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-002 | No registered IF-* contract for authentication, token validation, session revocation or role lookup; token format and TTL are UNKNOWN. | Recorded in this document; CNT-ACC-IDENTITY §3/§5. Route: API Governance (IC-002) and Security owner. |
| RGAP-PH01-004 | No registered IF-* contract or AuditEvent schema for audit write/query. | Recorded in this document; CNT-ACC-AUDIT lists no interface. Route: API Governance (IC-002). |

## 7. Traceability sources

- c3-components/CNT-ACC-IDENTITY/CMP-IDN-TENANCY.md
- 01-scope/scope-and-requirements.md NFR-004, CON-001/002/005

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
