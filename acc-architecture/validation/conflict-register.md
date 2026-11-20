# Architecture Visual Conflict Register
**Review date:** 2026-11-21
**Status:** `INCOMPLETE` — no unresolved conflict is hidden or relabelled as complete.

## Resolved by current source-backed documentation changes

| ID | Topic | Resolution/evidence | Status |
|---|---|---|---|
| RES-001 | Duplicate focal nodes/self-boundary edges in six C1 views | The current overlay contains one focal node for each named system; no `system boundary` self-edge remains. Genuine actor/system edges were retained. | RESOLVED — diagram defect |
| RES-002 | C3 Integration title/scope mismatch | `c3-components/CNT-ACC-INTEGRATION/component-diagram.md` names `CNT-ACC-INTEGRATION` as its viewpoint and parent. | RESOLVED — title only |
| RES-003 | Payment webhook bypassed adapter | The Payment C3 diagram shows `EXT-PAYMENT-PROVIDER → CMP-PAY-ADAPTER → CMP-PAY-ORCHESTRATOR`; signature verification remains at the adapter. | RESOLVED — visual route |
| RES-004 | C1 arrow interpretation | ADR-020 and the C1 overlay now state initiator direction; the standalone C2 view repeats the convention. | RESOLVED — documentation convention; owner review still separate |
| RES-005 | Mermaid renderer result was stale | A fresh `manus-render-diagram` pass accepted all 29 Mermaid blocks in the current tree, including the newly added relationship view. Earlier 26/28 reports are historical snapshots. | RESOLVED — syntax/render check |

## Open or blocked conflicts

| ID | Severity | Affected sources/IDs | Current evidence | Visual treatment | Required decision/owner |
|---|---|---|---|---|---|
| CON-001 | Critical | `IF-ACC-RESERVE-SAGA`, `IF-ACR-RESERVATION-RESP`, `CMP-INT-RESERVATION`, `CMP-CON-RESERVATION`, `CNT-ACC-ORDERS` | Interface contract TTL rows still suggest release/compensation after time while ADR-006/013/018 require UNKNOWN-safe handling and no effect solely because time passed. | Dynamic purchase flow shows UNKNOWN, reconciliation, and eligible compensation only; context map annotates the conflict. | Architecture + institution/operations owners must approve one versioned reservation/expiry contract. |
| CON-002 | High | `SYS-ACCORE`, `CNT-ACR-CONNECTOR`, `CNT-ACC-INTEGRATION`, ADR-015 | ACCore outbound-default posture and optional protected inbound capability are both documented; a deployment selection is not approved. | Context map shows connector-only boundary and labels command path policy-gated. | Security/operations/institution onboarding owner. |
| CON-003 | High | `IF-ACC-RESERVE-SAGA`, `IF-ACR-RESERVATION-RESP` | Response vocabulary/modality and synchronous vs query/callback delivery are not fully unified across contract and component records. | All alternatives remain labelled in integration/connector C3 views; no single mode is claimed. | API governance + integration owner. |
| CON-004 | High | `CNT-ACC-ORDERS`, `CNT-ACR-SALES`, `CNT-ACR-FINANCE`, ADR-019 | Order confirmation, reservation consumption, SalesOrder creation, and financial journal posting have distinct or open commitment points. | Context map and financial view separate the milestones and mark the trigger UNKNOWN. | Business/finance/institution owners. |
| CON-005 | Medium | `SYS-ACCSYSTEM` C2 views | Registry overlay and standalone C2 diagram are complementary candidates with different relationship selections; neither is authoritative. | Both paths are cross-linked and explicitly labelled complementary; no deletion or precedence is inferred. | Architecture owner must choose precedence or ratify complementary scopes. |
| CON-006 | Medium | publication interfaces and `dynamic-publication-flow.md` | Accepted receipt, Catalog-owned `listing_id` timing, in-progress duplicate response, and later result semantics remain open. | Publication sequence and failure table preserve the queue/acceptance/final-result distinction. | API governance + Catalog + Integration owners. |
| CON-007 | High | license activation/validation views, ADR-014 | Offline credential TTL/grace, revocation visibility, key rotation, and marketplace beneficiary mapping remain unresolved. | License dynamic view shows online/offline alternatives and UNKNOWN annotations. | Business/security/license owners. |

## Non-conflicts and explicit limits

- Registered IDs, parent mappings, document paths, and duplicate-ID checks are structurally consistent in the current repository.
- The conflict register does not claim that a proposed ADR is owner-approved merely because it is present in `registry/decisions.json`.
- Render success is syntax evidence only. It does not prove implementation, deployed connectivity, test execution, security approval, or production readiness.
