# CMP-LIC-ENTITLEMENT — Entitlement Evaluator

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-LIC-ENTITLEMENT |
| **Parent Container** | CNT-ACC-LICENSE |
| **Purpose** | Answers online license validation queries: given an institutional {institution_id + product_code} or marketplace {buyer_id + product_id/license_id} request, returns whether the entitlement is valid, what units/modules are licensed, and the license state. |
| **Scope Boundary** | Read-only entitlement evaluation. Does NOT modify license state (CMP-LIC-LIFECYCLE). |

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-CONNECTOR / CMP-CON-LICENSECHECK | Inbound | Online validation queries via IF-ACC-LICENSE-VALIDATE |
| License record store | Inbound | Reads license state |
| CNT-ACC-IDENTITY | Outbound | Validates requesting service identity |

---

## 3. Behavior, Rules, and State

**Validation flow:**
1. Receive validation request `{institution_id + product_code, modules_requested} for institutional validation OR {buyer_id + product_id/license_id, modules_requested} for marketplace validation`
2. Load license record; check: status=Active, not Expired, not Revoked
3. Check modules/units requested ≤ licensed capacity
4. Check validity period (valid_from ≤ today ≤ valid_until + grace_period)
5. Return `{valid: true/false, licensed_modules, units, expires_at, grace_until}`

**Rules:**
- Suspended license → valid=false
- Within grace period after expiry → valid=true with warning
- Usage/seat capacity exceeded → valid=false with capacity_exceeded flag

---

## 4. Data

Read-only consumer of License records owned by CMP-LIC-ISSUANCE and CMP-LIC-LIFECYCLE.

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| License DB unavailable (online path) | Return error; ACCore falls back to cached offline token (ADR-014) |
| License not found | Return valid=false |
| Ambiguous query | Apply the workflow-specific selection order: institutional `valid_from`, marketplace `issued_at`; use a deterministic identifier tie-break only after eligibility; log ambiguity. |

---

## 6. Security

- IF-ACC-LICENSE-VALIDATE restricted to authorized services only (CNT-ACR-CONNECTOR)
- CONFIRMED (idea.md §4.3): Validation does not expose ERP data

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "زمن استجابة خدمة الترخيص" and "محاولات استخدام وحدات غير مرخصة" monitored |


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Active license evaluation | Query with valid `institution_id` and active `product_code` | Entitlement evaluates to `VALID`; feature flags and seat limit returned |
| Expired license evaluation | Query for license past validity date and grace period | Entitlement evaluates to `EXPIRED`; restricted modules gated |
| Offline token verification | Signed offline JWT validated against public key | Signature and claims verified locally without network call |
