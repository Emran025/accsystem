# Skill: diagram-selection

Purpose: choose useful architecture views without losing scope or creating diagrams mechanically.

## Procedure

1. Read the core C4 and diagram-selection policies. Confirm scope, audience, goals, evidence, systems/teams/domains, and whether the work is one system or a portfolio.
2. Create the diagram plan first. Give every official C4 type—context, container, component, code, landscape, dynamic, deployment—and each relevant concern view a status, question, audience, evidence, rationale, artifact path/owner and validation state.
3. Produce C1 and C2 for each focal software system. For a multi-system portfolio, include a landscape view plus system-specific contexts where useful.
4. Decide C3 per container and C4 per selected component using complexity, business criticality, risk, boundaries, change coupling, ownership, uncertainty and implementation planning need. Keep complete inventories and explicit dispositions; deep drawings can be phased. Never claim partial coverage is complete.
5. Add deployment views per relevant environment when topology/security/operations matter. Add dynamic views only for named complicated/critical workflows. Add extra data/security/resilience/event/state views only to answer a concrete requirement or risk question; say which are outside C4 when appropriate.
6. Follow the notation policy: scope/title, audience, legend, explicit element type/responsibility, stable IDs, one-way labeled relationships, technology/protocol where applicable, and no invented implementation facts.
7. Validate syntax/rendering and visually inspect when possible; distinguish this from ID consistency. Record `NOT_VERIFIED` if unavailable. Revisit the plan when scope or architecture changes.

## Required output

Provide the completed plan, selected view paths, not-selected/deferred rationale and follow-up ownership, completeness/partition status, evidence/source IDs, validation status and open questions.
