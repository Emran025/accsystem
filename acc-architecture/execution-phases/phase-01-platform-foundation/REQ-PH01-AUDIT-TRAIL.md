# REQ-PH01-AUDIT-TRAIL — Tamper-evident audit of sensitive platform operations

**Document ID:** REQ-PH01-AUDIT-TRAIL  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-AUDIT-TRAIL |
| Phase ID | PH-01 |
| Title | Tamper-evident audit of sensitive platform operations |
| Statement | Sensitive platform operations produce tamper-evident audit events with actor, action, target, scope, timestamp and outcome. |
| Actors | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG, CNT-ACC-EVENTBUS |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | NFR-009; CON-008; ADR-011 §3; CNT-ACC-AUDIT |

## 2. Scope boundary and phase handoffs

- Audit events for publication, orders, payments and stock arise in later phases and extend this coverage then.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-AUD-001 | REQ-PH01-AUDIT-TRAIL | Each sensitive foundation operation type (authentication, role changes, support sessions, administrative actions, institution changes, license actions, credential changes) generates an audit event. | A sensitive operation is performed. | An audit event exists. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-001-01 | TEST (planned): audit coverage test | RETIRED | UNKN-002 |
| SREQ-PH01-AUD-002 | REQ-PH01-AUDIT-TRAIL | Each audit event records actor, role, operation, target resource, scope, timestamp, session and outcome. | An audit event is written. | All required fields are present. | SYS-ACCSYSTEM | CNT-ACC-AUDIT | AC-PH01-AUD-002-01 | TEST (planned): schema test | DRAFT | none recorded |
| SREQ-PH01-AUD-003 | REQ-PH01-AUDIT-TRAIL | Audit records are append-only and tamper-evident, with no application path that modifies or deletes them. | An attempt is made to alter an audit record. | The record is unchanged and alteration is detectable. | SYS-ACCSYSTEM | CNT-ACC-AUDIT | AC-PH01-AUD-003-01 | REVIEW (planned): storage and integrity review | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-004 | REQ-PH01-AUDIT-TRAIL | When the audit store is unavailable, behavior follows an explicit approved policy per operation class and a sensitive-operation audit event is never silently dropped. | Audit write fails. | Operation is blocked or event buffered per policy. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY | AC-PH01-AUD-004-01 | REVIEW (planned): policy approval | OWNER_REVIEW | ADR-017-GATE, UNKN-002 |
| SREQ-PH01-AUD-005 | REQ-PH01-AUDIT-TRAIL | Audit and event payloads minimize personal data and exclude secrets and payment credentials. | An audit or event payload is built. | No secrets or unnecessary personal data are included. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-EVENTBUS | AC-PH01-AUD-005-01 | REVIEW (planned): payload review | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-006 | REQ-PH01-AUDIT-TRAIL | Audit records are readable only by authorized platform admin/support (read-only) and compliance roles. | A user queries audit records. | Only authorized roles can read. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY | AC-PH01-AUD-006-01 | TEST (planned): audit access test | DRAFT | none recorded |
| SREQ-PH01-AUD-007 | REQ-PH01-AUDIT-TRAIL | Each authentication operation generates an audit event. | An authentication operation is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-007-01 | TEST (planned): authentication audit coverage test | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-008 | REQ-PH01-AUDIT-TRAIL | Each role change generates an audit event. | A role change is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-008-01 | TEST (planned): role-change audit coverage test | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-009 | REQ-PH01-AUDIT-TRAIL | Each support-session operation generates an audit event. | A support-session operation is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-009-01 | TEST (planned): support-session audit coverage test | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-010 | REQ-PH01-AUDIT-TRAIL | Each administrative action generates an audit event. | An administrative action is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-010-01 | TEST (planned): administrative-action audit coverage test | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-011 | REQ-PH01-AUDIT-TRAIL | Each institution change generates an audit event. | An institution change is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-011-01 | TEST (planned): institution-change audit coverage test | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-012 | REQ-PH01-AUDIT-TRAIL | Each license action generates an audit event. | A license action is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-012-01 | TEST (planned): license-action audit coverage test | DRAFT | UNKN-002 |
| SREQ-PH01-AUD-013 | REQ-PH01-AUDIT-TRAIL | Each credential change generates an audit event. | A credential change is performed. | An audit event exists for the operation. | SYS-ACCSYSTEM | CNT-ACC-AUDIT, CNT-ACC-IDENTITY, CNT-ACC-PLATFORMADMIN, CNT-ACC-LICENSE, CNT-ACC-INSTREG | AC-PH01-AUD-013-01 | TEST (planned): credential-change audit coverage test | DRAFT | UNKN-002 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-AUD-001 | Coverage of foundation operations | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009 |
| SREQ-PH01-AUD-002 | Required audit fields | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | FR-006 AC1; NFR-009 |
| SREQ-PH01-AUD-003 | Append-only and tamper-evident | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; CNT-ACC-AUDIT |
| SREQ-PH01-AUD-004 | Audit unavailability policy | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | CNT-ACC-AUDIT §5; NFR-009 |
| SREQ-PH01-AUD-005 | Privacy-minimal payloads | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | IF-ACC-EVENT-ENVELOPE §5.8; CON-004 |
| SREQ-PH01-AUD-006 | Restricted audit access | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | data-architecture.md §2 |
| SREQ-PH01-AUD-007 | Authentication audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |
| SREQ-PH01-AUD-008 | Role-change audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |
| SREQ-PH01-AUD-009 | Support-session audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |
| SREQ-PH01-AUD-010 | Administrative-action audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |
| SREQ-PH01-AUD-011 | Institution-change audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |
| SREQ-PH01-AUD-012 | License-action audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |
| SREQ-PH01-AUD-013 | Credential-change audit coverage | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF | TBD (RGAP-PH01-005) | NFR-009; SREQ-PH01-AUD-001 |

### Cycle 2 preservation and decomposition record

`SREQ-PH01-AUD-001` and its original acceptance criterion `AC-PH01-AUD-001-01` are retained unchanged as historical source records; the broad SREQ is now `RETIRED`. Its seven source-listed operation classes are represented by the DRAFT rows `SREQ-PH01-AUD-007` through `SREQ-PH01-AUD-013`, each with a unique acceptance criterion that checks event existence only. Required event fields remain covered separately by `SREQ-PH01-AUD-002` / `AC-PH01-AUD-002-01`. No operation class or behavior was added beyond the source list.

The actor IDs and C2 container set on the seven DRAFT rows are inherited from the retired aggregate row, not asserted as independently validated per-operation mappings. `RGAP-PH01-005` still blocks a function/use-case mapping, and `UNKN-002` remains open. All seven rows stay `DRAFT`; planned verification is not executed evidence.

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-AUD-001-01 | SREQ-PH01-AUD-001 | Performing each defined operation type yields an audit entry with required fields. | RGAP-PH01-004 | NFR-009 measurement method | NFR-009 |
| AC-PH01-AUD-002-01 | SREQ-PH01-AUD-002 | No audit event lacks actor, operation, target, timestamp or outcome. | RGAP-PH01-004 | FR-006 AC1; ADR-011 §3; NFR-009 | FR-006 AC1; NFR-009 |
| AC-PH01-AUD-003-01 | SREQ-PH01-AUD-003 | No update/delete path exists; an integrity check detects alteration (mechanism unspecified; write-once storage is an ASSUMPTION). | RGAP-PH01-004 | CNT-ACC-AUDIT §3, §6 | NFR-009; CNT-ACC-AUDIT |
| AC-PH01-AUD-004-01 | SREQ-PH01-AUD-004 | For each operation class the approved block-or-buffer policy applies; no event is lost without record. | RGAP-PH01-004 | CNT-ACC-AUDIT §5 (UNKNOWN) | CNT-ACC-AUDIT §5; NFR-009 |
| AC-PH01-AUD-005-01 | SREQ-PH01-AUD-005 | Payload review finds no secrets, raw card data or avoidable personal data. | IF-ACC-EVENT-ENVELOPE §5.8 | security-view; CON-004 | IF-ACC-EVENT-ENVELOPE §5.8; CON-004 |
| AC-PH01-AUD-006-01 | SREQ-PH01-AUD-006 | Unauthorized roles are denied; read-only roles cannot alter records. | RGAP-PH01-004 | data-architecture.md AuditEvent | data-architecture.md §2 |
| AC-PH01-AUD-007-01 | SREQ-PH01-AUD-007 | When an authentication operation is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |
| AC-PH01-AUD-008-01 | SREQ-PH01-AUD-008 | When a role change is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |
| AC-PH01-AUD-009-01 | SREQ-PH01-AUD-009 | When a support-session operation is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |
| AC-PH01-AUD-010-01 | SREQ-PH01-AUD-010 | When an administrative action is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |
| AC-PH01-AUD-011-01 | SREQ-PH01-AUD-011 | When an institution change is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |
| AC-PH01-AUD-012-01 | SREQ-PH01-AUD-012 | When a license action is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |
| AC-PH01-AUD-013-01 | SREQ-PH01-AUD-013 | When a credential change is performed, an audit entry exists for that operation. Required event fields remain covered by AC-PH01-AUD-002-01. | RGAP-PH01-004 | NFR-009 measurement method; AC-PH01-AUD-002-01 for required fields | NFR-009; source category preserved from SREQ-PH01-AUD-001 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Retention period is UNKNOWN (UNKN-002); records needed for reconciliation or statutory audit must not be deleted early.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-002 | Compliance/data-residency/retention framework (PCI-DSS, privacy, audit retention) not defined. | SREQ-PH01-AUD-001, SREQ-PH01-AUD-003, SREQ-PH01-AUD-004, SREQ-PH01-AUD-005, SREQ-PH01-AUD-007, SREQ-PH01-AUD-008, SREQ-PH01-AUD-009, SREQ-PH01-AUD-010, SREQ-PH01-AUD-011, SREQ-PH01-AUD-012, SREQ-PH01-AUD-013 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH01-AUD-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. The seven operation-class rows AUD-007..013 therefore still have no registered function/use case. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-004 | No registered IF-* contract or AuditEvent schema for audit write/query. | Recorded in this document; CNT-ACC-AUDIT lists no interface. Route: API Governance (IC-002). |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md NFR-009
- c2-containers/accsystem/CNT-ACC-AUDIT.md
- decisions/ADR-011.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
