# Architecture Documentation Assistant

A reusable, Markdown-first architecture agent package for evidence-led C1–C4 decomposition, structured traceability, decision governance, local retrieval, durable stage checkpoints, resumable model handoff, iterative cross-artifact consistency polish and automated checks. The folder contains mandatory consistency and output-depth policies, detailed templates, JSON contracts, a dependency-free RAG subsystem, validators and regression tests. Project architecture data belongs separately in `/home/ubuntu/architectures/<system-slug>/`.

## Package map

- `AGENT.md`, `SYSTEM-PROMPT.md`, `agent/`: operating contract, activation prompt, modular skills/profiles, manifest, and workflow routing.
- `OUTPUT-DEPTH-AND-AMPLIFIER.md`: mandatory per-artifact depth review, anti-shortcut checks, checkpoint/handoff guidance and a final-stage contradiction/coverage audit; runtime loads this policy into every session.
- `CONSISTENCY-AND-POLISH-POLICY.md`: authority rules and a repeated compare → repair → reread → recheck loop across requirements, decisions, C1–C4, diagrams, contracts, deployment and reports. Runtime loads this policy into every session.
- `templates/validation-reports/architecture-consistency-ledger.md`, `diagram-coverage-matrix.md`, `consistency-review-report.md`: project-level artifacts for preserving architecture invariants and mapping every applicable stable ID to the correct diagrams.
- `FINAL-CONSISTENCY-POLISH-PROMPT.md`: concise English invocation prompt for a fresh end-to-end consistency and diagram-coverage pass.
- `policies/diagram-selection-policy.md`, `policies/architecture-style-selection.md`: evidence-led view selection for large systems and a microservices-vs-alternatives decision method. The runtime loads these policies directly into every session.
- `rag/`, `knowledge-base/`: offline BM25 retrieval implementation and general evidence guidance.
- `schemas/`, `templates/`, `policies/`: registry contracts, reusable document templates and normative rules.
- `scripts/`, `tests/`: structural, artifact-depth, consistency-artifact, release-status coherence and regression checks. `validate_release_status.py` prevents contradictory Gate 7/manifest/findings from being reported as a clean release.
- `examples/sample-system/`: sample system, C1–C4 decomposition, registries, functions, ADRs, cross-cutting views and generated reports.

## Retrieval-augmented workflow

The included RAG implementation is real and local: Markdown, text and JSON files are chunked and ranked using BM25, then returned with source path and chunk citations. It has no third-party dependencies and makes no network calls. Build a separate index for each target architecture to prevent system-context mixing:

```bash
cd /home/ubuntu/architecture-assistant
python3 rag/cli.py index /home/ubuntu/architectures/<system-slug> --output /home/ubuntu/architectures/<system-slug>/.rag/index.json
python3 rag/cli.py search 'container responsibilities and data ownership' --index /home/ubuntu/architectures/<system-slug>/.rag/index.json -k 5
```

Retrieval is lexical, not embedding-based; it can miss synonyms and paraphrases. The index is a convenience for evidence discovery, not a source of truth. Inspect cited files, preserve provenance, and do not infer that an unreturned document does not exist. Do not index secrets. See `rag/README.md` for implementation and extension details.

## Operate the assistant

Follow `WORKFLOW.md` in autonomous mode: the assistant establishes a canonical consistency ledger and diagram-coverage matrix, carries them through all stages, compares cross-document claims, repairs evidence-supported conflicts, and rereads changed files and dependents until a full pass finds no new material issue or records a blocker/checkpoint. It does not stop for routine questions or per-stage/per-file approval. Unknowns become labeled and actionable; safe independent work continues. Runtime defaults to high reasoning effort and a larger, configurable step/token budget; persistent session transcripts and portable Markdown checkpoints support pause/resume and model switching. These controls improve process reliability but cannot guarantee absolute completeness. Edits are bounded to the configured architecture documentation folder, and replaced files are backed up. Configure `OPENAI_API_BASE` and `OPENAI_API_KEY`; see `agent/README.md`.

To initialize a new system, start from `templates/system/architecture-skeleton/`, create `/home/ubuntu/architectures/<system-slug>/`, and populate the registries using `schemas/`. Mark facts, assumptions, proposals and unresolved items separately. Continue existing systems by reading their overview, manifest, registry, decisions and last validation report first; preserve stable IDs and accepted decisions.

## Run the agent

Configure `OPENAI_API_BASE` and `OPENAI_API_KEY`, inspect available models, then run `python3 /home/ubuntu/architecture-assistant/agent/runtime.py --system-dir /home/ubuntu/architectures/<system-slug> --model <available-model> 'Read idea.md completely and follow all package policies. Produce the staged architecture, maintain its consistency ledger and diagram-coverage matrix, then run the iterative final consistency polish; reread and recheck every repaired artifact and diagram, and report unresolved blockers honestly.'`. The runtime prints a session ID and checkpoint/resume command. Use `--resume --session-id <id> --model <different-tool-capable-model>` to continue with another model. See `agent/README.md` and the standalone [final consistency-polish prompt](FINAL-CONSISTENCY-POLISH-PROMPT.md).

## Validate and test

Run `python3 /home/ubuntu/architecture-assistant/scripts/validate_architecture.py /home/ubuntu/architectures/<system-slug>`, `python3 /home/ubuntu/architecture-assistant/scripts/validate_artifact_depth.py /home/ubuntu/architectures/<system-slug>`, `python3 /home/ubuntu/architecture-assistant/scripts/validate_consistency_artifacts.py /home/ubuntu/architectures/<system-slug>`, and finally `python3 /home/ubuntu/architecture-assistant/scripts/validate_release_status.py /home/ubuntu/architectures/<system-slug>`. The first checks registry structure/references and status consistency; the second checks family-specific outline topics; the third checks required consistency artifacts, coverage rows for in-scope IDs, and referenced local diagram files. All are limited evidence—not semantic contradiction detection, human approval, security, diagram rendering, or production readiness. Reports are written under the target system's `validation/`.

Run the full assistant test suite with `python3 -m unittest discover -s /home/ubuntu/architecture-assistant/tests -v`. The suite covers architecture failure scenarios, unsafe-reference rejection, symlink/hardlink path containment, persistent checkpoint/resume behavior, output-limit continuation, self-approval rejection, coverage accounting, artifact-depth outline checks, consistency-matrix coverage and RAG ranking/chunking. Live provider connectivity and model quality still require separate operator testing. See [`REVIEW-AND-IMPROVEMENTS-AR.md`](REVIEW-AND-IMPROVEMENTS-AR.md) for the prior audit, and [`COMPARATIVE-GITHUB-REVIEW-AR.md`](COMPARATIVE-GITHUB-REVIEW-AR.md) for the 10-project public GitHub comparison and current evidence-based improvements. The suite currently contains 57 passing tests; the included ACC Ecosystem example deliberately remains Gate 7 `BLOCKED` until its recorded findings are actually resolved.

## Languages and maintenance

Generated architecture prose follows the user's selected language (English or Arabic), while IDs/code symbols remain stable. Keep one authoritative description per element. When changing assistant policies or validators, add regression cases and rerun the suite; when architecture changes, update the changelog and revalidate affected gates.
