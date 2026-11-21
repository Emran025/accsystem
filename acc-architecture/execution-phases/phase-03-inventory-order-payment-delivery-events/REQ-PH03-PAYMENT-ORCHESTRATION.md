# REQ-PH03-PAYMENT-ORCHESTRATION — Payment allocation, authorization and capture

**Document ID:** REQ-PH03-PAYMENT-ORCHESTRATION  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-PAYMENT-ORCHESTRATION |
| Phase ID | PH-03 |
| Title | Payment allocation, authorization and capture |
| Statement | Payment is requested only after all required reservations are accepted, per SellerOrder allocation, under the seller/agreement capture policy, without storing card data and with UNKNOWN outcomes preserved. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-ORDERS, CNT-ACC-PAYMENT |
| Related function/use case | FN-PAY-AUTHORIZE |
| Status | DRAFT |
| Evidence | FN-PAY-AUTHORIZE; FR-002 steps 6-7, 10; FR-009; ADR-007; ADR-016; CMP-PAY-ORCHESTRATOR; CON-004; NFR-006 |

## 2. Scope boundary and phase handoffs

- Provider capabilities and settlement policy are external gates; the unsupported path is blocked, not assumed.
- Alternatives preserved: aggregate vs separate attempts; authorize-then-capture vs approved immediate capture; manual/external payment.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-PAY-001 | REQ-PH03-PAYMENT-ORCHESTRATION | No payment authorization or capture is requested until every required seller reservation is definitively ACCEPTED. | Checkout reaches the payment step. | Payment begins only with all holds accepted. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-PAYMENT | AC-PH03-PAY-001-01 | TEST (planned): payment gating test | DRAFT | ADR-018-GATE |
| SREQ-PH03-PAY-002 | REQ-PH03-PAYMENT-ORCHESTRATION | Each SellerOrder has a payment allocation with seller, amount, currency, tax/delivery basis, policy snapshot, correlation and idempotency key. | Payment starts. | One allocation per SellerOrder. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-ORDERS | AC-PH03-PAY-002-01 | TEST (planned): allocation test | DRAFT | ADR-016-GATE, ASSUM-003 |
| SREQ-PH03-PAY-003 | REQ-PH03-PAYMENT-ORCHESTRATION | The policy resolver selects authorize-then-capture or immediate capture per seller/agreement, and incompatible policies in one transaction split into separate attempts or block checkout. | Allocations are created. | Each allocation follows one approved mode. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PAY-003-01 | TEST (planned): mixed policy test | DRAFT | ODEC-005, ADR-016-GATE, ADR-017-GATE |
| SREQ-PH03-PAY-004 | REQ-PH03-PAYMENT-ORCHESTRATION | AUTHORIZED means a hold, CAPTURED means collection, and neither alone means seller credit or settlement. | A payment state is recorded. | States remain distinct. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PAY-004-01 | TEST (planned): state model test | DRAFT | none recorded |
| SREQ-PH03-PAY-005 | REQ-PH03-PAYMENT-ORCHESTRATION | A timeout or lost response records AUTHORIZATION_UNKNOWN or CAPTURE_UNKNOWN and no duplicate financial effect or release occurs. | Provider response is missing. | UNKNOWN is held until reconciled. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-ORDERS | AC-PH03-PAY-005-01 | TEST (planned): payment unknown test (acceptance-test-plan.md item 4) | DRAFT | ADR-022-GATE |
| SREQ-PH03-PAY-006 | REQ-PH03-PAYMENT-ORCHESTRATION | A capture failure after confirmation leaves the order confirmed with a visible payment exception handled by retry, reconciliation, void or refund policy. | Capture fails after confirmation. | Exception recorded; no silent completion. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT, CNT-ACC-ORDERS | AC-PH03-PAY-006-01 | TEST (planned): capture failure test (acceptance-test-plan.md item 5) | DRAFT | none recorded |
| SREQ-PH03-PAY-007 | REQ-PH03-PAYMENT-ORCHESTRATION | Raw card data (PAN, CVV, expiry) is never stored or transits ACCSystem stores; tokenization or hosted checkout is used. | A payment method is used. | Only provider tokens/references are held. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PAY-007-01 | TEST (planned): data classification scan | DRAFT | UNKN-002 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-PAY-001 | No payment before all holds accepted | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | FR-009 AC1 |
| SREQ-PH03-PAY-002 | Per-SellerOrder allocation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | FN-PAY-AUTHORIZE |
| SREQ-PH03-PAY-003 | Capture policy per seller | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | ODEC-005; ADR-016 |
| SREQ-PH03-PAY-004 | Distinct money states | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | FN-PAY-AUTHORIZE |
| SREQ-PH03-PAY-005 | Unknown payment outcome | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | FR-009 AC5 |
| SREQ-PH03-PAY-006 | Capture failure after confirmation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | FN-PAY-AUTHORIZE; FR-009 |
| SREQ-PH03-PAY-007 | No raw card data | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-PAY-AUTHORIZE | NFR-006; CON-004 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-PAY-001-01 | SREQ-PH03-PAY-001 | With any reservation UNKNOWN, REJECTED or EXPIRED no payment request is issued. | IF-ACC-RESERVE-SAGA §3.5 | FR-009 AC1; FR-002 AC1 | FR-009 AC1 |
| AC-PH03-PAY-002-01 | SREQ-PH03-PAY-002 | Allocation fields are present; one aggregate provider transaction is used only when policies are compatible and the provider supports it. | RGAP-PH03-003 | FN-PAY-AUTHORIZE; CMP-PAY-ORCHESTRATOR | FN-PAY-AUTHORIZE |
| AC-PH03-PAY-003-01 | SREQ-PH03-PAY-003 | A shared transaction never silently chooses one of conflicting policies. | RGAP-PH03-003 | FN-PAY-AUTHORIZE step 2 | ODEC-005; ADR-016 |
| AC-PH03-PAY-004-01 | SREQ-PH03-PAY-004 | Capture does not imply seller credit; states are separately recorded. | RGAP-PH03-003 | FN-PAY-AUTHORIZE step 3 | FN-PAY-AUTHORIZE |
| AC-PH03-PAY-005-01 | SREQ-PH03-PAY-005 | Retries use the same operation key and no second authorization or capture results. | RGAP-PH03-003 | FR-009 AC5; FN-PAY-AUTHORIZE step 4 | FR-009 AC5 |
| AC-PH03-PAY-006-01 | SREQ-PH03-PAY-006 | The order is not rolled back and the exception is visible. | RGAP-PH03-003 | FN-PAY-AUTHORIZE step 5 | FN-PAY-AUTHORIZE; FR-009 |
| AC-PH03-PAY-007-01 | SREQ-PH03-PAY-007 | A data scan finds no raw card data. | RGAP-PH03-003 | NFR-006; CON-004 | NFR-006; CON-004 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Provider timeout never proves failure; circuit-open after possible dispatch is UNKNOWN unless no dispatch is evidenced.
- Which provider is used is open (ASSUM-003).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-018-GATE | ADR-018 reservation TTL values and async-callback mode require per-institution approval. | SREQ-PH03-PAY-001 |
| ADR-016-GATE | ADR-016 provider capabilities, commission/settlement policy, manual-payment approval flow are owner/finance/legal gates. | SREQ-PH03-PAY-002, SREQ-PH03-PAY-003 |
| ASSUM-003 | Single payment provider at MVP (to confirm at Phase 3 start). | SREQ-PH03-PAY-002 |
| ODEC-005 | Payment capture timing (authorize-then-capture vs immediate/contract-defined). | SREQ-PH03-PAY-003 |
| ADR-017-GATE | ADR-017 policy values (capture timing, tax, accounting trigger, retention, SLA, support access, license plans) need owner ratification. | SREQ-PH03-PAY-003 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH03-PAY-005 |
| UNKN-002 | Compliance/data-residency/retention framework (PCI-DSS, privacy, audit retention) not defined. | SREQ-PH03-PAY-007 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-003 | Payment operations (authorize, capture, void, refund) are internal adapter/orchestrator commands in CMP-PAY-ADAPTER; no registered IF-* covers them; the webhook interface is provider-defined (IC-003). | Recorded here; route: provider selection and API Governance. |

## 7. Traceability sources

- functions/specs/FN-PAY-AUTHORIZE.md
- c3-components/CNT-ACC-PAYMENT/CMP-PAY-ORCHESTRATOR.md
- decisions/ADR-016.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
