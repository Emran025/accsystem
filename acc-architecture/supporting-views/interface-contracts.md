# ACC Ecosystem — Interface Contracts

**View type:** Interface Contracts  
**Stage:** 6 — Supporting Views  
**Status:** PROPOSED  
**Source:** idea.md §6, §7, §9; registry/interfaces.json; registry/elements.json  
**Parent:** `acc-architecture/`

> [!IMPORTANT]
> Every assertion is labelled: **CONFIRMED** (stated in idea.md with section reference) / **ASSUMPTION** (reasonable inference from context, not stated explicitly) / **PROPOSAL** (recommended, not stated) / **UNKNOWN** (not addressed; consequence, owner and revisit trigger recorded).
>
> This document does not represent stakeholder approval or production readiness. API schemas and versioning policies must be formally specified in OpenAPI/AsyncAPI before implementation.

> [!NOTE]
> **Document version: V5.1** — Reservation contradiction fix applied. §3.4, §3.6, §9.4, and §10 have been updated to align with ADR-018: timeout/elapsed time alone is never proof of a reservation outcome; `UNKNOWN` must be held, queried, and reconciled before any compensating action. See Change Log at the end of this document for a summary of all V5.1 changes.

---

## Governance Rules Applied

- All IDs are taken from `registry/interfaces.json` and `registry/elements.json`; no IDs invented
- Fields not specified in idea.md are labelled UNKNOWN with `owner=OWNER_UNASSIGNED` and revisit trigger
- Interface version and exact field names require OpenAPI/AsyncAPI contract before implementation
- This document is a reference-level contract description, not an executable specification

---

## Interface Index

| Interface ID | Provider | Contract Type | Section |
|---|---|---|---|
| IF-ACC-CATALOG-QUERY | CNT-ACC-CATALOG | Synchronous REST | §1 |
| IF-ACC-ORDER-CREATE | CNT-ACC-ORDERS | Synchronous REST | §2 |
| IF-ACC-RESERVE-SAGA | CNT-ACC-INTEGRATION | Synchronous REST (saga step) | §3 |
| IF-ACC-PAYMENT-WEBHOOK | EXT-PAYMENT-PROVIDER | Inbound webhook (async) | §4 |
| IF-ACC-EVENT-ENVELOPE | CNT-ACC-EVENTBUS | Async event (message bus) | §5 |
| IF-ACC-LICENSE-VALIDATE | CNT-ACC-LICENSE | Synchronous REST | §6 |
| IF-ACC-SOFTDL | CNT-ACC-SOFTCAT | Synchronous REST | §7 |
| IF-ACR-PUBLISH-EVENT | CNT-ACR-CONNECTOR | Async event / outbound HTTP | §8 |
| IF-ACR-RESERVATION-RESP | CNT-ACR-CONNECTOR | Synchronous REST (callback) / async | §9 |

---

## 1. IF-ACC-CATALOG-QUERY

### 1.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-CATALOG-QUERY | CONFIRMED — registry/interfaces.json |
| Version | v1 (example; subject to OpenAPI contract) | ASSUMPTION |
| Protocol | HTTPS REST / JSON | ASSUMPTION — idea.md §6.2 shows REST path style |
| Contract type | Synchronous request/response | CONFIRMED — idea.md §6.1: "Synchronous API … search, view details" |

### 1.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACC-CATALOG | Catalog & Publication |
| Consumer | CNT-ACE-MOBILEAPP | ACCommerce Mobile/Web App |
| Consumer | CNT-ACR-COMMERCE | Commerce Workspace (ACCore) |
| Consumer | CNT-ACC-APIGATEWAY | API Gateway / BFF |

> [!NOTE]
> CNT-ACC-APIGATEWAY typically sits in front of CNT-ACC-CATALOG and routes calls from both CNT-ACE-MOBILEAPP and CNT-ACR-COMMERCE. The gateway is a consumer of the catalog query interface from an architectural routing perspective.

### 1.3 Purpose

Allows buyers (individuals and institutional employees) to search and retrieve product listings from the marketplace catalog. Returns the marketplace projection of product data — not the original product master. CONFIRMED: idea.md §5 "ACCSystem holds a published copy of the data needed for search, display, and ordering"; §6.2 `GET /v1/catalog/products`.

### 1.4 Request Schema

**Endpoint examples** (CONFIRMED from idea.md §6.2 — reference only, not final contract):

```
GET /v1/catalog/products?query={text}&seller_id={platform_institution_id}&category=...
GET /v1/catalog/products/{listing_id}
```

**Query parameters (shape — ASSUMPTION: exact field names and constraints require OpenAPI spec):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `query` | string | No | Free-text search query |
| `seller_id` | string (`platform_institution_id`) | No | Filter by institution seller |
| `category` | string | No | Category filter |
| `page` / `page_size` | integer | No | Pagination — ASSUMPTION |
| `sort` | string | No | Sort field — ASSUMPTION |

**Response schema (shape — ASSUMPTION):**

```json
{
  "listings": [
    {
      "listing_id": "string",
      "seller_product_id": "string",
      "platform_institution_id": "string",
      "name": "string",
      "description": "string",
      "price_snapshot": { "amount": "decimal", "currency": "string" },
      "availability_indicator": "string",
      "last_synced_at": "ISO-8601",
      "version": "integer",
      "images": ["url"],
      "category": "string"
    }
  ],
  "total": "integer",
  "page": "integer",
  "page_size": "integer"
}
```

> [!WARNING]
> The `price_snapshot` and `availability_indicator` are NOT authoritative for checkout. CONFIRMED — idea.md §5: "The availability shown in the ACCSystem catalog does not constitute a reservation guarantee." Re-verification occurs at checkout via IF-ACC-RESERVE-SAGA.

### 1.5 Error Cases

| HTTP Status | Scenario | Consumer Action |
|---|---|---|
| 400 | Invalid query parameters | Reject at gateway; return user-readable error |
| 401 | Missing/invalid auth token | Re-authenticate |
| 403 | Access to restricted listing category | Display access-denied message |
| 404 | `listing_id` not found | Display product-not-found |
| 429 | Rate limit exceeded | Backoff + retry with exponential delay |
| 500 | Internal catalog error | Retry with backoff; show generic error to user |

### 1.6 Versioning and Backward Compatibility

UNKNOWN — versioning strategy (URL path versioning, header versioning, content negotiation) not specified in idea.md.  
**Consequence:** Breaking changes to the catalog API could break all three consumers simultaneously.  
**Owner:** OWNER_UNASSIGNED  
**Revisit trigger:** Before Phase 1 (Marketplace Foundation) API finalization per idea.md §13

### 1.7 Idempotency

Safe GET operation — idempotent by HTTP semantics. No idempotency key required. CONFIRMED.

### 1.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport | TLS on all requests | CONFIRMED — idea.md §9: "TLS in transit" |
| Authentication | OAuth 2.0 / JWT Bearer token at API Gateway | CONFIRMED — idea.md §9 |
| Public catalog listing access | May be unauthenticated for browsing — UNKNOWN | UNKNOWN: whether anonymous browsing is permitted requires explicit security policy decision |
| Tenant isolation | Institution-scoped responses must enforce `institution_id` from token | CONFIRMED — idea.md §9: "tenant_id check on every request" |
| Rate limiting | Applied at CNT-ACC-APIGATEWAY | PROPOSAL — idea.md §3.1 describes API Gateway role; rate limit thresholds UNKNOWN |

### 1.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-004 | ACCSystem stores marketplace projection, not source |
| ADR | ADR-012 | Bounded-context services |
| Function | FN-INT-PUBLISH | Product publication populates catalog that this interface queries |
| Container | CNT-ACC-SEARCH | Search & Discovery also exposes query interface (relationship documented in separate query interface spec (OPEN)) |

---

## 2. IF-ACC-ORDER-CREATE

### 2.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-ORDER-CREATE | CONFIRMED — registry/interfaces.json |
| Version | v1 (subject to OpenAPI contract) | ASSUMPTION |
| Protocol | HTTPS REST / JSON | ASSUMPTION — idea.md §6.2 shows `POST /v1/orders` |
| Contract type | Synchronous request/response (order initiation); downstream saga is async | CONFIRMED — idea.md §6.1, §7.2 |

### 2.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACC-ORDERS | Order Management |
| Consumer | CNT-ACE-MOBILEAPP | ACCommerce Mobile/Web App |
| Consumer | CNT-ACR-COMMERCE | Commerce Workspace (ACCore) |
| Consumer | CNT-ACC-APIGATEWAY | API Gateway / BFF |

### 2.3 Purpose

Creates a new platform order from an active, validated checkout session. The order creation triggers the order saga (CMP-ORD-SAGA) which coordinates reservation (IF-ACC-RESERVE-SAGA), payment authorization (via CNT-ACC-PAYMENT), and confirmation. CONFIRMED — idea.md §7.2, §7.6.

### 2.4 Request Schema

**Endpoint** (CONFIRMED from idea.md §6.2 — reference only):

```
POST /v1/orders
```

**Request body (shape — ASSUMPTION: exact fields require OpenAPI spec):**

```json
{
  "checkout_session_id": "string",
  "buyer_id": "string",
  "institution_id": "string | null",
  "idempotency_key": "string",
  "lines": [
    {
      "listing_id": "string",
      "seller_product_id": "string",
      "platform_institution_id": "string",
      "quantity": "integer",
      "agreed_price": { "amount": "decimal", "currency": "string" }
    }
  ],
  "shipping_address": { },
  "payment_method_ref": "string",
  "correlation_id": "string"
}
```

**Response body (ASSUMPTION):**

```json
{
  "order_id": "string",
  "status": "PendingReservation",
  "created_at": "ISO-8601",
  "lines": [ ],
  "seller_orders": [ { "seller_order_id": "string", "platform_institution_id": "string" } ]
}
```

> [!NOTE]
> CONFIRMED — idea.md §8.3: At order confirmation, an immutable commercial snapshot of price, currency, discount, tax, quantity, seller name, and delivery terms is stored. Order creation response does not constitute order confirmation; that requires saga completion.

### 2.5 Error Cases

| HTTP Status | Scenario | Consumer Action |
|---|---|---|
| 400 | Invalid/expired checkout session | Re-initiate checkout |
| 400 | Price changed since snapshot | Refresh cart and re-checkout |
| 400 | Quantity unavailable (pre-saga check) | Refresh cart |
| 401 | Unauthenticated | Re-authenticate |
| 409 | Duplicate `idempotency_key` (order already exists) | Return existing order_id; no new order created |
| 422 | Business rule violation (e.g., seller inactive) | Show specific reason |
| 500 | Internal order service error | Retry with same `idempotency_key` |

### 2.6 Idempotency

**CONFIRMED** — idea.md §6.5: "Every command that may be re-sent must carry an `Idempotency-Key`; consumer must store previously processed keys." The `idempotency_key` in the request body is mandatory. If a request with the same key is received again, the same order response is returned without creating a duplicate order.

### 2.7 Versioning and Backward Compatibility

UNKNOWN — not specified in idea.md.  
**Consequence:** Consumer clients (mobile, web) may break on schema changes.  
**Owner:** OWNER_UNASSIGNED  
**Revisit trigger:** Phase 2 (Commerce Transactions) API finalization

### 2.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport | TLS | CONFIRMED |
| Authentication | OAuth 2.0 JWT Bearer (buyer or institution-scoped token) | CONFIRMED — idea.md §9 |
| Authorization | Buyer can only create order on behalf of their own identity; institution scoped by `institution_id` claim | CONFIRMED — idea.md §9: tenant_id check |
| Audit | OrderCreated event recorded in audit trail | CONFIRMED — idea.md §9 |

### 2.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-007 | Order domain coordinates, doesn't own payment/delivery logic |
| ADR | ADR-013 | Saga pattern for distributed order transaction |
| Component | CMP-ORD-SAGA | Saga orchestrator triggered by order creation |
| Component | CMP-ORD-SNAPSHOT | Commercial snapshot captured at confirmation |
| Function | FN-ORD-CONFIRM | Order confirmation function spec |

---

## 3. IF-ACC-RESERVE-SAGA

### 3.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-RESERVE-SAGA | CONFIRMED — registry/interfaces.json |
| Version | v1 (subject to OpenAPI contract) | ASSUMPTION |
| Protocol | HTTPS REST / JSON (saga orchestration step) | ASSUMPTION — idea.md §6.2 `POST /v1/integration/reservations/{reservation_id}/confirm` |
| Contract type | Synchronous REST (reservation request); response may be synchronous or via callback | CONFIRMED — idea.md §7.2: "Order Domain sends Reservation request to ACCore seller" |

### 3.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACC-INTEGRATION | Institution Integration Gateway |
| Consumer | CNT-ACC-ORDERS | Order Management |
| Consumer | CMP-ORD-SAGA | Order Saga Orchestrator |

### 3.3 Purpose

The saga step by which the Order domain requests an inventory reservation at the ACCore seller instance. CNT-ACC-INTEGRATION relays the reservation request to the appropriate ACCore via the Platform Connector (CNT-ACR-CONNECTOR). The ACCore seller validates price and availability and creates an expiring reservation. CONFIRMED — idea.md §7.2, §6.3: "ReservationRequested", "ReservationAccepted / Rejected".

### 3.4 Request Schema

**Endpoint** (CONFIRMED from idea.md §6.2 — reference only):

```
POST /v1/integration/reservations
```

**Request body (shape — ASSUMPTION):**

```json
{
  "idempotency_key": "string",
  "order_id": "string",
  "seller_order_id": "string",
  "platform_institution_id": "string",
  "correlation_id": "string",
  "lines": [
    {
      "listing_id": "string",
      "seller_product_id": "string",
      "quantity": "integer",
      "agreed_price": { "amount": "decimal", "currency": "string" }
    }
  ],
  "reservation_ttl_seconds": "integer"
}
```

> [!WARNING]
> `reservation_ttl_seconds` is a **request hint only**. The authoritative reservation TTL is set and enforced by ACCore's local policy. The saga MUST NOT treat elapsed wall-clock time as proof of expiry or proof that the reservation was rejected. Actual numeric values are configurable per ADR-022 and require approval per ADR-018. Field label: PROPOSAL.

**Response body — `ReservationAccepted` (ASSUMPTION):**

```json
{
  "reservation_id": "string",
  "status": "ACCEPTED",
  "expiry_at": "ISO-8601",
  "confirmed_price": { "amount": "decimal", "currency": "string" },
  "confirmed_quantity": "integer"
}
```

**Response body — `ReservationRejected` (ASSUMPTION):**

```json
{
  "reservation_id": "string",
  "status": "REJECTED",
  "reason_code": "PRICE_CHANGED | INSUFFICIENT_STOCK | SELLER_INACTIVE | OTHER",
  "reason_message": "string"
}
```

> **Canonical status vocabulary:** Response `status` MUST be one of `ACCEPTED`, `REJECTED`, or `UNKNOWN`. `UNKNOWN` is returned when ACCore cannot immediately determine the outcome (connectivity issue, partial write). An `UNKNOWN` response is **not** a rejection — the saga must query by `idempotency_key` and await resolution before taking any compensating action. Vocabulary cross-reference: ADR-018.

### 3.5 Saga Compensation

If reservation is rejected: checkout is halted; no payment is requested; cart is refreshed. CONFIRMED — idea.md §7.2: "If the seller rejects the reservation, Checkout stops and displays an actionable reason without final payment deduction."

If reservation is accepted but payment subsequently fails: reservation release is requested from ACCore via Integration Gateway. CONFIRMED — idea.md §7.5.

### 3.6 Error Cases

| Scenario | Handling |
|---|---|
| ACCore unreachable | Retry with same `idempotency_key`; exponential backoff; query existing reservation outcome | CONFIRMED — idea.md §7.5 |
| Timeout before response (no response received by saga) | Persist `UNKNOWN` on saga reservation state; block payment step; query ACCore using `idempotency_key` / `reservation_id`; do not compensate or release until a definitive `ACCEPTED`, `REJECTED`, or `EXPIRED` outcome is confirmed by ACCore query or reconciliation | PROPOSAL — aligns with ADR-006 §3.2, ADR-013 §4, ADR-018 |
| Invalid institution_id | Return 404/422 from Integration Gateway | ASSUMPTION |
| Reservation TTL expired | ACCore auto-releases; saga compensates | CONFIRMED — idea.md §7.2 |

### 3.7 Idempotency

**CONFIRMED** — idea.md §6.5. The `idempotency_key` must be stable per saga attempt. Repeated reservation requests with the same key return the same outcome without creating a duplicate reservation at ACCore.

### 3.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport | TLS between CNT-ACC-ORDERS → CNT-ACC-INTEGRATION → CNT-ACR-CONNECTOR | CONFIRMED — idea.md §4.3 |
| Service-to-service auth | OAuth 2.0 Client Credentials | CONFIRMED — idea.md §9: "OAuth 2.0 Client Credentials with rotatable secrets" |
| `institution_id` validation | Integration Gateway validates that the seller institution is active | CONFIRMED — idea.md §7.1 |

### 3.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-006 | Inventory reservation at ACCore before order confirmation |
| ADR | ADR-013 | Saga pattern |
| Component | CMP-ORD-SAGA | Orchestrates this saga step |
| Component | CMP-INT-RESERVATION | Reservation Relay — relays request to ACCore |
| Interface | IF-ACR-RESERVATION-RESP | ACCore's reservation response back to Integration |
| Function | FN-ORD-RESERVE | Reservation function spec |

---

## 4. IF-ACC-PAYMENT-WEBHOOK

### 4.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-PAYMENT-WEBHOOK | CONFIRMED — registry/interfaces.json |
| Version | Defined by payment provider (external) | UNKNOWN |
| Protocol | HTTPS POST (inbound webhook from provider) | CONFIRMED — idea.md §9: "webhook signature verification" |
| Contract type | Inbound async webhook | CONFIRMED — idea.md §6.1, §7.2 |

### 4.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | EXT-PAYMENT-PROVIDER | External Payment Provider(s) |
| Consumer | CNT-ACC-PAYMENT | Payment Orchestration |
| Consumer | CMP-PAY-ORCHESTRATOR | Payment Orchestrator |

### 4.3 Purpose

The external payment provider calls back into ACCSystem with payment event notifications: authorization results, capture confirmations, failures, refund outcomes, and dispute notifications. This is the boundary between the external payment world and ACCSystem's payment domain. CONFIRMED — idea.md §7.2: "Payment Domain: authorize… PaymentAuthorized or PaymentFailed".

### 4.4 Webhook Event Schema

The schema is provider-defined (UNKNOWN: specific provider field names). The expected event types ACCSystem must handle:

| Event Type | Meaning | ACCSystem Action |
|---|---|---|
| `payment.authorized` | Authorization succeeded | Saga: proceed to order confirmation |
| `payment.capture_confirmed` | Funds captured | Update PaymentAttempt to Captured |
| `payment.failed` | Authorization or capture failed | Saga: release reservation; fail order |
| `payment.refund_succeeded` | Refund processed | Update PaymentAttempt; notify order |
| `payment.refund_failed` | Refund failed | Alert operations; manual resolution |
| `payment.dispute_opened` | Chargeback/dispute | Alert finance team; freeze related order |

**Minimum expected envelope (ASSUMPTION — exact fields provider-specific):**

```json
{
  "event_id": "string (provider-assigned)",
  "event_type": "payment.authorized | ...",
  "occurred_at": "ISO-8601",
  "payment_reference": "string",
  "order_reference": "string",
  "amount": { "value": "decimal", "currency": "string" },
  "status": "string",
  "signature": "string (HMAC-SHA256)"
}
```

### 4.5 Security

| Control | Detail | Label |
|---|---|---|
| Signature verification | HMAC-SHA256 on every inbound webhook | CONFIRMED — idea.md §9: "webhook signature verification and replay protection" |
| Timestamp check | Reject if `|now - webhook_timestamp| > 5 minutes` | PROPOSAL — idea.md §9 requires timestamp check; tolerance is PROPOSAL |
| Event ID deduplication | `event_id` checked against idempotency store; duplicates silently acknowledged (HTTP 200) | CONFIRMED — idea.md §6.5: "Inbox/Processed Message Store to prevent double processing" |
| Transport | HTTPS only | CONFIRMED |
| Endpoint protection | Webhook endpoint not publicly discoverable; protected at gateway | PROPOSAL |

### 4.6 Idempotency

**CONFIRMED** — idea.md §6.5. The `event_id` from the provider is stored in the payment idempotency/inbox store. Repeated delivery of the same event produces no additional side effects.

### 4.7 Error Cases

| Scenario | Handling |
|---|---|
| Signature mismatch | Return HTTP 400; log security alert; do NOT process payload |
| Stale timestamp (replay attempt) | Return HTTP 400; log security alert |
| Duplicate event_id | Return HTTP 200; take no action (already processed) |
| Processing failure | Return HTTP 500; provider will retry; event eventually goes to DLQ |
| Unknown event type | Return HTTP 200; log warning; do not fail delivery |

### 4.8 Versioning and Backward Compatibility

UNKNOWN — provider's webhook version/schema evolution policy is external.  
**Consequence:** Provider schema changes may break payment processing without warning.  
**Owner:** OWNER_UNASSIGNED  
**Revisit trigger:** Before Phase 3 (Payment) go-live; requires provider integration agreement

### 4.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-007 | Order domain coordinates payment |
| Component | CMP-PAY-ORCHESTRATOR | Receives webhook; drives saga |
| Component | CMP-PAY-RECONCILIATION | Reconciliation against provider statement |
| Supporting view | security-view.md §6 | Webhook security controls |

---

## 5. IF-ACC-EVENT-ENVELOPE

### 5.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-EVENT-ENVELOPE | CONFIRMED — registry/interfaces.json |
| Version | Envelope version: `event_version` field per event | CONFIRMED — idea.md §6.4 |
| Protocol | Message broker / event bus (technology UNKNOWN) | ASSUMPTION — idea.md §3: "Event Bus / Message Broker" |
| Contract type | Asynchronous publish/subscribe | CONFIRMED — idea.md §6.1: "Asynchronous Events" |

### 5.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACC-EVENTBUS | Event Bus / Message Broker |
| Consumer | CNT-ACC-ORDERS | Order Management |
| Consumer | CNT-ACC-PAYMENT | Payment Orchestration |
| Consumer | CNT-ACC-DELIVERY | Delivery Management |
| Consumer | CNT-ACC-INTEGRATION | Institution Integration Gateway |
| Consumer | CNT-ACC-LICENSE | License & Entitlement Management |
| Consumer | CNT-ACC-NOTIFICATIONS | Notifications |

### 5.3 Purpose

Defines the standard envelope format for all events published to and consumed from the ACCSystem shared Event Bus. Every domain service uses this envelope to publish business events. This is the foundational async integration contract across all ACCSystem bounded contexts. CONFIRMED — idea.md §6.4.

### 5.4 Event Envelope Schema

**CONFIRMED from idea.md §6.4:**

```json
{
  "event_id": "uuid",
  "event_type": "string (e.g., 'OrderConfirmed')",
  "event_version": 1,
  "occurred_at": "ISO-8601 UTC",
  "producer": "string (e.g., 'accsystem.orders')",
  "institution_id": "string | null",
  "aggregate_id": "string (e.g., 'order_456')",
  "correlation_id": "uuid",
  "causation_id": "uuid | null",
  "idempotency_key": "string (stable-unique-key)",
  "data": { }
}
```

### 5.5 Catalogue of Business Events by Consumer

CONFIRMED from idea.md §6.3:

| Event Type | Publisher | Key Consumers | `data` Shape Summary |
|---|---|---|---|
| `OrderConfirmed` | CNT-ACC-ORDERS | CNT-ACC-PAYMENT, CNT-ACC-DELIVERY, CNT-ACC-INTEGRATION | `order_id`, `seller_order_id`, `lines`, `buyer_id`, `institution_id` — ASSUMPTION for `data` fields |
| `OrderCancelled` | CNT-ACC-ORDERS | CNT-ACC-INTEGRATION, CNT-ACC-PAYMENT, CNT-ACC-DELIVERY | `order_id`, `reason_code` — ASSUMPTION |
| `PaymentAuthorized` | CNT-ACC-PAYMENT | CNT-ACC-ORDERS | `payment_id`, `order_id`, `amount`, `currency` — ASSUMPTION |
| `PaymentCaptured` | CNT-ACC-PAYMENT | CNT-ACC-ORDERS | `payment_id`, `order_id` — ASSUMPTION |
| `PaymentFailed` | CNT-ACC-PAYMENT | CNT-ACC-ORDERS | `payment_id`, `order_id`, `failure_reason` — ASSUMPTION |
| `ShipmentCreated` | CNT-ACC-DELIVERY | CNT-ACC-ORDERS, CNT-ACC-NOTIFICATIONS | `shipment_id`, `order_id` — ASSUMPTION |
| `ShipmentDelivered` | CNT-ACC-DELIVERY | CNT-ACC-ORDERS, CNT-ACC-NOTIFICATIONS | `shipment_id`, `order_id`, `proof_of_delivery_ref` — ASSUMPTION |
| `ProductListingPublished` | CNT-ACC-INTEGRATION | CNT-ACC-CATALOG | `listing_id`, `seller_product_id`, `platform_institution_id`, `version` — ASSUMPTION |
| `ProductListingWithdrawn` | CNT-ACC-INTEGRATION | CNT-ACC-CATALOG | `listing_id` — ASSUMPTION |
| `LicenseIssued` | CNT-ACC-LICENSE | CNT-ACC-INTEGRATION, CNT-ACC-AUDIT | `license_id`, `institution_id`, `product`, `modules` — ASSUMPTION |
| `LicenseRevoked` | CNT-ACC-LICENSE | CNT-ACC-INTEGRATION, CNT-ACC-NOTIFICATIONS | `license_id`, `reason` — ASSUMPTION |
| `StockAvailabilityChanged` | CNT-ACC-INTEGRATION | CNT-ACC-CATALOG | `listing_id`, `availability_indicator` — ASSUMPTION |

> [!NOTE]
> `data` field shapes above are ASSUMPTION. Exact field names, types, required/optional status, and event-specific schemas must be formally specified per event in an AsyncAPI specification before implementation. The table shows what is inferable from idea.md §6.3 context.

### 5.6 Delivery Guarantees

| Property | Value | Label |
|---|---|---|
| Delivery semantics | At-least-once | CONFIRMED — idea.md §6.5: "Outbox pattern guarantees at-least-once delivery" |
| Consumer idempotency | Required — consumers must maintain Inbox / processed message store | CONFIRMED — idea.md §6.5 |
| Ordering | Per-aggregate ordering using `aggregate_id` as partition key | CONFIRMED — idea.md §6.5: "Messages requiring ordering must carry a grouping key such as order_id or seller_order_id" |
| Dead Letter Queue | Events exceeding retry limit go to DLQ | CONFIRMED — idea.md §6.5 |

### 5.7 Event Immutability

**CONFIRMED** — idea.md §6.5: "Events are immutable after publication; corrections require a new event or explicit compensation event."

### 5.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport to bus | TLS | CONFIRMED — idea.md §9 |
| Producer authorization | Service must be authorized to publish to its topic | PROPOSAL — specific bus ACL design UNKNOWN |
| Consumer authorization | Service must be authorized to subscribe to relevant topics | PROPOSAL |
| PII in event payloads | Minimize PII; audit events must not expose sensitive personal data | CONFIRMED — idea.md §9: privacy |

### 5.9 Versioning

UNKNOWN — event schema evolution strategy (backward-compatible expansion, versioned event types, schema registry) not specified in idea.md.  
**Consequence:** Breaking event schema changes would affect all 6 consumers simultaneously.  
**Owner:** OWNER_UNASSIGNED  
**Revisit trigger:** Before any consumer service moves to implementation; requires AsyncAPI contract and schema registry decision

### 5.10 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-005 | Integration via APIs and events with Outbox/Inbox and idempotency |
| Supporting view | resilience-observability.md | Outbox/Inbox pattern, DLQ policy |
| Container | CNT-ACC-EVENTBUS | Infrastructure container |

---

## 6. IF-ACC-LICENSE-VALIDATE

### 6.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-LICENSE-VALIDATE | CONFIRMED — registry/interfaces.json |
| Version | v1 (subject to OpenAPI contract) | ASSUMPTION |
| Protocol | HTTPS REST / JSON (online path); local signed entitlement token (offline path) | CONFIRMED — idea.md §4.3: "validates license at activation and periodically; or locally from short-lived signed entitlement" |
| Contract type | Synchronous REST (online) + local signed token verification (offline) | CONFIRMED — idea.md §4.3, ADR-014 |

### 6.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACC-LICENSE | License & Entitlement Management |
| Consumer | CNT-ACR-CONNECTOR | Platform Connector (ACCore) |
| Consumer | CMP-CON-LICENSECHECK | License Validator (ACCore) |

### 6.3 Purpose

Allows the ACCore backend to validate that an institution holds a valid, active license for the product or module it is attempting to use. Validates product, modules, seat/capacity limits, validity period, and license status. CONFIRMED — idea.md §4.3: "ACCore backend validates against License & Entitlement Management via documented service channel, or locally from short-lived signed entitlement per interruption policy."

> **Scope & Identity Note:** This interface contract documents the **Institutional License Validation** path (`institution_id + product_code`). For marketplace software licenses purchased by end-users/organizations on ACCommerce, validation is performed against the marketplace license registry using `{buyer_id, product_id}` (or `license_id`). As defined in `dynamic-license-flow.md §7` and `FN-LIC-VALIDATE`, institutional licenses and marketplace software licenses represent separate business workflows with distinct identity attributes and must not be conflated.

### 6.4 Request Schema (Online Path)

**Endpoint** (CONFIRMED from idea.md §6.2 — reference only):

```
POST /v1/licenses/validate
```

**Request body (shape — ASSUMPTION):**

```json
{
  "idempotency_key": "string",
  "institution_id": "string",
  "product_code": "string",
  "module_codes": ["string"],
  "seat_count": "integer | null",
  "installation_id": "string | null",
  "correlation_id": "string"
}
```

**Response body — valid license (ASSUMPTION):**

```json
{
  "license_id": "string",
  "status": "ACTIVE",
  "entitlement": {
    "product": "string",
    "modules": ["string"],
    "max_seats": "integer | null",
    "capacity_limit": "object | null",
    "valid_from": "ISO-8601",
    "valid_until": "ISO-8601",
    "grace_period_days": "integer"
  },
  "signed_entitlement_token": "string (JWT or similar)",
  "token_expires_at": "ISO-8601"
}
```

**Response body — invalid/suspended license (ASSUMPTION):**

```json
{
  "license_id": "string | null",
  "status": "SUSPENDED | REVOKED | EXPIRED | NOT_FOUND",
  "reason": "string",
  "grace_period_remaining_days": "integer | null"
}
```

### 6.5 Offline Validation Path

CONFIRMED — idea.md §4.3, ADR-014: "ACCore validates locally from a short-to-medium lived signed entitlement per interruption policy." The `signed_entitlement_token` returned in the online response is a locally verifiable signed credential (ASSUMPTION: JWT with platform signing key). ACCore caches and verifies this token locally without network connectivity, within its TTL. After TTL expiry, ACCore must re-validate online. Grace period behavior: UNKNOWN — specific grace period duration is an open decision (idea.md §12).

### 6.6 Idempotency

CONFIRMED — idea.md §6.5. `idempotency_key` required for validation requests. Online validation may be safely retried.

### 6.7 Error Cases

| Scenario | Handling |
|---|---|
| License not found | Return `NOT_FOUND`; ACCore must refuse to activate restricted module |
| License suspended/revoked | Return `SUSPENDED`/`REVOKED`; ACCore must restrict module usage |
| License expired + within grace period | Return `EXPIRED` with `grace_period_remaining_days`; ACCore allows usage per policy |
| License expired + past grace period | Return `EXPIRED`; ACCore must restrict usage |
| Service unavailable | Use cached `signed_entitlement_token` if within TTL; fail closed if expired | CONFIRMED — idea.md §4.3 |
| Seat limit exceeded | Return error with current/max seat counts; ACCore must refuse additional activations |

### 6.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport | TLS | CONFIRMED |
| Service-to-service auth | OAuth 2.0 Client Credentials (ACCore → License service) | CONFIRMED — idea.md §4.3: "via documented service channel with S2S auth" |
| Signed entitlement token | Platform signing key; short TTL; not forged by ACCore | CONFIRMED — idea.md §4.3; signing key management per ADR-014 |
| License ≠ Permission | License validates what can RUN; does not grant platform user permissions | CONFIRMED — idea.md §9, §3.1.1 |

### 6.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-010 | License Management and Identity are separate services |
| ADR | ADR-014 | Offline license validation via signed entitlement token |
| Component | CMP-LIC-ENTITLEMENT | Entitlement Evaluator — executes validation logic |
| Component | CMP-LIC-OFFLINE | Offline Credential Issuer — produces signed entitlement token |
| Component | CMP-CON-LICENSECHECK | ACCore-side license check component |
| Function | FN-LIC-VALIDATE | License validation function spec |

---

## 7. IF-ACC-SOFTDL

### 7.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACC-SOFTDL | CONFIRMED — registry/interfaces.json |
| Version | v1 (subject to OpenAPI contract) | ASSUMPTION |
| Protocol | HTTPS REST / JSON (metadata); HTTPS redirect to signed CDN URL (download) | CONFIRMED — idea.md §2.1.1: "signed URLs with time limits"; §6.2: `GET /v1/public/downloads/{asset_id}` |
| Contract type | Synchronous REST | CONFIRMED |

### 7.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACC-SOFTCAT | Software Catalog & Release Distribution |
| Consumer | CNT-ACM-PUBLIC | ACManagement Public Portal |
| Consumer | ACT-VISITOR | Public Portal Visitor |
| Consumer | ACT-INST-ADMIN | Institution Administrator |

### 7.3 Purpose

Provides public access to ACC software product catalog, release metadata, and secure download links for installers. The public portal (CNT-ACM-PUBLIC) consumes this to render public-facing software product and release pages. Visitors and institution admins can browse releases and obtain download links. CONFIRMED — idea.md §2.1.1, §7.7.

### 7.4 Request/Response Schema

**Endpoints** (CONFIRMED from idea.md §6.2 — reference only):

```
GET /v1/public/software-products
GET /v1/public/software-products/{product_code}/releases
GET /v1/public/downloads/{asset_id}
```

**Software product listing response (ASSUMPTION):**

```json
{
  "products": [
    {
      "product_code": "string",
      "name": "string",
      "description": "string",
      "current_version": "string",
      "supported_platforms": ["string"],
      "release_channels": ["stable", "beta"],
      "public_url": "string"
    }
  ]
}
```

**Release listing response (ASSUMPTION):**

```json
{
  "releases": [
    {
      "version": "string",
      "channel": "string",
      "release_date": "ISO-8601",
      "supported_platforms": ["string"],
      "system_requirements": { },
      "release_notes_url": "string",
      "assets": [
        {
          "asset_id": "string",
          "platform": "string",
          "file_name": "string",
          "sha256_checksum": "string",
          "signature_ref": "string",
          "size_bytes": "integer"
        }
      ]
    }
  ]
}
```

**Download link response (ASSUMPTION):**

```json
{
  "asset_id": "string",
  "download_url": "string (signed HTTPS URL to CDN)",
  "expires_at": "ISO-8601",
  "sha256_checksum": "string",
  "signature_ref": "string"
}
```

> [!IMPORTANT]
> CONFIRMED — idea.md §7.7, §9: "SHA-256 fingerprint published for each release"; "package signature; verify before install or update"; "HTTPS download links"; "signed URLs with time limits". The download URL is a signed, time-limited redirect to EXT-PACKAGE-CDN — the actual file is not served through ACCSystem application layer.

### 7.5 Download Integrity Controls

| Control | Detail | Label |
|---|---|---|
| SHA-256 checksum | Provided per asset; consumer must verify before installing | CONFIRMED — idea.md §7.7, §9 |
| Digital package signature | Published per release; consumer must verify | CONFIRMED — idea.md §7.7, §9 |
| Signed download URL | Time-limited signed URL to CDN | CONFIRMED — idea.md §2.1.1: "signed URLs with time limits" |
| Pre-publication scan | Package scanned before publishing release | CONFIRMED — idea.md §9 |
| Filename not proof of integrity | Consumers must not treat filename/URL as integrity evidence | CONFIRMED — idea.md §9 |

### 7.6 Error Cases

| HTTP Status | Scenario | Consumer Action |
|---|---|---|
| 404 | Product/release/asset not found | Display not-found message |
| 410 | Release withdrawn | Display withdrawn notice; show latest active release |
| 403 | Access to restricted download (if applicable) | Requires institution admin login — ASSUMPTION |
| 429 | Rate limit on download endpoint | Backoff; signed URL has limited sharing window |
| 500 | CDN/catalog error | Retry after delay |

### 7.7 Versioning

UNKNOWN — versioning strategy for software catalog API not specified.  
**Consequence:** Consumer portal (CNT-ACM-PUBLIC) would break on schema changes.  
**Owner:** OWNER_UNASSIGNED  
**Revisit trigger:** Phase 1 (Marketplace Foundation / ACManagement) finalization

### 7.8 Security

| Control | Detail | Label |
|---|---|---|
| Public access | Product listing and release metadata are publicly accessible | CONFIRMED — idea.md §2.1.1: "public page and appropriate download link" |
| Download auth (optional) | Restricted releases may require institution admin login | ASSUMPTION — idea.md implies visitor access for public portal |
| WAF + rate limiting | Public endpoints protected at edge | CONFIRMED — idea.md §9: WAF, rate limiting on public endpoints |
| CDN signed URLs | Download links signed with time expiry; prevent link sharing abuse | CONFIRMED |

### 7.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-010 | Software Catalog separate from License Management |
| Container | EXT-PACKAGE-CDN | Actual binary storage; CNT-ACC-SOFTCAT generates signed URL to it |
| Container | CNT-ACM-PUBLIC | Primary consumer; renders public portal pages |
| Supporting view | security-view.md §7 | Download integrity controls |

---

## 8. IF-ACR-PUBLISH-EVENT

### 8.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACR-PUBLISH-EVENT | CONFIRMED — registry/interfaces.json |
| Version | Negotiated per institution connector deployment | ASSUMPTION |
| Protocol | HTTPS POST (outbound from ACCore via Connector) | CONFIRMED — idea.md §4.3, §7.1: "Connector sends event to Integration Gateway with institution_id, product_id, version" |
| Contract type | Outbound async event (Outbox-driven HTTP delivery) | CONFIRMED — idea.md §6.5, §7.1 |

### 8.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACR-CONNECTOR | Platform Connector (ACCore) |
| Consumer | CNT-ACC-INTEGRATION | Institution Integration Gateway |
| Consumer | CMP-INT-GATEWAY | Integration Gateway component |

### 8.3 Purpose

ACCore publishes product data changes (new listings, updates, withdrawals, stock availability changes) to ACCSystem via this interface. The connector reads from the ACCore Outbox (CNT-ACR-OUTBOX) and delivers events to the Integration Gateway. CONFIRMED — idea.md §7.1, §6.3.

### 8.4 Event Schema

**Delivery:** HTTP POST to Integration Gateway endpoint (URL: UNKNOWN — requires platform configuration)

**Envelope** (CONFIRMED from idea.md §6.4):

```json
{
  "event_id": "uuid",
  "event_type": "ProductListingPublished | ProductListingUpdated | ProductListingWithdrawn | StockAvailabilityChanged",
  "event_version": 1,
  "occurred_at": "ISO-8601 UTC",
  "producer": "accore.{institution_id}.connector",
  "institution_id": "string (platform_institution_id)",
  "aggregate_id": "string (seller_product_id)",
  "correlation_id": "uuid",
  "causation_id": "uuid | null",
  "idempotency_key": "string",
  "data": { }
}
```

**`data` for `ProductListingPublished` / `ProductListingUpdated` (ASSUMPTION):**

```json
{
  "seller_product_id": "string",
  "platform_institution_id": "string",
  "version": "integer",
  "listing_data": {
    "name": "string",
    "description": "string",
    "price": { "amount": "decimal", "currency": "string" },
    "availability_indicator": "string",
    "category": "string",
    "images": ["url"],
    "permitted_fields": ["name", "description", "price", "..."]
  }
}
```

### 8.4.1 Publication Contract Semantics Summary

| Topic | Contract rule |
|---|---|
| Owning party | ACCore owns source product data and publication intent; ACCSystem owns the published listing, derived search projection, and listing lifecycle |
| Direction | ACCore → ACCSystem via connector | 
| Interaction pattern | Async event/message with outbox + retry; not a synchronous final-result contract | 
| Endpoints | Outbound HTTP delivery from ACCore connector to Integration Gateway, followed by internal ACCSystem event bus / catalog processing |
| Success outcome | Accepted publication results in assigned or retained `listing_id`; ACCSystem marks the listing active or updated |
| Rejection outcome | Validation or permission failures return a non-success response and must not create or mutate the listing |
| Duplicate delivery | Same `event_id` / `idempotency_key` is de-duplicated; duplicates are ignored |
| Out-of-order update | Older versions must not overwrite newer `version` values; stale messages are rejected or ignored |
| Acknowledgment semantics | HTTP 200/202 from the connector means the event was accepted for processing; it is not proof that search indexing or downstream consumers have finished |
| `listing_id` timing | `listing_id` is assigned on first accepted publish and retained across subsequent updates; withdrawal preserves the historical `listing_id` |
| Contract versioning | Versioning policy is outside the current package; a formal AsyncAPI schema registry is required before production use |

**`data` for `ProductListingWithdrawn` (ASSUMPTION):**

```json
{
  "seller_product_id": "string",
  "platform_institution_id": "string",
  "listing_id": "string | null",
  "reason": "string | null"
}
```

**`data` for `StockAvailabilityChanged` (ASSUMPTION):**

```json
{
  "seller_product_id": "string",
  "platform_institution_id": "string",
  "listing_id": "string | null",
  "availability_indicator": "IN_STOCK | LOW_STOCK | OUT_OF_STOCK"
}
```

> [!NOTE]
> The `data` field shapes are ASSUMPTION. Only permitted fields must be included — CONFIRMED idea.md §5.1: "This copy contains only the fields permitted for marketplace display."

### 8.5 Outbox Delivery Pattern

**CONFIRMED** — idea.md §7.1: "ACCore writes the publication record and event in a single local transaction via Outbox." The Connector reads the local Outbox and delivers to Integration Gateway. If delivery fails, it retries (CONFIRMED — idea.md §4.2: "ACCore can temporarily store integration messages and re-send on reconnection").

### 8.6 Idempotency

**CONFIRMED** — idea.md §6.5. `idempotency_key` is mandatory. The Integration Gateway must deduplicate via its Inbox. Repeated delivery of the same event produces no duplicate listing creation.

### 8.7 Error Cases

| Scenario | Handling |
|---|---|
| Integration Gateway unavailable | Connector retries with exponential backoff; Outbox retains event |
| Schema validation failure at gateway | Gateway returns 422; Connector logs and alerts; Outbox retains event |
| Institution auth rejected | Gateway returns 401/403; Connector alerts institution admin |
| Event malformed (bad JSON) | Gateway returns 400; Connector alerts |

### 8.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport | TLS (ACCore → Integration Gateway) | CONFIRMED — idea.md §4.3 |
| Service-to-service auth | OAuth 2.0 Client Credentials with rotatable institution-specific credentials | CONFIRMED — idea.md §4.3, §9 |
| `institution_id` validation | Integration Gateway validates token's `institution_id` matches payload | CONFIRMED — idea.md §9 |
| Schema and policy validation | Integration Gateway validates against publication schema and policies | CONFIRMED — idea.md §7.1 |

### 8.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-005 | Integration via Outbox/Inbox with idempotency |
| ADR | ADR-004 | ACCSystem stores marketplace projection |
| Component | CMP-CON-PUBLISHER | ACCore-side publisher |
| Component | CMP-INT-GATEWAY | Receives and validates events |
| Component | CMP-INT-PUBLICATION | Product Publication Worker — processes publication events |
| Function | FN-INT-PUBLISH | Publication function spec |
| Container | CNT-ACR-OUTBOX | ACCore outbox/inbox |

---

## 9. IF-ACR-RESERVATION-RESP

### 9.1 Identity

| Attribute | Value | Label |
|---|---|---|
| Interface ID | IF-ACR-RESERVATION-RESP | CONFIRMED — registry/interfaces.json |
| Version | v1 (subject to contract) | ASSUMPTION |
| Protocol | HTTPS REST response (synchronous) or async callback (UNKNOWN: exact delivery mode) | ASSUMPTION — idea.md §7.2 implies synchronous response in the happy path; async callback mode possible for slow reservation |
| Contract type | Synchronous REST response (from ACCore via Connector) or async event | ASSUMPTION — delivery mode is UNKNOWN |

### 9.2 Provider and Consumers

| Role | Element ID | Element Name |
|---|---|---|
| Provider | CNT-ACR-CONNECTOR | Platform Connector (ACCore) |
| Consumer | CNT-ACC-INTEGRATION | Institution Integration Gateway |
| Consumer | CMP-INT-RESERVATION | Reservation Relay |

### 9.3 Purpose

The ACCore seller's response to a reservation request initiated by the Order saga via IF-ACC-RESERVE-SAGA. ACCore validates price and stock and creates (or refuses) an expiring reservation. The response carries the reservation outcome (accepted/rejected), reservation ID, confirmed price, confirmed quantity, and expiry time. CONFIRMED — idea.md §7.2, §6.3: "ReservationAccepted / Rejected".

### 9.4 Response Schema

**`ReservationAccepted` (ASSUMPTION — exact fields require contract):**

```json
{
  "idempotency_key": "string (echoes request key)",
  "reservation_id": "string (ACCore-assigned)",
  "order_id": "string",
  "seller_order_id": "string",
  "platform_institution_id": "string",
  "status": "ACCEPTED",
  "confirmed_price": { "amount": "decimal", "currency": "string" },
  "confirmed_quantity": "integer",
  "expiry_at": "ISO-8601",
  "event_id": "uuid",
  "correlation_id": "uuid"
}
```

**`ReservationRejected` (ASSUMPTION):**

```json
{
  "idempotency_key": "string (echoes request key)",
  "reservation_id": "string | null",
  "order_id": "string",
  "seller_order_id": "string",
  "platform_institution_id": "string",
  "status": "REJECTED",
  "reason_code": "PRICE_CHANGED | INSUFFICIENT_STOCK | SELLER_INACTIVE | ITEM_DISCONTINUED | OTHER",
  "reason_message": "string",
  "event_id": "uuid",
  "correlation_id": "uuid"
}
```

> [!NOTE]
> `reservation_id` is CONFIRMED as ACCore-assigned — idea.md §5.2: \"reservation_id: ACCore-assigned; carried back in ReservationAccepted response.\" The authority for the final reservation decision lies with ACCore — this is the source-of-truth for inventory. CONFIRMED — idea.md §5: \"Actual inventory source of truth: ACCore seller.\"

> **Canonical status vocabulary (same as IF-ACC-RESERVE-SAGA):** `ACCEPTED` | `REJECTED` | `UNKNOWN`. Delivery mode: synchronous response by default; async-callback mode is available per ADR-015 connectivity configuration (PROPOSED/approval-required for specific institutions). Cross-reference: ADR-018, ADR-015.

### 9.5 Reservation Expiry

**ACCEPTED-OWNER / ADR-016** — ACCore creates an expiring reservation, but timeout or lost response is `UNKNOWN` and does not itself authorize release. The connector queries by reservation ID/idempotency key. Release/expiry occurs only under the configured policy after safe reconciliation; no fixed TTL is asserted.  
**Consequence:** Short TTL may cause reservation expiry during slow payment authorization; long TTL may hold inventory unnecessarily.  
**Owner:** OWNER_UNASSIGNED  
**Revisit trigger:** Phase 2 (Commerce Transactions) design

### 9.6 Idempotency

**CONFIRMED** — idea.md §6.5. The `idempotency_key` from the reservation request is echoed in the response. If ACCore receives a duplicate reservation request, it returns the existing reservation outcome.

### 9.7 Error Cases

| Scenario | Handling |
|---|---|
| Connector unreachable | Saga retries with same `idempotency_key` | CONFIRMED — idea.md §7.5 |
| Timeout — ACCore slow to respond | Query existing reservation status; retain UNKNOWN until definitive state or approved safe-expiry rule; compensate only after resolution | PROPOSAL |
| Invalid `order_id` / `seller_order_id` | ACCore returns 400; saga logs error |
| Duplicate response delivery | Integration Gateway deduplicates via `idempotency_key` / `event_id` |

### 9.8 Security

| Control | Detail | Label |
|---|---|---|
| Transport | TLS | CONFIRMED |
| Auth | ACCore Connector authenticated to Integration Gateway (service-to-service) | CONFIRMED — idea.md §4.3, §9 |
| `institution_id` validation | Integration Gateway validates that the response institution matches the request | CONFIRMED — idea.md §9 |

### 9.9 Cross-References

| Type | ID | Note |
|---|---|---|
| ADR | ADR-006 | Reservation at ACCore before order confirmation |
| ADR | ADR-013 | Saga pattern |
| Interface | IF-ACC-RESERVE-SAGA | The request interface this responds to |
| Component | CMP-INT-RESERVATION | Receives and relays reservation response |
| Component | CMP-ORD-SAGA | Acts on reservation outcome |
| Component | CMP-CON-RESERVATION | ACCore-side reservation handler |

---

## 10. Open Issues

| ID | Interface | Issue | Severity | Owner | Revisit Trigger |
|---|---|---|---|---|---|
| IC-001 | ALL | Versioning and backward compatibility strategy not defined for any interface | HIGH | OWNER_UNASSIGNED | Before Phase 1 API finalization |
| IC-002 | ALL | Exact field names, types, and constraints require OpenAPI/AsyncAPI formal specification — versioning strategy now partially resolved: see ADR-021 (URI-path versioning, additive-only within major version, 6-month deprecation notice) | HIGH | OWNER_UNASSIGNED | Before implementation begins |
| IC-003 | IF-ACC-PAYMENT-WEBHOOK | Payment provider webhook schema is provider-defined and may differ per provider | HIGH | OWNER_UNASSIGNED | Before Phase 3 payment provider selection |
| IC-004 | IF-ACC-EVENT-ENVELOPE | Message broker technology not specified; topics, partitioning, retention, and ACL design UNKNOWN | HIGH | OWNER_UNASSIGNED | Before Phase 1 infrastructure design |
| IC-005 | IF-ACC-RESERVE-SAGA | Reservation TTL duration not defined; impacts checkout UX and inventory hold strategy — **Partially resolved by ADR-018**: `reservation_ttl_seconds` is a request hint only; authoritative TTL is set by ACCore local policy per ADR-022; saga MUST NOT treat elapsed time as proof of expiry | MEDIUM | OWNER_UNASSIGNED | Phase 2 design; numeric policy values require approval per ADR-018 |
| IC-006 | IF-ACR-RESERVATION-RESP | Delivery mode (synchronous vs. async callback) for reservation response not confirmed — **Partially resolved by ADR-018**: synchronous by default; async-callback mode available per ADR-015 connectivity configuration, PROPOSED/approval-required for specific institutions | MEDIUM | OWNER_UNASSIGNED | Phase 2 design |
| IC-007 | IF-ACC-CATALOG-QUERY | Whether anonymous (unauthenticated) catalog browsing is permitted not specified | MEDIUM | OWNER_UNASSIGNED | Phase 1 security policy decision |
| IC-008 | IF-ACC-LICENSE-VALIDATE | Grace period duration for expired-license offline operation not specified | MEDIUM | OWNER_UNASSIGNED | idea.md §12 open decision: "offline license validation strategy" |
| IC-009 | IF-ACC-SOFTDL | Access control for restricted downloads (institutional vs. public) not fully specified | LOW | OWNER_UNASSIGNED | Phase 1 ACManagement design |

---

*This document is a reference-level contract description. It does not represent stakeholder approval, finalized API specifications, or production readiness. Formal OpenAPI/AsyncAPI specifications, provider agreements, and security review are required before implementation.*


## Remediation Addendum — Reservation and Multi-Seller Payment Contracts

`IF-ACC-RESERVE-SAGA` uses one unique reservation ID and idempotency key per SellerOrder. Its response enum is `ACCEPTED`, `REJECTED`, or `UNKNOWN`; `UNKNOWN` requires query/reconciliation and cannot trigger payment or unsafe release. Release is a separate idempotent command with `RELEASED`, `CONSUMED/COMMITTED`, or `UNKNOWN` outcome.

Payment commands carry ParentOrder, SellerOrder, seller, allocation amount, transaction currency, tax/delivery/commission basis, capture-policy ID, provider capability mode, correlation ID, and operation-specific idempotency key. The contract distinguishes authorization, capture, seller credit/transfer, commission payable, settlement, and manual payment. Aggregated provider transactions are permitted only for compatible seller policies; otherwise separate payment attempts are used.

Authentication is selected by ADR-015 policy; no interface embeds an unapproved API-key-or-mTLS alternative.
