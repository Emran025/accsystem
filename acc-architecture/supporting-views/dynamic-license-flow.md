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
- Authorized platform admin or institution-scoped admin acts within approved role, institution scope and issuance/request approval policy; exact role matrix remains OPEN
- Target product and license plan are defined in License & Entitlement catalog
- ACCore backend is operational

**Postconditions (success):**
- Institutional license advances ISSUED → ACTIVATED → ACTIVE when the applicable delivery, acknowledgment and operation conditions are met
- Signed entitlement token reaches ACCore through a separate license-owned issuance/delivery operation; its approved interface, channel, receiver and acknowledgement remain OPEN
- ACCore validates entitlement and enables licensed modules/features
- LicenseIssued + LicenseActivated events on Event Bus (audit trail)

---

## 2. License Activation Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
  participant ADM as ACManagement Admin / (Management Console)
  participant AGW as API Gateway / (ACCSystem)
  participant PA as Platform Administration / and Support
  participant LE as License and Entitlement / Management
  participant IA as Identity and Access
  participant BUS as Event Bus
  participant IGW as Integration Gateway
  participant ACC as ACCore / License Connector + Backend
  participant AUD as Audit and Observability

    Note over ADM,AUD: PHASE 1 - LICENSE REQUEST CREATION

    ADM->>AGW: Submit authenticated admin request, license fields illustrative, token format and MFA claim policy OPEN
    AGW->>AGW: Validate token/session and extract verified identity context, no authorization decision
    AGW->>PA: Forward authenticated LicenseRequest and identity context
    PA->>IA: Resolve role, membership and institution-scope data for this operation
    IA-->>PA: Role / membership data only, no central ALLOW/DENY verdict
    PA->>PA: Apply target workflow / approval policy (role matrix and approval rules OPEN)
    PA->>LE: CreateLicense after workflow authorization (fields and contract OPEN)

    Note over LE,BUS: PHASE 2 - LICENSE RECORD CREATION AND SIGNING

    LE->>LE: Validate institution eligibility and plan constraints
    LE->>LE: Create License record / (license_id, institution_id, product_code, plan_id, / seat_count, units[], valid_from, valid_until, status: ISSUED)
    LE->>LE: Arrange recoverable separate token signing work (format OPEN)
    LE->>BUS: publish LicenseIssued via durable event path
    BUS->>AUD: consume LicenseIssued to write AuditEvent
    LE-->>PA: LicenseCreated(license_id, status ISSUED)
    PA-->>AGW: Receipt under approved contract
    AGW-->>ADM: License issued, token readiness is separate

    Note over IGW,ACC: PHASE 3 - INSTITUTIONAL SIGNING AND DELIVERY
    alt Signing succeeds and delivery is acknowledged
        LE->>LE: Sign institutional scoped entitlement (token format, algorithm and key policy OPEN)
        LE->>IGW: Proposed signed-entitlement delivery via Integration, interface/channel OPEN
        IGW->>ACC: Logical delivery direction only, receiving component/channel/ACK OPEN
        ACC->>ACC: Candidate checks for signature, scope and credential bounds, approved contract OPEN
        ACC->>ACC: Store validated token locally if selected implementation requires it
        ACC-->>IGW: Candidate receipt, ACK meaning and durable responsibility OPEN
        IGW->>LE: Forward receipt only if selected by the approved contract
        LE->>LE: Advance ISSUED to ACTIVATED only after approved contract-valid receipt and policy conditions
        LE->>BUS: Publish LicenseActivated at approved transition
        BUS->>AUD: Audit activation
        ACC->>ACC: Begin authorized licensed operation
        LE->>LE: Advance ACTIVATED to ACTIVE under lifecycle policy
    else Signing or delivery unavailable / uncertain
        LE->>LE: Retain recoverable pending work, retry/reconcile under policy
        Note over LE,ACC: No token readiness or activation is inferred from a missing result
    end

    Note over LE,ACC: PROPOSED logical delivery. Receiver, interface, ACK, retry ownership, activation correlation and wire schema remain OPEN.
    Note over IGW,ACC: ADR-015 transport-initiation baseline: ACCore outbound for firewalled institutions, with polling, long-polling or a persistent channel as candidate mechanisms. Protected inbound remains optional.
    Note over LE,ACC: Arrows show the logical token path, not network initiation. This does not reuse read-only IF-ACC-LICENSE-VALIDATE or register a new delivery IF.

    Note over ADM,AUD: PHASE 4A - ONLINE PERIODIC VALIDATION

    loop Every validation_interval (configurable, no value selected)
        ACC->>ACC: Check if validation_interval elapsed
        ACC->>IGW: POST /v1/licenses/validate (TLS, service auth) / (institution_id, product_code, module_codes, seat_count, / installation_id, correlation_id)
        IGW->>LE: Validate institutional scope and requested usage (read-only)
        LE->>LE: Check license status (ACTIVE / SUSPENDED / REVOKED / EXPIRED)
        LE->>LE: Check seat/usage against limits
        
        alt License ACTIVE and within limits
            LE-->>IGW: status ACTIVE and entitlement (validity, modules, limits)
            IGW-->>ACC: ACTIVE plus entitlement, evaluation is distinct
            ACC->>ACC: Update local validation cache (last_validated_at = now)
            ACC->>ACC: Continue normal operation
        else License SUSPENDED or REVOKED
            LE-->>IGW: ValidationResult(status: SUSPENDED  or  REVOKED, reason)
            IGW-->>ACC: ValidationResult(status)
            ACC->>ACC: Restrict licensed features for known suspension/revocation, expiry grace is a separate policy
            Note over LE,BUS: Read-only validation returns status and optional telemetry, lifecycle-owned transitions publish LicenseSuspended or LicenseRevoked once per idempotent transition
            BUS->>AUD: AuditEvent
        else License EXPIRED
            LE-->>IGW: ValidationResult(status: EXPIRED)
            IGW-->>ACC: ValidationResult(EXPIRED, renewal_url)
            ACC->>ACC: Restrict unless applicable grace is approved, alert admin
        else Usage exceeds limits (seat overuse)
            LE-->>IGW: Capacity exceeded diagnostic/error (mapping OPEN)
            IGW-->>ACC: Capacity result, do not conflate ACTIVE with within limits
            ACC->>ACC: Refuse additional unapproved activations, apply any approved broader overage policy and alert admin
        end
        
        LE->>BUS: Optional validation telemetry, if approved, no lifecycle transition event
        BUS->>AUD: AuditEvent (validation result logged)
    end

    Note over ACC,LE: PHASE 4B - OFFLINE VALIDATION (when ACCSystem unreachable)

    alt ACCSystem unreachable during validation check
        ACC->>ACC: Attempt online validation to timeout/connection failure
        ACC->>ACC: Fall back to local signed entitlement token
        ACC->>ACC: Verify signature using an approved algorithm and trust anchor, algorithm and key distribution UNKNOWN, RS256 not selected
        ACC->>ACC: Check scoped identity, authenticated grant validity and credential expiry separately
        ACC->>ACC: If locally observed suspension or revocation applies, restrict, unseen revocations remain an offline limitation
        
        alt Entitlement still within validity window
            ACC->>ACC: Continue operation (offline mode - CONFIRMED per idea.md §4.2, §4.3)
            ACC->>ACC: Log offline validation event locally
            Note over ACC: Offline period bounded by entitlement TTL and grace period (UNKNOWN)
        else Entitlement expired and cannot reach platform
            ACC->>ACC: Restrict unless an applicable grace policy is approved
            ACC->>ACC: Alert institution admin - connectivity required for license renewal
            Note over ACC: Specific offline tolerance window is UNKNOWN - requires business decision
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
| ACTIVE | ACTIVATED | EXPIRED | Status timing relative to validity end and approved grace is OPEN |
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
| Coverage | Status, seat count, usage and unit list per contract | Signature, workflow/identity, grant validity and credential expiry; current revocation may be unavailable offline |
| Timing | Every `validation_interval` (configurable validation interval — no value selected) | Credential and grant bounds, observed revocation and approved applicable grace constrain offline use |
| Logged where | Platform AuditEvent (server-side) | ACCore local log; synced to platform on reconnect PROPOSED |
| Security risk | Requires connectivity | Revocation may be unseen offline, subject to credential/grant bounds and approved policy |

> [!WARNING]
> The offline tolerance window (entitlement TTL + grace period) is a **BLOCKER — UNKNOWN**. Too short → disrupts legitimate offline ACCore deployments. Too long → revoked licenses operate undetected. Requires business/security decision. See ADR-014.

---

## 5. Signed Entitlement Token Structure (PROPOSED)

```json
{
  "entitlement_id": "ent_uuid",
  "license_id": "lic_uuid",
  "workflow": "institutional",
  "institution_id": "inst_uuid",
  "product_code": "ACCORE",
  "units": ["FINANCE", "INVENTORY", "MARKETPLACE"],
  "seat_count": 50,
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "issued_at": "2026-01-01T00:00:00Z",
  "expires_at": "2026-01-02T00:00:00Z",
  "issuer": "accsystem.license",
  "grace_policy_ref": "policy-controlled"
}
```
*Illustrative claim values only: grant dates differ from credential issue/expiry; TTL, wire mapping, algorithm, key distribution and rotation require approval. Offline verification requires an approved trust anchor; its storage and update path are not selected.*

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
| LIC-006 | `validation/traceability-24-topics.md` records reported owner direction that ACCommerce is initially free; the original owner prompt is unavailable. Future monetization and access/entitlement model remain OPEN, distinct from purchased software licenses | UNKNOWN | Business |
| LIC-007 | Multi-unit license — partial unit revocation behavior | UNKNOWN | Business |

---

## 7. License Identity and Ownership Glossary

> [!IMPORTANT]
> This glossary is **authoritative** for all license-related documents. Use these definitions consistently across components, functions, interface contracts, and events.

| Term | Definition | Identifier(s) |
|---|---|---|
| **Licensee / Beneficiary** | Party entitled to use the software. Institutional flow is institution-scoped; marketplace record is buyer-scoped, but B2B beneficiary/delegation may differ and is OPEN. | `institution_id` (institutional); `buyer_id` identifies marketplace buyer, not an approved delegated-beneficiary mapping |
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
| **Product identifier** | `product_code` + `plan_id` | `product_id`; mapping to listing, seller product and software catalog identifiers is OPEN |
| **Publisher/Seller** | Platform itself (ACCSystem as publisher) | An institution's published product |
| **Initial state** | ISSUED → ACTIVATED → ACTIVE | Directly ACTIVE |
| **Seat/unit model** | Yes — `seat_count`, `units[]` | UNKNOWN (idea.md §12 — open decision) |
| **Offline token** | Policy-controlled credential TTL UNKNOWN; grant validity is separate | Policy-controlled credential TTL UNKNOWN; grant validity is separate |
| **Validation query** | `institution_id + product_code` | `buyer_id + product_id` or `license_id` |

> [!NOTE]
> These are **separate, explicitly identified workflows** — not variations of the same lifecycle. The identifier sets (`institution_id + product_code` vs `buyer_id + product_id`) must not be conflated. If a future requirement needs a unified query across both flows, it must be explicitly designed, not assumed.
