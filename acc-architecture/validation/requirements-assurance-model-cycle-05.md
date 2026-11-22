# Requirements assurance model — Cycle 05

**Baseline:** `62b49e2f853873374ebe9dcb46f287b8b0bb05bd`  
**Purpose:** adopt a substantive, standards-informed closure model for PH-01 through PH-04 without fabricating approval, implementation, security, contract, or acceptance evidence.

## Comparable models reviewed

ISO/IEC/IEEE 29148:2018 treats requirements engineering as a lifecycle process and defines requirements information products, attributes, and iterative requirements management. Its applicability to this repository is direct: a requirement needs more than a sentence and an ID; its source, relationships, lifecycle state, and verification information must remain managed together. [1]

ISO/IEC/IEEE 15288:2023 provides a common system life-cycle process framework covering conception through retirement and supports concurrent, iterative, recursive application. The related planning guidance treats project authorization and technical planning as explicit information products rather than assumptions hidden in implementation notes. [2]

NIST SP 800-218 (SSDF) recommends integrating secure-development practices into an organization’s existing lifecycle model. It is outcome-oriented rather than a substitute for a project’s own approval or acceptance authority. For this repository, security-related requirements therefore need security-specific evidence and review, while the requirements lifecycle remains the governing baseline. [3]

## Reform decisions adopted for ACC

### 1. Readiness is a claim with four independent dimensions

A requirement may be considered execution-ready only when four independent dimensions are satisfied:

1. **Lifecycle authority:** the row has the documented status and approval authority required by its governance state. A validator cannot create owner or stakeholder approval.
2. **Behavioral traceability:** the row traces to an authoritative outcome, Use Case, or function without replacing a missing outcome with a merely nearby identifier. A C4 element, function name, or implementation task is not itself an approved Use Case.
3. **Decision closure:** every policy, contract, security, provider, ownership, or operating choice needed to interpret the requirement has an accepted decision record or an explicitly authorized exception.
4. **Verification evidence:** the stated acceptance behavior has executed or otherwise produced the required review/contract/security evidence, with artifact identity, environment or baseline, result, date, and responsible reviewer.

These dimensions are conjunctive for execution readiness and must remain separately reportable. A structural PASS in one dimension cannot discharge another dimension.

### 2. Closure authority is claim-specific

The repository adopts a claim-authority matrix rather than a single undifferentiated “approved” label:

- **Requirement meaning and scope:** owner/stakeholder authority recorded in the lifecycle evidence.
- **Architecture and interface contract:** designated architecture or contract authority, with the decision/contract artifact and version.
- **Security behavior:** security reviewer or authority, with the applicable threat/control review and executed security evidence where required. SSDF practice is integrated here; it does not waive owner or acceptance gates.
- **Implementation behavior:** implementation evidence tied to a build or source baseline.
- **Acceptance:** the responsible acceptance authority, with executable result evidence.
- **Retirement:** governance-authorized historical disposition with resolvable evidence and successor mapping; retirement never proves successor implementation.

A person or automated assistant may prepare evidence and identify a closure candidate, but may not self-approve a claim whose authority is external to the assistant.

### 3. Evidence records must be falsifiable and reproducible

A verification or decision reference is not sufficient merely because it is non-empty. The closure record must allow a reviewer to locate the artifact and understand what was checked. At minimum, a closure candidate should identify the claim, artifact or contract, repository/build/environment baseline where applicable, observed result, date, responsible reviewer, and any exception or limitation. Planned work remains planned until this record exists with a truthful result.

The Cycle 04 retirement repair now enforces resolvable file and anchor targets for historical retirement evidence. This rule is extended as a governance principle to future decision and verification evidence, but no current non-retirement references are rewritten or promoted without evidence-specific validation.

### 4. Baselines and change impact are mandatory for promotion

A status promotion or closure must identify the baseline against which it was assessed and the affected traceability, decision, contract, security, and verification artifacts. A later edit to a source requirement, contract, decision, or acceptance criterion invalidates dependent evidence until impact is reviewed. This is the repository’s practical application of lifecycle configuration and information management; it prevents an old PASS from being silently reused after a material change.

### 5. Strict-ready remains fail-closed

The current strict-ready predicates remain valid and are not weakened. They are the machine gate for the four dimensions above:

- status errors represent lifecycle authority not established;
- unresolved Use Case/function placeholders represent behavioral traceability not established;
- open decisions represent decision closure not established;
- planned verification references represent verification evidence not established.

The 871 active occurrences therefore remain genuine until their claim-specific authority and evidence exist. No rows are closed in Cycle 05 solely because this model was documented.

## Executable loophole closure

The Cycle 05 audit found that `ACCEPTED` was previously only a writable status label. The validator now requires an accepted row to have a matching approval record, an active authorized approver, a content hash matching the current requirement, and a matching executed or reviewed verification record with a passing result, subject hash, artifact reference, and timestamp. The new registries are `execution-phases/authorized-approvers.json`, `execution-phases/requirement-approval-records.json`, and `execution-phases/requirement-verification-records.json`.

These registries are intentionally empty because the repository contains no truthful approval or acceptance evidence. An attempted direct status edit to `ACCEPTED` now fails structural validation rather than waiting for strict-ready to expose only the other predicates. This closes the highest-risk self-approval path without inventing any approver or test result.

## Decisions against common but unsafe shortcuts

- Do not convert every `TBD` to an existing function ID. That can create false traceability when the function artifact does not establish the requirement’s actor, outcome, preconditions, alternatives, or acceptance boundary.
- Do not treat `OWNER_REVIEW`, `PROPOSED`, or a technical baseline as `ACCEPTED` without the required authority record.
- Do not treat validator tests, diagram rendering, or report consistency as runtime, security, provider, financial, or acceptance evidence.
- Do not retire active rows to reduce the strict-ready count. Retirement is historical provenance, not implementation readiness.
- Do not treat a planned verification reference as executed because a similarly named test exists.

## Cycle 05 consequence

This is a governance and assurance reform, not a cosmetic count reduction. It gives each remaining blocker a falsifiable closure contract and preserves the distinction between repository integrity, architecture review, security assurance, implementation evidence, and acceptance. The current package remains **not ready** with 871 active blocker occurrences.

## References

[1]: https://standards.ieee.org/standard/29148-2018.html "IEEE/ISO/IEC 29148-2018 Requirements Engineering"
[2]: https://standards.ieee.org/ieee/15288/10424/ "IEEE/ISO/IEC 15288 Systems Life Cycle Processes"
[3]: https://csrc.nist.gov/pubs/sp/800/218/final "NIST SP 800-218 Secure Software Development Framework"
