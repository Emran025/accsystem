import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_consistency_artifacts import audit


class ConsistencyArtifactTests(unittest.TestCase):
    def make_system(self, root: Path):
        (root / "registry").mkdir(parents=True)
        (root / "validation").mkdir()
        (root / "registry/elements.json").write_text(json.dumps({"elements": [
            {"id": "SYS-ONE", "scope_status": "IN_SCOPE"},
            {"id": "CNT-ONE", "scope_status": "IN_SCOPE"},
            {"id": "EXT-OUT", "scope_status": "OUT_OF_SCOPE"},
        ]}))
        (root / "c1.mmd").write_text("flowchart LR\n A[System]\n")
        (root / "c2.mmd").write_text("flowchart LR\n A[Container]\n")
        (root / "validation/architecture-consistency-ledger.md").write_text(
            "# Ledger\n## Canonical terms and boundaries\n## Requirements, constraints and invariants\n## Decisions and architecture rules\n")
        (root / "validation/diagram-coverage-matrix.md").write_text(
            "# Matrix\n## Coverage by registered element\n"
            "| Element ID | Type | Views | Diagram | Presence | Disposition | Evidence |\n"
            "|---|---|---|---|---|---|---|\n"
            "| SYS-ONE | system | C1 | SYS-CONTEXT c1.mmd | yes | | source |\n"
            "| CNT-ONE | container | C2 | CNT-01 c2.mmd | yes | | source |\n"
            "## Diagram partition index\n## Coverage reconciliation\n")
        (root / "validation/consistency-review-report.md").write_text(
            "# Report\n- **Status:** PASSED\n## Findings and disposition\n"
            "## Diagram/unit coverage review\n## Read-after-write and checks\n## Fixed-point / handoff decision\n")

    def test_complete_structural_records_have_semantic_review_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_system(root)
            result = audit(root)
            self.assertEqual("STRUCTURAL_RECORDS_PRESENT_REQUIRES_SEMANTIC_REVIEW", result["status"])
            self.assertEqual(2, result["covered_ids"])
            self.assertTrue((root / result["report"]).is_file())

    def test_missing_in_scope_id_in_diagram_matrix_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_system(root)
            matrix = root / "validation/diagram-coverage-matrix.md"
            matrix.write_text(matrix.read_text().replace("| CNT-ONE | container | C2 | CNT-01 c2.mmd | yes | | source |\n", ""))
            result = audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(any("no row for in-scope ID CNT-ONE" in error for error in result["errors"]))

    def test_matrix_reference_to_missing_diagram_file_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_system(root)
            (root / "c2.mmd").unlink()
            result = audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(any("missing regular file: c2.mmd" in error for error in result["errors"]))

    def test_passed_report_with_open_major_finding_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_system(root)
            report = root / "validation/consistency-review-report.md"
            report.write_text(report.read_text() + "\n| CON-1 | MAJOR | conflicting claims | OPEN |\n")
            result = audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(any("PASSED while a BLOCKER/MAJOR" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
