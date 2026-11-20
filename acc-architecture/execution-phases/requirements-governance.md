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
