# REQ-PH03-SOFTWARE-LICENSE-ISSUANCE — Marketplace software license issuance from confirmed orders

**Document ID:** REQ-PH03-SOFTWARE-LICENSE-ISSUANCE  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-SOFTWARE-LICENSE-ISSUANCE |
| Phase ID | PH-03 |
| Title | Marketplace software license issuance from confirmed orders |
| Statement | A confirmed order containing licensed software triggers idempotent license issuance for the buyer, with token generation as a recoverable follow-up and validation by the marketplace identity path. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-LICENSE, CNT-ACC-EVENTBUS, CNT-ACC-ORDERS, CNT-ACC-IDENTITY |
| Related function/use case | FN-LIC-ACTIVATE |
| Status | DRAFT |
| Evidence | FN-LIC-ACTIVATE; FR-005; FR-013; IF-ACC-ORDER-CONFIRM; ADR-014 |

## 2. Scope boundary and phase handoffs

- Owner gate RGAP-PH03-009: phase placement is not explicit in execution-phases/README.md; it is placed here because the trigger OrderConfirmed first exists in PH-03. Owner review required.
- Institutional licenses are in PH-01 (REQ-PH01-LICENSE-LIFECYCLE).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-MLS-001 | REQ-PH03-SOFTWARE-LICENSE-ISSUANCE | Upon OrderConfirmed for a software item, the License service creates a license for the buyer, bounded to the confirmed order line and product. | OrderConfirmed with a licensed product line is consumed. | A license exists for the buyer. | SYS-ACCSYSTEM | CNT-ACC-LICENSE, CNT-ACC-EVENTBUS, CNT-ACC-ORDERS | AC-PH03-MLS-001-01 | TEST (planned): activation test | OWNER_REVIEW | none recorded |
| SREQ-PH03-MLS-002 | REQ-PH03-SOFTWARE-LICENSE-ISSUANCE | Replayed confirmation does not issue a duplicate license and distinct order lines are not suppressed. | The confirmation event is replayed. | One license per order line. | SYS-ACCSYSTEM | CNT-ACC-LICENSE | AC-PH03-MLS-002-01 | TEST (planned): replay test | OWNER_REVIEW | none recorded |
| SREQ-PH03-MLS-003 | REQ-PH03-SOFTWARE-LICENSE-ISSUANCE | Token generation after license creation is retried without implying readiness before signing succeeds. | Signing fails or is delayed. | License exists; token pending. | SYS-ACCSYSTEM | CNT-ACC-LICENSE | AC-PH03-MLS-003-01 | TEST (planned): signing failure test | OWNER_REVIEW | LIC-004 |
| SREQ-PH03-MLS-004 | REQ-PH03-SOFTWARE-LICENSE-ISSUANCE | The buyer-facing validation uses {buyer_id, product_id} through the proposed marketplace branch of license validation. | A buyer app validates its license. | Result per proposed branch. | SYS-ACCSYSTEM | CNT-ACC-LICENSE, CNT-ACC-IDENTITY | AC-PH03-MLS-004-01 | REVIEW (planned): contract approval | OWNER_REVIEW | LIC-006, UNKN-007 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-MLS-001 | Issue on OrderConfirmed | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-LIC-ACTIVATE | FN-LIC-ACTIVATE |
| SREQ-PH03-MLS-002 | Idempotent per order line | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-LIC-ACTIVATE | FN-LIC-ACTIVATE |
| SREQ-PH03-MLS-003 | Token follow-up recoverable | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-LIC-ACTIVATE | FN-LIC-ACTIVATE |
| SREQ-PH03-MLS-004 | Buyer validation path | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-LIC-ACTIVATE | FN-LIC-VALIDATE; IF-ACC-LICENSE-VALIDATE §6.3 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-MLS-001-01 | SREQ-PH03-MLS-001 | Confirmed order with software yields a license; orders without software yield none. | NOT SPECIFIED (source reference gap: RGAP-PH03-009) | FN-LIC-ACTIVATE §3-§4 | FN-LIC-ACTIVATE |
| AC-PH03-MLS-002-01 | SREQ-PH03-MLS-002 | Replay returns the existing license. | NOT SPECIFIED (source reference gap: RGAP-PH03-009) | FN-LIC-ACTIVATE §6 | FN-LIC-ACTIVATE |
| AC-PH03-MLS-003-01 | SREQ-PH03-MLS-003 | A signing failure does not roll back the license nor claim a ready token. | NOT SPECIFIED (source reference gap: RGAP-PH03-009) | FN-LIC-ACTIVATE §6-§7 | FN-LIC-ACTIVATE |
| AC-PH03-MLS-004-01 | SREQ-PH03-MLS-004 | Validation is limited to the buyer's own licenses. | NOT SPECIFIED (source reference gap: RGAP-PH03-009) | interface-contracts.md §6.3 (PROPOSED) | FN-LIC-VALIDATE; IF-ACC-LICENSE-VALIDATE §6.3 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Revocation on order cancellation is not specified in sources.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| LIC-004 | Entitlement token refresh strategy without manual admin action. | SREQ-PH03-MLS-003 |
| LIC-006 | ACCommerce initially free (reported owner direction); future monetization/entitlement model open. | SREQ-PH03-MLS-004 |
| UNKN-007 | ACCommerce individual-user monetization/entitlement model not defined. | SREQ-PH03-MLS-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-009 | Marketplace license validation branch is PROPOSED, not an approved wire contract (interface-contracts.md §6.3); phase placement of marketplace license issuance is not explicit in execution-phases/README.md. | Owner gate recorded here; placed in PH-03 only because its trigger OrderConfirmed first exists in PH-03. |

## 7. Traceability sources

- functions/specs/FN-LIC-ACTIVATE.md
- supporting-views/dynamic-license-flow.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
