# C4 Diagram Review Report — ACC Final-v4 Overlay

> **Historical finding set:** This report describes an earlier overlay review. Later focused corrections and the current full Mermaid run supersede its pre-correction diagram findings; unresolved semantic and owner gates remain open.

## Input identity and safe handling

Input was the ACC Final-v3 package identified by its contents: `validation/v3-audit.md`, `validation/change-report.md` titled V3, and the 131 regular-file/156-entry v3 archive delivered in the preceding pass. A fresh backup was created at `/tmp/acc-architecture/acc-architecture.v4-backup/` before edits. The original and earlier archives were not used as replacements.

## Registry-derived inventory

Inventory was extracted from `registry/elements.json` and cross-checked with `registry/decomposition-map.json` and `registry/architecture-manifest.json`.

| Level | Counting rule | Total |
|---|---|---:|
| C1 | Registered `type=system` | 7 |
| C2 | Registered `type=service`, `application`, or `data_store` | 30 |
| C2 supporting records | Registered interfaces | 9 |
| C3 | Registered `type=component` | 28 |
| C3 supporting records | Registered functions with C3 level | 7 |

The registry confirms six named ACC operational systems plus the portfolio boundary: ACCSystem, ACCore, ACCommerce, ACManagement, ACCMared Supervisor, and ACCMared Courier. The six-system expectation is therefore confirmed; no registry membership was changed.

## Coverage before and after

Baseline was determined by inspecting actual Markdown Mermaid blocks, not merely filenames.

| Level | Baseline | Post-overlay | Denominator | Result |
|---|---:|---:|---:|---|
| C1 system context | 0 complete dedicated views | 7 complete registry-derived views | 7 | COMPLETE |
| C2 container coverage | 1 partial ACCSystem container diagram; no complete registry matrix | 30 visible in 7 owning-system views | 30 | COMPLETE |
| C3 component decompositions | 7 component diagram files containing all 28 registered component IDs | 7 files / 28 IDs retained and syntax-rendered | 28 | COMPLETE |

“Complete” here means registry ID presence, correct parent grouping, editable Mermaid source, and syntax validation. It does not mean stakeholder approval, production readiness, or semantic certification.

## Files added or modified

| Path | Status | Reason |
|---|---|---|
| `c1-context/c4-context-and-container-overlays.md` | ADDED | Added registry-driven C1 landscape, seven C1 context views, and seven grouped C2 owning-system views. |
| `validation/c4-diagram-coverage-matrix.md` | ADDED | Enumerates every registered C1 system, C2 container, and C3 component with path, status, source, and rationale. |
| `validation/c4-diagram-review-report.md` | ADDED | This evidence and review report. |
| `validation/validation-status.md` | MODIFIED | Records the v4 diagram overlay and validation state. |

All other v3 paths were preserved. Existing canonical C3 diagrams were not rewritten because registry-ID coverage and source structure were already present; they were independently rendered and checked.

## Modeling decisions and conflicts

- `SYS-ACCECOSYSTEM` is shown as the portfolio/landscape boundary, while the six named operational systems retain separate boundaries and contexts.
- ACCore is shown as institution-controlled and as the source of truth for institutional product/inventory data. ACCSystem is shown as owning marketplace records and projections/snapshots, not ACCore master data.
- The C1 overlay uses logical integrations for documented relationships. It does not assert HTTP, event-bus, synchronous behavior, deployment co-location, or shared data ownership where the source does not establish those details.
- C2 views group all registry-listed child containers under their owning system. Only documented high-level logical relationships are drawn; absence of an edge is not an assertion that no runtime dependency exists.
- The existing C3 decomposition set is preserved for Orders, Integration, Payment, License, Identity, Catalog, and ACCore Connector. The registry’s C3-level functions and interfaces remain supporting records, not invented component decompositions.
- No unsupported C4-Code, class, or source-level diagram was added.

## Cross-cutting consistency review

The overlay and existing C3 views were checked against `ADR-001`, `ADR-002`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-008`, `ADR-009`, `ADR-013`, checkout/reservation/payment specifications, and the v3 audit. The diagrams do not show payment before all required reservations, treat ACCore as the final reservation authority, or convert timeout/circuit-breaker/lost-response states into definitive success or failure. Multi-seller ParentOrder/SellerOrder structure and seller-specific reservation/capture policy remain in the source views.

## Validation method and results

- Registry JSON parsing: **passed**.
- Registry-derived count and parent checks: **passed** — C1 7, C2 30, C3 components 28.
- Canonical ID coverage check: **passed** for all C1/C2 overlay IDs and all 28 registered C3 component IDs.
- Duplicate FR-002 numbering and prior v3 invariants: retained from v3 validation.
- Mermaid rendering: **passed** for the new C1/C2 overlay and all seven canonical C3 component diagrams using `manus-render-diagram`. Temporary PNGs were used only for validation and are not deliverables.
- Internal Markdown link checking and ZIP integrity will be rerun after the v4 archive is built.
- No structural/depth validator was available in the package or workspace; it was not run.
- Mermaid syntax validation is not semantic review, stakeholder approval, security review, or production certification.

## Remaining human review items

1. Owners should review the proposed/logical relationship labels, especially transport/protocol selection and deployment topology.
2. Operations and platform owners should approve concrete connectivity, offline, deployment, and policy details that remain configurable or external.
3. Stakeholders must approve the proposed overlay; no stakeholder approval or production readiness is claimed.

No fixable missing, orphaned, duplicate, or unsupported diagram coverage finding remains in the registry-derived C1–C3 scope after this overlay.


## v3-to-v4 archive comparison

The input v3 archive contains **131 regular files** and **156 total ZIP entries**. Hash comparison before packaging found **3 added**, **0 missing**, **131 shared**, and **2 modified** paths. The final v4 archive contains **134 regular files** and **159 total ZIP entries**. Missing input paths: **0**. Added paths: `acc-architecture/c1-context/c4-context-and-container-overlays.md`, `acc-architecture/validation/c4-diagram-coverage-matrix.md`, `acc-architecture/validation/c4-diagram-review-report.md`. Modified paths are `acc-architecture/validation/change-report.md` and `acc-architecture/validation/validation-status.md`; the three coverage artifacts listed above are added paths. No unrelated v3 source files were changed.


## V5 audit supplement — semantic review and closure-status correction (2026-11-19)

The v4 result above is retained as the historical record of registry-ID presence, parent grouping, and Mermaid rendering. Its `COMPLETE` status must not be read as proof of semantic C4 completeness. A later independent C4 and registry-first audit found incomplete C1/C2 relationships, six duplicated C1 focal nodes/self-edges, conflicting ACCSystem C2 depictions, a Payment webhook route inconsistent with its adapter record, and other unresolved cross-document issues. See `c4-diagram-consistency-report.md`, `c4-completeness-audit.md`, `c4-microservices-audit-findings.md`, and the item-specific reports in `c4-missing-items-agent-results.md`.

The registry-derived identity result remains 7/7 C1, 30/30 C2, and 28/28 C3. All C1/C2/C3 diagrams rendered in the lead's validation run. Across 28 Mermaid blocks in 13 Markdown files, 26 rendered and two supporting dynamic-view blocks were rejected; the full per-file status is recorded in `c4-completeness-audit.md`. A renderer pass is not a semantic review.

Current state is therefore **ID coverage present; semantic completeness and cross-document consistency not yet closed**. The v4 claims of no fixable findings are superseded for current status by the evidence-based v5 audit; the historical statements above are not silently edited or removed. Stakeholder/owner approval, security review, and production readiness remain unestablished.
