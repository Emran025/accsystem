# CMP-INT-PUBLICATION — Product Publication Worker

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-INT-PUBLICATION |
| **Parent Container** | CNT-ACC-INTEGRATION (Institution Integration Domain — ACCSystem) |
| **Purpose** | Receives product publication events from ACCore instances (via CMP-INT-GATEWAY) and routes them to CNT-ACC-CATALOG for listing creation, update, or withdrawal. Uses at-least-once processing/delivery with Inbox/Outbox deduplication and idempotent effects; duplicate deliveries may occur but must not duplicate side effects. |
| **Scope Boundary** | Owns event deduplication and routing to Catalog. Does NOT own listing business logic (CMP-CAT-LISTING owns that) or schema validation (CMP-CAT-VALIDATION owns that). |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CMP-INT-GATEWAY | Inbound (called by) | Delivers validated product events after gateway routing |
| Inbox Store (DB) | Read/Write | Deduplication by `event_id` |
| CMP-CAT-LISTING | Outbound (calls) | Create / update / withdraw listing |
| CMP-CAT-VALIDATION | Outbound (calls) | Validate schema + policy before listing write |
| Outbox Table | Write | Guarantees at-least-once delivery to Catalog |
| Event Bus | Outbound | Publishes `ProductPublicationProcessed` events |

---

## 3. Behavior, Rules, and State

### 3.1 Processing Steps

1. Receive event from CMP-INT-GATEWAY: `{event_id, event_type, institution_id, data}`.
2. **Inbox check:** Query Inbox Store for `event_id`. If already processed → return cached result (deduplicated).
3. Write `event_id` to Inbox Store (mark as processing) atomically within the same transaction as the Outbox write.
4. Pass event data to CMP-CAT-VALIDATION for schema + policy check.
   - If validation fails → return structured error to ACCore (via gateway); mark inbox as `rejected`; do NOT write to Outbox.
5. Write Outbox entry targeting CMP-CAT-LISTING with the validated payload.
6. Outbox relay picks up entry and calls CMP-CAT-LISTING.
7. Mark Inbox entry as `completed` on successful delivery.

### 3.2 Event Type Mapping

| Received Event | Action on CMP-CAT-LISTING |
|---|---|
| `ProductListingPublished` | Create new listing or publish new version |
| `ProductListingUpdated` | Update existing listing fields |
| `ProductListingWithdrawn` | Mark listing as withdrawn/inactive |

### 3.3 Business Rules

- **Idempotency:** Same `event_id` → same result returned, no duplicate listing write.
- Ordering: events for the same `seller_product_id` must be processed in order. Use `seller_product_id` as the message ordering key.
- A withdrawn listing is **not deleted** — it is marked inactive; historical record preserved.
- Validation failure is returned as a structured error; it is **not** retried (the problem is with the data, not the infrastructure).

---

## 4. Data and Side Effects

| Data Item | Owned By | Description |
|---|---|---|
| Inbox record | CMP-INT-PUBLICATION | `{event_id, institution_id, event_type, status, processed_at}` |
| Outbox entry | CMP-INT-PUBLICATION | Payload to be delivered to CMP-CAT-LISTING |
| `ProductPublicationProcessed` event | Event Bus | Published on successful processing |

- **Transaction boundary:** Inbox write + Outbox write are in the same DB transaction as the validation pass.

---

## 5. Failure, Security, and Operations

### 5.1 Failure Modes

| Failure | Response |
|---|---|
| Validation fails | Structured error returned; Inbox entry marked `rejected`; no Outbox entry |
| CMP-CAT-LISTING unavailable | Outbox retries delivery with backoff |
| Duplicate event received | Inbox check returns cached result immediately |
| DB fails during Inbox/Outbox write | Transaction rolls back; event not marked processed; ACCore retries |

### 5.2 Security

- Processes only events that passed CMP-INT-GATEWAY validation (institution_id confirmed from token).
- Does not accept direct calls — always receives via gateway.

### 5.3 Audit Events

| Event | Trigger |
|---|---|
| `ProductPublicationReceived` | Event received from gateway |
| `ProductPublicationRejected` | Validation fails |
| `ProductPublicationProcessed` | Successfully delivered to Catalog |

---

## 6. Verification and Tests

| Scenario | Expected Outcome |
|---|---|
| New product published | Inbox written; Outbox entry created; Catalog listing created |
| Same event_id received twice | Second call returns cached result; no duplicate listing |
| Validation fails (missing required field) | Structured error returned; no Outbox entry |
| CMP-CAT-LISTING temporarily down | Outbox retries; eventually delivered |
| Withdrawal event | Listing marked inactive; historical record intact |

---

## 7. Unknowns, Traceability, and ADR References

| Item | Status |
|---|---|
| Ordering guarantee mechanism: Kafka partition key or DB-level ordering? | UNKNOWN — depends on message broker choice |
| Max Outbox retry count before DLQ | UNKNOWN — config decision |

**ADR References:** ADR-004, ADR-005

**Requirement References:** §6.3 (business events), §6.5 (integration constraints), §7.1 (product publication flow)
