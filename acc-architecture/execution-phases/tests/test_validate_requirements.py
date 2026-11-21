"""Regression tests for the execution-phase requirements validator."""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "validate_requirements.py"
sys.path.insert(0, str(SCRIPT.parent))
import validate_requirements as validator  # noqa: E402


class RequirementsValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows, cls.load_errors = validator.load_rows()

    def validate_copy(self, change=None, strict_ready=False):
        rows = copy.deepcopy(self.rows)
        if change:
            change(rows)
        return validator.validate(rows, list(self.load_errors), require_rows=True, strict_ready=strict_ready)

    def find(self, rows, requirement_id):
        return next(row for row in rows if row["requirement_id"] == requirement_id)

    def test_current_registry_and_documents_pass_structural_validation(self):
        self.assertEqual([], self.validate_copy())

    def test_unknown_actor_reference_fails(self):
        def change(rows):
            self.find(rows, "SREQ-PH01-INST-001")["actor_ids"] = "ACT-NOT-REGISTERED"

        errors = self.validate_copy(change)
        self.assertTrue(any("invalid actor reference 'ACT-NOT-REGISTERED'" in error for error in errors))

    def test_unknown_function_reference_fails(self):
        def change(rows):
            self.find(rows, "SREQ-PH02-PUB-002")["use_case_id"] = "FN-NOT-REGISTERED"

        errors = self.validate_copy(change)
        self.assertTrue(any("unknown function reference FN-NOT-REGISTERED" in error for error in errors))

    def test_tbd_without_documented_gap_fails(self):
        def change(rows):
            self.find(rows, "SREQ-PH01-INST-001")["use_case_id"] = "TBD"

        errors = self.validate_copy(change)
        self.assertTrue(any("TBD related function/use case must cite a documented RGAP" in error for error in errors))

    def test_registry_statement_must_match_exact_document_row(self):
        def change(rows):
            self.find(rows, "SREQ-PH01-INST-001")["statement"] += " Extra untracked behavior."

        errors = self.validate_copy(change)
        self.assertTrue(any("SREQ-PH01-INST-001: registry/document mismatch for sub field 'Statement'" in error for error in errors))

    def test_each_sub_requirement_requires_acceptance_criteria(self):
        def change(rows):
            self.find(rows, "SREQ-PH01-INST-001")["acceptance_criteria"] = ""

        errors = self.validate_copy(change)
        self.assertTrue(any("SREQ-PH01-INST-001: at least one acceptance criterion is required" in error for error in errors))

    def test_strict_ready_does_not_confuse_planned_drafts_with_readiness(self):
        errors = self.validate_copy(strict_ready=True)
        self.assertTrue(any("strict-ready requires ACCEPTED status" in error for error in errors))
        self.assertTrue(any("strict-ready rejects unresolved function/use-case placeholders" in error for error in errors))
        self.assertTrue(any("strict-ready rejects planned-only verification" in error for error in errors))

    def test_empty_registry_fails_when_rows_are_required(self):
        errors = validator.validate([], [], require_rows=True)
        self.assertIn("registry has no rows; at least one requirement row is required in strict mode", errors)

    def test_document_path_outside_phase_folder_is_rejected_before_reading(self):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as outside:
            outside.write("not a requirement document")
            outside.flush()

            def change(rows):
                self.find(rows, "SREQ-PH01-INST-001")["document_path"] = outside.name

            errors = self.validate_copy(change)
        self.assertTrue(any("document_path must be under acc-architecture/execution-phases/phase-01-platform-foundation" in error for error in errors))
        self.assertFalse(any("cannot read requirement document" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
