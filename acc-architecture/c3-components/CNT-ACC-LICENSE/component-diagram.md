# C3 Component Diagram — CNT-ACC-LICENSE (License Management Service)

**Container:** CNT-ACC-LICENSE  
**System:** SYS-ACCSYSTEM  
**Status:** DRAFT | Evidence: idea.md §3.1, §7, §14

---

## Component Interaction Diagram

```mermaid
flowchart TD
    subgraph Callers["Triggering Sources"]
        EVENTBUS["CNT-ACC-EVENTBUS\n(OrderConfirmed event)"]
        IDENTITY["CNT-ACC-IDENTITY\n(AuthN/AuthZ)"]
        ACMANAGEMENT["SYS-ACMANAGEMENT\n(Admin Portal)"]
        ACCOMMERCE["SYS-ACCOMMERCE\n(License query)"]
        CONNECTOR["CNT-ACR-CONNECTOR\n(License validate — remote)"]
    end

    subgraph CNT-ACC-LICENSE["CNT-ACC-LICENSE — License Management Service"]
        ISSUANCE["CMP-LIC-ISSUANCE\nLicense Issuance Engine"]
        ENTITLEMENT["CMP-LIC-ENTITLEMENT\nEntitlement Query Handler"]
        LIFECYCLE["CMP-LIC-LIFECYCLE\nLicense Lifecycle Manager"]
        OFFLINE["CMP-LIC-OFFLINE\nOffline Token Generator"]
    end

    subgraph Stores["Data Stores"]
        LICDB[("License DB\nPostgres — licenses,\nentitlements, tokens")]
    end

    subgraph External["External & Downstream"]
        EVENTBUS2["CNT-ACC-EVENTBUS\n(LicenseActivated / Revoked)"]
        SOFTCAT["CNT-ACC-SOFTCAT\n(Software Catalog)"]
        AUDIT["CNT-ACC-AUDIT\n(Audit Log)"]
    end

    %% Issuance trigger
    EVENTBUS -->|"OrderConfirmed event\n{order_id, buyer_id, product_id}"| ISSUANCE
    ISSUANCE -->|"Validate software product"| SOFTCAT
    ISSUANCE -->|"Create License record"| LICDB
    ISSUANCE -->|"Request first offline token"| OFFLINE
    ISSUANCE -->|"Publish LicenseActivated"| EVENTBUS2
    ISSUANCE -->|"Audit: license issued"| AUDIT

    %% Offline token generation
    OFFLINE -->|"Sign token (private key, ADR-014)"| OFFLINE
    OFFLINE -->|"Store token metadata"| LICDB
    OFFLINE -->|"Return signed token"| ISSUANCE

    %% Entitlement query
    ACCOMMERCE -->|"IF-ACC-LICENSE-VALIDATE\nquery {license_id or buyer_id+product_id}"| ENTITLEMENT
    CONNECTOR -->|"IF-ACC-LICENSE-VALIDATE\n(online fallback)"| ENTITLEMENT
    ENTITLEMENT -->|"Read license state"| LICDB
    ENTITLEMENT -->|"Return Active / Expired / Revoked"| ACCOMMERCE

    %% Lifecycle management
    ACMANAGEMENT -->|"Renew / revoke / suspend"| LIFECYCLE
    LIFECYCLE -->|"Update license state"| LICDB
    LIFECYCLE -->|"Publish LicenseRevoked"| EVENTBUS2
    LIFECYCLE -->|"Audit: state change"| AUDIT
    IDENTITY -->|"AuthZ check"| LIFECYCLE
```

---

## Component Summary

| Component | ID | Role |
|---|---|---|
| License Issuance Engine | CMP-LIC-ISSUANCE | Consumes OrderConfirmed; creates License records; idempotent on order_id+product_id |
| Entitlement Query Handler | CMP-LIC-ENTITLEMENT | Answers online validation queries (IF-ACC-LICENSE-VALIDATE) |
| License Lifecycle Manager | CMP-LIC-LIFECYCLE | Admin-driven state transitions: renew, suspend, revoke |
| Offline Token Generator | CMP-LIC-OFFLINE | Produces short-lived signed entitlement tokens for offline use (ADR-014) |

---

## Key Flows

### Flow 1 — License Activation (post-purchase)
1. `OrderConfirmed` event consumed by **CMP-LIC-ISSUANCE**
2. ISSUANCE validates product exists in CNT-ACC-SOFTCAT
3. ISSUANCE writes License (`ACTIVE`, bound to buyer_id + product_id + order_id)
4. ISSUANCE calls **CMP-LIC-OFFLINE** to generate first signed entitlement token
5. `LicenseActivated` event published; audit entry written

### Flow 2 — Online Entitlement Check
1. Client calls `IF-ACC-LICENSE-VALIDATE` → **CMP-LIC-ENTITLEMENT**
2. ENTITLEMENT reads License from DB → returns `{status, expiry, product_scope}`
3. Caller caches result per TTL (ASSUMPTION — TTL duration: UNKNOWN)

### Flow 3 — Offline Token Consumption
1. ACCore's **CMP-CON-LICENSECHECK** holds a signed token from previous online session
2. Token validated locally: signature (platform public key), expiry, product_id match
3. If token expired and network available → fallback to online (Flow 2)

### Flow 4 — Admin Revocation
1. Admin via ACManagement calls LIFECYCLE with `{license_id, action=revoke}`
2. LIFECYCLE verifies admin permission via CNT-ACC-IDENTITY
3. LIFECYCLE sets License state → `REVOKED`; publishes `LicenseRevoked`
4. Existing offline tokens remain valid until expiry (ADR-014 trade-off — OPEN RISK)

---

## Open Decisions / Unknowns

| Item | Status | Consequence | Revisit Trigger |
|---|---|---|---|
| Offline token TTL | UNKNOWN | Long TTL = revocation delay; short TTL = connectivity requirement | License model decision (§12) |
| License model types (subscription vs perpetual) | UNKNOWN (idea.md §12) | Lifecycle rules differ significantly | Stakeholder decision required |
| Token refresh mechanism (push vs pull) | UNKNOWN | Offline duration limit | License model decision |

---

## Traceability

| Claim | Evidence |
|---|---|
| Software licensing as separate service | CONFIRMED (idea.md §3.1, §7 — License Management module) |
| Offline validation via signed token | CONFIRMED (idea.md §14 → ADR-014) |
| Issuance triggered by OrderConfirmed | CONFIRMED (idea.md §7.3 — post-purchase activation) |
| Token signing key management | ASSUMPTION — platform holds private key; ACCore receives public key at setup |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
