# ACC Ecosystem — Stage 1: Scope & Strategy

**Document ID:** SCOPE-001  
**Stage:** 1 — Scope & Strategy  
**Status:** PASSED (Stage 1 Scope complete)  
**Date:** 2026-11-15  
**Author:** stage01 (architecture assistant)  
**Sources:** idea.md (all 685 lines, fully read), DISC-001 (discovery-report.md)

---

## 1. Functional Requirements

> [!NOTE]
> Requirements are derived from idea.md. Each FR carries a stable ID, actor, trigger, normal path, alternate path, acceptance criteria, source section, and status.
> Status values: ACCEPTED-OWNER (explicit owner direction), DERIVED, ARCHITECTURAL-DEFAULT, CONFIGURABLE, DEFERRED, or EXTERNAL-GATE. Numeric commercial, legal, provider, and operational values are not invented.

---

### FR-001 — Product Publication by Institution

| Field | Value |
|---|---|
| **ID** | FR-001 |
| **Name** | Institution Product Publication to Marketplace |
| **Actor** | ACT-INST-EMPLOYEE (seller) via ACCore |
| **Trigger** | Employee selects fields to publish from Product Master and requests Publish Listing |
| **Normal Path** | 1. ACCore records publish event in local Outbox within the same DB transaction. 2. Platform Connector sends event to ACCSystem Integration Gateway (TLS, service auth). 3. Integration Gateway validates: institution eligibility, data schema, field policy. 4. Catalog & Publication creates or updates a Published Product / Listing record (listing_id assigned). 5. Search & Discovery index updated. 6. ACCSystem returns listing_id, version, and publication status to ACCore. |
| **Alternate Path** | A1 — Validation fails: ACCSystem returns structured error; ACCore records failure; employee corrected and retry. A2 — Integration Gateway temporarily unavailable: ACCore retains event in Outbox; Connector retries with exponential backoff and same idempotency key. |
| **Acceptance Criteria** | AC1: listing_id is returned on success. AC2: Published listing contains only the fields authorized by the institution's publish policy. AC3: Duplicate publish event with same idempotency key produces no duplicate listing record. AC4: Search index reflects published product within defined staleness window (target UNKNOWN — see UNKN-010). AC5: Failed publication generates a structured error with reason code returned to ACCore. |
| **Source** | idea.md §7.1 |
| **Status** | CONFIRMED |

---

### FR-002 — Individual Purchase Flow (B2C)

| Field | Value |
|---|---|
| **ID** | FR-002 |
| **Name** | Individual Buyer Purchase from Institution |
| **Actor** | ACT-INDIVIDUAL via ACCommerce |
| **Trigger** | Buyer initiates Checkout on a cart containing one or more marketplace listings |
| **Normal Path** | 1. ACCommerce sends checkout request to Commerce Core. 2. Cart & Checkout validates: buyer eligibility, item availability snapshot, price snapshot, delivery details. 3. Order Domain creates a ParentOrder and one SellerOrder per seller, then sends independent ReservationRequested commands to each seller ACCore via the logical connector contract. 4. Each seller ACCore validates current price and availability atomically, creates an expiring reservation, and responds with a reservation_id and expiry. 5. The saga waits for every required seller reservation. If a required reservation fails, checkout is blocked; eligible known holds may be released only after all relevant in-flight/UNKNOWN effects are reconciled and compensation is permitted and settled. No distributed atomic transaction is assumed. 6. Payment Domain requests authorization under the seller/agreement capture policy. 7. Payment Provider responds with a definitive result or UNKNOWN requiring reconciliation. 8. Order Domain confirms the ParentOrder and SellerOrders: creates Order record with immutable line snapshot (price, description, currency, quantity, seller name, delivery terms). Publishes OrderConfirmed. 9. Seller ACCore receives the seller-scoped OrderConfirmed, commits stock deduction and records the local sales transaction. 10. Payment Domain applies the configured capture/collection policy. 11. Delivery Domain creates one or more shipments and dispatches. 12. Order status and delivery updates flow to ACCommerce via Order/Notification APIs. |
| **Alternate Path** | A1 — Reservation rejected: Checkout halts, cart refreshed, buyer informed, no payment captured; eligible known effects are compensated only after relevant UNKNOWN peers are reconciled. A2 — Payment authorization is definitively declined: release only reservations confirmed accepted and eligible, after relevant payment/reservation effects are settled; record each result. A payment timeout enters PaymentUnknown and does not release until reconciled. A3 — ACCore unavailable after reservation sent: Retry reservation request with same idempotency key where safe; query only where the institution contract supports it, otherwise wait/escalate without repeating a possible effect. A4 — Payment authorization is confirmed but local confirmation fails: recovery queries payment and reservation states, then resumes or uses void/release/refund only after definitive evidence, eligibility, and a proven uncommitted/committed disposition; no blind compensation is assumed. A5 — Shipment creation fails: Order stays Confirmed with Pending Delivery status; Delivery Domain retries. |
| **Acceptance Criteria** | AC1: No payment is captured before ReservationAccepted. AC2: Duplicate checkout with same idempotency key does not produce duplicate order or payment. AC3: Order record contains immutable snapshot of price, quantity, seller, and delivery terms at time of confirmation. AC4: A confirmed ACCore hold expires only under the configured ACCore policy; a timeout or lost reservation response does not authorize release. Query/reconciliation or an agreed safe-expiry rule is required. AC5: Buyer receives order status updates through the notification flow. AC6: Correlation ID flows from checkout request through payment and delivery events. |
| **Source** | idea.md §7.2, §8 |
| **Status** | CONFIRMED |

---

### FR-003 — B2B Purchase Flow (Institution Buys from Institution)

| Field | Value |
|---|---|
| **ID** | FR-003 |
| **Name** | Institution-to-Institution Purchase |
| **Actor** | ACT-INST-EMPLOYEE (buyer) via ACCore Commerce Workspace |
| **Trigger** | Institution employee initiates checkout from ACCore's Commerce Workspace |
| **Normal Path** | Same reservation → payment → order confirmation flow as FR-002, initiated from ACCore Commerce Workspace. After order confirmation: seller ACCore receives a sales document/event linkable to its internal sales transaction; buyer ACCore receives a purchase document/event linkable to its internal purchase transaction. Financial records (invoices, payables) created in each ACCore only at the agreed accounting trigger point (e.g., order confirmed, shipped, or delivered — institution-defined). |
| **Alternate Path** | Same as FR-002 alternates. Additional: buyer ACCore unavailable — buyer purchase document is queued and replayed via Outbox. |
| **Acceptance Criteria** | AC1: Seller ACCore receives a seller_order_id linking to the central order. AC2: Buyer ACCore receives a buyer_transaction_id linking to the central order. AC3: Neither institution's internal financial record is created at Checkout time only; creation is tied to a defined commitment point. AC4: Cross-institution data isolation: buyer ACCore cannot read seller ACCore's ERP data, only the trade documents it is entitled to as a party to the order. |
| **Source** | idea.md §7.3 |
| **Status** | CONFIRMED |

---

### FR-004 — Delivery Dispatch and Tracking

| Field | Value |
|---|---|
| **ID** | FR-004 |
| **Name** | Delivery Dispatch, Assignment, Tracking, and Proof of Delivery |
| **Actor** | ACT-DELIVERY-SUPERVISOR (via ACCMared Supervisor), ACT-COURIER (via ACCMared Courier) |
| **Trigger** | OrderConfirmed event triggers Shipment creation in Delivery Domain |
| **Normal Path** | 1. Delivery Domain creates Shipment record. 2. Delivery Supervisor (ACCMared Supervisor) views and assigns Shipment to a Courier. 3. ACCMared Courier receives task. 4. Courier updates status (picked up, en-route, delivered) with proof (signature, photo, etc.). 5. ShipmentDelivered event published → Order Domain updates order status → Notifications sent to buyer. |
| **Alternate Path** | A1 — Courier unavailable: supervisor reassigns. A2 — Delivery fails: order moves to relevant failure state; return/compensation flow triggered. |
| **Acceptance Criteria** | AC1: Every applicable physical fulfillment is covered by one or more intended Shipment records, including supported split or multi-seller shipments; software-only orders need none. AC2: Duplicate ShipmentCreated events do not repeat the same intended shipment effect or suppress distinct shipments; grouping/cardinality requires Delivery/Product policy. AC3: Proof of delivery (type unspecified — UNKNOWN: define accepted proof types) is attached to Shipment record. AC4: Delivery status updates are reflected in Order status view for buyer. |
| **Source** | idea.md §3.1 (Delivery Management), §2 (ACCMared), §13 Phase 4 |
| **Status** | CONFIRMED |

---

### FR-005 — License Issuance and Validation

| Field | Value |
|---|---|
| **ID** | FR-005 |
| **Name** | Software License Issuance, Activation, and Validation |
| **Actor** | ACT-PLATFORM-ADMIN or authorized ACT-INST-ADMIN (via ACManagement Protected Console); ACCSystem License & Entitlement; ACCore License Connector |
| **Trigger** | Authorized admin requests license issuance or renewal for an institution/product; ACCore activates or periodically re-validates a licensed module |
| **Normal Path** | 1. Admin submits license request via ACManagement → Platform Management Services → License & Entitlement Management. 2. License & Entitlement validates institution eligibility and license plan. 3. Issues signed entitlement: contains product, modules, seats/capacity, validity period, license status. 4. LicenseIssued event published → ACCore License Connector receives → stores signed entitlement locally. 5. ACCore validates entitlement at module activation and periodically (online check or offline signed-token check). |
| **Alternate Path** | A1 — Validation fails (expired, suspended): ACCore module is restricted per grace-period policy (UNKN-009). A2 — License suspended by admin: LicenseSuspended event propagates to ACCore; module restricted. A3 — Connectivity unavailable during validation: ACCore validates against locally cached signed entitlement (if offline strategy adopted — UNKN-009 open). |
| **Acceptance Criteria** | AC1: Issued license entitlement is cryptographically signed. AC2: ACCore can validate entitlement without transmitting ERP data to ACCSystem. AC3: Revoked or suspended license results in module restriction within defined propagation window. AC4: License audit log records every issuance, activation, renewal, suspension, and revocation with actor, timestamp, institution, and product. AC5: License entitlement does not grant platform user permissions (orthogonal to Identity & Access). |
| **Source** | idea.md §7.7, §4.3, §9, §12 |
| **Status** | ACCEPTED-OWNER direction; plan attributes, prices, limits, and renewal policy are configurable |

---

### FR-006 — Platform Administration via ACManagement

| Field | Value |
|---|---|
| **ID** | FR-006 |
| **Name** | Platform User and Role Administration |
| **Actor** | ACT-PLATFORM-ADMIN, ACT-SUPPORT-STAFF (via ACManagement Protected Console) |
| **Trigger** | Admin initiates account management, role grant, support session, or user status change |
| **Normal Path** | 1. Admin authenticates to ACManagement Protected Console (MFA required). 2. Admin performs operation: activate/suspend/reactivate account, manage memberships, grant/revoke platform role, initiate time-limited support session. 3. ACManagement calls Platform Administration & Support service → orchestrates Identity & Access API. 4. PlatformRoleGranted / SupportAccessGranted event published → Audit Trail records event. |
| **Alternate Path** | A1 — Action requires approval: submitted for approval workflow; pending state shown. A2 — Support access to institution data: requires explicit consent or delegation from authorized institution party; scoped to institution, purpose, and time duration. |
| **Acceptance Criteria** | AC1: Every admin action generates an immutable audit event with actor, action, target, scope, and timestamp. AC2: Support session cannot exceed defined maximum duration or scope. AC3: Platform admin accounts are distinct from institution ERP accounts. AC4: Role grants require approval where policy mandates it. AC5: ACManagement does not directly read or write Identity & Access database; it orchestrates through published service API. |
| **Source** | idea.md §7.7, §9, §3.1.1 |
| **Status** | CONFIRMED |

---

### FR-007 — Software Release Publication and Download

| Field | Value |
|---|---|
| **ID** | FR-007 |
| **Name** | Software Release Publication and Secure Download |
| **Actor** | Product team (platform operator — actor not formally listed but implied); ACT-VISITOR or institution downloading software |
| **Trigger** | Product team publishes a new software version; visitor or institution requests download |
| **Normal Path** | 1. Product team submits release data to Software Catalog & Distribution: version, release channel, supported platforms, install requirements, release notes, SHA-256 checksum, package signature. 2. Installation files uploaded to EXT-PACKAGE-CDN. 3. Software Catalog stores metadata with reference to CDN asset. 4. SoftwareReleasePublished event emitted. 5. ACManagement Public Portal displays release information. 6. Visitor or institution requests download; ACManagement obtains download link from Software Catalog; link is HTTPS, optionally signed/time-limited for secure assets. 7. Downloader verifies SHA-256 and signature before installation. |
| **Alternate Path** | A1 — Release withdrawn: SoftwareReleaseWithdrawn event; download link disabled; release marked archived (not deleted). |
| **Acceptance Criteria** | AC1: Every release record contains version, channel, SHA-256 checksum, and digital signature reference. AC2: Download URLs are HTTPS; secure/restricted assets use signed, time-limited URLs. AC3: Package integrity check (checksum and signature) must be verifiable before the release is marked Available. AC4: Withdrawn release download links are invalidated; release history is preserved for audit. |
| **Source** | idea.md §7.7, §2.1.1, §9 |
| **Status** | CONFIRMED |

---

### FR-008 — Order Cancellation and Return

| Field | Value |
|---|---|
| **ID** | FR-008 |
| **Name** | Order Cancellation and Return Processing |
| **Actor** | ACT-INDIVIDUAL or ACT-INST-EMPLOYEE; Order Domain (automated compensation) |
| **Trigger** | Buyer or institution requests cancellation or return; cancellation eligibility check passes |
| **Normal Path** | 1. Cancellation requested (buyer or policy-triggered). 2. Order Domain checks eligibility (order state, cancellation policy). 3. Order Domain publishes OrderCancellationRequested event: – Reservation cancellation sent to seller ACCore. – Delivery Domain requested to stop/return shipment if dispatched. – Payment Domain initiates Void (pre-capture) or Refund (post-capture). 4. Each domain responds with its outcome (independent). 5. Partial outcomes are supported when one sub-step fails; release, void, or refund is performed only for eligible known effects after authoritative peer reconciliation and settled required compensation. 6. Order transitions to CancellationPending → Cancelled. |
| **Alternate Path** | A1 — Partial failure (e.g., delivery already with courier): Order remains in partial state; operations team alerted; manual resolution initiated. |
| **Acceptance Criteria** | AC1: Cancellation is recorded as an event and state transition; it is not a deletion. AC2: No payment is retained after a full cancellation unless policy specifies a cancellation fee (OPEN — not stated in idea.md). AC3: Partial compensation (refund without stock release, or stock released without refund) is detected and flagged for ops review. AC4: Return flow (ReturnPending → Returned) is a separate state path with its own compensation steps. |
| **Source** | idea.md §7.4, §7.5, §7.6 |
| **Status** | CONFIRMED (return/dispute details deferred to Phase 6) |

---

### FR-009 — Reservation + Payment Saga (Distributed Transaction Coordination)

| Field | Value |
|---|---|
| **ID** | FR-009 |
| **Name** | Reservation-Payment-Confirmation Distributed Saga |
| **Actor** | Order Domain (orchestrator); Payment Domain; ACCore Seller (via Integration) |
| **Trigger** | Checkout submitted; triggers Saga execution |
| **Normal Path** | Sequential steps: (1) Validate cart → (2) Send ReservationRequested → (3) Await ReservationAccepted/Rejected → (4) If accepted: request PaymentAuthorization → (5) Await PaymentAuthorized/Failed → (6) If authorized: publish OrderConfirmed → trigger stock commit, payment capture, shipment creation. |
| **Alternate Path** | Compensation: If step N fails after step N-1 succeeded, the saga records the per-effect outcome and performs only an eligible, policy-authorized compensation after all relevant UNKNOWN effects are reconciled. A captured payment requires a refund path rather than a void; an uncaptured authorization may be voided where supported. Order confirmation failure does not by itself prove that a possible payment effect is uncommitted. |
| **Acceptance Criteria** | AC1: Payment does not begin until every required seller reservation is definitively accepted. AC2: Stock commit and payment capture follow their separate configured state machines. AC3: Reservation timeout after dispatch produces UNKNOWN and does not authorize payment or release. AC4: Lost reservation acceptance and release responses are resolved by query/idempotency key without duplicate holds or unsafe releases. AC5: Payment timeout produces PaymentUnknown and no duplicate financial effect. AC6: Saga state survives restart and resumes idempotently. AC7: Operational timeout triggers escalation/reconciliation; compensation occurs only after the external state is definitive. AC8: Order, payment, reservation, capture, seller-credit, settlement, and outbox outcomes are audited. |
| **Source** | idea.md §7.2, §7.5, §6.5 |
| **Status** | CONFIRMED (saga implementation pattern PROPOSED) |

---

### FR-010 — Product Listing Update and Withdrawal

| Field | Value |
|---|---|
| **ID** | FR-010 |
| **Name** | Product Listing Update and Withdrawal |
| **Actor** | ACT-INST-EMPLOYEE via ACCore |
| **Trigger** | Employee modifies published product fields or withdraws listing |
| **Normal Path** | 1. ACCore updates product master; records ProductListingUpdated or ProductListingWithdrawn event in Outbox. 2. Connector sends event to Integration Gateway. 3. Catalog & Publication updates listing version or marks withdrawn. 4. Search index updated. |
| **Alternate Path** | A1 — Active orders reference withdrawn listing: Order records retain immutable snapshot; listing withdrawal does not affect in-flight orders. |
| **Acceptance Criteria** | AC1: Version number is incremented on every published update. AC2: Withdrawn listing is not shown to new buyers in search results. AC3: Existing orders with this listing are not affected by withdrawal. AC4: Idempotency ensures duplicate update events do not produce conflicting listing states. |
| **Source** | idea.md §6.3, §5.1 |
| **Status** | CONFIRMED |

---

### FR-011 — Stock Availability Signal Update

| Field | Value |
|---|---|
| **ID** | FR-011 |
| **Name** | Stock Availability Signal Propagation |
| **Actor** | ACCore (seller) via Platform Connector |
| **Trigger** | Inventory state changes in ACCore (stock in/out, reserve, adjust) |
| **Normal Path** | ACCore emits StockAvailabilityChanged event → Offer/Price/Availability domain updates indicative availability snapshot with timestamp. |
| **Acceptance Criteria** | AC1: Availability shown in marketplace is indicative only; it carries a last-updated timestamp. AC2: Final availability confirmation always comes from ACCore via reservation (FR-002 step 3). AC3: A stale or disconnected availability snapshot is hidden or marked unavailable; checkout must revalidate price and quantity at ACCore and create an atomic reservation before authorization. |
| **Source** | idea.md §5, §6.3 |
| **Status** | CONFIRMED |

---

### FR-012 — Institution Onboarding and Registry

| Field | Value |
|---|---|
| **ID** | FR-012 |
| **Name** | Institution Registration and Integration Setup |
| **Actor** | ACT-PLATFORM-ADMIN |
| **Trigger** | New institution contracted; onboarding initiated in ACCSystem |
| **Normal Path** | Platform admin creates institution record in Institution Registry (platform_institution_id assigned). Integration credentials issued. ACCore connector configured. Institution goes through activation state before being allowed to publish products. |
| **Acceptance Criteria** | AC1: Each institution has a unique, stable platform_institution_id. AC2: Institution cannot publish products until institution status = Active. AC3: Integration credentials are rotatable without service disruption. |
| **Source** | idea.md §3.1 (Institution Registry), §5.2 |
| **Status** | DERIVED |

---

### FR-013 — License Renewal, Suspension, and Revocation

| Field | Value |
|---|---|
| **ID** | FR-013 |
| **Name** | License Lifecycle Management (Renew / Suspend / Revoke / Expire) |
| **Actor** | ACT-PLATFORM-ADMIN (via ACManagement) |
| **Trigger** | Scheduled license expiry, admin action, or policy-triggered suspension |
| **Normal Path** | Admin or automated policy triggers license state change. License & Entitlement Management transitions license state and publishes appropriate event (LicenseRenewed, LicenseSuspended, LicenseRevoked, LicenseExpired). ACCore License Connector receives event and applies restriction or restoration. |
| **Acceptance Criteria** | AC1: Every license state change is recorded with actor, reason, timestamp, and affected institution/product. AC2: ACCore applies restriction within defined propagation window after event receipt. AC3: Grace period applied before full restriction where policy specifies (UNKN-003 — grace period duration not defined). |
| **Source** | idea.md §6.3, §3.1 |
| **Status** | CONFIRMED (grace period details OPEN — UNKN-003) |

---

## 2. Non-Functional Requirements

> [!NOTE]
> Where idea.md specifies no measurable target, the requirement is marked UNKNOWN. UNKNOWN targets must be resolved by the product/engineering owner before implementation.

---

### NFR-001 — API Response Time (Commerce APIs)

| Field | Value |
|---|---|
| **ID** | NFR-001 |
| **Category** | Performance |
| **Requirement** | Commerce Core APIs (search, product detail, cart, checkout initiation) must respond within a defined latency budget under expected peak load. |
| **Target** | UNKNOWN — no latency target stated in idea.md |
| **Measurement Method** | p50 / p95 / p99 latency measured at API Gateway under load test matching peak concurrency assumptions. |
| **Workload Assumptions** | UNKNOWN — no TPS/concurrent-user targets provided (see UNKN-010). |
| **Priority** | HIGH — directly affects buyer conversion. |
| **Verification Owner** | OWNER_UNASSIGNED — assign before Phase 2 |
| **Source** | idea.md §11 (Technical Metrics: API latency, error rates) |
| **Status** | OPEN |

---

### NFR-002 — Checkout Success Rate

| Field | Value |
|---|---|
| **ID** | NFR-002 |
| **Category** | Reliability |
| **Requirement** | Checkout end-to-end success rate (checkout initiated → order confirmed) must meet a defined target under normal operating conditions. |
| **Target** | UNKNOWN |
| **Measurement Method** | Business metric: (OrderConfirmed events / CheckoutInitiated events) over rolling window, excluding buyer-side cancellations. |
| **Workload Assumptions** | UNKNOWN |
| **Priority** | HIGH |
| **Verification Owner** | OWNER_UNASSIGNED |
| **Source** | idea.md §11 (Business Metrics: checkout success rate) |
| **Status** | OPEN |

---

### NFR-003 — Idempotency and Message Deduplication

| Field | Value |
|---|---|
| **ID** | NFR-003 |
| **Category** | Correctness / Reliability |
| **Requirement** | No business side-effect (order creation, payment capture, stock deduction, event publish) must be duplicated due to message retry, network timeout, or duplicate event delivery. |
| **Target** | Zero duplicate side-effects for any operation carrying an idempotency key; measurable via reconciliation report showing 0 duplicate orders/payments in audit log. |
| **Measurement Method** | Automated reconciliation: compare order IDs, payment attempt IDs, reservation IDs for duplicates; alert on mismatch. |
| **Workload Assumptions** | At-least-once delivery assumed for all message channels. |
| **Priority** | CRITICAL — mandatory constraint (CON-003) |
| **Verification Owner** | Engineering (order domain, payment domain owners) |
| **Source** | idea.md §6.5 |
| **Status** | CONFIRMED (mandatory constraint) |

---

### NFR-004 — Multi-Tenant Isolation

| Field | Value |
|---|---|
| **ID** | NFR-004 |
| **Category** | Security |
| **Requirement** | Institution A must not be able to read, write, or infer data belonging to Institution B through any ACCSystem API, event, or query path. |
| **Target** | Zero cross-tenant data leakage incidents; verified by penetration testing and automated tenant isolation tests. |
| **Measurement Method** | Security test suite: attempt cross-tenant API calls with valid credentials of Institution A; verify all return 403/404. Audit log review for unauthorized access attempts. |
| **Workload Assumptions** | N institutions; each with M users; all sharing ACCSystem infrastructure. |
| **Priority** | CRITICAL |
| **Verification Owner** | Security lead |
| **Source** | idea.md §9 |
| **Status** | CONFIRMED (mandatory constraint) |

---

### NFR-005 — License Validation Availability

| Field | Value |
|---|---|
| **ID** | NFR-005 |
| **Category** | Availability |
| **Requirement** | License validation must not block ACCore operation during transient ACCSystem unavailability, within defined offline grace period. |
| **Target** | UNKNOWN — grace period duration and offline behavior not defined (UNKN-009) |
| **Measurement Method** | Test: disconnect ACCore from ACCSystem; confirm licensed modules continue operating for grace period duration; confirm restriction applies after expiry. |
| **Workload Assumptions** | ACCore may operate at remote institution with unreliable connectivity. |
| **Priority** | HIGH |
| **Verification Owner** | OWNER_UNASSIGNED — assign before Phase 1 licensing |
| **Source** | idea.md §4.3, §12 |
| **Status** | OPEN (UNKN-009) |

---

### NFR-006 — Payment Data Security

| Field | Value |
|---|---|
| **ID** | NFR-006 |
| **Category** | Security |
| **Requirement** | Sensitive payment card data (PAN, CVV, expiry) must never be stored in ACCSystem. Tokenization or Hosted Checkout must be used. |
| **Target** | Zero instances of raw card data in ACCSystem data stores; verified by security scan and design review. |
| **Measurement Method** | Data classification scan of Payment Domain data stores; design review of payment flow. |
| **Workload Assumptions** | All payment flows routed through payment provider adapter. |
| **Priority** | CRITICAL |
| **Verification Owner** | Security lead; payment domain owner |
| **Source** | idea.md §9 |
| **Status** | CONFIRMED (mandatory constraint) |

---

### NFR-007 — Event Ordering and Message Delivery

| Field | Value |
|---|---|
| **ID** | NFR-007 |
| **Category** | Reliability |
| **Requirement** | Events requiring ordered delivery (e.g., order state transitions) must be delivered in order relative to their partition key (order_id or seller_order_id). Events not requiring strict ordering may be delivered out-of-order. |
| **Target** | Zero out-of-order state transitions for a given order_id; verified by integration test suite. |
| **Measurement Method** | Integration tests: publish events out of order; verify consumer detects and handles via ordering key. |
| **Workload Assumptions** | At-least-once delivery; consumers must implement idempotent handlers. |
| **Priority** | HIGH |
| **Verification Owner** | Engineering (order domain, event bus owners) |
| **Source** | idea.md §6.5 |
| **Status** | CONFIRMED |

---

### NFR-008 — Software Package Integrity

| Field | Value |
|---|---|
| **ID** | NFR-008 |
| **Category** | Security / Integrity |
| **Requirement** | Every software release package must carry a SHA-256 checksum and digital signature; integrity must be verified before the release is published as Available. |
| **Target** | 100% of Available-status releases have verified checksum and signature on record. |
| **Measurement Method** | Automated check in Software Catalog publish workflow; rejected releases recorded with reason. |
| **Workload Assumptions** | Low frequency (releases per month vs. per second for commerce operations). |
| **Priority** | HIGH |
| **Verification Owner** | Platform product team; Software Distribution owner |
| **Source** | idea.md §9, §7.7 |
| **Status** | CONFIRMED |

---

### NFR-009 — Audit Trail Completeness

| Field | Value |
|---|---|
| **ID** | NFR-009 |
| **Category** | Compliance / Observability |
| **Requirement** | All sensitive operations (product publication price changes, order creation, payment actions, stock commitment, license actions, role grants, support session start/end, admin actions) must generate tamper-evident audit events with actor, action, target, timestamp, and outcome. |
| **Target** | 100% of defined sensitive operation types produce audit events; verified by audit coverage test. |
| **Measurement Method** | Test: perform each sensitive operation type; verify audit log entry with required fields. |
| **Workload Assumptions** | Volume proportional to transaction rate. Retention period UNKNOWN (UNKN-002 — compliance framework not defined). |
| **Priority** | HIGH |
| **Verification Owner** | Security / compliance owner |
| **Source** | idea.md §9, §11 |
| **Status** | CONFIRMED (retention period OPEN — UNKN-002) |

---

### NFR-010 — Correlation ID End-to-End Tracing

| Field | Value |
|---|---|
| **ID** | NFR-010 |
| **Category** | Observability |
| **Requirement** | Every checkout, order, and payment flow must carry a correlation_id that propagates from the originating client through all ACCSystem domains and all messages to ACCore and ACCMared. |
| **Target** | 100% of order-related traces are queryable by a single correlation_id across all participating services. |
| **Measurement Method** | Test: initiate checkout; verify correlation_id appears in traces across Commerce, Integration, Payment, Delivery, and Notification domains. |
| **Workload Assumptions** | All transaction traffic. |
| **Priority** | HIGH — mandatory per idea.md §11 |
| **Verification Owner** | Engineering (observability owner) |
| **Source** | idea.md §11 |
| **Status** | CONFIRMED |

---

### NFR-011 — Independent Service Deployability

| Field | Value |
|---|---|
| **ID** | NFR-011 |
| **Category** | Deployability |
| **Requirement** | Each ACCSystem domain service (Search, Payment, Delivery, etc.) must be independently deployable and scalable without requiring a full platform deployment. |
| **Target** | Deployment of any single service does not require downtime or coordinated deployment of other services; verified by CI/CD pipeline test. |
| **Measurement Method** | Deployment test: deploy updated Search service independently; verify other services continue operating. |
| **Priority** | HIGH — mandatory constraint (CON-012) |
| **Verification Owner** | DevOps / platform engineering |
| **Source** | idea.md §3.2 |
| **Status** | CONFIRMED |

---

### NFR-012 — RPO / RTO per Domain

| Field | Value |
|---|---|
| **ID** | NFR-012 |
| **Category** | Recovery |
| **Requirement** | Each domain must have defined Recovery Point Objective (RPO) and Recovery Time Objective (RTO) with scheduled backup and restoration testing. |
| **Target** | UNKNOWN — no RPO/RTO targets stated in idea.md. idea.md §10.3 says targets must be defined per domain. |
| **Measurement Method** | Disaster recovery drill: measure actual recovery time against defined RTO; verify data loss within RPO. |
| **Priority** | HIGH |
| **Verification Owner** | OWNER_UNASSIGNED — assign before Phase 2 |
| **Source** | idea.md §10.3 |
| **Status** | OPEN (UNKN-001) |

---

## 3. Constraints

| ID | Constraint | Mandatory | Source |
|---|---|---|---|
| CON-001 | No shared database between institutions | YES | idea.md §1.2, §4.2 |
| CON-002 | API-only integration between ACCSystem services and between ACCSystem and ACCore | YES | idea.md §1.2, §3.2 |
| CON-003 | Outbox/Idempotency mandatory for all retryable commands and events | YES | idea.md §6.5 |
| CON-004 | No sensitive payment card data stored in ACCSystem | YES | idea.md §9 |
| CON-005 | Tenant ID validated from auth token; not trusted from client payload | YES | idea.md §9 |
| CON-006 | ACManagement must not bypass Identity & Access; it is a service client | YES | idea.md §3.1.1 |
| CON-007 | License entitlement and user permissions are orthogonal | YES | idea.md §9 |
| CON-008 | Support access to institution data requires explicit consent/delegation, is scoped and time-limited, and must be audited | YES | idea.md §9 |
| CON-009 | Published events are immutable; corrections via new events only | YES | idea.md §6.5 |
| CON-010 | Software packages require SHA-256 checksum and digital signature; download links must be HTTPS | YES | idea.md §9 |
| CON-011 | ACCSystem public (visitor) portal must not expose administrative APIs | YES | idea.md §9 |
| CON-012 | Each service must be independently deployable and scalable | YES | idea.md §3.2 |

---

## 4. Assumptions with Owner / Action / Trigger

| ID | Assumption | Owner | Action | Revisit Trigger |
|---|---|---|---|---|
| ASSUM-001 | Cloud-hosted container deployment | Project owner | Confirm target infrastructure | Before C2/deployment design |
| ASSUM-002 | Arabic primary UI language; API identifiers in English | Project owner / technical lead | Confirm locale and i18n strategy | Before API schema design |
| ASSUM-003 | Single payment provider at MVP | Product owner | Confirm Phase 3 scope | At Phase 3 start |
| ASSUM-004 | ACCore instances may share physical infrastructure but are logically isolated | Project owner | Define hosting contracts | Before institution onboarding |
| ASSUM-005 | ACManagement Protected Console enforces row-level scoping per institution | Security / product owner | Define access control policy | Before ACManagement design |
| ASSUM-006 | ACCMared covers platform-own fleet only at MVP | Product owner | Confirm delivery scope | Before Phase 4 |

---

## 5. Open Decisions (from idea.md §12)

> [!IMPORTANT]
> These decisions must be resolved before implementation begins in their respective phases.

| Decision ID | Decision | Initial Recommendation | Phase Needed |
|---|---|---|---|
| ODEC-001 | ACCore hosting and packaging | Institution-controlled local or institution-managed public cloud; integrated or split package configurable | Before Phase 1 |
| ODEC-002 | Price/stock freshness: indicative display + validate-and-reserve at checkout | Confirmed as design (see FACT-004, FR-002) | Phase 2 |
| ODEC-003 | Multi-seller cart: Parent Order + Seller Orders; MVP required | Parent/Seller Order model; all required reservations before authorization | Phase 2 |
| ODEC-004 | Accounting trigger point for B2B transactions | Define trigger per institution agreement (order confirm / ship / deliver / invoice) | Phase 5 |
| ODEC-005 | Payment capture timing | Seller/agreement policy supports authorize-then-capture and immediate/contract-defined modes under platform controls | Phase 3 |
| ODEC-006 | Settlement / commission domain | Define if platform is an intermediary collecting funds | Phase 6 |
| ODEC-007 | Returns and disputes capability | Add as Phase 6 capability; Returns domain design pending | Phase 6 |
| ODEC-008 | ACCore offline behavior scope | Define which modules operate offline and for how long | Phase 1 |
| ODEC-009 | Multi-currency and tax model | Define currency model and tax jurisdiction rules | Phase 5 |
| ODEC-010 | ACCMared delivery scope: platform fleet only or external logistics provider integration | ASSUM-006: platform fleet only at MVP | Phase 4 |
| ODEC-011 | License model: type, granularity, renewal, grace period | UNKN-003: requires product owner decision | Phase 1 |
| ODEC-012 | ACCommerce individual user monetization (free, subscription, freemium) | UNKN-007: requires business decision | Phase 2 |
| ODEC-013 | Support access policy: per-session consent or pre-authorized delegation; maximum duration and data masking | UNKN-008: requires security/policy decision | Phase 1 |
| ODEC-014 | License offline validation strategy: signed short-lived token or mandatory periodic connectivity | UNKN-009: requires product/security decision | Phase 1 |

---

## 6. Diagram Selection Plan

> Rationale for each of the 7 official C4 view types plus supporting views.

| View Type | Selection | Rationale |
|---|---|---|
| **System Landscape** | SELECTED | 6 internal systems + 2 external entities; essential for stakeholder communication and cross-system dependency overview. Produced in Stage 2. |
| **C1 System Context — SYS-ACCSYSTEM** | SELECTED | Focal system; highest complexity; every actor and external system interacts with it. Mandatory baseline view. |
| **C1 System Context — SYS-ACCORE** | SELECTED | Focal system; per-institution deployment; important boundary clarification. |
| **C1 System Context — SYS-ACCOMMERCE** | SELECTED (lightweight) | Direct commerce client; boundary and actor connections needed for integration clarity. |
| **C1 System Context — SYS-ACMANAGEMENT** | SELECTED (lightweight) | Two-zone architecture (public/protected); boundary is a critical security design element. |
| **C1 System Context — SYS-ACCMARED-SUP / SYS-ACCMARED-COU** | SELECTED (lightweight) | Delivery operations clients; relationships to Delivery Domain needed. |
| **C2 Container — SYS-ACCSYSTEM** | SELECTED | 13+ named domains; independently deployable services; highest design risk and complexity. |
| **C2 Container — SYS-ACCORE** | SELECTED | 8 named modules; ERP + Commerce Workspace + Platform Connector integration. |
| **C2 Container — SYS-ACCOMMERCE** | CONDITIONAL — defer to Stage 3 if ACCommerce is a thin client | ACCommerce may be primarily a UI client; container decomposition value depends on backend complexity. Revisit after C1 is stable. |
| **C2 Container — SYS-ACMANAGEMENT** | CONDITIONAL — defer to Stage 3 | ACManagement is a frontend client; backend containers live in SYS-ACCSYSTEM Platform Management domain. |
| **C3 Component — Order Management** | SELECTED | Saga orchestration; highest business risk and complexity. |
| **C3 Component — Payment Orchestration** | SELECTED | External integration; compensation logic; PCI-adjacent concerns. |
| **C3 Component — License & Entitlement** | SELECTED | Complex state machine (issue/activate/renew/suspend/revoke/expire); critical correctness. |
| **C3 Component — Institution Integration** | SELECTED | Multi-tenant bridge; Outbox/Inbox; async reliability. |
| **C4 Code** | NOT SELECTED | No implementation language confirmed; would be speculative. Reconsider when language stack is decided. |
| **Dynamic view — Purchase Saga** | SELECTED | Most complex distributed flow; mandatory for implementation guidance. |
| **Dynamic view — License Issuance** | SELECTED | Multi-system flow; business-critical. |
| **Dynamic view — Software Release Publication** | SELECTED | Integrity checks and CDN integration; worth documenting. |
| **Deployment view** | SELECTED | Multi-layer architecture described in idea.md §10.1; needed for infrastructure planning. |
| **Security / data classification view** | SELECTED | Multi-tenant isolation, PCI-adjacent payment data, support access — high-risk cross-cutting concerns. |

---

## 7. Architecture Style Decision — ACCSystem

### 7.1 Candidates

| Style | Description |
|---|---|
| **Modular Monolith** | All ACCSystem domains in one deployable unit; modules separated by code boundaries (packages/namespaces); single database per module or shared with schema isolation. |
| **Coarse-Grained Services** | 5–8 independently deployable services, each owning one or more related domains (e.g., Commerce Service, Fulfilment Service, Platform Management Service); shared infrastructure. |
| **Microservices** | Each domain is a fully independent, separately deployed and scaled service; each owns its database; communicates only via API or events. |

### 7.2 Analysis Against Constraints

| Factor | Modular Monolith | Coarse-Grained Services | Microservices |
|---|---|---|---|
| Independent deployment (CON-012) | FAILS — shared deployment unit | PASSES — each service deployed independently | PASSES — each service deployed independently |
| Independent scaling | FAILS — scale whole monolith | PARTIAL — scale at service granularity | PASSES — scale at domain granularity |
| Data ownership isolation (CON-002) | PARTIAL — requires discipline; shared DB risk | PASSES — each service owns its database | PASSES — strict per-domain database ownership |
| Operational maturity required | LOW | MEDIUM | HIGH — distributed systems expertise, service mesh, observability stack |
| Team topology fit | UNKNOWN — team size not stated | MEDIUM — fits small-to-medium engineering teams | HIGH team size requirement |
| Complexity vs. idea.md scope (13+ domains) | LOW fit — 13 domains in one monolith creates code-level coupling risk | GOOD fit — groups related domains; reduces inter-service calls | GOOD fit — maximum flexibility; high operational overhead |
| Risk of premature decomposition | NONE | LOW — decompose by bounded context, not function | HIGH if done prematurely |

### 7.3 Recommendation

**PROPOSED:** Adopt **coarse-grained services** as the initial ACCSystem architecture style, grouping the 13+ domains into approximately 5–6 independently deployable services:

1. **Commerce Service** — Catalog, Search, Offer/Price, Cart, Checkout, Order Management
2. **Fulfilment Service** — Payment Orchestration, Delivery Management, Notifications
3. **Institution Integration Service** — Integration Gateway, Sync Workers, Webhooks, Outbox/Inbox
4. **Platform Management Service** — Software Catalog & Distribution, License & Entitlement, Platform Administration & Support
5. **Platform Access Service** — API Gateway/BFF, Identity & Access, Institution Registry
6. **Observability Service** — Audit & Observability (shared infrastructure)

**Confidence:** MEDIUM  
**Key uncertainty:** Team topology, operational maturity, and infrastructure capacity are UNKNOWN (UNKN-010, ASSUM-001). These could push the decision toward a larger initial service or toward more decomposition.

**Migration path:** Internal module boundaries within each coarse-grained service must be enforced from day 1 (no cross-module direct database reads). This allows selective extraction of high-load domains (Payment, Search) into independent services as scaling evidence demands, without redesign.

**Reconsideration trigger:** If Payment Orchestration or Search & Discovery require independent scaling from other Commerce functions within the first 6 months of production, extract them as independent services.

> [!NOTE]
> This recommendation is PROPOSED by the architecture assistant. It has not been accepted by stakeholders. Final decision must be recorded as ADR-012 with stakeholder acceptance.

> [!IMPORTANT]
> **Terminology alignment (see ADR-012):** The 5–6 groups above are **initial deployment units** — coarse-grained runtime packages. They are distinct from the **17 logical bounded contexts** defined in idea.md §3.1 and the C2 container model, which represent data-ownership and API-contract boundaries that are enforced regardless of deployment grouping. Never share a database schema across bounded-context boundaries, even within the same deployment unit.

---

*Scope & Strategy stage content complete. This document feeds Stage 2 (C1 diagrams) and Stage 3 (C2 containers).*


## 8. Remediated Incremental Roadmap

1. **Shared foundations:** tenant identity, RBAC, audit, policy registry, Outbox/Inbox, correlation/idempotency, release/provenance, connector contract, and ACCore health state. Acceptance: institutions are isolated and unknown outcomes recoverable.
2. **Publication and discovery:** ACCore product publication, listing validation, multilingual fields, search, price/availability projection, and disconnected visibility. Acceptance: published listings are traceable and unavailable institutions are not purchasable.
3. **Reservation:** ParentOrder/SellerOrders, atomic ACCore reservation, concurrency control, expiry, compensation, and reconciliation. Acceptance: multi-seller carts cannot authorize before all required reservations.
4. **Payment and settlement:** provider adapter, payment code/intent, auth/capture policy, ledger, commission, seller credit, manual payments, and reconciliation. Acceptance: no duplicate financial effect and no raw card data.
5. **Delivery and tracking:** internal fleet provider first, assignment, tracking, proof of delivery, collection-data separation, and extensible external provider contract. Acceptance: delivery state is auditable and carrier funds are not assumed in core payment.

Clean Architecture is a guiding separation-of-concerns principle, not a chosen implementation stack.
