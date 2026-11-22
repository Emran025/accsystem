#!/usr/bin/env python3
"""Generate a row-level, traceable matrix of active strict-ready predicates."""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(VALIDATION_DIR))

import generate_strict_ready_dependency_ledger as dependency_ledger  # noqa: E402

validator = dependency_ledger.validator
FIELDS = (
    "baseline_commit",
    "requirement_id",
    "level",
    "phase_id",
    "document_path",
    "parent_requirement_id",
    "title",
    "statement",
    "status",
    "predicate_categories",
    "predicate_count",
    "use_case_id_source",
    "use_case_rgap_refs",
    "use_case_rgap_link_count",
    "acceptance_criteria",
    "open_decisions_source",
    "open_decision_refs",
    "decision_reference_count",
    "matched_adr_registry_statuses",
    "decision_refs_without_adr_match",
    "planned_verification_source",
)


def _unique_normalized_references(value: str) -> list[str]:
    """Return distinct recorded tokens in source order; never infer their status."""
    references = [validator._normal(item) for item in validator.split_values(value)]
    return list(dict.fromkeys(reference for reference in references if reference))


def build_row_matrix(
    rows: list[dict[str, str]],
    baseline_commit: str,
    decision_statuses: dict[str, str],
) -> list[dict[str, str]]:
    """Make one row per active requirement with exact triggering fields and links."""
    if not dependency_ledger.BASELINE_RE.fullmatch(baseline_commit):
        raise ValueError("baseline_commit must be a full 40-character lowercase Git SHA")

    matrix: list[dict[str, str]] = []
    for source_row in rows:
        findings = validator.strict_ready_findings(source_row)
        if not findings:
            continue
        requirement_id = source_row.get("requirement_id", "").strip()
        if not requirement_id:
            raise ValueError("active blocker row is missing requirement_id")

        categories = [category for category, _message in findings]
        has_use_case = "use_case" in categories
        gap_refs = sorted(set(validator.GAP_RE.findall(source_row.get("use_case_id", "")))) if has_use_case else []
        decision_refs = _unique_normalized_references(source_row.get("open_decisions", "")) if "decision" in categories else []
        matched_adrs: list[str] = []
        unmatched_refs: list[str] = []
        for reference in decision_refs:
            adr_match = re.fullmatch(r"(ADR-\d+)(?:-GATE)?", reference)
            adr_id = adr_match.group(1) if adr_match else ""
            if adr_id and adr_id in decision_statuses:
                status = decision_statuses[adr_id]
                matched_adrs.append(f"{reference} => {adr_id} [{status}]")
            else:
                unmatched_refs.append(reference)

        matrix.append({
            "baseline_commit": baseline_commit,
            "requirement_id": requirement_id,
            "level": source_row.get("level", "").strip(),
            "phase_id": source_row.get("phase_id", "").strip(),
            "document_path": source_row.get("document_path", "").strip(),
            "parent_requirement_id": source_row.get("parent_requirement_id", "").strip(),
            "title": source_row.get("title", "").strip(),
            "statement": source_row.get("statement", "").strip(),
            "status": source_row.get("status", "").strip(),
            "predicate_categories": ";".join(dependency_ledger.PREDICATE_NAMES[category] for category in categories),
            "predicate_count": str(len(categories)),
            "use_case_id_source": source_row.get("use_case_id", "") if has_use_case else "",
            "use_case_rgap_refs": ";".join(gap_refs) if gap_refs else ("(no RGAP ID recorded)" if has_use_case else ""),
            "use_case_rgap_link_count": str(len(gap_refs)),
            "acceptance_criteria": source_row.get("acceptance_criteria", "").strip(),
            "open_decisions_source": source_row.get("open_decisions", "") if "decision" in categories else "",
            "open_decision_refs": ";".join(decision_refs),
            "decision_reference_count": str(len(decision_refs)),
            "matched_adr_registry_statuses": ";".join(matched_adrs),
            "decision_refs_without_adr_match": ";".join(unmatched_refs),
            "planned_verification_source": source_row.get("verification_refs", "") if "verification" in categories else "",
        })

    level_order = {"main": 0, "sub": 1}
    matrix.sort(key=lambda item: (item["phase_id"], level_order.get(item["level"].lower(), 2), item["requirement_id"]))
    return matrix


def validate_output_path(path: str) -> Path:
    """Resolve output and keep it within the validation directory, including symlinks."""
    output = Path(path).resolve()
    validation_root = VALIDATION_DIR.resolve()
    try:
        output.relative_to(validation_root)
    except ValueError as error:
        raise ValueError("--output must remain inside acc-architecture/validation/") from error
    if output == validation_root:
        raise ValueError("--output must name a file inside acc-architecture/validation/")
    return output


def write_matrix(path: Path, matrix: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(matrix)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="full 40-character source commit SHA")
    parser.add_argument("--output", required=True, help="CSV output path inside acc-architecture/validation/")
    args = parser.parse_args()
    if not dependency_ledger.BASELINE_RE.fullmatch(args.baseline):
        parser.error("--baseline must be a full 40-character lowercase Git SHA")
    try:
        dependency_ledger.verify_baseline_inputs(args.baseline)
        output = validate_output_path(args.output)
    except ValueError as error:
        parser.error(str(error))

    rows, load_errors = validator.load_rows()
    structural_errors = validator.validate(rows, load_errors, require_rows=True, strict_ready=False)
    if structural_errors:
        for error in structural_errors:
            print("ERROR:", error)
        return 1

    matrix = build_row_matrix(rows, args.baseline, dependency_ledger.load_decision_statuses())
    output.parent.mkdir(parents=True, exist_ok=True)
    write_matrix(output, matrix)
    category_totals = {name: 0 for name in dependency_ledger.PREDICATE_ORDER}
    for item in matrix:
        for category in item["predicate_categories"].split(";"):
            category_totals[category] += 1
    predicate_total = sum(int(item["predicate_count"]) for item in matrix)
    print(f"Wrote {len(matrix)} active requirement rows and {predicate_total} predicate tags to {output.relative_to(VALIDATION_DIR.parent)}")
    for category, total in category_totals.items():
        print(f"  {category}: {total} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
