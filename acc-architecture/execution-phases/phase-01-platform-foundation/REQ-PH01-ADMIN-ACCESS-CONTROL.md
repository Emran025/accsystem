# REQ-PH01-ADMIN-ACCESS-CONTROL — Platform user, role and administration control

**Document ID:** REQ-PH01-ADMIN-ACCESS-CONTROL  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-ADMIN-ACCESS-CONTROL |
| Phase ID | PH-01 |
| Title | Platform user, role and administration control |
| Statement | Platform user lifecycle and privileged roles are administered through ACManagement acting as a service client of the platform administration and identity services, with least privilege, approval where required and separate admin identities. |
| Actors | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN |
| Locations | SYS-ACMANAGEMENT, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACM-ADMIN, CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | FR-006; CON-006; ADR-009; ADR-011; CNT-ACC-PLATFORMADMIN |

## 2. Scope boundary and phase handoffs

- Support sessions are specified in REQ-PH01-SUPPORT-ACCESS.
- ACCore-local roles remain in CNT-ACR-ORGUSERS and are not administered here.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-ADM-001 | REQ-PH01-ADMIN-ACCESS-CONTROL | An authorized administrator can activate, suspend and reactivate platform accounts and manage institution memberships, and the change takes effect on subsequent authentication. | Administrator performs an account operation in the console. | Account state changes and is enforced. | SYS-ACMANAGEMENT, SYS-ACCSYSTEM | CNT-ACM-ADMIN, CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY | AC-PH01-ADM-001-01, AC-PH01-ADM-001-02 | TEST (planned): account lifecycle test | DRAFT | none recorded |
| SREQ-PH01-ADM-002 | REQ-PH01-ADMIN-ACCESS-CONTROL | A platform role grant or revocation takes effect only after the approval required by policy; until then it remains pending and visible. | A role change is requested. | The change is pending until approved, then applied. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY, CNT-ACM-ADMIN | AC-PH01-ADM-002-01, AC-PH01-ADM-002-02 | TEST (planned): approval workflow test | OWNER_REVIEW | ADR-011-GATE |
| SREQ-PH01-ADM-003 | REQ-PH01-ADMIN-ACCESS-CONTROL | Authorization applies role permissions with contextual conditions (institution, branch, operation scope), and each service enforces its own authorization from resolved role data. | An authenticated request reaches a protected operation. | ALLOW or DENY per role and context. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-ADM-003-01, AC-PH01-ADM-003-02 | TEST (planned): permission matrix test | DRAFT | none recorded |
| SREQ-PH01-ADM-004 | REQ-PH01-ADMIN-ACCESS-CONTROL | ACManagement performs administration only through published platform service APIs and never reads or writes the Identity & Access store directly. | Any console administrative operation. | Every operation is traceable to a platform API call. | SYS-ACMANAGEMENT, SYS-ACCSYSTEM | CNT-ACM-ADMIN, CNT-ACC-APIGATEWAY, CNT-ACC-PLATFORMADMIN | AC-PH01-ADM-004-01 | REVIEW (planned): architecture/integration review | DRAFT | none recorded |
| SREQ-PH01-ADM-005 | REQ-PH01-ADMIN-ACCESS-CONTROL | Platform administrator accounts are distinct from institution ERP accounts. | A platform administrator account is created. | The account is not an ERP account. | SYS-ACCSYSTEM | CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN | AC-PH01-ADM-005-01 | TEST (planned): identity separation test | DRAFT | none recorded |
| SREQ-PH01-ADM-006 | REQ-PH01-ADMIN-ACCESS-CONTROL | Institution administrators use the protected console only within institution-scoped functions defined by an approved role matrix. | An institution administrator opens the console. | Only approved institution-scoped functions are available. | SYS-ACMANAGEMENT, SYS-ACCSYSTEM | CNT-ACM-ADMIN, CNT-ACC-IDENTITY | AC-PH01-ADM-006-01 | REVIEW (planned): role-matrix review | OWNER_REVIEW | ADR-011-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-ADM-001 | Account lifecycle administration | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-006 |
| SREQ-PH01-ADM-002 | Role grant with approval | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-006; ADR-011 |
| SREQ-PH01-ADM-003 | RBAC/ABAC authorization | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF, ACT-INST-ADMIN | TBD (RGAP-PH01-005) | CMP-IDN-RBAC; security-view §3 |
| SREQ-PH01-ADM-004 | ACManagement acts only as service client | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CON-006; ADR-009 |
| SREQ-PH01-ADM-005 | Separate admin identities | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | FR-006 AC3 |
| SREQ-PH01-ADM-006 | Institution-admin console scope | ACT-INST-ADMIN | TBD (RGAP-PH01-005) | CNT-ACM-ADMIN; traceability-24-topics.md topic 14 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-ADM-001-01 | SREQ-PH01-ADM-001 | A suspended account cannot obtain new tokens; PlatformUserSuspended/Activated/Reactivated events are published. | RGAP-PH01-003 | CNT-ACC-IDENTITY §2 | FR-006 |
| AC-PH01-ADM-001-02 | SREQ-PH01-ADM-001 | The operation requires an MFA-authenticated administrator session. | RGAP-PH01-002 | FR-006 normal path | FR-006 |
| AC-PH01-ADM-002-01 | SREQ-PH01-ADM-002 | Where policy mandates approval, a pending state is shown and no permission change applies before approval. | RGAP-PH01-003 | FR-006 AC4/A1 | FR-006; ADR-011 |
| AC-PH01-ADM-002-02 | SREQ-PH01-ADM-002 | PLATFORM_ADMIN and SUPPORT_STAFF grants are subject to strict approval; the approval flow is not defined. | RGAP-PH01-003 | ADR-011 §3 | FR-006; ADR-011 |
| AC-PH01-ADM-003-01 | SREQ-PH01-ADM-003 | A permitted role is allowed and audited; a privilege-escalation attempt is denied and raises a security alert. | RGAP-PH01-002 | CMP-IDN-RBAC §8 | CMP-IDN-RBAC; security-view §3 |
| AC-PH01-ADM-003-02 | SREQ-PH01-ADM-003 | A role change is reflected in permission evaluation within the token TTL. | RGAP-PH01-002 | CMP-IDN-RBAC §8 | CMP-IDN-RBAC; security-view §3 |
| AC-PH01-ADM-004-01 | SREQ-PH01-ADM-004 | No direct data path from the console to the identity store exists; all operations pass the gateway. | RGAP-PH01-003 | FR-006 AC5; CON-006 | CON-006; ADR-009 |
| AC-PH01-ADM-005-01 | SREQ-PH01-ADM-005 | An administrator identity cannot be used as, nor shares credentials with, an ACCore ERP account. | RGAP-PH01-002 | FR-006 AC3 | FR-006 AC3 |
| AC-PH01-ADM-006-01 | SREQ-PH01-ADM-006 | Scope is enforced by the approved role matrix; functions outside it are denied. | RGAP-PH01-012 | CNT-ACM-ADMIN §2 (ASSUMPTION) | CNT-ACM-ADMIN; traceability-24-topics.md topic 14 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Approval workflow engine is UNKNOWN; pending grants stay pending without automatic escalation (CNT-ACC-PLATFORMADMIN §5).
- Break-glass emergency access for administrators is UNKNOWN (actors document).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-011-GATE | ADR-011 approval flow (4-eyes) and session TTL policy keys not defined; assumption only. | SREQ-PH01-ADM-002, SREQ-PH01-ADM-006 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-003 | No registered IF-* contract for platform user lifecycle, role grant/revoke or support-session operations; PlatformRoleGranted/SupportAccessGranted are named in FR-006 but absent from the §5.5 event catalogue. | Recorded in this document; CNT-ACC-PLATFORMADMIN §2/§5. Route: API Governance (IC-002). |
| RGAP-PH01-002 | No registered IF-* contract for authentication, token validation, session revocation or role lookup; token format and TTL are UNKNOWN. | Recorded in this document; CNT-ACC-IDENTITY §3/§5. Route: API Governance (IC-002) and Security owner. |
| RGAP-PH01-012 | Boundary of institution-admin scope in the protected console (and the "complaint separation" in traceability topic 14) has no functional source. | Recorded here; actors-and-external-systems.md ACT-INST-ADMIN open question. |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-PLATFORMADMIN.md
- c2-containers/acmanagement/CNT-ACM-ADMIN.md
- decisions/ADR-009.md, ADR-011.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
