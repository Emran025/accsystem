#!/usr/bin/env python3
"""Validate presence and ID coverage of consistency-polish artifacts (not semantic consistency)."""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

REQUIRED = {
    "ledger": ("validation/architecture-consistency-ledger.md", ("Canonical terms and boundaries", "Requirements, constraints and invariants", "Decisions and architecture rules")),
    "diagram matrix": ("validation/diagram-coverage-matrix.md", ("Coverage by registered element", "Diagram partition index", "Coverage reconciliation")),
    "review report": ("validation/consistency-review-report.md", ("Findings and disposition", "Read-after-write and checks", "Fixed-point / handoff decision")),
}
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}|\b(?:TODO|TBD|FIXME)\b", re.I)
DISPOSITIONS = ("not applicable", "not_applicable", "not selected", "not_selected", "deferred", "unknown", "blocked", "partition", "out of scope", "out_of_scope")
DIAGRAM_PATH = re.compile(r"(?<![\w])([\w./-]+\.(?:mmd|puml|drawio|mermaid|svg|png|md))(?![\w])", re.I)


def safe_regular_file(root: Path, rel: str) -> tuple[Path | None, str | None]:
    candidate = root / rel
    if candidate.is_symlink():
        return None, f"must not be a symbolic link: {rel}"
    try:
        path = candidate.resolve()
        path.relative_to(root)
    except (OSError, ValueError):
        return None, f"missing or escapes project root: {rel}"
    if not path.is_file():
        return None, f"missing regular file: {rel}"
    if path.stat().st_nlink > 1:
        return None, f"must not be hard-linked: {rel}"
    return path, None


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.count("|") < 2:
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if cells and not all(set(cell) <= set(":- ") for cell in cells):
            rows.append(cells)
    return rows


def audit(root: str | Path) -> dict[str, Any]:
    root = Path(root).resolve()
    errors: list[str] = []
    contents: dict[str, str] = {}
    for label, (rel, headings) in REQUIRED.items():
        path, error = safe_regular_file(root, rel)
        if error:
            errors.append(f"{label}: {error}")
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"{label}: cannot read {rel}: {exc}")
            continue
        contents[label] = text
        for heading in headings:
            if heading.casefold() not in text.casefold():
                errors.append(f"{label}: required section missing: {heading}")
        if PLACEHOLDER.search(text):
            errors.append(f"{label}: unresolved template placeholder/TODO remains")

    registry_path, registry_error = safe_regular_file(root, "registry/elements.json")
    ids: set[str] = set()
    elements: list[Any] = []
    if registry_error:
        errors.append(f"registry: {registry_error}")
    else:
        try:
            payload = json.loads(registry_path.read_text(encoding="utf-8-sig"))
            elements = payload.get("elements", [])
            if not isinstance(elements, list):
                raise ValueError("elements must be an array")
            ids = {str(e["id"]) for e in elements if isinstance(e, dict) and e.get("scope_status") == "IN_SCOPE" and isinstance(e.get("id"), str)}
        except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
            errors.append(f"registry: invalid elements.json: {exc}")

    matrix = contents.get("diagram matrix", "")
    if "C4 Diagram Coverage Matrix" in matrix:
        matrix_types = {"system", "service", "application", "data_store", "component"}
        ids = {str(e["id"]) for e in elements if isinstance(e, dict) and e.get("scope_status") == "IN_SCOPE" and e.get("type") in matrix_types and isinstance(e.get("id"), str)}
    rows_by_id: dict[str, list[str]] = {}
    for cells in table_rows(matrix):
        matched_id = None
        exact_candidates: list[str] = []
        for cell in cells:
            normalized = cell.lstrip("`").strip()
            candidates = [element_id for element_id in ids
                          if re.match(rf"{re.escape(element_id)}(?![A-Z0-9-])", normalized)]
            descriptive = [element_id for element_id in candidates if normalized != element_id]
            if descriptive:
                matched_id = max(descriptive, key=len)
                break
            exact_candidates.extend(candidates)
        if matched_id is None and exact_candidates:
            matched_id = max(exact_candidates, key=len)
        if matched_id and (matched_id not in rows_by_id or len(cells) > len(rows_by_id[matched_id])):
            rows_by_id[matched_id] = cells
    missing = sorted(ids - rows_by_id.keys())
    for element_id in missing:
        errors.append(f"diagram matrix has no row for in-scope ID {element_id}")
    for element_id, cells in rows_by_id.items():
        if any("NOT-APPLICABLE" in cell.upper() for cell in cells):
            continue
        if len(cells) < 6:
            errors.append(f"diagram matrix row for {element_id} has fewer than 6 columns")
            continue
        diagram_reference = (cells[4].strip() if len(cells) >= 8 else cells[3].strip())
        disposition = next((cell.strip().casefold() for cell in reversed(cells)
                             if any(term in cell.casefold() for term in DISPOSITIONS + ("complete", "partial", "missing"))), "")
        if not diagram_reference and not any(term in disposition for term in DISPOSITIONS):
            errors.append(f"diagram matrix row for {element_id} has neither a diagram reference nor an explicit disposition")
        diagram_paths = DIAGRAM_PATH.findall(diagram_reference)
        if diagram_reference and not diagram_paths and not any(term in disposition for term in DISPOSITIONS):
            errors.append(f"diagram matrix row for {element_id} names a view but has no concrete diagram file path")
        for diagram_rel in diagram_paths:
            diagram_path, diagram_error = safe_regular_file(root, diagram_rel)
            if diagram_error:
                errors.append(f"diagram matrix row for {element_id}: {diagram_error}")
        if PLACEHOLDER.search(" | ".join(cells)):
            errors.append(f"diagram matrix row for {element_id} still contains a placeholder")

    report = contents.get("review report", "")
    status_match = re.search(r"\*\*Status:\*\*\s*(PASSED|PARTIAL|BLOCKED)\b", report, re.I)
    if report and not status_match:
        errors.append("review report must state Status as PASSED, PARTIAL, or BLOCKED")
    elif status_match and status_match.group(1).upper() == "PASSED":
        for cells in table_rows(report):
            row = " ".join(cells).casefold()
            if ("blocker" in row or "major" in row) and ("open" in row or "unresolved" in row or "blocked" in row):
                errors.append("review report is PASSED while a BLOCKER/MAJOR finding is open")
                break

    status = "BLOCKED" if errors else "STRUCTURAL_RECORDS_PRESENT_REQUIRES_SEMANTIC_REVIEW"
    out = root / "validation"
    target = out / "consistency-artifact-validation.md"
    writable = True
    try:
        if out.is_symlink():
            raise OSError("validation output directory must not be a symbolic link")
        out.mkdir(exist_ok=True)
        if target.is_symlink() or (target.exists() and target.stat().st_nlink > 1):
            raise OSError("validator report must not be a symlink or hard-linked file")
    except OSError as exc:
        errors.append(str(exc))
        status = "BLOCKED"
        writable = False
    report_lines = ["# Consistency artifact validation", "", f"Status: **{status}**", "",
                    f"In-scope IDs in registry: {len(ids)}", f"IDs represented in diagram matrix: {len(rows_by_id)}", "",
                    "This tool checks that required consistency artifacts exist, that in-scope IDs have diagram-coverage rows/dispositions, and that a report does not claim PASSED with obvious open major findings. It does NOT compare architectural meaning, detect all contradictions, or certify diagrams. Expert rereading and semantic review remain mandatory.", ""]
    report_lines += (["## Findings", ""] + [f"- BLOCKER: {error}" for error in errors]) if errors else ["No structural-record findings detected. This is not semantic approval."]
    if writable:
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=out, prefix=".consistency-validation-", delete=False) as tmp:
                temp_name = tmp.name
                tmp.write("\n".join(report_lines) + "\n")
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(temp_name, target)
        except OSError as exc:
            errors.append(f"Cannot atomically write consistency validation report: {exc}")
            status = "BLOCKED"
            if temp_name:
                try:
                    Path(temp_name).unlink(missing_ok=True)
                except OSError:
                    pass
    return {"status": status, "in_scope_ids": len(ids), "covered_ids": len(rows_by_id), "errors": errors,
            "report": "validation/consistency-artifact-validation.md"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("architecture_dir")
    args = parser.parse_args()
    result = audit(args.architecture_dir)
    print(f"{result['status']}: IDs={result['covered_ids']}/{result['in_scope_ids']}; findings={len(result['errors'])}; report={result['report']}")
    return 1 if result["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
