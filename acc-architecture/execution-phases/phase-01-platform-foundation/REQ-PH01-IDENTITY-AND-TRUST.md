# REQ-PH01-IDENTITY-AND-TRUST — Platform authentication, sessions and identity linking

**Document ID:** REQ-PH01-IDENTITY-AND-TRUST  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-IDENTITY-AND-TRUST |
| Phase ID | PH-01 |
| Title | Platform authentication, sessions and identity linking |
| Statement | ACCSystem authenticates platform users and service principals, issues short-lived revocable credentials and fails closed, so every later-phase operation runs in an identified, auditable session. |
| Actors | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY, CNT-ACR-ORGUSERS |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | CNT-ACC-IDENTITY; CMP-IDN-AUTH; CMP-IDN-SESSION; idea-derived security view §2; CON-005 |

## 2. Scope boundary and phase handoffs

- Roles for buyers, delivery supervisors and couriers are defined in the RBAC model but their operational use is enabled in later phases.
- Service-principal authentication toward ACCore is covered in REQ-PH01-CORE-CONNECTIVITY.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-AUTH-001 | REQ-PH01-IDENTITY-AND-TRUST | Identity & Access verifies user credentials and issues access and refresh tokens carrying role and institution-membership claims. | A user submits credentials. | Valid credentials yield tokens with role and membership claims. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-AUTH-001-01, AC-PH01-AUTH-001-02 | TEST (planned): login/claims test | RETIRED | ADR-022-GATE, IC-002 |
| SREQ-PH01-AUTH-002 | REQ-PH01-IDENTITY-AND-TRUST | Authentication of platform administrators and support staff requires a second factor. | A privileged account signs in. | No privileged token is issued without completed MFA. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY | AC-PH01-AUTH-002-01 | TEST (planned): privileged login test | DRAFT | ADR-017-GATE |
| SREQ-PH01-AUTH-003 | REQ-PH01-IDENTITY-AND-TRUST | Access tokens are short-lived, refresh tokens rotate on use, and a revoked session or token is rejected on later validation. | Refresh, logout or a security event occurs. | Revoked credentials no longer authenticate. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-AUTH-003-01, AC-PH01-AUTH-003-02 | TEST (planned): revocation test | DRAFT | ADR-011-GATE, ADR-022-GATE |
| SREQ-PH01-AUTH-004 | REQ-PH01-IDENTITY-AND-TRUST | Repeated failed authentication attempts are rate-limited at the gateway, subject to a lockout policy and logged as security signals. | Repeated failed logins occur. | Attempts are throttled/locked per policy and visible as signals. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-AUTH-004-01 | TEST (planned): lockout test | DRAFT | ADR-022-GATE |
| SREQ-PH01-AUTH-005 | REQ-PH01-IDENTITY-AND-TRUST | When credential, session or revocation stores are unavailable, authenticated requests are rejected while public routes stay available per route policy. | An identity dependency is unavailable. | No authenticated access on unverifiable identity. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-AUTH-005-01, AC-PH01-AUTH-005-02 | TEST (planned): identity outage test | DRAFT | none recorded |
| SREQ-PH01-AUTH-006 | REQ-PH01-IDENTITY-AND-TRUST | An institution employee may be linked to a platform membership for marketplace access without transferring ACCore-local roles or credentials. | An employee needs a unified marketplace identity. | A platform identity with institution scope exists; ERP roles stay local. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-IDENTITY, CNT-ACR-ORGUSERS | AC-PH01-AUTH-006-01, AC-PH01-AUTH-006-02 | REVIEW (planned): identity-linking design review | DRAFT | none recorded |
| SREQ-PH01-AUTH-007 | REQ-PH01-IDENTITY-AND-TRUST | Identity & Access accepts matching user credentials and rejects non-matching credentials. | A user submits credentials. | The credential attempt is accepted only when credentials match the account store. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-AUTH-007-01 | TEST (planned): credential verification test | DRAFT | ADR-022-GATE, IC-002 |
| SREQ-PH01-AUTH-008 | REQ-PH01-IDENTITY-AND-TRUST | After successful credential verification, Identity & Access issues access and refresh tokens carrying role and institution-membership claims. | User credential verification succeeds. | The issued token pair carries the resolved role and institution-membership claims. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-AUTH-008-01 | TEST (planned): token claims test | DRAFT | ADR-022-GATE, IC-002 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-AUTH-001 | Authenticate platform users | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CMP-IDN-AUTH §3 |
| SREQ-PH01-AUTH-002 | MFA for privileged accounts | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | CMP-IDN-AUTH §3; ADR-011 |
| SREQ-PH01-AUTH-003 | Short-lived tokens and revocation | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CMP-IDN-SESSION; ADR-011 §3 |
| SREQ-PH01-AUTH-004 | Brute-force limiting | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CMP-IDN-AUTH §3, §5 |
| SREQ-PH01-AUTH-005 | Fail-closed identity | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CNT-ACC-IDENTITY §6 |
| SREQ-PH01-AUTH-006 | Link institution employee to platform membership | ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CNT-ACR-ORGUSERS; CNT-ACC-IDENTITY §1 |
| SREQ-PH01-AUTH-007 | Credential verification | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CMP-IDN-AUTH §3 |
| SREQ-PH01-AUTH-008 | Issue tokens with claims | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-INST-EMPLOYEE | TBD (RGAP-PH01-005) | CMP-IDN-AUTH §3 |

### Cycle 3 preservation and decomposition record

`SREQ-PH01-AUTH-001` and its original criteria `AC-PH01-AUTH-001-01` and `AC-PH01-AUTH-001-02` remain in the document as historical source records; AUTH-001 is now `RETIRED`. The active decomposition is `SREQ-PH01-AUTH-007` (credential acceptance/rejection) and `SREQ-PH01-AUTH-008` (issuance of the claimed access/refresh token pair), each with a unique criterion. The original audit criterion is preserved only on the retired row; active authentication audit coverage remains in `SREQ-PH01-AUD-007`. Actors, locations, C2 containers, use-case gap and open gates on the new rows are conservatively inherited from AUTH-001 and are not claimed as operation-specific mappings. Token format, TTL and contract field details remain open.

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-AUTH-001-01 | SREQ-PH01-AUTH-001 | Valid credentials produce tokens with role and institution claims; invalid ones are rejected. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-AUTH §3 | CMP-IDN-AUTH §3 |
| AC-PH01-AUTH-001-02 | SREQ-PH01-AUTH-001 | Every authentication success and failure is recorded as an audit event. | NOT SPECIFIED (source reference gap: RGAP-PH01-004) | CNT-ACC-AUDIT | CMP-IDN-AUTH §3 |
| AC-PH01-AUTH-002-01 | SREQ-PH01-AUTH-002 | Login without the second factor yields no token; if MFA cannot be completed no privileged token is issued unless an approved fallback policy exists. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-AUTH §3, §5 (fallback UNKNOWN) | CMP-IDN-AUTH §3; ADR-011 |
| AC-PH01-AUTH-003-01 | SREQ-PH01-AUTH-003 | A used refresh token cannot be reused (rotation is a source ASSUMPTION). | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-SESSION §3 | CMP-IDN-SESSION; ADR-011 §3 |
| AC-PH01-AUTH-003-02 | SREQ-PH01-AUTH-003 | After logout or forced revocation, requests with the old token receive 401. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-SESSION §8 | CMP-IDN-SESSION; ADR-011 §3 |
| AC-PH01-AUTH-004-01 | SREQ-PH01-AUTH-004 | Failed attempts are logged; lockout and rate thresholds come from policy values (none asserted). | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-AUTH §5 | CMP-IDN-AUTH §3, §5 |
| AC-PH01-AUTH-005-01 | SREQ-PH01-AUTH-005 | Unavailable session/blacklist store causes rejection of authenticated requests (503/401), not acceptance. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CNT-ACC-IDENTITY §6 | CNT-ACC-IDENTITY §6 |
| AC-PH01-AUTH-005-02 | SREQ-PH01-AUTH-005 | Public-zone routes remain reachable per route policy. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CNT-ACC-APIGATEWAY §6 | CNT-ACC-IDENTITY §6 |
| AC-PH01-AUTH-006-01 | SREQ-PH01-AUTH-006 | The linked identity carries the institution claim but no copy of ACCore-local roles. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CNT-ACR-ORGUSERS §1; CMP-IDN-TENANCY | CNT-ACR-ORGUSERS; CNT-ACC-IDENTITY §1 |
| AC-PH01-AUTH-006-02 | SREQ-PH01-AUTH-006 | ACCSystem does not read the ACCore user store. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CON-001, CON-002 | CNT-ACR-ORGUSERS; CNT-ACC-IDENTITY §1 |
| AC-PH01-AUTH-007-01 | SREQ-PH01-AUTH-007 | Credentials matching the account store are accepted; credentials that do not match are rejected. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-AUTH §3 | CMP-IDN-AUTH §3 |
| AC-PH01-AUTH-008-01 | SREQ-PH01-AUTH-008 | Following successful credential verification, the issued access and refresh tokens carry the resolved role and institution-membership claims; token format and exact wire fields remain unspecified. | NOT SPECIFIED (source reference gap: RGAP-PH01-002) | CMP-IDN-AUTH §3; IC-002 | CMP-IDN-AUTH §3 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Token format (JWT or opaque), TTLs, lockout threshold and SSO/SAML support are UNKNOWN and not invented.
- Whether employees may call ACCSystem APIs independently of ACCore is UNKNOWN (actors-and-external-systems.md).
- Token replay: blacklist check plus short TTL limits exposure.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-AUTH-001 (historical), SREQ-PH01-AUTH-007, SREQ-PH01-AUTH-008, SREQ-PH01-AUTH-003, SREQ-PH01-AUTH-004 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH01-AUTH-001 (historical), SREQ-PH01-AUTH-007, SREQ-PH01-AUTH-008 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH01-AUTH-002 |
| ADR-011-GATE | ADR-011 approval flow (4-eyes) and session TTL policy keys not defined; assumption only. | SREQ-PH01-AUTH-003 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-002 | No registered IF-* contract for authentication, token validation, session revocation or role lookup; token format and TTL are UNKNOWN. | Recorded in this document; CNT-ACC-IDENTITY §3/§5. Route: API Governance (IC-002) and Security owner. |
| RGAP-PH01-004 | No registered IF-* contract or AuditEvent schema for audit write/query. | Recorded in this document; CNT-ACC-AUDIT lists no interface. Route: API Governance (IC-002). |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-IDENTITY.md
- c3-components/CNT-ACC-IDENTITY/
- supporting-views/security-view.md §2

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
