# Architecture consistency ledger

**Status:** PARTIAL — structural records are present; semantic consistency, owner approval, security, finance, operations, and release readiness remain open.

## Canonical terms and boundaries

- `UNKNOWN` is a retained state after a dispatched reservation timeout, lost response, or connectivity interruption; elapsed time alone does not prove rejection or expiry.
- No numeric reservation TTL is asserted. Only authoritative ACCore `EXPIRED` evidence or trusted reconciliation may resolve expiry.
- ACCore remains the institution-owned source of truth for institutional product, inventory, sales, finance, and organization data. ACCSystem owns marketplace projections and central commerce records.
- ACCommerce, ACManagement, and ACCMared are clients/front ends of platform capabilities; they are not alternative owners of ACCSystem backend records.

## Requirements, constraints and invariants

- Preserve per-institution isolation and the documented ParentOrder/SellerOrder and seller-specific reservation model.
- Do not infer connectivity direction, callback modality, accounting trigger, settlement policy, security approval, operational targets, or provider values from diagrams alone.
- Mermaid rendering and registry coverage are syntax/traceability evidence only; they do not establish semantic correctness or implementation behavior.

## Decisions and architecture rules

- Reservation uncertainty remains `UNKNOWN` until authoritative evidence or trusted reconciliation.
- The ACCSystem C2 organization has one canonical container view at `c1-context/landscape.md`; the registry-derived C2 overlay in `c1-context/c4-context-and-container-overlays.md` is retained as a cross-check. The C1 black-box context view is in `c1-context/systems/SYS-ACCSYSTEM.md`.
- Historical findings are retained and labeled as historical; no report claims owner approval or release readiness.

## Open decision gates

- Versioned ACCore/institution reservation response, expiry, callback/connectivity, notification, and reconciliation contract.
- Arrow-direction convention and C1/C2 semantic scope/precedence.
- Institutional accounting/finance trigger, settlement, payment, and operational policies.
- Security, legal, operations, stakeholder approval, and production-readiness evidence.
