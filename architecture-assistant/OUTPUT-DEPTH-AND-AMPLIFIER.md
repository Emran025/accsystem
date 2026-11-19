# Output Depth, Completeness, and Final-Stage Amplifier

## Purpose and authority

This policy turns “be detailed” into an observable authoring and review procedure. It applies to every architecture artifact, every stage handoff, and especially the final validation/release stage. Cross-artifact reconciliation and repeated read-after-write review are governed by `CONSISTENCY-AND-POLISH-POLICY.md` and are mandatory, not optional polish. Completeness means **all known, in-scope items in the declared inventory are accounted for and each selected deliverable meets its acceptance criteria**. It never means that an assistant can discover every unknown, guarantee a perfect design, or certify a system as safe for billion-dollar deployment without evidence and accountable human review.

Use the project evidence and user language. Preserve stable identifiers. Separate `CONFIRMED`, `ASSUMPTION`, `PROPOSED`, `UNKNOWN`, `UNRESOLVED`, `NOT_APPLICABLE`, `DEFERRED`, and `ACCEPTED` states. Every important assertion needs an evidence reference or a clearly labeled source/owner/action that can resolve it. Do not convert missing evidence into fabricated technical detail.

## Mandatory authoring loop — every artifact

Before writing:

1. Name the artifact's decision or implementation purpose, its audience, scope boundary, parent IDs, and source evidence.
2. Retrieve and inspect the complete relevant source records; a search excerpt is a lead, not proof that the source has been read completely. Follow up with direct reads or ranges for long files.
3. Build an itemized outline from the applicable template and policy. Tailor sections to the artifact; do not copy irrelevant headings as filler.
4. Identify dependencies, interfaces, data, behavior, failure modes, security and operational concerns that materially affect this artifact.

While writing:

5. Address each applicable outline item explicitly. For unknowns, record the unknown, its consequence, resolution evidence, responsible owner (or `OWNER_UNASSIGNED` with a named assignment action), and revisit trigger. For `NOT_APPLICABLE`, give a concise rationale.
6. Describe behavior as a sequence or contract where prose could hide ordering, state transitions, retries, idempotency, side effects, concurrency or failure semantics.
7. State alternatives and trade-offs for consequential proposals; label status and confidence. Distinguish what is evidenced from the assistant's recommendation.
8. Use specific IDs, examples, payload/field names, boundaries, pre/postconditions and measurable acceptance criteria when supported. If not supported, state what is needed instead of inventing precision.

Before saving:

9. Compare the artifact against every applicable template section and source. Mark each item `ADDRESSED`, `UNKNOWN/UNRESOLVED`, `NOT_APPLICABLE`, or `OUT_OF_SCOPE`; do not silently omit it.
10. Check internal consistency with requirements, assumptions, ADRs, interface contracts, parent/child registries, diagrams, deployment and other affected views. Escalate contradictions as blockers or explicit scoped releases, never as passing gates.
11. Replace generic claims (“secure”, “scalable”, “highly available”, “standard service”, “handles errors”) with concrete mechanisms, boundaries, failure cases, evidence, targets or explicit unknowns.
12. Reread the actual saved file after writing. Confirm it is complete, linked, correctly scoped, and not cut off by the model/token/tool limit.

## Depth is proportional, not word-count driven

Do not use fixed word counts, arbitrary minimum lengths, or repeated prose as a proxy for rigor. The expected detail grows with the number of responsibilities, interfaces, user journeys, state transitions, data classes, risks, dependencies and unresolved decisions. A simple artifact may be short only when the applicable checklist is demonstrably addressed and its small scope is evidenced. A complex or high-risk artifact must expand into independently reviewable sections and may require multiple files. Split large work by stable IDs or domains, not by dropping details.

A deliverable fails its depth check if it is only a title, single generic paragraph, list of technologies, diagram, percentage, or existence/status marker where the template calls for behavior, rationale, contracts, risks or tests. A long deliverable also fails if it is repetitive, speculative, contradictory, or unsupported.

## Minimum coverage checklist by artifact family

### System overview, discovery, scope, requirements

- Mission, users/actors, capabilities and measurable outcomes; supplied evidence/source map and source gaps.
- In-scope, out-of-scope, external and unresolved boundaries; ownership and lifecycle.
- Functional requirements with stable IDs, actor/trigger, normal and alternate paths, acceptance criteria and source/status.
- Non-functional requirements with units, measurement method, workload/tenant assumptions, priority and verification owner; unknown targets stay unknown.
- Constraints, assumptions, exclusions, dependencies, risks, contradictions, stakeholder decisions required and revisit triggers.
- For a portfolio, inventory all known systems, teams, owners, dependencies and hierarchy; partition without losing IDs or coverage.

### C1/context and system landscape

- Explicit viewpoint, scope/boundary, legend and status; system purpose.
- Every evidenced actor and external system, its responsibility/ownership/status, direction and purpose of each relationship.
- Protocol/data sensitivity/trust boundary when known; uncertainty marker when not.
- Traceability to inventory and requirements. Never depict internal details of an external system without evidence.

### C2/container

- Purpose, responsibilities and explicit non-responsibilities; parent, users/owners, deployment unit and scope/status.
- Inbound/outbound callers, interface direction, protocol/style, sync/async, authentication/trust, payload/data class and error/timeout behavior where known.
- Data ownership, stores, schemas/entities, lifecycle, consistency, retention/deletion, backup/restore and migration implications.
- Concurrency, idempotency, rate/size limits, scaling dimensions, availability/failure dependencies, retries/circuit breakers and recovery behavior.
- Security/privacy controls, secrets, authorization, audit, threat boundaries, observability and operational ownership.
- Technology rationale, alternatives, decision status/ADR, confidence, unresolved choices and consequences.
- C3 disposition for every container: selected, conditional, not selected, deferred, or blocked; include rationale, uncovered risk, accountable owner, concrete next step and reconsideration trigger.

### C3/component and C4/code

- Parent mapping, precise responsibility and boundaries; collaborators and dependency direction.
- Key operations/entry points, input/output/error contracts, state and side effects, transaction/concurrency/idempotency behavior where relevant.
- Data ownership and security checks; algorithm/business rules; dependency failure and testing strategy.
- For C4 code views, describe code-level structures actually evidenced or explicitly illustrative; do not invent source packages, classes, functions or signatures.
- Map each selected component to all known important code elements or label the view partial and enumerate the remainder. Explain non-selection and follow-up.

### Functions and end-to-end dynamic/data flows

- Trigger/actor, preconditions, authorization, validation, normal path, alternate paths, state transitions, postconditions and side effects.
- Ordering and owner of every step; request/event contracts, correlation/idempotency keys and transaction boundaries.
- Timeout, retries, duplicate delivery, partial failure, compensation, DLQ/replay/manual recovery and terminal outcomes.
- Data classification, ownership, read/write effects, consistency guarantees and retention implications.
- Observability signals, audit evidence, security/privacy controls and test cases including edge, failure, recovery and concurrency cases.
- For unresolved semantics, identify operational or business impact and a decision owner/action. Do not label an operation implementation-ready while critical contract details are unresolved.

### Interfaces, APIs, events and integrations

- Provider/consumer IDs, purpose, versioning/compatibility, protocol and trust/authentication.
- Request/response or event envelope with required/optional fields, types, constraints, units, examples where evidence permits, errors and privacy classification.
- Delivery/ordering/replay/expiry/idempotency behavior, SLOs/rate/size/timeout/retry rules, deprecation and compatibility strategy.
- Ownership, monitoring, failure escalation, test/contract evidence, secrets handling and unresolved commitments.

### Data, security and cross-cutting views

- Data entities/classification, authority/source of truth, ownership, access, lifecycle, lineage, retention/deletion and recovery.
- Threats/trust boundaries, attacker assumptions, mitigations, residual risks, authorization and audit evidence; distinguish controls present from proposed.
- For performance/reliability, workload assumptions, measurable SLI/SLO/targets, bottlenecks, capacity, backpressure, failure domains, recovery and validation method.
- For observability/operations, signals, ownership, alert/action/runbook, deployment/rollback and incident/recovery path.
- Explicit applicability disposition and rationale for every required concern; `UNKNOWN` is not equivalent to covered.

### ADRs and deployment

- Problem/context with evidence and IDs; decision status and decision authority.
- Viable alternatives compared against actual constraints, costs, failure/operational/security consequences and reversibility.
- Selected proposal, confidence, rejected alternatives and reasons, assumptions, migration/rollback, affected artifacts, revisit triggers and required acceptance.
- Deployment environments, trust/network zones, runtime units, storage, identity/secrets, scaling/failure/backup/restore/rollout/rollback, ownership and cost drivers.
- Clearly mark unconfirmed cloud providers, topology, products, regions and sizing as `PROPOSED` or `UNKNOWN`; never present examples as production facts.

### Validation, reports and handoffs

- Record exact command/tool/version, timestamp, scope/artifact revision, actual result and evidence path for each check.
- Separate structural registry validation, content/depth review, cross-artifact consistency, diagram ID/syntax/render/visual checks, security review and human approval. A pass in one category is not a pass in another.
- List missing, incomplete, deferred, accepted exception, unresolved and unverified items separately by ID. An exception is not a delivered artifact and does not count as complete coverage.
- Reconcile stage states across the stage ledger, manifest and report. Never use `PASSED` when any required check is unexecuted, failed, blocked or inconsistent.
- Provide actionable owners, next actions and resumption point. Include the portable checkpoint path/session ID at a deliberate stop.

## Final-stage amplifier — must run before any completion answer

At stage 7, and again before the user-facing final answer, perform this audit deliberately. Treat it as a second substantive review pass, not a request to rewrite the summary in more words.

1. **Inventory reconciliation:** compare idea/source inventory, stable-ID registries, decomposition maps, requirements, important operations, interfaces, selected views, and actual files. Name every unmatched/duplicate/orphan/unknown item.
2. **Depth challenge:** inspect high-risk and high-complexity artifacts against the family checklists above. Expand any summary that hides behavior, trade-offs, failure states, operational details or unresolved decisions.
3. **Contradiction challenge:** compare requirements vs. assumptions, ADRs, issue log, acceptance status, registry claims, diagrams and deployment. A discrepancy is a finding even when each individual file looks plausible.
4. **Evidence challenge:** sample and directly reread source files behind major claims. Mark unverified facts/proposals and lower confidence. Search results alone are not authoritative.
5. **Traceability and diagram challenge:** reconcile the `diagram-coverage-matrix.md` against every in-scope registry ID and the actual view files. Verify that all relevant C1/C2 units, selected C3 components, evidenced C4 items, critical flow steps, runtime units and applicable concerns appear in the appropriate diagrams or have explicit dispositions. Check partition indexes/cross-links for large views. Follow parent-child, operation-function, decision-element, interface-provider/consumer and diagram IDs in both directions; distinguish ID checks from syntax/render/visual and semantic verification.
6. **Residual risk and readiness challenge:** identify the top unresolved business, security, data, reliability, scalability, compliance, migration and operability questions that could invalidate the design. State impact and owner/action.
7. **Expansion pass:** repair omissions supported by evidence. Where evidence is absent, add a clear unresolved record, consequence, owner and trigger—never fill gaps by guessing. Continue independent work.
8. **Repair, reread, repeat:** update every artifact and diagram affected by an evidence-supported fix. Reopen and reread each saved change and all directly impacted dependents from disk, then rerun relevant checks and recheck the finding from both directions. Repeat the whole cross-artifact pass until a complete pass finds no new material contradiction. If limits prevent another pass, checkpoint exact open findings and mark `PARTIAL`/`BLOCKED`; do not treat an interrupted polish loop as clean.
9. **Gate recomputation:** run `scripts/validate_architecture.py`, `scripts/validate_artifact_depth.py`, and `scripts/validate_consistency_artifacts.py` after repairs; reconcile their reports with the consistency ledger, diagram matrix, consistency-review report, manifest, status report and checkpoint. The depth and matrix scripts check outline/record structure only; manually verify content truth and adequacy. Required gates pass only with evidence for every required check. Mark unavailable/semantic/manual checks `NOT_VERIFIED`, not `PASSED`.
10. **Honest completion statement:** report scope actually covered, selected/deferred views, remaining blockers, validation limits and confidence. Use `COMPLETE_WITH_LIMITATIONS`, `PARTIAL`, or `BLOCKED` as appropriate. Never claim 100% certainty or production readiness from a model-generated document set.

## Stop, checkpoint and resume

At every stage boundary, checkpoint the stage name/status, evidence reviewed, artifacts touched, concise durable findings, blockers/unknowns, and ordered next actions. Before pausing due to a limit, provider interruption, context migration or model switch, save the current transcript/session and make the portable checkpoint readable. Resume by rereading the checkpoint and relevant artifacts, verify the last completed stage instead of blindly trusting it, continue from the first incomplete action, and preserve stable IDs and provenance. Do not mark a stage complete merely because files were generated; its exit gate must have been checked.
