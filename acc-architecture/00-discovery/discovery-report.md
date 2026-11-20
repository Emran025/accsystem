# ACC Ecosystem — Stage 0: Discovery & Scale Screen

**Document ID:** DISC-001  
**Stage:** 0 — Discovery & Scale Screen  
**Status:** PASSED (Stage 0 Discovery complete)  
**Date:** 2026-11-15  
**Author:** stage01 (architecture assistant)  
**Source:** idea.md v1.1 — ACManagement & Licensing Extension (685 lines, fully read)

---

## 1. Source / Evidence Inventory

### 1.1 Files Reviewed

| File | Lines | Read Status | Notes |
|---|---|---|---|
| `idea.md` | 685 | REVIEWED IN PRIOR SOURCE CONTEXT; NOT BUNDLED IN THIS REPOSITORY | External primary source cited by section; independent re-verification requires the source artifact or an approved snapshot |
| `architecture-assistant/AGENT.md` | 38 | FULLY READ | Operating rules and depth contract |
| `architecture-assistant/OUTPUT-DEPTH-AND-AMPLIFIER.md` | 130 | FULLY READ | Authoring checklists |
| `architecture-assistant/examples/sample-system/registry/` | 6 JSON files | STRUCTURE CONFIRMED | Used as structural template only |

### 1.2 Confirmed vs. Assumed

- **CONFIRMED** items are reported as directly stated in the external `idea.md` source context and cited by section; because that source is not bundled here, they are not independently reproducible from this repository alone.
- **ASSUMPTION** items are reasonable inferences not explicitly stated in `idea.md`.  
- **PROPOSAL** items are architecture-assistant recommendations.  
- **UNKNOWN** items are gaps that could block design decisions.

---

## 2. System Identification

### 2.1 Internal Systems

| System ID | Name | Type | Description | Source |
|---|---|---|---|---|
| SYS-ACCSYSTEM | ACCSystem | Backend Platform | Central marketplace + Platform Management Control Plane. Contains Commerce, Integration, Fulfilment, and Platform Management domains. | idea.md §0, §2, §3 |
| SYS-ACCORE | ACCore | Per-Institution Platform | Per-institution ERP + marketplace client. Each institution operates an independent instance with its own backend and database. | idea.md §0, §2, §4 |
| SYS-ACCOMMERCE | ACCommerce | Mobile/Web Application | Individual-buyer shopping application. Clients Commerce Core in ACCSystem. | idea.md §0, §2.1 |
| SYS-ACMANAGEMENT | ACManagement | Web Application | Public portal (unauthenticated) + protected admin console. Fronts Platform Management Services in ACCSystem. | idea.md §2.1.1, §3.1.1 |
| SYS-ACCMARED-SUP | ACCMared Supervisor | Flutter Desktop App | Delivery supervisor desktop application. Manages delivery teams, tasks, and execution monitoring. | idea.md §2.1 |
| SYS-ACCMARED-COU | ACCMared Courier | Mobile Application | Courier/delivery-agent mobile app. Receives tasks, updates pickup/delivery status, provides proof of delivery. | idea.md §2.1 |

### 2.2 External Systems

| System ID | Name | Type | Owned By | Interaction Summary | Source |
|---|---|---|---|---|---|
| EXT-PAYMENT-PROVIDER | External Payment Provider(s) | Third-party Payment Service | External vendor(s) | Receives payment authorization/capture requests from Payment Orchestration domain; returns payment state via callbacks/webhooks. | idea.md §6.3, §3.1 |
| EXT-PACKAGE-CDN | Software Package CDN / Object Storage | Third-party CDN + Object Storage | External vendor(s) | Stores signed installation packages; serves download URLs to ACManagement via Software Catalog & Distribution. | idea.md §2.1.1, §10.2 |

### 2.3 ACCSystem Internal Domains / Bounded Contexts

The following logical domains were CONFIRMED in `idea.md §3.1`:

| Domain | Boundary | Key Services |
|---|---|---|
| Platform Access | API Gateway / BFF, Identity & Access, Institution Registry | Entry point; auth; tenant registry |
| Commerce Domain | Catalog & Publication, Search & Discovery, Offer/Price/Availability, Cart & Checkout, Order Management | Core marketplace commerce |
| Fulfilment Domains | Payment Orchestration, Delivery Management, Cancellation/Returns | Post-order fulfilment |
| Institution Integration | Integration Gateway, Publication/Sync Workers, Webhooks, Event Inbox/Outbox | ACCore ↔ ACCSystem bridge |
| Platform Management Domain | Software Catalog & Release Distribution, License & Entitlement Management, Platform Administration & Support | Backend for ACManagement |
| Shared Platform Infrastructure | Event Bus / Message Broker, Audit, Logs, Metrics, Traces | Cross-cutting observability |
| Software Distribution | Object Storage / CDN, Signed packages, Checksums | Downstream of Platform Management |

---

## 3. Actor Identification

| Actor ID | Name | Category | Systems Used | Trust Level | Source |
|---|---|---|---|---|---|
| ACT-INDIVIDUAL | Individual Buyer | End user | ACCommerce | Authenticated (platform account) | idea.md §1.1 |
| ACT-INST-EMPLOYEE | Institution Employee / Seller | Institution staff | ACCore (Commerce Workspace, Product Master) | Authenticated (institution + platform account) | idea.md §4.1 |
| ACT-INST-ADMIN | Institution Administrator | Institution staff | ACCore (Organization & Users module), ACManagement (license scope) | Authenticated; elevated within institution | idea.md §2.1 |
| ACT-PLATFORM-ADMIN | Platform Administrator | Platform operator | ACManagement (Protected Console), ACCSystem Platform Admin services | Authenticated; privileged; MFA required | idea.md §9, §7.7 |
| ACT-SUPPORT-STAFF | Platform Support Staff | Platform operator | ACManagement (Protected Console), ACCSystem Support sessions | Authenticated; just-in-time scoped access | idea.md §9, §7.7 |
| ACT-DELIVERY-SUPERVISOR | Delivery Supervisor | Operations | ACCMared Supervisor (desktop) | Authenticated | idea.md §2.1 |
| ACT-COURIER | Courier / Delivery Agent | Operations | ACCMared Courier (mobile) | Authenticated | idea.md §2.1 |
| ACT-VISITOR | Public Portal Visitor | Anonymous | ACManagement (Public Portal only) | Unauthenticated | idea.md §2.1 |

---

## 4. Integration Boundaries

### 4.1 ACCore ↔ ACCSystem

- **Protocol:** TLS + service-to-service authentication (OAuth 2.0 Client Credentials or equivalent). CONFIRMED: idea.md §4.3.
- **Pattern (Outbound from ACCore):** Events via Outbox → Integration Gateway. Product publication, stock availability, reservation responses.
- **Pattern (Inbound to ACCore):** Reservation requests, order commands, license entitlements. If inbound connection to institution server not possible, outbound polling or secure message channel permitted.
- **Idempotency:** Outbox / Inbox pattern mandatory. CONFIRMED: idea.md §4.1, §6.5.

### 4.2 ACCSystem ↔ Payment Providers

- **Protocol:** Adapter per provider. Webhooks for async callbacks with signature verification and replay protection. CONFIRMED: idea.md §9.
- **Data:** No sensitive card data stored in ACCSystem. Tokenization / Hosted Checkout preferred. CONFIRMED: idea.md §9.

### 4.3 ACCSystem ↔ Software Package CDN

- **Pattern:** Platform Management domain stores release metadata; ملفات الحزم hosted in Object Storage/CDN. ACManagement exposes public download links; signed/time-limited URLs for secure assets. CONFIRMED: idea.md §2.1.1, §10.2.

### 4.4 ACManagement ↔ ACCSystem

- **Pattern:** ACManagement is a frontend client; all backend logic lives in Platform Management services within ACCSystem. No direct database access. CONFIRMED: idea.md §3.1.1.

### 4.5 ACCMared ↔ ACCSystem

- **Pattern:** ACCMared apps are clients of Delivery Management domain in ACCSystem. Fulfilment domain dispatches to ACCMared; courier updates flow back. CONFIRMED: idea.md §2, context diagram.

---

## 5. Ownership Boundaries

| Concern | Owner System | Non-Owner Clarification |
|---|---|---|
| Product definition (master) | ACCore (seller institution) | ACCSystem holds a published/projection copy only |
| Inventory (actual stock) | ACCore (seller institution) | ACCSystem holds an indicative availability snapshot |
| Operational ERP (accounting, HR, procurement) | ACCore (each institution) | ACCSystem does not replicate ERP data |
| Central order record | ACCSystem — Order Domain | ACCore receives a reference/event for local sales recording |
| Payment transaction record | ACCSystem — Payment Domain (+ payment provider) | Card data never stored in ACCSystem |
| Delivery shipment record | ACCSystem — Delivery Domain | ACCMared apps are UI clients; they do not own delivery data |
| License & entitlement record | ACCSystem — License & Entitlement Management | ACCore validates against this authoritative record |
| Software release metadata | ACCSystem — Software Catalog & Distribution | Installation files in EXT-PACKAGE-CDN |
| Platform user accounts & roles | ACCSystem — Identity & Access | ACManagement orchestrates workflows; does not own identity data |
| Institution employee records & local ERP roles | ACCore (each institution) | ACManagement does not manage these |

---

## 6. Complexity Signals

### 6.1 Distributed Transactions

**Signal level: HIGH.** The core purchase flow (Reservation → Payment → Order Confirm → Stock Deduction → Shipment) crosses ACCore, ACCSystem Payment Domain, ACCSystem Order Domain, and ACCSystem Delivery Domain. There is no single ACID transaction spanning these. CONFIRMED in idea.md §7.1–§7.5.

- Saga / Compensation pattern required: idea.md §7.4–§7.5 describes partial failure handling and cancellation steps.
- Outbox/Inbox mandatory to prevent lost-event scenarios: idea.md §6.5.
- Idempotency keys mandatory for all commands: idea.md §6.5.

### 6.2 Multi-Tenant Isolation

**Signal level: HIGH.** Each institution operates an independent ACCore instance with its own database. Tenant isolation must be enforced at every ACCSystem API call (tenant_id validated from token, not from client-supplied header). CONFIRMED: idea.md §4.2, §9.

Risk: Cross-institution data leakage through Catalog (listings must carry institution scoping), Order routing (must verify seller_id matches listing), and ACManagement admin operations (must scope to authorized institution).

### 6.3 Async Event Mesh

**Signal level: HIGH.** At least 20 distinct business event types are defined (idea.md §6.3), flowing across Commerce, Integration, Payment, Delivery, Platform Management, and License domains. Event ordering for some flows (e.g., order state machine) requires partition keys (order_id, seller_order_id). Dead-Letter Queues and retry policies are mandatory.

### 6.4 Licensing Subsystem

**Signal level: MEDIUM-HIGH.** License & Entitlement Management issues, activates, renews, suspends, revokes, and expires licenses. ACCore must validate against this service at activation and periodically. Offline validation via signed short-lived entitlement token is proposed (idea.md §4.3). License model details are an OPEN DECISION (idea.md §12).

### 6.5 Delivery Operations

**Signal level: MEDIUM.** ACCMared Supervisor (Flutter Desktop) and ACCMared Courier (mobile) are operational clients of Delivery Domain. Real-time task assignment, status updates, and proof of delivery are required. Whether ACCMared covers only the platform's own fleet or also integrates external logistics providers is an OPEN DECISION (idea.md §12).

### 6.6 Software Release Distribution

**Signal level: MEDIUM.** Signed packages with SHA-256 checksums, versioned release channels, secure download URLs, and package integrity verification before publish. CDN integration required for large file distribution.

---

## 7. Contradiction Log

| ID | Description | Location in idea.md | Impact | Status |
|---|---|---|---|---|
| CONTRA-001 | idea.md §13 names 6 implementation phases, but Phase 1 includes ACManagement, License & Entitlement, and Platform Admin baseline alongside marketplace foundation. This is a wide Phase 1 scope that may conflict with typical MVP sequencing. | §13 | Medium — phase scoping must be validated against team capacity; may cause Phase 1 to be too large. | OPEN |
| CONTRA-002 | idea.md §2.1 says "institution administrator" can use ACManagement "وفق نطاق الترخيص" (according to license scope), implying institution admins have some ACManagement access. §3.1.1 and §9 clarify that ACManagement manages ACCSystem-level accounts and does not manage local ACCore employees. The boundary between "institution admin accessing licensing in ACManagement" vs. "institution admin in ACCore" needs sharper definition. | §2.1, §3.1.1 | Low-Medium — requires explicit trust-level and permission scoping for ACT-INST-ADMIN in ACManagement. | OPEN |
| CONTRA-003 | idea.md §10.3 header is numbered "10.3" but appears as a sub-section under "10.2 Database Rules" in the document structure (uses ##### heading). Minor formatting inconsistency; no semantic conflict. | §10.3 | None | NOTED |
| GAP-001 | No SLA targets or availability percentage are stated in idea.md for any service. | Entire document | Blocks NFR definition — marked UNKNOWN in requirements. | OPEN |
| GAP-002 | No data residency, regulatory jurisdiction, or compliance framework (PCI-DSS, GDPR, local data protection laws) is mentioned. | Entire document | Potential HIGH risk for payment data and cross-border personal data. | OPEN |
| GAP-003 | ACCMared: unclear whether the fleet is platform-owned or whether external logistics providers are also integrated. | §12 | Affects Delivery Domain design and interface contracts. | OPEN DECISION |
| GAP-004 | Settlement / commission model for the platform as an intermediary is not specified. | §12 | Blocks Financial Domain design if platform takes a cut from transactions. | OPEN DECISION |
| GAP-005 | Multi-currency and tax model not defined. | §12 | Blocks pricing and checkout domain design for multi-jurisdiction deployment. | OPEN DECISION |
| GAP-006 | ACCommerce subscription / consumer licensing model not defined. | §12 | Whether individual buyers need any license or just a free account is unresolved. | OPEN DECISION |

---

## 8. Facts, Assumptions, Proposals, Unknowns

### 8.1 Facts (CONFIRMED from idea.md)

| ID | Fact | Section |
|---|---|---|
| FACT-001 | ACCSystem is the central marketplace and shared services platform; not a per-institution ERP. | §0, §3 |
| FACT-002 | Each institution operates an independent ACCore instance with its own backend and database. | §1.2, §4.2 |
| FACT-003 | ACCommerce and ACCore's Commerce Workspace are both clients of the same Commerce Core in ACCSystem. | §1.1, §2.2 |
| FACT-004 | ACCSystem stores a published/projected copy of product data; ACCore owns the master. | §5, §5.1 |
| FACT-005 | Outbox/Inbox pattern and idempotency are mandatory. | §6.5 |
| FACT-006 | No cross-institution direct database access is permitted; integration is via API and events only. | §1.2, §4.2 |
| FACT-007 | ACManagement is a frontend client of Platform Management Services inside ACCSystem; it does not own backend data. | §3.1.1 |
| FACT-008 | License & Entitlement Management is separate from Identity & Access; a license does not equal a user permission and vice versa. | §3.1.1, §9 |
| FACT-009 | Payment data: card-sensitive data must not be stored in ACCSystem; use tokenization/hosted checkout. | §9 |
| FACT-010 | Delivery management (shipment, assignment, tracking) is owned by Delivery Domain in ACCSystem; ACCMared apps are UI clients. | §2, §8 (ADR-008) |
| FACT-011 | Software release files are stored in Object Storage / CDN (EXT-PACKAGE-CDN); ACCSystem stores release metadata only. | §2.1.1, §10.2 |
| FACT-012 | ACCSystem stores an order snapshot (price, description, currency, quantity) at order confirmation; it must not rely on current product state to interpret historical orders. | §8.3 |
| FACT-013 | Platform admin accounts and support sessions require MFA, least-privilege, approval/delegation, time-limited scope, and full audit trail. | §9, §7.7 |
| FACT-014 | Reservation at ACCore seller must precede payment authorization; if reservation fails, checkout halts without payment capture. | §7.2 |
| FACT-015 | Correlation IDs must flow end-to-end from client through all domains and messages. | §11 |
| FACT-016 | ACCore can operate in limited offline mode; must cache integration messages and replay on reconnect. | §4.2 |

### 8.2 Assumptions (Not explicitly in idea.md)

| ID | Assumption | Rationale | Owner / Trigger |
|---|---|---|---|
| ASSUM-001 | Deployment target is cloud-hosted (containers/Kubernetes or equivalent managed container platform). | idea.md §10.1 describes containerized services and CDN; no on-premise-only constraint stated. | OWNER_UNASSIGNED — confirm with project owner before infrastructure design |
| ASSUM-002 | Arabic is the primary language for the product UI; API layer will be English-identifier with Arabic content fields. | Document is entirely in Arabic; "language: Arabic" is in registry. | OWNER_UNASSIGNED — confirm locale strategy before API schema design |
| ASSUM-003 | A single primary payment provider will be supported at MVP; multi-provider support is in Phase 6. | idea.md §13 (Phase 3: "one payment provider"); Phase 6 adds more. | Revisit at Phase 3 completion |
| ASSUM-004 | All ACCore instances are logically separate but may share physical infrastructure managed by the platform operator. | idea.md §4.2 allows "dedicated hosting environment" but does not mandate fully separate infrastructure. | Confirm per institution contract |
| ASSUM-005 | ACManagement Protected Console enforces row-level scoping so that an Institution Admin can only see their institution's license records, not other institutions'. | idea.md §2.1.1 implies ACManagement manages ACCSystem-level accounts and licenses but does not explicitly define row-level filtering rules. | OWNER_UNASSIGNED — clarify before ACManagement access control design |
| ASSUM-006 | Mared (supervisor + courier) operates only on the platform's own delivery fleet at MVP; external logistics provider integration is deferred. | idea.md §12 identifies this as an open decision; safest MVP assumption is platform-only fleet. | Revisit at Phase 4 |

### 8.3 Proposals (Architecture-assistant recommendations)

| ID | Proposal | Confidence | Rationale |
|---|---|---|---|
| PROP-001 | Adopt Saga (choreography-based for async flows, orchestration-based for multi-step payment+reservation) for distributed transactions. | MEDIUM | idea.md §7.5 describes partial failure handling and compensation; Saga is the standard pattern. No technology selected yet. |
| PROP-002 | Use PostgreSQL as the primary relational store per domain service, with domain-scoped schemas at minimum, separate databases as target. | LOW | Standard for domain-isolated data ownership; technology not stated in idea.md. |
| PROP-003 | Use a managed message broker (e.g., Apache Kafka or cloud-managed equivalent) for the event bus. | LOW | idea.md §3.1 references "Event Bus / Message Broker" and "DLQ / retry policies"; technology not specified. |
| PROP-004 | Implement event envelope versioning from day 1; use schema registry to manage evolution of the 20+ event types. | MEDIUM-HIGH | idea.md §6.4 defines a standard envelope; evolution strategy not stated but critical given the event count. |
| PROP-005 | Modular monolith for ACCSystem in Phase 0–2, with selective extraction of Payment and Integration domains to independent deployable services by Phase 3. | MEDIUM | See §12 Architecture Style Decision in scope document. Revisit after Phase 2 operational evidence. |

### 8.4 Unknowns (Gaps that could block design)

| ID | Unknown | Consequence if Unresolved | Responsible Owner | Revisit Trigger |
|---|---|---|---|---|
| UNKN-001 | SLA / availability targets for each domain. | Cannot define NFRs with units; cannot design for redundancy or circuit breaker thresholds. | Product owner | Before C2 container design |
| UNKN-002 | Data residency and compliance framework (PCI-DSS, GDPR, local regulations). | Payment domain design, personal data handling, and audit log retention all depend on this. | Legal / compliance owner | Before Payment Domain design |
| UNKN-003 | License model details: license type granularity (per institution / per installation / per module / per seat / capacity-based), renewal cycle, grace period duration. | Blocks License & Entitlement data model and ACCore validation logic. | Product owner | Before Phase 1 implementation |
| UNKN-004 | ACCMared delivery scope: platform-only fleet vs. external logistics provider integration. | Affects Delivery Domain interface contracts and shipment assignment logic. | Product owner | Before Phase 4 |
| UNKN-005 | Settlement / commission model for platform transactions. | Affects Payment and potentially a Financial/Settlement domain that may need to be added. | Business / finance owner | Before Phase 3 |
| UNKN-006 | Multi-currency and tax/VAT model. | Blocks checkout pricing, order snapshot schema, and reconciliation logic. | Business / finance owner | Before Phase 2 checkout design |
| UNKN-007 | ACCommerce individual-user monetization model (free app, subscription, freemium). | Affects identity model and whether individual users require entitlement checks. | Product owner | Before Phase 2 |
| UNKN-008 | Support access policy for ACCSystem: per-session consent from institution or pre-authorized delegation; maximum session duration and data masking rules. | Affects Platform Administration & Support service design and audit schema. | Security / policy owner | Before Phase 1 platform admin implementation |
| UNKN-009 | Offline validation strategy for licenses: signed short-lived token or mandatory periodic connectivity; grace period duration. | Affects ACCore license connector design and risk of service-disruption due to connectivity. | Product / security owner | Before Phase 1 licensing implementation |
| UNKN-010 | Expected transaction volumes and peak concurrency per domain (checkout/s, orders/day, messages/s). | Cannot size infrastructure, define rate limits, or validate scalability approach. | Product / DevOps owner | Before capacity planning |

---

## 9. Scope Partition

### 9.1 In-Scope

| Item | Reason |
|---|---|
| ACCSystem platform (all domains) | Focal system; central platform. |
| ACCore (per-institution ERP) | Focal system; primary data source; integration partner. |
| ACCommerce (individual shopping app) | Direct commerce client; in-scope for integration. |
| ACManagement (public portal + admin console) | In-scope; explicitly defined in idea.md. |
| ACCMared Supervisor (Flutter desktop) | Delivery operations client; in-scope. |
| ACCMared Courier (mobile) | Delivery operations client; in-scope. |
| Payment integration interface | Interface contract to external providers; in-scope. |
| Software distribution interface | Interface contract to CDN; in-scope. |
| Multi-tenant isolation architecture | Core architectural constraint. |
| License & Entitlement system | Explicitly scoped in idea.md v1.1. |
| Event bus / message mesh | Cross-cutting infrastructure. |
| Audit & observability | Cross-cutting; mandatory per idea.md §11. |

### 9.2 Out-of-Scope (architecture documentation)

| Item | Reason |
|---|---|
| Internal business logic of ACCore institution-specific modules | Each institution may customize; not platform-owned. |
| Payment provider internal implementation | Third-party; interface contract only. |
| CDN / Object Storage internal implementation | Third-party; interface contract only. |
| Mapping / geo services (if used by delivery) | Not mentioned in idea.md; defer. |
| Consumer-facing analytics / recommendation engine | Mentioned as future addition in Search; deferred. |
| Settlement / commission financial domain | OPEN DECISION; not modeled in this stage. |

### 9.3 External (documented as interface only)

- EXT-PAYMENT-PROVIDER: Payment authorization, capture, refund, reconciliation webhooks.  
- EXT-PACKAGE-CDN: Signed package storage, download URL generation.

### 9.4 Deferred

| Item | Phase |
|---|---|
| Multi-provider payment support | Phase 6 |
| External logistics provider integration | Phase 4 or 6 (pending UNKN-004) |
| Returns & disputes as a full capability | Phase 6 |
| Settlement / commission domain | Phase 6 |
| Multi-currency / multi-jurisdiction tax | Phase 5–6 (pending UNKN-006) |
| Advanced search recommendations | Phase 6 |

---

## 10. Key Constraints Extracted from idea.md

| Constraint ID | Constraint | Source |
|---|---|---|
| CON-001 | No shared database between institutions; each ACCore has its own isolated database. | idea.md §1.2, §4.2 |
| CON-002 | No direct database access between ACCSystem services or between ACCSystem and ACCore; all integration via APIs or events. | idea.md §1.2, §3.2, §4.2 |
| CON-003 | Outbox/Inbox pattern and idempotency keys are mandatory for all commands and events that may be retried. | idea.md §6.5 |
| CON-004 | Payment card-sensitive data must not be stored in ACCSystem; tokenization or hosted checkout required. | idea.md §9 |
| CON-005 | Tenant ID must be validated from the authentication token; must not be accepted from client-supplied payload without verification. | idea.md §9 |
| CON-006 | ACManagement must not bypass Identity & Access; it is a client of platform services, not a replacement. | idea.md §3.1.1 |
| CON-007 | License entitlement and user permissions are orthogonal; a license does not grant user permissions and vice versa. | idea.md §9, §3.1.1 |
| CON-008 | Support access to institution data requires explicit consent or delegation, is scoped to purpose and duration, and must be fully audited. | idea.md §9, §7.7 |
| CON-009 | Published events are immutable; corrections must be issued as new events or compensating events. | idea.md §6.5 |
| CON-010 | Software package files must have SHA-256 checksums and digital signatures verified before publish; download links must be HTTPS; signed/time-limited URLs for secure downloads. | idea.md §9, §7.7 |
| CON-011 | ACCSystem must not expose an administrative API through the public (visitor-facing) portal routes. | idea.md §9 |
| CON-012 | Each service/domain must be independently deployable and scalable without requiring full platform deployment. | idea.md §3.2 |

---

## 11. Architecture Style Preliminary Signal

This is a preliminary signal; the full analysis is in the Strategy section of `scope-and-requirements.md`.

The architecture described in idea.md uses explicit bounded-context language, prescribes independent data stores per domain, requires independent deployment and scaling per service (CON-012), and lists 13+ named domains. This signals that **coarse-grained services or microservices** are the intended approach, not a modular monolith.

However, the document also cautions against fragmentation (idea.md §3.2 alert box: "do not fragment every small function into a separate service without cause"). A **pragmatic coarse-grained services** approach (5–8 independently deployable services at ACCSystem level, with internal modules within each service) is proposed for the initial build, with selective further decomposition driven by independent scaling needs. This is recorded as PROPOSED with MEDIUM confidence pending stakeholder confirmation and team topology review.

---

## 12. Diagram Selection Preliminary Signal

| View | Disposition | Rationale |
|---|---|---|
| System Landscape (C1-L) | SELECTED | Multiple systems; essential overview. |
| System Context per focal system (C1-C) | SELECTED for SYS-ACCSYSTEM, SYS-ACCORE | Two focal systems per brief. Other systems: documented at C1 level. |
| Container (C2) | SELECTED for SYS-ACCSYSTEM | High complexity; 13+ domains. ACCore C2 also selected (8 modules). |
| Component (C3) | SELECTED for high-risk ACCSystem containers (Order, Payment, License, Integration) | High business risk; distributed transaction coordination. |
| Code (C4) | NOT SELECTED | No implementation language confirmed; would be speculative. |
| Dynamic view | SELECTED — Purchase saga, License issuance, Software release flows | Three high-risk distributed flows. |
| Deployment view | SELECTED | Multi-layer deployment described in idea.md §10.1. |

Full rationale in `scope-and-requirements.md § Diagram Selection Plan`.

---

## 13. Discovery Summary

The ACC Ecosystem is a **multi-system, multi-tenant, event-driven commerce and platform management ecosystem** comprising 6 internal systems, 2 external service integrations, 8 actor types, and approximately 13 named bounded contexts within ACCSystem alone.

**Key complexity drivers:** distributed transaction coordination (Reservation → Payment → Order saga), per-institution database isolation, async event mesh with 20+ event types, licensing subsystem with offline validation requirement, and a software distribution pipeline with signed package integrity requirements.

**Critical open decisions** (from idea.md §12) that must be resolved before C2/C3 implementation: license model granularity (UNKN-003), ACCMared delivery scope (UNKN-004), settlement/commission model (UNKN-005), multi-currency/tax model (UNKN-006), SLA/availability targets (UNKN-001), and compliance framework (UNKN-002).

---

*Discovery stage complete. Outputs feed Stage 1 (Scope & Strategy) and Stage 2 (C1 Context).*


## Remediation disposition (2026-11-19)

Historical discovery assumptions are retained as history. Current authoritative decisions are: multi-seller carts are required in MVP; ACCore connectivity defaults to an outbound connector; ACCore is inventory source of truth; timeout/lost response is UNKNOWN; payment capture supports controlled seller/agreement modes; and provider, legal, tax, retention, residency, and operational numeric values remain external/configurable gates. See ADR-015, ADR-016, ADR-017 and validation/traceability-24-topics.md.
