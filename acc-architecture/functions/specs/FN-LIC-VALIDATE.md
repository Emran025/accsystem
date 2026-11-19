# FN-LIC-VALIDATE — License Validation Function Specification

**Function ID:** FN-LIC-VALIDATE  
**Operation ID:** OP-LIC-VALIDATE  
**Status:** DRAFT | Evidence: idea.md §7, ADR-010, ADR-014

---

> **SCOPE NOTE:** This function covers **two distinct license validation paths** for two different license workflows:
>
> - **Institutional License Validation (Primary)** — ACCore backend validates that an institution holds a valid, active institutional license for the product it is running. Query identity: \{institution_id, product_code}\. This is the path served by IF-ACC-LICENSE-VALIDATE §6.4 (see \supporting-views/interface-contracts.md §6\).
> - **Marketplace Software License Validation** — ACCommerce/end-user client validates that a buyer holds an active software license for a purchased product. Query identity: \{buyer_id, product_id}\.
>
> These are **not interchangeable** identity models. See \supporting-views/dynamic-license-flow.md §7\ for the authoritative identity and ownership glossary.

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | FN-LIC-VALIDATE |
| **Name** | License Validation (Institutional + Marketplace Paths) |
| **Layer** | Query function — two paths: online (CNT-ACC-LICENSE) and offline (CNT-ACR-CONNECTOR) |
| **Triggering Components** | CMP-LIC-ENTITLEMENT (online path); CMP-CON-LICENSECHECK (offline path at ACCore) |
| **Operation ID** | OP-LIC-VALIDATE |
| **Interface** | IF-ACC-LICENSE-VALIDATE (primary: institutional online path; marketplace path uses same endpoint with different query parameters — see §4) |

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
| P2 | Query specifies `{buyer_id, product_id}` or `license_id` | CMP-LIC-ENTITLEMENT | 400 |
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
   a. Query License DB:

      -- Institutional path query only:
      SELECT * FROM licenses
      WHERE institution_id = {institution_id} AND product_code = {product_code}
        AND status = 'ACTIVE'
      ORDER BY valid_from DESC LIMIT 1

      -- Marketplace path query only:
      SELECT * FROM licenses
      WHERE buyer_id = {buyer_id} AND product_id = {product_id}
      ORDER BY issued_at DESC LIMIT 1

   b. Evaluate status:
      - ACTIVE and not expired → VALID
      - ACTIVE but expires_at < now → EXPIRED
      - REVOKED → INVALID
      - SUSPENDED → INVALID (soft)
      - Not found → NOT_FOUND

   c. Return:
      {
        result: VALID | EXPIRED | INVALID | NOT_FOUND,
        license_id,
        status,
        expires_at,
        product_scope: {product_id, features_included},
        new_token: (if requested, generate fresh offline token — ASSUMPTION)
      }

4. Caller caches result per TTL (ASSUMPTION: caller-side caching; TTL = UNKNOWN)
```

### Offline Path

```
1. ACCore application calls CMP-CON-LICENSECHECK.validate(buyer_id, product_id, token)

2. CMP-CON-LICENSECHECK:
   a. Parse token claims: {buyer_id, product_id, issued_at, expires_at, signature}
   b. Verify signature using platform public key
   c. If signature invalid → INVALID (tampered)
   d. If expires_at < now:
      - If network available → fallback to online path (step 1 above)
      - If network unavailable → EXPIRED_OFFLINE (apply grace period — UNKNOWN)
   e. Verify claims: buyer_id match, product_id match
   f. Return result

3. ACCore application uses result to gate software feature access
```

---

## 5. Postconditions

| # | Postcondition |
|---|---|
| Q1 | Caller receives definitive validation result: VALID, EXPIRED, INVALID, or NOT_FOUND |
| Q2 | (Online path only) Fresh offline token optionally returned for subsequent offline use |
| Q3 | (Online path) Validation event written to CNT-ACC-AUDIT (ASSUMPTION — rate-limited) |

---

## 6. Data, Side Effects, and Idempotency

### 6.1 Data Persisted and Side Effects
- **Data Read/Persisted:** Read-only query against License DB for entitlement records. If fresh offline token is requested, token issuance timestamp is persisted.
- **Side Effects:** Emits validation telemetry event (rate-limited); logs failed validation attempts to security audit log. No business state side effect.
- **Transaction Boundary:** Non-transactional read query with read-committed isolation.

### 6.2 Idempotency

This is a **read-only query** — inherently idempotent. No state mutations occur.

Exception: if online validation also generates a fresh offline token, that token generation follows FN-LIC-ACTIVATE token generation idempotency rules.

---

## 7. Failure / Rollback

No rollback required (read-only).

| Failure Scenario | Mitigation |
|---|---|
| License DB unavailable (online path) | Return 503; caller may retry or fall back to cached result |
| ACCSystem unreachable (offline path) | Use offline token if valid; apply grace period if expired |
| Offline token expired + no network | Return EXPIRED_OFFLINE; application behavior: UNKNOWN (policy decision) |
| Token signature check fails (key rotation) | Try all current valid keys; if all fail → INVALID |

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Online caller auth | JWT required; ACT-INST-EMPLOYEE or ACT-INDIVIDUAL or ACCore service identity |
| Result scope | Validation result scoped to `{buyer_id, product_id}`; cannot query other buyers' licenses |
| Token non-transferability | Token claims include buyer_id; mis-matched buyer → INVALID |
| Audit (online) | High-volume; ASSUMPTION: audit at sampling rate or only for INVALID results to manage volume |

---

## 9. Traceability

| Claim | Evidence |
|---|---|
| Institutional online validation API | CONFIRMED (IF-ACC-LICENSE-VALIDATE §6.4 — interface-contracts.md §6) |
| Institutional query identity: institution_id + product_code | CONFIRMED (IF-ACC-LICENSE-VALIDATE §6.4 request schema) |
| Marketplace query identity: uyer_id + product_id | CONFIRMED (marketplace license flow — dynamic-license-flow.md §7) |
| Offline validation via signed token | CONFIRMED (ADR-014, CMP-CON-LICENSECHECK) |
| Two workflows are distinct, not interchangeable | CONFIRMED (dynamic-license-flow.md §7 glossary) |
| Grace period | UNKNOWN (idea.md §12 — open decision) |
| Token TTL | UNKNOWN (idea.md §12) |
| Audit at high volume | ASSUMPTION — audit policy for high-frequency validation calls not specified |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
