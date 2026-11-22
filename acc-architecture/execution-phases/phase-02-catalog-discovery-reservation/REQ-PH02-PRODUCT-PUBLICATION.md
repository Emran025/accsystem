# REQ-PH02-PRODUCT-PUBLICATION — Product projection preparation and submission at ACCore

**Document ID:** REQ-PH02-PRODUCT-PUBLICATION  
**Phase:** PH-02 — Catalog, Discovery and Reservation  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH02-PRODUCT-PUBLICATION |
| Phase ID | PH-02 |
| Title | Product projection preparation and submission at ACCore |
| Statement | An institution can select publishable fields of a product from its Product Master and submit a versioned projection to ACCSystem reliably, with the source of truth remaining in ACCore. |
| Actors | ACT-INST-EMPLOYEE |
| Locations | SYS-ACCORE |
| Primary C4 containers | CNT-ACR-PRODUCTMASTER, CNT-ACR-OUTBOX, CNT-ACR-CONNECTOR |
| Related function/use case | FN-INT-PUBLISH |
| Status | DRAFT |
| Evidence | FR-001; FR-010; FN-INT-PUBLISH §4 steps 1-3; ADR-004; ADR-005; CNT-ACR-PRODUCTMASTER |

## 2. Scope boundary and phase handoffs

- In scope: ACCore-side preparation and submission. ACCSystem admission and listing handling are in REQ-PH02-LISTING-INGESTION.
- Authentication and Outbox/Inbox mechanics come from PH-01 (REQ-PH01-CORE-CONNECTIVITY, REQ-PH01-MESSAGE-RELIABILITY).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH02-PUB-001 | REQ-PH02-PRODUCT-PUBLICATION | An institution employee selects which Product Master fields are published, and the projection contains only fields authorized by the institution publish policy. | Employee requests Publish Listing. | A projection with only authorized fields is prepared. | SYS-ACCORE | CNT-ACR-PRODUCTMASTER | AC-PH02-PUB-001-01 | TEST (planned): field policy test | DRAFT | PUB-004 |
| SREQ-PH02-PUB-002 | REQ-PH02-PRODUCT-PUBLICATION | A publication request is recorded in the ACCore Outbox in the same transaction as the product change. | Employee saves a publication request. | Product change and outbox entry commit together. | SYS-ACCORE | CNT-ACR-PRODUCTMASTER, CNT-ACR-OUTBOX | AC-PH02-PUB-002-01 | TEST (planned): transaction atomicity test | DRAFT | none recorded |
| SREQ-PH02-PUB-003 | REQ-PH02-PRODUCT-PUBLICATION | Each publication or update of a product carries a monotonically increasing version. | A product is published or updated. | The version exceeds the previous one. | SYS-ACCORE | CNT-ACR-PRODUCTMASTER | AC-PH02-PUB-003-01 | TEST (planned): version test | DRAFT | none recorded |
| SREQ-PH02-PUB-004 | REQ-PH02-PRODUCT-PUBLICATION | The connector sends outbox publication requests to ACCSystem with a stable idempotency key and marks them sent only on a contract-valid acceptance receipt. | A pending publication outbox entry exists. | Entry is retried until accepted or definitively rejected. | SYS-ACCORE | CNT-ACR-CONNECTOR, CNT-ACR-OUTBOX | AC-PH02-PUB-004-01, AC-PH02-PUB-004-02 | TEST (planned): outage retry test | DRAFT | PUB-005 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH02-PUB-001 | Publishable field selection | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FR-001 AC2 |
| SREQ-PH02-PUB-002 | Atomic publication intent | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FN-INT-PUBLISH; CON-003 |
| SREQ-PH02-PUB-003 | Monotonic version | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FN-INT-PUBLISH; FR-010 AC1 |
| SREQ-PH02-PUB-004 | Reliable submission | ACT-INST-EMPLOYEE | FN-INT-PUBLISH | FN-INT-PUBLISH; FR-001 A2 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH02-PUB-001-01 | SREQ-PH02-PUB-001 | Fields outside the publish policy are absent from the projection. | IF-ACR-PUBLISH-EVENT §8.4 | FR-001 AC2 | FR-001 AC2 |
| AC-PH02-PUB-002-01 | SREQ-PH02-PUB-002 | No outbox entry exists without the committed product change and vice versa. | IF-ACR-PUBLISH-EVENT §8.5 | FN-INT-PUBLISH §4 step 2 | FN-INT-PUBLISH; CON-003 |
| AC-PH02-PUB-003-01 | SREQ-PH02-PUB-003 | Consecutive submissions for one product have strictly increasing versions. | IF-ACR-PUBLISH-EVENT §8.4 | FN-INT-PUBLISH §4 | FN-INT-PUBLISH; FR-010 AC1 |
| AC-PH02-PUB-004-01 | SREQ-PH02-PUB-004 | Retries reuse the key {institution_id}:{seller_product_id}:{version}. | IF-ACR-PUBLISH-EVENT §8.6 | FN-INT-PUBLISH §6.2 | FN-INT-PUBLISH; FR-001 A2 |
| AC-PH02-PUB-004-02 | SREQ-PH02-PUB-004 | Definitive 4xx errors are recorded for correction; transient errors retry with backoff. | IF-ACR-PUBLISH-EVENT §8.7 | FN-INT-PUBLISH §7 | FN-INT-PUBLISH; FR-001 A2 |

## 5. Alternate paths, failure, exception and uncertainty handling

- ACCSystem unavailable: the event stays in the Outbox; retried with the same key.
- Same seller_product_id from several ACCore instances is an open conflict question (PUB-003).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| PUB-004 | Which listing fields are permitted for publication is not defined. | SREQ-PH02-PUB-001 |
| PUB-005 | Acceptance receipt vs queued Catalog-owned listing_id, in-progress duplicate response, rejected-attempt representation. | SREQ-PH02-PUB-004 |

## 7. Traceability sources

- functions/specs/FN-INT-PUBLISH.md
- supporting-views/dynamic-publication-flow.md
- c3-components/CNT-ACR-CONNECTOR/CMP-CON-PUBLISHER.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
