# CNT-ACC-PAYMENT — Payment Orchestration

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-PAYMENT |
| **Purpose** | Orchestrates payment authorization, capture, reconciliation, and refund flows with external payment providers. Provides reliable, idempotent payment operations to the Order domain. |
| **Scope Boundary** | Owns payment transaction records and payment state. Does NOT own raw card data (tokenized at provider) or order state. |

CONFIRMED (idea.md §3.1): "Payment Orchestration — إنشاء محاولات الدفع، التكامل مع مزودي الدفع، المطابقة، الاسترداد وحالة الدفع."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-ORDERS / CMP-ORD-SAGA | Inbound | Triggered by saga for payment authorization; receives refund triggers from CMP-ORD-CANCEL |
| EXT-PAYMENT-PROVIDER | Bidirectional | Outbound auth/capture/refund calls; inbound webhooks (IF-ACC-PAYMENT-WEBHOOK) |
| CNT-ACC-EVENTBUS | Outbound | Publishes PaymentAuthorized, PaymentCaptured, PaymentFailed, RefundCompleted events |
| CNT-ACC-AUDIT | Outbound | Logs all payment operations |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Provider integration | CONFIRMED (idea.md §9) | No card data storage; Tokenization/Hosted Checkout from provider |
| Webhook security | CONFIRMED (idea.md §9) | Signature verification + timing check + replay protection |
| Payment model | CONFIRMED (idea.md §12 recommendation) | Auth-then-capture; UNKNOWN: exact trigger for capture |

---

## 4. Data Owned

- Payment Attempt: `{payment_id, order_id, amount, currency, provider_reference, status, created_at}`
- Webhook event log (for reconciliation)
- Refund records

CONFIRMED (idea.md §3.1): "سجلات معاملات الدفع ومراجع المزود؛ لا تخزن بيانات البطاقة الحساسة."

---

## 5. Interfaces

- **IF-ACC-PAYMENT-WEBHOOK** (consumer): Inbound webhook from EXT-PAYMENT-PROVIDER
- Publishes PaymentAuthorized/Failed/Captured events via IF-ACC-EVENT-ENVELOPE
- Function: FN-PAY-AUTHORIZE

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Provider unreachable or timeout without final answer | Circuit breaker in CMP-PAY-ADAPTER; `PaymentUnknown` event published instead of a final failure until reconciliation confirms the provider outcome |
| Duplicate webhook received | Idempotency check on payment_id; no double-capture |
| Reconciliation discrepancy | CONFIRMED (idea.md §11): "Payment Reconciliation" metrics flagged; ops alert |
| Refund failure | RefundFailed event published; ops investigation required |

---

## 7. Security

- CONFIRMED (idea.md §9): No raw card storage; tokenization at provider
- CONFIRMED (idea.md §9): Webhook signature + replay protection
- Payment records are sensitive; access restricted to authorized services only

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): Payment reconciliation: "الفرق بين حالة الدفع في ACCSystem وحالة المزود" |
| Settlement | UNKNOWN (idea.md §12): Settlement/commissions domain — OWNER_UNASSIGNED |
| Scaling | Stateless orchestrator; payment DB is the stateful component |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-PAY-ORCHESTRATOR — Payment Orchestrator
- CMP-PAY-ADAPTER — Provider Adapter
- CMP-PAY-RECONCILIATION — Reconciliation Engine
- CMP-PAY-REFUND — Refund Coordinator

See: `c3-components/CNT-ACC-PAYMENT/`
