# CNT-ACC-OFFER — Offer / Price / Availability

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-OFFER |
| **Purpose** | Provides current price and availability snapshots for marketplace listings, including real-time or near-real-time re-verification at checkout. Maintains marketplace offer projections — not the inventory source of truth. |
| **Scope Boundary** | Owns marketplace price/availability snapshot with staleness metadata. Does NOT own the original inventory or pricing (source at CNT-ACR-PRODUCTMASTER / CNT-ACR-INVENTORY). |

CONFIRMED (idea.md §3.1): "Offer / Price / Availability — عرض السعر وشروط البيع وحالة الإتاحة بحسب آخر تحديث وسياسة التحقق."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-CATALOG | Inbound | Receives price/availability updates from listing change events |
| CNT-ACC-CART | Inbound | Cart service queries current offer for price validation |
| CNT-ACC-ORDERS | Inbound | Pre-confirmation re-verification of price snapshot |
| CNT-ACR-CONNECTOR (via Integration) | Inbound | Receives StockAvailabilityChanged events |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Cache | ASSUMPTION | Price/availability snapshots are cache-friendly — likely Redis or similar. Not confirmed. |
| Staleness policy | UNKNOWN (idea.md §12) | "حداثة السعر والمخزون" — open decision. OWNER_UNASSIGNED. |

---

## 4. Data Owned

- Offer snapshots: `{listing_id, current_price, currency, availability_status, last_updated_at, staleness_ttl}`

Does NOT own: Real inventory levels (CNT-ACR-INVENTORY), authoritative pricing (CNT-ACR-PRODUCTMASTER).

CONFIRMED (idea.md §5): "نسخة عروض السوق ولقطة السعر/الإتاحة مع وقت التحديث؛ ليس سجل المخزون الأصلي."

---

## 5. Interfaces

- Provides: Price/availability query API (consumed by CNT-ACC-CART for validation)
- Provides: Re-verification signal at checkout before order confirmation

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Offer service unavailable | Checkout blocked; cannot confirm price — fail-safe (do not proceed with stale price) |
| Stale snapshot older than TTL | Re-query or flag staleness warning to buyer |

---

## 7. Security

- Institution isolation: each offer is scoped to platform_institution_id — CONFIRMED (idea.md §9)
- Price cannot be set by client; always read from service — prevents price manipulation

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Offer query latency; staleness alert threshold. Targets: UNKNOWN |
| Risk | Stale price at checkout leads to customer disputes; re-verification at checkout mitigates |

---

## 9. C3 Disposition

**EXCEPTION:** Straightforward read-through cache with staleness policy. C3 deferred pending pricing-rule complexity decision (open decision idea.md §12). Revisit trigger: when tiered pricing, promotions, or dynamic pricing rules are introduced.
