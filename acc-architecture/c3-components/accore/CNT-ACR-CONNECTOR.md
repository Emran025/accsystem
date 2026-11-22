# CNT-ACR-CONNECTOR — Platform Connector (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-CONNECTOR |
| **Purpose** | Integration bridge between an ACCore institution instance and the ACCSystem platform. Handles outbound product publication events, inbound reservation handling, inbound order event reception, and license validation. Implements Outbox/Inbox pattern for reliable messaging. |
| **Scope Boundary** | Owns integration protocol and message relay logic. Does NOT own product master data (CNT-ACR-PRODUCTMASTER) or inventory state (CNT-ACR-INVENTORY). |

CONFIRMED (idea.md §4.1): "Platform Connector — موصل التكامل، مزامنة المنتجات، استقبال الطلبات والأحداث وإرسال الردود."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-PRODUCTMASTER | Inbound | Product data for publication events |
| CNT-ACR-INVENTORY | Bidirectional | Checks and commits inventory reservations |
| CNT-ACR-SALES | Outbound | Delivers confirmed order data for sales record creation |
| CNT-ACR-OUTBOX | Bidirectional | Reads outbound events from Outbox; writes incoming events to Inbox |
| CNT-ACC-INTEGRATION | Bidirectional | IF-ACR-PUBLISH-EVENT and IF-ACR-RESERVATION-RESP are registered connector interfaces; reservation requests are relayed through CMP-INT-RESERVATION to CMP-CON-RESERVATION, but that connector leg has no registered IF-* ID and its transport/schema remain OPEN |
| CNT-ACC-LICENSE | Outbound (via IF-ACC-LICENSE-VALIDATE) | Connector requests online license validation from the license provider |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Transport | PROPOSED (ADR-015) | HTTPS/TLS is the source-stated security baseline; ADR-015 leaves the concrete transport/channel selection open. |
| Authentication | PROPOSED (ADR-015) | Per-institution security/operations policy selects OAuth 2.0 Client Credentials or mTLS; neither is enabled by client request. |
| Messaging pattern | CONFIRMED (idea.md §6.5) | Outbox/Inbox; at-least-once; idempotency keys |
| Connectivity model | PROPOSED (ADR-015) | For firewalled institutions, outbound-initiated connectivity is the proposed default using polling, long-polling, or a persistent channel. Protected inbound is optional and approval-gated; logical message direction is not a mandatory transport-initiation mode. |

---

## 4. Data Owned

- Outbox: queued outbound events (product publication, reservation responses)
- Inbox: received inbound events (reservation requests, order confirmations) with deduplication state
- ID mapping table: `{platform_institution_id ↔ local_institution_reference}`

---

## 5. Interfaces

- **IF-ACR-PUBLISH-EVENT** (provider): Product publication events → CNT-ACC-INTEGRATION
- **IF-ACR-RESERVATION-RESP** (provider): Reservation responses → CNT-ACC-INTEGRATION
- **Reservation request relay:** `IF-ACC-RESERVE-SAGA` terminates at CNT-ACC-INTEGRATION and is consumed by CNT-ACC-ORDERS / CMP-ORD-SAGA. Integration relays to CMP-CON-RESERVATION; no connector-leg IF-* ID is registered.
- **IF-ACC-ORDER-CONFIRM** (consumer): Receives authorized recipient-scoped confirmation via the selected ADR-015 channel
- **IF-ACC-LICENSE-VALIDATE** (consumer): Online license validation

---

## 6. Failure Modes

| Failure | Response |
|---|---|
| ACCSystem unreachable | Events queued in Outbox; retried with exponential backoff on reconnect — CONFIRMED (idea.md §4.2) |
| Duplicate reservation request | Inbox deduplication by idempotency_key — CONFIRMED (idea.md §6.5) |
| Reservation action fails or response is lost | Report REJECTED only with authoritative rejection evidence; otherwise preserve UNKNOWN and reconcile before repeating the effect |

---

## 7. Security

- PROPOSED (ADR-015): TLS with per-institution policy-selected OAuth 2.0 Client Credentials or mTLS, subject to security/owner onboarding approval; neither method is enabled by client request.
- CONFIRMED (idea.md §9): Institution identity included in every message
- CONFIRMED (idea.md §4.3): License validation does not expose ERP data to ACCSystem

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "Integration Health — آخر مزامنة لكل مؤسسة، زمن استجابة ACCore" |
| Offline operation | CONFIRMED (idea.md §4.2): ACCore can queue messages during connectivity loss |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-CON-PUBLISHER — Product Publication Client
- CMP-CON-RESERVATION — Reservation Handler
- CMP-CON-ORDERRECEIVER — Order Event Receiver
- CMP-CON-LICENSECHECK — License Validator (offline capable)

See: `c3-components/CNT-ACR-CONNECTOR/`


---

## 8. Open Risks and Decisions

- Connectivity mode is governed by ADR-015: outbound-initiated connector is the default for firewalled institutions; protected inbound mode is optional. Transport selection and channel parameters remain controlled operations policy.
