# CMP-CON-LICENSECHECK — License Validator

**Component ID:** CMP-CON-LICENSECHECK  
**Container:** CNT-ACR-CONNECTOR  
**System:** SYS-ACCORE (per-institution instance)  
**C4 Level:** C3 — Component  
**Status:** DRAFT | Evidence: idea.md §7, §14 → ADR-014

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | CMP-CON-LICENSECHECK |
| **Name** | License Validator |
| **Container** | CNT-ACR-CONNECTOR |
| **Responsibility** | Validates software entitlement tokens locally without requiring a network call to ACCSystem. Uses platform public key (ADR-014). Falls back to online validation via IF-ACC-LICENSE-VALIDATE when the offline token is expired and network is available. |

---

## 2. Collaborators

| Collaborator | Direction | Interface / Event | Purpose |
|---|---|---|---|
| ACCore application layer | Inbound | Internal call (library or service) | Requests license validation for a buyer + product |
| Platform Public Key Store | Read | Config file or certificate store | Verifies token signature (public key) |
| CNT-ACC-LICENSE (CMP-LIC-ENTITLEMENT) | Outbound (conditional) | IF-ACC-LICENSE-VALIDATE | Online fallback when offline token expired |
| Token Cache | Read/Write | Local cache | Caches last validated token and result |

---

## 3. Data Owned

**Token Cache Entry (local, ephemeral):**
```
cache_key           string ("{buyer_id}:{product_id}")
token               string (JWT or signed blob — ADR-014)
token_expiry        timestamp
last_validated_at   timestamp
last_result         enum {VALID, INVALID, EXPIRED}
```

**Platform Public Key (config, not operational data):**
```
key_id              string (key rotation ID)
public_key_pem      string
valid_from          timestamp
valid_until         timestamp (nullable)
```

---

## 4. Behavior / Rules / State

### Validation Logic (ADR-014)

```
function validate(buyer_id, product_id, token):
  if token is null or not present:
    return INVALID (no entitlement token)
  
  parse token claims: {buyer_id, product_id, issued_at, expires_at, signature}
  
  step 1 — signature check:
    verify signature using platform public key
    if invalid → return INVALID (tampered or wrong key)
  
  step 2 — expiry check:
    if expires_at < now:
      if network available:
        → online fallback (IF-ACC-LICENSE-VALIDATE)
        if online says ACTIVE → refresh token (new token returned)
        → return online result
      else:
        → return EXPIRED_OFFLINE (use grace period if configured — UNKNOWN)
  
  step 3 — claims check:
    verify token.buyer_id == requested buyer_id
    verify token.product_id == requested product_id
    if mismatch → return INVALID
  
  → return VALID
```

### Token Refresh
- When online fallback succeeds: ACCSystem returns new signed token with fresh expiry
- New token stored in Token Cache for subsequent offline use
- ASSUMPTION: token TTL is configured by platform (UNKNOWN — exact TTL; idea.md §12)

### Grace Period (UNKNOWN)
- After token expiry, offline behavior during grace period: UNKNOWN — policy not specified
- OWNER_UNASSIGNED; revisit trigger: License model specification

---

## 5. Failure Modes

| Failure | Detection | Mitigation |
|---|---|---|
| Token signature invalid | Crypto verification fails | Return INVALID immediately; log anomaly |
| Token expired, no network | Expiry + network check | Return EXPIRED_OFFLINE; application decides behavior (ASSUMPTION: allow limited access during grace period) |
| Public key unavailable | Key store read fails | FAIL-CLOSED: return INVALID; alert operations |
| Public key expired (rotation) | valid_until < now | Load next valid key; ASSUMPTION: multiple keys supported for rotation overlap |
| Online fallback unavailable | Connection timeout | Return EXPIRED_OFFLINE; application decides behavior |
| Tampered token | Signature mismatch | Return INVALID; log with token metadata for security audit |

---

## 6. Security

| Concern | Control |
|---|---|
| Public key integrity | Public key distributed at ACCore instance provisioning; signed by platform (ASSUMPTION) |
| Key rotation | Platform rotates key pair periodically; ACCSystem signs new tokens with new key; both keys valid during overlap |
| No private key at ACCore | ACCore NEVER receives or stores the platform private key — offline validation uses public key only (ADR-014 core constraint) |
| Token replay | Tokens are buyer + product specific; non-transferable; replay by different buyer → claims check fails |
| Audit | All INVALID results logged with token metadata (without full token) |

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| Key distribution | Platform must have operational procedure for distributing updated public keys to all ACCore instances |
| Token TTL tuning | Short TTL = more online calls (connectivity requirement); long TTL = slower revocation propagation. Currently UNKNOWN. |
| Offline duration | Directly tied to token TTL + grace period. Must be decided by business. |

---

## 8. Traceability

| Claim | Evidence |
|---|---|
| Offline validation via signed token | CONFIRMED (idea.md §14 → ADR-014) |
| Public key at ACCore, private key at ACCSystem | CONFIRMED (ADR-014 — offline validation design) |
| Grace period | UNKNOWN (idea.md §12 — open decision on offline license validation strategy) |
| Token TTL | UNKNOWN (idea.md §12 — open decision) |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
