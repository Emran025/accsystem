# REQ-PH03-INVENTORY-COMMITMENT — Authoritative inventory and stock commitment

**Document ID:** REQ-PH03-INVENTORY-COMMITMENT  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-INVENTORY-COMMITMENT |
| Phase ID | PH-03 |
| Title | Authoritative inventory and stock commitment |
| Statement | Inventory remains authoritative at each seller ACCore, and stock is committed against an accepted reservation only when that seller receives its authorized order confirmation, with failures reconciled rather than rolled back implicitly. |
| Actors | ACT-INST-EMPLOYEE |
| Locations | SYS-ACCORE, SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACR-INVENTORY, CNT-ACR-CONNECTOR, CNT-ACR-SALES, CNT-ACC-INTEGRATION |
| Related function/use case | FN-ORD-CONFIRM |
| Status | DRAFT |
| Evidence | FR-002 step 9; FR-003; FN-ORD-CONFIRM §4.1; ADR-001; ADR-006; ADR-019 (negative-scope context only; not a gate for inventory commitment or reconciliation); CMP-CON-ORDERRECEIVER; CNT-ACR-INVENTORY |

## 2. Scope boundary and phase handoffs

- Indicative availability presentation is PH-02. This document covers source inventory and commitment.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-INV-001 | REQ-PH03-INVENTORY-COMMITMENT | ACCSystem holds only reservation request/result state and indicative projections; actual stock and warehouse movement remain in the seller ACCore. | Any inventory decision is needed. | Decision is made at ACCore. | SYS-ACCORE | CNT-ACR-INVENTORY, CNT-ACR-CONNECTOR | AC-PH03-INV-001-01 | REVIEW (planned): data ownership review | DRAFT | none recorded |
| SREQ-PH03-INV-002 | REQ-PH03-INVENTORY-COMMITMENT | ACCore commits stock deduction by consuming the accepted reservation and records the local sale only upon receiving the seller-scoped OrderConfirmed. | Seller ACCore receives OrderConfirmed. | Reservation is CONSUMED/COMMITTED. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY, CNT-ACR-SALES | AC-PH03-INV-002-01 | TEST (planned): commit test | DRAFT | none recorded |
| SREQ-PH03-INV-003 | REQ-PH03-INVENTORY-COMMITMENT | If ACCore does not process the confirmation or the local record fails, the order stays confirmed in ACCSystem in a reconciliation condition and is retried, not rolled back. | Inventory commit fails or the event is not processed. | A pending condition is retained and retried. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY, CNT-ACC-INTEGRATION | AC-PH03-INV-003-01 | TEST (planned): commit failure test | DRAFT | none recorded |
| SREQ-PH03-INV-004 | REQ-PH03-INVENTORY-COMMITMENT | A B2B buyer purchase-document effect at the buyer ACCore never commands seller stock. | A buyer institution receives its purchase handoff. | Only the buyer purchase record is created. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-SALES | AC-PH03-INV-004-01 | TEST (planned): role separation test | DRAFT | none recorded |
| SREQ-PH03-INV-005 | REQ-PH03-INVENTORY-COMMITMENT | Institution-owned warehouse or storage references are carried only where an approved contract defines them. | Order or shipment context needs a warehouse reference. | Reference is present only under an approved contract. | SYS-ACCORE | CNT-ACR-INVENTORY, CNT-ACR-CONNECTOR | AC-PH03-INV-005-01 | REVIEW (planned): contract review | OWNER_REVIEW | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-INV-001 | Inventory authority stays at ACCore | ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | ADR-001; ADR-006 |
| SREQ-PH03-INV-002 | Commit on seller confirmation | ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FR-002 step 9; FN-ORD-CONFIRM |
| SREQ-PH03-INV-003 | Commit failure is reconciled | ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FN-ORD-CONFIRM §7 |
| SREQ-PH03-INV-004 | Buyer purchase does not command seller stock | ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FR-003; CNT-ACR-SALES |
| SREQ-PH03-INV-005 | Warehouse reference handling | ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | execution-phases/README.md §5 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-INV-001-01 | SREQ-PH03-INV-001 | No ACCSystem record is treated as authoritative stock. | IF-ACC-RESERVE-SAGA §3.3 | ADR-001; data-architecture §3 | ADR-001; ADR-006 |
| AC-PH03-INV-002-01 | SREQ-PH03-INV-002 | Stock is deducted only after the confirmation event is processed. | IF-ACC-ORDER-CONFIRM §2A | FN-ORD-CONFIRM §4.1 | FR-002 step 9; FN-ORD-CONFIRM |
| AC-PH03-INV-003-01 | SREQ-PH03-INV-003 | No saga rollback occurs; possible effects are reconciled before repeat. | IF-ACC-ORDER-CONFIRM §2A | FN-ORD-CONFIRM §7 | FN-ORD-CONFIRM §7 |
| AC-PH03-INV-004-01 | SREQ-PH03-INV-004 | Buyer-role handoff causes no seller inventory change. | IF-ACC-ORDER-CONFIRM §2A | CNT-ACR-SALES §2 | FR-003; CNT-ACR-SALES |
| AC-PH03-INV-005-01 | SREQ-PH03-INV-005 | No warehouse reference is invented by ACCSystem. | NOT SPECIFIED (source reference gap: RGAP-PH03-008) | CNT-ACR-INVENTORY §4 | execution-phases/README.md §5 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Reservation release cannot affect CONSUMED/COMMITTED stock.
- Post-confirmation reversal rules need institutional and product approval.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

ADR-019 governs institution-local financial journal posting, not inventory commitment or reconciliation; it is not a gate for this requirement.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|


| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-001 | The catalog has no dedicated FN-* for cancellation, return coordination, refund/void, payment reconciliation, ledger/settlement or external delivery events. The existing DRAFT `FN-ORD-CONFIRM` defines the OrderConfirmed seller-inventory commitment handoff and its retry/reconciliation behavior, so it is the related function for this requirement; this does not create a standalone stock-commit function. | Retained only where no existing catalog function directly relates to the requirement; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH03-008 | Warehouse/storage references are institution-owned data of CNT-ACR-INVENTORY but no contract carries them to ACCSystem. | Recorded here; owner review required before any requirement relies on them. |

## 7. Traceability sources

- functions/specs/FN-ORD-CONFIRM.md
- c3-components/CNT-ACR-CONNECTOR/CMP-CON-ORDERRECEIVER.md
- c2-containers/accore/CNT-ACR-INVENTORY.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
