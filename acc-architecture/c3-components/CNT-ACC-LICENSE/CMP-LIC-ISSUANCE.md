# CMP-LIC-ISSUANCE — License Issuance & Activation

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-LIC-ISSUANCE |
| **Parent Container** | CNT-ACC-LICENSE (License & Entitlement Management — ACCSystem) |
| **Purpose** | Supports authorized admin-initiated institutional issuance and OrderConfirmed-triggered marketplace software issuance. Creates license records, activates entitlements, and coordinates initial offline token issuance as a separate retriable follow-up. |
| **Scope Boundary** | License creation and activation only. Does NOT manage license lifecycle transitions (CMP-LIC-LIFECYCLE) or ongoing validation (CMP-LIC-ENTITLEMENT). |

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-EVENTBUS | Inbound | Subscribes to OrderConfirmed events for marketplace software items |
| CNT-ACM-ADMIN | Inbound | Authorized platform-admin or institution-scoped admin request through platform administration, subject to role/approval policy |
| CMP-LIC-LIFECYCLE | Outbound | Hands off newly created license for lifecycle registration |
| CMP-LIC-OFFLINE | Outbound | Receives separate retriable token-issuance work: institutional ISSUED before activation/delivery, marketplace after direct ACTIVE creation |
| CNT-ACC-EVENTBUS | Outbound | Publishes LicenseIssued, LicenseActivated events |
| CNT-ACC-AUDIT | Outbound | Logs issuance events |

---

## 3. Behavior, Rules, and State

**Issuance steps:**
1. Receive an authorized platform-admin or institution-scoped admin issuance request as policy permits, or an OrderConfirmed event for marketplace issuance; check software classification for the latter. Role, institution scope and approvals remain gated.
2. If not a software product → skip (no license needed)
3. Institutional license issuance creates `ISSUED`; activation advances it to `ACTIVATED` then `ACTIVE`. Marketplace post-purchase issuance creates the license directly `ACTIVE`.
4. Associate institutional records with `institution_id + product_code`; associate marketplace records with `buyer_id + product_id` and retain `publisher_institution_id` as seller identity. Units/seats and validity remain workflow-specific.
5. Retain LicenseIssued + LicenseActivated events via Outbox at their applicable workflow transitions; event timing versus token readiness remains a contract gate. Require an atomic local follow-up intent or an approved equivalent durable discovery mechanism so a crash cannot lose separate signing/delivery work. Duplicate operations recover incomplete work without issuing another license.

**Rules:**
- Marketplace idempotency key: `order_id + product_id`; sufficiency for repeated lines/quantities remains OPEN. Institutional admin issuance has its own authorized operation identity.
- License type (per-institution, per-seat, per-unit) depends on product configuration — UNKNOWN (open decision §12)
- Validity period and grace period: UNKNOWN — to be defined per product/plan. OWNER_UNASSIGNED.

---

## 4. Data and Side Effects

| Data | Owned |
|---|---|
| License record: `{license_id, workflow, institution_id + product_code OR buyer_id + product_id, publisher_institution_id (marketplace), units, status, valid_from, valid_until, grace_policy_ref}` | CMP-LIC-ISSUANCE |
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

- Marketplace license scoped to `buyer_id`; cross-buyer license access is blocked — CONFIRMED (idea.md §9)
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
