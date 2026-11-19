# Cross-Artifact Consistency and Iterative Polish Policy

## Authority and intent

This policy is mandatory throughout the workflow, not only during final editing. It complements `AGENT.md`, `WORKFLOW.md`, `OUTPUT-DEPTH-AND-AMPLIFIER.md`, the C4 model and the quality gates. Stable-ID registries remain authoritative for identities and hierarchy; direct source/user evidence remains authoritative for facts; accepted decisions are authoritative only within their stated scope and phase. A generated summary, diagram, ADR or later-stage artifact never silently overrides an authoritative source.

The goal is one coherent, versioned architecture whose artifacts describe the same system at their respective levels of abstraction. C1, C2, C3, C4 and supporting views are intentionally different—not copies—but their boundaries, IDs, relationships, assumptions, decision status and scope must reconcile.

## Canonical baseline: create early, update continuously

During discovery/scope, create and maintain these project artifacts under the system documentation root:

- `validation/architecture-consistency-ledger.md`: current accepted/proposed facts, requirements, constraints, assumptions, terminology, boundaries, ownership, data authorities, interfaces, technology decisions, phase/version scope, evidence and affected artifacts.
- `validation/diagram-coverage-matrix.md`: every in-scope element ID mapped to its required/applicable diagram view(s), diagram IDs/files, and disposition. A diagram can be split into indexed views; record the partition and cross-links.
- `validation/consistency-review-report.md`: findings across artifacts, severity, affected IDs/files, authoritative evidence, resolution or unresolved disposition, and recheck result.

Use `templates/validation-reports/` as the starting structure. Do not create a parallel truth source: these artifacts are navigational ledgers derived from source evidence, registry, requirements and accepted decisions. Record provenance and status for each baseline statement. If these files already exist, inspect, reconcile and preserve their history rather than replacing them blindly.

## Invariants for every stage

1. **Read before extending.** Before a new phase or major artifact, reread the relevant baseline ledger, registry, requirements, accepted/proposed ADRs, issue/open-question records, prior-stage artifacts and applicable diagrams. On model handoff, verify current files rather than trusting only the checkpoint summary.
2. **Freeze the vocabulary and scope.** Reuse stable IDs, canonical names, phase/version qualifiers, system boundaries, ownership and terms. If they change, record the change and update every affected artifact; never let renamed concepts or phase assumptions drift silently.
3. **Propagate decisions.** Every material decision/constraint must identify affected requirements, containers/components/code views, interfaces/data flows, deployment and diagrams. Mark unaffected areas or reasons. After an ADR or scope change, reopen dependent artifacts and gates.
4. **Update as-you-go.** At each stage boundary, update the consistency ledger and diagram-coverage matrix alongside registries and artifacts, not as an end-only retrospective. Record the checkpoint and changed artifact paths.
5. **Match level of abstraction.** A C1 diagram shows system boundary, people and external systems; C2 shows every in-scope container/data store or explicitly partitions them; selected C3 views show all claimed-selected components; C4 views show only code structures supported by source evidence. Dynamic and deployment diagrams map their steps/runtime units to IDs. Never add internal detail at a higher level merely to make views look identical.
6. **No silent omission.** Every applicable registered unit appears in its relevant view(s), or is explicitly `NOT_APPLICABLE`, `NOT_SELECTED`, `DEFERRED`, `UNKNOWN`, or `BLOCKED` with rationale and follow-up. If a diagram is too large, split it by domain/container/flow and create a navigable index; do not drop units or create an unreadable omnibus diagram.
7. **Preserve conflict rather than average it away.** When sources disagree, record exact statements, source/authority, scope/phase/date, impact and owner/action. Resolve only with evidence or an explicit authorized decision. Otherwise keep it unresolved and block the affected gate. Do not choose the most recent generated document just because it is newer.

## Required iterative consistency-polish loop

Run this loop after every major scope/decision change and as the final release gate. The writer must inspect the saved artifacts anew; do not approve from memory of drafting.

### Pass A — Establish comparison set

- Record the artifact revision/time, stable-ID inventory and source snapshot used.
- Enumerate all in-scope IDs and material claims, and all relevant requirements, assumptions, ADRs, interface/data contracts, operations, deployment decisions, diagrams, deferrals and quality gates.
- Build/update bidirectional mappings: requirement ↔ artifacts; parent ↔ children; operation ↔ function; interface ↔ provider/consumer; decision ↔ affected IDs; element ↔ each applicable diagram; flow step ↔ interface/container/data effect; runtime unit ↔ deployment.

### Pass B — Cross-check from multiple directions

Review at least the following comparisons, using the actual saved files:

- Idea/source requirements against scope, functional and NFR records; confirm IDs and phase qualifiers agree.
- Assumptions, exclusions, open issues and ADR status against every design claim that depends on them.
- C1 actors/external systems/boundary against the inventory; C2 containers/data stores and relationships against the same inventory.
- C2 parent/child coverage against selected C3 component registries/views; C3 coverage and evidence against any selected C4 code/module views.
- APIs/events/interfaces against both consumer and provider records, function contracts, data-flow steps, auth/trust, failure/retry semantics and diagrams.
- Data ownership/source-of-truth, schemas, lifecycle and consistency claims across containers, functions, integrations, security, backup/recovery and deployment.
- Deployment runtime units, networks/trust zones, stores, identity/secrets and environments against C2, C3, ADRs and operational views.
- Diagram coverage matrix against the registered elements and actual diagrams. Check that diagrams use the right level, include every applicable stable ID, preserve relationship direction/labels, link partitions and do not show stale/deleted/proposed-as-confirmed units.
- Stage ledger, manifest, consistency report, diagram plan, depth report and unresolved-issues register against one another; status and counts must not conflict.

Record every discrepancy as a finding with severity (`BLOCKER`, `MAJOR`, `MINOR`, `OBSERVATION`), claim A vs claim B, source authority, affected IDs/files/views, consequence, resolution evidence, owner/action and status. A contradiction is not fixed by editing only one side without examining all dependents.

### Pass C — Repair by authority and impact

- Determine the correct source of truth using direct evidence and explicit authority/scope, not recency or plausibility alone.
- If evidence supports resolution, update the canonical ledger/decision first, then every impacted registry/artifact/diagram/report. Preserve old decision history where appropriate.
- If a required detail is unavailable, mark it unresolved, state both alternatives and impact, assign an owner/action or assignment action and revisit trigger, and keep the affected gate blocked/in progress.
- Refresh every dependent diagram from the current registries and records. Regenerate its stable-ID mapping; do not patch visual text while leaving its source table or diagram plan stale.
- Add an entry to the polish log naming finding ID, files/views changed and downstream items reopened.

### Pass D — Read-after-write and independent recheck

After any repair:

1. Reopen and reread every changed file from disk; reread each directly affected parent/child, contract, ADR, diagram and report.
2. Re-run structural, references, traceability, diagram-ID and outline checks; run syntax/render/visual checks where available. Do not infer diagram correctness from ID checks.
3. Re-run the same finding against both sides of the contradiction and the full impact set. Confirm the corrected statements agree and remain properly scoped.
4. Update the consistency report, diagram matrix, manifest and checkpoint; remove a finding only with linked evidence showing resolution.
5. Begin another pass if any edit could have changed a dependency, boundary, name, ID, requirement, decision status, flow or diagram. Continue until a full pass creates no new material finding and all required fixes have been reread/rechecked.

This is a bounded fixed-point process, not an infinite loop. If context, token, time or provider limits prevent a clean pass, save the exact remaining findings and affected files in the checkpoint; mark the project `PARTIAL`/`BLOCKED` and resume there. Never convert a loop limit into a clean bill of health. Human semantic review remains required for domain truth and consequential architecture decisions.

## Release criteria

The consistency gate may be `PASSED` only when:

- the scope/ID inventory reconciles with registries and every item has a clear disposition;
- `scripts/validate_consistency_artifacts.py` finds no missing required artifact or in-scope ID row; this is only a matrix-presence check, not proof that the diagram is semantically correct;
- the consistency ledger, requirements, ADRs, interface/data/function contracts, diagrams, deployment views and status reports agree or explicitly document scoped versions/known unresolved items;
- no unresolved `BLOCKER` or `MAJOR` contradiction remains in the claimed release scope;
- every selected diagram is mapped and its relevant units are covered or explicitly partitioned; unselected views have evidence-based disposition;
- all post-repair reads and checks are recorded with commands/results, and reports/manifests/checkpoint statuses agree;
- remaining minor/observational findings, unverified render/visual/security checks and human decisions are visible and do not get described as verified.

A pass means only that the documented consistency review found no open material contradiction in the declared scope at the recorded revision. It does not prove discovery of unknown requirements, semantic correctness, security, production readiness or completeness beyond available evidence.

## Plan, execute, and verify each material repair
For each material repair, keep a compact plan in the checkpoint: affected IDs/files and dependents, authoritative evidence, intended change, risk, and exact check(s) that will test it. Do not create a duplicate source of truth or turn routine edits into a user approval barrier. After editing, reopen the changed artifacts and all impacted dependents from disk, rerun applicable checks, and record actual command, version, timestamp, exit status and result. A validator may report a consistent `BLOCKED` release; do not change source statuses merely to make the validator return a clean result. Use scenario/negative fixtures to prove that a blocker cannot coexist with a claimed PASS, and keep tool status checks distinct from domain and human review.
