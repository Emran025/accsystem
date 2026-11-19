# Architecture validation and release report

## Run metadata
- System/IDs: {{name, system ID, scope}}
- Artifact revision/fingerprint: {{revision or stable file list}}
- Run timestamp/timezone: {{timestamp}}
- Tool and version: {{commands, Python/runtime versions}}
- Overall disposition: `{{PASSED|BLOCKED|PARTIAL|NOT_VERIFIED}}` — explain; do not use one result to imply all review types passed.

## Gate results
| Gate/check family | Status | Command/reviewer | Evidence/output path | Scope/revision checked | Limitations and next action |
|---|---|---|---|---|---|
| Structural registries/references | {{status}} | {{tool/version}} | {{path}} | {{scope}} | {{limitations/action}} |
| Inventory and decomposition coverage | {{status}} | {{review/tool}} | {{path}} | {{scope}} | {{omissions}} |
| Artifact depth review | {{status}} | {{reviewer/policy}} | {{path}} | {{artifacts}} | {{items needing expansion}} |
| Cross-artifact consistency | {{status}} | {{reviewer/method}} | {{path}} | {{claims compared}} | {{contradictions}} |
| Diagram ID/syntax/render/visual | {{separate statuses}} | {{tools/reviewer}} | {{files/output}} | {{views}} | {{unverified portions}} |
| Security/operations/human acceptance | {{separate statuses}} | {{reviewer}} | {{evidence}} | {{scope}} | {{limits}} |

## Coverage accounting (separate categories; no blended percentage)
- In-scope inventory total: {{count and inventory reference}}
- Selected deliverables required / delivered: {{IDs and paths}}
- Artifacts actually reviewed for depth: {{IDs/paths}}
- Deferred/not selected: {{IDs, reasons, residual risk, owner/action, trigger}}
- Explicitly authorized waivers/exceptions: {{IDs, authority, approval reference/date and replacement evidence}}
- Unresolved/blocked: {{IDs, impact, owner/action}}
- Not verified: {{checks, reason and required evidence}}

## Blockers and warnings
| ID/check | Evidence | Impact | Repair/input needed | Owner | Revisit trigger |
|---|---|---|---|---|---|
| {{item}} | {{path/line/tool result}} | {{impact}} | {{action}} | {{owner/assignment action}} | {{trigger}} |

## Cross-artifact contradiction review
Compare and reconcile requirements, assumptions, ADRs, unresolved issues, interfaces, diagrams, deployment and stage/manifest state. List conflicts by IDs and disposition; unresolved material conflicts keep the affected gate blocked.

## Release decision and handoff
- Release disposition and rationale: {{COMPLETE_WITH_LIMITATIONS|PARTIAL|BLOCKED}}
- Checks passed: {{only checks actually executed}}
- Checks not passed/not verified: {{named checks}}
- Human decisions still required: {{decision, authority, evidence}}
- Next actions in priority order: {{actions and owners}}
- Portable checkpoint/session: {{path/session ID/current stage}}
