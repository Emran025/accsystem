# FN-LIC-ACTIVATE — License Activation Function Specification

**Function ID:** FN-LIC-ACTIVATE  
**Operation ID:** OP-LIC-ACTIVATE  
**Status:** DRAFT | Evidence: idea.md §7, §7.3, ADR-010, ADR-014

---

## 1. Identity

| Field | Value |
|---|---|
| **ID** | FN-LIC-ACTIVATE |
| **Name** | License Activation |
| **Layer** | Async post-confirmation flow — triggered by OrderConfirmed event |
| **Triggering Component** | CMP-LIC-ISSUANCE (subscribes to OrderConfirmed via CNT-ACC-EVENTBUS) |
| **Operation ID** | OP-LIC-ACTIVATE |

---

## 2. Trigger

- **Who:** Automatic — triggered by `OrderConfirmed` event from CNT-ACC-ORDERS
- **What:** Issue a license for each software product in the confirmed order
- **How:** CNT-ACC-EVENTBUS delivers OrderConfirmed → CMP-LIC-ISSUANCE processes each software item

> [!NOTE]
> This function is **asynchronous** relative to the checkout response. The buyer receives order confirmation before license activation completes. Activation latency should be < 30 seconds (ASSUMPTION). If activation fails, it is retried — the buyer is notified when the license is ready.

---

## 3. Preconditions

| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | OrderConfirmed event received with valid payload | CMP-LIC-ISSUANCE | Reject + DLQ |
| P2 | Order item is a software product (not physical) | CMP-LIC-ISSUANCE (check CNT-ACC-SOFTCAT) | Skip item (no license for physical goods) |
| P3 | Software product exists in CNT-ACC-SOFTCAT | CMP-LIC-ISSUANCE | Retry; alert if product not found after N retries |
| P4 | License not already activated for this `{order_id, product_id}` | CMP-LIC-ISSUANCE idempotency | Return existing license (no-op) |

---

## 4. Execution Flow

```
1. CNT-ACC-EVENTBUS delivers OrderConfirmed to CMP-LIC-ISSUANCE

2. CMP-LIC-ISSUANCE:
   For each item in order.items where item.type = SOFTWARE:

   a. Idempotency check: {order_id}:{product_id} already activated?
      → YES: return existing license_id (no-op)
      → NO: continue

   b. Validate software product:
      Query CNT-ACC-SOFTCAT: does product_id exist and is ACTIVE?
      → NO: retry; alert after N failures (product must exist if order confirmed)

   c. Create License record (Marketplace Software License — see dynamic-license-flow.md §7):
      {
        license_id: UUID (generated),
        buyer_id: order.buyer_id,           ← LICENSEE / BENEFICIARY for this flow
        product_id: item.product_id,
        publisher_institution_id: item.seller_id,  ← the institution that published/sold the product; NOT the licensee
        order_id: order.order_id,
        status: ACTIVE,                     ← marketplace licenses start ACTIVE directly (no ISSUED→ACTIVATED lifecycle)
        issued_at: now(),
        expires_at: null (or subscription end — UNKNOWN per §12),
        license_type: UNKNOWN (see §12 — perpetual vs subscription)
      }

   d. CMP-LIC-OFFLINE: generate first offline entitlement token:
      {
        buyer_id,
        product_id,
        issued_at: now(),
        expires_at: now() + TOKEN_TTL (UNKNOWN — policy decision),
        signature: sign(payload, platform_private_key)
      }

   e. Store token reference in License record

   f. Publish LicenseActivated event:
      {license_id, buyer_id, product_id, institution_id, order_id, issued_at}
      → CNT-ACC-NOTIFICATIONS (notify buyer license is ready)
      → Optionally: deliver token to buyer client (mechanism: UNKNOWN)

3. Write audit entry: license issued for order_id + product_id
```

---

## 5. Postconditions

| # | Postcondition |
|---|---|
| Q1 | License record exists: status=ACTIVE, bound to buyer_id + product_id + order_id |
| Q2 | First offline entitlement token generated and stored |
| Q3 | LicenseActivated event published |
| Q4 | Buyer notification triggered |
| Q5 | Idempotency key `{order_id}:{product_id}` stored |

---

## 6. Data, Side Effects, and Idempotency

### 6.1 Data Persisted and Side Effects
- **Data Persisted:** License record `{license_id, buyer_id, product_id, publisher_institution_id, status: 'ACTIVE'}` persisted in License DB; activation record persisted with timestamp.
- **Side Effects:** Emits `LicenseActivated` event to Event Bus; generates signed offline entitlement token; writes activation audit record.
- **Transaction Boundary:** Atomic local transaction within `CNT-ACC-LICENSE` creates license and activation record.

### 6.2 Idempotency

| Field | Value |
|---|---|
| **Key** | `{order_id}:{product_id}` |
| **Store** | CNT-ACC-LICENSE DB |
| **Mechanism** | Unique constraint on (order_id, product_id); UPSERT returns existing license_id |
| **Behavior on duplicate** | Return existing `{license_id, status}` without re-creating or re-generating token |

---

## 7. Failure / Rollback

| Failure Scenario | Mitigation |
|---|---|
| Software Catalog unavailable | Retry with backoff; event stays in bus or Outbox |
| License DB write fails | Retry; idempotent UPSERT safe to retry |
| Token generation fails | Retry; license record not finalized until token generated |
| Event delivery delayed (DLQ) | At-least-once delivery; idempotency handles re-delivery |
| Buyer cancels order after activation | License revocation via CMP-LIC-LIFECYCLE (separate flow); no auto-rollback |

> [!NOTE]
> There is **no compensation / rollback** for license activation. Licenses are only revoked through the explicit lifecycle flow (CMP-LIC-LIFECYCLE). If an order is cancelled after activation, the license must be revoked as a separate business operation.

---

## 8. Security / Authorization

| Concern | Control |
|---|---|
| Caller | Only CNT-ACC-EVENTBUS event delivery (internal); no external trigger |
| Token signing | Private key held only by ACCSystem; ACCore receives only public key |
| License scope | License is buyer + product specific; cannot be transferred |
| Audit | All license issuance events written to CNT-ACC-AUDIT with actor=SYSTEM |

---

## 9. Traceability

| Claim | Evidence |
|---|---|
| License activation triggered by OrderConfirmed | CONFIRMED (idea.md §7.3 — post-purchase activation) |
| Software catalog validation at activation | CONFIRMED (idea.md §7 — Software Catalog service) |
| Offline token generation at activation | CONFIRMED (ADR-014, CMP-LIC-OFFLINE) |
| License type (subscription vs perpetual) | UNKNOWN (idea.md §12 — open decision on license model types) |
| Token TTL | UNKNOWN (idea.md §12 — open decision on offline license validation strategy) |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
