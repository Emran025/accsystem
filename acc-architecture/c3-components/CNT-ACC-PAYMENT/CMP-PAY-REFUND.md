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

- Receives refund trigger with `{order_id, payment_id, amount, reason}`
- Checks payment record state via CMP-PAY-ORCHESTRATOR — refund only valid if payment was Authorized or Captured
- If payment was Authorized but not Captured → void the authorization (no money moved)
- If payment was Captured → initiate refund via provider
- Use a stable operation-specific idempotency key across redelivery and recovery of the same authorized void/refund; the existing `order_id + refund_attempt_number` sketch needs Finance/API/provider review to ensure distinct operations are not conflated and a retry does not generate a new financial effect. Do not advance an attempt number merely because a response was lost.
- Void applies only to an uncaptured authorization; a captured payment requires an authorized refund path. Full versus partial refund eligibility and amount follow approved policy and payment state; no automatic full refund is assumed. Lost responses remain UNKNOWN and retain the operation key.

---

## 4. Data and Side Effects

| Data Item | Owned By |
|---|---|
| Refund record: `{refund_id, order_id, payment_id, amount, status, provider_ref}` | CMP-PAY-REFUND |
| Outbox entries for RefundCompleted/RefundFailed | Shared Outbox |

---

## 5. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Provider refund call fails | Retry with configured backoff and idempotency_key; when the configured recovery policy is exhausted, emit a review/DLQ state and alert Operations. Reconcile provider state before another refund attempt. |
| Payment not in refundable state | RefundFailed event; log warning; no retry |
| Void fails or response is lost | If dispatch may have occurred, retain UNKNOWN and reconcile provider state before any retry; use the same operation key. Definitive failure follows approved recovery; unresolved cases remain pending/review. |

CONFIRMED (idea.md §7.4): "يتحقق Order Domain من قابلية الإلغاء، ثم ينسق Payment Domain عملية Void أو Refund حسب حالة الدفع."

---

## 6. Security

- Refund triggers only accepted from authorized internal services (Order domain)
- All refund operations logged — CONFIRMED (idea.md §9)
- No raw card data accessed; provider handles refund via payment_id/token

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Refund completion rate; refund latency. Targets: UNKNOWN |
| Risk | Partial refund logic for partial cancellation is UNKNOWN — OWNER_UNASSIGNED; revisit: returns/disputes domain design (Phase 6) |
