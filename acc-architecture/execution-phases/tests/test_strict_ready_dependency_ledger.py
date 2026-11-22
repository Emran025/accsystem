"""Tests for the Cycle 07 strict-ready dependency ledger generator."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ACC_ARCH = Path(__file__).resolve().parents[2]
VALIDATION_DIR = ACC_ARCH / "validation"
sys.path.insert(0, str(VALIDATION_DIR))

import generate_strict_ready_dependency_ledger as ledger  # noqa: E402

BASELINE = "a" * 40


class StrictReadyDependencyLedgerTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {
                "requirement_id": "REQ-PH01-TEST",
                "level": "main",
                "status": "DRAFT",
                "use_case_id": "TBD (RGAP-PH01-001)",
                "open_decisions": "ADR-001-GATE, IC-002, none recorded",
                "verification_refs": "TEST (planned): shared test",
            },
            {
                "requirement_id": "SREQ-PH01-TEST-001",
                "level": "sub",
                "status": "OWNER_REVIEW",
                "use_case_id": "TBD (RGAP-PH01-001)",
                "open_decisions": "ADR-001-GATE",
                "verification_refs": "TEST (planned): shared test",
            },
            {
                "requirement_id": "SREQ-PH01-TEST-RETIRED",
                "level": "sub",
                "status": "RETIRED",
                "use_case_id": "TBD (RGAP-PH01-001)",
                "open_decisions": "ADR-001-GATE",
                "verification_refs": "TEST (planned): retired test",
            },
        ]

    def test_groups_predicates_and_links_without_inventing_non_adr_status(self):
        rows = ledger.build_dependency_ledger(self.rows, BASELINE, {"ADR-001": "proposed"})
        by_key = {(row["predicate"], row["group_key"]): row for row in rows}

        self.assertEqual(6, len(rows))
        self.assertEqual("2", by_key[("use_case_traceability", "RGAP-PH01-001")]["affected_requirement_count"])
        adr = by_key[("open_decision_reference", "ADR-001-GATE")]
        self.assertEqual("ADR-001", adr["matched_adr_id"])
        self.assertEqual("proposed", adr["matched_adr_status"])
        self.assertEqual("2", adr["affected_requirement_count"])
        non_adr = by_key[("open_decision_reference", "IC-002")]
        self.assertEqual("IC", non_adr["syntax_prefix"])
        self.assertEqual("", non_adr["matched_adr_id"])
        self.assertEqual("", non_adr["matched_adr_status"])
        self.assertEqual("2", by_key[("planned_verification", "TEST (planned): shared test")]["affected_requirement_count"])
        self.assertNotIn("SREQ-PH01-TEST-RETIRED", ";".join(row["requirement_ids"] for row in rows))

    def test_duplicate_id_across_levels_is_counted_once_as_other(self):
        duplicate_rows = [
            {"requirement_id": "REQ-PH01-DUP", "level": "main", "status": "DRAFT"},
            {"requirement_id": "REQ-PH01-DUP", "level": "sub", "status": "DRAFT"},
        ]

        rows = ledger.build_dependency_ledger(duplicate_rows, BASELINE, {})

        self.assertEqual(1, len(rows))
        self.assertEqual("1", rows[0]["affected_requirement_count"])
        self.assertEqual("0", rows[0]["main_requirement_count"])
        self.assertEqual("0", rows[0]["sub_requirement_count"])
        self.assertEqual("1", rows[0]["other_requirement_count"])

    def test_unlinked_use_case_placeholder_is_retained_for_follow_up(self):
        rows = ledger.build_dependency_ledger(
            [{"requirement_id": "REQ-PH01-NO-GAP", "level": "main", "status": "DRAFT", "use_case_id": "TBD"}],
            BASELINE,
            {},
        )
        gap = next(row for row in rows if row["predicate"] == "use_case_traceability")

        self.assertEqual("(no RGAP ID recorded)", gap["group_key"])
        self.assertEqual("unlinked_placeholder", gap["reference_kind"])
        self.assertEqual("REQ-PH01-NO-GAP", gap["requirement_ids"])

    def test_baseline_must_be_a_full_git_sha(self):
        with self.assertRaises(ValueError):
            ledger.build_dependency_ledger(self.rows, "6a773c7", {"ADR-001": "proposed"})

    def test_baseline_commit_and_grouping_inputs_are_verified(self):
        source_blobs = [(ledger.REPO_ROOT / source).read_bytes() for source in ledger.SOURCE_INPUTS]
        matching_results = [Mock(returncode=0, stdout=b"")]
        matching_results.extend(Mock(returncode=0, stdout=blob) for blob in source_blobs)
        with patch.object(ledger.subprocess, "run", side_effect=matching_results) as run:
            ledger.verify_baseline_inputs(BASELINE)
        self.assertEqual(1 + len(source_blobs), run.call_count)
        self.assertEqual(
            [["git", "cat-file", "-e", f"{BASELINE}^{{commit}}"]]
            + [["git", "show", f"{BASELINE}:{source.as_posix()}"] for source in ledger.SOURCE_INPUTS],
            [call.args[0] for call in run.call_args_list],
        )

        with patch.object(ledger.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "full 40-character lowercase Git SHA"):
                ledger.verify_baseline_inputs("not-a-sha")
        run.assert_not_called()

        mismatched_results = [
            Mock(returncode=0, stdout=b""),
            Mock(returncode=0, stdout=source_blobs[0]),
            Mock(returncode=0, stdout=b"different input"),
        ]
        with patch.object(ledger.subprocess, "run", side_effect=mismatched_results):
            with self.assertRaisesRegex(ValueError, "differs from baseline"):
                ledger.verify_baseline_inputs(BASELINE)

        missing_source_results = [Mock(returncode=0, stdout=b""), Mock(returncode=0, stdout=source_blobs[0]), Mock(returncode=1, stdout=b"")]
        with patch.object(ledger.subprocess, "run", side_effect=missing_source_results):
            with self.assertRaisesRegex(ValueError, "does not contain required source input"):
                ledger.verify_baseline_inputs(BASELINE)

        with patch.object(ledger.subprocess, "run", return_value=Mock(returncode=1, stdout=b"")):
            with self.assertRaisesRegex(ValueError, "commit does not exist"):
                ledger.verify_baseline_inputs(BASELINE)

    def test_cli_rejects_output_outside_validation_including_traversal_and_symlink(self):
        with tempfile.TemporaryDirectory() as target_dir:
            token = Path(target_dir).name
            link = ledger.VALIDATION_DIR / f".output-link-test-{token}"
            link.symlink_to(target_dir, target_is_directory=True)
            outputs = [
                Path(target_dir) / "outside.csv",
                ledger.VALIDATION_DIR / ".." / f"outside-{token}.csv",
                link / "through-link.csv",
            ]
            try:
                with patch.object(ledger, "verify_baseline_inputs") as baseline_check:
                    for output in outputs:
                        argv = ["generator", "--baseline", BASELINE, "--output", str(output)]
                        with contextlib.redirect_stderr(io.StringIO()):
                            with patch.object(ledger.sys, "argv", argv):
                                with self.assertRaises(SystemExit) as error:
                                    ledger.main()
                        self.assertEqual(2, error.exception.code)
                        self.assertFalse(output.resolve().exists())
                    self.assertEqual(len(outputs), baseline_check.call_count)
            finally:
                link.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
