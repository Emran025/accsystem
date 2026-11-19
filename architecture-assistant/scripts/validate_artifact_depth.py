#!/usr/bin/env python3
"""Heuristic artifact-outline audit; this is not a semantic quality certifier."""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

# Each group is a family-specific topic that must be visibly addressed.
# This intentionally avoids fixed word counts: it checks outline/content coverage,
# then leaves correctness and adequacy to expert review.
PROFILES: dict[str, dict[str, tuple[str, ...]]] = {
    "C2": {
        "purpose and responsibility": ("purpose", "responsibilit", "scope", "owns"),
        "explicit boundary/non-responsibilities": ("does not own", "non-responsibilit", "boundary", "exclusion"),
        "interfaces and dependencies": ("interface", "inbound", "outbound", "communicat", "dependenc", "contract"),
        "data ownership and consistency": ("data", "persist", "store", "schema", "consisten", "retention"),
        "security/trust": ("security", "auth", "trust", "privacy", "secret"),
        "operations/reliability": ("operat", "observab", "monitor", "deploy", "recovery", "scal", "availability"),
        "failure behavior": ("failure", "error", "retry", "timeout", "resilien", "compensation"),
        "technology rationale/decision status": ("technology", "stack", "adr", "decision", "proposed", "confidence"),
        "open risks/owner/action": ("unknown", "open", "risk", "owner", "revisit", "unresolved"),
    },
    "C3": {
        "identity, parent, scope and purpose": ("identity", "parent", "scope", "purpose", "responsibilit"),
        "interfaces/collaborators": ("interface", "collaborat", "dependenc", "caller", "provider"),
        "behavior/rules/state": ("behavior", "processing", "normal path", "business rule", "state", "operation"),
        "data and side effects": ("data", "read/written", "side effect", "persist", "transaction"),
        "failure/security/operations": ("failure", "security", "authorization", "operat", "retry", "timeout"),
        "verification/tests": ("test", "verification", "acceptance", "scenario"),
        "unknowns/traceability": ("unknown", "open", "risk", "owner", "requirement", "adr", "diagram"),
    },
    "C4": {
        "code scope and evidence": ("code", "module", "package", "function", "source", "implementation"),
        "responsibility and behavior": ("purpose", "responsibilit", "behavior", "algorithm", "processing"),
        "interfaces and dependencies": ("interface", "input", "output", "dependenc", "collaborat"),
        "data/state/side effects": ("data", "state", "side effect", "transaction", "persist"),
        "failure/security considerations": ("failure", "error", "security", "authorization", "exception"),
        "tests/verification": ("test", "verification", "acceptance", "coverage"),
        "unknowns and related IDs": ("unknown", "open", "requirement", "adr", "component", "traceability"),
    },
    "FUNCTION": {
        "purpose/trigger/ownership": ("purpose", "trigger", "owner", "operation", "parent"),
        "preconditions/inputs/validation": ("precondition", "input", "parameter", "validat", "constraint"),
        "processing and normal/alternate behavior": ("processing", "step", "normal path", "alternate", "business rule"),
        "outputs/postconditions": ("output", "return", "postcondition", "result", "invariant"),
        "data/side effects/transaction": ("data", "side effect", "transaction", "idempot", "concurren"),
        "failures/retries/timeouts": ("failure", "error", "retry", "timeout", "compensation"),
        "security/authorization": ("security", "auth", "permission", "principal", "audit"),
        "tests/acceptance evidence": ("test", "acceptance", "verification", "scenario"),
        "unknowns/owner/action": ("unknown", "open", "owner", "unresolved", "revisit"),
    },
    "INTERFACE": {
        "provider/consumer/purpose": ("provider", "consumer", "purpose", "caller", "owner"),
        "contract/schema/version": ("contract", "schema", "version", "request", "response", "event"),
        "security/authentication/data classification": ("security", "auth", "trust", "classification", "sensitive"),
        "errors/timeouts/retry/idempotency": ("error", "failure", "timeout", "retry", "idempot"),
        "compatibility/delivery semantics": ("compatib", "ordering", "delivery", "replay", "deprecat"),
        "tests/monitoring/unknowns": ("test", "monitor", "observab", "unknown", "open", "owner"),
    },
    "DECISION": {
        "problem/context/evidence": ("problem", "context", "evidence", "source", "affected"),
        "alternatives/trade-offs": ("alternative", "option", "trade-off", "tradeoff", "considered"),
        "decision/status/rationale": ("decision", "status", "proposed", "accepted", "rationale"),
        "consequences/risks": ("consequence", "risk", "cost", "failure", "security"),
        "confidence/reversibility/revisit": ("confidence", "revers", "revisit", "trigger", "reconsider"),
        "affected IDs/implementation": ("affected", "ids", "migration", "implementation", "owner"),
    },
}

PLACEHOLDERS = [
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile(r"\b(?:TODO|TBD|FIXME|LOREM IPSUM)\b", re.I),
    re.compile(r"(^|\s)\.\.\.(\s|$)"),
]


def infer_family(level: str) -> str | None:
    return {"C2": "C2", "C3": "C3", "C4": "C4", "FUNCTION": "FUNCTION", "INTERFACE": "INTERFACE", "DECISION": "DECISION"}.get(level)


def assess_document(path: str, level: str, text: str) -> dict[str, Any]:
    family = infer_family(level)
    if family is None:
        return {"path": path, "level": level, "status": "NOT_IN_SCOPE", "missing_topics": [], "placeholders": []}
    normalized = re.sub(r"[`*_#>|]", " ", text.lower())
    profile = PROFILES[family]
    missing = [topic for topic, terms in profile.items() if not any(term in normalized for term in terms)]
    placeholders = [pattern.pattern for pattern in PLACEHOLDERS if pattern.search(text)]
    status = "STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW" if not missing and not placeholders else "INCOMPLETE_OUTLINE"
    return {"path": path, "level": level, "family": family, "status": status,
            "missing_topics": missing, "placeholders": placeholders}


def audit(root: str | Path) -> dict[str, Any]:
    root = Path(root).resolve()
    registry_path = root / "registry" / "elements.json"
    errors: list[str] = []
    elements = []
    if registry_path.is_symlink() or (registry_path.exists() and registry_path.stat().st_nlink > 1):
        errors.append("Element registry must not be a symlink or hard-linked file")
    else:
        try:
            payload = json.loads(registry_path.read_text(encoding="utf-8"))
            elements = payload.get("elements", [])
            if not isinstance(elements, list):
                raise ValueError("elements must be an array")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"Cannot read element registry: {exc}")
    docs: dict[tuple[str, str], list[str]] = {}
    for element in elements:
        if not isinstance(element, dict) or element.get("scope_status") != "IN_SCOPE":
            continue
        level = element.get("level", "")
        if infer_family(level) is None:
            continue
        rel = element.get("doc")
        if not isinstance(rel, str) or not rel:
            errors.append(f"{element.get('id', '<unknown>')}: missing document path")
            continue
        candidate = root / rel
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            errors.append(f"{element.get('id')}: unsafe relative document path: {rel}")
            continue
        if candidate.is_symlink():
            errors.append(f"{element.get('id')}: document must not be a symbolic link: {rel}")
            continue
        path = candidate.resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"{element.get('id')}: document path escapes architecture root: {rel}")
            continue
        docs.setdefault((rel, level), []).append(str(element.get("id", "<unknown>")))
    results = []
    for (rel, level), ids in sorted(docs.items()):
        path = root / rel
        if not path.is_file():
            errors.append(f"{', '.join(ids)}: document missing: {rel}")
            continue
        if path.stat().st_nlink > 1:
            errors.append(f"{', '.join(ids)}: document must not be hard-linked: {rel}")
            continue
        try:
            body = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"{', '.join(ids)}: document unreadable: {rel}: {exc}")
            continue
        result = assess_document(rel, level, body)
        result["element_ids"] = ids
        results.append(result)
    incomplete = [item for item in results if item["status"] == "INCOMPLETE_OUTLINE"]
    out = root / "validation"
    target = out / "depth-review-report.md"
    writable = True
    try:
        if out.is_symlink():
            raise OSError("validation output directory must not be a symbolic link")
        out.mkdir(exist_ok=True)
        if target.is_symlink() or (target.exists() and target.stat().st_nlink > 1):
            raise OSError("depth review report must not be a symlink or hard-linked file")
    except OSError as exc:
        errors.append(str(exc))
        writable = False
    overall = "BLOCKED_FOR_CONTENT_REVIEW" if errors or incomplete else "STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW"
    report = ["# Artifact-depth outline review", "",
              f"Overall: **{overall}**", "",
              "This heuristic checks visible topic coverage and common unresolved placeholders only. It does not judge whether claims are correct, sufficiently specific, evidence-backed, internally consistent, secure, or implementation-ready. A structurally present outline always requires expert semantic review.", "",
              f"Documents reviewed: {len(results)}; incomplete outlines: {len(incomplete)}; registry/path findings: {len(errors)}.", "",
              "| Level | IDs | Document | Outline status | Missing topics | Placeholder markers |",
              "|---|---|---|---|---|---|"]
    for item in results:
        report.append(f"| {item['level']} | {', '.join(item['element_ids'])} | `{item['path']}` | {item['status']} | {', '.join(item['missing_topics']) or 'None'} | {', '.join(item['placeholders']) or 'None'} |")
    if errors:
        report += ["", "## Findings"] + [f"- BLOCKER: {error}" for error in errors]
    report += ["", "## Required next step", "",
               "Expand each incomplete artifact using its family template. For genuinely unknown topics, record the unknown, impact, evidence/action, accountable owner or assignment action, and revisit trigger; do not add filler. Reconcile requirements, assumptions, decisions, interfaces, diagrams, deployment and open issues. This report is not a substitute for the final semantic/consistency audit.", ""]
    if writable:
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=out, prefix=".depth-review-", delete=False) as tmp:
                temp_name = tmp.name
                tmp.write("\n".join(report))
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(temp_name, target)
        except OSError as exc:
            errors.append(f"Cannot atomically write depth review report: {exc}")
            overall = "BLOCKED_FOR_CONTENT_REVIEW"
            if temp_name:
                try:
                    Path(temp_name).unlink(missing_ok=True)
                except OSError:
                    pass
    return {"status": overall, "reviewed": len(results), "incomplete": len(incomplete),
            "errors": errors, "results": results, "report": "validation/depth-review-report.md"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("architecture_dir")
    args = parser.parse_args()
    result = audit(args.architecture_dir)
    print(f"{result['status']}: reviewed={result['reviewed']}, incomplete={result['incomplete']}, findings={len(result['errors'])}; report={result['report']}")
    return 1 if result["status"] == "BLOCKED_FOR_CONTENT_REVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
