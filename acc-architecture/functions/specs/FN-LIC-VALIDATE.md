# FN-LIC-VALIDATE — License Validation Function Specification

**Function ID:** FN-LIC-VALIDATE  
**Operation ID:** OP-LIC-VALIDATE  
**Status:** DRAFT | Evidence: idea.md §7, ADR-010, ADR-014

---

> **SCOPE NOTE:** This function covers **two distinct license validation paths** for two different license workflows:
>
> - **Institutional License Validation** — ACCore validates the scoped `{institution_id, product_code}` path, described by IF-ACC-LICENSE-VALIDATE §6.4.
> - **Marketplace Software License Validation** — ACCommerce/end-user client uses `{buyer_id, product_id}` or an authorized `license_id`; the shared-interface mapping is proposed, not approved.
>
> These identities are **not interchangeable**. See `supporting-views/dynamic-license-flow.md` §7.

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | FN-LIC-VALIDATE |
| **Name** | License Validation (Institutional + Marketplace Paths) |
| **Layer** | Query function — two paths: online (CNT-ACC-LICENSE) and offline (CNT-ACR-CONNECTOR) |
| **Triggering Components** | CMP-LIC-ENTITLEMENT (online path); CMP-CON-LICENSECHECK (offline path at ACCore) |
| **Operation ID** | OP-LIC-VALIDATE |
| **Interface** | IF-ACC-LICENSE-VALIDATE institutional POST; proposed marketplace GET/by-ID branches are separate request shapes pending API Governance — see §4 and interface §6 |

---

## 2. Trigger

- **Online path:** ACCore application or ACCommerce client calls IF-ACC-LICENSE-VALIDATE when no valid offline token is held
- **Offline path:** ACCore application calls CMP-CON-LICENSECHECK with a locally held signed entitlement token (no network call to ACCSystem)

---

## 3. Preconditions

### Online Path
| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | Caller is authenticated | CNT-ACC-IDENTITY | 401 |
| P2 | Institutional query specifies `{institution_id, product_code}`; marketplace query specifies `{buyer_id, product_id}` or `license_id` | CMP-LIC-ENTITLEMENT | 400 |
| P3 | ACCSystem is reachable | Network layer | Falls back to offline path if token available |

### Offline Path
| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | Signed token is present in local cache | CMP-CON-LICENSECHECK | INVALID (no token) |
| P2 | Platform public key is available | Key store | INVALID (cannot verify) |

---

## 4. Execution Flow

### Online Path

```
1. Caller → IF-ACC-LICENSE-VALIDATE:

   -- Institutional License path (IF-ACC-LICENSE-VALIDATE §6.4 — primary):
   POST /v1/licenses/validate
   Body: {institution_id, product_code, [module_codes], [seat_count], [installation_id]}
   Header: Authorization: Bearer {oauth2_access_token}  -- S2S OAuth 2.0 CC

   -- Marketplace Software License path:
   GET /v1/licenses/validate?buyer_id={id}&product_id={id}
   OR  GET /v1/licenses/{license_id}/status
   Header: Authorization: Bearer {JWT}

2. CNT-ACC-APIGATEWAY → CNT-ACC-IDENTITY: validate token (JWT or OAuth 2.0 CC)

3. CMP-LIC-ENTITLEMENT:
   a. Authorize the caller for the selected workflow and requested identity (including by-ID lookup).
   b. Find matching records by institution_id + product_code OR buyer_id + product_id;
      retain matches in all states for negative diagnostics. For an authorized license_id,
      check the record's workflow and scope instead of bypassing authorization.
   c. Evaluate each candidate's applicable status, grant validity and requested scope/limits
      under approved policy BEFORE selecting among eligible candidates.
   d. Proposed deterministic selection: institutional valid_from descending or marketplace
      issued_at descending, then a stable license-ID tie-break. Multiple entitlement combination,
      date boundaries, null expiry, grace and negative precedence for multiple ineligible matches
      remain OPEN to Product/Business; do not fabricate VALID or NOT_FOUND.
   e. Return the workflow-specific contract result (institutional lifecycle status plus
      entitlement, or proposed marketplace result). A token reference, if present, refers
      to separate issuance; status and evaluation result are not interchangeable.

4. Caller caches result per TTL (ASSUMPTION: caller-side caching; TTL = UNKNOWN)
```

### Offline Path

```
1. ACCore application calls CMP-CON-LICENSECHECK with the selected workflow context and token:
   institutional {institution_id, product_code} OR marketplace {buyer_id, product_id}.
2. Verify signature and appropriate workflow, license and scoped identity claims; check grant
   effective/validity bounds separately from credential issue/expiry under approved policy.
   Invalid signature, missing key or mismatched identity never yields VALID.
   If credential expired, use online validation when available; otherwise EXPIRED_OFFLINE
   and restrict/fail closed unless an approved applicable grace policy permits otherwise.
   Token issue/refresh is a separate retriable operation, not a validation side effect.

3. ACCore application uses result to gate software feature access
```

---

## 5. Postconditions

| # | Postcondition |
|---|---|
| Q1 | Caller receives an appropriate scoped result (including invalid, expired, not-found, over-capacity or unresolved policy/availability); lifecycle status and evaluation verdict are distinct |
| Q2 | Validation returns entitlement status only; token issuance/refresh is a separate retriable operation, not a side effect of this read-only query. |
| Q3 | (Online path) Validation event written to CNT-ACC-AUDIT (ASSUMPTION — rate-limited) |

---

## 6. Data, Side Effects, and Idempotency

### 6.1 Data Persisted and Side Effects
- **Data Read/Persisted:** Read-only query against License DB for entitlement records. Token issuance is excluded from this function and is handled by a separate license-owned operation.
- **Side Effects:** Emits validation telemetry event (rate-limited); logs failed validation attempts to security audit log. No business state side effect.
- **Transaction Boundary:** Non-transactional read query with read-committed isolation.

### 6.2 Idempotency

This is a **read-only query** — inherently idempotent. No state mutations occur.

Token generation and its idempotency rules belong to the activation/token-issuance operation; validation remains read-only.

---

## 7. Failure / Rollback

No rollback required (read-only).

| Failure Scenario | Mitigation |
|---|---|
| License DB unavailable (online path) | Return 503; caller may retry or fall back to cached result |
| ACCSystem unreachable (offline path) | Use valid scoped offline token; after expiry restrict/fail closed unless applicable grace is approved |
| Offline token expired + no network | Return EXPIRED_OFFLINE; application behavior: UNKNOWN (policy decision) |
| Token signature check fails (key rotation) | Try all current valid keys; if all fail → INVALID |

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Online caller auth | JWT required; ACT-INST-EMPLOYEE or ACT-INDIVIDUAL or ACCore service identity |
| Result scope | Institutional result scoped to `{institution_id, product_code}`; marketplace result scoped to `{buyer_id, product_id/license_id}`; cannot cross workflow or beneficiary scope |
| Token non-transferability | Verify workflow-specific institutional or marketplace identity and scope; mismatch → INVALID |
| Audit (online) | High-volume; ASSUMPTION: audit at sampling rate or only for INVALID results to manage volume |

---

## 9. Traceability

| Claim | Evidence |
|---|---|
| Institutional online validation API | CONFIRMED (IF-ACC-LICENSE-VALIDATE §6.4 — interface-contracts.md §6) |
| Institutional query identity: institution_id + product_code | CONFIRMED (IF-ACC-LICENSE-VALIDATE §6.4 request schema) |
| Marketplace query identity: `buyer_id + product_id` | CONFIRMED (marketplace license flow — dynamic-license-flow.md §7) |
| Offline validation via signed token | CONFIRMED (ADR-014, CMP-CON-LICENSECHECK) |
| Two workflows are distinct, not interchangeable | CONFIRMED (dynamic-license-flow.md §7 glossary) |
| Grace period | UNKNOWN (idea.md §12 — open decision) |
| Token TTL | UNKNOWN (idea.md §12) |
| Audit at high volume | ASSUMPTION — audit policy for high-frequency validation calls not specified |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
