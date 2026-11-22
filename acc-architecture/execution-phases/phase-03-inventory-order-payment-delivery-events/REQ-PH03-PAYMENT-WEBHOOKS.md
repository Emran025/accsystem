# REQ-PH03-PAYMENT-WEBHOOKS — Provider adapter and webhook handling

**Document ID:** REQ-PH03-PAYMENT-WEBHOOKS  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-PAYMENT-WEBHOOKS |
| Phase ID | PH-03 |
| Title | Provider adapter and webhook handling |
| Statement | Provider events are authenticated, deduplicated and mapped to the scoped payment operation before any state change, and ambiguous events remain UNKNOWN. |
| Actors | ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM |
| Primary C4 containers | CNT-ACC-PAYMENT |
| Related function/use case | FN-PAY-AUTHORIZE |
| Status | DRAFT |
| Evidence | IF-ACC-PAYMENT-WEBHOOK; CMP-PAY-ADAPTER; ADR-016; IC-003 |

## 2. Scope boundary and phase handoffs

- Provider schema is external and unspecified (IC-003).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-PWH-001 | REQ-PH03-PAYMENT-WEBHOOKS | The adapter verifies signature and timestamp of each inbound webhook and rejects invalid or replayed ones. | A webhook arrives. | Only valid events proceed. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PWH-001-01 | TEST (planned): webhook security test | DRAFT | IC-003 |
| SREQ-PH03-PWH-002 | REQ-PH03-PAYMENT-WEBHOOKS | A duplicate provider event yields no repeated effect and distinct lifecycle events of one payment are not suppressed. | The provider redelivers an event. | No duplicate effect. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PWH-002-01 | TEST (planned): duplicate webhook test | DRAFT | IC-003 |
| SREQ-PH03-PWH-003 | REQ-PH03-PAYMENT-WEBHOOKS | Each provider result is applied only through the durable mapping of provider reference, payment attempt, SellerOrder and allocation, never to order_id alone. | A provider event is processed. | It affects one allocation. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PWH-003-01 | TEST (planned): mapping test | DRAFT | IC-003 |
| SREQ-PH03-PWH-004 | REQ-PH03-PAYMENT-WEBHOOKS | Provider differences are isolated in the adapter, and an open circuit breaker never defines a business outcome. | The provider is slow or unavailable. | Fail-fast without declaring failure. | SYS-ACCSYSTEM | CNT-ACC-PAYMENT | AC-PH03-PWH-004-01 | TEST (planned): breaker test | DRAFT | ADR-022-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-PWH-001 | Webhook authentication | ACT-PLATFORM-ADMIN | FN-PAY-AUTHORIZE | IF-ACC-PAYMENT-WEBHOOK §4.5 |
| SREQ-PH03-PWH-002 | Duplicate event handling | ACT-PLATFORM-ADMIN | FN-PAY-AUTHORIZE | IF-ACC-PAYMENT-WEBHOOK §4.6 |
| SREQ-PH03-PWH-003 | Scoped mapping | ACT-PLATFORM-ADMIN | FN-PAY-AUTHORIZE | CMP-PAY-ADAPTER |
| SREQ-PH03-PWH-004 | Provider isolation and breaker | ACT-PLATFORM-ADMIN | FN-PAY-AUTHORIZE | CMP-PAY-ADAPTER §3.3 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-PWH-001-01 | SREQ-PH03-PWH-001 | A bad signature or stale timestamp returns 400 and raises a security alert. | IF-ACC-PAYMENT-WEBHOOK §4.7 | IF-ACC-PAYMENT-WEBHOOK §4.5 | IF-ACC-PAYMENT-WEBHOOK §4.5 |
| AC-PH03-PWH-002-01 | SREQ-PH03-PWH-002 | Redelivery is acknowledged only from a durable completed result. | IF-ACC-PAYMENT-WEBHOOK §4.6 | CNT-ACC-PAYMENT §6 | IF-ACC-PAYMENT-WEBHOOK §4.6 |
| AC-PH03-PWH-003-01 | SREQ-PH03-PWH-003 | An event that cannot be mapped is recorded UNKNOWN for reconciliation. | IF-ACC-PAYMENT-WEBHOOK §4.4 | CMP-PAY-ADAPTER §3.1 | CMP-PAY-ADAPTER |
| AC-PH03-PWH-004-01 | SREQ-PH03-PWH-004 | Circuit-open yields unavailable or UNKNOWN per dispatch evidence, not PAYMENT_FAILED. | NOT SPECIFIED (source reference gap: RGAP-PH03-003) | resilience-observability.md §1.3 | CMP-PAY-ADAPTER §3.3 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Unknown event type: respond 200 and log; do not fail delivery.
- Dispute events alert finance and freeze the order (detail deferred with ODEC-007).

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| IC-003 | Payment-provider webhook schema is provider-defined and may differ per provider. | SREQ-PH03-PWH-001, SREQ-PH03-PWH-002, SREQ-PH03-PWH-003 |
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH03-PWH-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-003 | Payment operations (authorize, capture, void, refund) are internal adapter/orchestrator commands in CMP-PAY-ADAPTER; no registered IF-* covers them; the webhook interface is provider-defined (IC-003). | Recorded here; route: provider selection and API Governance. |

## 7. Traceability sources

- supporting-views/interface-contracts.md §4
- c3-components/CNT-ACC-PAYMENT/CMP-PAY-ADAPTER.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
