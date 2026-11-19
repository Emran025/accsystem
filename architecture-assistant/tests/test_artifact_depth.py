import shutil
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_artifact_depth import assess_document, audit

SAMPLE = Path(__file__).resolve().parents[1] / "examples" / "sample-system"


class ArtifactDepthTests(unittest.TestCase):
    def test_detailed_reference_container_covers_outline_groups(self):
        text = (SAMPLE / "c2-containers/containers/CNT-API.md").read_text(encoding="utf-8")
        result = assess_document("CNT-API.md", "C2", text)
        self.assertEqual("STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW", result["status"])
        self.assertEqual([], result["missing_topics"])

    def test_short_container_is_flagged_with_named_missing_topics(self):
        result = assess_document("CNT-API.md", "C2", "# CNT-API\nHandles requests and saves data.\n")
        self.assertEqual("INCOMPLETE_OUTLINE", result["status"])
        self.assertIn("failure behavior", result["missing_topics"])
        self.assertIn("security/trust", result["missing_topics"])

    def test_template_placeholders_are_reported(self):
        result = assess_document("function.md", "FUNCTION", "# Function\nPurpose {{describe here}}\nTODO add tests")
        self.assertIn("INCOMPLETE_OUTLINE", result["status"])
        self.assertTrue(result["placeholders"])

    def test_audit_writes_report_and_keeps_human_review_limitation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "system"
            shutil.copytree(SAMPLE, root)
            result = audit(root)
            report = root / "validation/depth-review-report.md"
            self.assertEqual("BLOCKED_FOR_CONTENT_REVIEW", result["status"])
            self.assertGreater(result["incomplete"], 0)
            self.assertTrue(report.is_file())
            text = report.read_text(encoding="utf-8")
            self.assertIn("does not judge whether claims are correct", text)
            self.assertIn("CNT-DB", text)

    def test_audit_rejects_symlinked_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "system"
            shutil.copytree(SAMPLE, root)
            external = Path(temp) / "outside.md"
            external.write_text("# Secret external content")
            (root / "linked.md").symlink_to(external)
            registry = root / "registry/elements.json"
            registry.write_text(json.dumps({"elements": [{"id": "CNT-X", "level": "C2", "scope_status": "IN_SCOPE", "doc": "linked.md"}]}))
            result = audit(root)
            self.assertTrue(any("symbolic link" in error for error in result["errors"]))
            self.assertEqual("# Secret external content", external.read_text())

    def test_audit_rejects_hard_linked_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "system"
            shutil.copytree(SAMPLE, root)
            external = Path(temp) / "outside.md"
            external.write_text("# External document")
            (root / "linked.md").hardlink_to(external)
            registry = root / "registry/elements.json"
            registry.write_text(json.dumps({"elements": [{"id": "CNT-X", "level": "C2", "scope_status": "IN_SCOPE", "doc": "linked.md"}]}))
            result = audit(root)
            self.assertTrue(any("hard-linked" in error for error in result["errors"]))

    def test_audit_never_writes_through_report_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "system"
            shutil.copytree(SAMPLE, root)
            external = Path(temp) / "outside-report.md"
            external.write_text("preserve")
            report = root / "validation/depth-review-report.md"
            report.unlink(missing_ok=True)
            report.symlink_to(external)
            result = audit(root)
            self.assertTrue(any("report must not be a symlink" in error for error in result["errors"]))
            self.assertEqual("preserve", external.read_text())


if __name__ == "__main__":
    unittest.main()
