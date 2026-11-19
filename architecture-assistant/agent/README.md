# Runnable, resumable architecture agent

This package includes a tool-calling architecture agent, modular stage skills, local BM25 retrieval, structural validators, automatic architecture-document writes with backup-on-replacement, and durable checkpoints. The runtime is designed for longer staged work: it defaults to high reasoning effort, 64 model/tool cycles per turn and 10,000 completion tokens (subject to provider limits), saves complete conversation snapshots after tool rounds, and emits a provider-neutral Markdown checkpoint. These controls improve capacity and continuity; they do not guarantee semantic completeness or production readiness.

## Configure and run

Set `OPENAI_API_BASE` and `OPENAI_API_KEY` in the shell or a secrets manager; never commit a key. The endpoint must serve `/models` and `/chat/completions`. Confirm tool-calling support with `--list-models`. `ARCH_AGENT_MODEL` or `--model` selects a tool-capable model available at that endpoint.

```bash
export OPENAI_API_BASE='https://your-compatible-endpoint/v1'
export OPENAI_API_KEY='your-secret'
python3 agent/runtime.py --system-dir /path/to/architectures/my-system --list-models
python3 agent/runtime.py --system-dir /path/to/architectures/my-system --model <tool-capable-model> 'Analyze the entire system and produce the complete staged architecture set'
```

A one-shot task prints its session ID, portable checkpoint path and exact resume command. At a safe stage boundary, or when the configured step budget is reached, resume the saved transcript:

```bash
python3 agent/runtime.py --system-dir /path/to/architectures/my-system \
  --resume --session-id <printed-session-id> --model <available-tool-capable-model>
```

You may switch to a different tool-capable model/provider endpoint: session state is provider-neutral Chat Completions conversation data, while `AGENT-CHECKPOINT-<session-id>.md` is a readable handoff summary. The new model must use the same workspace. For manual transfer to a different agent/runtime, provide the Markdown checkpoint and relevant artifacts; do not treat it as a replacement for rereading source evidence. A new session prints its own session ID. `--effort`, `--max-tool-steps`, `--max-completion-tokens`, and `--timeout` can be overridden; provider/model limits still apply.

To work interactively, omit the task text. The agent saves after each complete tool round and can be resumed after `/exit` or interruption using the printed session ID. `--skills id1,id2` narrows active skill instructions; use it only when the task truly needs a narrower workflow.

## What is persisted

Full session JSON is stored under `<system-dir>/.assistant-state/<session-id>.json`; do not put credentials or unrelated secrets in prompts or architecture inputs. The portable Markdown checkpoint summarizes the task, latest stage status, findings, artifact paths, blockers and next actions. The agent exposes `checkpoint_architecture_stage` and is instructed to call it at every stage boundary. On resume, it should verify checkpoint claims against actual files before continuing.

A step/token/provider interruption is not successful completion. The runtime marks a paused or blocked state and provides a resume path; stage completion remains governed by checked exit gates. If a provider returns `finish_reason=length`, the agent is instructed to continue from the cut-off point. Long files are read in explicit ranges; excerpts report their line range and whether more remains. Oversized tool results are reported as unavailable instead of being silently truncated.

## Tools and safety

The agent can search local project docs, list/read files in the configured architecture folder, run structural validation, the artifact-depth outline audit, and consistency-artifact/diagram-ID coverage validation, checkpoint stage progress and write architecture documentation. These validators can expose missing IDs or outline topics; they cannot judge truth, semantic consistency or visual correctness. Existing files are backed up under `.assistant-backups/` before replacement. Tools reject absolute paths, traversal, hidden/internal paths, symlinks, hard links, oversized files and unsupported file types. Writes are bounded to the configured architecture documentation folder; source code, production infrastructure and external systems are out of scope.

Model output is untrusted. Claims must be evidence-backed or explicitly labeled as assumptions, proposals or unresolved. Structural validation is not semantic review, full JSON Schema conformance, security certification or diagram visual validation. Human architecture-owner acceptance remains necessary for consequential decisions and waivers. Model calls may incur provider charges; no live model call is made by the test suite.

## Development and verification

Runtime and tests use Python standard library only. Run:

```bash
python3 -m py_compile agent/runtime.py scripts/*.py rag/*.py tests/*.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_architecture.py examples/sample-system
# Expected: BLOCKED for intentionally short legacy fixture notes; expanded reference artifacts are checked separately.
python3 scripts/validate_artifact_depth.py examples/sample-system
# Expected: BLOCKED until this compact smoke fixture has its project-specific ledger and full ID-to-diagram matrix.
python3 scripts/validate_consistency_artifacts.py examples/sample-system
```

Tests mock the model; provider interoperability still requires an endpoint-specific live integration test. Before production use, add a security review, real-system expert evaluation, model/provider compatibility tests, schema validation, diagram parsing/rendering and human sign-off.
