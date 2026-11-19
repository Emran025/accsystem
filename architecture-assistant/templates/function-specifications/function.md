# {{FUNCTION_ID}} — {{Function Name}}

## Ownership, purpose and evidence
- System/container/component/module: `{{IDs}}`
- Parent business operation: `{{OP_ID}}`; related requirements: `{{FR/NFR IDs}}`
- Purpose, actor/trigger and outcome: {{precise behavior}}
- Evidence/status: `{{CONFIRMED|ASSUMPTION|PROPOSED|UNKNOWN}}`; source paths: {{references}}
- Language/signature status: {{language-neutral until implementation evidence exists}}

## Contract
- Preconditions: {{authorization, state and required input conditions}}
- Inputs: {{name, type, required/optional, format, bounds, units, classification}}
- Validation/business rules: {{rule IDs and deterministic outcomes}}
- Outputs: {{success, errors, partial outcomes and externally observable effects}}
- Postconditions/invariants: {{what must be true after each outcome}}
- Normal processing steps: {{ordered steps and dependencies}}
- Alternate/business paths: {{conditions and resulting state}}

## State, data and side effects
- Data read/written and authoritative owner: {{entities/store IDs}}
- Transaction boundary and consistency: {{atomicity/commit semantics or UNKNOWN}}
- Idempotency key/deduplication behavior: {{scope, retention and duplicate result}}
- Concurrency/race behavior: {{locking/versioning/conflict result or UNKNOWN}}
- Events/messages/external calls: {{contract IDs, order and delivery semantics}}

## Failure and security semantics
| Failure/condition | Observable response/state | Retry/timeout/compensation | Caller/operator action |
|---|---|---|---|
| {{specific case}} | {{contract}} | {{policy or UNKNOWN}} | {{action/owner}} |

- Authorization and trust boundary: {{principal, permission and enforcement point}}
- Sensitive-data handling, audit and secrets: {{controls/status}}
- Logging/metrics/traces/correlation: {{signals and redaction rules}}
- Rate/size/SLO constraints: {{evidence-based values or explicit unknowns}}

## Verification
- Unit tests: {{normal, validation, boundary, error and invariant cases}}
- Integration/contract tests: {{dependencies and failure simulation}}
- Concurrency/idempotency/replay tests: {{where applicable}}
- Acceptance criteria and evidence: {{measurable checks and owner}}
- Related ADRs, interfaces, diagrams and artifacts: {{IDs/paths}}

## Open matters
| Unknown/decision | Impact | Resolution evidence/action | Owner or assignment action | Revisit trigger |
|---|---|---|---|---|
| {{None with rationale, or item}} | {{impact}} | {{action}} | {{owner}} | {{trigger}} |

Implementation readiness: `{{READY|PROPOSED|PARTIAL|BLOCKED}}`. Do not claim READY while critical contract, failure, security or data semantics remain unresolved.
