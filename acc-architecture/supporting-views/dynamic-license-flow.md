# ACC Ecosystem — Dynamic View: License Activation Flow (Critical Flow #3)

**View type:** Dynamic / Sequence Diagram  
**Stage:** 6 — Supporting Views  
**Status:** PROPOSED  
**Source:** idea.md Sections 7.7, 4.3, 9, 12  
**Parent:** `acc-architecture/`

---

## 1. Purpose and Scope

This view documents the license activation flow for ACCore institutions. It covers:
1. ACManagement admin issuing/renewing a license via the Management Console
2. License & Entitlement Management service generating and signing an entitlement
3. ACCore License Connector receiving the entitlement
4. Online license validation path (periodic check against platform)
5. Offline license validation path (local signed credential check)

**Preconditions:**
- Institution is registered with `platform_institution_id`
- Platform admin has `license:write` role (RBAC)
- Target product and license plan are defined in License & Entitlement catalog
- ACCore backend is operational

**Postconditions (success):**
- License record created with status=ACTIVATED
- Signed entitlement token delivered to ACCore
- ACCore validates entitlement and enables licensed modules/features
- LicenseIssued + LicenseActivated events on Event Bus (audit trail)

---

## 2. License Activation Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant ADM as ACManagement Admin<br/>(Management Console)
    participant AGW as API Gateway<br/>(ACCSystem)
    participant PA as Platform Administration<br/>& Support
    participant LE as License & Entitlement<br/>Management
    participant IA as Identity & Access
    participant BUS as Event Bus
    participant IGW as Integration Gateway
    participant ACC as ACCore<br/>License Connector + Backend
    participant AUD as Audit & Observability

    Note over ADM,AUD: PHASE 1 — LICENSE REQUEST CREATION

    ADM->>AGW: POST /v1/management/institutions/{institution_id}/licenses<br/>Authorization: Bearer <admin_jwt + MFA><br/>{product_code, plan_id, seat_count, valid_from, valid_until, units[]}
    AGW->>AGW: Validate JWT (MFA claim required), extract admin_id, check role: license:write
    AGW->>PA: ForwardLicenseRequest(admin_id, institution_id, product_code, plan_id, params)
    PA->>IA: VerifyAdminPermission(admin_id, action: license:issue, resource: institution_id)
    IA-->>PA: Permission GRANTED (role + scope confirmed)
    PA->>LE: CreateLicense(institution_id, product_code, plan_id, seat_count,<br/>valid_from, valid_until, units[], issued_by: admin_id)

    Note over LE,BUS: PHASE 2 — LICENSE RECORD CREATION AND SIGNING

    LE->>LE: Validate institution eligibility and plan constraints
    LE->>LE: Create License record<br/>{license_id, institution_id, product_code, plan_id,<br/>seat_count, units[], valid_from, valid_until, status: ISSUED}
    LE->>LE: Generate signed Entitlement token (JWT or signed JSON)<br/>{entitlement_id, license_id, institution_id, product_code,<br/>units[], seat_count, valid_from, valid_until, issued_at,<br/>signature: RS256(private_key)}
    LE->>BUS: publish LicenseIssued<br/>{license_id, institution_id, product_code, issued_by, issued_at, correlation_id}
    BUS->>AUD: consume LicenseIssued → write immutable AuditEvent
    LE-->>PA: LicenseCreated(license_id, entitlement_token)
    PA-->>AGW: 201 Created (license_id, status: ISSUED)
    AGW-->>ADM: License issued — license_id, status: ISSUED

    Note over IGW,ACC: PHASE 3 — ENTITLEMENT DELIVERY TO ACCORE

    LE->>IGW: DeliverEntitlement(institution_id, entitlement_token, license_id,<br/>idempotency_key: license_id, correlation_id)
    IGW->>ACC: POST /v1/licenses/entitlement (TLS, service auth)<br/>{entitlement_token, license_id, delivered_at}

    ACC->>ACC: Verify entitlement token signature (RS256 with platform public key)
    ACC->>ACC: Check entitlement validity (not_before, not_after, institution_id match)
    ACC->>ACC: Store entitlement token locally (encrypted at rest)
    ACC->>ACC: Enable licensed units/features per entitlement.units[]
    ACC->>ACC: Set license_check_at = now + validation_interval

    ACC-->>IGW: 200 OK — EntitlementAcknowledged(entitlement_id)
    IGW->>LE: DeliveryConfirmed(license_id, entitlement_id, activated_at)
    LE->>LE: Update License status → ACTIVATED
    LE->>BUS: publish LicenseActivated<br/>{license_id, entitlement_id, institution_id, activated_at, correlation_id}
    BUS->>AUD: consume LicenseActivated → write immutable AuditEvent

    Note over ADM,AUD: PHASE 4A — ONLINE PERIODIC VALIDATION

    loop Every validation_interval (configurable, no value selected)
        ACC->>ACC: Check if validation_interval elapsed
        ACC->>IGW: POST /v1/licenses/validate (TLS, service auth)<br/>{license_id, entitlement_id, institution_id, check_at: now,<br/>usage: {active_seats, active_units[]}}
        IGW->>LE: ValidateLicense(license_id, entitlement_id, usage)
        LE->>LE: Check license status (ACTIVE / SUSPENDED / REVOKED / EXPIRED)
        LE->>LE: Check seat/usage against limits
        
        alt License ACTIVE and within limits
            LE-->>IGW: ValidationResult(status: VALID, valid_until, usage_ok: true)
            IGW-->>ACC: ValidationResult(VALID, valid_until)
            ACC->>ACC: Update local validation cache (last_validated_at = now)
            ACC->>ACC: Continue normal operation
        else License SUSPENDED or REVOKED
            LE-->>IGW: ValidationResult(status: SUSPENDED | REVOKED, reason)
            IGW-->>ACC: ValidationResult(status)
            ACC->>ACC: Restrict licensed features (grace period policy applies — UNKNOWN duration)
            LE->>BUS: publish LicenseSuspended | LicenseRevoked
            BUS->>AUD: AuditEvent
        else License EXPIRED
            LE-->>IGW: ValidationResult(status: EXPIRED)
            IGW-->>ACC: ValidationResult(EXPIRED, renewal_url)
            ACC->>ACC: Enter grace period (UNKNOWN duration) — alert institution admin
        else Usage exceeds limits (seat overuse)
            LE-->>IGW: ValidationResult(status: VALID, usage_ok: false, overage_detail)
            IGW-->>ACC: ValidationResult(usage_ok: false)
            ACC->>ACC: Alert institution admin; block new seat activations
        end
        
        LE->>BUS: LicenseValidated event (periodic)
        BUS->>AUD: AuditEvent (validation result logged)
    end

    Note over ACC,LE: PHASE 4B — OFFLINE VALIDATION (when ACCSystem unreachable)

    alt ACCSystem unreachable during validation check
        ACC->>ACC: Attempt online validation → timeout/connection failure
        ACC->>ACC: Fall back to local signed entitlement token
        ACC->>ACC: Verify signature on stored entitlement (RS256 with cached platform public key)
        ACC->>ACC: Check entitlement.valid_until > now
        
        alt Entitlement still within validity window
            ACC->>ACC: Continue operation (offline mode — CONFIRMED per idea.md §4.2, §4.3)
            ACC->>ACC: Log offline validation event locally
            Note over ACC: Offline period bounded by entitlement TTL and grace period (UNKNOWN)
        else Entitlement expired and cannot reach platform
            ACC->>ACC: Enter grace period (if configured — UNKNOWN)
            ACC->>ACC: Alert institution admin — connectivity required for license renewal
            Note over ACC: Specific offline tolerance window is UNKNOWN — requires business decision
        end
    end
```

---

## 3. License State Machine

| State | Transitions From | Transitions To | Trigger |
|---|---|---|---|
| ISSUED | — | ACTIVATED | Entitlement delivered to ACCore + acknowledged |
| ACTIVATED | ISSUED / RENEWED | ACTIVE (operational) | ACCore begins using license |
| ACTIVE | ACTIVATED | SUSPENDED | Admin suspension action |
| ACTIVE | ACTIVATED | REVOKED | Admin revocation action |
| ACTIVE | ACTIVATED | EXPIRED | `valid_until` timestamp passed |
| ACTIVE | ACTIVATED | RENEWED | Renewal issued before expiry |
| SUSPENDED | ACTIVE | ACTIVE | Suspension lifted |
| SUSPENDED | ACTIVE | REVOKED | Further action taken |
| EXPIRED | ACTIVE | RENEWED | Renewal issued |
| RENEWED | EXPIRED / ACTIVE | ACTIVE | New entitlement delivered and acknowledged |
| REVOKED | Any | (terminal) | Irrevocable revocation (compliance event) |

---

## 4. Online vs Offline Validation Comparison

| Attribute | Online Path | Offline Path |
|---|---|---|
| Trigger | Periodic validation interval elapsed | ACCSystem unreachable |
| Validation source | License & Entitlement Management service (authoritative) | Local signed entitlement token (cached) |
| Covers revocation? | Yes — real-time status check | No — revocation not reflected until connectivity restored |
| Coverage | Full: status, seat count, usage, unit list | Limited: signature validity + expiry only |
| Timing | Every `validation_interval` (configurable validation interval — no value selected) | Until entitlement TTL expires or connectivity restored |
| Logged where | Platform AuditEvent (server-side) | ACCore local log; synced to platform on reconnect PROPOSED |
| Security risk | Requires connectivity | Revoked license may operate offline until TTL expires |

> [!WARNING]
> The offline tolerance window (entitlement TTL + grace period) is a **BLOCKER — UNKNOWN**. Too short → disrupts legitimate offline ACCore deployments. Too long → revoked licenses operate undetected. Requires business/security decision. See ADR-014.

---

## 5. Signed Entitlement Token Structure (PROPOSED)

```json
{
  "entitlement_id": "ent_uuid",
  "license_id": "lic_uuid",
  "institution_id": "inst_uuid",
  "product_code": "ACCORE",
  "units": ["FINANCE", "INVENTORY", "MARKETPLACE"],
  "seat_count": 50,
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "issued_at": "2026-01-01T00:00:00Z",
  "issuer": "accsystem.license",
  "grace_period_days": 7
}
```
*Signed with RS256 using platform License & Entitlement signing key. ACCore holds platform public key for offline verification.*

> [!NOTE]
> Token format (JWT vs custom signed JSON vs signed binary) is **PROPOSED**. JWT (RFC 7519) is recommended for ecosystem compatibility and existing library support.

---

## 6. Open Issues

| ID | Issue | Severity | Owner |
|---|---|---|---|
| LIC-001 | Offline tolerance window — entitlement TTL and grace period duration | HIGH | Business/Security |
| LIC-002 | License revocation propagation — how quickly must ACCore honor a revocation | HIGH | Business/Legal |
| LIC-003 | Seat overuse enforcement — block vs alert vs retroactive billing | MEDIUM | Business |
| LIC-004 | Entitlement token refresh strategy — how ACCore gets renewed token without manual admin action | MEDIUM | Architecture |
| LIC-005 | Key rotation — how platform public key rotation is propagated to ACCore instances | MEDIUM | Architecture/Security |
| LIC-006 | ACCommerce license model — not addressed (assumed free; see idea.md §12) | UNKNOWN | Business |
| LIC-007 | Multi-unit license — partial unit revocation behavior | UNKNOWN | Business |

---

## 7. License Identity and Ownership Glossary

> [!IMPORTANT]
> This glossary is **authoritative** for all license-related documents. Use these definitions consistently across components, functions, interface contracts, and events.

| Term | Definition | Identifier(s) |
|---|---|---|
| **Licensee / Beneficiary** | The party entitled to use the licensed software. For **institutional licenses** (this flow): the institution. For **marketplace licenses** (FN-LIC-ACTIVATE flow): the individual or institutional buyer. | `institution_id` (institutional) OR `buyer_id` (marketplace) |
| **Buyer** | The party who transacted the purchase. May differ from beneficiary in B2B scenarios. For marketplace flow: `buyer_id`. | `buyer_id` |
| **Publisher / Seller** | The institution that publishes the product to the marketplace and receives payment. This is **not** the license beneficiary. | `publisher_institution_id` (= `item.seller_id` in order context) |
| **Institution operating the installation** | The ACCore instance that runs the licensed software. For institutional licenses = Licensee. For marketplace licenses, the institution operating on behalf of a buyer is a separate concept (OPEN — not yet modelled). | `institution_id` |
| **Product** | The software product being licensed. | `product_id` (marketplace), `product_code` (institutional catalog) |
| **Installation** | A specific running instance of licensed software at an institution. | Not yet modelled — OPEN |
| **License** | The record of an entitlement grant. Contains: license_id, licensee identifier, product identifier, status, validity period. | `license_id` |
| **Entitlement** | The right to use a specific set of features/units/seats, bound to a license. May be represented as a signed token for offline use. | `entitlement_id`, signed token |

### Two Distinct License Workflows

| Dimension | Institutional License (this flow) | Marketplace Software License (FN-LIC-ACTIVATE) |
|---|---|---|
| **Trigger** | Admin action via ACManagement | Automatic — triggered by `OrderConfirmed` event |
| **Licensee identifier** | `institution_id` | `buyer_id` |
| **Product identifier** | `product_code` + `plan_id` | `product_id` (marketplace listing) |
| **Publisher/Seller** | Platform itself (ACCSystem as publisher) | An institution's published product |
| **Initial state** | ISSUED → ACTIVATED → ACTIVE | Directly ACTIVE |
| **Seat/unit model** | Yes — `seat_count`, `units[]` | UNKNOWN (idea.md §12 — open decision) |
| **Offline token** | Long-lived entitlement (months — ADR-014) | Short-lived (TTL UNKNOWN — ADR-014) |
| **Validation query** | `institution_id + product_code` | `buyer_id + product_id` or `license_id` |

> [!NOTE]
> These are **separate, explicitly identified workflows** — not variations of the same lifecycle. The identifier sets (`institution_id + product_code` vs `buyer_id + product_id`) must not be conflated. If a future requirement needs a unified query across both flows, it must be explicitly designed, not assumed.
