# ACC Ecosystem — Security View

**View type:** Security Architecture  
**Stage:** 6 — Supporting Views  
**Status:** PROPOSED  
**Source:** idea.md Sections 9, 7.7, 4.3, 6  
**Parent:** `acc-architecture/`

> [!IMPORTANT]
> Controls are labelled: **CONFIRMED** (stated in idea.md), **PROPOSED** (recommended, not stated), **UNKNOWN** (not addressed in idea.md).

---

## 1. Threat Model Overview

### 1.1 Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│ INTERNET (untrusted zone)                                           │
│  Unauthenticated visitors, bots, scrapers, malicious actors        │
│                              │                                       │
│                          WAF + Rate Limiting                        │
│                              │                                       │
├──────────────────────────────▼──────────────────────────────────────┤
│ PUBLIC EDGE (semi-trusted — rate-limited, monitored)               │
│  ACManagement Public Portal, software download endpoints           │
│                              │                                       │
│                       API Gateway / BFF                             │
│            (token authentication / routing; not authorization)      │
│                              │                                       │
├──────────────────────────────▼──────────────────────────────────────┤
│ AUTHENTICATED CLIENT ZONE                                           │
│  ACCommerce users, ACCore institutional users, ACCMared operators  │
│                              │                                       │
│           JWT / OAuth 2.0 token validation at gateway              │
│                              │                                       │
├──────────────────────────────▼──────────────────────────────────────┤
│ ACCSystem APPLICATION LAYER (private zone)                         │
│  Domain services: Commerce, Integration, Payment, Delivery,        │
│  Identity, Catalog, Licensing, Platform Admin                      │
│          │ service-to-service (mTLS / OAuth 2.0 CC)               │
├──────────▼──────────────────────────────────────────────────────────┤
│ ACCSystem DATA LAYER (private/restricted)                          │
│  Domain DBs, Event Bus, Object Storage, Search Index               │
├─────────────────────────────────────────────────────────────────────┤
│ INSTITUTION ZONE (external trusted peer)                           │
│  ACCore per-institution — TLS + service credentials               │
│  → Integration Gateway as the ONLY entry point                     │
├─────────────────────────────────────────────────────────────────────┤
│ EXTERNAL PROVIDERS (external trusted peers, limited scope)         │
│  Payment Providers — webhook verification                          │
│  Software Package CDN — signed URLs                                │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Actor Types and Trust Levels

| Actor | Description | Trust Level | Authentication Mechanism |
|---|---|---|---|
| Unauthenticated visitor | Public web browsing, software catalog | Untrusted | None — WAF + rate limiting |
| Individual buyer | ACCommerce shopper | Low-trusted (authenticated) | OAuth 2.0 / OIDC + short-lived JWT |
| Institution employee | ACCore staff accessing marketplace | Medium-trusted (institution-scoped) | ACCore auth + institution binding; JWT with `institution_id` claim |
| Institution admin | Manages institution's marketplace listings, purchases | Medium-trusted | Same as institution employee; elevated role claim |
| Platform admin | ACCSystem operator — manages users, licenses, releases | High-trusted (privileged) | MFA mandatory; short-lived scoped tokens; RBAC |
| Support staff | Time-limited JIT access to institution data | High-trusted (time-limited, scoped) | MFA; JIT approval flow; scoped token with explicit expiry |
| ACCore service | Backend-to-backend integration | High-trusted (service) | ADR-015 policy-selected OAuth 2.0 Client Credentials or mTLS |
| Payment Provider | External webhook sender | External (signature-verified) | HMAC signature on webhook payload |
| CDN / Package Store | Software distribution | External (content integrity) | Signed URLs; SHA-256 checksum verification |

---

## 2. Authentication

### 2.1 Per-Actor Mechanism

| Actor | Mechanism | Standard | Evidence |
|---|---|---|---|
| Individual buyer | OAuth 2.0 Authorization Code + PKCE; short-lived JWT access token | OIDC / OAuth 2.0 | CONFIRMED — idea.md §9: "unified platform authentication" |
| Institution employee (ACCore-initiated) | ACCore authenticates locally; passes institution-scoped token or identity claim to ACCSystem | Institution-federated | CONFIRMED — idea.md §4.3: "TLS + service-to-service auth"; §9: "institution_id on every request" |
| Platform admin | MFA mandatory; privileged session with short TTL | MFA + RBAC | CONFIRMED — idea.md §9: "MFA, least-privilege, pre-approval, time-limited access" for admin accounts |
| Support staff | JIT approval workflow; time-limited scoped token | JIT access | CONFIRMED — idea.md §9 and §7.7: JIT support access with approval, time-limited, scoped, audited |
| ACCore service (S2S) | ADR-015 policy-selected OAuth 2.0 Client Credentials or mTLS with rotatable credentials/certificates | OAuth 2.0 CC or mTLS | CONFIRMED in principle — idea.md §9; selected method requires onboarding/security policy |
| Delivery operators (ACCMared) | Short-lived tokens; session revocation; no hardcoded service secrets in mobile app | OAuth 2.0 / OIDC | CONFIRMED — idea.md §9: "short-lived tokens, secure storage, session revocation, no service secrets in mobile app" |
| Payment Provider webhook | HMAC-SHA256 signature verification on every inbound webhook | Webhook signature | CONFIRMED — idea.md §9: "webhook signature verification and replay protection" |

### 2.2 Token Requirements (CONFIRMED from idea.md §9)

- Short-lived access tokens for all client-facing flows
- Secure storage for tokens in mobile apps (no plaintext local storage)
- Session revocation capability
- No service secrets embedded in client application bundles

---

## 3. Authorization

### 3.1 RBAC / ABAC Model

**CONFIRMED from idea.md §9:** "RBAC/ABAC — general roles with contextual conditions such as institution, branch, job function, and operation scope."

| Role Type | Scope | Example Permissions |
|---|---|---|
| Anonymous | Public | Browse catalog, view software releases, download public packages |
| Buyer | User-scoped | Create cart, checkout, view own orders |
| Institution employee | Institution-scoped (`institution_id`) | View institution's listings, view institution's orders |
| Institution seller admin | Institution-scoped | Publish/update/withdraw listings, manage institution's marketplace presence |
| ACCMared Supervisor | Delivery team-scoped | Manage delivery tasks, assign couriers |
| ACCMared Courier | Courier-scoped | View assigned tasks, update delivery status, record proof of delivery |
| Platform admin | Platform-wide | Manage platform users, issue/revoke licenses, manage software releases |
| Support staff (JIT) | Time-limited + institution-scoped | Read access to specified institution's order/account data within approved scope |
| Audit reviewer | Read-only | Access to audit event log |

### 3.2 Tenant Isolation Enforcement

**CONFIRMED from idea.md §9:** "tenant_id check on every request; do not rely on client-supplied value without verification from token and permission."

Implementation requirements:
1. `institution_id` / `tenant_id` extracted from verified JWT, never from request body/query string without token backing
2. Every domain service applies tenant filter before returning data
3. Cross-tenant data access is a **hard security boundary** — institution A cannot read institution B's operational data
4. Violation detection: anomalous cross-tenant access attempts logged and alerted (see Security Signals in observability)

### 3.3 License vs. Permission Separation

**CONFIRMED from idea.md §9, §3.1.1:**

> "Product entitlement (what the institution is licensed to run, in what capacity and duration) MUST be separated from user permissions (what a user is allowed to do). A product license does not automatically grant ACCSystem admin rights; a support role does not grant a product license."

| Dimension | System | Controls |
|---|---|---|
| What institution can RUN | License & Entitlement Management | License record → signed entitlement → ACCore validates |
| What USER can DO | Identity & Access | RBAC/ABAC role claims in JWT |
| These do not substitute each other | — | Enforced by separate services; no cross-dependency |

---

## 4. Secrets Management

| Requirement | Status | Detail |
|---|---|---|
| TLS on all service-to-service communication | CONFIRMED | idea.md §4.3: "TLS + service-to-service authentication" |
| TLS on ACCore ↔ Integration Gateway | CONFIRMED | idea.md §4.3 |
| No secrets in application code | CONFIRMED | idea.md §9: "encryption key management outside code" |
| Rotatable service credentials (ACCore S2S) | CONFIRMED | idea.md §9: "rotatable certificates/secrets" |
| Encryption at rest for sensitive data | CONFIRMED | idea.md §9: "TLS in transit; encryption of sensitive data at rest; key management outside code" |
| Secret management system (vault) | PROPOSED | External secret manager (e.g., HashiCorp Vault, cloud KMS) for service credentials, signing keys, DB passwords. OWNER: Infrastructure team |
| Key rotation schedule | UNKNOWN | Rotation frequency for signing keys, service credentials not defined in idea.md. OWNER: Security team |
| Certificate management | PROPOSED | Automated cert renewal for TLS; short-lived certs preferred for mTLS PROPOSED |

---

## 5. Payment Security

**CONFIRMED from idea.md §9:** "No storage of sensitive card data; use Tokenization/Hosted Checkout from provider where possible."

| Control | Status | Detail |
|---|---|---|
| No raw card data storage | CONFIRMED | Payment provider handles card data; ACCSystem stores only provider token and reference |
| Tokenization / Hosted Checkout | CONFIRMED | idea.md §9 — use provider's tokenization |
| PCI-DSS scope reduction | PROPOSED | By using hosted checkout / tokenization, ACCSystem aims to minimize PCI scope. Formal PCI-DSS assessment required. |
| Payment webhook signature verification | CONFIRMED | idea.md §9 — signature + replay protection |
| Payment webhook replay protection | CONFIRMED | idea.md §9 — timestamp check + nonce/event_id deduplication |
| Payment reconciliation | PROPOSED | Scheduled reconciliation between ACCSystem payment status and provider statement. Discrepancies alerted. |
| Refund authorization | PROPOSED | Refunds authorized only by Order domain with payment domain execution; dual-party check PROPOSED |

---

## 6. Webhook Security

**CONFIRMED from idea.md §9:** "Verify signature, timestamp, and prevent replay attacks."

Implementation requirements (PROPOSED detail):
1. Each incoming webhook validated with HMAC-SHA256 using provider-specific secret key
2. Timestamp header checked against a provider- and Security-approved replay tolerance; value UNKNOWN until calibrated
3. `event_id` checked against idempotency store — reject duplicates silently (return 200 to avoid retrigger)
4. Webhook endpoint not exposed publicly without authentication layer
5. Webhook processing failures logged to DLQ for investigation

---

## 7. Download Integrity

**CONFIRMED from idea.md §7.7, §9:**

| Control | Status | Detail |
|---|---|---|
| SHA-256 checksum per release | CONFIRMED | idea.md §7.7: "SHA-256 fingerprint published for each release" |
| Digital signature on packages | CONFIRMED | idea.md §7.7: "package signature; verify before install or update" |
| HTTPS download links only | CONFIRMED | idea.md §9: "HTTPS download links" |
| Signed URLs for downloads | CONFIRMED | idea.md §2.1.1: "signed URLs with time limits" |
| Pre-publication package scan | CONFIRMED | idea.md §9: "scan packages before publishing" |
| Filename/URL not proof of integrity | CONFIRMED | idea.md §9: "do not treat filename or download URL as evidence of integrity" |
| Checksum verification at install | PROPOSED | ACCore installation client must verify SHA-256 before applying package |

---

## 8. Support Access (JIT — Just-In-Time)

**CONFIRMED from idea.md §7.7, §9:**

| Attribute | Requirement | Status |
|---|---|---|
| Approval/authorization required | Support session requires explicit approval or delegated authorization from authorized party | CONFIRMED |
| Institution-scoped | Access limited to specified institution only | CONFIRMED |
| Purpose-scoped | Access limited to stated purpose (e.g., order investigation) — not broad data access | CONFIRMED |
| Time-limited | Session auto-expires at granted duration; no permanent support access | CONFIRMED |
| Fully audited | Who started it, what was accessed, when it ended — recorded in Audit Trail | CONFIRMED |
| MFA enforced for support staff | Support staff accounts require MFA | CONFIRMED |
| Least privilege | Minimum access rights for the stated purpose | CONFIRMED |
| No persistent elevated access | Support staff cannot retain elevated access after session expiry | CONFIRMED |
| Token scope enforcement | Support session token carries explicit `institution_id`, `purpose`, `expires_at` claims | PROPOSED |

---

## 9. Audit Trail

**CONFIRMED from idea.md §9:** "Tamper-resistant audit log for sensitive operations: publication, pricing, order, refund, courier assignment."

### 9.1 Events That Must Be Immutably Logged

| Event Category | Events | Sensitivity |
|---|---|---|
| Product operations | ProductListingPublished, ProductListingWithdrawn, ProductListingUpdated | PLATFORM-INTERNAL |
| Pricing | Price change events, Offer updates | PLATFORM-INTERNAL |
| Orders | OrderConfirmed, OrderCancelled, ReturnRequested | PLATFORM-INTERNAL |
| Payments | PaymentAuthorized, PaymentCaptured, PaymentFailed, Refund | HIGHLY SENSITIVE |
| Courier assignment | Shipment assigned to courier | PLATFORM-INTERNAL |
| License operations | LicenseIssued, LicenseActivated, LicenseRevoked, LicenseSuspended | PLATFORM-INTERNAL |
| Platform access | PlatformRoleGranted, PlatformRoleRevoked | HIGHLY SENSITIVE |
| Support sessions | SupportAccessGranted, SupportAccessExpired, SupportAccessRevoked | HIGHLY SENSITIVE |
| User account changes | PlatformUserActivated, PlatformUserSuspended | PLATFORM-INTERNAL |
| Auth events | Failed login attempts, MFA failures, token revocations | HIGHLY SENSITIVE |

### 9.2 Audit Log Access Controls

| Role | Access |
|---|---|
| Platform admin | Full read access to platform audit log |
| Support staff | Read access to audit events scoped to their active session institution only |
| Security/compliance | Read-only access per authorization |
| Domain services | Write-only (append-only) |
| No actor | Modify or delete audit events — immutability required |

### 9.3 Audit Log Immutability Strategy (PROPOSED)

- Append-only storage; no UPDATE or DELETE operations permitted
- Write-once storage backend PROPOSED (e.g., object storage with object lock, or immutable ledger service)
- Hash chaining or Merkle structure PROPOSED for tamper evidence
- Regular integrity verification scheduled PROPOSED

---

## 10. Residual Risks

| Risk ID | Description | Severity | Owner | Mitigation Status | Mitigation Trigger |
|---|---|---|---|---|---|
| SR-001 | ACCore institution compromise — malicious product publication or reservation manipulation | HIGH | Architecture/Security | PROPOSED — Integration Gateway validates schema + policy; anomaly detection PROPOSED | Before go-live |
| SR-002 | Insider threat — platform admin abusing broad access | HIGH | Security/Governance | PROPOSED — MFA, least privilege, all actions audited; dual-approval for critical operations PROPOSED | Before go-live |
| SR-003 | Payment webhook spoofing if signature key compromised | HIGH | Security/Payment | PROPOSED — Key rotation; monitoring for signature failures | Key rotation policy required |
| SR-004 | Cross-tenant data leakage via API bug | HIGH | Engineering/Security | PROPOSED — Mandatory `tenant_id` filter unit tests; penetration test before launch | Before production launch |
| SR-005 | Offline license validation bypass — forged signed entitlement | MEDIUM | Architecture/Security | PROPOSED — Strong signing key; short TTL on entitlement tokens; revocation propagation | Before licensing launch |
| SR-006 | Support staff accessing data beyond session scope | HIGH | Security/Governance | PROPOSED — JIT token scope enforcement; session scope logged; anomaly alerts | Before support access feature launch |
| SR-007 | Download integrity check skipped by ACCore client | MEDIUM | Product/Engineering | PROPOSED — Installation client must enforce checksum verification; cannot be bypassed | Before software distribution launch |
| SR-008 | DDoS on public software download endpoints | MEDIUM | Infrastructure/Security | PROPOSED — CDN + WAF + rate limiting; signed URL TTLs limit link sharing | Before public portal launch |
| SR-009 | Service credential rotation failure — stale credentials used | MEDIUM | Infrastructure/DevOps | PROPOSED — Automated rotation with rotation monitoring; alerts on near-expiry | Operational procedure |
| SR-010 | PCI-DSS scope underestimated if payment flow touches raw card data | HIGH | Finance/Legal/Engineering | UNKNOWN — Formal PCI assessment required; depends on provider integration model | Before payment launch |
| SR-011 | Audit log tampering by privileged DB access | HIGH | Security/Infrastructure | PROPOSED — Write-once storage; IAM separation of audit writes from admin DB access | Before go-live |
| SR-012 | GDPR/data privacy compliance — PII retention beyond legal basis | MEDIUM | Legal/Engineering | UNKNOWN — Retention policy and legal basis not defined in idea.md | Legal review required |

---

## 11. Security Controls Summary

| Control | Category | Status |
|---|---|---|
| Unified platform authentication (OAuth 2.0 / OIDC) | Authentication | CONFIRMED |
| MFA for platform admin and support staff | Authentication | CONFIRMED |
| Short-lived tokens; secure mobile storage | Authentication | CONFIRMED |
| Session revocation | Authentication | CONFIRMED |
| S2S OAuth 2.0 Client Credentials or mTLS with rotatable credentials/certificates | Authentication | CONFIRMED in principle; method selected by ADR-015 policy |
| RBAC/ABAC with contextual conditions | Authorization | CONFIRMED |
| `tenant_id` check on every request | Authorization | CONFIRMED |
| License ≠ Permission separation | Authorization | CONFIRMED |
| TLS in transit | Transport | CONFIRMED |
| Encryption at rest for sensitive data | Data | CONFIRMED |
| Key management outside application code | Secrets | CONFIRMED |
| No raw card data storage | Payment | CONFIRMED |
| Tokenization / Hosted Checkout | Payment | CONFIRMED |
| Webhook HMAC-SHA256 signature + replay protection | Integration | CONFIRMED |
| SHA-256 checksum + digital signature on packages | Distribution | CONFIRMED |
| Signed HTTPS download URLs | Distribution | CONFIRMED |
| JIT support access with approval, scope, time limit, audit | Support | CONFIRMED |
| Tamper-resistant audit log for sensitive operations | Audit | CONFIRMED |
| WAF + rate limiting on public endpoints | Edge | PROPOSED |
| Secret management system (vault) | Secrets | PROPOSED |
| Automated cert/key rotation | Secrets | PROPOSED |
| PCI-DSS formal assessment | Compliance | UNKNOWN |
| GDPR retention/deletion policy | Compliance | UNKNOWN |
| Penetration testing before launch | Testing | PROPOSED |
| Anomaly detection for cross-tenant access | Monitoring | PROPOSED |
