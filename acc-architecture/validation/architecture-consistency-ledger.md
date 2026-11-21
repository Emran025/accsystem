# Architecture consistency ledger

**Status:** PARTIAL — structural records are present; semantic consistency, owner approval, security, finance, operations, and release readiness remain open.

## Canonical terms and boundaries

- `UNKNOWN` is a retained state after a dispatched reservation timeout, lost response, or connectivity interruption; elapsed time alone does not prove rejection or expiry.
- No numeric reservation TTL is asserted. Only authoritative ACCore `EXPIRED` evidence or trusted reconciliation may resolve expiry.
- ACCore remains the institution-owned source of truth for institutional product, inventory, sales, finance, and organization data. ACCSystem owns marketplace projections and central commerce records.
- ACCommerce, ACManagement, and ACCMared are clients/front ends of platform capabilities; they are not alternative owners of ACCSystem backend records.
- `IF-ACC-CATALOG-QUERY` remains registered at `CNT-ACC-CATALOG`; its internal C3 destination is `UNKNOWN`. `CNT-ACC-SEARCH` is a candidate only, not an asserted mapping.
- `IF-ACC-RESERVE-SAGA` terminates at the registered `CNT-ACC-INTEGRATION` boundary. Integration's relay to ACCore is a separate, currently unregistered connector leg.
- ACCore `ProductListing*` messages are source-side Outbox messages delivered through `IF-ACR-PUBLISH-EVENT`; their inclusion in an event catalogue does not establish ACCSystem Event Bus publication.

## Requirements, constraints and invariants

- Preserve per-institution isolation and the documented ParentOrder/SellerOrder and seller-specific reservation model.
- Do not infer connectivity direction, callback modality, accounting trigger, settlement policy, security approval, operational targets, or provider values from diagrams alone.
- Mermaid rendering and registry coverage are syntax/traceability evidence only; they do not establish semantic correctness or implementation behavior.
- C1 remains a black-box view of ACCSystem with people and external systems; internal containers/components belong in C2/C3. The C2 landscape retains the registered container inventory.

## Decisions and architecture rules

- Reservation uncertainty remains `UNKNOWN` until authoritative evidence or trusted reconciliation.
- The canonical ACCSystem C1 black-box view is `c1-context/context-diagram.md`; the C1 source record is `c1-context/systems/SYS-ACCSYSTEM.md`. The canonical C2 container view is `c2-containers/accsystem/container-diagram.md`; the registry-derived C2 overlay in `c1-context/c4-context-and-container-overlays.md` is only a cross-check.
- Historical findings are retained and labeled as historical; no report claims owner approval or release readiness.

## Baselines recorded after `d63a60d`

- **Schema ownership (`PROPOSED` under ADR-012):** each bounded context owns its logical schema and migrations; no context reads or writes another context's tables, including when co-hosted. ADR-012 remains `PROPOSED`; physical isolation is `OPEN` between dedicated schemas in a shared database and separate databases or instances. See `supporting-views/data-architecture.md` and `supporting-views/deployment-view.md`.
- **Physical storage (`OPEN`):** PostgreSQL and MySQL remain alternatives for ACCSystem pending workload, migration/portability, backup/restore, residency, and operations evidence. ACCore's owner-directed MySQL use does not decide ACCSystem's engine.
- **License delivery (`PROPOSED` baseline):** outbound-initiated ACCore connectivity is the ADR-015 baseline for firewalled institutions; polling, long-polling, or a persistent channel are candidate mechanisms, and protected inbound remains optional. No token-delivery interface, receiver, ACK contract, retry owner, or wire schema is registered or selected.
- **Payment/reconciliation boundary:** reconciliation may record evidence/discrepancies and raise alerts. `CMP-PAY-ORCHESTRATOR` is not assigned `SellerCredit*` or settlement-event publication; corrective-command authority and route remain open.
- **Arrow convention:** ADR-020 describes the logical interaction initiator, not physical network-connection initiation; response/callback flow may be reverse. The reversible convention remains `OWNER-REVIEW-REQUIRED` and `NOT STAKEHOLDER-APPROVED`.
- **Publication-event boundary:** ACCore Outbox messages, Integration processing/audit records, and Catalog state events are distinct event families. The Catalog-to-Event-Bus-to-Search-Sync path is recorded in C3; exact Catalog event names/schemas and mapping from ACCore Outbox messages to Catalog state events remain open.

## Open decision gates

- Internal target and service mapping for `IF-ACC-CATALOG-QUERY`; do not resolve this by assuming Search or a particular Catalog component.
- Owner review of ADR-012's proposed bounded-context schema-ownership rule and operations selection of physical isolation (dedicated schemas in a shared database versus separate databases/instances), plus ACCSystem engine, deployment, DDL/migration portability, and operational selection.
- Owner review of ADR-018's UNKNOWN-safe technical baseline and a versioned ACCore/institution reservation contract: connector-leg interface, response/query or callback modality, expiry evidence, idempotency, notification, and reconciliation.
- License token format/trust/key policy, receiver, delivery interface/channel, acknowledgement semantics, retry ownership, activation correlation, and lifecycle timing.
- Exact Catalog event names/schemas and mapping from ACCore `ProductListing*` messages to Catalog state events, plus any additional routes or consumers beyond the C3-recorded Catalog-to-Event-Bus-to-Search-Sync path.
- Institutional accounting/finance trigger, settlement evidence, correction-command authority/route, payment events, and operational policies.
- Owner/stakeholder review of ADR-020's logical-arrow convention and source-level relationship semantics.
- Security, legal, operations, stakeholder approval, and production-readiness evidence.
