"""Tests for historical/current reconciliation of strict-ready diagnostic indexes."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ACC_ARCH = Path(__file__).resolve().parents[2]
VALIDATION_DIR = ACC_ARCH / "validation"
sys.path.insert(0, str(VALIDATION_DIR))

import validate_strict_ready_diagnostic_indexes as index_validator  # noqa: E402


class StrictReadyDiagnosticIndexTests(unittest.TestCase):
    def test_historical_artifact_baselines_are_explicit_and_not_rebased(self):
        self.assertEqual(
            "bb107fd6b9f5d95d27d3367dab6b9cca11d16dfe",
            index_validator.HISTORICAL_SOURCE_SNAPSHOT,
        )
        self.assertEqual(
            "6a773c76badc945bc9d7ea01f6ebbc8cbcf98a65",
            index_validator.HISTORICAL_LEDGER_BASELINE,
        )
        self.assertEqual(
            "507c7523de96818da30b2d4c2abcab23d0e86b0a",
            index_validator.HISTORICAL_MATRIX_BASELINE,
        )
        self.assertEqual(
            index_validator.HISTORICAL_LEDGER_BASELINE,
            index_validator.require_expected_baseline(
                [{"baseline_commit": index_validator.HISTORICAL_LEDGER_BASELINE}],
                index_validator.HISTORICAL_LEDGER_BASELINE,
                "Cycle 07 ledger",
            ),
        )
        with self.assertRaisesRegex(ValueError, "historical baseline"):
            index_validator.require_expected_baseline(
                [{"baseline_commit": index_validator.HISTORICAL_MATRIX_BASELINE}],
                index_validator.HISTORICAL_LEDGER_BASELINE,
                "Cycle 07 ledger",
            )

    def test_link_reconciliation_accepts_equal_sets_and_rejects_drift(self):
        ledger = [
            {"predicate": "lifecycle_status", "requirement_ids": "REQ-A;REQ-B"},
            {"predicate": "planned_verification", "requirement_ids": "REQ-B"},
        ]
        matrix = [
            {"requirement_id": "REQ-A", "predicate_categories": "lifecycle_status"},
            {"requirement_id": "REQ-B", "predicate_categories": "lifecycle_status;planned_verification"},
        ]

        self.assertEqual(3, index_validator.reconcile_associations(ledger, matrix))
        with self.assertRaisesRegex(ValueError, "diagnostic links differ"):
            index_validator.reconcile_associations(ledger, matrix[:1])

    def test_recorded_artifact_links_must_match_regenerated_and_each_other(self):
        ledger = [{"predicate": "lifecycle_status", "requirement_ids": "REQ-A;REQ-B"}]
        matrix = [
            {"requirement_id": "REQ-A", "predicate_categories": "lifecycle_status"},
            {"requirement_id": "REQ-B", "predicate_categories": "lifecycle_status"},
        ]
        self.assertEqual(
            2,
            index_validator.verify_view_links(ledger, matrix, ledger, matrix, "test snapshot"),
        )
        with self.assertRaisesRegex(ValueError, "dependency-ledger links differ"):
            index_validator.verify_view_links(
                ledger,
                matrix,
                [{"predicate": "lifecycle_status", "requirement_ids": "REQ-A"}],
                matrix,
                "test snapshot",
            )
        with self.assertRaisesRegex(ValueError, "row-matrix links differ"):
            index_validator.verify_view_links(ledger, matrix, ledger, matrix[:1], "test snapshot")

    def test_csv_rendering_is_stable_and_uses_lf_terminators(self):
        fields = ("baseline_commit", "requirement_id")
        records = [{"baseline_commit": "a" * 40, "requirement_id": "REQ-01"}]

        first = index_validator.render_csv(fields, records)
        second = index_validator.render_csv(fields, records)

        self.assertEqual(first, second)
        self.assertEqual(
            b"baseline_commit,requirement_id\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,REQ-01\n",
            first,
        )

    def test_historical_and_current_indexes_reconcile_to_their_own_inputs(self):
        results = index_validator.check_indexes()
        historical = results["historical"]
        cycle16 = results["cycle16"]
        cycle17 = results["cycle17"]
        current = results["current"]

        self.assertEqual(268, historical["requirement_rows"])
        self.assertEqual(871, historical["predicate_tags"])
        self.assertEqual(871, historical["row_predicate_associations"])
        self.assertEqual(549, historical["ledger_groups"])
        cycle12 = results["cycle12"]
        self.assertEqual(268, cycle12["requirement_rows"])
        self.assertEqual(870, cycle12["predicate_tags"])
        self.assertEqual(870, cycle12["row_predicate_associations"])
        self.assertEqual(549, cycle12["ledger_groups"])
        cycle13 = results["cycle13"]
        self.assertEqual(268, cycle13["requirement_rows"])
        self.assertEqual(859, cycle13["predicate_tags"])
        self.assertEqual(859, cycle13["row_predicate_associations"])
        self.assertEqual(549, cycle13["ledger_groups"])
        self.assertEqual(
            "b9bcb42e1f2098671b1ee8d7ee53c9160c9e15fb297505de2a5db4c66ddfaa71",
            cycle13["source_inputs_sha256"],
        )
        cycle14 = results["cycle14"]
        self.assertEqual(268, cycle14["requirement_rows"])
        self.assertEqual(855, cycle14["predicate_tags"])
        self.assertEqual(855, cycle14["row_predicate_associations"])
        self.assertEqual(549, cycle14["ledger_groups"])
        self.assertEqual(
            "7256e432ff5ee6a4d3df51f752d4cb937709d8d430433ac8326b43e938fa8c5b",
            cycle14["source_inputs_sha256"],
        )
        cycle15 = results["cycle15"]
        self.assertEqual(268, cycle15["requirement_rows"])
        self.assertEqual(845, cycle15["predicate_tags"])
        self.assertEqual(845, cycle15["row_predicate_associations"])
        self.assertEqual(549, cycle15["ledger_groups"])
        self.assertEqual(
            "18e343ba30d6091315f4e27bb0d4e5d73c57e832e58d9305c513e0214b7fcf0a",
            cycle15["source_inputs_sha256"],
        )
        self.assertEqual(268, cycle16["requirement_rows"])
        self.assertEqual(840, cycle16["predicate_tags"])
        self.assertEqual(840, cycle16["row_predicate_associations"])
        self.assertEqual(549, cycle16["ledger_groups"])
        self.assertEqual(
            "c081c2e85a288a6b365b83a5bd46311613fc84cacb209e5f8575091127f37c7f",
            cycle16["source_inputs_sha256"],
        )
        self.assertEqual(268, cycle17["requirement_rows"])
        self.assertEqual(835, cycle17["predicate_tags"])
        self.assertEqual(835, cycle17["row_predicate_associations"])
        self.assertEqual(549, cycle17["ledger_groups"])
        self.assertEqual("e1afb3623aa07fd47b3d609f7b3e67bdcf6ffead", cycle17["actual_source_snapshot"])
        self.assertEqual("47b8b08b86676233be17063e4101d17d8b27bdfa", cycle17["reconciliation_commit"])
        self.assertEqual(
            "c556587077de798cd764092f3a56361a73b19beda7c975ca7e7dff6e9a2f7118",
            cycle17["source_inputs_sha256"],
        )
        self.assertEqual(268, current["requirement_rows"])
        self.assertEqual(835, current["predicate_tags"])
        self.assertEqual(835, current["row_predicate_associations"])
        self.assertEqual(549, current["ledger_groups"])
        self.assertEqual(
            "c556587077de798cd764092f3a56361a73b19beda7c975ca7e7dff6e9a2f7118",
            current["source_inputs_sha256"],
        )
        self.assertEqual(
            "1dcb9065e8bf707a5069e32c82bce3deb4022737",
            index_validator.CYCLE17_RECORDED_START_COMMIT,
        )
        self.assertEqual("47b8b08b86676233be17063e4101d17d8b27bdfa", index_validator.current_indexes.CYCLE_START_COMMIT)
        self.assertEqual("strict-ready-dependency-ledger-cycle-16.csv", index_validator.CYCLE16_LEDGER_PATH.name)
        self.assertEqual("strict-ready-row-matrix-cycle-16.csv", index_validator.CYCLE16_MATRIX_PATH.name)
        self.assertEqual("f56df9778c146ab5d529e0073ec8a2e20851ce71", index_validator.CYCLE16_SOURCE_SNAPSHOT)
        self.assertEqual(
            "7a0a295c3806365b9100b79edf3032c377944d4d6b9d8204510bddbf70d7cac8",
            cycle12["source_inputs_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
