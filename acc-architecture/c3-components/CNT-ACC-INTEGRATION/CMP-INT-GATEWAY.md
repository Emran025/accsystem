# CMP-INT-GATEWAY — Integration Gateway

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-INT-GATEWAY |
| **Parent Container** | CNT-ACC-INTEGRATION (Institution Integration Domain — ACCSystem) |
| **Purpose** | Serves as the single entry point for all inbound connections from ACCore instances. Validates transport security, service credentials, institution identity, and event payload schema before routing to downstream handlers. Contains no business logic. |
| **Scope Boundary** | Owns connection validation and routing. Does NOT perform business logic, write to business domain data, or make decisions about reservation or publication outcomes. |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| ACCore Connector (CMP-CON-PUBLISHER, CMP-CON-RESERVATION, CMP-CON-ORDERRECEIVER) | Inbound | Source of all events and API calls from ACCore instances |
| CMP-INT-PUBLICATION | Outbound (routes to) | Receives ProductListingPublished/Updated/Withdrawn events |
| CMP-INT-RESERVATION | Outbound (routes to) | Relays reservation requests and receives validated reservation outcomes through the configured response/query or approved callback path |
| CMP-INT-ORDERNOTIFY | Outbound (routes to) | Receives outbound order event delivery requests |
| Institution Registry | Outbound (calls) | Validates `institution_id` from token against registry |
| Identity & Access (OAuth2 provider) | Outbound (calls) | Validates service credentials (client_credentials flow) |
| Audit / Event Bus | Outbound | Logs connection events and routing decisions |

---

## 3. Behavior, Rules, and State

### 3.1 Inbound Validation Steps

For every inbound request:

1. **TLS validation:** Enforce TLS 1.2+. Reject any non-TLS connection.
2. **Service credential validation:** Apply the per-institution authentication mode selected under ADR-015: OAuth2 Client Credentials and/or mTLS; API keys are not implied. Validate the authenticated principal under the selected method.
3. **Institution identity check:** Derive the institution from the authenticated principal: from the validated token claim for OAuth, or from the approved certificate-to-institution mapping for mTLS-only mode. Cross-check any request body/path `institution_id`; if it is absent where allowed, use only the authenticated binding, and if it mismatches → reject with `403 Forbidden`.
4. **Schema validation:** Validate event payload against the registered schema for the declared `event_type`. If schema fails → return structured validation error.
5. **Route:** Forward validated payload to the appropriate downstream handler based on `event_type`.

### 3.2 Routing Table

| Event Type | Handler |
|---|---|
| `ProductListingPublished` | CMP-INT-PUBLICATION |
| `ProductListingUpdated` | CMP-INT-PUBLICATION |
| `ProductListingWithdrawn` | CMP-INT-PUBLICATION |
| `ReservationAccepted` | CMP-INT-RESERVATION |
| `ReservationRejected` | CMP-INT-RESERVATION |
| `StockAvailabilityChanged` | Offer/Availability Service |

Reservation **status** includes `ACCEPTED`, `REJECTED`, `UNKNOWN` and authoritative `EXPIRED` (ADR-018). Immediate response and trusted query/reconciliation must preserve these outcomes; if a per-institution callback is approved, its versioned form routes to the relay after validation. Literal callback event names/schema for UNKNOWN or EXPIRED are not established and must not be invented from status labels.

### 3.3 Business Rules

- Gateway does **not** make business decisions. It is a validation and routing layer.
- Failed validation responses are structured errors with machine-readable codes (not raw HTTP errors).
- Gateway must be stateless. All state is managed by downstream handlers.
- Rate limiting applies per `institution_id` to prevent event flooding.

---

## 4. Data and Side Effects

| Data Item | Owned By | Description |
|---|---|---|
| Routing policy config | CMP-INT-GATEWAY | Schema registry references, event-type-to-handler map |
| Access / audit log | Audit Service | Every inbound request logged: institution_id, event_type, outcome, timestamp |

- **No business data written by Gateway itself.** All writes are downstream.
- **Stateless:** Gateway holds no per-request state across calls.

---

## 5. Failure, Security, and Operations

### 5.1 Failure Modes

| Failure | Response |
|---|---|
| TLS negotiation fails | Connection rejected at network layer |
| Token invalid / expired | `401 Unauthorized` with error code |
| `institution_id` mismatch | `403 Forbidden` |
| Schema validation failure | `422 Unprocessable Entity` with field-level error |
| Downstream handler unavailable | `503 Service Unavailable`; ACCore Connector retries with backoff |
| Schema registry unavailable | Fail open (UNKNOWN) or fail closed — needs policy decision |

### 5.2 Security

- **POLICY-CONTROLLED:** OAuth2 Client Credentials and/or mTLS per ADR-015; onboarding and security approval select the institution mode.
- Institution identity is derived from the authenticated principal, **not** from an untrusted request body: validated token claim for OAuth, or approved certificate-to-institution mapping for mTLS-only mode. Any request body identity is cross-validated against that binding.
- WAF and rate limiting enforced at edge layer before gateway (§10.1).
- No institution can send events on behalf of another institution.
- All rejected requests are logged to audit with reason.

### 5.3 Audit Events

| Event | Trigger |
|---|---|
| `IntegrationRequestReceived` | Every inbound request (success or failure) |
| `IntegrationRequestRejected` | Validation failure with reason |
| `IntegrationRequestRouted` | Successful routing to handler |

---

## 6. Verification and Tests

| Scenario | Expected Outcome |
|---|---|
| Valid request with correct credentials and schema | Routed to correct handler; `IntegrationRequestRouted` logged |
| Expired token | `401` returned; not routed |
| `institution_id` in body differs from token claim | `403` returned; not routed; audit log entry |
| Malformed event payload | `422` with field-level errors; not routed |
| Unknown `event_type` | `400 Bad Request`; not routed |
| ACCore sends request on behalf of wrong institution | `403`; audit log with security flag |
| Rate limit exceeded | `429 Too Many Requests`; alert if sustained |

---

## 7. Unknowns, Traceability, and ADR References

| Item | Status | Owner / Action |
|---|---|---|
| Exact auth mechanism: OAuth2 Client Credentials and/or mTLS per institution | UNKNOWN — ADR-015 owner/security approval required | Architecture + Security team; before Phase 1 |
| Schema registry: which service owns event schemas? | UNKNOWN | Architecture team; define before Phase 1 |
| Fail-open vs fail-closed when schema registry unavailable | UNKNOWN | Architecture + Product; before Phase 1 |

**ADR References:** ADR-005 (Outbox/Idempotency/Integration patterns), §9 (service-to-service auth)

**Requirement References:** §4.3 (ACCore communication model), §6.1 (integration patterns), §6.3 (business events), §6.5 (integration constraints)
