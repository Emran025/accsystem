# CNT-API — Shipment API

## Identity, purpose and boundary

- Parent: `SYS-PARCELFLOW`; scope: `IN_SCOPE`; status: illustrative design, not implementation evidence.
- Purpose: validate merchant shipment submissions, coordinate carrier booking, persist/retrieve booking state, and return an outcome that `CNT-WEB` can present.
- Owns: request validation (`CMP-API-VALIDATION`), booking coordination (`CMP-API-BOOKING`), and persistence access (`CMP-API-REPOSITORY`) within the sample boundary.
- Does not own: merchant UI behavior (`CNT-WEB`), parcel data storage (`CNT-DB`), or any internal carrier behavior (`EXT-CARRIER`).
- Deployment unit, team owner, runtime and production topology: `UNKNOWN`.
- Evidence: sample system overview, scope, component records, `FN-ORDER-001`, and `interfaces/integrations/carrier-booking.md`.

## Inbound and outbound contracts

| Direction | Peer | Interaction | Current sample evidence | Open contract details |
|---|---|---|---|---|
| Inbound | `CNT-WEB` | HTTPS/JSON shipment submission and status retrieval | HTTP-style request indicated by fixture | Authentication, API versioning, schema/units, idempotency key, error envelope and rate/size limits |
| Outbound | `EXT-CARRIER` | HTTPS-style carrier booking request | External integration identified | Provider authentication, request/response fields, provider errors, timeout, retryability, rate limits, duplicate semantics and label retrieval |
| Outbound | `CNT-DB` | SQL-style persistence/read | Relational persistence indicated in fixture | Product/schema, transaction boundary, isolation, migrations, retention, backup and recovery |

These protocol/product choices are illustrative unless confirmed by an actual contract. The API must not infer carrier internals from this description.

## Behavioral responsibilities

1. Accept a request from the web boundary and establish request/correlation identity.
2. Validate required origin/destination and positive parcel dimensions as recorded by `FN-ORDER-001`; return field-specific errors before any external or persistence side effect on invalid input.
3. For valid input, coordinate the carrier booking call and persist the resulting state through the repository boundary.
4. Return or expose the booking outcome and label reference when available; allow status retrieval for the web workflow.

Steps 1, 3 and 4 describe the sample capability, not a fully specified production protocol. The fixture does not define when a booking becomes terminal, whether booking is synchronous, or how a timeout with unknown carrier outcome is reconciled.

## Data ownership and side effects

`CNT-API` orchestrates state changes; `CNT-DB` is the sample persistence owner. The entity schema, authoritative lifecycle, write ordering, transaction/compensation boundary, consistency window, tenant key, address classification, retention/deletion and label storage location are unresolved. No persistence write or carrier call should occur for a request rejected by `FN-ORDER-001`. Duplicate submissions and replay must be explicitly designed before implementation to avoid duplicate carrier bookings.

## Security and operations

The fixture does not define caller authentication, authorization roles, tenant isolation, service identity, secret management, encryption policy, audit retention, request limits, SLOs, logging/metrics/traces, on-call ownership, or recovery objectives. `HTTPS` alone is not a complete security design. Before a real deployment, define trust boundaries and identity, redact address/label data from logs, set provider timeouts and rate controls, correlate each booking across web/API/carrier/store, and document incident/manual-reconciliation procedures.

## Technology and decomposition

Python is proposed in `ADR-002` but is not accepted. The API is decomposed into the three known components above; the component records and decomposition map remain the authoritative mapping. C3 is required for this example. A coarse-grained single API is a proposal in `ADR-003`, not a stakeholder commitment.

## Risks and open decisions

| Unknown/risk | Impact | Resolution action | Owner | Revisit trigger |
|---|---|---|---|---|
| Carrier timeout/unknown outcome and duplicate booking | Duplicate labels, inconsistent state, manual support burden | Agree idempotency/reconciliation contract and failure tests | `OWNER_UNASSIGNED` — appoint integration owner | Before carrier integration implementation |
| Address/label data classification and retention | Privacy, access, storage and deletion obligations | Complete data classification and jurisdiction review | `OWNER_UNASSIGNED` — appoint data/privacy owner | Before production data is stored |
| Authentication, authorization and tenant separation | Unauthorized booking or cross-merchant data exposure | Define identity/permission model and threat review | `OWNER_UNASSIGNED` — appoint security owner | Before pilot |
| Workload, SLO and recovery objectives | Under/over-provisioning and undefined availability | Obtain workload/SLO and RTO/RPO evidence | `OWNER_UNASSIGNED` — appoint service owner | Before deployment design approval |

Disposition: `PARTIAL` for implementation. The illustrative responsibilities are documented; critical interface, data, security and operational contracts remain unresolved.
