import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_release_status import audit


class ReleaseStatusTests(unittest.TestCase):
    def make_system(self, root: Path):
        (root / "registry").mkdir(parents=True)
        (root / "validation").mkdir()
        (root / "registry/architecture-manifest.json").write_text(json.dumps({"stages": {
            "discovery": "PASSED", "scope": "PASSED", "C1": "PASSED", "C2": "PASSED",
            "C3": "PASSED", "C4": "PASSED", "validation": "PASSED"}}))
        (root / "validation/validation-status.md").write_text(
            "| Gate 7 | Release | **PASSED** | checks run | evidence |\n")
        (root / "validation/architecture-consistency-ledger.md").write_text("# Ledger\n")
        (root / "validation/diagram-coverage-matrix.md").write_text("# Matrix\n")
        (root / "validation/consistency-review-report.md").write_text(
            "**Status:** PASSED\n## Findings\nNo open findings.\n")
        (root / "validation/traceability-report.md").write_text("# Traceability report\nNo open findings.\n")
        (root / "validation/coverage-report.md").write_text("# Coverage report\nNo open findings.\n")
        (root / "validation/depth-review-report.md").write_text("# Depth review\nOverall: **PASSED**\n")
        (root / "validation/consistency-artifact-validation.md").write_text("# Consistency validation\nStatus: **PASSED**\n")

    def test_consistent_release_pass_is_accepted_as_status_consistency(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.make_system(root)
            result=audit(root)
            self.assertEqual("CONSISTENT", result["status"])
            self.assertEqual([], result["errors"])

    def test_pass_conflicting_with_traceability_blocker_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.make_system(root)
            (root / "validation/traceability-report.md").write_text(
                "# Traceability report\n- BLOCKER: manifest validation remains IN_PROGRESS\n")
            result=audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(any("PASSED despite open BLOCKER/MAJOR" in item for item in result["errors"]))

    def test_gate_manifest_mismatch_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.make_system(root)
            manifest=root / "registry/architecture-manifest.json"
            value=json.loads(manifest.read_text()); value["stages"]["validation"]="IN_PROGRESS"
            manifest.write_text(json.dumps(value))
            result=audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(any("Gate 7 is PASSED but manifest" in item for item in result["errors"]))

    def test_pass_without_required_ledgers_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.make_system(root)
            (root / "validation/diagram-coverage-matrix.md").unlink()
            result=audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(any("release PASS requires validation/diagram-coverage-matrix.md" in item for item in result["errors"]))

    def test_consistent_blocked_release_is_not_misreported_as_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.make_system(root)
            manifest=root / "registry/architecture-manifest.json"
            value=json.loads(manifest.read_text()); value["stages"]["validation"]="BLOCKED"
            manifest.write_text(json.dumps(value))
            (root / "validation/validation-status.md").write_text(
                "| Gate 7 | Release | **BLOCKED** | checks run | blockers remain |\n")
            (root / "validation/traceability-report.md").write_text("- BLOCKER: evidence gap\n")
            result=audit(root)
            self.assertEqual("CONSISTENT", result["status"])
            self.assertEqual("BLOCKED", result["gate_status"])


    def test_audit_output_hardlink_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.make_system(root)
            target=root / "outside.txt"
            target.write_text("preserve me")
            os.link(target, root / "validation/release-status-audit.md")
            result=audit(root)
            self.assertEqual("BLOCKED", result["status"])
            self.assertEqual("preserve me", target.read_text())
            self.assertTrue(any("hard-linked" in item for item in result["errors"]))


if __name__ == "__main__":
    unittest.main()
