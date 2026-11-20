# Change Report — 2026-11-20 local remediation

**Baseline:** repository `Emran025/accsystem`, branch `main`, HEAD `99e440dd55a7d3ff424fb207069ed23ae2563e05`. The working copy was cloned locally because no repository was present in the sandbox. No commit, push, visibility change, release, tag, or upload was performed.

## Changes applied

- Converted the root `README.md` from UTF-16LE to UTF-8 without a BOM and repaired architecture links relative to the repository root. Updated current registry/rendering/status facts.
- Added `.gitignore` for Python bytecode, caches, local assistant state/index/backups, and temporary files; removed the tracked generated `.pyc` file.
- Made the main registry loader BOM-safe (`utf-8-sig`), hardened Markdown-link parsing against malformed/absolute/path-traversal references, and changed validation report writes to reject symlink/hardlink targets and use temporary-file plus atomic replacement.
- Replaced focused validator wrappers' unconditional `sys.argv[1]` access with argparse-based CLIs, including safe `--help` behavior.
- Corrected the canonical C1 overlay aliases and removed the undefined `AS` edge; status wording in that overlay now distinguishes literal coverage from semantic completeness.
- Replaced the reservation TTL auto-release/compensation claim with the ADR-018 safe rule: elapsed time leaves `UNKNOWN`; only authoritative `EXPIRED` or trusted reconciliation may resolve it. Canonical immediate/terminal vocabulary is explicit, while policy and approval gates remain open.
- Replaced deprecated reservation response vocabulary in affected contract/component/function prose where the source meaning was clear.
- Corrected two Mermaid syntax issues in the dynamic license/publication views; both now render successfully with `manus-render-diagram`.
- Updated the manifest counts/provenance and marked the older broad consistency report as historical.

## Executed verification

- `python3 -m unittest discover -s architecture-assistant/tests -v`: **57/57 passed** after changes.
- `python3 architecture-assistant/scripts/validate_architecture.py acc-architecture`: **PASS** after BOM-safe loading; this is structural registry/reference validation only.
- `python3 architecture-assistant/scripts/validate_diagrams.py --help`: **PASS** and no longer crashes from missing `argv[1]`.
- `manus-render-diagram` on the two previously failing dynamic views: **PASS** for both.
- Canonical count script: 113 elements, 7 operations, 7 functions, 9 interfaces, 22 decisions, 7 systems, 30 containers, 28 components.

## Not closed by this change

Runtime symlink-parent/TOCTOU and atomic assistant-state writes, provider retry/response validation, profile loading, RAG secret/scope policy, full JSON Schema validation, complete Mermaid AST validation, C1/C2 relationship semantics, institutional connectivity/payment/accounting policy, owner approval, security/legal/finance/operations review, and production readiness remain open. These are recorded as risks or external gates rather than silently decided.
