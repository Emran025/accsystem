# {{ID}} — {{Name}}

## Identity, purpose and scope
- Parent system: `{{system_id}}`; type: `{{service|application|data_store|...}}`
- Scope/status/evidence: `{{IN_SCOPE|...}} / {{CONFIRMED|ASSUMPTION|PROPOSED|UNKNOWN}}`; {{source paths and IDs}}
- Business purpose and outcomes: {{specific capabilities}}
- Responsibilities: {{owned responsibilities}}
- Explicit non-responsibilities and boundaries: {{neighbor ownership}}
- Users/teams/operational owner: {{known owner or assignment action}}
- Deployment unit vs logical boundary: {{distinguish from deployment topology}}

## Responsibilities and behavior
- Entry points/operations: {{IDs, callers and triggers}}
- Normal and important alternate flows: {{ordered behavior or references}}
- Business invariants/state: {{known rules and source}}
- C3 disposition: `{{SELECTED|NOT_SELECTED|CONDITIONAL|DEFERRED|BLOCKED}}`; rationale, uncovered risk, owner/action and revisit trigger: {{details}}

## Interfaces and dependencies
| Direction | Caller/provider ID | API/event/contract ID | Protocol/style | Data and trust | Timeout/error/retry |
|---|---|---|---|---|---|
| {{in/out}} | {{ID}} | {{ID}} | {{known/proposed/unknown}} | {{classification/boundary}} | {{contract or unknown}} |

Describe versioning/compatibility, authentication/authorization, sync/async semantics, ordering, idempotency, rate/size limits and dependency failure behavior. Link each contract rather than repeating incompatible copies.

## Data and consistency
- Owned entities/schema and source of truth: {{IDs and ownership}}
- Stores, cache, events and data lineage: {{relationships}}
- Lifecycle, retention/deletion, privacy/classification: {{policy/status}}
- Transaction and consistency guarantees: {{evidence or explicit unknown}}
- Backup/restore, migration and data-loss considerations: {{known/proposed/unresolved}}

## Security, reliability and operations
- Trust zones/network exposure: {{boundary and evidence}}
- Identity, authorization, secrets, encryption and audit: {{actual vs proposed controls}}
- Availability/failure domains, timeouts, retries, circuit breakers, backpressure and recovery: {{specific behavior}}
- SLO/SLI, workload/capacity/scaling dimensions: {{measured evidence or unknowns}}
- Logs/metrics/traces/alerts/runbooks/on-call owner: {{signals and actions}}
- Deployment, rollout, rollback and incident implications: {{reference or unresolved}}

## Technology and design rationale
- Stack/runtime: {{CONFIRMED|PROPOSED|UNKNOWN with source}}
- Alternatives and constraints: {{trade-offs}}
- ADRs/affected IDs: {{links}}
- Confidence and revisit triggers: {{basis and conditions}}

## Open risks and decisions
| Unknown/risk | Impact | Resolution evidence/action | Owner or assignment action | Revisit trigger |
|---|---|---|---|---|
| {{item or none with rationale}} | {{impact}} | {{action}} | {{owner}} | {{trigger}} |

## Acceptance and traceability
- Requirements/operations/functions/interfaces: {{IDs}}
- Data models/flows/diagrams/tests: {{paths and IDs}}
- Completeness within declared scope: `{{COMPLETE|PARTIAL|BLOCKED}}`; justify against the depth checklist and list remaining items.
