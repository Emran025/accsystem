# CMP-CAT-SEARCHSYNC — Search Index Synchronizer

**Component ID:** CMP-CAT-SEARCHSYNC  
**Container:** CNT-ACC-CATALOG  
**System:** SYS-ACCSYSTEM  
**C4 Level:** C3 — Component  
**Status:** DRAFT | Evidence: idea.md §3.1, §4

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | CMP-CAT-SEARCHSYNC |
| **Name** | Search Index Synchronizer |
| **Container** | CNT-ACC-CATALOG |
| **Responsibility** | Propagates approved listing state changes to CNT-ACC-SEARCH, ensuring the search index reflects the current active catalog. Event-driven; handles retries and failure recovery. |

---

## 2. Collaborators

| Collaborator | Direction | Interface / Event | Purpose |
|---|---|---|---|
| CMP-CAT-LISTING | Inbound event | `ListingApproved`, `ListingUpdated`, `ListingRemoved` | Source of truth events triggering sync |
| CNT-ACC-SEARCH | Outbound API | Search index write API | Upsert or delete search document |
| CNT-ACC-EVENTBUS | Inbound subscription | Event subscription | Receives listing events via event bus |
| Sync State Store | Read/Write | DB / cache | Tracks last-synced version per listing for idempotency and retry |

---

## 3. Data Owned

**Sync State Record (operational state, not business entity):**
```
listing_id      UUID (FK)
last_synced_version  integer
last_synced_at  timestamp
sync_status     enum {SYNCED, PENDING, FAILED}
retry_count     integer
last_error      text (nullable)
```

No separate business data owned — search documents are projections of Listing data.

---

## 4. Behavior / Rules / State

### Event Handling

| Event | Action on CNT-ACC-SEARCH |
|---|---|
| `ListingApproved` | Upsert document: `{listing_id, title, description, price_snapshot, availability_snapshot, institution_id, media_refs}` |
| `ListingUpdated` | Upsert document with new snapshot values |
| `ListingRemoved` | Delete document by `listing_id` |
| `ListingRejected` | A never-indexed new listing may need no removal; a rejected update/revalidation can have prior indexed content. Product/Catalog must decide the authoritative permitted state and its index effect; do not assume either always hide or always retain. |

### Idempotency
- Each event carries `{listing_id, event identity, and an approved ordering/change identity}`; source product version alone is insufficient for every removal or stock/change event.
- An implementation must use a distinct monotonic Catalog change revision or equivalent ordered, event-idempotent state/tombstone reconciliation so same-version removal cannot be skipped and stale upserts cannot resurrect removed content. Exact mechanism is an Operations/Architecture gate.
- Upsert is idempotent at CNT-ACC-SEARCH level (by listing_id). Rebuilds need an approved state-reset/generation or equivalent procedure: replay against retained `last_synced_version` alone may skip every needed entry. Preserve version guards and protect concurrent newer updates and withdrawals; Operations/Architecture must select and verify the mechanism.

### Retry Policy
1. First attempt: immediate.
2. On failure: exponential backoff using configurable `catalog.retry_policy`; no schedule is asserted.
3. After the configured retry policy is exhausted: mark `sync_status=FAILED`; alert operations.
4. Manual re-trigger available via admin operation.

---

## 5. Failure Modes

| Failure | Detection | Mitigation |
|---|---|---|
| CNT-ACC-SEARCH unavailable | Connection error / timeout | Retry with backoff; event stays in bus or Outbox until consumed |
| Partial sync (search document partially written) | Health check on search API | Search API must be idempotent; re-send full document |
| Event bus message loss | At-least-once delivery by CNT-ACC-EVENTBUS | Duplicate events handled via version-based idempotency |
| Index inconsistency / out-of-order replay | Version/state comparison and reconciliation | Project authoritative permitted Catalog state; protect against stale replay and concurrent withdrawal, without assuming global ordering |
| Search document schema mismatch | Schema validation on write | Fail-closed: do not write corrupt document; alert operations |

---

## 6. Security

| Concern | Control |
|---|---|
| Write-only access to search index | CMP-CAT-SEARCHSYNC is the sole writer to CNT-ACC-SEARCH documents; enforced by search service ACL |
| Data minimization | Only approved listing fields sent to search; no buyer data, no internal IDs beyond listing_id |
| Audit | Sync failures logged to CNT-ACC-AUDIT with listing_id and error — ASSUMPTION |

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| Sync lag | Search results may lag listing approval. Target and monitoring require Operations/Product evidence and approval. |
| Bulk re-index | Rebuild the current permitted Catalog projection, including withdrawal/removal reconciliation; coordinate sync-state reset or generation with concurrent changes and verify completeness. Exact procedure and admin mechanism remain UNKNOWN. |
| Throughput | UNKNOWN — depends on listing publication rate. Stateless workers can be scaled horizontally. |

---

## 8. Traceability

| Claim | Evidence |
|---|---|
| Search as separate container | CONFIRMED (idea.md §3.1 — CNT-ACC-SEARCH separate from CNT-ACC-CATALOG) |
| Event-driven sync pattern | PROPOSAL — consistent with event-driven integration philosophy (idea.md §14, ADR-005) |
| Retry and DLQ policy | ASSUMPTION — exact parameters require operational decision |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Incremental index sync | Approved Catalog `ListingUpdated` event received | Search document updated under version guard and cache invalidated; latency target requires approval |
| De-listing removal | Approved Catalog `ListingRemoved` event received | Search document marked deleted/hidden; excluded from subsequent search queries. Mapping from upstream withdrawal/retraction remains open |
| Search cluster timeout | Search cluster unavailable during sync attempt | Event re-queued with exponential backoff; dead-letter alert raised when the configured retry policy is exhausted |
