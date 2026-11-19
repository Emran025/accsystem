# Resilience and Observability View — ACC Ecosystem

**Artifact:** supporting-views/resilience-observability.md  
**Status:** DRAFT | Evidence: idea.md §11, §14, ADR-005, ADR-006, ADR-013

Operational values in this view are policy keys, not approved numbers. Operations/SRE owns calibration using load, SLO, recovery, legal, and audit evidence before production approval.

## 1. Resilience Patterns

### 1.1 Outbox / Inbox

| Concern | Policy |
|---|---|
| Sender crash | Write the Outbox record in the same local transaction as the business operation. |
| Duplicate delivery | Receiver Inbox and idempotency key; at-least-once delivery. |
| Delivery lag | `outbox.poll_interval` or CDC mode; value is configurable and must be calibrated by Operations/SRE. |
| Stuck messages | Monitor `outbox.stuck_age`; alert and preserve the message for safe retry/reconciliation. |
| Cleanup | `outbox.retention_policy`; deletion is prohibited while needed for deduplication, reconciliation, or audit. |
| Dispatch uncertainty | Preserve message, delivery state, and idempotency key. A local dispatch failure is not the same as possible delivery; query/retry safely. |

### 1.2 Conditional Saga Compensation

| Effect | Definitive evidence | Unknown evidence | Compensation condition |
|---|---|---|---|
| Seller reservation | ACCore `REJECTED` or confirmed accepted state | Timeout, circuit-open after dispatch, lost response | Release only confirmed accepted reservations after a definitive checkout/payment failure; release result is independently reconciled. |
| Payment authorization/capture | Provider definitive decline/void/failure or confirmed effect | Timeout, circuit-open after dispatch, lost response | Void/refund only after provider state and operation validity are established; never repeat a financial effect blindly. |
| Order confirmation | Local transaction did not commit | External effect may exist or commit status is uncertain | Query local snapshot/outbox and external states; retry transaction or reconcile, not blanket rollback. |
| Post-confirmation operations | Domain-specific definitive failure | Delivery/commit/capture result unknown | Keep explicit pending/failed/unknown state and reconcile under that domain policy. |

Compensation commands are per SellerOrder/Reservation/PaymentAttempt, idempotent, and auditable. A failed or unknown compensation becomes `COMPENSATION_PENDING/UNKNOWN`; it remains open for policy-driven retry and escalation.

### 1.3 Circuit Breaker Policy

A circuit breaker limits or prevents a new network attempt. It never determines the business outcome of a request that may already have been sent.

| Call | Open-state behavior | External-effect rule | Owner/configuration |
|---|---|---|---|
| Reservation → ACCore | Do not emit `REJECTED` merely because the circuit is open. If no dispatch is durably recorded, return a local unavailable result; if dispatch may have occurred, persist `UNKNOWN`. | Query ACCore by reservation ID/idempotency key before retry or release. | Operations/SRE: `reservation.cb.*`, calibrated from availability/recovery evidence. |
| Payment → provider | Do not emit `PAYMENT_FAILED` merely because the circuit is open. Record `AUTHORIZATION_UNKNOWN` or `CAPTURE_UNKNOWN` when dispatch may have occurred. | Provider status/reconciliation precedes retry, void, release, or capture repetition. | Operations/SRE: `payment.cb.*`, provider contract and recovery evidence. |
| Catalog validation | If no external business effect was sent, retain `PENDING_REVIEW` and return a local dependency-unavailable result. | No financial/order compensation is implied. | Operations/SRE: `catalog.cb.*`, service SLO evidence. |
| Search sync | Queue the event with its idempotency key and preserve listing state. | Retry/reconcile delivery; no listing rollback solely from circuit state. | Operations/SRE: `search.cb.*`. |
| License activation | Preserve the activation event and explicit pending state. | Query/retry idempotently; do not revoke an unknown activation without evidence. | Operations/SRE: `license.cb.*`. |

Thresholds, open/half-open behavior, deadlines, and recovery windows are policy configuration. No percentages, latency limits, retry counts, or time windows are asserted here. `fail-fast` means “do not start a new attempt”; it is not synonymous with a business failure.

### 1.4 DLQ Policy

DLQ routing is a delivery/recovery state, not proof that the target rejected or did not execute the command. Keys include `dlq.retry_policy`, `dlq.alert_policy`, and `dlq.replay_policy`, owned by Operations/SRE. Before replaying a financial or reservation command, query the source of truth using its idempotency key.

### 1.5 Idempotency Catalog

All retryable commands carry stable keys. Reservation, payment, release, void, capture, refund, order confirmation, and outbox delivery return stored results or reconcile before another side effect. Read-only validation remains locally safe to retry. Retention is governed by `idempotency.retention_policy` and must cover reconciliation/audit needs.

## 2. Observability

Metrics and alerts use named policy keys rather than unapproved thresholds. Examples include `checkout.success_rate`, `saga.compensation_rate`, `provider.call_latency`, `outbox.queue_depth`, `auth.failure_rate`, and `payment.decline_rate`. Operations/SRE owns baseline collection and approval; no target percentage, count, duration, or latency promise is asserted.

Logs use `logging.application_retention`, `logging.audit_retention`, `logging.security_retention`, and `logging.outbox_retention`, each requiring Legal/Audit/Operations review. Retention must not discard records required for reconciliation, deduplication, security investigation, or statutory audit.

Trace propagation uses correlation and idempotency identifiers. Health endpoints expose liveness/readiness; their exact probe format is a deployment standard to be selected, not an asserted numeric policy.

## 3. Fault Scenarios

| Scenario | Expected behavior |
|---|---|
| ACCore unreachable | Circuit limits new calls. Products may be marked unavailable for new checkout, but a sent reservation remains UNKNOWN until queried/reconciled. |
| Payment provider unavailable | New payment attempts may be blocked. A sent authorization/capture remains UNKNOWN; no release/void/retry until provider reconciliation. |
| Event bus degraded | Preserve outbox/inbox state; orders and notifications have explicit delivery states. |
| Identity degraded | Apply identity policy; unrelated domains do not inherit financial UNKNOWN semantics. |
| Search/catalog degraded | Preserve source-of-truth listing state and queue/retry index work. |

## 4. Recovery Procedures — INCOMPLETE PROPOSALS

| Procedure | Trigger | Steps |
|---|---|---|
| Stuck saga recovery | Configured operational policy threshold | Identify state and dispatch evidence; query the source of truth; apply only state-valid idempotent compensation; record result and escalate if still unknown. |
| Catalog re-index | Search index inconsistency | Replay source events with idempotency and verify against catalog source of truth. |
| ACCore reconnection | Connectivity restored | Resume preserved outbox messages safely; query pending reservations before replay/release. |

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready | Numeric and retention policies require owner approval and evidence.*
