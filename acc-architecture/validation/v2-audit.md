# HISTORICAL — NOT CURRENT CERTIFICATION — V2 Follow-up Audit — Timeout, Compensation, and Capture Consistency

**Scope:** Entire `acc-architecture/` package after the `pasted_content_2.txt` follow-up pass.

> Current status is governed by `validation/validation-status.md`, the architecture manifest, and later dated repair checkpoints. The classifications below are provenance for the V2 snapshot only.

| Search area / hit class | Classification | Evidence / action |
|---|---|---|
| `FN-ORD-CHECKOUT` timeout and compensation | Fixed | Rewritten: known final outcomes compensate confirmed effects only; unknown outcomes enter UNKNOWN/reconciliation and stop dependent steps. |
| `FN-ORD-RESERVE`, connector reservation states | Consistent | Atomic ACCore reservation, query-before-retry, idempotent release, no fixed TTL, and no timeout-as-rejection. |
| `FN-ORD-CONFIRM` local confirmation failure | Fixed/consistent | Recovery queries payment/reservation state; unknown outcomes are not blindly voided/released. |
| `CMP-ORD-SAGA` operational timeout | Consistent | Timeout is not a business outcome; state is escalated/reconciled before compensation. |
| `CMP-ORD-STATEMACHINE` | Consistent | Parent/Seller state transitions require accepted reservations and preserve UNKNOWN/payment-unknown paths. |
| Dynamic purchase flow | Consistent | Multi-seller sequence, per-seller reservations, payment policy branches, and outbox confirmation render successfully. |
| FR-002 / FR-009 scope criteria | Fixed | Safe ACCore expiry rule, no duplicate step numbering, testable unknown/recovery criteria, no universal capture rule. |
| Universal capture-after-confirmation wording | Fixed | Checkout and scope now reference seller/agreement policy; authorize-then-capture and immediate capture are separate paths. |
| Automatic release after unknown expiry | Fixed | Interface, connector, and checkout require reconciliation or a configured safe-expiry rule. |
| Remaining timeout/UNKNOWN mentions | Valid gate/state | Operational thresholds, retry schedules, saga monitoring, and provider/legal values remain configurable or external; no numeric value is asserted. |

## Checks performed

- Recursive keyword audit over timeout, compensation, release, UNKNOWN, expiry, capture, settlement, and FAILED terms.
- Cross-document semantic review of checkout, reservation, confirmation, saga, state machine, dynamic flow, FR-002, and FR-009.
- Registry JSON parsing and local Markdown-link check.
- Duplicate FR-002 step-number check.
- Mermaid rendering of affected purchase and order-component diagrams.
- ZIP integrity and input-path preservation checks.

The package's original structural/depth validators were not included in the input package or available in the workspace, so they were not run. Written acceptance criteria are not represented as executed application tests.
