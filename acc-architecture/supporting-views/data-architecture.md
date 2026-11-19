# ACC Ecosystem — Data Architecture View

**View type:** Data Architecture  
**Stage:** 6 — Supporting Views  
**Status:** PROPOSED  
**Source:** idea.md Sections 5, 6, 7, 8  
**Parent:** `acc-architecture/`

---

## 1. Purpose and Scope

This view documents the data entities, ownership boundaries, consistency models, cross-domain data flows, key identifier strategy, and retention/deletion policies for the ACC Ecosystem. It is the authoritative reference for understanding which system is the source of truth for each data class, what ACCSystem holds as a projection, and how data moves across domain boundaries.

> [!IMPORTANT]
> Per idea.md Section 5: "This section is the most important architectural contract in the system. Data ownership for every data type must be defined before services are written, or conflicting copies of inventory, orders, and products will emerge."

---

## 2. Data Entity Catalog

| Entity | Authority / Source of Truth | ACCSystem Projection | Access Rights | Lifecycle | Retention / Deletion |
|---|---|---|---|---|---|
| **Product** (Original Master) | ACCore at selling institution | None — original never copied | ACCore employees per institution roles | Created/updated by Product Master module; deleted by institution | UNKNOWN — institution policy |
| **Product Listing** (Published) | ACCSystem Catalog domain | IS the projection — `listing_id` owned by ACCSystem | Readable by all marketplace consumers; writable only by Integration Gateway on behalf of seller institution | Created on `ProductListingPublished`; deactivated on `ProductListingWithdrawn`; versioned | UNKNOWN — marketplace retention policy; archived on withdrawal |
| **Stock / Inventory** | ACCore Inventory & Warehousing | Availability snapshot (approximate/cached) in Offer/Price/Availability service | Institution-internal write; read-only snapshot exposed via Integration | Realtime at ACCore; snapshot updated on `StockAvailabilityChanged` | UNKNOWN |
| **Cart** | ACCSystem Cart & Checkout domain | Owned by ACCSystem | Buyer-scoped (individual or institution employee) | Temporary; TTL-based expiry; abandoned carts purged per policy | Controlled policy — owner and jurisdiction dependent; configure before production|
| **CheckoutSession** | ACCSystem Cart & Checkout domain | Owned by ACCSystem | Buyer-scoped; read-only to Order domain on conversion | Ephemeral; invalidated on reservation failure, payment failure, or order confirmation | Controlled policy — owner and jurisdiction dependent; configure before production|
| **ParentOrder** | ACCSystem Order Management domain | IS the canonical record | Buyer + relevant institution staff (scoped by `tenant_id` / order participation) | Created on order confirmation; state machine transitions logged immutably | Controlled retention policy; legal/compliance approval required; delete or anonymize PII only where policy permits |
| **SellerOrder** | ACCSystem Order Management domain | IS the record (sub-entity of ParentOrder) | Seller institution via Integration | Created on order split per seller; closed on fulfillment or cancellation | Same as ParentOrder |
| **OrderLine** | ACCSystem Order Management domain | IS the record; snapshot of price/product at confirmation time | Same as ParentOrder/SellerOrder | Immutable after confirmation per idea.md 8.3 — commercial snapshot | Same as ParentOrder |
| **Reservation** | ACCore at selling institution (authoritative decision) | ACCSystem holds request/response state only | Order domain (write); Integration Gateway (relay) | Created on `ReservationRequested`; expires on TTL or `ReservationAccepted/Rejected`; released on failure | Controlled policy — owner and jurisdiction dependent; configure before production|
| **PaymentAttempt** | ACCSystem Payment Orchestration domain | IS the record (references provider record) | Payment domain internal; Order domain reads status | Created on payment initiation; terminal on capture, void, or refund | Controlled policy — owner and jurisdiction dependent; configure before production|
| **Shipment** | ACCSystem Delivery Management domain | IS the record | Delivery domain internal; ACCMared Supervisor/Courier (operational); buyer (read-only status) | Created on `OrderConfirmed`; closed on `ShipmentDelivered` or cancellation | Controlled policy — owner and jurisdiction dependent; configure before production|
| **Institution** | ACCSystem Institution Registry | IS the central record (non-ERP data only: ID, status, integration config) | Platform admin (write); integration services (read) | Registered on onboarding; deactivated/archived on offboarding | UNKNOWN |
| **License** | ACCSystem License & Entitlement Management | IS the record; reference shared to ACCore via signed entitlement | Platform admin + License service (write); ACCore License Connector (read) | Issued → Activated → Renewed/Suspended/Revoked/Expired | Controlled policy — owner and jurisdiction dependent; configure before production|
| **Entitlement** | ACCSystem License & Entitlement Management | IS the record; signed credential issued to ACCore | ACCore License Connector (validate); License service (issue/revoke) | Derived from License; short-to-medium lived signed token; refresh on renewal | UNKNOWN — TTL embedded in signed token |
| **SoftwareRelease** | ACCSystem Software Catalog & Distribution | IS the record | Public read (metadata); Platform admin (write); CDN (asset storage) | Published → Active → Withdrawn; metadata retained after withdrawal | Controlled policy — owner and jurisdiction dependent; configure before production|
| **SupportSession** | ACCSystem Platform Administration & Support | IS the record | Support staff (time-limited scope); platform admin (audit); subject institution (audit view) | Created on approval; auto-expires per granted duration | Controlled policy — owner and jurisdiction dependent; configure before production|
| **PlatformUser** | ACCSystem Identity & Access | IS the record for platform-level identity | Identity & Access (write); Platform Administration & Support (workflow) | Active → Suspended → Reactivated; deleted per GDPR/policy | UNKNOWN — retain audit trail post-deletion |
| **AuditEvent** | ACCSystem Audit & Observability | IS the immutable record | Audit service (write); platform admin/support (read-only); legal/compliance | Created on sensitive operations; never modified | Controlled policy — owner and jurisdiction dependent; configure before production|

---

## 3. Data Ownership Table (from idea.md Section 5)

| Data Type | Source of Truth | ACCSystem Role | Update Rule |
|---|---|---|---|
| Original product data | ACCore (seller) | No copy — integration projection only | Seller publishes via outbox → Integration |
| Published product images/attributes | ACCore or institution media store | Marketplace media reference/copy of authorized fields | Only permitted fields published |
| Offer price | Seller institution | Price snapshot with `last_updated` timestamp | Re-verified before order confirmation |
| Actual inventory | ACCore (seller) | Approximate availability indicator with sync timestamp | Final reservation at source ACCore |
| Cart | ACCSystem | Owns cart | Linked to buyer identity; TTL-scoped |
| Commercial order | ACCSystem Order domain | Owns canonical record | State transitions only via documented events |
| Local sale record | ACCore (seller) | Integration reference/status only | ACCore records on agreed commit point |
| Local purchase record | ACCore (buyer) — B2B only | Integration reference/status only | ACCore buyer records on agreed commit point |
| Payment | ACCSystem Payment domain + provider record | Owns transaction metadata; no raw card data | Confirmed via callback/webhook + reconciliation |
| Shipment/delivery | ACCSystem Delivery domain | Owns operational record | Via fulfillment events + proof of delivery |
| Internal financial entries | ACCore (each institution) | No copy of ERP ledger | Produced by institution per document triggers |

### 3.1 Sovereignty Rules

**Data that NEVER leaves ACCore:**
- Internal ERP ledger entries and financial reconciliation
- Employee records, HR data, internal roles
- Full product master data beyond authorized listing fields
- Internal warehouse movements and stock adjustments
- Institution-internal purchase orders and supplier data
- ERP audit trails specific to institution operations

**Data shared as projection (ACCSystem holds a derived copy):**
- Authorized product listing fields (`listing_id` → `seller_product_id` → `platform_institution_id`)
- Availability indicator (not authoritative; re-verified before commit)
- Price snapshot (not authoritative; re-verified before commit)
- Reservation outcome (request/response relayed; decision at ACCore)
- Order status references (integration reference IDs for seller commit)

---

## 4. Cross-Domain Data Flows

### 4.1 Product Data Flow: ACCore → Integration → Catalog → Search

```
ACCore Product Master
  │  Employee modifies product, selects publishable fields
  │  → ACCore writes ProductListingPublished event to Outbox
  ▼
ACCore Outbox Worker (Connector)
  │  Reads event from local Outbox
  │  → HTTP POST to Integration Gateway (TLS, service auth)
  │    Payload: { institution_id, seller_product_id, version, listing_data }
  ▼
Integration Gateway (ACCSystem)
  │  Validates institution auth, schema, publishing policy
  │  → Delivers to Catalog & Publication service
  ▼
Catalog & Publication
  │  Creates/updates Product Listing record (listing_id assigned)
  │  → Publishes event to Event Bus: ProductListingPublished
  ▼
Search & Discovery
  │  Consumes ProductListingPublished event
  │  → Updates search index
  ▼
Integration Gateway
  │  Returns listing_id, version, status to ACCore
  │  → ACCore stores listing_id as marketplace reference
```

**Consistency:** Eventual — ACCore product master updated; listing projection may lag by seconds to minutes depending on event processing latency.

### 4.2 Order Data Flow: Order → Payment → Delivery

```
Order Domain (ACCSystem)
  │  Creates ParentOrder + SellerOrder records
  │  → Publishes ReservationRequested to Integration
  ▼
Integration Gateway → ACCore (seller)
  │  ACCore validates price + stock → creates Reservation
  │  → Returns ReservationAccepted (reservation_id, expiry) or ReservationRejected
  ▼
Order Domain
  │  On Accept: transitions to PendingPayment
  │  → Instructs Payment Orchestration to authorize
  ▼
Payment Orchestration → Payment Provider
  │  Authorization request
  │  → PaymentAuthorized or PaymentFailed
  ▼
Order Domain (on PaymentAuthorized)
  │  Transitions to Confirmed
  │  → Publishes OrderConfirmed to Event Bus
  │    Consumers: ACCore seller (commit sale), Payment (capture), Delivery (create shipment)
  ▼
ACCore (seller)
  │  Consumes OrderConfirmed
  │  → Commits stock deduction, records local sale at agreed point
  ▼
Payment Domain
  │  Captures payment
  │  → Publishes PaymentCaptured
  ▼
Delivery Domain
  │  Creates Shipment on OrderConfirmed
  │  → Assigns courier, dispatches
  │  → Publishes ShipmentCreated / ShipmentDelivered
  ▼
Order Domain
  │  Aggregates delivery + payment events
  │  → Updates ParentOrder status to Dispatched → Delivered → Completed
```

**Consistency:** Saga-based eventual consistency — each step idempotent, compensating transactions defined for failure paths (see Section 7.5 of idea.md and Resilience View).

---

## 5. Consistency Model per Domain

| Domain | Consistency Model | Rationale |
|---|---|---|
| ACCore (each instance) | Strong (local ACID transactions) | ERP operations require ACID; institution owns its DB |
| Catalog & Publication | Eventual | Acceptable for search/browse; staleness tolerable |
| Search & Discovery | Eventual (derived index) | Search index rebuilt from events; can re-index |
| Offer / Price / Availability | Eventual (snapshot) + Strong at reservation | Snapshot for display; source verified at checkout |
| Cart & Checkout | Strong (session-scoped) | Cart consistency within session required |
| Order Management | Strong for state transitions (saga coordinator) | Order state machine transitions must be atomic; saga handles cross-domain |
| Payment Orchestration | Strong (payment ledger) + Eventual (reconciliation) | Payment records ACID; reconciliation eventual |
| Delivery Management | Eventual (event-driven) | Delivery status updates are event-driven |
| Integration Gateway | At-least-once with idempotency | Outbox/Inbox guarantees delivery; duplicates handled by idempotency keys |
| License & Entitlement | Strong (license issuance) + Eventual (validation cache) | License records authoritative; local validation cache with bounded staleness |
| Platform Administration | Strong (access control decisions) | Access grants/revocations must be consistent |

---

## 6. Key Identifiers Map (idea.md Section 5.2)

| Identifier | Owner | Scope | Usage |
|---|---|---|---|
| `platform_institution_id` | ACCSystem Institution Registry | Platform-wide | Identifies institution in all platform records, messages, and APIs; propagated as `tenant_id` |
| `seller_product_id` | ACCore (seller institution) | Per institution | ACCore's internal product ID; carried in listing records for traceability back to source |
| `listing_id` | ACCSystem Catalog domain | Platform-wide | Marketplace listing identifier assigned by ACCSystem on first publication |
| `order_id` | ACCSystem Order Management | Platform-wide | Canonical order identifier for ParentOrder |
| `seller_order_id` | ACCSystem Order Management | Platform-wide | SellerOrder identifier (sub-order per seller) |
| `buyer_transaction_id` | ACCore (buyer institution) | Per institution | B2B buyer's internal purchase record reference; carried in order integration messages |
| `reservation_id` | ACCore (seller) | Per reservation | ACCore-assigned; carried back in `ReservationAccepted` response |
| `payment_id` | ACCSystem Payment domain | Platform-wide | Internal payment attempt identifier |
| `provider_payment_ref` | External Payment Provider | External | Provider's transaction reference; stored in PaymentAttempt for reconciliation |
| `shipment_id` | ACCSystem Delivery domain | Platform-wide | Shipment record identifier |
| `license_id` | ACCSystem License & Entitlement | Platform-wide | License record identifier |
| `entitlement_id` | ACCSystem License & Entitlement | Platform-wide | Signed entitlement token identifier |
| `event_id` | Producing service | Platform-wide | UUID per event; used for idempotency at consumer |
| `correlation_id` | Originating client/service | Platform-wide | Propagated through entire flow — from ACCommerce/ACCore → all downstream; required per idea.md §11 |
| `causation_id` | Producing service | Platform-wide | ID of the event/request that caused this event; enables causal chain reconstruction |
| `idempotency_key` | Calling client | Per operation | Stable key for safe retry; stored by consumers to detect duplicates |

---

## 7. Data Sovereignty

### 7.1 Data That Never Leaves ACCore (per idea.md §1.2, §4.2, §5)

- Internal ERP accounting entries, general ledger
- Employee profiles, HR records, payroll
- Internal product master attributes beyond marketplace-authorized fields
- Raw inventory movements, warehouse operations
- Institution-internal business rules and pricing logic
- Local audit trails for ERP operations
- Supplier contracts and procurement records

### 7.2 Data Shared as Projection to ACCSystem

The following data crosses from ACCore to ACCSystem via Integration Gateway, as a **projected copy only**:
- Authorized product listing fields (name, description, images, category, price, availability indicator)
- Stock availability change signal (not authoritative count)
- Reservation outcome (accept/reject decision + reservation_id)
- Order status confirmations (commit acknowledgment)

> [!WARNING]
> ACCSystem must NEVER make business decisions based on projected inventory counts without a confirmed reservation from ACCore. The catalog availability indicator is for display only. Per idea.md §5: "The availability shown in the ACCSystem catalog does not constitute a reservation guarantee."

### 7.3 Data That Never Flows to ACCore from ACCSystem

- Other institutions' product master data
- Other institutions' order or financial data
- Platform-level admin configuration beyond the institution's own entitlements
- Raw payment card data (never stored anywhere in the system)

---

## 8. Retention and Deletion Policy

> [!NOTE]
> Specific retention targets are **UNKNOWN** in idea.md. The values below are **PROPOSED** defaults requiring legal/compliance stakeholder approval before implementation.

| Data Class | Proposed Retention | Deletion Trigger | PII Handling |
|---|---|---|---|
| AuditEvent | 7 years PROPOSED | Manual archival after retention period | Minimize PII in audit payloads; anonymize where possible |
| PaymentAttempt | 7 years PROPOSED | Retention period expiry | PCI-DSS requirements apply; no raw card data stored |
| ParentOrder / SellerOrder / OrderLine | 7 years PROPOSED | Retention period expiry | PII in shipping address — anonymize post-completion |
| Cart / CheckoutSession | 30 days inactivity PROPOSED | TTL expiry | Purge fully on expiry |
| Reservation | 7 days post-resolution PROPOSED | Resolution + 7 days | No sensitive PII |
| Shipment | 3 years PROPOSED | Retention expiry | Delivery address is PII — anonymize post-delivery |
| License / Entitlement | 7 years post-expiry PROPOSED | Expiry + retention period | Institution data, low PII risk |
| SupportSession | 7 years PROPOSED | Retention period expiry | Audit requirement; scope and actor must be retained |
| PlatformUser | Retain audit trail post-deletion PROPOSED | Account closure | GDPR right-to-erasure applies to personal data; audit trail anonymized |
| SoftwareRelease (metadata) | Indefinite PROPOSED | Manual withdrawal (metadata retained) | No PII |
| SoftwareRelease (binaries) | Per CDN/storage policy UNKNOWN | CDN lifecycle rules | No PII |
| Search Index | Derived; rebuilt from events | On re-index; on listing withdrawal | Derived data only |

**BLOCKER:** Retention/deletion targets require legal, compliance, and finance stakeholder sign-off before implementation. Mark all PROPOSED values as UNRESOLVED.

---

## 9. Data Classification

| Classification | Examples | Controls |
|---|---|---|
| **PUBLIC** | Published product listings, software release metadata, software download links | Available without authentication |
| **BUYER-SCOPED** | Cart contents, order status, delivery tracking for buyer | Auth required; `user_id` or `institution_id` scope enforced |
| **INSTITUTION-SCOPED** | Seller order details, reservation responses, institution listing management | `tenant_id` / `institution_id` check mandatory on every request |
| **PLATFORM-INTERNAL** | Payment attempt records, audit events, support session records | Restricted to authorized platform services and admin roles |
| **HIGHLY SENSITIVE** | Payment provider tokens, service credentials, signing keys | Secret management system; never in application code or logs |

---

## 10. Open Issues / Blockers

| ID | Issue | Severity | Owner | Action |
|---|---|---|---|---|
| DA-001 | Retention/deletion periods for all entity classes | HIGH | Legal/Compliance | Define before data layer implementation |
| DA-002 | GDPR/PDPA compliance scope — which jurisdictions apply | HIGH | Legal | Determine before launch |
| DA-003 | PII fields in OrderLine commercial snapshot — anonymization strategy | MEDIUM | Privacy/Engineering | Define anonymization policy post-completion |
| DA-004 | ACCore DB backup strategy — RPO per institution | UNKNOWN | Architecture/Infra | Define per institution SLA |
| DA-005 | B2B buyer ACCore integration — which events trigger purchase record creation | MEDIUM | Business/Architecture | Define commit point rules |
| DA-006 | Multi-currency data model — currency fields on price snapshots | UNKNOWN | Business/Architecture | Define before cross-border commerce |
