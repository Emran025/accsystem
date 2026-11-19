# CNT-ACC-SEARCH — Search & Discovery

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-SEARCH |
| **Purpose** | Provides fast, indexed search and discovery capabilities over the marketplace product catalog. Consumes listing events from CNT-ACC-CATALOG to maintain a derived search index. |
| **Scope Boundary** | Owns a derived, rebuildable search index. Does NOT own listing source data (CNT-ACC-CATALOG) or inventory data. |

CONFIRMED (idea.md §3.1): "Search & Discovery — الفهرسة، البحث، التصفية، الفرز، التوصيات عند إضافتها."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-CATALOG (via CMP-CAT-SEARCHSYNC) | Inbound | Receives listing change events to update search index |
| CNT-ACC-APIGATEWAY | Inbound | Receives search query requests from client apps |
| CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE | Inbound (via gateway) | Submit search queries |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Search engine | UNKNOWN | Elasticsearch, OpenSearch, or cloud-native search — not specified. C3 deferred pending this decision. OWNER_UNASSIGNED. |
| Index rebuild | CONFIRMED (idea.md §3.1) | "فهرس بحث مشتق قابل لإعادة البناء" — index is rebuildable from catalog data |

---

## 4. Data Owned

- Derived search index (listings, attributes, facets)
- Index metadata (last updated timestamp per listing)

Does NOT own: Authoritative listing records (CNT-ACC-CATALOG).

---

## 5. Interfaces

- Provides: Search API (GET /v1/catalog/products?query=...) — CONFIRMED (idea.md §6.2)
- Consumes: Listing change events from CNT-ACC-CATALOG

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Search index unavailable | Browse by catalog direct query as fallback (degraded, slower). PROPOSAL |
| Index lag | Listings appear in search with delay; eventual consistency acceptable |
| CONFIRMED (idea.md §10.3) | "عدم ربط توافر البحث بتوافر الدفع أو التوصيل" — search availability is independent |

---

## 7. Security

- Read-only public endpoint; no mutation via search API
- Catalog data shown in search is already institution-approved for marketplace visibility

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Search query latency, index freshness lag. Targets: UNKNOWN |
| Scaling | Read-heavy workload; horizontal scaling of search nodes |
| Risk | Index can be rebuilt from catalog events if corrupted |

---

## 9. C3 Disposition

**EXCEPTION:** Search index service; primary architectural value is at the data-architecture view level, not software-component decomposition. C3 deferred pending search technology selection. See: `supporting-views/data-architecture.md`. Revisit trigger: when search technology is selected and relevance tuning or semantic search is planned.
