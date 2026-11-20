# CMP-PAY-REFUND — Refund Coordinator

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-PAY-REFUND |
| **Parent Container** | CNT-ACC-PAYMENT (Payment Orchestration — ACCSystem) |
| **Purpose** | Initiates and tracks payment refunds for cancelled or failed orders. Called by CMP-ORD-CANCEL or as part of saga compensation via CMP-ORD-SAGA. Coordinates with CMP-PAY-ADAPTER for provider-side refund execution. |
| **Scope Boundary** | Owns refund request records and their lifecycle. Does NOT make cancellation decisions — triggered by Order domain. |

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CMP-ORD-CANCEL | Inbound | Triggers refund for cancelled orders |
| CMP-ORD-SAGA | Inbound | Compensation: triggers void/refund when order confirmation fails after payment |
| CMP-PAY-ADAPTER | Outbound | Calls external payment provider for refund execution |
| CNT-ACC-EVENTBUS | Outbound | Publishes RefundCompleted/RefundFailed events |
| CNT-ACC-AUDIT | Outbound | Logs all refund operations |

---

## 3. Behavior, Rules, and State

- Receives a scoped refund/void command with `{order_id, payment_id, seller_order_id, allocation_id, amount, currency, operation_id, reason}` plus the authoritative provider authorization/capture reference when known; if the reference is not present, the coordinator loads it atomically from the payment record and rejects/quarantines when it cannot establish the correct scope. This is an internal command shape, not a new external wire contract.
- Checks payment record state and scoped SellerOrder/payment allocation via CMP-PAY-ORCHESTRATOR; an operation is eligible only when the authoritative state, amount, currency, policy and provider capability permit it
- If payment was authoritatively Authorized and not Captured → select void only where the provider supports it and policy permits; an in-flight or uncertain capture remains UNKNOWN and is reconciled first
- If payment was authoritatively Captured → initiate only an eligible full or partial refund with positive amount, matching transaction currency and allocation scope; atomically claim the eligible remaining allocation so concurrent refunds cannot exceed it; exact eligibility and amount remain policy-gated
- Use an immutable operation identity and stable operation-specific idempotency key across redelivery and recovery of the same authorized void/refund; bind it to the payment, seller/allocation scope, amount, currency and operation type. Conflicting parameters for an existing key are rejected/reviewed. The existing `order_id + refund_attempt_number` sketch needs Finance/API/provider review to ensure distinct operations are not conflated and a retry does not generate a new financial effect. Do not advance an attempt number merely because a response was lost.
- Void applies only to an uncaptured authorization; a captured payment requires an authorized refund path. Full versus partial refund eligibility and amount follow approved policy and payment state; no automatic full refund is assumed. Lost responses remain UNKNOWN and retain the operation key.

---

## 4. Data and Side Effects

| Data Item | Owned By |
|---|---|
| Refund record: `{refund_id, order_id, payment_id, seller_order_id, allocation_id, operation_id, amount, currency, status, provider_auth_id?, provider_capture_id?, provider_ref}` | CMP-PAY-REFUND |
| Immutable operation identity and request fingerprint; conflicting reuse of an operation key is rejected/reviewed, not treated as a retry | CMP-PAY-REFUND |
| Atomic local result plus outbox intent for every terminal/provider-observed outcome; recovery republishes the intent without repeating the provider effect | CMP-PAY-REFUND / Shared Outbox |
| Provider result and approved ledger adjustment references | Payment ledger / settlement boundary; exact posting policy remains owner-gated |

---

## 5. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Provider refund call fails | Retry with configured backoff and the same operation key only after the configured recovery policy permits it; when exhausted, emit a review/DLQ state and alert Operations. Reconcile provider state before another refund attempt. |
| Payment state is authoritatively invalid for the requested operation | Record definitive rejection; no financial retry. `UNKNOWN`, `CAPTURE_REQUESTED`, `CAPTURE_UNKNOWN`, or possible prior dispatch is non-terminal: reconcile before selecting void/refund or repeating an effect. |
| Void fails or response is lost | If dispatch may have occurred, retain UNKNOWN and reconcile provider state before any retry; use the same operation key. Definitive failure follows approved recovery; unresolved cases remain pending/review. |

CONFIRMED (idea.md §7.4): "يتحقق Order Domain من قابلية الإلغاء، ثم ينسق Payment Domain عملية Void أو Refund حسب حالة الدفع."

---

## 6. Security

- Refund triggers only accepted from authorized internal services (Order domain)
- All refund operations logged — CONFIRMED (idea.md §9)
- No raw card data accessed; the coordinator passes the adapter’s required authoritative `provider_auth_id` for void or `provider_capture_id` for refund, resolved from the scoped payment record; `payment_id` is not itself substituted for a provider reference.

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Refund completion rate; refund latency. Targets: UNKNOWN |
| Risk | Partial refund logic for partial cancellation is UNKNOWN — OWNER_UNASSIGNED; revisit: returns/disputes domain design (Phase 6) |

## 8. Verification scenarios (planned, not executed)

- Known uncaptured authorization: a permitted void uses the same durable operation identity and records the authoritative result.
- Known captured payment: an approved full or partial refund validates allocation, amount and currency; no automatic amount is assumed.
- Capture or refund response lost after possible dispatch: retain `UNKNOWN`, reconcile before another financial effect, and preserve provider evidence.
- Definitive invalid state, unsupported provider capability or policy denial: record a non-terminal/definitive result according to evidence without retrying an incompatible operation.
- Concurrent capture versus void, two refund requests, conflicting same-key parameters, wrong seller/allocation scope and restart after dispatch are rejected, quarantined or reconciled without exceeding the eligible captured allocation.
- Refund/void outcome and any approved ledger adjustment link to the same scoped operation and remain distinct from seller-credit or settlement finality. These are acceptance scenarios, not runtime execution evidence.
