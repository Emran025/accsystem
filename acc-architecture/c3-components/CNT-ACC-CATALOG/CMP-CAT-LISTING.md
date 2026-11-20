# CMP-CAT-LISTING — Product Listing Manager

**Component ID:** CMP-CAT-LISTING  
**Container:** CNT-ACC-CATALOG  
**System:** SYS-ACCSYSTEM  
**C4 Level:** C3 — Component  
**Status:** DRAFT | Evidence: idea.md §3.1, §4, §14 → ADR-004

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | CMP-CAT-LISTING |
| **Name** | Product Listing Manager |
| **Container** | CNT-ACC-CATALOG |
| **Responsibility** | Maintains the marketplace catalog as a projection of institution products published from ACCore instances. Owns `Listing` entity lifecycle. |
| **Source of truth?** | No — projection only. Source of truth is ACCore's Product Master (CNT-ACR-PRODUCTMASTER). CONFIRMED (idea.md §4, ADR-004) |

---

## 2. Collaborators

| Collaborator | Direction | Interface / Event | Purpose |
|---|---|---|---|
| CMP-INT-PUBLICATION | Inbound | `ListingPublicationRequest` event | Receives validated publication payloads from integration layer |
| CMP-CAT-VALIDATION | Inbound call | Internal sync call | Returns validation verdict before record is written |
| CMP-CAT-SEARCHSYNC | Outbound event | `ListingApproved`, `ListingUpdated`, `ListingRemoved` | Triggers search index update |
| CNT-ACC-EVENTBUS | Outbound | Event envelope | Publishes listing state events |
| CNT-ACC-AUDIT | Outbound | Audit entry | Records listing create/update/remove actions |
| Catalog DB | Read/Write | SQL | Persists Listing records |

---

## 3. Data Owned

**Listing Entity:**
```
listing_id              UUID (PK, generated)
seller_product_id       string (source ID from ACCore)
platform_institution_id UUID (FK — institution)
title                   string (from publication payload)
description             text
price_snapshot          decimal + currency_code
availability_snapshot   enum {IN_STOCK, OUT_OF_STOCK, LIMITED}
media_refs              JSON array of CDN URLs
status                  enum {PENDING_REVIEW, ACTIVE, REJECTED, REMOVED}
version                 integer (monotonic, from ACCore publication)
last_synced_at          timestamp
created_at              timestamp
updated_at              timestamp
rejection_reason        text (nullable)
```

**Data governance:**
- Listing is immutable beyond status transitions and snapshot updates
- Price/stock is a **snapshot**, not live — staleness policy is UNKNOWN (idea.md §12); ASSUMPTION: stale until next publication event
- Media URLs reference EXT-PACKAGE-CDN — not stored locally

---

## 4. Behavior / Rules / State

### State Machine

These Catalog moderation states are distinct from pre-admission validation/permission rejection, which must not create or mutate a listing. How a rejected update affects prior ACTIVE content and its search projection remains a Product/Catalog decision; preserve prior history until governed.

```
PENDING_REVIEW → ACTIVE       (on CMP-CAT-VALIDATION PASS)
PENDING_REVIEW → REJECTED     (on CMP-CAT-VALIDATION FAIL)
ACTIVE         → REMOVED      (on seller retraction or admin action)
ACTIVE         → PENDING_REVIEW (on update publication — re-validates)
REJECTED       → PENDING_REVIEW (on seller re-submission)
```

### Rules
1. **Idempotency:** Publication events identified by `{seller_product_id, platform_institution_id, version}`. Duplicate version → ignored (no-op). Lower version → ignored.
2. **Projection update:** When a new version arrives with higher `version` number, replace snapshot fields; keep listing_id stable.
3. **Removal:** Seller withdrawal and administrative removal retain listing history and can result in removal from search. This view names `ProductRetracted` and `REMOVED`; IF-ACR-PUBLISH-EVENT names `ProductListingWithdrawn`, while other views use `WITHDRAWN`. API/Integration/Catalog must approve their mapping and versioned event/state names; do not assume they are wire synonyms. Catalog emits its applicable removal event (currently described as `ListingRemoved`).
4. **No price-enforcement:** ACCSystem does not enforce price changes at order time (see CNT-ACC-OFFER for real-time offer validation). CONFIRMED (idea.md §12 — open decision on freshness).

---

## 5. Failure Modes

| Failure | Detection | Mitigation |
|---|---|---|
| Duplicate publication event | version check | Idempotent write (UPSERT by {seller_product_id, institution_id, version}) |
| Validation service unavailable | CMP-CAT-VALIDATION call fails | Leave listing in PENDING_REVIEW; retry on next event; DLQ after N retries |
| Search sync failure | CMP-CAT-SEARCHSYNC event not consumed | Outbox pattern for event delivery; CNT-ACC-EVENTBUS supports at-least-once delivery attempts and duplicate-safe effects, with retry/DLQ recovery policy still gated |
| CDN media URL invalid | No validation at receipt | UNKNOWN — validation policy not specified; ASSUMPTION: validate URL format only |
| Out-of-order version delivery | version < current | Ignore silently; log discarded version for observability |

---

## 6. Security

| Concern | Control |
|---|---|
| Write access to listings | Only CMP-INT-PUBLICATION (via event) and admin (via CNT-ACC-PLATFORMADMIN) may modify listings — no direct external write |
| Institution isolation | `platform_institution_id` enforced on every query — no cross-institution listing read without explicit authorization |
| Content injection via title/description | Input sanitized by CMP-CAT-VALIDATION before record write |
| Audit trail | All create/update/remove events written to CNT-ACC-AUDIT with actor, timestamp, version |

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| Catalog size | UNKNOWN — number of institutions × products. Pagination required on all list queries. Index on `status`, `platform_institution_id`. |
| Stale data | Price/stock snapshot may lag real ACCore state. Downstream order path re-validates via CNT-ACC-OFFER. CONFIRMED (ADR-004). |
| Rehydration | If Catalog DB is lost, re-publication from all ACCore instances can rebuild projection. Operational procedure: UNKNOWN. |

---

## 8. Traceability

| Claim | Evidence |
|---|---|
| Marketplace projection pattern | CONFIRMED (idea.md §4.1, §14 → ADR-004) |
| ACCSystem does not own product master | CONFIRMED (idea.md §4.1 — ACCore is source of truth) |
| Price staleness as open issue | CONFIRMED (idea.md §12 — open decision on price/stock freshness) |
| CMP-CAT-VALIDATION pre-write | PROPOSAL — logical separation of concerns; validation step not explicitly described in idea.md §4 |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Create product listing | Valid catalog listing payload from authorized institution | Listing persisted as approved; Catalog state event emitted; exact publication-to-Catalog event mapping is an API/Catalog gate |
| Duplicate listing submission | Same institution submits listing with identical idempotency key | HTTP 200 returned with existing listing ID; no duplicate record created |
| Invalid taxonomy code | Listing references nonexistent category taxonomy | Pre-admission rejection records the attempt but does not mutate the listing; exact error code and separate moderation outcomes require contract/policy approval |
| Bulk listing query | Query with institution and status filter | Returns paginated listing array matching filter criteria |
