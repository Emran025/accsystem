# Completeness Policy

Maintain a complete inventory of known in-scope systems, containers/data stores, important operations, interfaces, dependencies, owners and material uncertainties. Completeness is measured against the declared evidence-backed scope; it is not a guarantee that no unknown requirements exist.

For every candidate view/element, record one explicit disposition: selected and delivered; selected but incomplete; not selected; conditional; deferred; blocked; or authorized waiver. For a non-selected/deferred item, provide stable ID, rationale/evidence, affected requirement and residual risk, responsible owner (or named assignment action), next action and a concrete revisit trigger. Missing owner/trigger means the disposition is unresolved, not complete.

Within any selected C3/C4 scope, enumerate all known meaningful components/code structures or label the view `PARTIAL` and name the uncovered remainder. Map important operations to behavior/function detail at the level the evidence supports. A function catalog, registry row, file count, diagram, exception marker or coverage percentage is not proof of a complete analysis.

Report separately: inventoried items; required selected deliverables; artifacts delivered; artifacts actually reviewed for depth; deferred/not-selected items; blocked/unresolved items; and explicit waivers. A deferred/exempt/exception item is never counted as a completed deliverable. Unknown implementation detail is not an approved exception; identify impact, owner/action and evidence needed.

A waiver of a required baseline or stakeholder-accepted scope requires explicit acceptance from an authorized user/stakeholder, a verifiable approval reference/date and replacement evidence. The assistant cannot approve a waiver or mark a self-generated `approved` flag as accepted. Any scope/phase qualification must be named and applied consistently across requirements, assumptions, ADRs, diagrams, registries and reports.
