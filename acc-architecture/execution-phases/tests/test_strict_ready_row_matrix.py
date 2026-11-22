"""Tests for the strict-ready row matrix generator."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ACC_ARCH = Path(__file__).resolve().parents[2]
VALIDATION_DIR = ACC_ARCH / "validation"
sys.path.insert(0, str(VALIDATION_DIR))

import generate_strict_ready_row_matrix as row_matrix  # noqa: E402

BASELINE = "a" * 40


class StrictReadyRowMatrixTests(unittest.TestCase):
    def test_row_preserves_exact_sources_and_does_not_infer_unknown_decision_status(self):
        rows = [
            {
                "requirement_id": "REQ-PH01-TEST",
                "level": "main",
                "phase_id": "PH-01",
                "document_path": "acc-architecture/execution-phases/phase-01/test.md",
                "title": "Test requirement",
                "statement": "Recorded statement",
                "status": "DRAFT",
                "use_case_id": "TBD (RGAP-PH01-005)",
                "acceptance_criteria": "AC-PH01-TEST-001-01",
                "open_decisions": "ADR-001-GATE; IC-002; none recorded",
                "verification_refs": "TEST (planned): shared test",
            },
            {"requirement_id": "REQ-PH01-ACCEPTED", "status": "ACCEPTED"},
            {"requirement_id": "SREQ-PH01-RETIRED-001", "status": "RETIRED"},
        ]

        matrix = row_matrix.build_row_matrix(rows, BASELINE, {"ADR-001": "proposed"})

        self.assertEqual(1, len(matrix))
        item = matrix[0]
        self.assertEqual("lifecycle_status;use_case_traceability;open_decision_reference;planned_verification", item["predicate_categories"])
        self.assertEqual("4", item["predicate_count"])
        self.assertEqual("TBD (RGAP-PH01-005)", item["use_case_id_source"])
        self.assertEqual("RGAP-PH01-005", item["use_case_rgap_refs"])
        self.assertEqual("AC-PH01-TEST-001-01", item["acceptance_criteria"])
        self.assertEqual("ADR-001-GATE; IC-002; none recorded", item["open_decisions_source"])
        self.assertEqual("ADR-001-GATE;IC-002", item["open_decision_refs"])
        self.assertEqual("2", item["decision_reference_count"])
        self.assertEqual("ADR-001-GATE => ADR-001 [proposed]", item["matched_adr_registry_statuses"])
        self.assertEqual("IC-002", item["decision_refs_without_adr_match"])
        self.assertEqual("TEST (planned): shared test", item["planned_verification_source"])

    def test_current_matrix_reconciles_all_predicates_and_dependency_links(self):
        rows, errors = row_matrix.validator.load_rows()
        self.assertEqual([], errors)
        decision_statuses = row_matrix.dependency_ledger.load_decision_statuses()

        matrix = row_matrix.build_row_matrix(rows, BASELINE, decision_statuses)

        self.assertEqual(268, len(matrix))
        self.assertEqual(835, sum(int(item["predicate_count"]) for item in matrix))
        category_counts = Counter(
            category
            for item in matrix
            for category in item["predicate_categories"].split(";")
        )
        self.assertEqual({
            "lifecycle_status": 268,
            "use_case_traceability": 165,
            "open_decision_reference": 179,
            "planned_verification": 223,
        }, dict(category_counts))
        signatures = Counter(item["predicate_categories"] for item in matrix)
        self.assertEqual(8, len(signatures))
        self.assertEqual(82, signatures["lifecycle_status;use_case_traceability;open_decision_reference;planned_verification"])
        self.assertEqual(165, sum(int(item["use_case_rgap_link_count"]) for item in matrix))
        self.assertEqual(
            0,
            sum(
                "use_case_traceability" in item["predicate_categories"].split(";")
                and not item["use_case_id_source"].strip()
                for item in matrix
            ),
        )
        self.assertEqual(365, sum(int(item["decision_reference_count"]) for item in matrix))
        refs = {ref for item in matrix for ref in item["open_decision_refs"].split(";") if ref}
        self.assertEqual(61, len(refs))
        with tempfile.TemporaryDirectory(dir=VALIDATION_DIR) as temp_dir:
            first = Path(temp_dir) / "first.csv"
            second = Path(temp_dir) / "second.csv"
            row_matrix.write_matrix(first, matrix)
            row_matrix.write_matrix(second, matrix)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_baseline_must_be_a_full_git_sha(self):
        with self.assertRaisesRegex(ValueError, "full 40-character lowercase Git SHA"):
            row_matrix.build_row_matrix([], "507c752", {})

    def test_output_path_rejects_external_traversal_and_symlink_targets(self):
        with tempfile.TemporaryDirectory() as target_dir:
            token = Path(target_dir).name
            link = VALIDATION_DIR / f".row-matrix-output-test-{token}"
            link.symlink_to(target_dir, target_is_directory=True)
            output_paths = [
                Path(target_dir) / "outside.csv",
                VALIDATION_DIR / ".." / f"outside-{token}.csv",
                link / "through-link.csv",
            ]
            try:
                for path in output_paths:
                    with self.subTest(path=path):
                        with self.assertRaisesRegex(ValueError, "must remain inside"):
                            row_matrix.validate_output_path(str(path))
                allowed = VALIDATION_DIR / "inside-test.csv"
                self.assertEqual(allowed.resolve(), row_matrix.validate_output_path(str(allowed)))
            finally:
                link.unlink(missing_ok=True)

    def test_cli_rejects_baseline_input_mismatch_before_writing(self):
        with tempfile.TemporaryDirectory(dir=VALIDATION_DIR) as temp_dir:
            output = Path(temp_dir) / "must-not-be-created.csv"
            argv = ["generator", "--baseline", BASELINE, "--output", str(output)]
            with patch.object(
                row_matrix.dependency_ledger,
                "verify_baseline_inputs",
                side_effect=ValueError("current source input differs from baseline"),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    with patch.object(row_matrix.sys, "argv", argv):
                        with self.assertRaises(SystemExit) as error:
                            row_matrix.main()
            self.assertEqual(2, error.exception.code)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
