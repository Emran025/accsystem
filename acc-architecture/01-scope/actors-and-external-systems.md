# Actors and External Systems Reference

**Document:** `01-scope/actors-and-external-systems.md`
**System:** SYS-ACCECOSYSTEM — ACC Ecosystem
**Source:** `idea.md` §2, §2.1, §2.1.1, §9
**Status:** CONFIRMED from idea.md unless labeled otherwise
**Governance:** Every claim labeled CONFIRMED / ASSUMPTION / PROPOSAL / UNKNOWN

---

## 1. Human Actors

### ACT-INDIVIDUAL — Individual Buyer

| Field | Value |
|---|---|
| **ID** | ACT-INDIVIDUAL |
| **Name** | Individual Buyer / Consumer |
| **Trust Level** | Low — authenticated platform account; no institutional affiliation required |
| **Authentication Method** | Platform identity (SYS-ACCSYSTEM Identity & Access); short-lived session tokens (CONFIRMED — idea.md §9: "short-lived tokens, secure storage, session revocation, no service secrets embedded in mobile app") |
| **Systems Accessed** | SYS-ACCOMMERCE (primary UI); SYS-ACCSYSTEM Commerce Core (catalog, search, cart, checkout, orders, notifications) via ACCommerce |
| **Data Provided** | Account credentials, billing/shipping address, cart selections, payment initiation signal |
| **Data Received** | Product listings (market projection, not seller-internal data — CONFIRMED idea.md §5), order status, delivery tracking, notifications |
| **Sensitivity** | Medium — personal data (address, identity), payment reference tokens; raw card data never stored in platform (CONFIRMED idea.md §9) |
| **Security Controls** | Authenticated session, RBAC (Consumer role), TLS in transit (CONFIRMED idea.md §9), payment tokenization/hosted checkout (CONFIRMED idea.md §9), no raw card data stored |
| **Open Questions** | UNKNOWN: Whether ACCommerce requires email verification or supports social login. Consequence: identity assurance level for purchases is undefined. Owner: OWNER_UNASSIGNED. Revisit trigger: Identity & Access design spec finalized. |

---

### ACT-INST-EMPLOYEE — Institution Employee

| Field | Value |
|---|---|
| **ID** | ACT-INST-EMPLOYEE |
| **Name** | Institution Employee |
| **Trust Level** | Medium — authenticated within ACCore of their institution; ERP-level roles scoped to that institution |
| **Authentication Method** | ACCore institution-local identity; institution-scoped roles and permissions (CONFIRMED idea.md §4.1 "Organization & Users module"); if unified marketplace identity is needed, linked to a platform membership without transferring local ERP permissions (CONFIRMED idea.md §2.1.1) |
| **Systems Accessed** | SYS-ACCORE (primary — ERP modules, Commerce Workspace, Platform Connector); SYS-ACCSYSTEM (indirectly via ACCore: catalog, orders) |
| **Data Provided** | Product master data, inventory events, publication requests, order confirmations/rejections, reservation responses |
| **Data Received** | Market order commands, reservation requests, publication status, notifications from ACCSystem |
| **Sensitivity** | High — institution's internal product, inventory, pricing, and financial data; must not be visible to other institutions (CONFIRMED idea.md §9, §13.1) |
| **Security Controls** | ACCore RBAC/ABAC (institution-scoped), no direct DB access from ACCSystem (CONFIRMED idea.md §1.2), Outbox/Inbox pattern for integration (CONFIRMED idea.md §4.1), tenant_id enforced per request (CONFIRMED idea.md §9) |
| **Open Questions** | UNKNOWN: Whether employees may directly access ACCSystem APIs independently of ACCore (bypassing the Platform Connector). Consequence: scope of platform identity linking is undefined. Owner: OWNER_UNASSIGNED. Revisit trigger: Identity & Access design finalized. |

---

### ACT-INST-ADMIN — Institution Administrator

| Field | Value |
|---|---|
| **ID** | ACT-INST-ADMIN |
| **Name** | Institution Administrator |
| **Trust Level** | Medium-High — elevated within their institution's ACCore; may hold platform-level membership for license management via ACManagement |
| **Authentication Method** | ACCore local identity (institution-scoped admin role); platform membership for ACManagement Protected Console where license scope applies (CONFIRMED idea.md §2.1.1) |
| **Systems Accessed** | SYS-ACCORE (full ERP admin); SYS-ACMANAGEMENT (Protected Console — license management, institution-level entitlement, user membership at platform level) |
| **Data Provided** | License activation/renewal requests, institution settings, publication policies, user membership requests |
| **Data Received** | License status, entitlement details, platform-level account states, software release metadata for download |
| **Sensitivity** | High — institution licensing data, entitlements, platform membership records |
| **Security Controls** | MFA for Protected Console (CONFIRMED idea.md §9: "MFA, least privilege, pre-approval, time-limited access for platform admin accounts"); RBAC scoped to institution; audit trail (CONFIRMED idea.md §9) |
| **Open Questions** | UNKNOWN: Exact boundary of what institution admin can manage in Protected Console vs. what requires ACT-PLATFORM-ADMIN approval. Consequence: least-privilege policy cannot be enforced until roles are designed. Owner: OWNER_UNASSIGNED. Revisit trigger: Platform Administration & Support role matrix defined. |

---

### ACT-PLATFORM-ADMIN — Platform Administrator

| Field | Value |
|---|---|
| **ID** | ACT-PLATFORM-ADMIN |
| **Name** | ACC Platform Administrator |
| **Trust Level** | High — privileged platform account; separate from institution accounts (CONFIRMED idea.md §9) |
| **Authentication Method** | ACCSystem Identity & Access; MFA mandatory; RBAC/ABAC with least-privilege principle; pre-approval required; time-limited privileged access (CONFIRMED idea.md §9, §7.7) |
| **Systems Accessed** | SYS-ACMANAGEMENT Protected Console (primary UI); SYS-ACCSYSTEM Platform Management domain (Platform Administration & Support, License & Entitlement, Software Catalog & Release Distribution) |
| **Data Provided** | License issuance/renewal commands, software release publications, user account management actions, role grant/revoke, support session authorization |
| **Data Received** | Full platform management data: license registry, platform user accounts, release catalog, audit logs, support session records |
| **Sensitivity** | Very High — privileged admin access; role grants, license control, audit events |
| **Security Controls** | MFA (CONFIRMED), RBAC/ABAC (CONFIRMED), least-privilege (CONFIRMED), secret rotation (CONFIRMED idea.md §9), pre-approval workflow (CONFIRMED idea.md §7.7), immutable audit trail (CONFIRMED idea.md §9), WAF + rate limiting on ACManagement entry point (CONFIRMED idea.md §9) |
| **Open Questions** | UNKNOWN: Whether platform admins have break-glass emergency access procedures. Consequence: incident response capability undefined. Owner: OWNER_UNASSIGNED. Revisit trigger: Platform Administration & Support design finalized. |

---

### ACT-SUPPORT-STAFF — Platform Support Staff

| Field | Value |
|---|---|
| **ID** | ACT-SUPPORT-STAFF |
| **Name** | ACC Platform Support Staff |
| **Trust Level** | Medium-High — platform-level account with scoped, temporary access; NOT permanently wide-access (CONFIRMED idea.md §7.7, §9) |
| **Authentication Method** | ACCSystem Identity & Access; support session must be explicitly granted, institution-scoped, purpose-bound, time-limited (CONFIRMED idea.md §7.7); MFA (CONFIRMED idea.md §9) |
| **Systems Accessed** | SYS-ACMANAGEMENT Protected Console (support workflows); SYS-ACCSYSTEM Platform Administration & Support service (session management, scoped access to institution data under explicit authorization) |
| **Data Provided** | Support session requests, resolution actions within authorized scope |
| **Data Received** | Scoped institution data only under explicit authorization; not general access to all institutions' data (CONFIRMED idea.md §7.7) |
| **Sensitivity** | High — access to customer institution data requires explicit consent/authorization per session |
| **Security Controls** | Just-in-Time Support Access (CONFIRMED idea.md §15 glossary), time-bound sessions (CONFIRMED), institution+purpose+duration scoped (CONFIRMED idea.md §7.7), full audit trail (CONFIRMED), SupportAccessGranted/Expired/Revoked events emitted (CONFIRMED idea.md §6.3) |
| **Open Questions** | UNKNOWN: Whether institution must explicitly consent per support session or can pre-authorize. Consequence: consent model and legal/compliance requirements unclear. Owner: OWNER_UNASSIGNED. Revisit trigger: Support access policy designed (idea.md §12 open decision). |

---

### ACT-DELIVERY-SUPERVISOR — Delivery Supervisor

| Field | Value |
|---|---|
| **ID** | ACT-DELIVERY-SUPERVISOR |
| **Name** | Delivery Operations Supervisor |
| **Trust Level** | Medium — platform-operational account; delivery domain only |
| **Authentication Method** | ACCSystem Identity & Access; platform role scoped to Delivery Management domain; short-lived tokens (CONFIRMED idea.md §9) |
| **Systems Accessed** | SYS-ACCMARED-SUP (Flutter desktop — primary UI); SYS-ACCSYSTEM Delivery Management (shipment dispatch, courier assignment, tracking, proof-of-delivery) |
| **Data Provided** | Delivery team assignments, task dispatch decisions, delivery status confirmations |
| **Data Received** | Shipment list, courier positions, delivery status events, proof-of-delivery records |
| **Sensitivity** | Medium — delivery operational data, courier assignment, shipment details; no payment card data, no institution ERP data |
| **Security Controls** | Authenticated platform account, delivery-scoped RBAC, short-lived tokens (CONFIRMED idea.md §9), TLS in transit (CONFIRMED) |
| **Open Questions** | UNKNOWN: Whether delivery supervisors belong to the platform or to contracted third-party delivery companies. Consequence: affects trust level, data isolation, and contractual access scope. Owner: OWNER_UNASSIGNED. Revisit trigger: Delivery model decision resolved (idea.md §12 open decision). |

---

### ACT-COURIER — Courier / Delivery Agent

| Field | Value |
|---|---|
| **ID** | ACT-COURIER |
| **Name** | Field Courier / Delivery Agent |
| **Trust Level** | Low-Medium — operational account; narrowly scoped to assigned delivery tasks |
| **Authentication Method** | ACCSystem Identity & Access; short-lived tokens (CONFIRMED idea.md §9: "short-lived tokens, secure storage, session revocation, no service secrets in mobile app") |
| **Systems Accessed** | SYS-ACCMARED-COU (mobile app — primary UI); SYS-ACCSYSTEM Delivery Management (task receive, status updates, proof-of-delivery submission) |
| **Data Provided** | Task acceptance/rejection, pickup/delivery status updates, proof-of-delivery (photo, signature, etc.) |
| **Data Received** | Assigned delivery tasks, shipment details, recipient contact (minimum necessary), delivery instructions |
| **Sensitivity** | Medium — recipient personal data (address, contact) for delivery; no payment data, no institution ERP data |
| **Security Controls** | Short-lived tokens (CONFIRMED), secure local storage, session revocation, TLS in transit (CONFIRMED idea.md §9), no service secrets embedded in mobile app (CONFIRMED idea.md §9) |
| **Open Questions** | UNKNOWN: Whether the courier app supports offline mode (task caching when connectivity is intermittent). Consequence: delivery operations in low-connectivity environments undefined. Owner: OWNER_UNASSIGNED. Revisit trigger: ACCMared Courier offline requirements specified. |

---

### ACT-VISITOR — Unauthenticated Visitor

| Field | Value |
|---|---|
| **ID** | ACT-VISITOR |
| **Name** | Unauthenticated Website Visitor |
| **Trust Level** | None — no authentication; public access only |
| **Authentication Method** | None — public portal requires no credentials (CONFIRMED idea.md §2.1.1: "public zone for visitors") |
| **Systems Accessed** | SYS-ACMANAGEMENT Public Portal only; SYS-ACCSYSTEM Software Catalog & Release Distribution public APIs (`/v1/public/software-products`, `/v1/public/downloads/{asset_id}` — CONFIRMED idea.md §6.2) |
| **Data Provided** | None (read-only browsing) |
| **Data Received** | ACC system descriptions, feature lists, release notes, version requirements, public download links; download links are HTTPS signed URLs (CONFIRMED idea.md §9) |
| **Sensitivity** | None — all data served to visitors is intentionally public |
| **Security Controls** | WAF + rate limiting on ACManagement public path (CONFIRMED idea.md §9: "apply WAF protection, rate limiting, login attempt logging"); public portal must not expose any admin API (CONFIRMED idea.md §9); file integrity via SHA-256 checksums and digital signatures (CONFIRMED idea.md §9) |
| **Open Questions** | UNKNOWN: Whether download links require any form of token/captcha to prevent bulk scraping. Consequence: CDN cost and bandwidth abuse risk. Owner: OWNER_UNASSIGNED. Revisit trigger: Software Distribution security policy finalized. |

---

## 2. External Systems

### EXT-PAYMENT-PROVIDER — External Payment Provider

| Field | Value |
|---|---|
| **ID** | EXT-PAYMENT-PROVIDER |
| **Name** | External Payment Provider(s) |
| **Trust Level** | External Trusted Service — integrated via documented adapter; not part of ACC Ecosystem |
| **Authentication Method** | Service-to-service: OAuth 2.0 Client Credentials or equivalent with rotatable secrets (CONFIRMED idea.md §9); webhook signature verification + replay protection (CONFIRMED idea.md §9) |
| **Systems Accessed** | SYS-ACCSYSTEM Payment Orchestration domain (outbound integration) |
| **Direction** | Bidirectional: ACCSystem calls provider APIs for authorization/capture/refund; provider calls ACCSystem webhooks for payment state callbacks |
| **Data Provided to Platform** | Payment authorization result, capture confirmation, refund status, reconciliation data |
| **Data Received from Platform** | Payment initiation requests, refund requests, transaction identifiers |
| **Sensitivity** | Very High — financial transaction data; raw card data must NEVER transit ACCSystem (CONFIRMED idea.md §9: tokenization/hosted checkout from provider) |
| **Security Controls** | Tokenization / Hosted Checkout (CONFIRMED idea.md §9); webhook signature + timing verification + replay protection (CONFIRMED idea.md §9); provider-side PCI-DSS compliance (ASSUMPTION — not stated in idea.md, standard for payment providers); Circuit Breaker (CONFIRMED idea.md §10.3) |
| **Open Questions** | UNKNOWN: Which specific payment providers are targeted (e.g., Stripe, Moyasar, Tap). Consequence: adapter implementation and regional compliance requirements undefined. Owner: OWNER_UNASSIGNED. Revisit trigger: Commercial/legal vendor selection completed. |

---

### EXT-PACKAGE-CDN — Software Package CDN / Object Storage

| Field | Value |
|---|---|
| **ID** | EXT-PACKAGE-CDN |
| **Name** | Software Package CDN / Object Storage |
| **Trust Level** | External Trusted Infrastructure — cloud object storage and CDN; not part of ACC Ecosystem business logic |
| **Authentication Method** | Service-to-service: signed URLs generated by SYS-ACCSYSTEM Software Catalog & Release Distribution; ACCSystem controls access via time-limited signed download links (CONFIRMED idea.md §2.1.1, §6.2, §9) |
| **Systems Accessed** | SYS-ACCSYSTEM Software Catalog & Release Distribution (asset publishing); SYS-ACMANAGEMENT Public Portal (download link presentation) |
| **Direction** | Platform → CDN for publishing; Visitor/Installer → CDN for downloading via signed HTTPS URLs |
| **Data Provided to Platform** | Download availability, CDN metadata |
| **Data Received from Platform** | Installer packages, release assets, checksums, digital signatures |
| **Sensitivity** | High — software packages must carry valid digital signatures and SHA-256 checksums; tampered packages could compromise installations (CONFIRMED idea.md §9: "digital signing, SHA-256 per release, HTTPS download links, pre-publish package checks") |
| **Security Controls** | Signed URLs (time-limited) for downloads (CONFIRMED idea.md §2.1.1); digital package signatures (CONFIRMED idea.md §9); SHA-256 checksums published per release (CONFIRMED idea.md §9); installation integrity verification before update (CONFIRMED idea.md §7.7) |
| **Open Questions** | UNKNOWN: Whether the CDN is a managed cloud service (e.g., AWS S3 + CloudFront) or self-hosted. Consequence: SLA, geographic availability, and compliance scope differ. Owner: OWNER_UNASSIGNED. Revisit trigger: Infrastructure provider selected. |

---

## 3. Summary Table

| ID | Name | Type | Trust Level | Primary System |
|---|---|---|---|---|
| ACT-INDIVIDUAL | Individual Buyer | Human Actor | Low (authenticated) | SYS-ACCOMMERCE |
| ACT-INST-EMPLOYEE | Institution Employee | Human Actor | Medium | SYS-ACCORE |
| ACT-INST-ADMIN | Institution Administrator | Human Actor | Medium-High | SYS-ACCORE + SYS-ACMANAGEMENT |
| ACT-PLATFORM-ADMIN | Platform Administrator | Human Actor | High | SYS-ACMANAGEMENT |
| ACT-SUPPORT-STAFF | Platform Support Staff | Human Actor | Medium-High (scoped) | SYS-ACMANAGEMENT |
| ACT-DELIVERY-SUPERVISOR | Delivery Supervisor | Human Actor | Medium | SYS-ACCMARED-SUP |
| ACT-COURIER | Courier / Delivery Agent | Human Actor | Low-Medium | SYS-ACCMARED-COU |
| ACT-VISITOR | Unauthenticated Visitor | Human Actor | None | SYS-ACMANAGEMENT (Public Portal) |
| EXT-PAYMENT-PROVIDER | External Payment Provider | External System | External Trusted | SYS-ACCSYSTEM (via adapter) |
| EXT-PACKAGE-CDN | Software Package CDN | External System | External Trusted | SYS-ACCSYSTEM (via signed URLs) |

---

*Last updated: generated from idea.md v1.1 (2026-11-15). All governance labels (CONFIRMED/ASSUMPTION/PROPOSAL/UNKNOWN) are defined per claim above.*
