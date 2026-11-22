# REQ-PH02-SELLER-RESERVATION — Seller-scoped inventory reservation

**Document ID:** REQ-PH02-SELLER-RESERVATION  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-SELLER-RESERVATION |
| Phase ID | PH-02 |
| Title | Seller-scoped inventory reservation |
| Statement | Each seller's ACCore decides a reservation request atomically and reports a definitive ACCEPTED or REJECTED outcome or an honest UNKNOWN, with ACCore remaining the inventory source of truth. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-CART, CNT-ACC-INTEGRATION, CNT-ACC-ORDERS, CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY |
| Related function/use case | FN-ORD-RESERVE |
| Status | DRAFT |
| Evidence | FN-ORD-RESERVE; FR-002 step 3-5; FR-009; ADR-006; ADR-018; CMP-INT-RESERVATION; CMP-CON-RESERVATION |

## 2. Scope boundary and phase handoffs

- Stock commit after OrderConfirmed is PH-03. Release after payment failure is PH-03.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-RSV-001 | REQ-PH02-SELLER-RESERVATION | Checkout issues one reservation request per distinct seller with a stable scoped idempotency key persisted before dispatch. | Checkout reaches reservation. | One request per seller. | SYS-ACCSYSTEM | CNT-ACC-CART, CNT-ACC-INTEGRATION, CNT-ACC-ORDERS | AC-PH02-RSV-001-01 | TEST (planned): per-seller request test | DRAFT | RP-03 |
| SREQ-PH02-RSV-002 | REQ-PH02-SELLER-RESERVATION | ACCore checks stock and creates the reservation in one local atomic transaction so concurrent last-unit requests yield at most one accepted hold. | ACCore receives a reservation request. | ACCEPTED or REJECTED recorded. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY | AC-PH02-RSV-002-01 | TEST (planned): last-unit race test | DRAFT | ADR-006-GATE |
| SREQ-PH02-RSV-003 | REQ-PH02-SELLER-RESERVATION | An ACCEPTED outcome carries the reservation reference, confirmed price and quantity and the expiry policy reference. | Stock suffices. | Accepted response. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY | AC-PH02-RSV-003-01 | TEST (planned): contract test | DRAFT | IC-005, IC-006 |
| SREQ-PH02-RSV-004 | REQ-PH02-SELLER-RESERVATION | Insufficient stock, changed price or inactive seller yields a definitive REJECTED outcome with a reason and no hold. | Stock or price check fails. | Rejected response. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY | AC-PH02-RSV-004-01 | TEST (planned): rejection test | DRAFT | none recorded |
| SREQ-PH02-RSV-005 | REQ-PH02-SELLER-RESERVATION | A duplicate request with the same key returns the original result without a second hold. | Request replayed. | Original result. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-INVENTORY | AC-PH02-RSV-005-01 | TEST (planned): duplicate test | DRAFT | ADR-022-GATE |
| SREQ-PH02-RSV-006 | REQ-PH02-SELLER-RESERVATION | The reservation boundary exposes an aggregate result: all required reservations ACCEPTED, any definitive failure, or any UNKNOWN, and UNKNOWN blocks progression beyond the boundary. | All seller outcomes are collected. | One aggregate outcome. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-INTEGRATION | AC-PH02-RSV-006-01 | TEST (planned): multi-seller outcome test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-RSV-001 | Seller-scoped request identity | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-RESERVE | FN-ORD-RESERVE |
| SREQ-PH02-RSV-002 | Atomic ACCore reservation | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-RESERVE | FN-ORD-RESERVE |
| SREQ-PH02-RSV-003 | Accepted outcome content | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-RESERVE | FN-ORD-RESERVE |
| SREQ-PH02-RSV-004 | Rejected outcome | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-RESERVE | FR-002 A1; FN-ORD-RESERVE |
| SREQ-PH02-RSV-005 | Duplicate request | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-RESERVE | FN-ORD-RESERVE |
| SREQ-PH02-RSV-006 | Aggregate outcome at the boundary | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | FN-ORD-RESERVE | FN-ORD-CHECKOUT step 4 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-RSV-001-01 | SREQ-PH02-RSV-001 | Each seller has exactly one request with a stable key. | IF-ACC-RESERVE-SAGA §3.4 | FN-ORD-RESERVE | FN-ORD-RESERVE |
| AC-PH02-RSV-002-01 | SREQ-PH02-RSV-002 | Two concurrent requests for the last unit yield at most one ACCEPTED. | IF-ACC-RESERVE-SAGA §3.4 | FN-ORD-RESERVE tests; acceptance item 2 | FN-ORD-RESERVE |
| AC-PH02-RSV-003-01 | SREQ-PH02-RSV-003 | Response includes reservation id, confirmed price/quantity and expiry. | IF-ACR-RESERVATION-RESP §9.4 | FN-ORD-RESERVE | FN-ORD-RESERVE |
| AC-PH02-RSV-004-01 | SREQ-PH02-RSV-004 | REJECTED carries a reason code and creates no hold. | IF-ACC-RESERVE-SAGA §3.4 | FR-002 A1 | FR-002 A1; FN-ORD-RESERVE |
| AC-PH02-RSV-005-01 | SREQ-PH02-RSV-005 | No second hold is created. | IF-ACC-RESERVE-SAGA §3.7 | FN-ORD-RESERVE | FN-ORD-RESERVE |
| AC-PH02-RSV-006-01 | SREQ-PH02-RSV-006 | Progression beyond the boundary requires every required reservation ACCEPTED. | IF-ACC-RESERVE-SAGA §3.5 | FN-ORD-CHECKOUT step 4; FR-009 AC1 | FN-ORD-CHECKOUT step 4 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Reservation TTL is configurable and authoritative at ACCore; request value is a hint (IC-005).
- Delivery mode sync by default; callback per institution approval (IC-006).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| RP-03 | Reservation response vocabulary and delivery-mode contract gate open. | SREQ-PH02-RSV-001 |
| ADR-006-GATE | ADR-006 reservation hold TTL unknown (policy:reservation.hold_ttl_seconds, ADR-022). | SREQ-PH02-RSV-002 |
| IC-005 | Reservation TTL not defined; request value is a hint only (partially resolved by ADR-018). | SREQ-PH02-RSV-003 |
| IC-006 | Reservation response delivery mode (sync vs async callback) not confirmed (partially resolved by ADR-018). | SREQ-PH02-RSV-003 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH02-RSV-005 |

## 7. Traceability sources

- functions/specs/FN-ORD-RESERVE.md
- c3-components/CNT-ACC-INTEGRATION/CMP-INT-RESERVATION.md
- c3-components/CNT-ACR-CONNECTOR/CMP-CON-RESERVATION.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
