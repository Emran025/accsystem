#!/usr/bin/env python3
"""Generate a grouped, traceable dependency index for strict-ready predicates."""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ACC_ARCH = Path(__file__).resolve().parents[1]
REPO_ROOT = ACC_ARCH.parent
VALIDATION_DIR = ACC_ARCH / "validation"
EXECUTION_PHASES = ACC_ARCH / "execution-phases"
sys.path.insert(0, str(EXECUTION_PHASES))

import validate_requirements as validator  # noqa: E402

BASELINE_RE = re.compile(r"^[0-9a-f]{40}$")
SOURCE_INPUTS = (
    Path("acc-architecture/execution-phases/requirements-registry.csv"),
    Path("acc-architecture/registry/decisions.json"),
)
FIELDS = (
    "baseline_commit",
    "predicate",
    "group_key",
    "reference_kind",
    "syntax_prefix",
    "requirement_status",
    "matched_adr_id",
    "matched_adr_status",
    "affected_requirement_count",
    "main_requirement_count",
    "sub_requirement_count",
    "other_requirement_count",
    "requirement_ids",
)
PREDICATE_NAMES = {
    "status": "lifecycle_status",
    "use_case": "use_case_traceability",
    "decision": "open_decision_reference",
    "verification": "planned_verification",
}
PREDICATE_ORDER = tuple(PREDICATE_NAMES.values())


def load_decision_statuses() -> dict[str, str]:
    """Load recorded ADR statuses without inferring status for other tokens."""
    path = ACC_ARCH / "registry" / "decisions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item.get("status", "") for item in data.get("decisions", [])}


def verify_baseline_inputs(baseline_commit: str) -> None:
    """Require the commit to exist and its grouping inputs to match this worktree."""
    if not BASELINE_RE.fullmatch(baseline_commit):
        raise ValueError("baseline_commit must be a full 40-character lowercase Git SHA")
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", f"{baseline_commit}^{{commit}}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if commit_check.returncode != 0:
        raise ValueError("baseline commit does not exist in this Git repository")

    for source in SOURCE_INPUTS:
        show = subprocess.run(
            ["git", "show", f"{baseline_commit}:{source.as_posix()}"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        )
        if show.returncode != 0:
            raise ValueError(f"baseline does not contain required source input {source}")
        current_path = REPO_ROOT / source
        if not current_path.is_file() or show.stdout != current_path.read_bytes():
            raise ValueError(f"current source input differs from baseline: {source}")


def _active_level_map(rows: list[dict[str, str]]) -> dict[str, str]:
    levels_by_id: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row.get("status", "").strip() == "RETIRED":
            continue
        requirement_id = row.get("requirement_id", "").strip()
        if not requirement_id:
            continue
        level = row.get("level", "").strip().lower()
        levels_by_id[requirement_id].add(level if level in {"main", "sub"} else "other")
    return {
        requirement_id: next(iter(levels)) if levels in ({"main"}, {"sub"}) else "other"
        for requirement_id, levels in levels_by_id.items()
    }


def build_dependency_ledger(
    rows: list[dict[str, str]],
    baseline_commit: str,
    decision_statuses: dict[str, str],
) -> list[dict[str, str]]:
    """Group active predicate hits by requirement or traceability reference."""
    if not BASELINE_RE.fullmatch(baseline_commit):
        raise ValueError("baseline_commit must be a full 40-character lowercase Git SHA")

    level_by_id = _active_level_map(rows)
    groups: dict[tuple[str, str], dict[str, object]] = {}

    def add(
        predicate: str,
        group_key: str,
        requirement_id: str,
        *,
        reference_kind: str,
        syntax_prefix: str = "",
        requirement_status: str = "",
        matched_adr_id: str = "",
        matched_adr_status: str = "",
    ) -> None:
        key = (predicate, group_key)
        entry = groups.setdefault(key, {
            "requirement_ids": set(),
            "reference_kind": reference_kind,
            "syntax_prefix": syntax_prefix,
            "requirement_status": requirement_status,
            "matched_adr_id": matched_adr_id,
            "matched_adr_status": matched_adr_status,
        })
        entry["requirement_ids"].add(requirement_id)

    for row in rows:
        findings = {category for category, _message in validator.strict_ready_findings(row)}
        if not findings:
            continue
        requirement_id = row.get("requirement_id", "").strip()
        if not requirement_id:
            continue
        status = row.get("status", "").strip()

        if "status" in findings:
            add(
                PREDICATE_NAMES["status"], requirement_id, requirement_id,
                reference_kind="requirement_id", requirement_status=status,
            )

        if "use_case" in findings:
            gap_ids = sorted(set(validator.GAP_RE.findall(row.get("use_case_id", ""))))
            if gap_ids:
                for gap_id in gap_ids:
                    add(PREDICATE_NAMES["use_case"], gap_id, requirement_id, reference_kind="RGAP_ID")
            else:
                add(
                    PREDICATE_NAMES["use_case"], "(no RGAP ID recorded)", requirement_id,
                    reference_kind="unlinked_placeholder",
                )

        if "decision" in findings:
            for reference in validator.split_values(row.get("open_decisions", "")):
                reference = validator._normal(reference)
                if not reference:
                    continue
                adr_match = re.fullmatch(r"(ADR-\d+)(?:-GATE)?", reference)
                adr_id = adr_match.group(1) if adr_match else ""
                adr_status = decision_statuses.get(adr_id, "") if adr_id else ""
                add(
                    PREDICATE_NAMES["decision"], reference, requirement_id,
                    reference_kind="open_decision_field_token",
                    syntax_prefix=reference.split("-", 1)[0],
                    matched_adr_id=adr_id if adr_id in decision_statuses else "",
                    matched_adr_status=adr_status,
                )

        if "verification" in findings:
            reference = " ".join(row.get("verification_refs", "").split())
            if reference:
                add(
                    PREDICATE_NAMES["verification"], reference, requirement_id,
                    reference_kind="planned_verification_text",
                )

    ledger: list[dict[str, str]] = []
    for (predicate, group_key), entry in sorted(
        groups.items(), key=lambda item: (PREDICATE_ORDER.index(item[0][0]), item[0][1])
    ):
        requirement_ids = sorted(entry["requirement_ids"])
        counts = _count_levels(level_by_id, requirement_ids)
        ledger.append({
            "baseline_commit": baseline_commit,
            "predicate": predicate,
            "group_key": group_key,
            "reference_kind": entry["reference_kind"],
            "syntax_prefix": entry["syntax_prefix"],
            "requirement_status": entry["requirement_status"],
            "matched_adr_id": entry["matched_adr_id"],
            "matched_adr_status": entry["matched_adr_status"],
            "affected_requirement_count": str(len(requirement_ids)),
            "main_requirement_count": str(counts["main"]),
            "sub_requirement_count": str(counts["sub"]),
            "other_requirement_count": str(counts["other"]),
            "requirement_ids": ";".join(requirement_ids),
        })
    return ledger


def _count_levels(level_by_id: dict[str, str], requirement_ids: list[str]) -> dict[str, int]:
    """Count each requirement ID once, assigning conflicting levels to other."""
    counts = {"main": 0, "sub": 0, "other": 0}
    for requirement_id in requirement_ids:
        counts[level_by_id.get(requirement_id, "other")] += 1
    return counts


def write_ledger(path: Path, ledger: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ledger)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="full 40-character source commit SHA")
    parser.add_argument("--output", required=True, help="CSV output path inside acc-architecture/validation/")
    args = parser.parse_args()
    if not BASELINE_RE.fullmatch(args.baseline):
        parser.error("--baseline must be a full 40-character lowercase Git SHA")
    try:
        verify_baseline_inputs(args.baseline)
    except ValueError as error:
        parser.error(str(error))

    output = Path(args.output).resolve()
    try:
        output.relative_to(VALIDATION_DIR.resolve())
    except ValueError:
        parser.error("--output must remain inside acc-architecture/validation/")

    rows, load_errors = validator.load_rows()
    structural_errors = validator.validate(rows, load_errors, require_rows=True, strict_ready=False)
    if structural_errors:
        for error in structural_errors:
            print("ERROR:", error)
        return 1

    ledger = build_dependency_ledger(rows, args.baseline, load_decision_statuses())
    output.parent.mkdir(parents=True, exist_ok=True)
    write_ledger(output, ledger)
    counts: dict[str, int] = defaultdict(int)
    links: dict[str, int] = defaultdict(int)
    for item in ledger:
        counts[item["predicate"]] += 1
        links[item["predicate"]] += int(item["affected_requirement_count"])
    print(f"Wrote {len(ledger)} grouped entries to {output.relative_to(ACC_ARCH.parent)}")
    for predicate in PREDICATE_ORDER:
        print(f"  {predicate}: {counts[predicate]} groups; {links[predicate]} requirement links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
