# Requirements Decomposition and Traceability Governance

**Status:** Framework only — no functional requirements are approved by this document.  
**Scope:** `acc-architecture/execution-phases/`  
**Normative language:** `MUST` is mandatory, `SHOULD` is the default unless an approved exception exists, and `MAY` is optional.

## 1. Purpose

This document defines how ACC requirements will be organized after the four execution boundaries have been agreed. It prevents a phase boundary document from becoming an unstructured requirements list and provides a machine-checkable link from every requirement to its execution phase, application/system location, and C4 container.

The framework creates five phase folders. Phases 01–04 are implementation phases. Phase 05 is a future product/intelligence phase and is intentionally a scope placeholder only; no Phase 05 functional requirements may be added until its boundary is separately authorized.

The framework does **not** approve business policy, API shape, database schema, provider behavior, security protocol, pricing policy, or production readiness. Those remain subject to the existing ADR and owner-gated decisions.

## 2. Required hierarchy

The required decomposition is:

```text
Phase
└── Main requirement document
    └── Main requirement record
        └── Sub-requirement records
            └── Acceptance criteria
                ├── API/event/UI contract reference
                ├── domain/data reference
                ├── C4 container reference
                └── verification reference
```

The terms are intentionally distinct:

| Level | Meaning | Required identity |
|---|---|---|
| Phase | Delivery boundary and gate | `PH-01` … `PH-05` |
| Main requirement document | A bounded business requirement area; one document per main requirement | `REQ-PHxx-...` filename/document ID |
| Main requirement | A coherent capability or business outcome that can contain several related sub-requirements | `REQ-...` |
| Sub-requirement | One observable, testable behavior or rule under one main requirement | `SREQ-...` |
| Acceptance criterion | Evidence that one sub-requirement is satisfied | `AC-...` |
| Implementation task | Engineering work derived later; never used as a requirement substitute | `TASK-...` |

A function catalog entry is not automatically a requirement. A C4 container is not automatically proof that a requirement is implemented. The traceability record must state the relationship explicitly.

## 3. Document and identifier naming

Main requirement documents MUST use a stable filename and contain the same document ID in their title:

```text
REQ-PH02-CATALOG-MANAGEMENT.md
REQ-PH02-PRODUCT-DISCOVERY.md
REQ-PH03-PAYMENT-ORCHESTRATION.md
```

Recommended identifier forms:

```text
REQ-PH02-CATALOG-MANAGEMENT
SREQ-PH02-CAT-001
AC-PH02-CAT-001-01
```

A sub-requirement MUST have exactly one `parent_requirement_id`. A parent cannot be inferred from a filename, heading, or folder alone.

Requirement statements MUST describe system behavior or a business rule that can be observed and verified. They MUST NOT be written as SQL operations, tables, code tasks, or a list of unrelated actions joined by `and`.

The atomicity rule is:

> An atomic requirement has one observable outcome and one verification target. It is not defined by the number of database writes, tables, services, or API operations used internally.

One use case MAY produce several sub-requirements and MAY use more than one internal database operation, event, or API operation. Conversely, one API operation MUST NOT be used as proof that all business requirements in a document are satisfied.

## 4. Mandatory requirement tables

Every future main requirement document MUST contain these tables. Empty tables are permitted only while the document is marked `DRAFT` and the missing content is explicitly recorded as a gap.

### 4.1 Main requirement table

| Field | Rule |
|---|---|
| Requirement ID | One `REQ-...` identifier |
| Phase ID | Exactly one `PH-01` … `PH-05` |
| Title | One bounded outcome |
| Statement | Business/system outcome, not an implementation task |
| Actors | Existing actor IDs or an explicitly marked proposed actor |
| Locations | Comma-separated canonical system IDs, for example `SYS-ACCORE, SYS-ACCSYSTEM` |
| Primary C4 containers | One or more existing `CNT-...` IDs |
| Related function/use case | Existing ID or `TBD` with a recorded gap |
| Status | `DRAFT`, `PROPOSED`, `OWNER_REVIEW`, `ACCEPTED`, or `RETIRED` |
| Evidence | Source, model, ADR, scenario, or owner decision reference |

### 4.2 Sub-requirement table

| Field | Rule |
|---|---|
| Sub-requirement ID | One unique `SREQ-...` identifier |
| Parent requirement ID | Exactly one existing main `REQ-...` identifier |
| Statement | One atomic, observable, testable behavior or rule |
| Trigger/precondition | Explicit where applicable; do not hide it in prose |
| Expected outcome | One primary outcome |
| Locations | Comma-separated canonical system IDs; at least one is required |
| C4 containers | One or more existing C2 container IDs; each MUST belong to a listed location |
| Acceptance criteria | One or more `AC-...` references |
| Verification | Test, review, simulation, or contract evidence reference |
| Status | Same controlled vocabulary as the main requirement |
| Open decisions | ADR/owner gate references; do not silently resolve them |

The canonical location value is the C1 system ID from `registry/elements.json`, not an informal label. For example, use `SYS-ACCORE` rather than only `ACCore`. Human-readable labels MAY appear in prose, but machine-readable tables MUST use IDs.

### 4.3 Acceptance-criteria traceability

In an acceptance-criteria table, the `API/event/UI contract reference` cell MUST cite a source that actually defines the contract behavior. A package-local `RGAP-*` identifier records a missing source reference; it is not a contract ID and MUST NOT appear alone as a contract reference. When no canonical contract reference is recorded, use `NOT SPECIFIED (source reference gap: RGAP-...)`. If a canonical contract is cited but a related traceability gap remains, label it separately as `OPEN (related gap: RGAP-...)`. Do not infer a contract from a nearby component, function, or gap record.

## 5. Location and C4 binding rules

Every main requirement and every sub-requirement MUST declare where it exists in the ecosystem:

```text
Locations: SYS-ACCORE, SYS-ACCSYSTEM
C4 containers: CNT-ACR-PRODUCTMASTER, CNT-ACC-CATALOG
```

The following checks are mandatory:

1. Every location ID MUST exist in `registry/elements.json` at C1 and be a system, not a person or external system.
2. Every C4 ID MUST exist in `registry/elements.json` at C2 and be an application, service, or data store.
3. Every C4 container's `parent_id` MUST be one of the declared location IDs.
4. The referenced requirement document MUST exist under the declared phase folder.
5. The document MUST contain the requirement ID and every declared C4 container ID. A row that merely names a nonexistent or unmentioned container is invalid.
6. A row MUST NOT use a prose-only location such as `the marketplace` or `some backend`.
7. A requirement that spans ACCore and ACCSystem MUST declare both systems and at least one C4 container under each system when both systems perform behavior. If one system is only an external dependency or evidence source, that distinction MUST be stated in the table.

The validator proves referential and structural truth only. It cannot prove that the described business behavior is semantically correct or already implemented. Semantic ownership review remains required.

### 5.1 Lifecycle semantics in strict-ready evaluation

`RETIRED` is a historical traceability state, not an active delivery state. A retired row MUST remain structurally synchronized with its source document so its provenance, supersession, decomposition, and acceptance-criterion ownership remain auditable. It MUST NOT be promoted to `ACCEPTED`, deleted, merged, or used as evidence that its successor is implemented.

Every `RETIRED` row MUST have a matching record in `retired-requirements.json` with its source document, explicit historical disposition, evidence reference, and successor IDs or an explicitly documented historical disposition. The `evidence_ref` MUST be a repository-relative file reference whose target exists; when it includes a `#fragment`, that anchor MUST also exist. The validator MUST reject an unregistered retirement, a mismatched source document, a missing successor, an unresolved evidence target or anchor, or a registry record whose row is no longer `RETIRED`.

When `successor_ids` are used, they MUST be unique, resolve to existing requirement rows, MUST NOT include the retired source itself, and MUST NOT point to another `RETIRED` row. The existence of a successor ID alone does not prove semantic equivalence or decomposition; the cited evidence must support the mapping, including any cross-phase or cross-document handoff.

Each sub-requirement's parent MUST resolve to a main requirement in the same phase and requirement document; the registry's `document_id` and `document_path` must match the parent row. The active strict-ready gate applies status, unresolved function/Use Case, open-decision, and planned-verification predicates to active rows only **after** retirement provenance has passed. Retired rows are excluded from those active-readiness predicates, while all structural, identifier, document, parent, location, container, and reference checks continue to apply. This prevents historical source rows from blocking the current package without weakening any gate for `DRAFT`, `PROPOSED`, or `OWNER_REVIEW` rows or allowing an active row to evade the gate by changing its status.

### 5.2 Execution-readiness assurance model

Execution readiness is a conjunctive claim across four independently evidenced dimensions: lifecycle authority, behavioral traceability, decision closure, and verification evidence. The status field cannot create owner or stakeholder approval; a C4 element or function ID cannot substitute for an authoritative Use Case outcome; a non-empty decision reference cannot prove that a policy or contract was accepted; and a planned verification reference cannot prove execution.

Each closure candidate MUST identify the authority applicable to the claim, the evidence artifact and baseline, the observed result or decision, the date, the responsible reviewer, and any limitation or exception. A source, contract, decision, acceptance criterion, security control, or implementation baseline change MUST trigger impact review of dependent closure evidence before promotion is retained. The detailed Cycle 05 model and standards basis are recorded in `validation/requirements-assurance-model-cycle-05.md`.

`ACCEPTED` is an evidence-derived state, not a writable label. Every accepted row MUST have a matching record in `requirement-approval-records.json` whose content hash matches the current requirement, whose approver is active in `authorized-approvers.json`, and whose approval reference and timestamp are present. It MUST also have a matching `requirement-verification-records.json` record with `EXECUTED` or `REVIEWED` state, `PASS` result, matching subject hash, artifact reference, and execution timestamp. Missing, stale, assistant-generated, or authority-unlisted records MUST fail validation. The current registries intentionally contain no approval or verification records, consistent with the current zero `ACCEPTED` rows.

The authorized-approver registry MUST contain at most one entry per normalized identity; approval and verification registries MUST contain at most one record per requirement ID. Duplicate or malformed evidence records MUST fail closed rather than being silently collapsed by a last-record-wins index.

The claim-authority boundary is explicit: owners or stakeholders authorize requirement meaning and scope; designated architecture or contract authority accepts architecture and interface contracts; security authority reviews security claims; implementation evidence is tied to a build or source baseline; and the acceptance authority records functional acceptance. An assistant or structural validator may prepare or check evidence but MUST NOT self-approve an external authority claim.

### 5.3 Strict-ready diagnostic counts

Strict-ready diagnostics MUST distinguish **predicate occurrences** from **unique affected requirement rows**. One active requirement row may fail several predicates, so the sum of status, traceability, decision, and verification counts is not a count of distinct requirements or distinct upstream issues. Reports SHOULD show row counts by requirement level and identify repeated traceability/decision references as links for investigation, not as evidence that a shared reference is one resolved issue.

These diagnostic groupings do not change the gate: every active row remains subject to each applicable predicate, and parent readiness MUST NOT be inferred from child rows. A non-empty decision reference remains open until the applicable authority and evidence close it; a planned verification reference remains unexecuted until execution evidence is recorded. Known empty-value descriptions such as `none recorded` are not decision references. Use `validate_requirements.py --check --strict-ready --summary` for the overlapping count view; omit `--summary` to retain row-level diagnostics. Either strict-ready mode MUST preserve its failing exit status while blockers remain.

### 5.4 Coexisting alternatives and independent gates

When authoritative project sources support multiple compatible paths, the architecture package MUST model the paths behind one shared behavioral contract rather than requiring a premature global choice. The machine-readable selection contract MUST identify the operational context at which the choice belongs (for example, institution, workflow, transaction, interface, deployment, or operation), its source-backed dimensions and resolution mode, the exact eligible-path allowlist, source-derived eligibility conditions, any complete or partial source-stated default, and fail-closed behavior for missing, ineligible, conflicting, or ambiguous selection. A partial default (such as an outbound direction without a chosen channel) MUST NOT resolve an entire path; a proposed default MUST remain approval-gated. The selector MUST NOT invent a wire/API field, precedence rule, numeric threshold, or path beyond the source scope. A request or client-controlled value MUST NOT bypass the applicable owner, security, finance, legal, or API-governance authority.

Each multi-path scope MUST retain: (1) exact source links and affected registry IDs; (2) the shared contract and a structured selector contract; (3) at least two currently selectable, source-supported behavior paths; (4) a one-to-one mapping of source-derived acceptance criteria to the path(s) or cross-path scenarios to which they actually apply; and (5) explicit failure, retry/idempotency, recovery, security, and audit treatment. Criteria for a deferred path, an excluded statement, or an orthogonal configuration dimension MUST NOT be counted as acceptance for a selectable path. Acceptance criteria mapped into a design register MUST be labelled as not executed until independent runtime evidence is recorded.

Path selection MUST NOT close or dilute a separate blocker for source/use-case traceability, data ownership or system boundaries, state-machine meaning, success/failure semantics, idempotency, security invariants, audit obligations, financial authority, owner approval, or external evidence. `UNKNOWN`, `OPEN`, `DRAFT`, and `OWNER_REVIEW` remain unchanged unless the required authoritative evidence and decision are recorded. An assistant, model, or structural validator MUST NOT substitute for the named approval authority.

The statuses have distinct meanings: `RUNTIME_SELECTABLE` means the architecture design describes a complete, validated, source-traceable selector contract and all applicable path-design fields; it does not mean code exists, a path is activated, owner approval is granted, or the requirement is strict-ready. A reference selector under `validation/` may demonstrate fail-closed resolution and regression properties only; it MUST NOT be presented as ACCSystem runtime code or implementation evidence. `IMPLEMENTED_MULTI_PATH` MUST require linked implementation evidence and executed/reviewed PASS evidence for the applicable paths. A source-to-registry conflict MUST be marked `DESIGN_REVIEW_REQUIRED` and MUST NOT be counted as runtime-selectable until reconciled.

The independent check is `python3 acc-architecture/validation/validate_multi_path_readiness.py`; its schema, fail-closed reference selector, and regression tests are in `acc-architecture/validation/multi-path-readiness-register.json`, `acc-architecture/validation/multi_path_selector_reference.py`, and `acc-architecture/execution-phases/tests/test_multi_path_readiness.py`. This check MUST fail when a path, shared contract, complete selector allowlist/context/default/failure rule, acceptance-applicability mapping, failure/recovery/audit/security treatment, or separate gate is missing or inconsistent. It is not wired to relax `validate_requirements.py --check --strict-ready`, which remains an independent fail-closed gate.

## 6. Machine-readable registry

`requirements-registry.csv` is the query surface for phase/application/container coverage. It uses quoted CSV cells when a value contains commas. The `locations` and `c4_containers` fields are intentionally comma-separated inside their cells so the same values remain readable in Markdown tables.

Each row represents one main or sub-requirement. The registry MUST remain synchronized with the tables in the requirement document. The validator checks both directions for the IDs and C4 references that it can observe.

Run the checker from the repository root:

```bash
python3 acc-architecture/execution-phases/validate_requirements.py --check
python3 acc-architecture/execution-phases/validate_requirements.py --check --require-rows
python3 acc-architecture/execution-phases/validate_requirements.py --query --phase PH-02
python3 acc-architecture/execution-phases/validate_requirements.py --query --location SYS-ACCORE
python3 acc-architecture/execution-phases/validate_requirements.py --query --container CNT-ACC-CATALOG
```

`--require-rows` is intentionally not used for the initial scaffold because no functional requirements have been authorized yet. It MUST be used once a phase requirement package is declared ready for review.

## 7. Empty or fabricated requirement prevention

A requirement is considered structurally empty or fabricated when it has any of the following conditions:

- missing ID, phase, status, statement, location, or C4 container;
- a location or C4 ID that does not exist in the registry;
- a C4 container whose parent system is not declared as a location;
- a document path that does not exist;
- a document that does not contain the requirement ID or the declared C4 IDs;
- a sub-requirement with no valid parent;
- a Phase 05 row, because Phase 05 is not open for requirements;
- a placeholder such as `TBD`, `N/A`, or `some service` in a field that requires a concrete reference.

The checker reports these as errors. It does not convert a failed check into approval.

## 8. Review prompt for each requirement package

Before accepting a requirement package, the reviewer MUST answer:

1. Is the requirement assigned to the correct phase boundary?
2. Is it one outcome, or have unrelated outcomes been joined together?
3. Is it a business/system behavior rather than an implementation task?
4. Are all actors, channels, and locations explicit?
5. Does every listed C4 container actually belong to the listed system?
6. Is each C4 reference present in the requirement document rather than copied into the registry only?
7. Is the behavior supported by an existing model, function, state, interface, ADR, or owner decision?
8. Are unresolved policy and owner decisions preserved rather than silently invented?
9. Are acceptance criteria and verification evidence specific enough to falsify the claim?
10. Does the requirement add a capability, or merely restate an existing requirement under a different name?

A `PASS` from the script means the references are structurally credible. It does not mean the requirement is approved, implemented, secure, performant, or production-ready.
