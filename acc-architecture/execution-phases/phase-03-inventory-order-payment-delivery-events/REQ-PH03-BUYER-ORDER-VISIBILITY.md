# REQ-PH03-BUYER-ORDER-VISIBILITY — Buyer-facing order, payment and delivery status

**Document ID:** REQ-PH03-BUYER-ORDER-VISIBILITY  
**Phase:** PH-03 — Inventory, Order, Payment and External Delivery Events  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH03-BUYER-ORDER-VISIBILITY |
| Phase ID | PH-03 |
| Title | Buyer-facing order, payment and delivery status |
| Statement | Buyers see authoritative order, payment-exception and delivery status through their channel, and affected institutions receive notifications, without exposing unconfirmed outcomes as final. |
| Actors | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE |
| Locations | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-ORDERS, CNT-ACC-APIGATEWAY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE, CNT-ACC-NOTIFICATIONS, CNT-ACC-INTEGRATION, CNT-ACC-PAYMENT |
| Related function/use case | TBD (RGAP-PH03-007) |
| Status | DRAFT |
| Evidence | FR-002 steps 11-12, AC5; FR-003; CNT-ACC-NOTIFICATIONS; NFR-010 |

## 2. Scope boundary and phase handoffs

- Notification provider and channels are UNKNOWN (RGAP-PH03-011).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH03-BOV-001 | REQ-PH03-BUYER-ORDER-VISIBILITY | A buyer can view the status of own orders, including pending, unknown-review and payment-exception conditions, labelled honestly. | A buyer opens an order. | Authoritative status shown. | SYS-ACCSYSTEM, SYS-ACCOMMERCE, SYS-ACCORE | CNT-ACC-ORDERS, CNT-ACC-APIGATEWAY, CNT-ACE-MOBILEAPP, CNT-ACR-COMMERCE | AC-PH03-BOV-001-01 | TEST (planned): order visibility test | DRAFT | none recorded |
| SREQ-PH03-BOV-002 | REQ-PH03-BUYER-ORDER-VISIBILITY | The platform sends notifications for key order and payment outcomes to authorized recipients via the configured channel. | A notification-worthy event occurs. | Recipient notified. | SYS-ACCSYSTEM | CNT-ACC-NOTIFICATIONS, CNT-ACC-ORDERS | AC-PH03-BOV-002-01 | TEST (planned): notification test | OWNER_REVIEW | UNKN-001 |
| SREQ-PH03-BOV-003 | REQ-PH03-BUYER-ORDER-VISIBILITY | An order can be traced end to end by its correlation_id across checkout, reservation, payment and confirmation. | Support or operations trace an order. | One identifier links all hops. | SYS-ACCSYSTEM | CNT-ACC-ORDERS, CNT-ACC-INTEGRATION, CNT-ACC-PAYMENT | AC-PH03-BOV-003-01 | TEST (planned): trace test | DRAFT | none recorded |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH03-BOV-001 | Authorized status view | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-007) | FR-002 AC5 |
| SREQ-PH03-BOV-002 | Notifications | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-007) | FR-002 step 12 |
| SREQ-PH03-BOV-003 | Correlation traceability | ACT-INDIVIDUAL, ACT-INST-EMPLOYEE | TBD (RGAP-PH03-007) | NFR-010 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH03-BOV-001-01 | SREQ-PH03-BOV-001 | Only the buyer's own orders are returned; an unresolved outcome is never shown as confirmed or failed. | NOT SPECIFIED (source reference gap: RGAP-PH03-007) | FR-002 AC5 | FR-002 AC5 |
| AC-PH03-BOV-002-01 | SREQ-PH03-BOV-002 | Notifications contain only authorized data and are not sent for unconfirmed outcomes as final. | NOT SPECIFIED (source reference gap: RGAP-PH03-011) | CNT-ACC-NOTIFICATIONS | FR-002 step 12 |
| AC-PH03-BOV-003-01 | SREQ-PH03-BOV-003 | A trace by correlation_id spans all four steps. | NOT SPECIFIED (source reference gap: RGAP-PH03-007) | NFR-010 | NFR-010 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Notification delivery failure must not alter order state.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| UNKN-001 | SLA/availability targets per domain not defined (discovery-report.md). | SREQ-PH03-BOV-002 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH03-007 | No registered IF-* for buyer-facing order/payment/delivery status reads or notifications (FR-002 step 12 names Order/Notification APIs only). | Recorded here; route: API Governance (IC-002). |
| RGAP-PH03-011 | Notification channels, providers and templates are UNKNOWN (CNT-ACC-NOTIFICATIONS §3). | Recorded here; owner unassigned. |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-002, NFR-010
- c2-containers/accsystem/CNT-ACC-NOTIFICATIONS.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
