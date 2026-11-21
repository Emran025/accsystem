# REQ-PH01-SUPPORT-ACCESS — Scoped just-in-time support access

**Document ID:** REQ-PH01-SUPPORT-ACCESS  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-SUPPORT-ACCESS |
| Phase ID | PH-01 |
| Title | Scoped just-in-time support access |
| Statement | Platform support staff reach institution data only through explicit, institution-scoped, purpose-bound, time-limited support sessions that are audited and cannot confer permissions or entitlements. |
| Actors | ACT-SUPPORT-STAFF, ACT-INST-ADMIN, ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACMANAGEMENT |
| Primary C4 containers | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY, CNT-ACM-ADMIN, CNT-ACC-LICENSE, CNT-ACC-EVENTBUS, CNT-ACC-AUDIT |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | CON-008; FR-006 A2/AC2; ADR-011; UNKN-008; policy-and-gates.md |

## 2. Scope boundary and phase handoffs

- The consent model (per-session vs pre-authorized) is an open owner decision; requirements apply to whichever model is approved.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-SUP-001 | REQ-PH01-SUPPORT-ACCESS | A support session is created with explicit institution, purpose, function scope and expiry before any institution data is reachable. | Support staff request access. | A scoped session record exists. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY, CNT-ACM-ADMIN | AC-PH01-SUP-001-01, AC-PH01-SUP-001-02 | TEST (planned): support scope test (acceptance-test-plan.md item 11) | DRAFT | none recorded |
| SREQ-PH01-SUP-002 | REQ-PH01-SUPPORT-ACCESS | Support access to institution data requires explicit consent or delegation from an authorized institution party in the form selected by policy. | Support staff request access to institution data. | Without recorded consent/delegation no data access is possible. | SYS-ACCSYSTEM | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY | AC-PH01-SUP-002-01 | REVIEW (planned): consent-model review | OWNER_REVIEW | UNKN-008, ODEC-013, ADR-011-GATE |
| SREQ-PH01-SUP-003 | REQ-PH01-SUPPORT-ACCESS | A support session ends at its granted expiry, not exceeding the approved maximum, and expired sessions are revoked automatically. | Session expiry time is reached. | The session no longer grants access. | SYS-ACCSYSTEM | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY | AC-PH01-SUP-003-01, AC-PH01-SUP-003-02 | TEST (planned): expiry test | DRAFT | UNKN-008, ODEC-013 |
| SREQ-PH01-SUP-004 | REQ-PH01-SUPPORT-ACCESS | A support session cannot grant platform roles or license entitlement. | Support staff act within a session. | Roles and entitlements are unchanged by the session. | SYS-ACCSYSTEM | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY, CNT-ACC-LICENSE | AC-PH01-SUP-004-01 | TEST (planned): privilege boundary test | DRAFT | none recorded |
| SREQ-PH01-SUP-005 | REQ-PH01-SUPPORT-ACCESS | Support sessions default to read-only access unless a broader scope is explicitly approved, and masking applies per approved rules. | A support session is granted. | Default scope is read-only. | SYS-ACCSYSTEM | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY | AC-PH01-SUP-005-01 | TEST (planned): read-only default test | OWNER_REVIEW | UNKN-008, ODEC-013 |
| SREQ-PH01-SUP-006 | REQ-PH01-SUPPORT-ACCESS | Grant, expiry and revocation of support access publish events and audit records. | Support access is granted, expires or is revoked. | Events and audit records exist. | SYS-ACCSYSTEM | CNT-ACC-PLATFORMADMIN, CNT-ACC-EVENTBUS, CNT-ACC-AUDIT | AC-PH01-SUP-006-01 | TEST (planned): audit coverage test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-SUP-001 | Session scope | ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | CON-008; FR-006 AC2 |
| SREQ-PH01-SUP-002 | Authorization basis | ACT-SUPPORT-STAFF, ACT-INST-ADMIN | TBD (RGAP-PH01-005) | FR-006 A2; ADR-011 |
| SREQ-PH01-SUP-003 | Time limit and expiry | ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | FR-006 AC2 |
| SREQ-PH01-SUP-004 | No privilege conferral | ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | CON-007; CON-008 |
| SREQ-PH01-SUP-005 | Least-privilege read-only default | ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | policy-and-gates.md; ADR-011 |
| SREQ-PH01-SUP-006 | Session events and audit | ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | FR-006 AC1; NFR-009 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-SUP-001-01 | SREQ-PH01-SUP-001 | Session record holds {session_id, staff_id, institution_id, purpose, scope, granted_at, expires_at, status}. | RGAP-PH01-003 | CNT-ACC-PLATFORMADMIN §4 | CON-008; FR-006 AC2 |
| AC-PH01-SUP-001-02 | SREQ-PH01-SUP-001 | Access outside the granted institution, purpose or scope is denied. | RGAP-PH01-003 | CON-008 | CON-008; FR-006 AC2 |
| AC-PH01-SUP-002-01 | SREQ-PH01-SUP-002 | A session without the approved consent/delegation record cannot reach institution data. | RGAP-PH01-003 | FR-006 A2 | FR-006 A2; ADR-011 |
| AC-PH01-SUP-003-01 | SREQ-PH01-SUP-003 | After expiry access is denied; a cleanup job revokes sessions not expired on time and alerts operations. | RGAP-PH01-003 | CNT-ACC-PLATFORMADMIN §5 | FR-006 AC2 |
| AC-PH01-SUP-003-02 | SREQ-PH01-SUP-003 | A grant beyond the approved maximum duration is rejected (maximum not asserted). | RGAP-PH01-003 | FR-006 AC2 | FR-006 AC2 |
| AC-PH01-SUP-004-01 | SREQ-PH01-SUP-004 | Attempts to grant roles or entitlements through a support session are denied. | RGAP-PH01-003 | acceptance-test-plan.md item 11; CON-007 | CON-007; CON-008 |
| AC-PH01-SUP-005-01 | SREQ-PH01-SUP-005 | Write operations in a default session are denied; masking follows approved rules (none defined). | RGAP-PH01-003 | policy-and-gates.md support access | policy-and-gates.md; ADR-011 |
| AC-PH01-SUP-006-01 | SREQ-PH01-SUP-006 | SupportAccessGranted/Expired/Revoked events and audit records exist for each lifecycle step. | RGAP-PH01-003 | CNT-ACC-PLATFORMADMIN §2 | FR-006 AC1; NFR-009 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Per-session consent vs pre-authorization remains UNKNOWN; neither is selected here.
- Approval workflow unavailable: pending grants remain pending.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-008 | Support-access policy: per-session consent vs pre-authorized delegation, maximum duration, data masking. | SREQ-PH01-SUP-002, SREQ-PH01-SUP-003, SREQ-PH01-SUP-005 |
| ODEC-013 | Support-access policy: per-session consent vs pre-authorized delegation; maximum duration; data masking. | SREQ-PH01-SUP-002, SREQ-PH01-SUP-003, SREQ-PH01-SUP-005 |
| ADR-011-GATE | ADR-011 approval flow (4-eyes) and session TTL policy keys not defined; assumption only. | SREQ-PH01-SUP-002 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-003 | No registered IF-* contract for platform user lifecycle, role grant/revoke or support-session operations; PlatformRoleGranted/SupportAccessGranted are named in FR-006 but absent from the §5.5 event catalogue. | Recorded in this document; CNT-ACC-PLATFORMADMIN §2/§5. Route: API Governance (IC-002). |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md CON-008, FR-006
- decisions/ADR-011.md
- supporting-views/policy-and-gates.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
