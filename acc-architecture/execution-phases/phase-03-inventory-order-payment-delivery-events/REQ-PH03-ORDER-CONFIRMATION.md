# REQ-PH03-ORDER-CONFIRMATION — Order confirmation guards and handoff

**Document ID:** REQ-PH03-ORDER-CONFIRMATION  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-ORDER-CONFIRMATION |
| Phase ID | PH-03 |
| Title | Order confirmation guards and handoff |
| Statement | An order is confirmed only when every required reservation remains accepted and every required payment allocation is definitively successful, committing the immutable snapshot, state and OrderConfirmed event atomically. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-ORDERS, CNT-ACC-PAYMENT, CNT-ACR-OUTBOX, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-EVENTBUS, CNT-ACR-SALES, CNT-ACR-FINANCE |
| Related function/use case | FN-ORD-CONFIRM |
| Status | DRAFT |
| Evidence | FN-ORD-CONFIRM; FR-002 step 8; FR-003; FR-009; ADR-013; ADR-019; CMP-ORD-SNAPSHOT |

## 2. Scope boundary and phase handoffs

- Confirmation is the ACCSystem commitment point, not a distributed commit and not a universal financial posting (ADR-019).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-CNF-001 | REQ-PH03-ORDER-CONFIRMATION | Confirmation requires every SellerOrder reservation still authoritatively accepted and definitive AUTHORIZED or CAPTURED success for every required allocation per its approved mode. | Saga reaches the confirm step. | Confirmed or blocked. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-PAYMENT | AC-PH03-CNF-001-01 | TEST (planned): guard test | DRAFT | none recorded |
| SREQ-PH03-CNF-002 | REQ-PH03-ORDER-CONFIRMATION | Immutable snapshot, Confirmed state and OrderConfirmed outbox record commit in one local transaction. | Confirmation commits. | All three or none. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-ORDERS, CNT-ACR-OUTBOX | AC-PH03-CNF-002-01 | TEST (planned): atomicity test | DRAFT | none recorded |
| SREQ-PH03-CNF-003 | REQ-PH03-ORDER-CONFIRMATION | The snapshot stores price, description, currency, quantity, seller and delivery terms and is never updated. | Order is confirmed. | Snapshot exists and is immutable. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-CNF-003-01 | TEST (planned): snapshot test | DRAFT | UNKN-006 |
| SREQ-PH03-CNF-004 | REQ-PH03-ORDER-CONFIRMATION | Replaying confirmation returns the stored confirmation result even after fulfillment advances. | Confirmation is replayed. | Stored result returned. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-CNF-004-01 | TEST (planned): replay test | DRAFT | none recorded |
| SREQ-PH03-CNF-005 | REQ-PH03-ORDER-CONFIRMATION | Integration delivers OrderConfirmed to each authorized seller (and B2B buyer) institution with only recipient- and role-authorized data via at-least-once delivery. | OrderConfirmed is published. | Each recipient gets its scoped projection. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-EVENTBUS | AC-PH03-CNF-005-01 | TEST (planned): scope test | DRAFT | RP-04 |
| SREQ-PH03-CNF-006 | REQ-PH03-ORDER-CONFIRMATION | ACCore creates its local sale or purchase record and applies its own approved accounting trigger; OrderConfirmed is not a universal journal-posting instruction. | ACCore processes the handoff. | Local records follow institution policy. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-SALES, CNT-ACR-FINANCE | AC-PH03-CNF-006-01 | REVIEW (planned): Finance owner review | OWNER_REVIEW | ODEC-004, ADR-019-GATE, RP-04 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-CNF-001 | Confirmation guards | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FN-ORD-CONFIRM; FR-009 AC1 |
| SREQ-PH03-CNF-002 | Atomic commit | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FN-ORD-CONFIRM |
| SREQ-PH03-CNF-003 | Immutable commercial snapshot | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FR-002 AC3 |
| SREQ-PH03-CNF-004 | Idempotent confirmation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | FN-ORD-CONFIRM §6 |
| SREQ-PH03-CNF-005 | Recipient-scoped handoff | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | IF-ACC-ORDER-CONFIRM §2A; FR-003 AC4 |
| SREQ-PH03-CNF-006 | Local record and accounting trigger | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CONFIRM | ADR-019; FR-003 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-CNF-001-01 | SREQ-PH03-CNF-001 | UNKNOWN or incomplete allocations block confirmation. | IF-ACC-ORDER-CREATE §2.4 | FN-ORD-CONFIRM §3 P1-P3 | FN-ORD-CONFIRM; FR-009 AC1 |
| AC-PH03-CNF-002-01 | SREQ-PH03-CNF-002 | A failed transaction leaves no partial confirmation; relay failure after commit does not undo the order. | IF-ACC-ORDER-CONFIRM §2A | FN-ORD-CONFIRM §4.1 | FN-ORD-CONFIRM |
| AC-PH03-CNF-003-01 | SREQ-PH03-CNF-003 | No update or delete is issued against a snapshot; later product changes do not alter it. | NOT SPECIFIED (source reference gap: RGAP-PH03-006) | FR-002 AC3; CMP-ORD-SNAPSHOT | FR-002 AC3 |
| AC-PH03-CNF-004-01 | SREQ-PH03-CNF-004 | Snapshot and event are not rewritten or republished. | NOT SPECIFIED (source reference gap: RGAP-PH03-006) | FN-ORD-CONFIRM §6 | FN-ORD-CONFIRM §6 |
| AC-PH03-CNF-005-01 | SREQ-PH03-CNF-005 | A recipient never receives another institution's data; distinct buyer and seller effects are not suppressed by one key. | IF-ACC-ORDER-CONFIRM §2A | CMP-INT-ORDERNOTIFY §3 | IF-ACC-ORDER-CONFIRM §2A; FR-003 AC4 |
| AC-PH03-CNF-006-01 | SREQ-PH03-CNF-006 | Financial posting occurs only under the institution's configured trigger. | NOT SPECIFIED (source reference gap: RGAP-PH03-006) | ADR-019; FR-003 AC3 | ADR-019; FR-003 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Downstream capture, stock commit, seller credit and delivery are independent state machines, not synchronous consequences of confirmation.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-019-GATE | ADR-019 governs the institution-local financial journal trigger, not atomic confirmation or recipient projection. | SREQ-PH03-CNF-006 |
| UNKN-006 | Multi-currency and tax/VAT model not defined. | SREQ-PH03-CNF-003 |
| RP-04 | OrderConfirmed vs financial journal posting trigger (interim: ADR-019, approval required). | SREQ-PH03-CNF-005, SREQ-PH03-CNF-006 |
| ODEC-004 | Accounting trigger point for B2B transactions. | SREQ-PH03-CNF-006 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-006 | IF-ACC-ORDER-CONFIRM payload mapping (items/lines/line_items, payment_ref/payment_reference, disclosure scope, snapshot version) is a proposal only. | Recorded here; interface-contracts.md §2A. Route: API Governance. |

## 7. Traceability sources

- functions/specs/FN-ORD-CONFIRM.md
- decisions/ADR-019.md
- c3-components/CNT-ACC-ORDERS/CMP-ORD-SNAPSHOT.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
