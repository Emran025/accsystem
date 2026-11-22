#!/usr/bin/env python3
"""Reconcile immutable historical strict-ready indexes and current source indexes."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent
REPO_ROOT = VALIDATION_DIR.parents[1]
sys.path.insert(0, str(VALIDATION_DIR))
sys.path.insert(0, str(VALIDATION_DIR.parent / "execution-phases"))

import generate_strict_ready_current_indexes as current_indexes  # noqa: E402
import generate_strict_ready_dependency_ledger as dependency_ledger  # noqa: E402
import generate_strict_ready_row_matrix as row_matrix  # noqa: E402

validator = dependency_ledger.validator
HISTORICAL_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-07.csv"
HISTORICAL_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-08.csv"
HISTORICAL_SOURCE_SNAPSHOT = "bb107fd6b9f5d95d27d3367dab6b9cca11d16dfe"
HISTORICAL_LEDGER_BASELINE = "6a773c76badc945bc9d7ea01f6ebbc8cbcf98a65"
HISTORICAL_MATRIX_BASELINE = "507c7523de96818da30b2d4c2abcab23d0e86b0a"
CYCLE12_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-12.csv"
CYCLE12_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-12.csv"
CYCLE12_SOURCE_SNAPSHOT = "df75f5d614df01930393168c66fe890563fb171b"
CYCLE12_START_COMMIT = "bf22243023cdf661a241cf2d7c289ef6339ddbe6"
CYCLE12_SOURCE_DIGEST = "7a0a295c3806365b9100b79edf3032c377944d4d6b9d8204510bddbf70d7cac8"
CYCLE13_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-13.csv"
CYCLE13_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-13.csv"
CYCLE13_SOURCE_SNAPSHOT = "6d0d3720d0905bd320f2b96290733fa01e167b54"
CYCLE13_START_COMMIT = "df75f5d614df01930393168c66fe890563fb171b"
CYCLE13_SOURCE_DIGEST = "b9bcb42e1f2098671b1ee8d7ee53c9160c9e15fb297505de2a5db4c66ddfaa71"
CYCLE14_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-14.csv"
CYCLE14_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-14.csv"
CYCLE14_SOURCE_SNAPSHOT = "834b38d3543298e0dc5c7415f36fc444ec785132"
CYCLE14_START_COMMIT = "6d0d3720d0905bd320f2b96290733fa01e167b54"
CYCLE14_SOURCE_DIGEST = "7256e432ff5ee6a4d3df51f752d4cb937709d8d430433ac8326b43e938fa8c5b"
CYCLE15_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-15.csv"
CYCLE15_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-15.csv"
CYCLE15_SOURCE_SNAPSHOT = "bb9a3e12651e11c3a41b90252ed9759d73dc62e5"
CYCLE15_START_COMMIT = "834b38d3543298e0dc5c7415f36fc444ec785132"
CYCLE15_SOURCE_DIGEST = "18e343ba30d6091315f4e27bb0d4e5d73c57e832e58d9305c513e0214b7fcf0a"
CYCLE16_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-16.csv"
CYCLE16_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-16.csv"
CYCLE16_SOURCE_SNAPSHOT = "f56df9778c146ab5d529e0073ec8a2e20851ce71"
CYCLE16_START_COMMIT = "bb9a3e12651e11c3a41b90252ed9759d73dc62e5"
CYCLE16_SOURCE_DIGEST = "c081c2e85a288a6b365b83a5bd46311613fc84cacb209e5f8575091127f37c7f"
CYCLE17_LEDGER_PATH = VALIDATION_DIR / "strict-ready-dependency-ledger-cycle-17.csv"
CYCLE17_MATRIX_PATH = VALIDATION_DIR / "strict-ready-row-matrix-cycle-17.csv"
CYCLE17_RECORDED_START_COMMIT = "1dcb9065e8bf707a5069e32c82bce3deb4022737"
CYCLE17_SOURCE_SNAPSHOT = "e1afb3623aa07fd47b3d609f7b3e67bdcf6ffead"
CYCLE17_RECONCILIATION_COMMIT = "47b8b08b86676233be17063e4101d17d8b27bdfa"
CYCLE17_SOURCE_DIGEST = "c556587077de798cd764092f3a56361a73b19beda7c975ca7e7dff6e9a2f7118"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        return list(reader.fieldnames), list(reader)


def render_csv(fieldnames: tuple[str, ...], records: list[dict[str, str]]) -> bytes:
    """Render canonical UTF-8 CSV bytes using the generators' exact format."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return buffer.getvalue().encode("utf-8")


def git_blob(commit: str, path: Path) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path.as_posix()}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(f"cannot read {path} from historical source snapshot {commit}")
    return result.stdout


def historical_source_snapshot(commit: str) -> tuple[list[dict[str, str]], dict[str, str]]:
    registry_blob = git_blob(commit, dependency_ledger.SOURCE_INPUTS[0])
    decision_blob = git_blob(commit, dependency_ledger.SOURCE_INPUTS[1])
    rows = list(csv.DictReader(io.StringIO(registry_blob.decode("utf-8"), newline="")))
    decision_data = json.loads(decision_blob.decode("utf-8"))
    statuses = {item["id"]: item.get("status", "") for item in decision_data.get("decisions", [])}
    return rows, statuses


def source_inputs_sha256_from_snapshot(commit: str) -> str:
    """Hash registry/decision blobs from a recorded Git source snapshot."""
    digest = hashlib.sha256()
    for source in dependency_ledger.SOURCE_INPUTS:
        content = git_blob(commit, source)
        digest.update(source.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(content)).encode("ascii"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def ledger_associations(records: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {
        (record["predicate"], requirement_id)
        for record in records
        for requirement_id in record["requirement_ids"].split(";")
        if requirement_id
    }


def matrix_associations(records: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {
        (category, record["requirement_id"])
        for record in records
        for category in record["predicate_categories"].split(";")
        if category
    }


def require_expected_baseline(records: list[dict[str, str]], expected: str, label: str) -> str:
    baselines = {record.get("baseline_commit", "") for record in records}
    if baselines != {expected}:
        raise ValueError(f"{label} must retain its historical baseline {expected}; found {sorted(baselines)}")
    return expected


def reconcile_associations(
    ledger_records: list[dict[str, str]],
    matrix_records: list[dict[str, str]],
) -> int:
    ledger_links = ledger_associations(ledger_records)
    matrix_links = matrix_associations(matrix_records)
    if ledger_links != matrix_links:
        ledger_only = sorted(ledger_links - matrix_links)[:5]
        matrix_only = sorted(matrix_links - ledger_links)[:5]
        raise ValueError(f"diagnostic links differ; ledger-only={ledger_only}; matrix-only={matrix_only}")
    return len(ledger_links)


def verify_view_links(
    recorded_ledger: list[dict[str, str]],
    recorded_matrix: list[dict[str, str]],
    generated_ledger: list[dict[str, str]],
    generated_matrix: list[dict[str, str]],
    label: str,
) -> int:
    if ledger_associations(recorded_ledger) != ledger_associations(generated_ledger):
        raise ValueError(f"{label} dependency-ledger links differ from regenerated links")
    if matrix_associations(recorded_matrix) != matrix_associations(generated_matrix):
        raise ValueError(f"{label} row-matrix links differ from regenerated links")
    recorded_count = reconcile_associations(recorded_ledger, recorded_matrix)
    generated_count = reconcile_associations(generated_ledger, generated_matrix)
    if recorded_count != generated_count:
        raise ValueError(f"{label} recorded and regenerated cross-index link counts differ")
    return recorded_count


def check_historical_indexes() -> dict[str, int]:
    ledger_fields, recorded_ledger = read_csv(HISTORICAL_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(HISTORICAL_MATRIX_PATH)
    if tuple(ledger_fields) != dependency_ledger.FIELDS:
        raise ValueError("Cycle 07 dependency ledger header differs from its historical generator schema")
    if tuple(matrix_fields) != row_matrix.FIELDS:
        raise ValueError("Cycle 08 row matrix header differs from its historical generator schema")

    require_expected_baseline(recorded_ledger, HISTORICAL_LEDGER_BASELINE, "Cycle 07 ledger")
    require_expected_baseline(recorded_matrix, HISTORICAL_MATRIX_BASELINE, "Cycle 08 matrix")
    rows, decision_statuses = historical_source_snapshot(HISTORICAL_SOURCE_SNAPSHOT)
    generated_ledger = dependency_ledger.build_dependency_ledger(rows, HISTORICAL_LEDGER_BASELINE, decision_statuses)
    generated_matrix = row_matrix.build_row_matrix(rows, HISTORICAL_MATRIX_BASELINE, decision_statuses)
    if render_csv(dependency_ledger.FIELDS, generated_ledger) != HISTORICAL_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 07 ledger differs from its immutable historical source snapshot")
    if render_csv(row_matrix.FIELDS, generated_matrix) != HISTORICAL_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 08 matrix differs from its immutable historical source snapshot")
    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 07/08"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("historical matrix predicate total differs from its source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
    }


def check_cycle12_indexes() -> dict[str, int | str]:
    ledger_fields, recorded_ledger = read_csv(CYCLE12_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(CYCLE12_MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 12 dependency ledger header differs from its generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 12 row matrix header differs from its generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {CYCLE12_START_COMMIT}:
        raise ValueError(f"Cycle 12 indexes must retain cycle-start commit {CYCLE12_START_COMMIT}")
    source_digest = source_inputs_sha256_from_snapshot(CYCLE12_SOURCE_SNAPSHOT)
    if source_digest != CYCLE12_SOURCE_DIGEST:
        raise ValueError("Cycle 12 recorded source snapshot no longer matches its expected input digest")
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {source_digest}:
        raise ValueError("Cycle 12 index source-input digest does not match its recorded source snapshot")

    rows, decision_statuses = historical_source_snapshot(CYCLE12_SOURCE_SNAPSHOT)
    generated_ledger = current_indexes._with_snapshot_metadata(
        dependency_ledger.build_dependency_ledger(rows, CYCLE12_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE12_START_COMMIT,
    )
    generated_matrix = current_indexes._with_snapshot_metadata(
        row_matrix.build_row_matrix(rows, CYCLE12_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE12_START_COMMIT,
    )
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != CYCLE12_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 12 dependency ledger differs from its recorded source snapshot")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != CYCLE12_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 12 row matrix differs from its recorded source snapshot")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 12"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 12 row matrix count differs from its source snapshot")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 12 matrix predicate total differs from its source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "source_inputs_sha256": source_digest,
    }


def check_cycle13_indexes() -> dict[str, int | str]:
    ledger_fields, recorded_ledger = read_csv(CYCLE13_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(CYCLE13_MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 13 dependency ledger header differs from its generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 13 row matrix header differs from its generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {CYCLE13_START_COMMIT}:
        raise ValueError(f"Cycle 13 indexes must retain cycle-start commit {CYCLE13_START_COMMIT}")
    source_digest = source_inputs_sha256_from_snapshot(CYCLE13_SOURCE_SNAPSHOT)
    if source_digest != CYCLE13_SOURCE_DIGEST:
        raise ValueError("Cycle 13 recorded source snapshot no longer matches its expected input digest")
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {source_digest}:
        raise ValueError("Cycle 13 index source-input digest does not match its recorded source snapshot")

    rows, decision_statuses = historical_source_snapshot(CYCLE13_SOURCE_SNAPSHOT)
    generated_ledger = current_indexes._with_snapshot_metadata(
        dependency_ledger.build_dependency_ledger(rows, CYCLE13_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE13_START_COMMIT,
    )
    generated_matrix = current_indexes._with_snapshot_metadata(
        row_matrix.build_row_matrix(rows, CYCLE13_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE13_START_COMMIT,
    )
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != CYCLE13_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 13 dependency ledger differs from its recorded source snapshot")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != CYCLE13_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 13 row matrix differs from its recorded source snapshot")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 13"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 13 row matrix count differs from its source snapshot")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 13 matrix predicate total differs from its source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "source_inputs_sha256": source_digest,
    }


def check_cycle14_indexes() -> dict[str, int | str]:
    """Verify the immutable Cycle 14 artifacts against their recorded source snapshot."""
    ledger_fields, recorded_ledger = read_csv(CYCLE14_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(CYCLE14_MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 14 dependency ledger header differs from its generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 14 row matrix header differs from its generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {CYCLE14_START_COMMIT}:
        raise ValueError(f"Cycle 14 indexes must retain cycle-start commit {CYCLE14_START_COMMIT}")
    source_digest = source_inputs_sha256_from_snapshot(CYCLE14_SOURCE_SNAPSHOT)
    if source_digest != CYCLE14_SOURCE_DIGEST:
        raise ValueError("Cycle 14 recorded source snapshot no longer matches its expected input digest")
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {source_digest}:
        raise ValueError("Cycle 14 index source-input digest does not match its recorded source snapshot")

    rows, decision_statuses = historical_source_snapshot(CYCLE14_SOURCE_SNAPSHOT)
    generated_ledger = current_indexes._with_snapshot_metadata(
        dependency_ledger.build_dependency_ledger(rows, CYCLE14_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE14_START_COMMIT,
    )
    generated_matrix = current_indexes._with_snapshot_metadata(
        row_matrix.build_row_matrix(rows, CYCLE14_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE14_START_COMMIT,
    )
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != CYCLE14_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 14 dependency ledger differs from its immutable source snapshot")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != CYCLE14_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 14 row matrix differs from its immutable source snapshot")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 14"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 14 row matrix count differs from its recorded source snapshot")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 14 matrix predicate total differs from its recorded source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "source_inputs_sha256": source_digest,
    }


def check_cycle15_indexes() -> dict[str, int | str]:
    """Verify immutable Cycle 15 indexes against the bb9a3e1 source snapshot."""
    ledger_fields, recorded_ledger = read_csv(CYCLE15_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(CYCLE15_MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 15 dependency ledger header differs from its historical generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 15 row matrix header differs from its historical generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {CYCLE15_START_COMMIT}:
        raise ValueError(f"Cycle 15 indexes must retain their historical baseline {CYCLE15_START_COMMIT}")
    source_digest = source_inputs_sha256_from_snapshot(CYCLE15_SOURCE_SNAPSHOT)
    if source_digest != CYCLE15_SOURCE_DIGEST:
        raise ValueError("Cycle 15 recorded source snapshot no longer matches its expected input digest")
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {source_digest}:
        raise ValueError("Cycle 15 index source-input digest does not match its historical source snapshot")

    rows, decision_statuses = historical_source_snapshot(CYCLE15_SOURCE_SNAPSHOT)
    generated_ledger = current_indexes._with_snapshot_metadata(
        dependency_ledger.build_dependency_ledger(rows, CYCLE15_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE15_START_COMMIT,
    )
    generated_matrix = current_indexes._with_snapshot_metadata(
        row_matrix.build_row_matrix(rows, CYCLE15_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE15_START_COMMIT,
    )
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != CYCLE15_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 15 dependency ledger differs from its immutable source snapshot")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != CYCLE15_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 15 row matrix differs from its immutable source snapshot")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 15"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 15 row matrix count differs from its historical source snapshot")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 15 matrix predicate total differs from its historical source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "source_inputs_sha256": source_digest,
    }


def check_cycle16_indexes() -> dict[str, int | str]:
    """Verify immutable Cycle 16 artifacts against their recorded f56df97 source snapshot."""
    ledger_fields, recorded_ledger = read_csv(CYCLE16_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(CYCLE16_MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 16 dependency ledger header differs from its historical generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 16 row matrix header differs from its historical generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {CYCLE16_START_COMMIT}:
        raise ValueError(f"Cycle 16 indexes must retain their historical baseline {CYCLE16_START_COMMIT}")
    source_digest = source_inputs_sha256_from_snapshot(CYCLE16_SOURCE_SNAPSHOT)
    if source_digest != CYCLE16_SOURCE_DIGEST:
        raise ValueError("Cycle 16 recorded source snapshot no longer matches its expected input digest")
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {source_digest}:
        raise ValueError("Cycle 16 index source-input digest does not match its historical source snapshot")

    rows, decision_statuses = historical_source_snapshot(CYCLE16_SOURCE_SNAPSHOT)
    generated_ledger = current_indexes._with_snapshot_metadata(
        dependency_ledger.build_dependency_ledger(rows, CYCLE16_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE16_START_COMMIT,
    )
    generated_matrix = current_indexes._with_snapshot_metadata(
        row_matrix.build_row_matrix(rows, CYCLE16_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE16_START_COMMIT,
    )
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != CYCLE16_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 16 dependency ledger differs from its immutable source snapshot")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != CYCLE16_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 16 row matrix differs from its immutable source snapshot")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 16"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 16 row matrix count differs from its historical source snapshot")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 16 matrix predicate total differs from its historical source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "source_inputs_sha256": source_digest,
    }


def check_cycle17_indexes() -> dict[str, int | str]:
    """Preserve Cycle 17 artifacts and identify their actual input snapshot."""
    ledger_fields, recorded_ledger = read_csv(CYCLE17_LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(CYCLE17_MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 17 dependency ledger header differs from its generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 17 row matrix header differs from its generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {CYCLE17_RECORDED_START_COMMIT}:
        raise ValueError("Cycle 17 artifacts must retain their originally recorded start commit")
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {CYCLE17_SOURCE_DIGEST}:
        raise ValueError("Cycle 17 artifacts do not retain their recorded source-input digest")

    source_digest = source_inputs_sha256_from_snapshot(CYCLE17_SOURCE_SNAPSHOT)
    reconciliation_digest = source_inputs_sha256_from_snapshot(CYCLE17_RECONCILIATION_COMMIT)
    mislabeled_start_digest = source_inputs_sha256_from_snapshot(CYCLE17_RECORDED_START_COMMIT)
    if source_digest != CYCLE17_SOURCE_DIGEST or reconciliation_digest != CYCLE17_SOURCE_DIGEST:
        raise ValueError("Cycle 17 actual source snapshot and baseline reconciliation do not match the recorded digest")
    if mislabeled_start_digest == CYCLE17_SOURCE_DIGEST:
        raise ValueError("Cycle 17 start-commit provenance mismatch was not reproduced")

    rows, decision_statuses = historical_source_snapshot(CYCLE17_SOURCE_SNAPSHOT)
    generated_ledger = current_indexes._with_snapshot_metadata(
        dependency_ledger.build_dependency_ledger(rows, CYCLE17_RECORDED_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE17_RECORDED_START_COMMIT,
    )
    generated_matrix = current_indexes._with_snapshot_metadata(
        row_matrix.build_row_matrix(rows, CYCLE17_RECORDED_START_COMMIT, decision_statuses),
        source_digest,
        CYCLE17_RECORDED_START_COMMIT,
    )
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != CYCLE17_LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 17 dependency ledger differs from its actual recorded source snapshot")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != CYCLE17_MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 17 row matrix differs from its actual recorded source snapshot")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "historical Cycle 17"
    )
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 17 row matrix count differs from its actual source snapshot")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 17 predicate total differs from its actual source snapshot")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "recorded_start_commit": CYCLE17_RECORDED_START_COMMIT,
        "actual_source_snapshot": CYCLE17_SOURCE_SNAPSHOT,
        "reconciliation_commit": CYCLE17_RECONCILIATION_COMMIT,
        "source_inputs_sha256": source_digest,
        "mislabeled_start_digest": mislabeled_start_digest,
    }


def check_current_indexes() -> dict[str, int | str]:
    ledger_fields, recorded_ledger = read_csv(current_indexes.LEDGER_PATH)
    matrix_fields, recorded_matrix = read_csv(current_indexes.MATRIX_PATH)
    if tuple(ledger_fields) != current_indexes.LEDGER_FIELDS:
        raise ValueError("Cycle 18 dependency ledger header differs from its generator schema")
    if tuple(matrix_fields) != current_indexes.MATRIX_FIELDS:
        raise ValueError("Cycle 18 row matrix header differs from its generator schema")

    starts = {record.get("cycle_start_commit", "") for record in recorded_matrix + recorded_ledger}
    if starts != {current_indexes.CYCLE_START_COMMIT}:
        raise ValueError(f"Cycle 18 indexes must retain cycle-start commit {current_indexes.CYCLE_START_COMMIT}")
    source_digest = current_indexes.source_inputs_sha256()
    digests = {record.get("source_inputs_sha256", "") for record in recorded_matrix + recorded_ledger}
    if digests != {source_digest}:
        raise ValueError("Cycle 18 index source-input digest does not match the current registry and decision inputs")

    generated_ledger, generated_matrix, generated_digest = current_indexes.build_current_indexes()
    if generated_digest != source_digest:
        raise ValueError("Cycle 18 source-input digest changed while indexes were generated")
    if render_csv(current_indexes.LEDGER_FIELDS, generated_ledger) != current_indexes.LEDGER_PATH.read_bytes():
        raise ValueError("Cycle 18 dependency ledger is not byte-identical to current generator output")
    if render_csv(current_indexes.MATRIX_FIELDS, generated_matrix) != current_indexes.MATRIX_PATH.read_bytes():
        raise ValueError("Cycle 18 row matrix is not byte-identical to current generator output")

    link_count = verify_view_links(
        recorded_ledger, recorded_matrix, generated_ledger, generated_matrix, "current Cycle 18"
    )
    rows, load_errors = validator.load_rows()
    structural_errors = validator.validate(rows, load_errors, require_rows=True, strict_ready=False)
    if structural_errors:
        raise ValueError("current structural validation failed: " + "; ".join(structural_errors[:5]))
    summary = validator.summarize_strict_ready(rows)
    predicate_count = sum(int(record["predicate_count"]) for record in generated_matrix)
    if len(generated_matrix) != summary["unique_affected_rows"]:
        raise ValueError("Cycle 18 row matrix count differs from the current strict-ready affected-row count")
    if predicate_count != summary["predicate_occurrences"]:
        raise ValueError("Cycle 18 matrix predicate total differs from current strict-ready summary")
    return {
        "requirement_rows": len(generated_matrix),
        "predicate_tags": predicate_count,
        "row_predicate_associations": link_count,
        "ledger_groups": len(generated_ledger),
        "source_inputs_sha256": source_digest,
    }


def check_indexes() -> dict[str, dict[str, int | str]]:
    return {
        "historical": check_historical_indexes(),
        "cycle12": check_cycle12_indexes(),
        "cycle13": check_cycle13_indexes(),
        "cycle14": check_cycle14_indexes(),
        "cycle15": check_cycle15_indexes(),
        "cycle16": check_cycle16_indexes(),
        "cycle17": check_cycle17_indexes(),
        "current": check_current_indexes(),
    }


def main() -> int:
    try:
        results = check_indexes()
    except Exception as error:  # diagnostics should return a concise CLI failure
        print("FAIL:", error)
        return 1
    historical = results["historical"]
    cycle12 = results["cycle12"]
    cycle13 = results["cycle13"]
    cycle14 = results["cycle14"]
    cycle15 = results["cycle15"]
    cycle16 = results["cycle16"]
    cycle17 = results["cycle17"]
    current = results["current"]
    print("PASS: historical Cycle 07/08 indexes retain their recorded source snapshot")
    print(
        f"  historical requirements={historical['requirement_rows']}; predicate_tags={historical['predicate_tags']}; "
        f"row/predicate links={historical['row_predicate_associations']}; ledger_groups={historical['ledger_groups']}"
    )
    print("PASS: Cycle 12 indexes retain their recorded df75f5d source snapshot")
    print(
        f"  Cycle 12 requirements={cycle12['requirement_rows']}; predicate_tags={cycle12['predicate_tags']}; "
        f"row/predicate links={cycle12['row_predicate_associations']}; ledger_groups={cycle12['ledger_groups']}"
    )
    print(f"  cycle_start_commit={CYCLE12_START_COMMIT}; source_inputs_sha256={cycle12['source_inputs_sha256']}")
    print("PASS: historical Cycle 13 indexes retain their recorded 6d0d372 source snapshot")
    print(
        f"  Cycle 13 requirements={cycle13['requirement_rows']}; predicate_tags={cycle13['predicate_tags']}; "
        f"row/predicate links={cycle13['row_predicate_associations']}; ledger_groups={cycle13['ledger_groups']}"
    )
    print(f"  cycle_start_commit={CYCLE13_START_COMMIT}; source_inputs_sha256={cycle13['source_inputs_sha256']}")
    print("PASS: historical Cycle 14 indexes retain their recorded 834b38d source snapshot")
    print(
        f"  Cycle 14 requirements={cycle14['requirement_rows']}; predicate_findings={cycle14['predicate_tags']}; "
        f"row/predicate links={cycle14['row_predicate_associations']}; ledger_groups={cycle14['ledger_groups']}"
    )
    print(f"  cycle_start_commit={CYCLE14_START_COMMIT}; source_inputs_sha256={cycle14['source_inputs_sha256']}")
    print("PASS: immutable Cycle 15 indexes match their recorded bb9a3e1 source snapshot")
    print(
        f"  Cycle 15 requirements={cycle15['requirement_rows']}; predicate_findings={cycle15['predicate_tags']}; "
        f"row/predicate links={cycle15['row_predicate_associations']}; ledger_groups={cycle15['ledger_groups']}"
    )
    print(f"  cycle_start_commit={CYCLE15_START_COMMIT}; source_inputs_sha256={cycle15['source_inputs_sha256']}")
    print("PASS: immutable Cycle 16 indexes match their recorded f56df97 source snapshot")
    print(
        f"  Cycle 16 requirements={cycle16['requirement_rows']}; predicate_findings={cycle16['predicate_tags']}; "
        f"row/predicate links={cycle16['row_predicate_associations']}; ledger_groups={cycle16['ledger_groups']}"
    )
    print(f"  cycle_start_commit={CYCLE16_START_COMMIT}; source_inputs_sha256={cycle16['source_inputs_sha256']}")
    print("PASS: historical Cycle 17 indexes match the e1afb36 source snapshot")
    print(
        f"  Cycle 17 requirements={cycle17['requirement_rows']}; predicate_findings={cycle17['predicate_tags']}; "
        f"row/predicate links={cycle17['row_predicate_associations']}; ledger_groups={cycle17['ledger_groups']}"
    )
    print(
        f"  recorded_cycle_start={cycle17['recorded_start_commit']}; actual_input_snapshot={cycle17['actual_source_snapshot']}; "
        f"matching_reconciliation={cycle17['reconciliation_commit']}; source_inputs_sha256={cycle17['source_inputs_sha256']}"
    )
    print(f"  provenance check: recorded start inputs hash to {cycle17['mislabeled_start_digest']}")
    print("PASS: current Cycle 18 indexes match the live structurally valid source inputs")
    print(
        f"  current requirements={current['requirement_rows']}; predicate_findings={current['predicate_tags']}; "
        f"row/predicate links={current['row_predicate_associations']}; ledger_groups={current['ledger_groups']}"
    )
    print(f"  cycle_start_commit={current_indexes.CYCLE_START_COMMIT}; source_inputs_sha256={current['source_inputs_sha256']}")
    print(
        f"  historical artifact baselines: Cycle 07={HISTORICAL_LEDGER_BASELINE}, "
        f"Cycle 08={HISTORICAL_MATRIX_BASELINE}; shared historical source snapshot={HISTORICAL_SOURCE_SNAPSHOT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
