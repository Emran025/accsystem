# REQ-PH02-CHECKOUT-PREPARATION — Cart and checkout preparation up to the reservation boundary

**Document ID:** REQ-PH02-CHECKOUT-PREPARATION  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-CHECKOUT-PREPARATION |
| Phase ID | PH-02 |
| Title | Cart and checkout preparation up to the reservation boundary |
| Statement | Buyers can build a buyer-scoped multi-seller cart and start an idempotent checkout that is validated and grouped by seller, stopping at the reservation boundary without any payment step. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-CART, CNT-ACC-OFFER, CNT-ACC-IDENTITY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE |
| Related function/use case | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) |
| Status | DRAFT |
| Evidence | FR-002 steps 1-3; FR-003; FN-ORD-CHECKOUT steps 1-4; ADR-016; CNT-ACC-CART |

## 2. Scope boundary and phase handoffs

- Payment, confirmation and order lifecycle are PH-03. Order-record placement is owner gate RGAP-PH02-004.
- ACCommerce monetization (UNKN-007, LIC-006) is open; ACCommerce is reportedly free initially.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-CHK-001 | REQ-PH02-CHECKOUT-PREPARATION | A cart is temporary, editable and accessible only to its authenticated buyer. | A buyer adds or edits cart items. | Cart reflects items and current offer data. | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE | CNT-ACC-CART, CNT-ACC-OFFER, CNT-ACC-IDENTITY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE | AC-PH02-CHK-001-01, AC-PH02-CHK-001-02 | TEST (planned): cart scope test | DRAFT | UNKN-007 |
| SREQ-PH02-CHK-002 | REQ-PH02-CHECKOUT-PREPARATION | A multi-seller cart is grouped by seller with no cross-seller line mixing. | Checkout starts on a cart with several sellers. | One group per seller. | SYS-ACCSYSTEM | CNT-ACC-CART | AC-PH02-CHK-002-01 | TEST (planned): grouping test | DRAFT | ODEC-003 |
| SREQ-PH02-CHK-003 | REQ-PH02-CHECKOUT-PREPARATION | Checkout validates buyer eligibility, availability snapshot, price snapshot and delivery details and records the applicable policy versions. | Buyer initiates checkout. | A validated checkout session exists. | SYS-ACCSYSTEM | CNT-ACC-CART, CNT-ACC-OFFER | AC-PH02-CHK-003-01, AC-PH02-CHK-003-02 | TEST (planned): validation test | DRAFT | UNKN-006, ODEC-009, ODEC-003 |
| SREQ-PH02-CHK-004 | REQ-PH02-CHECKOUT-PREPARATION | Repeating a checkout with the same checkout_session_id produces no duplicate checkout effect. | Checkout is retried. | One effect. | SYS-ACCSYSTEM | CNT-ACC-CART | AC-PH02-CHK-004-01 | TEST (planned): duplicate checkout test | DRAFT | ADR-022-GATE |
| SREQ-PH02-CHK-005 | REQ-PH02-CHECKOUT-PREPARATION | Checkout in this phase proceeds only to the seller-scoped reservation request and does not request payment authorization. | Reservations are requested. | No payment step is started. | SYS-ACCSYSTEM | CNT-ACC-CART | AC-PH02-CHK-005-01 | REVIEW (planned): boundary review | OWNER_REVIEW | ODEC-003 |
| SREQ-PH02-CHK-006 | REQ-PH02-CHECKOUT-PREPARATION | An institution employee can start the same checkout from the ACCore Commerce Workspace. | Employee initiates checkout in the workspace. | Same checkout preparation applies. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-COMMERCE, CNT-ACC-CART | AC-PH02-CHK-006-01 | TEST (planned): workspace test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-CHK-001 | Buyer-scoped cart | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) | CNT-ACC-CART |
| SREQ-PH02-CHK-002 | Seller grouping | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) | ADR-016; ODEC-003 |
| SREQ-PH02-CHK-003 | Checkout validation and snapshots | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) | FR-002; FN-ORD-CHECKOUT |
| SREQ-PH02-CHK-004 | Idempotent checkout session | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) | FR-002 AC2 |
| SREQ-PH02-CHK-005 | Stop at reservation boundary | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) | execution-phases/README.md §4 |
| SREQ-PH02-CHK-006 | Institution (B2B) checkout initiation | ACT-INST-EMPLOYEE | FN-ORD-CHECKOUT (steps 1-3 only; RGAP-PH02-003) | FR-003 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-CHK-001-01 | SREQ-PH02-CHK-001 | No cross-buyer cart access is possible. | RGAP-PH02-003 | CNT-ACC-CART §7 | CNT-ACC-CART |
| AC-PH02-CHK-001-02 | SREQ-PH02-CHK-001 | Cart price comes from Offer. | RGAP-PH02-003 | CNT-ACC-CART §7 | CNT-ACC-CART |
| AC-PH02-CHK-002-01 | SREQ-PH02-CHK-002 | N sellers yield N groups; one seller yields one. | RGAP-PH02-003 | CMP-ORD-MULTISELLER tests; ADR-016 | ADR-016; ODEC-003 |
| AC-PH02-CHK-003-01 | SREQ-PH02-CHK-003 | Invalid or changed price/quantity stops checkout with refreshed data. | RGAP-PH02-003 | FR-002 steps 2; IF-ACC-ORDER-CREATE §2.5 | FR-002; FN-ORD-CHECKOUT |
| AC-PH02-CHK-003-02 | SREQ-PH02-CHK-003 | Tax, currency and delivery snapshot content depends on the open model. | RGAP-PH02-009 | FN-ORD-CHECKOUT step 1 | FR-002; FN-ORD-CHECKOUT |
| AC-PH02-CHK-004-01 | SREQ-PH02-CHK-004 | Duplicate checkout with the same key yields no duplicate. | RGAP-PH02-003 | FR-002 AC2; function-catalog idempotency | FR-002 AC2 |
| AC-PH02-CHK-005-01 | SREQ-PH02-CHK-005 | No payment request is issued from the PH-02 flow. | RGAP-PH02-004 | execution-phases/README.md §4 | execution-phases/README.md §4 |
| AC-PH02-CHK-006-01 | SREQ-PH02-CHK-006 | Workspace and ACCommerce use one checkout capability. | RGAP-PH02-003 | FR-003; ADR-003 | FR-003 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Offer validation fails: checkout blocked and updated price shown.
- Session TTL is UNKNOWN.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-007 | ACCommerce individual-user monetization/entitlement model not defined. | SREQ-PH02-CHK-001 |
| ODEC-003 | Multi-seller cart model (ParentOrder + SellerOrders); MVP direction recorded in ADR-016. | SREQ-PH02-CHK-002, SREQ-PH02-CHK-003, SREQ-PH02-CHK-005 |
| UNKN-006 | Multi-currency and tax/VAT model not defined. | SREQ-PH02-CHK-003 |
| ODEC-009 | Multi-currency and tax model/jurisdiction rules. | SREQ-PH02-CHK-003 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH02-CHK-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-003 | Cart and checkout-session endpoints (POST /v1/carts, /v1/checkouts) are reference examples only; no registered IF-* covers them. | Recorded here; CNT-ACC-CART §5. Route: API Governance (IC-002). |
| RGAP-PH02-009 | Tax-line, currency and delivery-term snapshot content for checkout is undefined pending the tax/currency model. | Recorded here; UNKN-006/ODEC-009 owner gate. |
| RGAP-PH02-004 | Placement boundary of ParentOrder/SellerOrder record creation: PH-02 requires seller-scoped reservation requests while PH-03 lists ParentOrder/SellerOrder records; FN-ORD-CHECKOUT persists them before reservation. | Owner gate recorded here and in REQ-PH03-ORDER-AGGREGATE. This draft places only the seller-scoped reservation subject identity in PH-02 and the order aggregate lifecycle in PH-03. |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-002, FR-003
- functions/specs/FN-ORD-CHECKOUT.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
