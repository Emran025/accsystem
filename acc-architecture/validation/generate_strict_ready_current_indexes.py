#!/usr/bin/env python3
"""Generate current strict-ready indexes with cycle-start commit and input digest."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent
REPO_ROOT = VALIDATION_DIR.parents[1]
EXECUTION_PHASES = VALIDATION_DIR.parent / "execution-phases"
sys.path.insert(0, str(VALIDATION_DIR))
sys.path.insert(0, str(EXECUTION_PHASES))

import generate_strict_ready_dependency_ledger as dependency_ledger  # noqa: E402
import generate_strict_ready_row_matrix as row_matrix  # noqa: E402

validator = dependency_ledger.validator
CYCLE_START_COMMIT = "47b8b08b86676233be17063e4101d17d8b27bdfa"
LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-18.csv"
MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-18.csv"

LEDGER_FIELDS = ("cycle_start_commit", "source_inputs_sha256", *dependency_ledger.FIELDS[1:])
MATRIX_FIELDS = ("cycle_start_commit", "source_inputs_sha256", *row_matrix.FIELDS[1:])


def source_inputs_sha256() -> str:
    """Hash exact registry/decision bytes used to derive the current index groups."""
    digest = hashlib.sha256()
    for source in dependency_ledger.SOURCE_INPUTS:
        path = REPO_ROOT / source
        content = path.read_bytes()
        digest.update(source.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(content)).encode("ascii"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def _with_snapshot_metadata(
    records: list[dict[str, str]],
    source_digest: str,
    cycle_start_commit: str = CYCLE_START_COMMIT,
) -> list[dict[str, str]]:
    rendered: list[dict[str, str]] = []
    for source in records:
        row = {
            "cycle_start_commit": cycle_start_commit,
            "source_inputs_sha256": source_digest,
        }
        row.update({key: value for key, value in source.items() if key != "baseline_commit"})
        rendered.append(row)
    return rendered


def build_current_indexes() -> tuple[list[dict[str, str]], list[dict[str, str]], str]:
    rows, load_errors = validator.load_rows()
    structural_errors = validator.validate(rows, load_errors, require_rows=True, strict_ready=False)
    if structural_errors:
        raise ValueError("structural validation failed: " + "; ".join(structural_errors[:5]))

    source_digest = source_inputs_sha256()
    statuses = dependency_ledger.load_decision_statuses()
    ledger = dependency_ledger.build_dependency_ledger(rows, CYCLE_START_COMMIT, statuses)
    matrix = row_matrix.build_row_matrix(rows, CYCLE_START_COMMIT, statuses)
    return (
        _with_snapshot_metadata(ledger, source_digest),
        _with_snapshot_metadata(matrix, source_digest),
        source_digest,
    )


def write_csv(path: Path, fields: tuple[str, ...], records: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    try:
        ledger, matrix, digest = build_current_indexes()
    except Exception as error:
        print("FAIL:", error)
        return 1

    write_csv(LEDGER_PATH, LEDGER_FIELDS, ledger)
    write_csv(MATRIX_PATH, MATRIX_FIELDS, matrix)
    predicate_total = sum(int(row["predicate_count"]) for row in matrix)
    print("Wrote current Cycle 18 strict-ready indexes")
    print(f"  cycle_start_commit={CYCLE_START_COMMIT}")
    print(f"  source_inputs_sha256={digest}")
    print(f"  active_rows={len(matrix)}; predicate_findings={predicate_total}; ledger_groups={len(ledger)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
