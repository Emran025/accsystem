# REQ-PH01-LICENSE-VALIDATION — Institutional license validation (online and offline)

**Document ID:** REQ-PH01-LICENSE-VALIDATION  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-LICENSE-VALIDATION |
| Phase ID | PH-01 |
| Title | Institutional license validation (online and offline) |
| Statement | ACCore can establish whether its institution holds a valid entitlement for a product or module, online or from a locally verified signed credential, without sending ERP data to ACCSystem and failing closed for licensed functions. |
| Actors | ACT-INST-ADMIN, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-LICENSE, CNT-ACC-APIGATEWAY, CNT-ACR-CONNECTOR, CNT-ACC-IDENTITY |
| Related function/use case | FN-LIC-VALIDATE |
| Status | DRAFT |
| Evidence | FN-LIC-VALIDATE; IF-ACC-LICENSE-VALIDATE §6; ADR-014; NFR-005; CMP-LIC-ENTITLEMENT; CMP-CON-LICENSECHECK |

## 2. Scope boundary and phase handoffs

- Only the institutional validation path is in PH-01; the marketplace {buyer_id, product_id} path is proposed and belongs with REQ-PH03-SOFTWARE-LICENSE-ISSUANCE.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-LICV-001 | REQ-PH01-LICENSE-VALIDATION | License & Entitlement evaluates candidate licenses for {institution_id, product_code} in all states and returns lifecycle status and evaluation result without conflating them. | ACCore requests validation with no valid offline credential. | A scoped result (valid, expired, suspended, not found, over capacity) is returned. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-LICENSE, CNT-ACC-APIGATEWAY, CNT-ACR-CONNECTOR | AC-PH01-LICV-001-01, AC-PH01-LICV-001-02 | TEST (planned): validation matrix test | DRAFT | UNKN-003, LIC-003, ADR-017-GATE |
| SREQ-PH01-LICV-002 | REQ-PH01-LICENSE-VALIDATION | Validation requires an authenticated caller authorized for the institutional scope and neither requests nor exposes ERP data. | A validation request arrives. | Only authorized, in-scope callers receive results. | SYS-ACCSYSTEM | CNT-ACC-LICENSE, CNT-ACC-IDENTITY, CNT-ACC-APIGATEWAY | AC-PH01-LICV-002-01, AC-PH01-LICV-002-02 | TEST (planned): auth and scope test | DRAFT | none recorded |
| SREQ-PH01-LICV-003 | REQ-PH01-LICENSE-VALIDATION | ACCore verifies a locally held signed entitlement against the platform public key, checking workflow, institution/product identity and grant bounds, without a network call. | ACCore checks a licensed module without connectivity. | VALID only for a correctly signed, in-scope, in-bounds credential. | SYS-ACCORE | CNT-ACR-CONNECTOR | AC-PH01-LICV-003-01 | TEST (planned): offline token test (acceptance-test-plan.md item 8) | DRAFT | UNKN-009, ODEC-014, LIC-001 |
| SREQ-PH01-LICV-004 | REQ-PH01-LICENSE-VALIDATION | After credential expiry without successful online validation, licensed functions are restricted unless an applicable grace policy is approved, while separately permitted local ERP operation continues. | Offline credential expires with no connectivity. | Licensed functions are restricted; local ERP data is unharmed. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-CONNECTOR, CNT-ACC-LICENSE | AC-PH01-LICV-004-01, AC-PH01-LICV-004-02 | TEST (planned): connectivity-loss/expiry test | OWNER_REVIEW | UNKN-003, UNKN-009, ODEC-008, ODEC-014, IC-008, LIC-001 |
| SREQ-PH01-LICV-005 | REQ-PH01-LICENSE-VALIDATION | Issuing or refreshing an offline credential is a separate retriable license-owned operation, not a side effect of read-only validation. | A credential is issued or refreshed. | Validation stays read-only; issuance is recoverable. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-LICENSE, CNT-ACR-CONNECTOR | AC-PH01-LICV-005-01, AC-PH01-LICV-005-02 | TEST (planned): issuance recovery test | DRAFT | LIC-004 |
| SREQ-PH01-LICV-006 | REQ-PH01-LICENSE-VALIDATION | The platform signing key stays within ACCSystem and rotated keys are accepted by validators holding the active key set; tampered credentials are rejected. | The platform rotates its signing key. | Validators accept new and still-valid keys. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-LICENSE, CNT-ACR-CONNECTOR | AC-PH01-LICV-006-01 | TEST (planned): key rotation test | OWNER_REVIEW | LIC-005 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-LICV-001 | Online institutional validation | ACT-INST-ADMIN, ACT-INST-EMPLOYEE | FN-LIC-VALIDATE | FN-LIC-VALIDATE; FR-005 |
| SREQ-PH01-LICV-002 | Authenticated, scoped, no ERP data | ACT-INST-ADMIN, ACT-INST-EMPLOYEE | FN-LIC-VALIDATE | FR-005 AC2; FN-LIC-VALIDATE §8 |
| SREQ-PH01-LICV-003 | Offline local verification | ACT-INST-ADMIN, ACT-INST-EMPLOYEE | FN-LIC-VALIDATE | FN-LIC-VALIDATE; ADR-014 |
| SREQ-PH01-LICV-004 | Expiry restricts licensed functions | ACT-INST-ADMIN, ACT-INST-EMPLOYEE | FN-LIC-VALIDATE | NFR-005; ADR-017 |
| SREQ-PH01-LICV-005 | Separate token issuance and refresh | ACT-INST-ADMIN, ACT-INST-EMPLOYEE | FN-LIC-VALIDATE | FN-LIC-VALIDATE; CMP-LIC-OFFLINE |
| SREQ-PH01-LICV-006 | Signing key custody and rotation | ACT-INST-ADMIN, ACT-INST-EMPLOYEE | FN-LIC-VALIDATE | ADR-014; CMP-LIC-OFFLINE |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-LICV-001-01 | SREQ-PH01-LICV-001 | Valid, expired, suspended, revoked and not-found licenses yield distinct results; unresolved policy is not reported as VALID. | IF-ACC-LICENSE-VALIDATE §6.4 | FN-LIC-VALIDATE §4 | FN-LIC-VALIDATE; FR-005 |
| AC-PH01-LICV-001-02 | SREQ-PH01-LICV-001 | Selection among eligible candidates is deterministic (proposed: valid_from descending, then stable ID); combination of multiple entitlements remains OPEN. | IF-ACC-LICENSE-VALIDATE §6.4 | CMP-LIC-ENTITLEMENT §3 | FN-LIC-VALIDATE; FR-005 |
| AC-PH01-LICV-002-01 | SREQ-PH01-LICV-002 | Unauthenticated calls get 401; cross-institution queries are denied. | IF-ACC-LICENSE-VALIDATE §6.8 | FN-LIC-VALIDATE §8 | FR-005 AC2; FN-LIC-VALIDATE §8 |
| AC-PH01-LICV-002-02 | SREQ-PH01-LICV-002 | Request and response contain no ERP data. | IF-ACC-LICENSE-VALIDATE §6.4 | FR-005 AC2 | FR-005 AC2; FN-LIC-VALIDATE §8 |
| AC-PH01-LICV-003-01 | SREQ-PH01-LICV-003 | Invalid signature, missing key or mismatched identity never yields VALID. | IF-ACC-LICENSE-VALIDATE §6.5 | FN-LIC-VALIDATE §4 offline | FN-LIC-VALIDATE; ADR-014 |
| AC-PH01-LICV-004-01 | SREQ-PH01-LICV-004 | EXPIRED_OFFLINE restricts licensed modules; no grace applies unless approved. | IF-ACC-LICENSE-VALIDATE §6.7 | FN-LIC-VALIDATE §7 | NFR-005; ADR-017 |
| AC-PH01-LICV-004-02 | SREQ-PH01-LICV-004 | Permitted local ERP operations continue and data is not corrupted. | IF-ACC-LICENSE-VALIDATE §6.5 | ADR-017 | NFR-005; ADR-017 |
| AC-PH01-LICV-005-01 | SREQ-PH01-LICV-005 | A validation call changes no state. | IF-ACC-LICENSE-VALIDATE §6.6 | FN-LIC-VALIDATE §6 | FN-LIC-VALIDATE; CMP-LIC-OFFLINE |
| AC-PH01-LICV-005-02 | SREQ-PH01-LICV-005 | Signing failure leaves issuance work durable and retriable; no readiness claim precedes successful signing. | RGAP-PH01-009 | FN-LIC-ACTIVATE §6; CMP-LIC-OFFLINE §5 | FN-LIC-VALIDATE; CMP-LIC-OFFLINE |
| AC-PH01-LICV-006-01 | SREQ-PH01-LICV-006 | After rotation, tokens signed with the new key verify; tampered payloads fail. | IF-ACC-LICENSE-VALIDATE §6.5 | CMP-LIC-OFFLINE §8 | ADR-014; CMP-LIC-OFFLINE |

## 5. Alternate paths, failure, exception and uncertainty handling

- License DB unavailable: online result is an error and ACCore falls back to a valid cached credential.
- Key compromise: emergency rotation procedure UNKNOWN.
- Revocation window between revocation and offline credential expiry is an unresolved risk (LIC-002).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-003 | License model granularity, renewal cycle and grace-period duration not defined. | SREQ-PH01-LICV-001, SREQ-PH01-LICV-004 |
| LIC-003 | Seat overuse enforcement: block vs alert vs retroactive billing. | SREQ-PH01-LICV-001 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH01-LICV-001 |
| UNKN-009 | License offline-validation strategy and grace period not defined. | SREQ-PH01-LICV-003, SREQ-PH01-LICV-004 |
| ODEC-014 | License offline-validation strategy: short-lived signed token vs mandatory periodic connectivity. | SREQ-PH01-LICV-003, SREQ-PH01-LICV-004 |
| LIC-001 | Offline tolerance window: entitlement TTL and grace-period duration. | SREQ-PH01-LICV-003, SREQ-PH01-LICV-004 |
| ODEC-008 | ACCore offline behavior scope (which modules operate offline and for how long). | SREQ-PH01-LICV-004 |
| IC-008 | Grace period for expired-license offline operation not specified. | SREQ-PH01-LICV-004 |
| LIC-004 | Entitlement token refresh strategy without manual admin action. | SREQ-PH01-LICV-005 |
| LIC-005 | Platform public-key rotation propagation to ACCore instances. | SREQ-PH01-LICV-006 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-009 | Event catalogue §5.5 lists LicenseIssued/Activated/Revoked only; FR-005/FR-013 also name LicenseRenewed/Suspended/Expired; license admin API has no IF-* ID. | Recorded here; route: API Governance (IC-002). |

## 7. Traceability sources

- functions/specs/FN-LIC-VALIDATE.md
- supporting-views/interface-contracts.md §6
- decisions/ADR-014.md
- c3-components/CNT-ACC-LICENSE/, CNT-ACR-CONNECTOR/CMP-CON-LICENSECHECK.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
