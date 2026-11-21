# REQ-PH03-ORDER-AGGREGATE — ParentOrder, SellerOrder and order state

**Document ID:** REQ-PH03-ORDER-AGGREGATE  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-ORDER-AGGREGATE |
| Phase ID | PH-03 |
| Title | ParentOrder, SellerOrder and order state |
| Statement | A checkout is represented by one ParentOrder and one SellerOrder per seller with explicit authoritative state, append-only transitions and idempotent creation. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-ORDERS, CNT-ACC-CART, CNT-ACC-APIGATEWAY, CNT-ACR-OUTBOX |
| Related function/use case | FN-ORD-CHECKOUT |
| Status | DRAFT |
| Evidence | FR-002; FR-009; IF-ACC-ORDER-CREATE; CMP-ORD-MULTISELLER; CMP-ORD-STATEMACHINE; ADR-013; ADR-016 |

## 2. Scope boundary and phase handoffs

- Owner gate RGAP-PH02-004: the pre-reservation order shell placement between PH-02 and PH-03 is unresolved; this document covers the order aggregate lifecycle.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-ORD-001 | REQ-PH03-ORDER-AGGREGATE | ParentOrder, all SellerOrders and their outbox records are written in one local transaction, and a repeated split returns the existing orders. | A validated checkout is turned into an order. | N SellerOrders under one ParentOrder. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-CART | AC-PH03-ORD-001-01 | TEST (planned): split test | RETIRED | ODEC-003 |
| SREQ-PH03-ORD-007 | REQ-PH03-ORDER-AGGREGATE | For a validated checkout with one or more sellers, ACCSystem persists one ParentOrder, one SellerOrder per seller, and their corresponding SellerOrderCreated outbox events in one local transaction. | A validated checkout is split into an order. | The ParentOrder, all SellerOrders and their outbox records commit together, or none are committed. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-CART | AC-PH03-ORD-007-01 | TEST (planned): aggregate/outbox transaction atomicity test | DRAFT | ODEC-003, IC-002, ADR-021-GATE, RGAP-PH02-004 |
| SREQ-PH03-ORD-008 | REQ-PH03-ORDER-AGGREGATE | When a split for the same validated checkout is repeated or concurrently retried, ACCSystem returns the existing ParentOrder and SellerOrders without creating duplicate order or SellerOrderCreated outbox records. | A previously persisted split request is repeated or retried concurrently. | The existing ParentOrder and SellerOrders are returned without duplicate order or outbox records. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-CART | AC-PH03-ORD-008-01 | TEST (planned): repeated/concurrent split replay test | DRAFT | ODEC-003, IC-002, ADR-021-GATE, RGAP-PH02-004 |
| SREQ-PH03-ORD-002 | REQ-PH03-ORDER-AGGREGATE | Creating an order with the same idempotency key returns the existing order. | Order create is retried. | One order. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-APIGATEWAY | AC-PH03-ORD-002-01 | TEST (planned): duplicate order test | DRAFT | IC-002, ADR-021-GATE |
| SREQ-PH03-ORD-003 | REQ-PH03-ORDER-AGGREGATE | Order state changes follow the permitted transition graph for each SellerOrder and invalid transitions are rejected. | A state change is requested. | Allowed or InvalidStateTransition. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-ORD-003-01 | TEST (planned): transition test | DRAFT | ADR-018-GATE |
| SREQ-PH03-ORD-004 | REQ-PH03-ORDER-AGGREGATE | ParentOrder state is computed from SellerOrder states and never advances independently. | A SellerOrder changes state. | Parent reflects the aggregate. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-ORD-004-01 | TEST (planned): aggregation test | DRAFT | none recorded |
| SREQ-PH03-ORD-005 | REQ-PH03-ORDER-AGGREGATE | Each transition is appended to history together with its outbox event in one transaction, under optimistic concurrency. | A transition commits. | History and event persist together. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-ORDERS, CNT-ACR-OUTBOX | AC-PH03-ORD-005-01 | TEST (planned): concurrency test | DRAFT | IC-004 |
| SREQ-PH03-ORD-006 | REQ-PH03-ORDER-AGGREGATE | Each SellerOrder stores the policy, tax and currency snapshot references that applied, and later policy edits never alter them. | An order is created or confirmed. | Snapshot references are fixed. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-ORD-006-01 | TEST (planned): snapshot immutability test | OWNER_REVIEW | UNKN-006, ODEC-009, ADR-017-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-ORD-001 | Split by seller | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | CMP-ORD-MULTISELLER; ADR-016 |
| SREQ-PH03-ORD-002 | Idempotent order creation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | FR-002 AC2 |
| SREQ-PH03-ORD-003 | State machine enforcement | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | CMP-ORD-STATEMACHINE |
| SREQ-PH03-ORD-004 | Parent state is aggregate | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | CMP-ORD-STATEMACHINE §3.4 |
| SREQ-PH03-ORD-005 | Append-only history atomic with outbox | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | CMP-ORD-STATEMACHINE §4 |
| SREQ-PH03-ORD-006 | Policy and currency snapshot references | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | ADR-017; topics 6 |
| SREQ-PH03-ORD-007 | Atomic aggregate and outbox creation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | CMP-ORD-MULTISELLER §§19-20, 25-26; FN-ORD-CHECKOUT §§11-12 |
| SREQ-PH03-ORD-008 | Duplicate-safe split replay | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT | CMP-ORD-MULTISELLER §§25-26, 30-36; FN-ORD-CHECKOUT §48; ADR-013 §§3-4 |

### Cycle 7 preservation and decomposition record

`SREQ-PH03-ORD-001` and its original criterion `AC-PH03-ORD-001-01` remain unchanged as historical source records; the source row is now `RETIRED`. The evidence-supported decomposition is `SREQ-PH03-ORD-007` for atomic local persistence of the ParentOrder, SellerOrders and their outbox records, and `SREQ-PH03-ORD-008` for duplicate-safe repeated/concurrent split replay. The children conservatively reuse the existing actors, system/container bindings and `FN-ORD-CHECKOUT`; no new function or use-case ID is assigned. `ORD-001` remains distinct from `ORD-002`; no key-equivalence claim or merge is made. `ODEC-003`, `IC-002`, `ADR-021-GATE` and the PH-02/PH-03 placement gap `RGAP-PH02-004` remain open. Child verification is planned only; this decomposition does not assert implementation, test execution, owner approval or readiness.

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-ORD-001-01 | SREQ-PH03-ORD-001 | One seller yields one SellerOrder; concurrent retries create no duplicates. | IF-ACC-ORDER-CREATE §2.4 | CMP-ORD-MULTISELLER tests | CMP-ORD-MULTISELLER; ADR-016 |
| AC-PH03-ORD-002-01 | SREQ-PH03-ORD-002 | Duplicate key returns the existing order_id with no new order. | IF-ACC-ORDER-CREATE §2.5-2.6 | FR-002 AC2 | FR-002 AC2 |
| AC-PH03-ORD-003-01 | SREQ-PH03-ORD-003 | Unlisted transitions are rejected; unknown/review states are non-terminal. | IF-ACC-ORDER-CREATE §2.4 | CMP-ORD-STATEMACHINE §3.2 | CMP-ORD-STATEMACHINE |
| AC-PH03-ORD-004-01 | SREQ-PH03-ORD-004 | Parent state is derivable from SellerOrder states. | IF-ACC-ORDER-CREATE §2.4 | CMP-ORD-STATEMACHINE §3.4 | CMP-ORD-STATEMACHINE §3.4 |
| AC-PH03-ORD-005-01 | SREQ-PH03-ORD-005 | Concurrent transition attempts do not both succeed. | IF-ACC-EVENT-ENVELOPE §5.4 | CMP-ORD-STATEMACHINE §4 | CMP-ORD-STATEMACHINE §4 |
| AC-PH03-ORD-006-01 | SREQ-PH03-ORD-006 | Changing a policy after confirmation leaves the order unchanged. | RGAP-PH03-006 | acceptance-test-plan.md item 9; ADR-017 | ADR-017; topics 6 |
| AC-PH03-ORD-007-01 | SREQ-PH03-ORD-007 | Given a validated checkout, one ParentOrder and one SellerOrder per seller are persisted with their corresponding SellerOrderCreated outbox records in one local transaction; a failure before commit leaves none of those records committed. | IF-ACC-ORDER-CREATE §2.4 (reference only; formal schema approval remains open) | CMP-ORD-MULTISELLER §§19-20, 25-26; FN-ORD-CHECKOUT §§11-12, 28, 34 | CMP-ORD-MULTISELLER; FN-ORD-CHECKOUT |
| AC-PH03-ORD-008-01 | SREQ-PH03-ORD-008 | Given a previously persisted split for the same validated checkout, when the request is repeated or concurrently retried, the existing ParentOrder and SellerOrders are returned and no duplicate order or SellerOrderCreated outbox record is created. | IF-ACC-ORDER-CREATE §§2.5-2.6 (reference only; response/schema approval remains open) | CMP-ORD-MULTISELLER §§25-26, 30-36; FN-ORD-CHECKOUT §48 | CMP-ORD-MULTISELLER; FN-ORD-CHECKOUT; ADR-013 §§3-4 |

## 5. Alternate paths, failure, exception and uncertainty handling

- PENDING_REVIEW and PendingPaymentReview mapping to order states is an owner decision.
- Product-visible partial orders are deferred and cannot occur implicitly (ADR-016).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ODEC-003 | Multi-seller cart model (ParentOrder + SellerOrders); MVP direction recorded in ADR-016. | SREQ-PH03-ORD-001 (RETIRED), SREQ-PH03-ORD-007, SREQ-PH03-ORD-008 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH03-ORD-002, SREQ-PH03-ORD-007, SREQ-PH03-ORD-008 |
| ADR-021-GATE | ADR-021 interface versioning is interim, approval-required. | SREQ-PH03-ORD-002, SREQ-PH03-ORD-007, SREQ-PH03-ORD-008 |
| ADR-018-GATE | ADR-018 reservation TTL values and async-callback mode require per-institution approval. | SREQ-PH03-ORD-003 |
| IC-004 | Message-broker technology, topics, partitioning, retention and ACL design unspecified. | SREQ-PH03-ORD-005 |
| UNKN-006 | Multi-currency and tax/VAT model not defined. | SREQ-PH03-ORD-006 |
| ODEC-009 | Multi-currency and tax model/jurisdiction rules. | SREQ-PH03-ORD-006 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH03-ORD-006 |
| RGAP-PH02-004 | Placement of the pre-reservation order shell between PH-02 checkout preparation and PH-03 order aggregate remains unresolved; see REQ-PH02-CHECKOUT-PREPARATION §6 and this document §2. | SREQ-PH03-ORD-001 (RETIRED), SREQ-PH03-ORD-007, SREQ-PH03-ORD-008 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-006 | IF-ACC-ORDER-CONFIRM payload mapping (items/lines/line_items, payment_ref/payment_reference, disclosure scope, snapshot version) is a proposal only. | Recorded here; interface-contracts.md §2A. Route: API Governance. |

## 7. Traceability sources

- c3-components/CNT-ACC-ORDERS/
- supporting-views/interface-contracts.md §2

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
