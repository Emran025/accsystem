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
> This function is **asynchronous** relative to the checkout response. The buyer receives order confirmation before license activation completes. Activation latency is controlled by approved Operations policy, with no numeric target established here. Failures remain recoverable; buyer notification of readiness must not precede the actually required token/readiness evidence.

---

## 3. Preconditions

| # | Precondition | Checked By | On Failure |
|---|---|---|---|
| P1 | OrderConfirmed event received with valid payload | CMP-LIC-ISSUANCE | Reject + DLQ |
| P2 | Order item is a software product (not physical) | CMP-LIC-ISSUANCE (check CNT-ACC-SOFTCAT) | Skip item (no license for physical goods) |
| P3 | Software classification and applicable catalog lookup validated where the approved mapping exists | CMP-LIC-ISSUANCE | Preserve pending work and escalate per policy if mapping or catalog result is unresolved |
| P4 | Marketplace issuance identified by `{order_id, product_id}` (key sufficiency remains OPEN) | CMP-LIC-ISSUANCE idempotency | Return existing license and recover any incomplete token/readiness work without creating another license |

---

## 4. Execution Flow

```
1. CNT-ACC-EVENTBUS delivers OrderConfirmed to CMP-LIC-ISSUANCE

2. CMP-LIC-ISSUANCE:
   For each item in order.items where item.type = SOFTWARE:

   a. Idempotency check: {order_id}:{product_id} already activated?
      → YES: return existing license_id and recover incomplete token/readiness work; no duplicate license
      → NO: continue

   b. Validate software classification and applicable catalog record where mapping exists.
      Mapping among marketplace product/listing/seller-product and software-catalog product_code
      is OPEN; preserve pending work and escalate if unavailable or unresolved.

   c. Create License record (Marketplace Software License — see dynamic-license-flow.md §7):
      {
        license_id: UUID (generated),
        buyer_id: order.buyer_id,           ← buyer-scoped record; B2B beneficiary/delegation is OPEN
        product_id: item.product_id,
        publisher_institution_id: item.seller_id,  ← the institution that published/sold the product; NOT the licensee
        order_id: order.order_id,
        status: ACTIVE,                     ← marketplace licenses start ACTIVE directly (no ISSUED→ACTIVATED lifecycle)
        issued_at: now(),
        expires_at: null (or subscription end — UNKNOWN per §12),
        license_type: UNKNOWN (see §12 — perpetual vs subscription)
      }

   d. Commit License and activation records locally. Require either an atomic local token-follow-up
      intent in that commit or an explicitly designed equivalent durable discovery/recovery mechanism;
      exact enqueue, claims, and recovery design remain OPEN. Signing is separate and retriable.
      Proposed workflow-specific claims include workflow, license_id, buyer_id, product_id,
      issued_at and expires_at; grant validity and credential TTL are distinct (ADR-014).
   e. On successful separate issuance, store the token reference and deliver it where supported.
   f. Preserve LicenseActivated and buyer notification; event-versus-token-ready sequencing
      and delivery mechanism remain OPEN. An additional institution_id must have an explicitly
      defined role/provenance; publisher_institution_id identifies the seller, not the buyer.

3. Write audit entry: license issued for order_id + product_id
```

---

## 5. Postconditions

| # | Postcondition |
|---|---|
| Q1 | License record exists: status=ACTIVE, bound to buyer_id + product_id + order_id |
| Q2 | Separate token issuance is recoverable; token is ready only when issuance succeeds |
| Q3 | LicenseActivated event is retained; its sequencing relative to token readiness remains OPEN |
| Q4 | Buyer readiness notification remains supported and must reflect the agreed readiness condition |
| Q5 | Idempotency key `{order_id}:{product_id}` stored |

---

## 6. Data, Side Effects, and Idempotency

### 6.1 Data Persisted and Side Effects
- **Data Persisted:** License record `{license_id, buyer_id, product_id, publisher_institution_id, status: 'ACTIVE'}` persisted in License DB; activation record persisted with timestamp.
- **Side Effects:** Emits `LicenseActivated` event to Event Bus; generates signed offline entitlement token; writes activation audit record.
- **Transaction Boundary:** Atomic local transaction within `CNT-ACC-LICENSE` creates license and activation records; token follow-up must be made crash-recoverable either by an atomic local intent or an approved equivalent durable discovery mechanism. Token signing, delivery and readiness events are separate, idempotent/reconcilable operations; exact design and event sequencing remain OPEN.

### 6.2 Idempotency

| Field | Value |
|---|---|
| **Key** | `{order_id}:{product_id}` |
| **Store** | CNT-ACC-LICENSE DB |
| **Mechanism** | Unique constraint on (order_id, product_id); UPSERT returns existing license_id |
| **Behavior on duplicate** | Return existing `{license_id, status}` without re-creating the license; separately resume any incomplete token follow-up. Sufficiency of this key for repeated lines/quantity remains an order/product decision. |

---

## 7. Failure / Rollback

| Failure Scenario | Mitigation |
|---|---|
| Software Catalog unavailable | Retry with backoff; event stays in bus or Outbox |
| License DB write fails | Retry; idempotent UPSERT safe to retry |
| Token generation fails or process crashes | Preserve committed activation and recover token/readiness work through the required durable intent or approved equivalent; retry/reconcile without duplicating the license or claiming readiness before signing succeeds |
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
