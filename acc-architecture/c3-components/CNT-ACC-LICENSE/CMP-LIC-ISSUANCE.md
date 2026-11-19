# CMP-LIC-ISSUANCE — License Issuance & Activation

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-LIC-ISSUANCE |
| **Parent Container** | CNT-ACC-LICENSE (License & Entitlement Management — ACCSystem) |
| **Purpose** | Triggered by OrderConfirmed events for software products. Creates license records, activates entitlements, and coordinates the initial optional issuance of an offline entitlement token. |
| **Scope Boundary** | License creation and activation only. Does NOT manage license lifecycle transitions (CMP-LIC-LIFECYCLE) or ongoing validation (CMP-LIC-ENTITLEMENT). |

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-EVENTBUS | Inbound | Subscribes to OrderConfirmed events |
| CMP-LIC-LIFECYCLE | Outbound | Hands off newly created license for lifecycle registration |
| CMP-LIC-OFFLINE | Outbound | Triggers initial signed entitlement token issuance (optional) |
| CNT-ACC-EVENTBUS | Outbound | Publishes LicenseIssued, LicenseActivated events |
| CNT-ACC-AUDIT | Outbound | Logs issuance events |

---

## 3. Behavior, Rules, and State

**Issuance steps:**
1. Receive OrderConfirmed event; check if order contains a software/licensed product
2. If not a software product → skip (no license needed)
3. If software product → create License record with status=Active
4. Associate license with: institution_id, product_id, units/seats (from order), validity period
5. Publish LicenseIssued + LicenseActivated events via Outbox

**Rules:**
- Idempotency key: `order_id + product_id` — same order cannot create duplicate license
- License type (per-institution, per-seat, per-unit) depends on product configuration — UNKNOWN (open decision §12)
- Validity period and grace period: UNKNOWN — to be defined per product/plan. OWNER_UNASSIGNED.

---

## 4. Data and Side Effects

| Data | Owned |
|---|---|
| License record: `{license_id, institution_id, product_id, units, status=Active, valid_from, valid_until, grace_period}` | CMP-LIC-ISSUANCE |
| Activation record: `{activation_id, license_id, activated_at}` | CMP-LIC-ISSUANCE |

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| OrderConfirmed event processed twice | Idempotency key check — no duplicate license created |
| License DB unavailable | Event reprocessed via Event Bus retry; Outbox holds events |
| Product not found in license config | Log error; alert ops; order remains Confirmed |

---

## 6. Security

- Marketplace license scoped to uyer_id; cross-buyer license access is blocked — CONFIRMED (idea.md §9)
- publisher_institution_id on license record identifies the seller; it does NOT grant the publisher access to the buyer's license entitlement data — CONFIRMED (dynamic-license-flow.md §7)
- CONFIRMED (idea.md §1.1): License ≠ user permission; issuance does not grant platform admin access

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "فشل التفعيل" monitored |
| Risk | License model types undefined (open decision §12) — OWNER_UNASSIGNED |


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Software order confirmation | `OrderConfirmed` received for software product | License record created in `ACTIVE` state; `publisher_institution_id` recorded |
| Duplicate order event | Identical `order_id` event received twice | Idempotency key prevents duplicate license creation |
| Non-software order | `OrderConfirmed` received for physical product | Component skips license issuance; no license record created |
