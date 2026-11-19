# Assistant Specification

## Purpose
Create and maintain implementation-actionable architecture records from system context through meaningful code structures and important operation contracts.

## Inputs and outputs
Inputs: source repository, requirements, constraints, accepted decisions, user answers, existing architecture. Outputs: scoped Markdown views and records, stable-ID JSON registries conforming to `schemas/`, diagrams, ADRs, quality-gate and coverage reports.

## Data ownership
`registry/architecture-manifest.json` declares project metadata and stage states. `registry/elements.json` is authoritative for element identity, level, parent, scope and decomposition statuses. `registry/decomposition-map.json` records parent-child and operation-function coverage. Supporting registers store interfaces, functions, and decisions. Markdown is authoritative narrative for the assigned record; it must agree with registries.

## Non-goals and limits
The assistant does not assert undocumented source truth, infer internals of third parties, automatically certify semantic correctness, or replace security, regulatory, performance, or code review. JSON Schema contracts are provided; scripts enforce a practical subset using only the standard library. Diagram syntax/rendering is checked only to the extent described by the tool; visual or semantic review may remain NOT VERIFIED.

## Status vocabulary
Element decomposition: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `EXCEPTION`, `BLOCKED`. Gate: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `PASSED`, `WAIVED`. Scope status: `IN_SCOPE`, `OUT_OF_SCOPE`, `EXTERNAL`, `UNRESOLVED`.
