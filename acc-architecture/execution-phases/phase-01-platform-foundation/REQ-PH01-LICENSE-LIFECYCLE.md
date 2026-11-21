# REQ-PH01-LICENSE-LIFECYCLE — Institutional license issuance and lifecycle

**Document ID:** REQ-PH01-LICENSE-LIFECYCLE  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-LICENSE-LIFECYCLE |
| Phase ID | PH-01 |
| Title | Institutional license issuance and lifecycle |
| Statement | Institutional licenses and signed entitlements are issued, activated, renewed, suspended, revoked and expired under an auditable lifecycle independent of user permissions. |
| Actors | ACT-PLATFORM-ADMIN, ACT-INST-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACMANAGEMENT, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-INSTREG, CNT-ACC-AUDIT, CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-IDENTITY |
| Related function/use case | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) |
| Status | DRAFT |
| Evidence | FR-005; FR-013; CON-007; ADR-010; ADR-014; CNT-ACC-LICENSE |

## 2. Scope boundary and phase handoffs

- Only the institutional workflow (institution_id + product_code) is in PH-01. The marketplace post-purchase license (FN-LIC-ACTIVATE) depends on OrderConfirmed and is in REQ-PH03-SOFTWARE-LICENSE-ISSUANCE.
- License plan attributes, prices, limits and renewal policy are configurable and not invented (FR-005 status).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-LIC-001 | REQ-PH01-LICENSE-LIFECYCLE | On an authorized request License & Entitlement validates institution eligibility and plan and issues an institutional license in state ISSUED bound to the institution and product. | Administrator submits a license request through ACManagement. | A license record with product, modules, seats/capacity and validity exists. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-INSTREG | AC-PH01-LIC-001-01, AC-PH01-LIC-001-02 | TEST (planned): issuance test | RETIRED | UNKN-003, ODEC-011, ADR-017-GATE |
| SREQ-PH01-LIC-002 | REQ-PH01-LICENSE-LIFECYCLE | Every issued institutional entitlement is cryptographically signed by the platform. | A license is issued. | The entitlement is verifiable with the platform public key. | SYS-ACCSYSTEM | CNT-ACC-LICENSE | AC-PH01-LIC-002-01 | TEST (planned): signature verification test | DRAFT | LIC-005 |
| SREQ-PH01-LIC-003 | REQ-PH01-LICENSE-LIFECYCLE | An institutional subscription progresses ISSUED to ACTIVATED to ACTIVE, and transitions outside the permitted graph are rejected. | An administrator activates a subscription. | State follows the permitted graph. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN | AC-PH01-LIC-003-01 | TEST (planned): state machine test | DRAFT | none recorded |
| SREQ-PH01-LIC-004 | REQ-PH01-LICENSE-LIFECYCLE | License state changes are applied by authorized actors or scheduled policy with actor, reason, timestamp and affected institution/product recorded; revocation is permanent. | An administrator action, scheduled expiry or policy trigger occurs. | The license is in the new state with a record. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-AUDIT | AC-PH01-LIC-004-01, AC-PH01-LIC-004-02 | TEST (planned): lifecycle test | RETIRED | UNKN-003, LIC-001 |
| SREQ-PH01-LIC-005 | REQ-PH01-LICENSE-LIFECYCLE | A license state-change event reaches the ACCore license connector, which restricts or restores licensed modules within the approved propagation window. | A suspension, revocation, expiry or renewal event is published. | ACCore applies the restriction or restoration. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-LICENSE, CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH01-LIC-005-01, AC-PH01-LIC-005-02 | TEST (planned): propagation test (acceptance-test-plan.md item 8) | RETIRED | LIC-002, UNKN-009, ADR-017-GATE |
| SREQ-PH01-LIC-006 | REQ-PH01-LICENSE-LIFECYCLE | License entitlement does not grant platform user permissions, and user permissions do not confer entitlement. | A license is issued or a role is granted. | The other dimension is unchanged. | SYS-ACCSYSTEM | CNT-ACC-LICENSE, CNT-ACC-IDENTITY | AC-PH01-LIC-006-01 | TEST (planned): orthogonality test | DRAFT | none recorded |
| SREQ-PH01-LIC-007 | REQ-PH01-LICENSE-LIFECYCLE | License & Entitlement rejects an institutional license request when institution eligibility or plan validation fails, without creating a license record. | An administrator submits an institutional license request. | An ineligible institution or invalid plan does not produce a license record. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-INSTREG | AC-PH01-LIC-007-01 | TEST (planned): eligibility and plan rejection test | DRAFT | UNKN-003, ODEC-011, ADR-017-GATE |
| SREQ-PH01-LIC-008 | REQ-PH01-LICENSE-LIFECYCLE | After an authorized institutional license request passes eligibility and plan validation, License & Entitlement creates a license bound to the institution and product in state ISSUED. | An authorized administrator request passes institution and plan validation. | The institutional license record exists in state ISSUED. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-INSTREG | AC-PH01-LIC-008-01 | TEST (planned): institutional ISSUED-record test | DRAFT | UNKN-003, ODEC-011, ADR-017-GATE |
| SREQ-PH01-LIC-009 | REQ-PH01-LICENSE-LIFECYCLE | When an authorized actor or scheduled policy applies a license state change (including renewal, suspension, revocation, or expiry), the change is recorded with actor, reason, timestamp, and affected institution/product. | An authorized actor or scheduled policy applies a license state change. | The state-change record contains actor, reason, timestamp, institution, and product. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-AUDIT | AC-PH01-LIC-009-01 | TEST (planned): license state-change audit test | DRAFT | UNKN-003, LIC-001 |
| SREQ-PH01-LIC-010 | REQ-PH01-LICENSE-LIFECYCLE | A revoked license never returns to Active. | A license is revoked. | The revoked license does not return to Active; expiry/grace timing is not asserted. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-LICENSE, CNT-ACM-ADMIN, CNT-ACC-AUDIT | AC-PH01-LIC-010-01 | TEST (planned): revoked-license terminality test | DRAFT | UNKN-003, LIC-001 |
| SREQ-PH01-LIC-011 | REQ-PH01-LICENSE-LIFECYCLE | A published license state-change event is delivered to the ACCore license connector under the Outbox/Inbox rules; event mapping and numeric propagation policy remain open. | A license state-change event is published. | The event reaches the ACCore license connector under the stated delivery rules. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-LICENSE, CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH01-LIC-011-01 | TEST (planned): license event Outbox/Inbox delivery test | DRAFT | LIC-002, UNKN-009, ADR-017-GATE |
| SREQ-PH01-LIC-012 | REQ-PH01-LICENSE-LIFECYCLE | After a LicenseSuspended event, ACCore restricts the licensed module; no numeric propagation window is asserted. | A LicenseSuspended event is published. | The licensed module is restricted in ACCore; propagation timing remains open. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-LICENSE, CNT-ACC-EVENTBUS, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH01-LIC-012-01 | TEST (planned): LicenseSuspended restriction test | DRAFT | LIC-002, UNKN-009, ADR-017-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-LIC-001 | Issue institutional license | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-005 |
| SREQ-PH01-LIC-002 | Signed entitlement | ACT-PLATFORM-ADMIN, ACT-INST-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-005 AC1; ADR-014 |
| SREQ-PH01-LIC-003 | Activation progression | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | CMP-LIC-LIFECYCLE |
| SREQ-PH01-LIC-004 | Renew, suspend, revoke, expire | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-013 |
| SREQ-PH01-LIC-005 | Propagation to ACCore | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-013; FR-005 |
| SREQ-PH01-LIC-006 | Entitlement is not permission | ACT-PLATFORM-ADMIN, ACT-INST-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | CON-007; FR-005 AC5 |
| SREQ-PH01-LIC-007 | Reject ineligible issuance request | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-005; CMP-LIC-ISSUANCE §3 |
| SREQ-PH01-LIC-008 | Create institutional license in ISSUED | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-005; CMP-LIC-ISSUANCE §3-4 |
| SREQ-PH01-LIC-009 | Audit record for license state changes | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-013 AC1; FR-005 AC4 |
| SREQ-PH01-LIC-010 | Revocation is terminal | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-013; CMP-LIC-LIFECYCLE §3 |
| SREQ-PH01-LIC-011 | License event delivery to ACCore | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | IF-ACC-EVENT-ENVELOPE §5.6; CNT-ACC-LICENSE §2; FR-013; FR-005 |
| SREQ-PH01-LIC-012 | Suspension restricts licensed modules | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005; related FN-LIC-VALIDATE in REQ-PH01-LICENSE-VALIDATION) | FR-013 AC2; FR-005 A2 |

### Cycle 3 preservation and decomposition record

`SREQ-PH01-LIC-001` and its original criteria `AC-PH01-LIC-001-01` and `AC-PH01-LIC-001-02` remain unchanged as historical source records; LIC-001 is now `RETIRED`. The active decomposition is `SREQ-PH01-LIC-007` (reject failed eligibility/plan validation without creating a record) and `SREQ-PH01-LIC-008` (create the institution/product-bound license in `ISSUED` state), each with a unique criterion. The declared actor, locations, C2 set, function gap and owner-gated license references are inherited conservatively; no operation-specific container ownership or license-policy values are inferred. Plan granularity, validity/units semantics and other existing license decisions remain open.

## 4. Acceptance criteria

### Cycle 4 preservation and decomposition record

`SREQ-PH01-LIC-005` and its original criteria remain unchanged as a `RETIRED` source record. `LIC-011` covers event delivery and `LIC-012` retains only the evidence-backed `LicenseSuspended` restriction outcome. The source's broader restriction/restoration mapping for revocation, expiry, and renewal, restoration behavior, and propagation timing remain open under `LIC-002`, `UNKN-009`, `ADR-017-GATE`, and `RGAP-PH01-009`; no numeric window or event mapping is inferred.


### Cycle 4 preservation and decomposition record

`SREQ-PH01-LIC-004` and its two original criteria remain unchanged as a `RETIRED` source record; `LIC-009` covers the audit record and `LIC-010` the terminal-revocation invariant. Renewal, suspension, revocation, and expiry remain in the historical source scope, but these children do not define permitted transitions, a state graph, renewal cycle, expiry/grace timing, or other lifecycle policy. `UNKN-003` and `LIC-001` remain open.


| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-LIC-001-01 | SREQ-PH01-LIC-001 | An ineligible institution or invalid plan is rejected without a license record. | RGAP-PH01-009 | FR-005 normal path | FR-005 |
| AC-PH01-LIC-001-02 | SREQ-PH01-LIC-001 | The record carries institution_id, product_code, units, status and validity. | RGAP-PH01-009 | CNT-ACC-LICENSE §4 | FR-005 |
| AC-PH01-LIC-002-01 | SREQ-PH01-LIC-002 | A signed entitlement verifies; a modified one fails verification. | IF-ACC-LICENSE-VALIDATE §6.5 | ADR-014 | FR-005 AC1; ADR-014 |
| AC-PH01-LIC-003-01 | SREQ-PH01-LIC-003 | Invalid transitions are rejected and the state history records actor and reason. | RGAP-PH01-009 | CMP-LIC-LIFECYCLE §3 | CMP-LIC-LIFECYCLE |
| AC-PH01-LIC-004-01 | SREQ-PH01-LIC-004 | Each change records actor, reason, timestamp, institution and product. | RGAP-PH01-009 | FR-013 AC1; FR-005 AC4 | FR-013 |
| AC-PH01-LIC-004-02 | SREQ-PH01-LIC-004 | A revoked license never returns to Active; expiry timing relative to any grace is not asserted. | RGAP-PH01-009 | CMP-LIC-LIFECYCLE §3 | FR-013 |
| AC-PH01-LIC-005-01 | SREQ-PH01-LIC-005 | After a LicenseSuspended event ACCore restricts the module; no numeric window is asserted. | RGAP-PH01-009 | FR-013 AC2; FR-005 A2 | FR-013; FR-005 |
| AC-PH01-LIC-005-02 | SREQ-PH01-LIC-005 | Event delivery follows the Outbox/Inbox rules. | IF-ACC-EVENT-ENVELOPE §5.6 | CNT-ACC-LICENSE §2 | FR-013; FR-005 |
| AC-PH01-LIC-006-01 | SREQ-PH01-LIC-006 | Issuing a license changes no role assignment; granting a role makes no license valid. | RGAP-PH01-009 | FR-005 AC5; CON-007 | CON-007; FR-005 AC5 |
| AC-PH01-LIC-007-01 | SREQ-PH01-LIC-007 | An ineligible institution or invalid plan is rejected and no license record is created. | RGAP-PH01-009 | FR-005 normal path; CMP-LIC-ISSUANCE §3 | FR-005; CMP-LIC-ISSUANCE §3 |
| AC-PH01-LIC-008-01 | SREQ-PH01-LIC-008 | A successful authorized institutional request creates a record bound to institution_id and product_code in state ISSUED, carrying units and validity as specified by the applicable license configuration; no policy values are asserted. | RGAP-PH01-009 | CNT-ACC-LICENSE §4; CMP-LIC-ISSUANCE §3-4 | FR-005; CMP-LIC-ISSUANCE §3-4 |
| AC-PH01-LIC-009-01 | SREQ-PH01-LIC-009 | Each license state change records actor, reason, timestamp, institution and product. | RGAP-PH01-009 | FR-013 AC1; FR-005 AC4 | FR-013 |
| AC-PH01-LIC-010-01 | SREQ-PH01-LIC-010 | A revoked license never returns to Active; expiry timing relative to any grace is not asserted. | RGAP-PH01-009 | CMP-LIC-LIFECYCLE §3 | FR-013 |
| AC-PH01-LIC-011-01 | SREQ-PH01-LIC-011 | License state-change event delivery follows the Outbox/Inbox rules to the ACCore license connector. | IF-ACC-EVENT-ENVELOPE §5.6 | CNT-ACC-LICENSE §2 | FR-013; FR-005 |
| AC-PH01-LIC-012-01 | SREQ-PH01-LIC-012 | After a LicenseSuspended event ACCore restricts the module; no numeric propagation window is asserted. | RGAP-PH01-009 | FR-013 AC2; FR-005 A2 | FR-013; FR-005 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Grace period and its relationship to Expired status are OPEN (UNKN-003); no automatic grace.
- Scheduled expiry job failure: license stays Active past expiry; monitoring alert required.
- Seat overuse enforcement is OPEN (LIC-003).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-003 | License model granularity, renewal cycle and grace-period duration not defined. | SREQ-PH01-LIC-001 (historical), SREQ-PH01-LIC-007, SREQ-PH01-LIC-008, SREQ-PH01-LIC-004 (historical), SREQ-PH01-LIC-009, SREQ-PH01-LIC-010 |
| ODEC-011 | License model: type, granularity, renewal, grace period. | SREQ-PH01-LIC-001 (historical), SREQ-PH01-LIC-007, SREQ-PH01-LIC-008 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH01-LIC-001 (historical), SREQ-PH01-LIC-007, SREQ-PH01-LIC-008, SREQ-PH01-LIC-005 (historical), SREQ-PH01-LIC-011, SREQ-PH01-LIC-012 |
| LIC-005 | Platform public-key rotation propagation to ACCore instances. | SREQ-PH01-LIC-002 |
| LIC-001 | Offline tolerance window: entitlement TTL and grace-period duration. | SREQ-PH01-LIC-004 (historical), SREQ-PH01-LIC-009, SREQ-PH01-LIC-010 |
| LIC-002 | License revocation propagation: how quickly ACCore must honor a revocation. | SREQ-PH01-LIC-005 (historical), SREQ-PH01-LIC-011, SREQ-PH01-LIC-012 |
| UNKN-009 | License offline-validation strategy and grace period not defined; the source criterion establishes only the suspended-event restriction, not the mapping for every lifecycle event. | SREQ-PH01-LIC-005 (historical), SREQ-PH01-LIC-011, SREQ-PH01-LIC-012 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-009 | Event catalogue §5.5 lists LicenseIssued/Activated/Revoked only; FR-005/FR-013 also name LicenseRenewed/Suspended/Expired; license admin API has no IF-* ID. Existing acceptance evidence maps LicenseSuspended to restriction only; effects for revoked, expired, renewed, restoration events, and propagation timing remain undefined. | Blocking event/contract mapping gap; route: API Governance (IC-002) and license owner approval of propagation semantics/timing (`LIC-002`, `UNKN-009`, `ADR-017-GATE`). |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-005, FR-013
- c3-components/CNT-ACC-LICENSE/CMP-LIC-ISSUANCE.md, CMP-LIC-LIFECYCLE.md
- supporting-views/dynamic-license-flow.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
