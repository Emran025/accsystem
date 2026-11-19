# Architecture Diagram Plan — {{system_or_portfolio_name}}

Scope level: {{portfolio/system}} · Owner/audience: {{owner_and_audience}} · Status: {{DRAFT/REVIEWED/APPROVED}} · Evidence baseline: {{source_inventory_and_date}}

## Architecture scale and analysis plan

Systems in scope: {{count_and_registry_ids_or_unknown}}. Teams/owners: {{known_owners_or_unknown}}. Important domain boundaries: {{known_boundaries}}. Major integration/deployment/risk drivers: {{evidence_and_sources}}. Analysis partition: {{portfolio_to_system_to_container_or_other}}. Completeness status: {{FULL/PARTIAL/UNRESOLVED}}. Explicit deferred areas, owners, next actions: {{list_or_none}}.

## C4 and supporting view decisions

For every official C4 view below, set a status and rationale. Never omit rows. `REQUIRED`/`SELECTED` must link to the artifact; `CONDITIONAL` names its trigger; `NOT_SELECTED` explains why it adds no value for this scope; `UNRESOLVED` states the missing decision/input. Include source references and intended audience.

| View | Priority/status | Scope and audience | Question it answers | Evidence/rationale and trigger | Artifact path/owner | Validation status |
|---|---|---|---|---|---|---|
| System context (C1) | REQUIRED | {{}} | {{system boundary, actors, external systems}} | {{}} | {{}} | {{}} |
| Container (C2) | REQUIRED | {{}} | {{applications, services, data stores and communication}} | {{}} | {{}} | {{}} |
| Component (C3) | CONDITIONAL | {{selected containers}} | {{internal responsibilities/boundaries}} | {{selection criteria; listed non-selected containers}} | {{}} | {{}} |
| Code (C4) | OPTIONAL | {{important components only}} | {{implementation structure}} | {{complexity/value; code evidence}} | {{}} | {{}} |
| System landscape | CONDITIONAL | {{portfolio/enterprise/department}} | {{how multiple systems fit together}} | {{multi-system scope or reason not selected}} | {{}} | {{}} |
| Dynamic | CONDITIONAL | {{named use case/feature}} | {{runtime interaction/order/failure}} | {{complexity/criticality or reason not selected}} | {{}} | {{}} |
| Deployment | CONDITIONAL | {{environment per view}} | {{software instances on infrastructure}} | {{known topology/operations drivers or unresolved}} | {{}} | {{}} |

## Additional concern-specific views

| View/question | C4 view or separate concern view? | Priority/status | Evidence/rationale | Artifact path/owner | Validation status |
|---|---|---|---|---|---|
| {{e.g., security trust boundaries, data lifecycle, resilience, event flow}} | {{}} | {{}} | {{}} | {{}} | {{}} |

## Review and change control

Reviewed with: {{stakeholders}} · Date: {{date}} · Decisions/ADRs: {{IDs}} · Changes that trigger re-selection: {{scope/domain/deployment/ownership/risk changes}}.

Legend for status: `REQUIRED` = baseline deliverable; `SELECTED` = evidence-based chosen view; `CONDITIONAL` = create only when stated trigger is met; `NOT_SELECTED` = consciously excluded with rationale; `UNRESOLVED` = missing evidence/decision; `OPTIONAL` = useful focused detail but not a completion blocker unless a requirement makes it so.

## Stage artifact trail
Record actual saved diagram artifacts created or refreshed at each stage. Update the row at every checkpoint; include the path and scope, diagram view/partition, evidence snapshot or revision, maturity (`PROVISIONAL`/`REVIEWED`/`FINAL`), and separate syntax/render/visual status. The final-stage row must enumerate actual delivered diagram files and index/partition paths. A plan entry without an existing diagram file is not a completed diagram deliverable.

| Stage | Actual diagram artifact(s) and view | Scope/partition and evidence revision | Maturity | Syntax/parser | Render | Visual review | Follow-up |
|---|---|---|---|---|---|---|---|
| {{stage 0–7}} | {{path(s), not a promise}} | {{}} | {{}} | {{PASSED/FAILED/NOT_VERIFIED}} | {{}} | {{}} | {{}} |
