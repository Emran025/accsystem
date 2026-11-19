# ACC Diagram Completeness Audit

**Audit date:** 2026-11-19. **Source archive:** `acc-architecture.zip`, SHA-256 `806faea3966d0abb0b3b955360bee2529d3bd9238e5b265862ed82da76bc45ac`. **Method:** an independent reviewer started from `registry/elements.json`, cross-checked `registry/decomposition-map.json`, interfaces, functions and decisions, then inspected actual Mermaid blocks and local file paths. It did not treat the coverage matrix or plausible filenames as proof. No files were edited by the auditor.

## Registry-derived counts

- C1 software systems: **7/7** have corresponding focal C1 views and literal IDs in Mermaid.
- C2 containers: **30/30** are represented by ID in a system-level container view. All 30 have registered parents.
- C3 components: **28/28** occur in **7/7** registered C3 parent diagrams. The 28 components are grouped into seven container decompositions; there are not 28 separate component diagrams.
- Parent decomposition map: **7/7** selected C3 parent groups and **28/28** registered child IDs represented.
- Registry element records: **105**, including the above C1/C2/C3 elements plus contextual/external records, functions, and decisions. No duplicate registry IDs or names found. All 105 `doc` paths exist.
- Supporting records: **9** registered interfaces, **7** registered functions, and **14** decisions.
- Mermaid evidence: **28** fenced Mermaid blocks across **13** Markdown files. Actual diagram set includes the landscape, eight context/overlay blocks, six C2 overlays, one standalone ACCSystem container diagram, seven C3 component diagrams, and five supporting dynamic diagrams.
- Local Markdown relative file links checked: **0 unresolved targets**.

These numerators and denominators measure literal registered identity and file coverage. They do not establish semantic completeness, relationship correctness, deployment status, owner approval, or implementation behavior.

## C3 exceptions

`registry/elements.json` records **33 EXCEPTION** entries relevant to decomposition: **23** C2 containers without a C3 decomposition and **10** contextual records (eight actors and two external systems). The registry includes rationales for the 23 C2 exceptions, such as deferred UI internals, institution-owned ACCore internals, cross-cutting infrastructure, or low-complexity containers. These remain documented registry exceptions; this audit does not approve, revoke, or reinterpret them.

The coverage matrix contains rows for the 7 C1, 30 C2, and 28 selected C3 elements (65 rows), but it does not enumerate the 23 C2 decomposition exceptions as `NOT-APPLICABLE` rows or link an exception appendix. The rationale exists in the registry, so this is a matrix auditability gap, not evidence that the exception rationales are absent.

## Semantic completeness and traceability

The ACCSystem focal C1 overlay is semantically incomplete relative to `c1-context/systems/SYS-ACCSYSTEM.md` and `c1-context/landscape.md`: the view does not show several documented direct client-system relationships and CDN distribution, despite relevant system IDs appearing elsewhere in the file. A generic `ACTORS` node in focal views also does not identify which registered actors have which documented relationships. This finding is distinct from the 7/7 C1 ID-presence result.

Nine interface IDs are registered. Five were found as literal labels in Mermaid. Four—`IF-ACC-CATALOG-QUERY`, `IF-ACC-ORDER-CREATE`, `IF-ACC-EVENT-ENVELOPE`, and `IF-ACC-SOFTDL`—were not found as literal interface IDs in Mermaid. Some corresponding edges may be drawn without their interface IDs. C4 does not require an ID on every edge; this is a low-severity traceability improvement, not a claim that relationships are absent.

The independent C4 review also identified C2 views whose directly connected support elements/relationships are omitted, two materially different ACCSystem C2 diagrams without a precedence rule, duplicate focal-node/self-edges in six C1 diagrams, a title/scope mismatch in the Integration C3 diagram, and a Payment webhook route inconsistent with its component record. These are listed in `c4-diagram-consistency-report.md` and assigned separate evidence tickets in `c4-missing-items-agent-results.md` when those reports are complete.

## Syntax and link checks

`manus-render-diagram` successfully rendered all C1/C2/C3 diagrams in the reviewed source set. In total, **26/28 Mermaid blocks** rendered successfully. The two failures are in supporting views, not the C1/C2/C3 diagram set:

- `supporting-views/dynamic-license-flow.md`: renderer reported a parse error near the `end` following the “new seat activations” flow at source block line 77.
- `supporting-views/dynamic-publication-flow.md`: renderer reported a parse error at the transition to `Note over EMP` after “Search indexing complete” at source block line 73.

These failures establish that the renderer rejected the blocks, not whether the source is invalid in all Mermaid versions or viewers. Both are recorded as syntax unresolved pending a targeted parse/render pass. Successful rendering proves parser acceptance by this tool only; it does not prove semantic correctness.

## Orphans and unregistered diagram elements

No unindexed Mermaid-bearing file was found in the inspected source set. All seven component-diagram directories align to selected registered C3 parent decompositions. The completeness recount did identify support/store/helper nodes in some C3 diagrams that are not among the registered C3 component IDs. Such nodes may be valid C4 supporting containers or implementation details; whether they are approved architecture elements is `STATUS-UNKNOWN` unless a registry/specification source says otherwise. Do not treat every unregistered node as an orphan component or silently expand the registry.

## Status distinctions

- **Diagram-file existence:** present for the selected C1/C2/C3 and C3 parent diagrams reviewed.
- **Literal ID coverage:** 7/7 C1, 30/30 C2, 28/28 C3.
- **Mermaid rendering:** all C1/C2/C3 diagrams rendered; 26/28 blocks overall rendered; two supporting blocks remain unresolved.
- **Semantic consistency:** not fully complete; see the contradiction register and item tickets.
- **Guidance review:** performed against original C4 descriptions and practitioner distributed-systems guidance; findings are in `c4-standards-review.md`.
- **Owner approval:** not established by this audit.
- **Production readiness:** not established by this audit.

## References

Source counts and findings derive from `registry/elements.json`, `registry/decomposition-map.json`, `registry/interfaces.json`, `registry/functions.json`, `registry/decisions.json`, `validation/c4-diagram-coverage-matrix.md`, and actual Mermaid content. The independent completeness result also records that all local relative link targets exist. External-link availability and application/runtime behavior were not tested.

## Full registry exception register

The registry contains **23** C2 `decomposition_status=EXCEPTION` records. Each is listed with its exact element ID/name, parent, registry reason, and replacement documentation. `approved`/`accepted_by` below reproduce registry fields; the audit does not independently approve these exceptions. All source paths are relative to the package root.

- `CNT-ACC-APIGATEWAY` — API Gateway / BFF; parent `SYS-ACCSYSTEM`; reason: Routing/security cross-cut; no complex business logic to decompose into C3 components. Cross-cutting concerns documented in security-view.md and resilience-observability.md.; replacement evidence: `c2-containers/accsystem/CNT-ACC-APIGATEWAY.md`, `supporting-views/security-view.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-INSTREG` — Institution Registry; parent `SYS-ACCSYSTEM`; reason: Registry/CRUD service; complexity does not justify C3 decomposition at this stage. Deferred: revisit if multi-tier tenancy or complex approval workflows are added.; replacement evidence: `c2-containers/accsystem/CNT-ACC-INSTREG.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-SEARCH` — Search & Discovery; parent `SYS-ACCSYSTEM`; reason: Search index service; primary value is data-architecture view, not software-component decomposition. Data architecture documented in data-architecture.md. C3 deferred pending search-technology selection.; replacement evidence: `c2-containers/accsystem/CNT-ACC-SEARCH.md`, `supporting-views/data-architecture.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-OFFER` — Offer / Price / Availability; parent `SYS-ACCSYSTEM`; reason: Price/availability snapshot service; straightforward read-through with staleness policy. C3 deferred pending pricing-rule complexity decision (open decision in idea.md §12).; replacement evidence: `c2-containers/accsystem/CNT-ACC-OFFER.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-CART` — Cart & Checkout; parent `SYS-ACCSYSTEM`; reason: Stateful session service; key behavior documented in function specs FN-ORD-CHECKOUT. C3 deferred to implementation planning phase.; replacement evidence: `c2-containers/accsystem/CNT-ACC-CART.md`, `functions/specs/FN-ORD-CHECKOUT.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-DELIVERY` — Delivery Management; parent `SYS-ACCSYSTEM`; reason: Delivery domain; C3 deferred pending ACCMared integration design and delivery-provider scope decision (open decision §12).; replacement evidence: `c2-containers/accsystem/CNT-ACC-DELIVERY.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-NOTIFICATIONS` — Notifications; parent `SYS-ACCSYSTEM`; reason: Notification dispatch service; complexity low relative to other domains. C3 deferred to Phase 4+ planning.; replacement evidence: `c2-containers/accsystem/CNT-ACC-NOTIFICATIONS.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-AUDIT` — Audit & Observability; parent `SYS-ACCSYSTEM`; reason: Observability infrastructure; components described in resilience-observability.md. C3 not selected: standard logging/metrics/tracing patterns, not novel business logic.; replacement evidence: `c2-containers/accsystem/CNT-ACC-AUDIT.md`, `supporting-views/resilience-observability.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-SOFTCAT` — Software Catalog & Release Distribution; parent `SYS-ACCSYSTEM`; reason: Release catalog service; key workflows documented in dynamic-license-flow.md and dynamic-publication-flow.md. C3 conditional: revisit when release-signing pipeline design is planned.; replacement evidence: `c2-containers/accsystem/CNT-ACC-SOFTCAT.md`, `supporting-views/dynamic-license-flow.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-PLATFORMADMIN` — Platform Administration & Support; parent `SYS-ACCSYSTEM`; reason: Admin workflow service; key security controls documented in security-view.md. C3 conditional: revisit when approval workflow and JIT-access implementation is planned.; replacement evidence: `c2-containers/accsystem/CNT-ACC-PLATFORMADMIN.md`, `supporting-views/security-view.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACC-EVENTBUS` — Event Bus / Message Broker; parent `SYS-ACCSYSTEM`; reason: Shared infrastructure; decomposed through interface contracts and observability docs, not software components.; replacement evidence: `c2-containers/accsystem/CNT-ACC-EVENTBUS.md`, `supporting-views/interface-contracts.md`, `supporting-views/resilience-observability.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-PRODUCTMASTER` — Product Master (ACCore); parent `SYS-ACCORE`; reason: ERP module; source of truth for product data. C3 deferred: ACCore internal architecture is institution-owned; platform architecture defines the integration boundary, not ACCore internals.; replacement evidence: `c2-containers/accore/CNT-ACR-PRODUCTMASTER.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-INVENTORY` — Inventory & Warehousing (ACCore); parent `SYS-ACCORE`; reason: ERP module; institution-internal. C3 deferred for same reason as CNT-ACR-PRODUCTMASTER.; replacement evidence: `c2-containers/accore/CNT-ACR-INVENTORY.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-SALES` — Sales & Procurement (ACCore); parent `SYS-ACCORE`; reason: ERP module; institution-internal. C3 deferred.; replacement evidence: `c2-containers/accore/CNT-ACR-SALES.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-FINANCE` — Finance / Accounting (ACCore); parent `SYS-ACCORE`; reason: ERP module; institution-internal. Financial record rules are institution-defined (open decision §12). C3 deferred.; replacement evidence: `c2-containers/accore/CNT-ACR-FINANCE.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-ORGUSERS` — Organization & Users (ACCore); parent `SYS-ACCORE`; reason: ERP module; institution-internal user management, independent of platform Identity & Access. C3 deferred.; replacement evidence: `c2-containers/accore/CNT-ACR-ORGUSERS.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-COMMERCE` — Commerce Workspace (ACCore); parent `SYS-ACCORE`; reason: ACCore's marketplace UI client; mirrors ACCommerce's role but embedded in ACCore. C3 deferred to implementation planning.; replacement evidence: `c2-containers/accore/CNT-ACR-COMMERCE.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACR-OUTBOX` — Outbox / Inbox (ACCore); parent `SYS-ACCORE`; reason: Transactional messaging infrastructure; pattern documented in resilience-observability.md. No business-logic components to decompose.; replacement evidence: `c2-containers/accore/CNT-ACR-OUTBOX.md`, `supporting-views/resilience-observability.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACE-MOBILEAPP` — ACCommerce Mobile / Web App; parent `SYS-ACCOMMERCE`; reason: Client application; UI decomposition deferred to frontend implementation planning. Key behavior documented in FR-002.; replacement evidence: `c2-containers/accommerce/CNT-ACE-MOBILEAPP.md`, `01-scope/scope-and-requirements.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACM-PUBLIC` — ACManagement Public Portal; parent `SYS-ACMANAGEMENT`; reason: Unauthenticated web portal; UI decomposition deferred. Key content documented in SYS-ACMANAGEMENT.md and security-view.md.; replacement evidence: `c2-containers/acmanagement/CNT-ACM-PUBLIC.md`, `supporting-views/security-view.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-ACM-ADMIN` — ACManagement Protected Admin Console; parent `SYS-ACMANAGEMENT`; reason: Authenticated admin web console; frontend decomposition deferred. Key workflows documented in security-view.md and dynamic-license-flow.md.; replacement evidence: `c2-containers/acmanagement/CNT-ACM-ADMIN.md`, `supporting-views/security-view.md`, `supporting-views/dynamic-license-flow.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-AMD-SUPERVISOR` — ACCMared Supervisor Desktop App; parent `SYS-ACCMARED-SUP`; reason: Flutter desktop client; UI decomposition deferred to Phase 4 implementation planning.; replacement evidence: `c2-containers/accmared/CNT-AMD-SUPERVISOR.md`; registry `approved=True`, `accepted_by=coordinator-direct`.
- `CNT-AMD-COURIER` — ACCMared Courier Mobile App; parent `SYS-ACCMARED-COU`; reason: Mobile courier client; UI decomposition deferred to Phase 4 implementation planning.; replacement evidence: `c2-containers/accmared/CNT-AMD-COURIER.md`; registry `approved=True`, `accepted_by=coordinator-direct`.

The eight actor and two external-system records are context elements, not C3 decompositions. They appear in the C1/landscape registry context and are not included in the 23 C2 exception count.


### Targeted parser follow-up

A Mermaid 12.2.0 syntax-only parse of the two rejected sequence-diagram blocks independently reproduced the parse errors near the unparsed message/end transition in `dynamic-license-flow.md` and the message-to-`Note over EMP` transition in `dynamic-publication-flow.md`. The library parse API did not provide a reliable all-diagram syntax-only pass for the other diagram types in this environment, so the all-diagram result remains the 26/28 renderer pass above. No source block was edited during this validation.


The interface-label finding is a traceability observation rather than a C4 rule: the original C4 pages define diagram scope and relevant relationship context but do not prescribe ACC registry IDs on every edge. [1] [2] [3]

## External references

[1]: https://c4model.com/diagrams/system-context "System context diagram"
[2]: https://c4model.com/diagrams/container "Container diagram"
[3]: https://c4model.com/diagrams/component "Component diagram"

Access date: 2026-11-19.
