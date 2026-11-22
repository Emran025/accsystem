# REQ-PH02-PRODUCT-DISCOVERY — Browsing, search and product detail for buyer channels

**Document ID:** REQ-PH02-PRODUCT-DISCOVERY  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-PRODUCT-DISCOVERY |
| Phase ID | PH-02 |
| Title | Browsing, search and product detail for buyer channels |
| Statement | Buyers on the individual (ACCommerce) and institution (ACCore Commerce Workspace) channels can browse, search and view product details from the marketplace projection. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-CATALOG, CNT-ACC-APIGATEWAY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE, CNT-ACC-SEARCH, CNT-ACC-IDENTITY |
| Related function/use case | TBD (RGAP-PH02-001) |
| Status | DRAFT |
| Evidence | IF-ACC-CATALOG-QUERY; ADR-003; ADR-004; CNT-ACC-SEARCH; scope §8 step 2 |

## 2. Scope boundary and phase handoffs

- Recommendations and personalization are PH-05 and are not specified.
- Anonymous browsing permission is an open security decision (IC-007).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-DSC-001 | REQ-PH02-PRODUCT-DISCOVERY | Authorized buyers can query listings by text, seller and category and retrieve a listing detail by identifier. | A buyer submits a query or detail request. | Matching marketplace projections are returned. | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE | CNT-ACC-CATALOG, CNT-ACC-APIGATEWAY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE | AC-PH02-DSC-001-01, AC-PH02-DSC-001-02 | TEST (planned): query contract test | DRAFT | IC-007, IC-002 |
| SREQ-PH02-DSC-002 | REQ-PH02-PRODUCT-DISCOVERY | Search serves results from a derived index independent of payment or delivery availability. | A buyer submits a text search. | Results come from the index. | SYS-ACCSYSTEM | CNT-ACC-SEARCH, CNT-ACC-CATALOG | AC-PH02-DSC-002-01 | TEST (planned): search independence test | DRAFT | none recorded |
| SREQ-PH02-DSC-003 | REQ-PH02-PRODUCT-DISCOVERY | Both buyer channels use the same marketplace query capability with actor type enforced by identity. | Either channel queries the catalog. | Same results contract. | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE | CNT-ACC-APIGATEWAY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE, CNT-ACC-IDENTITY | AC-PH02-DSC-003-01 | REVIEW (planned): channel parity review | DRAFT | none recorded |
| SREQ-PH02-DSC-004 | REQ-PH02-PRODUCT-DISCOVERY | Institution-scoped responses enforce the institution from the token. | An institution-scoped query is made. | Only permitted data is returned. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-IDENTITY | AC-PH02-DSC-004-01 | TEST (planned): scoped query test | DRAFT | none recorded |
| SREQ-PH02-DSC-005 | REQ-PH02-PRODUCT-DISCOVERY | Listing fields can carry multiple languages with provenance-preserving translation. | A listing carries more than one language. | Fields are presented per locale. | SYS-ACCSYSTEM | CNT-ACC-CATALOG, CNT-ACC-SEARCH | AC-PH02-DSC-005-01 | REVIEW (planned): locale/content review | OWNER_REVIEW | PUB-004 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-DSC-001 | Catalog query | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | IF-ACC-CATALOG-QUERY |
| SREQ-PH02-DSC-002 | Indexed search | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | CNT-ACC-SEARCH §6; idea §10.3 |
| SREQ-PH02-DSC-003 | Shared commerce core for both channels | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | ADR-003 |
| SREQ-PH02-DSC-004 | Tenant-scoped responses | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | IF-ACC-CATALOG-QUERY §1.8 |
| SREQ-PH02-DSC-005 | Multilingual listing fields | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH02-001) | scope §8 step 2; topic 23 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-DSC-001-01 | SREQ-PH02-DSC-001 | Queries return projection fields only, never product master data. | IF-ACC-CATALOG-QUERY §1.4 | ADR-004 | IF-ACC-CATALOG-QUERY |
| AC-PH02-DSC-001-02 | SREQ-PH02-DSC-001 | Unknown listing returns 404; rate limiting returns 429. | IF-ACC-CATALOG-QUERY §1.5 | IF-ACC-CATALOG-QUERY §1.5 | IF-ACC-CATALOG-QUERY |
| AC-PH02-DSC-002-01 | SREQ-PH02-DSC-002 | Search remains available when payment or delivery services are down. | NOT SPECIFIED (source reference gap: RGAP-PH02-006) | CNT-ACC-SEARCH §6 | CNT-ACC-SEARCH §6; idea §10.3 |
| AC-PH02-DSC-003-01 | SREQ-PH02-DSC-003 | Channels differ by authorization, not by catalog logic. | IF-ACC-CATALOG-QUERY §1.2 | ADR-003 | ADR-003 |
| AC-PH02-DSC-004-01 | SREQ-PH02-DSC-004 | Cross-institution reads outside query policy are denied. | IF-ACC-CATALOG-QUERY §1.8 | NFR-004 | IF-ACC-CATALOG-QUERY §1.8 |
| AC-PH02-DSC-005-01 | SREQ-PH02-DSC-005 | Locale-specific fields are stored and returned without altering the source text. | NOT SPECIFIED (source reference gap: RGAP-PH02-001) | traceability-24-topics.md topic 23 | scope §8 step 2; topic 23 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Search index unavailable: direct catalog browse fallback is a PROPOSAL (CNT-ACC-SEARCH §6).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| IC-007 | Whether anonymous catalog browsing is permitted is not specified. | SREQ-PH02-DSC-001 |
| IC-002 | Exact field names/types require formal OpenAPI/AsyncAPI specification. | SREQ-PH02-DSC-001 |
| PUB-004 | Which listing fields are permitted for publication is not defined. | SREQ-PH02-DSC-005 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH02-001 | functions/function-catalog.md has no FN-* for browsing, search, offer presentation or cart preparation (only FN-INT-PUBLISH, FN-ORD-CHECKOUT, FN-ORD-RESERVE exist). | Recorded in registry column use_case_id as TBD; route: function inventory step (execution-phases/README.md §8). |
| RGAP-PH02-006 | The search API (GET /v1/catalog/products) is not a registered IF-*; relation to IF-ACC-CATALOG-QUERY is an OPEN separate spec (interface-contracts.md §1.9). | Recorded here; route: API Governance. |

## 7. Traceability sources

- supporting-views/interface-contracts.md §1
- c2-containers/accsystem/CNT-ACC-SEARCH.md, CNT-ACC-CATALOG.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
