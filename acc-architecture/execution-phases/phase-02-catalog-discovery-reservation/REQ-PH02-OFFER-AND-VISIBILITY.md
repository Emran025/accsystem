# REQ-PH02-OFFER-AND-VISIBILITY — Indicative price/availability and visibility states

**Document ID:** REQ-PH02-OFFER-AND-VISIBILITY  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-OFFER-AND-VISIBILITY |
| Phase ID | PH-02 |
| Title | Indicative price/availability and visibility states |
| Statement | Marketplace price and availability are shown as indicative timestamped snapshots, and stale, unavailable or disconnected states are hidden or labeled so unavailable institutions are not purchasable. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-OFFER, CNT-ACC-CATALOG, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR, CNT-ACC-SEARCH, CNT-ACC-CART |
| Related function/use case | TBD (RGAP-PH02-001) |
| Status | DRAFT |
| Evidence | FR-011; ODEC-002; ADR-004; CNT-ACC-OFFER; deployment-view §2; acceptance-test-plan.md item 7 |

## 2. Scope boundary and phase handoffs

- Authoritative stock and stock commitment are in PH-03; this document covers the indicative projection only.
- Service windows (RGAP-PH02-005) have no source definition and are not specified.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-OFR-001 | REQ-PH02-OFFER-AND-VISIBILITY | Displayed price and availability are indicative snapshots carrying a last-updated timestamp. | A listing is displayed. | Snapshot and timestamp shown. | SYS-ACCSYSTEM | CNT-ACC-OFFER, CNT-ACC-CATALOG | AC-PH02-OFR-001-01 | TEST (planned): snapshot test | DRAFT | ADR-004-GATE |
| SREQ-PH02-OFR-002 | REQ-PH02-OFFER-AND-VISIBILITY | A StockAvailabilityChanged signal updates the indicative snapshot. | ACCore emits a stock availability change. | Snapshot updated with timestamp. | SYS-ACCSYSTEM, SYS-ACCORE | CNT-ACC-OFFER, CNT-ACC-INTEGRATION, CNT-ACR-CONNECTOR | AC-PH02-OFR-002-01 | TEST (planned): signal test | DRAFT | IC-002 |
| SREQ-PH02-OFR-003 | REQ-PH02-OFFER-AND-VISIBILITY | A stale snapshot or a disconnected institution is hidden or marked unavailable. | Snapshot exceeds staleness policy or connectivity is unavailable. | Listing is hidden or unavailable. | SYS-ACCSYSTEM | CNT-ACC-OFFER, CNT-ACC-SEARCH, CNT-ACC-INTEGRATION | AC-PH02-OFR-003-01, AC-PH02-OFR-003-02 | TEST (planned): connectivity visibility test (acceptance-test-plan.md item 7) | DRAFT | ADR-004-GATE, ADR-022-GATE |
| SREQ-PH02-OFR-004 | REQ-PH02-OFFER-AND-VISIBILITY | Prices shown and used come from Offer, and client-submitted prices are rejected. | A client submits or reads a price. | Only service price is used. | SYS-ACCSYSTEM | CNT-ACC-OFFER, CNT-ACC-CART | AC-PH02-OFR-004-01 | TEST (planned): price tampering test | DRAFT | none recorded |
| SREQ-PH02-OFR-005 | REQ-PH02-OFFER-AND-VISIBILITY | Displayed availability never constitutes a reservation, and checkout must revalidate price and quantity at ACCore. | Buyer proceeds from display to checkout. | Authoritative check occurs at reservation. | SYS-ACCSYSTEM | CNT-ACC-OFFER, CNT-ACC-CART | AC-PH02-OFR-005-01 | REVIEW (planned): flow review | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-OFR-001 | Indicative snapshot with timestamp | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | FR-011; ODEC-002 |
| SREQ-PH02-OFR-002 | Stock signal intake | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | FR-011 |
| SREQ-PH02-OFR-003 | Stale or disconnected hidden or labeled | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | FR-011 AC3; topics 10 |
| SREQ-PH02-OFR-004 | Price from service not client | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | CNT-ACC-OFFER §7 |
| SREQ-PH02-OFR-005 | Revalidation requirement stated | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | FR-011 AC2; ODEC-002 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-OFR-001-01 | SREQ-PH02-OFR-001 | Availability and price always carry last-updated time and are not authoritative. | IF-ACC-CATALOG-QUERY §1.4 | FR-011 AC1 | FR-011; ODEC-002 |
| AC-PH02-OFR-002-01 | SREQ-PH02-OFR-002 | The snapshot reflects the latest signal and its time. | IF-ACC-EVENT-ENVELOPE §5.5 | FR-011 normal path | FR-011 |
| AC-PH02-OFR-003-01 | SREQ-PH02-OFR-003 | Listings of a CONNECTIVITY_UNAVAILABLE institution are removed from search/promotion or marked unavailable. | RGAP-PH02-002 | deployment-view §2; FR-011 AC3 | FR-011 AC3; topics 10 |
| AC-PH02-OFR-003-02 | SREQ-PH02-OFR-003 | Staleness limit is a policy value; none asserted. | RGAP-PH02-002 | ADR-022 | FR-011 AC3; topics 10 |
| AC-PH02-OFR-004-01 | SREQ-PH02-OFR-004 | A client-supplied price is rejected. | RGAP-PH02-002 | CNT-ACC-OFFER §7 | CNT-ACC-OFFER §7 |
| AC-PH02-OFR-005-01 | SREQ-PH02-OFR-005 | Checkout proceeds only through the ACCore reservation, not on the snapshot. | IF-ACC-RESERVE-SAGA §3.3 | FR-011 AC2 | FR-011 AC2; ODEC-002 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Offer service unavailable: checkout is blocked rather than using a stale price (CNT-ACC-OFFER §6).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-004-GATE | ADR-004 price/stock freshness policy unknown; snapshot staleness window unspecified. | SREQ-PH02-OFR-001, SREQ-PH02-OFR-003 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH02-OFR-002 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH02-OFR-003 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-001 | functions/function-catalog.md has no FN-* for browsing, search, offer presentation or cart preparation (only FN-INT-PUBLISH, FN-ORD-CHECKOUT, FN-ORD-RESERVE exist). | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH02-002 | No registered IF-* for the offer/price/availability query API (CNT-ACC-OFFER §5) or for institution-facing stock-signal intake beyond the named StockAvailabilityChanged event (§5.5, shape ASSUMPTION). | Recorded here; route: API Governance (IC-002). |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-011
- c2-containers/accsystem/CNT-ACC-OFFER.md
- supporting-views/deployment-view.md §2

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
