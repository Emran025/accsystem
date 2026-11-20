# CMP-CON-ORDERRECEIVER — Order Event Receiver

**Component ID:** CMP-CON-ORDERRECEIVER  
**Container:** CNT-ACR-CONNECTOR  
**System:** SYS-ACCORE (per-institution instance)  
**C4 Level:** C3 — Component  
**Status:** DRAFT | Evidence: idea.md §4.3, §8, ADR-005

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | CMP-CON-ORDERRECEIVER |
| **Name** | Order Event Receiver |
| **Container** | CNT-ACR-CONNECTOR |
| **Responsibility** | Consumes `OrderConfirmed` events delivered from ACCSystem's Integration Layer. Triggers sales order creation in CNT-ACR-SALES. Idempotent — processes each order exactly once. Writes to ACCore's Inbox for reliable at-least-once processing. |

---

## 2. Collaborators

| Collaborator | Direction | Interface / Event | Purpose |
|---|---|---|---|
| CNT-ACC-INTEGRATION (CMP-INT-ORDERNOTIFY) | Inbound | HTTP POST or message delivery | Receives `OrderConfirmed` event payload |
| ACCore Inbox (CNT-ACR-OUTBOX/Inbox) | Write | Local DB | Persists incoming event before processing (Inbox pattern) |
| CNT-ACR-SALES | Outbound | Internal API | Creates institution sales order from confirmed marketplace order |
| CNT-ACR-INVENTORY | Outbound | Internal API | Transitions inventory reservation → `CONFIRMED` (committed sale) |
| Idempotency Store | Read/Write | Local DB | Tracks processed order_ids |

---

## 3. Data Owned

**Inbox Record:**
```
inbox_id            UUID (PK)
source_system       string ("ACCSystem")
event_type          string ("OrderConfirmed")
order_id            UUID (from ACCSystem)
payload             JSON (full OrderConfirmed event)
status              enum {RECEIVED, PROCESSING, PROCESSED, FAILED}
received_at         timestamp
processed_at        timestamp (nullable)
retry_count         integer
```

---

## 4. Behavior / Rules / State

### Processing Flow
1. Receive `OrderConfirmed` event: `{order_id, buyer_id, items:[{seller_product_id, quantity, price_snapshot}], total, payment_ref}`
2. Write to Inbox with `status=RECEIVED` (atomic — if this step fails, ACCSystem can retry)
3. Check idempotency: has `order_id` already been processed? If YES → return ACK (no-op)
4. Mark Inbox `status=PROCESSING`
5. Call CNT-ACR-SALES: create SalesOrder `{accore_order_id, acc_order_id=order_id, items, total}`
6. Call CNT-ACR-INVENTORY: confirm reservation for each item (transitions `ACCEPTED → CONFIRMED`)
7. Mark Inbox `status=PROCESSED`; store `order_id` in idempotency store

### Error Handling
- If CNT-ACR-SALES fails: mark Inbox `FAILED`; retry after backoff
- If CNT-ACR-INVENTORY confirm fails: retry; if persists → alert operations (inventory state divergence)
- ACCSystem retries delivery until it receives 200 ACK or max retries

### Idempotency
- Key: `order_id` (globally unique across ACCSystem)
- ACK returned on first processing AND on duplicates — prevents ACCSystem from retrying indefinitely

---

## 5. Failure Modes

| Failure | Detection | Mitigation |
|---|---|---|
| Duplicate `OrderConfirmed` delivery | Idempotency check on `order_id` | Return ACK; skip processing |
| CNT-ACR-SALES unavailable | Internal API failure | Retry; Inbox remains PROCESSING; alert if >N retries |
| Inbox write failure | DB error | Return 500 to ACCSystem → ACCSystem retries |
| Partial processing (Sales created, Inventory confirm fails) | Inbox status | Manual reconciliation; alert operations — inventory and sales must be consistent |
| ACCSystem sends event for wrong institution | institution_id mismatch | Reject with 403; log anomaly |

---

## 6. Security

| Concern | Control |
|---|---|
| Authentication of incoming event | ADR-015 controlled method set: OAuth 2.0 Client Credentials, mTLS, or another approved method; no arbitrary per-request selection |
| Payload validation | Validate required fields; reject malformed events with 400 |
| Institution scope | `institution_id` in event must match this ACCore instance's institution_id |
| Financial data integrity | Sales order created from ACCSystem event data; amount must match price_snapshot; ASSUMPTION: no repricing in ACCore |

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| Sales order deduplication | ACCore's SalesOrder must also be idempotent on `acc_order_id` |
| Inventory reconciliation | Periodic reconciliation between CNT-ACC-ORDERS reservation state and CNT-ACR-INVENTORY is recommended (PROPOSAL) |
| Event ordering | Multiple items per order → one `OrderConfirmed` event per order (not per item); ASSUMPTION |

---

## 8. Traceability

| Claim | Evidence |
|---|---|
| Inbox pattern for reliable event consumption | CONFIRMED (idea.md §4.3, ADR-005) |
| Sales order creation triggered by order confirmation | CONFIRMED (idea.md §4 — ACCore manages institution's sales records) |
| Idempotency on order_id | CONFIRMED (functions.json — FN-ORD-CONFIRM idempotency) |
| Financial record commitment point | UNKNOWN (idea.md §12 — open decision; this is one candidate) |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Inbound order receipt | ACCSystem delivers confirmed order payload | Order validated and written to local ACCore sales store; HTTP 200 returned |
| Duplicate order notification | Same order delivered with existing `order_id` | Idempotent acknowledgment; no duplicate local sales order created |
| Internal ACCore DB down | Local database unavailable | Rejection with HTTP 503; ACCSystem retains event in outbox for retry |
