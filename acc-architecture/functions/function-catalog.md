# Function Catalog — ACC Ecosystem

**Artifact ID:** functions/function-catalog.md  
**Status:** DRAFT | Evidence: idea.md §8, §9, registry/functions.json

> [!NOTE]
> This catalog lists all system-level functions (cross-container flows) defined in the architecture. Each function maps to one or more Operation IDs and specifies the triggering container, key components, idempotency strategy, and related ADRs.

---

## Function Registry

| Function ID | Name | Trigger | Triggering Container | Key Components | Idempotency Key | Related ADRs |
|---|---|---|---|---|---|---|
| FN-ORD-CHECKOUT | Checkout | Buyer submits cart | CNT-ACC-CART | CMP-ORD-SAGA, CMP-INT-RESERVATION, CMP-PAY-ORCHESTRATOR | `checkout_session_id` | ADR-006, ADR-007, ADR-013 |
| FN-ORD-RESERVE | Inventory Reservation | Saga step 1 | CNT-ACC-ORDERS (CMP-ORD-SAGA) | CMP-INT-RESERVATION, CMP-CON-RESERVATION | `{order_id}:{seller_id}` | ADR-006, ADR-013 |
| FN-ORD-CONFIRM | Order Confirmation | Saga step 3 (post-payment) | CNT-ACC-ORDERS (CMP-ORD-SAGA) | CMP-ORD-SNAPSHOT, CMP-ORD-STATEMACHINE | `order_id` | ADR-007, ADR-013 |
| FN-PAY-AUTHORIZE | Payment Authorization | Saga step 2 | CNT-ACC-ORDERS (CMP-ORD-SAGA) | CMP-PAY-ORCHESTRATOR, CMP-PAY-ADAPTER | `{seller_order_id/allocation_id}:{operation_key} (exact provider/payment key remains contract-gated)` | ADR-007 |
| FN-LIC-ACTIVATE | License Activation | OrderConfirmed event | CNT-ACC-LICENSE | CMP-LIC-ISSUANCE, CMP-LIC-OFFLINE | `{order_id}:{product_id}` | ADR-010, ADR-014 |
| FN-LIC-VALIDATE | License Validation | Query from ACCore or ACCommerce | CNT-ACC-LICENSE / CNT-ACR-CONNECTOR | CMP-LIC-ENTITLEMENT, CMP-CON-LICENSECHECK | n/a (read-only) | ADR-010, ADR-014 |
| FN-INT-PUBLISH | Product Publication | Publication event from ACCore | CNT-ACR-CONNECTOR / CNT-ACC-INTEGRATION | CMP-CON-PUBLISHER, CMP-INT-GATEWAY, CMP-INT-PUBLICATION, CMP-CAT-LISTING | `{product_id}:{institution_id}:{version}` | ADR-004, ADR-005 |

---

## Operation-to-Function Mapping

| Operation ID | Function ID | Description |
|---|---|---|
| OP-CHECKOUT | FN-ORD-CHECKOUT | Buyer submits cart for purchase |
| OP-RESERVE | FN-ORD-RESERVE | Reserve inventory at ACCore during saga |
| OP-ORDER-CONFIRM | FN-ORD-CONFIRM | Finalize order after payment |
| OP-PAY-AUTHORIZE | FN-PAY-AUTHORIZE | Authorize payment via payment provider |
| OP-LIC-ACTIVATE | FN-LIC-ACTIVATE | Activate license post-purchase |
| OP-LIC-VALIDATE | FN-LIC-VALIDATE | Validate entitlement (online or offline) |
| OP-PUBLISH-LISTING | FN-INT-PUBLISH | Publish product from ACCore to marketplace |

---

## Cross-Cutting Concerns

### Idempotency Strategy Summary

| Function | Strategy | Store | TTL |
|---|---|---|---|
| FN-ORD-CHECKOUT | Dedup on `checkout_session_id` | CNT-ACC-ORDERS DB | Retry/reconciliation/audit retention (exact duration policy-gated) |
| FN-ORD-RESERVE | Dedup by unique reservation/SellerOrder idempotency key in CNT-ACR-CONNECTOR | Local ACCore DB | Configured to cover retries and reconciliation; no fixed duration |
| FN-ORD-CONFIRM | Immutable confirmation record keyed independently of current fulfillment state | CNT-ACC-ORDERS DB | Retain for order/reconciliation/audit policy |
| FN-PAY-AUTHORIZE | Scoped `{seller_order_id/allocation_id}:{operation_key}`; exact provider key is contract-gated | CNT-ACC-PAYMENT DB | Retain through retry/reconciliation/audit policy |
| FN-LIC-ACTIVATE | Scoped license/order operation identity; marketplace cardinality and exact key remain owner-gated | CNT-ACC-LICENSE DB | Retain for license/reconciliation/audit policy |
| FN-LIC-VALIDATE | n/a — read-only | n/a | n/a |
| FN-INT-PUBLISH | Approved publication/change identity must distinguish update, withdrawal, and repeated stock changes; exact key or Catalog revision/tombstone is owner-gated | CNT-ACC-CATALOG DB | Retain for retry/reconciliation/audit policy |

### Error / Compensation Summary

| Function | Compensation / Rollback | ADR |
|---|---|---|
| FN-ORD-CHECKOUT | Reconcile authoritative peer outcomes; release or void only eligible known effects under guards, and retain UNKNOWN/recovery until settled | ADR-013 |
| FN-ORD-RESERVE | Release only eligible confirmed holds after authoritative failure/expiry, peer reconciliation, and UNKNOWN-safe recovery | ADR-006 |
| FN-PAY-AUTHORIZE | Void/refund via CMP-PAY-REFUND | ADR-007 |
| FN-ORD-CONFIRM | Commercial order commitment distinct from any institution-local accounting/journal commitment; cancellation is a new flow | ADR-007 |
| FN-LIC-ACTIVATE | No rollback — activation follows confirmed order; revocation is lifecycle operation | ADR-010 |
| FN-INT-PUBLISH | Idempotent upsert; no rollback — retraction is separate operation | ADR-004 |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
