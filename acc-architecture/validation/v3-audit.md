# V3 Comprehensive Audit Register — ADR-013, Circuit Breakers, and Numeric Policies

**Scope:** Entire `acc-architecture/` directory after the `pasted_content_3.txt` pass.

## Reproducible searches

The following searches were run recursively over Markdown and JSON source files:

```text
timeout|timed out|circuit breaker|fail-fast|unavailable|connection lost|retry exhausted|dead letter
compensate|compensation|rollback|release reservation|void authorization|FAILED|REJECTED|payment failed
UNKNOWN|reconcile|idempotency|expiry|retention|archive|backoff|threshold|ASSUMPTION
numeric values with days|hours|minutes|seconds|ms|percentages|retry/attempt counts
```

The search results were read in context, not treated as automatic contradictions. No open contradiction remains in the classifications below.

## Auditable result register

| Area / representative paths | Classification | Review result |
|---|---|---|
| `decisions/ADR-013.md` context, decision table, consequences | Contradiction fixed | Replaced “every failure undo all” and blanket release/void with per-SellerOrder/Reservation/PaymentAttempt conditional compensation. Added local-before-dispatch, definitive-result, UNKNOWN-after-dispatch, compensation-pending, and configurable-retention rules. Status remains `PROPOSED`, not owner-accepted. |
| `supporting-views/resilience-observability.md` reservation circuit breaker | Safely unknown / valid configuration | Open circuit prevents a new attempt; local non-dispatch may be reported only with durable evidence. If dispatch may have occurred, state is UNKNOWN and ACCore query/reconciliation precedes retry or release. Thresholds use `reservation.cb.*`, owned by Operations/SRE. |
| `supporting-views/resilience-observability.md` payment circuit breaker | Safely unknown / valid configuration | Open circuit never emits `PAYMENT_FAILED` by itself. `AUTHORIZATION_UNKNOWN`/`CAPTURE_UNKNOWN` is persisted when dispatch may have occurred; provider reconciliation precedes retry, void, release, or capture. `payment.cb.*` is owned by Operations/SRE. |
| Outbox/connector delivery | Safely unknown / valid configuration | Dispatch uncertainty preserves message, state, and idempotency key. DLQ means delivery/recovery state, not proof of non-execution. Replay requires source-of-truth query for financial/reservation commands. |
| `FN-ORD-CHECKOUT`, `FN-ORD-RESERVE`, `FN-ORD-CONFIRM`, `FN-PAY-AUTHORIZE` | Consistent | Timeout/lost response becomes UNKNOWN; known definitive failures permit only state-valid idempotent compensation; local failure before dispatch can roll back locally. Capture modes remain seller/agreement-specific. |
| `CMP-ORD-SAGA`, `CMP-ORD-STATEMACHINE`, dynamic purchase flow | Consistent | Parent saga and seller sub-operations persist state, block dependent steps on UNKNOWN, and reconcile before compensation. No timeout-to-FAILED arrow or unconditional release remains. |
| `ADR-006` payment uncertainty rules | Consistent | Provider timeout is not final failure; state resolution precedes financial repetition or reservation release. Circuit-breaker language now distinguishes local non-dispatch from possible dispatch. |
| `CMP-PAY-ADAPTER` | Contradiction fixed | Open circuit and provider timeout preserve ambiguity; thresholds/SLIs use policy keys and Operations/SRE evidence rather than unsupported values. |
| Non-financial catalog/search/license failures | Consistent local failure / valid gate | Local validation failures may remain `FAIL`/`REJECTED` when the validator has definitive evidence. Dependency outages retain pending/queued state or local unavailable status; no financial UNKNOWN semantics are generalized unnecessarily. |
| `CMP-CAT-SEARCHSYNC`, publication/order notification/refund retry policies | Valid configuration | Explicit schedules/counts were removed. Configured backoff/recovery/DLQ policies retain idempotency and operational review. |
| Retention and archival (`ADR-013`, resilience, ADR-011) | Valid configuration/gate | Fixed `90 days`, `7 days`, `30 days`, `1 year`, `7 years`, and session-hour examples were removed. Policy keys require Operations/SRE, Legal, Security, or Audit approval and must preserve reconciliation/audit state. |
| Remaining numeric values in source | Valid gate / technical syntax | Identifiers, HTTP status codes, data types, version numbers, and explicitly sourced protocol/domain values are not operational defaults. No unsupported ASSUMPTION/PROPOSAL numeric policy remains. |

## Cross-document invariants verified

1. Unknown is not rejection or definitive failure.
2. A sent reservation/payment command with no final response blocks dependent steps and enters query/reconciliation.
3. Release, void, refund, capture retry, and reservation retry require resolved state and idempotency evidence.
4. Compensation is per effect, idempotent, and remains pending/unknown when its result is uncertain.
5. Multi-seller MVP and seller/agreement-specific capture modes remain intact.
6. Operational values have named policy keys and accountable owner/evidence gates.
7. Diagrams contain no timeout-to-FAILED or timeout-to-release edge for reservation/payment flows.

## Remaining gates

Only genuine external/configurable gates remain: provider selection/capability, tax/legal/residency/retention/PCI, returns/disputes, workload/SLO/DR evidence, authentication policy, and Operations/SRE calibration of circuit, retry, timeout, DLQ, and retention policy keys. These are not unresolved documentation contradictions.
