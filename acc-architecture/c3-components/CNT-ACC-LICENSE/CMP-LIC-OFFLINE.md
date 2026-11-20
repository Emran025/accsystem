# CMP-LIC-OFFLINE — Offline Credential Issuer

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-LIC-OFFLINE |
| **Parent Container** | CNT-ACC-LICENSE |
| **Purpose** | Issues short-lived signed entitlement tokens that ACCore can validate locally without connecting to ACCSystem. Implements ADR-014 (offline license validation strategy). |
| **Scope Boundary** | Token issuance only. Token validation occurs at CMP-CON-LICENSECHECK in ACCore. |

CONFIRMED (idea.md §4.3): "يتحقق Backend الخاص بـ ACCore من License & Entitlement Management عبر قناة خدمة موثقة، أو يتحقق محلياً من اعتماد موقّع قصير/متوسط العمر وفق سياسة الانقطاع."
CONFIRMED (idea.md §14, ADR-014): Signed entitlement tokens for offline validation.

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CMP-LIC-ENTITLEMENT | Inbound | Provides current entitlement state before token is signed |
| CMP-LIC-ISSUANCE | Inbound | Separate retriable work: institutional token after ISSUED and before activation; marketplace token after the directly ACTIVE license record |
| CNT-ACR-CONNECTOR / CMP-CON-LICENSECHECK | Consumer | Receives tokens and validates them locally |

---

## 3. Behavior, Rules, and State

**Token structure (PROPOSAL — exact format UNKNOWN):** See the two valid illustrative workflow-specific examples in ADR-014: institutional `institution_id + product_code`; marketplace `buyer_id + product_id`. Each includes `workflow`, `license_id`, issue/expiry and signature; institutional module/seat claims remain supported. Grant validity and token TTL are separate. Both workflows need authenticated, locally verifiable grant bounds or equivalent evidence for offline use; missing required evidence cannot grant access. Perpetual/null-expiry semantics, claim encoding and JWT mapping require approval.

**Rules:**
- Token TTL: short-lived (UNKNOWN: exact duration — hours to days depending on product sensitivity). OWNER_UNASSIGNED.
- Signed with platform private key; CMP-CON-LICENSECHECK validates with platform public key
- Revoked licenses → new tokens NOT issued. An offline validator may not yet know revocation; any token-derived use remains bounded by credential expiry, grant validity, observed revocation and applicable approved policy. Revocation exposure is an unresolved risk, not an unconditional right to operate until TTL.
- Grace after token expiry is UNKNOWN and applies only if explicitly approved; otherwise restrict licensed features while preserving separately permitted local operation.

**Signing key management:** UNKNOWN — technology and key rotation process not specified. OWNER_UNASSIGNED.

---

## 4. Data and Side Effects

| Data | Owned |
|---|---|
| Token issuance log: `{token_id, license_id, issued_at, expires_at}` | CMP-LIC-OFFLINE |

Tokens themselves are stateless (signed payloads) — no server-side session needed.

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Signing key unavailable | No token-ready claim; retain durable issuance work for recovery, and use independently authorized online validation where supported |
| License revoked but old token not yet expired | Offline revocation may be unseen; enforce known revocation and grant/credential bounds, and resolve exposure policy with Security/Product |
| Key compromise | Emergency key rotation needed — UNKNOWN: rotation procedure. OWNER_UNASSIGNED. |

---

## 6. Security

- CONFIRMED (idea.md §12): Short-lived signed credential balances offline protection and connectivity resilience
- Asymmetric signing: private key never leaves ACCSystem; public key distributed to ACCore
- CONFIRMED (idea.md §9): Key management must be outside source code

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "فشل التحقق" monitored |
| Risk | Revocation window (time between license revocation and offline token expiry) is a known security gap — size determined by TTL policy (UNKNOWN) |


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Offline token generation | Request for offline entitlement token | Cryptographically signed JWT produced with platform private key and claims |
| Platform key rotation | Key rotation event triggered | New tokens signed with new key; verification supports active key set |
| Tampered token rejection | Client modifies payload claims | Verification algorithm rejects signature; access denied |
