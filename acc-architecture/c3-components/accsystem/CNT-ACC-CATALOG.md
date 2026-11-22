# CNT-ACC-CATALOG — Catalog & Publication

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-CATALOG |
| **Purpose** | Receives, validates, and maintains the marketplace projection (listing) of products published from ACCore institutions. Manages listing lifecycle (publish, update, withdraw) and synchronizes approved listings to the search index. |
| **Scope Boundary** | Owns the marketplace listing projection only. Does NOT own the source product master (at CNT-ACR-PRODUCTMASTER). Price and stock are snapshots, not sources of truth. |

CONFIRMED (idea.md §3.1): "Catalog & Publication — استقبال بيانات المنتجات المنشورة، التحقق منها، إصدارها/إيقافها."
CONFIRMED (idea.md §14, ADR-004): "ACCSystem يخزن نسخة سوقية منتقاة من بيانات المنتج ولا يملك المصدر الأصلي."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-INTEGRATION | Inbound | Delivers validated publication events from ACCore |
| CNT-ACC-SEARCH | Outbound | Pushes listing updates to search index via CMP-CAT-SEARCHSYNC |
| CNT-ACC-APIGATEWAY | Inbound | Consumer catalog queries via IF-ACC-CATALOG-QUERY |
| CNT-ACE-MOBILEAPP | Inbound (via gateway) | Catalog browsing |
| CNT-ACR-COMMERCE | Inbound (via gateway) | Catalog browsing (institutional shopping) |
| CNT-ACC-EVENTBUS | Outbound | Publishes ListingApproved, ListingUpdated, ListingWithdrawn events |
| CNT-ACC-AUDIT | Outbound | Logs all publication decisions |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Data store | UNKNOWN | Relational or document DB for listing records. OWNER_UNASSIGNED. |
| Media storage | CONFIRMED (idea.md §10.2) | Product media stored in Object Storage (EXT-PACKAGE-CDN or similar); catalog stores references |

---

## 4. Data Owned

- Product Listing records: `{listing_id, seller_product_id, platform_institution_id, title, description, price_snapshot, availability_snapshot, media_refs, status, version, last_synced_at}`
- Publication history and version chain
- Content policy validation results

CONFIRMED (idea.md §3.1): "نسخة السوق المنشورة من المنتج ومعلومات مصدرها وإصدارها."
CONFIRMED (idea.md §5.1): "يجب أن يحفظ ACCSystem رقم الإصدار ووقت آخر مزامنة."

Does NOT own: Original product master, real-time inventory/stock, raw media files.

---

## 5. Interfaces

- **IF-ACC-CATALOG-QUERY** (provider): REST API for catalog browsing (consumers: CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE, CNT-ACC-APIGATEWAY)
- Consumes: Publication events from CNT-ACC-INTEGRATION

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Search index sync fails | CMP-CAT-SEARCHSYNC retries; listing is approved in catalog even if search index lags |
| Publication event malformed | CMP-CAT-VALIDATION rejects; ListingRejected event published; error logged |
| Catalog DB unavailable | Browse/query returns 503; publication pipeline pauses |

---

## 7. Security

- Institution isolation: each listing is scoped to platform_institution_id; cross-institution read is controlled by query policy — CONFIRMED (idea.md §9)
- Content policy enforcement via CMP-CAT-VALIDATION before listing goes live — PROPOSAL

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Catalog query availability and latency. Targets: UNKNOWN |
| Staleness | UNKNOWN (open decision §12): Price/stock freshness policy — how stale can the catalog snapshot be? OWNER_UNASSIGNED |
| Risk | Stale price snapshot could lead to price discrepancy; re-verification at checkout mitigates — CONFIRMED (idea.md §5) |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-CAT-LISTING — Product Listing Manager
- CMP-CAT-VALIDATION — Publication Validator
- CMP-CAT-SEARCHSYNC — Search Index Synchronizer

See: `c3-components/CNT-ACC-CATALOG/`
