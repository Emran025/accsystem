# ACC Ecosystem Architecture

Architecture documentation for the ACC Ecosystem: a central marketplace and platform-management control plane integrated with a separate ERP instance operated by each institution, plus the client applications and external services around them. This repository describes the intended system boundaries, interfaces, decisions, flows, and validation status; it is **not application source code or a deployable implementation**.

> **Status — current snapshot, 20 November 2026:** The package contains C1–C3 architecture views and a registry-first audit. Its semantic review is **incomplete**. The reservation contract now consistently preserves `UNKNOWN` after elapsed time or a lost response; only authoritative `EXPIRED` or trusted reconciliation may resolve expiry, and no numeric TTL is asserted. Connectivity, interface modality, accounting, diagram-scope, security, operations, and ownership questions remain open. Historical audit findings are retained in validation reports and are not current closure claims. This documentation does not establish stakeholder approval, security or legal compliance, production readiness, or implemented behavior.

## Start here

- [Discovery and system boundaries](acc-architecture/00-discovery/discovery-report.md) introduces the systems, actors, external dependencies, ownership boundaries, and integration surface.
- [Scope and requirements](acc-architecture/01-scope/scope-and-requirements.md) records functional requirements, non-functional requirements, constraints, assumptions, and open decisions.
- [System landscape](acc-architecture/c1-context/landscape.md) is the portfolio-level map. The [C1/C2 context and container overlays](acc-architecture/c1-context/c4-context-and-container-overlays.md) provide the focal system and container views.
- [Current validation status](acc-architecture/validation/validation-status.md), the [audit findings](acc-architecture/validation/c4-microservices-audit-findings.md), and the [remediation plan](acc-architecture/validation/c4-microservices-remediation-plan.md) explain what is verified and what still needs review.

For a first pass, read those in order. Then use the sections below to go deeper by system, architecture level, or concern.

## What the architecture describes

**ACCSystem** is the platform-operated marketplace and platform-management control plane. It owns marketplace projections of institution products, central carts and orders, payment transaction records, delivery records, platform identity and administration, software-release metadata, licensing, and integration state. It is not a unified ERP.

**ACCore** is an institution-owned ERP operated as an independent instance for each institution. Each instance is the source of truth for that institution’s product master, actual inventory, local sales and finance records, and employee and organization data. ACCSystem holds marketplace projections and central commerce records; it does not own institution ERP databases or card-sensitive payment data.

The surrounding applications are clients of platform capabilities: **ACCommerce** provides the individual-buyer shopping experience; **ACManagement** separates a public software portal from a protected administration console; **ACCMared Supervisor** and **ACCMared Courier** are delivery-operations clients. The external boundaries include payment provider(s) and software-package CDN/object storage. The [system landscape](acc-architecture/c1-context/landscape.md) and each [system context record](acc-architecture/c1-context/systems/) document their roles and relationships. Some arrow-direction semantics in the C1 material are under review; consult the caveats below before treating a drawn arrow as an approved network or data-flow contract.

The registry currently identifies **113 elements** across **7 systems, 30 C2 containers, and 28 C3 components**, with the C3 components grouped into seven selected container decompositions. It also records **7 operations, 9 interfaces, 7 functions, and 22 decisions**. These are inventory counts, not proof that every relationship is semantically complete or approved. The [canonical registries](acc-architecture/registry/) are the structured inventory; C3 decomposition exceptions and their rationales are documented separately.

## Architecture navigation

### C1 — systems and context

- [Portfolio landscape and actor/system registry](acc-architecture/c1-context/landscape.md)
- [System context records](acc-architecture/c1-context/systems/)
- [C1/C2 overlays](acc-architecture/c1-context/c4-context-and-container-overlays.md)

### C2 — containers and boundaries

- [ACCSystem container diagram](acc-architecture/c2-containers/accsystem/container-diagram.md)
- [ACCSystem container records](acc-architecture/c2-containers/accsystem/)
- [ACCore container records](acc-architecture/c2-containers/accore/)
- [ACCommerce container record](acc-architecture/c2-containers/accommerce/)
- [ACManagement container records](acc-architecture/c2-containers/acmanagement/)
- [ACCMared container records](acc-architecture/c2-containers/accmared/)

### C3 — component decompositions

The seven selected C3 decompositions are under [`c3-components/`](acc-architecture/c3-components/): Catalog, Identity, Integration, License, Orders, Payment, and the ACCore Connector. Each decomposition directory contains its component diagram and the registered component descriptions.

### Cross-cutting views

- [Interface contracts](acc-architecture/supporting-views/interface-contracts.md) and the structured [interface registry](acc-architecture/registry/interfaces.json)
- [Multi-seller purchase flow](acc-architecture/supporting-views/dynamic-purchase-flow.md)
- [Product publication flow](acc-architecture/supporting-views/dynamic-publication-flow.md)
- [License activation flow](acc-architecture/supporting-views/dynamic-license-flow.md)
- [Data architecture](acc-architecture/supporting-views/data-architecture.md) and [financial ledger/settlement](acc-architecture/supporting-views/financial-ledger-and-settlement.md)
- [Security](acc-architecture/supporting-views/security-view.md), [resilience and observability](acc-architecture/supporting-views/resilience-observability.md), and [deployment](acc-architecture/supporting-views/deployment-view.md)
- [Policy and launch gates](acc-architecture/supporting-views/policy-and-gates.md)

### Decisions and registries

- [Architecture Decision Records and stakeholder review gate](acc-architecture/decisions/)
- [Architecture manifest](acc-architecture/registry/architecture-manifest.json)
- [Element registry](acc-architecture/registry/elements.json), [decomposition map](acc-architecture/registry/decomposition-map.json), [interface registry](acc-architecture/registry/interfaces.json), [function registry](acc-architecture/registry/functions.json), and [decision registry](acc-architecture/registry/decisions.json)

## Core documented invariants

- Each institution’s ACCore data is isolated from other institutions; ACCSystem product and availability data are marketplace projections, not the institutional source of truth.
- A multi-seller cart is represented by one `ParentOrder` and a seller-specific `SellerOrder` for each seller. Inventory reservation is owned by the relevant ACCore, not by a central stock projection.
- A timeout or lost response after dispatch is not by itself proof of acceptance or rejection. The safe-flow documentation uses `UNKNOWN`, query/reconciliation, and idempotency rather than assuming an outcome.
- Client applications do not own the platform’s order, payment, license, or delivery backend records. ACManagement and ACCMared are front ends for ACCSystem services.
- Technology choices, hosting details, service deployment evidence, and configurable commercial or operational policies remain open where the source documents label them `UNKNOWN`, `PROPOSED`, or owner-dependent.

These statements summarize the documented model. Where a contradiction exists, the current source-of-truth question is called out below rather than silently resolved here.

## Current review status and open questions

The manifest records C1–C3 structural stages as passed, C4 as not started, and validation as in progress; these statuses do not certify semantic completeness or owner approval. The V5 audit distinguishes literal registry-ID coverage from semantic completeness: all selected C1, C2, and C3 IDs were found in views, but that result does not certify their relationships or the design. The latest detailed status is in [`validation/validation-status.md`](acc-architecture/validation/validation-status.md).

The following issues remain open and materially affect implementation or interpretation:

- **Reservation timeout and expiry:** the interface row now preserves `UNKNOWN` until authoritative ACCore `EXPIRED` or trusted reconciliation. The versioned institutional contract, notification/connectivity behavior, policy calibration, and executable acceptance evidence remain open; no TTL value is asserted here.
- **ACCore connectivity:** sources describe outbound-initiated connectivity as the default for firewalled institutions and protected inbound connectivity as optional, while some views can be read as requiring direct inbound access.
- **Reservation response contract:** response terms and synchronous-versus-callback delivery differ across interface and component documents.
- **Accounting trigger:** reservation consumption, SalesOrder creation, and financial journal posting are not established as one universal event; the accounting trigger is institution-dependent or unresolved.
- **Diagram scope and direction:** some C1/C2 views may be intentionally partial, two ACCSystem C2 views have no declared precedence, and arrow meaning is not consistently distinguished from caller, data-flow direction, or dependency.
- **Supporting diagram rendering:** the two previously failing supporting sequence diagrams now render successfully; the full Mermaid validator also renders the discovered Mermaid blocks with the available renderer. Rendering is tool evidence, not semantic approval. Any older report saying those two blocks still fail is historical.
- **Decision-gate count:** the current decision registry and numbered ADR files each contain 22 entries. Any older report citing 17 or 14 is historical/stale and must not be used as the current denominator.

See the [cross-level consistency report](acc-architecture/validation/c4-diagram-consistency-report.md), [completeness audit](acc-architecture/validation/c4-completeness-audit.md), and [testable remediation plan](acc-architecture/validation/c4-microservices-remediation-plan.md) for evidence, owners, approval gates, and acceptance criteria. The remediation plan is the appropriate place to track closure; this README does not mark open items resolved.

## Governance and change discipline

The package distinguishes `CONFIRMED`, `PROPOSED`, `ASSUMPTION`, and `UNKNOWN` claims. Preserve those distinctions when editing. Registry IDs and parent-child relationships should remain traceable across the registries, specifications, and views. Record a proposed architecture choice as proposed until an authorized stakeholder accepts it; AI-generated analysis is not stakeholder approval. The [stakeholder review gate](acc-architecture/decisions/ADR-STAKEHOLDER-REVIEW-GATE.md) describes its sign-off process, subject to reconciling the ADR count noted above.

No top-level `LICENSE` file is included in this package. This README does not grant open-source reuse rights; confirm the applicable rights before redistributing or reusing the architecture material.
