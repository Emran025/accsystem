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
| P3 | Scoped `{seller_product_id, institution_id, version}` business operation | CMP-CAT-LISTING idempotency | Completed duplicate returns available outcome; incomplete/conflicting work requires recovery, not a second effect |
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
   Header: Authorization: Bearer {oauth2_access_token}  ← illustrative OAuth 2.0 Client Credentials path; ADR-015 policy may select OAuth 2.0 Client Credentials or mTLS (IF-ACR-PUBLISH-EVENT §8.8)

---

ACCSystem Side:
4. CMP-INT-GATEWAY receives request:
   a. Authenticate institution using the ADR-015-selected OAuth 2.0 Client Credentials or mTLS policy; when OAuth is selected, validate the Bearer token and resolve token → platform_institution_id (IF-ACR-PUBLISH-EVENT §8.8)
   b. Schema-validate payload
   c. Route to CMP-INT-PUBLICATION

5. CMP-INT-PUBLICATION:
   a. Check source event identity and scoped institution/product/version business key.
   b. Validate; persist rejected attempt and return non-success for pre-admission validation/permission failure without creating or mutating a listing.
   c. For accepted work persist Integration Inbox + Catalog delivery intent in one Integration-local transaction; relay asynchronously and retain recovery state.
   d. A completed duplicate returns its recorded outcome when available; an in-progress or uncertain duplicate follows the owner-approved status/retry contract.

6. CMP-CAT-LISTING (after delivery):
   a. Apply institution/product/version idempotency and stale-version guards.
   b. On approved processing create or update the Catalog-owned listing and emit the applicable catalog state event.
   c. A separate catalog moderation/revalidation rejection, and its impact on a previous ACTIVE version, require Product/Catalog policy; do not conflate it with pre-admission rejection.

7. CMP-CAT-SEARCHSYNC updates the derived index asynchronously from the approved Catalog state; failures are retried/reconciled under policy.

8. IF-ACR-PUBLISH-EVENT describes an acceptance receipt (HTTP 200/202) with assigned/retained listing_id, not proof that indexing finished. How this Catalog-owned ID is available at acceptance while work is queued, or how a later result preserves compatibility, remains an API/Integration/Catalog gate. A durable receipt must not be given as a final processing result.

9. The ACCore Outbox marks SENT only on the contract-valid acceptance receipt; definitive pre-admission errors are recorded for correction and resubmission; transient or uncertain delivery is retained/recovered under policy. Institution notification of rejection remains an ASSUMPTION.
```

---

## 5. Postconditions

### After successful catalog processing (not merely receipt):
| # | Postcondition |
|---|---|
| Q1 | Listing record exists: status=ACTIVE in CNT-ACC-CATALOG |
| Q2 | Search synchronizes asynchronously; visibility is verified separately |
| Q3 | Applicable Catalog state event is published via its durable event path; exact source-to-catalog event mapping requires approval |
| Q4 | Outbox message marked SENT |

### On pre-admission rejection:
| # | Postcondition |
|---|---|
| Q1 | Rejected attempt and reason recorded; no listing created or mutated |
| Q2 | Structured non-success is returned; no Catalog delivery intent is created |
| Q3 | ACCore records failure and can correct and resubmit |
| Q4 | Institution notification remains an assumption; separately approved catalog moderation outcomes retain their own history and policy |

---

## 6. Data, Side Effects, and Idempotency

### 6.1 Data Persisted and Side Effects
- **Data Persisted:** Product listing records written to Catalog DB; publication event record written to Integration Outbox table with `PENDING` state.
- **Side Effects:** Emits `ProductListingPublished` domain event to Event Bus; invalidates search cache entries for the publishing institution; updates audit log.
- **Transaction Boundary:** Integration commits its accepted Inbox state and Catalog-delivery intent locally; Catalog owns its separate listing write and durable event path. No cross-container atomic commit is asserted; dispatch occurs after the relevant local commit.

### 6.2 Idempotency

| Field | Value |
|---|---|
| **Key** | `{seller_product_id}:{institution_id}:{version}` |
| **Store** | Integration Inbox for source event; Catalog business/version guard for listing effects |
| **Behavior on duplicate** | Return an available recorded outcome only where valid; recover in-progress/uncertain work without repeated listing/version effect |
| **Version semantics** | Lower version than current → silent ignore (not an error) |

---

## 7. Failure / Rollback

| Failure Scenario | Mitigation |
|---|---|
| ACCSystem returns 4xx | Outbox marks FAILED; institution must fix payload and re-publish |
| ACCSystem returns 5xx | Outbox retries with the configured backoff policy |
| Validation fails | REJECTED outcome — not a failure; seller must correct content |
| Search sync fails | Listing remains ACTIVE in catalog but not searchable; CMP-CAT-SEARCHSYNC retries |
| Catalog write committed, event relay fails | Preserve local durable event intent where supported; retry/DLQ/reconcile, without claiming downstream completion |

Pre-admission rejections can be corrected and resubmitted. Separately approved Catalog moderation states and resubmission remain available; visibility of an earlier active version on a rejected update is an open Product/Catalog decision.

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Institution authentication | **ADR-015 policy-selected OAuth 2.0 Client Credentials or mTLS** — the OAuth path uses institution-specific client credentials and a Bearer token; the mTLS path uses approved client certificates. Final method and provisioning details require onboarding/security approval (IF-ACR-PUBLISH-EVENT §8.8, interface-contracts.md). |
| Token binding | ACCSystem authorization server validates that the token's `client_id` maps to exactly one `platform_institution_id`; payload `institution_id` must match — mismatch → 403 |
| Credential rotation | Rotate the selected OAuth secret or mTLS certificate through platform-admin lifecycle controls; exact transition and revocation policy remains deployment-specific |
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
