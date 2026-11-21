# REQ-PH03-CANCELLATION-COORDINATION — Cancellation and return coordination

**Document ID:** REQ-PH03-CANCELLATION-COORDINATION  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-CANCELLATION-COORDINATION |
| Phase ID | PH-03 |
| Title | Cancellation and return coordination |
| Statement | Cancellation of an order coordinates payment reversal and stock/reservation release for each SellerOrder with independent partial outcomes, and an order becomes Cancelled only when all required downstream compensation is settled. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-ORDERS, CNT-ACC-PAYMENT, CNT-ACC-INTEGRATION, CNT-ACC-NOTIFICATIONS |
| Related function/use case | TBD (RGAP-PH03-001) |
| Status | DRAFT |
| Evidence | FR-008; CMP-ORD-CANCEL; ADR-016; ADR-018; acceptance-test-plan.md items 5-6 |

## 2. Scope boundary and phase handoffs

- Return and dispute handling (ODEC-007) is deferred; only the coordination boundary documented in the sources is stated.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-CNC-001 | REQ-PH03-CANCELLATION-COORDINATION | An authorized actor may request cancellation of an eligible order, and ineligible requests are rejected with the order unchanged. | A cancellation is requested. | Accepted for processing or rejected. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-CNC-001-01 | TEST (planned): eligibility test | DRAFT | ODEC-007 |
| SREQ-PH03-CNC-002 | REQ-PH03-CANCELLATION-COORDINATION | Cancellation per SellerOrder determines release, void or refund from authoritative payment and reservation state, and does not infer state from absence of a response. | Cancellation is accepted. | Each SellerOrder gets its correct compensation. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-PAYMENT, CNT-ACC-INTEGRATION | AC-PH03-CNC-002-01 | TEST (planned): cancellation matrix test (acceptance-test-plan.md item 5) | DRAFT | ADR-018-GATE |
| SREQ-PH03-CNC-003 | REQ-PH03-CANCELLATION-COORDINATION | Compensation outcomes are tracked per SellerOrder and a partial result is explicit rather than reported as full cancellation. | Some SellerOrders cancel and others fail. | Partial status visible. | SYS-ACCSYSTEM | CNT-ACC-ORDERS | AC-PH03-CNC-003-01 | TEST (planned): partial cancellation test | DRAFT | ODEC-007 |
| SREQ-PH03-CNC-004 | REQ-PH03-CANCELLATION-COORDINATION | Cancellation events are emitted to affected institutions with only authorized data, and delivery halts or coordinates per delivery mode. | Cancellation completes or fails. | Affected parties are notified. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-INTEGRATION, CNT-ACC-NOTIFICATIONS | AC-PH03-CNC-004-01 | TEST (planned): event handoff test | OWNER_REVIEW | ODEC-007 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-CNC-001 | Eligible cancellation requests | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | FR-008 |
| SREQ-PH03-CNC-002 | Per-SellerOrder compensation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | FR-008; CMP-ORD-CANCEL |
| SREQ-PH03-CNC-003 | Independent partial outcomes | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | CMP-ORD-CANCEL |
| SREQ-PH03-CNC-004 | Cancellation notification and handoff | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-001) | FR-008; CMP-ORD-CANCEL §4 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-CNC-001-01 | SREQ-PH03-CNC-001 | An ineligible state (e.g. already delivered) is rejected and the order is unchanged. | RGAP-PH03-005 | FR-008 A1 | FR-008 |
| AC-PH03-CNC-002-01 | SREQ-PH03-CNC-002 | Hold-only paths release/void; captured paths refund; UNKNOWN is reconciled first. | RGAP-PH03-005 | CMP-ORD-CANCEL §3; FR-008 | FR-008; CMP-ORD-CANCEL |
| AC-PH03-CNC-003-01 | SREQ-PH03-CNC-003 | Cancelled is set only after all required compensation succeeds; otherwise a pending/failed compensation state remains. | RGAP-PH03-005 | CMP-ORD-CANCEL §3 | CMP-ORD-CANCEL |
| AC-PH03-CNC-004-01 | SREQ-PH03-CNC-004 | OrderCancelled is delivered at least once with recipient-scoped content; schema is not asserted. | RGAP-PH03-005 | CMP-ORD-CANCEL §4 | FR-008; CMP-ORD-CANCEL §4 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Stock restoration after commit needs institutional and product approval; no implicit restoration is specified.
- Return flows are deferred.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ODEC-007 | Returns and disputes capability (deferred; design pending). | SREQ-PH03-CNC-001, SREQ-PH03-CNC-003, SREQ-PH03-CNC-004 |
| ADR-018-GATE | ADR-018 reservation TTL values and async-callback mode require per-institution approval. | SREQ-PH03-CNC-002 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-001 | functions/function-catalog.md has no FN-* for cancellation, return coordination, refund/void, payment reconciliation, stock commit, ledger/settlement or external delivery events. | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH03-005 | OrderCancelled, ReturnRequested and OrderReturned schemas, consumers and delivery channel are not defined; ReturnRequested timing is inconsistent in sources. | Recorded here; CMP-ORD-CANCEL §4. Route: event-contract owners. |

## 7. Traceability sources

- c3-components/CNT-ACC-ORDERS/CMP-ORD-CANCEL.md
- 01-scope/scope-and-requirements.md FR-008

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
