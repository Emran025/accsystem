# FN-INT-PUBLISH — Product Publication Function Specification

**Function ID:** FN-INT-PUBLISH  
**Operation ID:** OP-PUBLISH-LISTING  
**Status:** DRAFT | Evidence: idea.md §4, §4.3, ADR-004, ADR-005

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | FN-INT-PUBLISH |
| **Name** | Product Publication |
| **Layer** | Cross-system integration flow: ACCore → ACCSystem |
| **Triggering Component** | CMP-CON-PUBLISHER (ACCore side) → CMP-INT-GATEWAY (ACCSystem side) |
| **Operation ID** | OP-PUBLISH-LISTING |
| **Interface** | IF-ACR-PUBLISH-EVENT |

---

## 2. Trigger

- **Who:** Institution employee (initiates in ACCore product management); CMP-CON-PUBLISHER sends automatically via Outbox
- **What:** Publish or update a product listing from ACCore to the ACCSystem marketplace catalog
- **How:** CMP-CON-PUBLISHER reads from CNT-ACR-OUTBOX → sends IF-ACR-PUBLISH-EVENT → CMP-INT-GATEWAY

---

## 3. Preconditions

| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | Institution is registered and active in ACCSystem | CMP-INT-GATEWAY (institution lookup) | 403 Unauthorized Institution |
| P2 | Publication payload is well-formed | CMP-INT-GATEWAY (schema validation) | 400 Bad Request; Outbox → FAILED |
| P3 | `{seller_product_id, institution_id, version}` is not already processed | CMP-CAT-LISTING idempotency | Return existing listing ID (no-op) |
| P4 | `version` > current listing version (if updating) | CMP-CAT-LISTING | Silently ignore (older version) |
| P5 | ACCSystem is reachable | Network | Retry with backoff via CMP-CON-PUBLISHER |

---

## 4. Execution Flow

```
ACCore Side:
1. Institution employee requests product publication in ACCore product management UI
2. CNT-ACR-PRODUCTMASTER creates/updates product and writes publication request to CNT-ACR-OUTBOX:
   {
     message_type: "ProductPublication",
     seller_product_id: "...",
     institution_id: "...",
     version: N (monotonic),
     title,
     description,
     price,
     currency_code,
     availability: IN_STOCK | OUT_OF_STOCK,
     media_refs: [...],
     category_id: "..."
   }

3. CMP-CON-PUBLISHER polls/reads from Outbox:
   POST IF-ACR-PUBLISH-EVENT to CNT-ACC-INTEGRATION endpoint
   Header: Idempotency-Key: {institution_id}:{seller_product_id}:{version}
   Header: Authorization: Bearer {oauth2_access_token}  ← OAuth 2.0 Client Credentials (CONFIRMED — IF-ACR-PUBLISH-EVENT §8.8)

---

ACCSystem Side:
4. CMP-INT-GATEWAY receives request:
   a. Authenticate institution: validate OAuth 2.0 Bearer token; resolve token → platform_institution_id (CONFIRMED — IF-ACR-PUBLISH-EVENT §8.8)
   b. Schema-validate payload
   c. Route to CMP-INT-PUBLICATION

5. CMP-INT-PUBLICATION:
   a. Log publication event
   b. Call CMP-CAT-LISTING.publish(payload)

6. CMP-CAT-LISTING:
   a. Idempotency check: {seller_product_id}:{institution_id}:{version} already processed?
      → YES: return existing listing_id (200 OK — no-op)
      → NO: continue
   b. Call CMP-CAT-VALIDATION.validate(payload)

7. CMP-CAT-VALIDATION:
   a. Format checks, completeness checks, category validation
   b. Return PASS or FAIL + violations

8. CMP-CAT-LISTING (on PASS):
   a. UPSERT Listing record (status=ACTIVE)
   b. Publish ListingApproved event → CNT-ACC-EVENTBUS
   c. Return: {listing_id, status: APPROVED}

   CMP-CAT-LISTING (on FAIL):
   a. Write Listing record (status=REJECTED)
   b. Publish ListingRejected event → CNT-ACC-EVENTBUS
   c. Return: {listing_id, status: REJECTED, violations: [...]}

9. CMP-CAT-SEARCHSYNC (async, via event bus):
   On ListingApproved: upsert search document in CNT-ACC-SEARCH
   On ListingRejected: no-op

10. ACCSystem response propagates back to CMP-INT-GATEWAY → HTTP response to CMP-CON-PUBLISHER:
    - 200 APPROVED or 200 REJECTED: Outbox marks SENT (both are valid terminal outcomes)
    - 4xx: Outbox marks FAILED (content error — notify institution admin)
    - 5xx: Outbox retries

11. Institution admin notified of REJECTED outcome (via CNT-ACC-NOTIFICATIONS — ASSUMPTION)
```

---

## 5. Postconditions

### On APPROVED:
| # | Postcondition |
|---|---|
| Q1 | Listing record exists: status=ACTIVE in CNT-ACC-CATALOG |
| Q2 | Listing visible in search (CNT-ACC-SEARCH updated by CMP-CAT-SEARCHSYNC) |
| Q3 | ListingApproved event published to event bus |
| Q4 | Outbox message marked SENT |

### On REJECTED:
| # | Postcondition |
|---|---|
| Q1 | Listing record exists: status=REJECTED |
| Q2 | ListingRejected event published |
| Q3 | Outbox message marked SENT |
| Q4 | Institution admin notified with violation reasons |

---

## 6. Data, Side Effects, and Idempotency

### 6.1 Data Persisted and Side Effects
- **Data Persisted:** Product listing records written to Catalog DB; publication event record written to Integration Outbox table with `PENDING` state.
- **Side Effects:** Emits `ProductListingPublished` domain event to Event Bus; invalidates search cache entries for the publishing institution; updates audit log.
- **Transaction Boundary:** Local database transaction within `CNT-ACC-INTEGRATION` persists listing and Outbox record atomically. Event Bus dispatch occurs asynchronously post-commit.

### 6.2 Idempotency

| Field | Value |
|---|---|
| **Key** | `{seller_product_id}:{institution_id}:{version}` |
| **Store** | CNT-ACC-CATALOG DB (listing table unique constraint) |
| **Behavior on duplicate** | Return `{listing_id, status}` of existing record — no re-processing |
| **Version semantics** | Lower version than current → silent ignore (not an error) |

---

## 7. Failure / Rollback

| Failure Scenario | Mitigation |
|---|---|
| ACCSystem returns 4xx | Outbox marks FAILED; institution must fix payload and re-publish |
| ACCSystem returns 5xx | Outbox retries with the configured backoff policy |
| Validation fails | REJECTED outcome — not a failure; seller must correct content |
| Search sync fails | Listing remains ACTIVE in catalog but not searchable; CMP-CAT-SEARCHSYNC retries |
| Partial write (listing written, event not published) | Outbox pattern prevents split-brain; event published as part of Outbox-to-bus delivery |

No rollback: publication is an advisory operation. REJECTED listings can be re-submitted with corrections.

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Institution authentication | **OAuth 2.0 Client Credentials** — institution-specific client credentials issued at ACCore provisioning time; CMP-CON-PUBLISHER obtains a Bearer token from ACCSystem's authorization server and presents it on each request. CONFIRMED (IF-ACR-PUBLISH-EVENT §8.8, interface-contracts.md). |
| Token binding | ACCSystem authorization server validates that the token's `client_id` maps to exactly one `platform_institution_id`; payload `institution_id` must match — mismatch → 403 |
| Credential rotation | OAuth 2.0 client secret rotation does not require code changes; new secret provisioned via platform admin; old secret revoked after transition period |
| Scope | Institution can only publish products for its own `institution_id` (enforced by token → institution_id binding) |
| Transport | HTTPS/TLS only — no plaintext connections accepted |
| Content injection | CMP-CAT-VALIDATION sanitizes text fields |
| Audit | All publication events (approved, rejected) written to CNT-ACC-AUDIT |

---

## 9. Traceability

| Claim | Evidence |
|---|---|
| ACCore → ACCSystem product publication | CONFIRMED (idea.md §4.3 — institution product listing) |
| Outbox pattern for reliable delivery | CONFIRMED (ADR-005, CNT-ACR-OUTBOX) |
| ACCSystem as catalog quality gatekeeper | CONFIRMED (ADR-004 — validation at ACCSystem) |
| Institution notification on rejection | ASSUMPTION — notification mechanism not detailed in idea.md §4 |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
