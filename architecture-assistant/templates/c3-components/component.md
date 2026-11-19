# {{ID}} — {{Name}}

## Identity, status and scope
- Parent container: `{{container_id}}`
- Scope/status: `{{IN_SCOPE|OUT_OF_SCOPE|UNRESOLVED}} / {{CONFIRMED|ASSUMPTION|PROPOSED|UNKNOWN}}`
- Source evidence: `{{paths and stable IDs}}`
- Purpose and users: {{specific purpose, trigger and caller}}
- Explicit responsibilities: {{enumerated responsibilities}}
- Explicit non-responsibilities/boundaries: {{neighboring ownership and excluded work}}
- C3 scope completeness: {{complete within stated scope | partial; enumerate remainder}}

## Interfaces and collaborations
| Direction | Caller/provider | Contract or operation | Protocol/interaction | Data/status | Failure behavior |
|---|---|---|---|---|---|
| {{in/out}} | {{ID}} | {{name/ID}} | {{sync/async, protocol}} | {{payload/classification}} | {{timeout/retry/error/unknown}} |

## Behavior and rules
- Entry points/operations: {{IDs and triggers}}
- Normal path: {{ordered behavior}}
- Alternate paths and business rules: {{rules with evidence or proposed label}}
- State transitions and invariants: {{if applicable; otherwise reason}}
- Preconditions, postconditions and observable effects: {{specific contract}}

## Data and consistency
- Data read/written and authority: {{entities/owner/source of truth}}
- Persistence/cache/event effects: {{stores and lifecycle}}
- Transaction, consistency, idempotency and concurrency: {{behavior or explicit unknown}}
- Privacy/classification/retention implications: {{controls or unknown}}

## Failure, security and operations
- Failure modes and dependency behavior: {{timeout, retry, partial failure, compensation, terminal outcomes}}
- Authorization/trust boundary/secrets/audit: {{known controls vs proposals}}
- Logs, metrics, traces and correlation: {{signals and operational owner}}
- Capacity/performance/reliability expectations: {{evidence-based targets or unknowns}}
- Recovery/runbook/testability: {{replay, rollback, recovery and test strategy}}

## Design and traceability
- Key algorithms/technology constraints: {{evidence; do not invent implementation}}
- Component dependencies and dependency direction: {{IDs and rationale}}
- Code/module mappings: {{IDs or UNKNOWN until implementation evidence}}
- Related requirements, functions, interfaces, ADRs, diagrams and tests: {{IDs/paths}}
- Alternatives/trade-offs/confidence: {{where a decision is consequential}}

## Gaps and acceptance
| Unknown/risk | Impact | Evidence/action to resolve | Owner or assignment action | Revisit trigger |
|---|---|---|---|---|
| {{item or None with rationale}} | {{impact}} | {{action}} | {{owner}} | {{trigger}} |

- Review disposition: `{{COMPLETE_WITHIN_SCOPE|PARTIAL|BLOCKED}}`; justify against the applicable output-depth checklist.
