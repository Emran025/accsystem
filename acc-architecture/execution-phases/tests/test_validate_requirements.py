"""Regression tests for the execution-phase requirements validator."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_contract_reference_cells_label_package_gap_ids_as_unresolved(self):
        failures = []
        for document in sorted(SCRIPT.parent.glob("phase-*/REQ-*.md")):
            contract_column = None
            in_table = False
            for line_number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
                if "API/event/UI contract reference" in line:
                    header = [cell.strip() for cell in line.strip().strip("|").split("|")]
                    contract_column = header.index("API/event/UI contract reference")
                    in_table = True
                    continue
                if not in_table:
                    continue
                if not line.lstrip().startswith("|"):
                    if line.strip():
                        in_table = False
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) <= contract_column or not cells[0].startswith("AC-"):
                    continue
                reference = cells[contract_column]
                if "RGAP-" in reference and not (
                    reference.startswith("NOT SPECIFIED (source reference gap: RGAP-")
                    or "OPEN (related gap: RGAP-" in reference
                ):
                    failures.append(f"{document.relative_to(SCRIPT.parent)}:{line_number}: {reference}")
        self.assertFalse(failures, "\n".join(failures))

    def test_pub_001_is_not_attached_to_duplicate_or_stale_noop_subrequirements(self):
        rows = {row["requirement_id"]: row for row in self.rows}

        self.assertIn("PUB-001", rows["REQ-PH02-LISTING-INGESTION"]["open_decisions"])
        self.assertIn("PUB-001", rows["REQ-PH02-LISTING-LIFECYCLE"]["open_decisions"])
        self.assertIn("PUB-001", rows["SREQ-PH02-LCY-001"]["open_decisions"])
        self.assertNotIn("PUB-001", rows["SREQ-PH02-ING-007"]["open_decisions"])
        self.assertNotIn("PUB-001", rows["SREQ-PH02-ING-008"]["open_decisions"])

    def test_inventory_and_shipment_requirements_link_to_registered_order_confirmation_function(self):
        rows = {row["requirement_id"]: row for row in self.rows}
        expected = {
            "REQ-PH03-INVENTORY-COMMITMENT": "FN-ORD-CONFIRM",
            **{f"SREQ-PH03-INV-{index:03}": "FN-ORD-CONFIRM" for index in range(1, 6)},
            "REQ-PH04-SHIPMENT-CREATION": "FN-ORD-CONFIRM",
            "SREQ-PH04-SHP-001": "FN-ORD-CONFIRM",
            "SREQ-PH04-SHP-002": "FN-ORD-CONFIRM",
            "SREQ-PH04-SHP-003": "FN-ORD-CONFIRM; FN-LIC-ACTIVATE",
            "SREQ-PH04-SHP-004": "FN-ORD-CONFIRM",
        }

        registered_functions = validator.load_function_ids()
        for requirement_id, use_case_id in expected.items():
            with self.subTest(requirement_id=requirement_id):
                self.assertEqual(use_case_id, rows[requirement_id]["use_case_id"])
                self.assertTrue(set(validator.FN_RE.findall(use_case_id)) <= registered_functions)
                self.assertNotIn(
                    "use_case",
                    [category for category, _message in validator.strict_ready_findings(rows[requirement_id])],
                )

    def test_cycle14_function_traces_are_canonical_and_do_not_close_other_predicates(self):
        rows = {row["requirement_id"]: row for row in self.rows}
        expected = {
            "SREQ-PH02-OFR-005": "FN-ORD-RESERVE",
            "SREQ-PH03-PRC-001": "FN-PAY-AUTHORIZE",
            "SREQ-PH03-EXD-004": "FN-ORD-CONFIRM",
            "SREQ-PH03-LDG-002": "FN-PAY-AUTHORIZE",
        }
        registered_functions = validator.load_function_ids()
        for requirement_id, function_id in expected.items():
            with self.subTest(requirement_id=requirement_id):
                row = rows[requirement_id]
                self.assertEqual(function_id, row["use_case_id"])
                self.assertIn(function_id, row["evidence_refs"])
                self.assertTrue(set(validator.FN_RE.findall(row["use_case_id"])) <= registered_functions)
                findings = [category for category, _message in validator.strict_ready_findings(row)]
                self.assertNotIn("use_case", findings)
                self.assertIn("status", findings)
                self.assertIn("verification", findings)
                if row["open_decisions"].strip():
                    self.assertIn("decision", findings)

        # Narrow supporting evidence must not be generalized into unrelated behaviors.
        for requirement_id in ("SREQ-PH01-CONN-003", "SREQ-PH01-CONN-004", "SREQ-PH01-CONN-005"):
            self.assertEqual("TBD (RGAP-PH01-006)", rows[requirement_id]["use_case_id"])
        self.assertEqual("TBD (RGAP-PH03-004)", rows["SREQ-PH03-LDG-001"]["use_case_id"])

    def test_cycle14_function_traces_are_canonical_and_do_not_close_other_predicates(self):
        rows = {row["requirement_id"]: row for row in self.rows}
        expected = {
            "SREQ-PH02-OFR-005": "FN-ORD-RESERVE",
            "SREQ-PH03-PRC-001": "FN-PAY-AUTHORIZE",
            "SREQ-PH03-EXD-004": "FN-ORD-CONFIRM",
            "SREQ-PH03-LDG-002": "FN-PAY-AUTHORIZE",
        }
        registered_functions = validator.load_function_ids()
        for requirement_id, function_id in expected.items():
            with self.subTest(requirement_id=requirement_id):
                row = rows[requirement_id]
                self.assertEqual(function_id, row["use_case_id"])
                self.assertIn(function_id, row["evidence_refs"])
                self.assertTrue(set(validator.FN_RE.findall(row["use_case_id"])) <= registered_functions)
                findings = [category for category, _message in validator.strict_ready_findings(row)]
                self.assertNotIn("use_case", findings)
                self.assertIn("status", findings)
                self.assertIn("verification", findings)
                if row["open_decisions"].strip():
                    self.assertIn("decision", findings)

        # Narrow supporting evidence must not be generalized into unrelated behaviors.
        for requirement_id in ("SREQ-PH01-CONN-003", "SREQ-PH01-CONN-004", "SREQ-PH01-CONN-005"):
            self.assertEqual("TBD (RGAP-PH01-006)", rows[requirement_id]["use_case_id"])
        self.assertEqual("TBD (RGAP-PH03-004)", rows["SREQ-PH03-LDG-001"]["use_case_id"])

    def test_cycle15_reference_narrowing_keeps_source_decisions_and_verification_open(self):
        """Documentary traceability regression only; this does not test application behavior."""
        rows = {row["requirement_id"]: row for row in self.rows}
        expected_decisions = {
            "SREQ-PH02-CHK-003": "UNKN-006, ODEC-009",
            "SREQ-PH03-SAG-001": "",
            "SREQ-PH03-SAG-002": "RP-01, ADR-018-GATE",
            "SREQ-PH03-CNC-001": "",
            "SREQ-PH03-CNC-003": "",
            "SREQ-PH03-CNC-004": "",
            "SREQ-PH03-VRF-001": "",
            "SREQ-PH04-DEX-002": "",
            "SREQ-PH03-EXD-002": "ADR-008-GATE",
            "SREQ-PH03-EXD-003": "",
            "SREQ-PH03-EXD-004": "",
            "SREQ-PH04-DEN-002": "",
            "SREQ-PH04-DEN-003": "",
        }
        expected_status = {
            "SREQ-PH02-CHK-003": "DRAFT",
            "SREQ-PH03-SAG-001": "DRAFT",
            "SREQ-PH03-SAG-002": "DRAFT",
            "SREQ-PH03-CNC-001": "DRAFT",
            "SREQ-PH03-CNC-003": "DRAFT",
            "SREQ-PH03-CNC-004": "OWNER_REVIEW",
            "SREQ-PH03-VRF-001": "DRAFT",
            "SREQ-PH04-DEX-002": "OWNER_REVIEW",
            "SREQ-PH03-EXD-002": "OWNER_REVIEW",
            "SREQ-PH03-EXD-003": "OWNER_REVIEW",
            "SREQ-PH03-EXD-004": "DRAFT",
            "SREQ-PH04-DEN-002": "OWNER_REVIEW",
            "SREQ-PH04-DEN-003": "OWNER_REVIEW",
        }
        for requirement_id, decisions in expected_decisions.items():
            with self.subTest(requirement_id=requirement_id):
                row = rows[requirement_id]
                self.assertEqual(decisions, row["open_decisions"])
                self.assertEqual(expected_status[requirement_id], row["status"])
                self.assertIn("planned", row["verification_refs"].lower())
                findings = [category for category, _message in validator.strict_ready_findings(row)]
                self.assertIn("status", findings)
                self.assertIn("verification", findings)
                if decisions:
                    self.assertIn("decision", findings)
                else:
                    self.assertNotIn("decision", findings)

        # Decisions remain open where they materially govern scope or behavior.
        for requirement_id, reference in {
            "SREQ-PH02-CHK-002": "ODEC-003",
            "SREQ-PH02-CHK-005": "ODEC-003",
            "SREQ-PH03-ORD-003": "ADR-018-GATE",
            "SREQ-PH03-CNC-002": "ADR-018-GATE",
            "SREQ-PH03-VRF-003": "ODEC-007",
            "SREQ-PH03-EXD-001": "ODEC-010",
            "SREQ-PH04-DEN-001": "ODEC-010",
        }.items():
            self.assertIn(reference, rows[requirement_id]["open_decisions"])

        decision_scopes = {
            ("phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md", "ODEC-003"):
                {"SREQ-PH02-CHK-002", "SREQ-PH02-CHK-005"},
            ("phase-03-inventory-order-payment-delivery-events/REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY.md", "ADR-018-GATE"):
                {"SREQ-PH03-SAG-002"},
            ("phase-03-inventory-order-payment-delivery-events/REQ-PH03-CANCELLATION-COORDINATION.md", "ODEC-007"):
                set(),
            ("phase-03-inventory-order-payment-delivery-events/REQ-PH03-VOID-AND-REFUND.md", "ODEC-007"):
                {"SREQ-PH03-VRF-003"},
            ("phase-03-inventory-order-payment-delivery-events/REQ-PH03-EXTERNAL-DELIVERY-EVENTS.md", "ODEC-010"):
                {"SREQ-PH03-EXD-001"},
            ("phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-ENABLEMENT.md", "ODEC-010"):
                {"SREQ-PH04-DEN-001"},
            ("phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-EXCEPTIONS.md", "ODEC-007"):
                set(),
        }
        phase_root = SCRIPT.parent
        for (relative_path, decision_id), expected_affected in decision_scopes.items():
            document = (phase_root / relative_path).read_text(encoding="utf-8")
            tables = validator._tables_in_section(document, "## 6. Open decisions and documented gaps")
            table = validator._table_by_header(tables, ("Decision / gate ID", "Source meaning", "Affected sub-requirements"))
            self.assertIsNotNone(table, relative_path)
            cells = next(row for row in table[1:] if row[0] == decision_id)
            affected = {item.strip() for item in cells[2].split(",") if item.strip().startswith("SREQ-")}
            self.assertEqual(expected_affected, affected, relative_path)

        # Parent scopes still show the deferred owner decisions; they were not globally closed.
        for requirement_id, reference in {
            "REQ-PH02-CHECKOUT-PREPARATION": "ODEC-003",
            "REQ-PH03-CANCELLATION-COORDINATION": "ODEC-007",
            "REQ-PH03-VOID-AND-REFUND": "ODEC-007",
            "REQ-PH04-DELIVERY-EXCEPTIONS": "ODEC-007",
            "REQ-PH03-EXTERNAL-DELIVERY-EVENTS": "ODEC-010",
            "REQ-PH04-DELIVERY-ENABLEMENT": "ODEC-010",
        }.items():
            self.assertIn(reference, rows[requirement_id]["open_decisions"])

    def test_cycle16_decision_scope_and_open_policy_gaps_remain_source_bounded(self):
        """Documentary traceability regression only; not application or acceptance testing."""
        rows = {row["requirement_id"]: row for row in self.rows}

        self.assertIn("ADR-019-GATE", rows["REQ-PH03-ORDER-CONFIRMATION"]["open_decisions"])
        self.assertEqual("none recorded", rows["SREQ-PH03-CNF-002"]["open_decisions"])
        self.assertEqual("RP-04", rows["SREQ-PH03-CNF-005"]["open_decisions"])
        self.assertIn("ADR-019-GATE", rows["SREQ-PH03-CNF-006"]["open_decisions"])
        self.assertEqual("", rows["REQ-PH03-INVENTORY-COMMITMENT"]["open_decisions"])
        inventory_scope_reference = (
            "ADR-019 (negative-scope context only; not a gate for inventory commitment or reconciliation)"
        )
        inventory_parent = rows["REQ-PH03-INVENTORY-COMMITMENT"]
        self.assertIn(inventory_scope_reference, inventory_parent["evidence_refs"])
        inventory_doc = (SCRIPT.parent / "phase-03-inventory-order-payment-delivery-events" /
                         "REQ-PH03-INVENTORY-COMMITMENT.md").read_text(encoding="utf-8")
        self.assertIn(inventory_scope_reference, inventory_doc)
        for requirement_id in ("SREQ-PH03-INV-002", "SREQ-PH03-INV-003"):
            self.assertNotIn("ADR-019-GATE", rows[requirement_id]["open_decisions"])
        self.assertNotIn("ADR-019-GATE", rows["REQ-PH03-SOFTWARE-LICENSE-ISSUANCE"]["open_decisions"])
        self.assertEqual("none recorded", rows["SREQ-PH03-MLS-001"]["open_decisions"])

        self.assertIn("ADR-022-GATE", rows["REQ-PH02-RESERVATION-RECOVERY"]["open_decisions"])
        self.assertEqual("RP-03, IC-006", rows["SREQ-PH02-RRC-002"]["open_decisions"])
        self.assertIn("ADR-022-GATE", rows["SREQ-PH02-RRC-006"]["open_decisions"])

        self.assertIn("IC-003", rows["REQ-PH03-PAYMENT-RECONCILIATION"]["open_decisions"])
        self.assertIn("IC-003", rows["SREQ-PH03-PRC-001"]["open_decisions"])
        self.assertNotIn("IC-003", rows["SREQ-PH03-PRC-004"]["open_decisions"])
        self.assertIn("UNKN-005", rows["SREQ-PH03-PRC-004"]["open_decisions"])
        self.assertIn("ADR-016-GATE", rows["SREQ-PH03-PRC-004"]["open_decisions"])
        for requirement_id in (
            "REQ-PH03-PAYMENT-WEBHOOKS",
            "SREQ-PH03-PWH-001",
            "SREQ-PH03-PWH-002",
            "SREQ-PH03-PWH-003",
        ):
            self.assertIn("IC-003", rows[requirement_id]["open_decisions"])

        # The three publication decisions remain separate: allowed fields, receipt/listing ID, lifecycle effects.
        self.assertIn("PUB-004", rows["SREQ-PH02-PUB-001"]["open_decisions"])
        self.assertNotIn("PUB-005", rows["SREQ-PH02-PUB-001"]["open_decisions"])
        self.assertEqual("PUB-005", rows["SREQ-PH02-PUB-004"]["open_decisions"])
        self.assertIn("PUB-006", rows["SREQ-PH02-LCY-001"]["open_decisions"])
        publication_flow = (SCRIPT.parents[1] / "supporting-views" / "dynamic-publication-flow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("| PUB-004 | Maximum listing fields schema", publication_flow)
        self.assertIn("| PUB-005 | Receipt vs queued Catalog-owned ID", publication_flow)
        self.assertIn("| PUB-006 | Map publication/update/withdrawal source events", publication_flow)

        # These policy gaps remain open on their parent requirements; no approval is inferred.
        for requirement_id, reference in {
            "REQ-PH01-OBSERVABILITY-AND-RECOVERY": "UNKN-001",
            "REQ-PH03-PAYMENT-ORCHESTRATION": "UNKN-002",
        }.items():
            self.assertIn(reference, rows[requirement_id]["open_decisions"])
            self.assertIn(
                "decision",
                [category for category, _message in validator.strict_ready_findings(rows[requirement_id])],
            )

    def test_cycle16_offline_rows_are_conditional_and_preserve_backend_authority(self):
        """Documentary requirement regression only; does not execute the courier application."""
        rows = {row["requirement_id"]: row for row in self.rows}
        offline_ids = (
            "SREQ-PH04-OFS-001",
            "SREQ-PH04-OFS-002",
            "SREQ-PH04-OFS-003",
        )
        for requirement_id in offline_ids:
            with self.subTest(requirement_id=requirement_id):
                row = rows[requirement_id]
                self.assertIn("If an owner-approved offline mode is enabled", row["statement"])
                self.assertEqual("OWNER_REVIEW", row["status"])
                self.assertIn("ADR-008-GATE", row["open_decisions"])
                self.assertIn("planned", row["verification_refs"].lower())

        phase_root = SCRIPT.parent
        offline_doc = (phase_root / "phase-04-accmared-internal-delivery" / "REQ-PH04-OFFLINE-COURIER-SYNC.md").read_text(
            encoding="utf-8"
        )
        adr008 = (SCRIPT.parents[1] / "decisions" / "ADR-008.md").read_text(encoding="utf-8")
        courier = (SCRIPT.parents[1] / "c2-containers" / "accmared" / "CNT-AMD-COURIER.md").read_text(
            encoding="utf-8"
        )
        delivery = (SCRIPT.parents[1] / "c2-containers" / "accsystem" / "CNT-ACC-DELIVERY.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("Entries are applied once", offline_doc)
        self.assertIn("Retries and replays do not create duplicate authoritative state changes", offline_doc)
        self.assertIn("are not globally selected by this ADR", adr008)
        self.assertIn("client intent, not authoritative shipment state", courier)
        self.assertIn("alone commits or rejects the authoritative transition", delivery)

    def test_cycle17_scope_corrections_keep_source_gaps_and_owner_states_explicit(self):
        """Documentary traceability regressions only; not application or acceptance tests."""
        rows = {row["requirement_id"]: row for row in self.rows}

        message = rows["SREQ-PH01-MSG-006"]
        self.assertEqual("IC-002, ADR-021-GATE", message["open_decisions"])
        self.assertEqual("DRAFT", message["status"])
        self.assertIn("planned", message["verification_refs"].lower())
        self.assertIn(
            "decision",
            [category for category, _message in validator.strict_ready_findings(message)],
        )
        message_doc = (SCRIPT.parent / "phase-01-platform-foundation" /
                       "REQ-PH01-MESSAGE-RELIABILITY.md").read_text(encoding="utf-8")
        message_tables = validator._tables_in_section(
            message_doc, "## 6. Open decisions and documented gaps"
        )
        message_table = validator._table_by_header(
            message_tables, ("Decision / gate ID", "Source meaning", "Affected sub-requirements")
        )
        self.assertIsNotNone(message_table)
        message_scopes = {row[0]: row[2] for row in message_table[1:]}
        self.assertNotIn("SREQ-PH01-MSG-006", message_scopes["IC-004"])
        self.assertIn("SREQ-PH01-MSG-006", message_scopes["IC-002"])
        self.assertIn("SREQ-PH01-MSG-006", message_scopes["ADR-021-GATE"])

        ph04_rows = {
            "REQ-PH04-DELIVERY-DISPATCH": "DRAFT",
            "REQ-PH04-COURIER-OPERATIONS": "DRAFT",
            "SREQ-PH04-DSP-001": "OWNER_REVIEW",
            "SREQ-PH04-DSP-003": "OWNER_REVIEW",
            "SREQ-PH04-CRO-001": "DRAFT",
        }
        for requirement_id, expected_status in ph04_rows.items():
            with self.subTest(requirement_id=requirement_id):
                row = rows[requirement_id]
                self.assertEqual("", row["open_decisions"])
                self.assertEqual(expected_status, row["status"])
                if row["level"] == "sub":
                    self.assertIn("planned", row["verification_refs"].lower())
                    self.assertNotIn(
                        "decision",
                        [category for category, _message in validator.strict_ready_findings(row)],
                    )
        self.assertIn("ADR-011-GATE", rows["REQ-PH01-ADMIN-ACCESS-CONTROL"]["open_decisions"])

        arch_root = SCRIPT.parents[1]
        courier_container = (arch_root / "c2-containers" / "accmared" /
                             "CNT-AMD-COURIER.md").read_text(encoding="utf-8")
        courier_doc = (SCRIPT.parent / "phase-04-accmared-internal-delivery" /
                       "REQ-PH04-COURIER-OPERATIONS.md").read_text(encoding="utf-8")
        adr011 = (arch_root / "decisions" / "ADR-011.md").read_text(encoding="utf-8")
        self.assertIn("Short-lived tokens", courier_container)
        self.assertNotRegex(courier_container, r"(?i)\b(?:token\s+)?(?:ttl|lifetime)\s*[:=]\s*\d+")
        self.assertIn("no numeric lifetime", courier_doc)
        self.assertIn("RGAP-PH04-002", courier_doc)
        self.assertNotIn("ACT-COURIER", adr011)
        self.assertIn("ACT-PLATFORM-ADMIN", adr011)
        self.assertIn("ACT-SUPPORT-STAFF", adr011)

        dispatch_doc = (SCRIPT.parent / "phase-04-accmared-internal-delivery" /
                        "REQ-PH04-DELIVERY-DISPATCH.md").read_text(encoding="utf-8")
        self.assertIn("do not classify supervisor listing, assignment or reassignment that way", dispatch_doc)
        self.assertIn("no approval policy is inferred", dispatch_doc)
        self.assertIn(
            "supervisor-conflict and prioritization behavior remains unspecified",
            dispatch_doc.lower(),
        )

        criterion_sources = {
            "phase-03-inventory-order-payment-delivery-events/REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY.md":
                ("AC-PH03-LDG-002-01", "RGAP-PH03-004", "FN-PAY-AUTHORIZE § Flow step 3"),
            "phase-03-inventory-order-payment-delivery-events/REQ-PH03-EXTERNAL-DELIVERY-EVENTS.md":
                ("AC-PH03-EXD-004-01", "RGAP-PH03-002", "FN-ORD-CONFIRM; ADR-013"),
        }
        for relative_path, (criterion_id, stale_gap, source) in criterion_sources.items():
            document = (SCRIPT.parent / relative_path).read_text(encoding="utf-8")
            criterion_line = next(
                line for line in document.splitlines() if line.startswith(f"| {criterion_id} |")
            )
            self.assertNotIn(stale_gap, criterion_line)
            self.assertIn(source, criterion_line)

        self.assertIn("ADR-016", rows["SREQ-PH03-LDG-002"]["open_decisions"])
        self.assertIn("ODEC-006", rows["SREQ-PH03-LDG-002"]["open_decisions"])

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

    def test_all_unresolved_use_case_placeholders_require_documented_gap_links(self):
        for placeholder in ("TBC", "UNKNOWN", "UNRESOLVED"):
            with self.subTest(placeholder=placeholder):
                def change(rows):
                    self.find(rows, "SREQ-PH01-POL-001")["use_case_id"] = placeholder

                errors = self.validate_copy(change)
                self.assertTrue(any(
                    f"{placeholder} related function/use case must cite a documented RGAP" in error
                    for error in errors
                ))

        documented_errors = []
        validator._validate_use_case_references(
            {"use_case_id": "UNKNOWN (RGAP-PH01-007)"},
            validator.load_function_ids(),
            "The source gap is RGAP-PH01-007.",
            "synthetic requirement",
            documented_errors,
        )
        self.assertEqual([], documented_errors)

    def test_ldg_003_and_ldg_004_keep_distinct_source_gap_facets(self):
        rows = {row["requirement_id"]: row for row in self.rows}
        self.assertEqual("TBD (RGAP-PH03-004)", rows["SREQ-PH03-LDG-003"]["use_case_id"])
        self.assertEqual("TBD (RGAP-PH03-004)", rows["SREQ-PH03-LDG-004"]["use_case_id"])

        document = (SCRIPT.parents[2] / rows["SREQ-PH03-LDG-003"]["document_path"]).read_text(encoding="utf-8")
        tables = validator._tables_in_section(document, "## 4. Acceptance criteria")
        table = validator._table_by_header(
            tables,
            (
                "Acceptance criterion", "Proves", "Criterion", "API/event/UI contract reference",
                "Scope/data/state/container reference", "Source/evidence",
            ),
        )
        criteria = {row[0]: row for row in table[1:] if row[0].startswith("AC-")}
        self.assertIn("RGAP-PH03-010", criteria["AC-PH03-LDG-003-01"][3])
        self.assertNotIn("RGAP-PH03-004", criteria["AC-PH03-LDG-003-01"][3])
        self.assertIn("RGAP-PH01-007", criteria["AC-PH03-LDG-004-01"][3])
        self.assertIn("RGAP-PH03-004", rows["REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY"]["use_case_id"])

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

    def test_strict_ready_summary_separates_overlapping_predicates_from_unique_rows(self):
        rows = [
            {
                "requirement_id": "REQ-PH01-TEST",
                "level": "main",
                "status": "DRAFT",
                "use_case_id": "TBD (RGAP-PH01-001)",
                "open_decisions": "ADR-001-GATE, ODEC-001",
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
                "requirement_id": "SREQ-PH01-TEST-002",
                "level": "sub",
                "status": "RETIRED",
                "use_case_id": "TBD (RGAP-PH01-001)",
                "open_decisions": "ADR-001-GATE",
                "verification_refs": "TEST (planned): retired test",
            },
        ]

        summary = validator.summarize_strict_ready(rows)

        self.assertEqual(2, summary["active_rows"])
        self.assertEqual(2, summary["unique_affected_rows"])
        self.assertEqual(8, summary["predicate_occurrences"])
        self.assertEqual({"main": 1, "sub": 1, "other": 0}, summary["active_rows_by_level"])
        self.assertEqual(2, summary["distinct_decision_refs"])
        self.assertEqual(3, summary["decision_reference_pairs"])
        self.assertEqual(1, len(summary["use_case_gap_ids"]))
        self.assertEqual(2, summary["use_case_gap_pairs"])
        self.assertEqual(1, summary["distinct_verification_refs"])

    def test_rgaps_mentioned_in_use_case_cells_are_not_all_strict_ready_blocker_roots(self):
        active_rows = [row for row in self.rows if row.get("status", "").strip() != "RETIRED"]
        all_mentioned_roots = {
            gap_id
            for row in active_rows
            for gap_id in validator.GAP_RE.findall(row.get("use_case_id", ""))
        }
        summary = validator.summarize_strict_ready(active_rows)
        blocker_roots = set(summary["use_case_gap_ids"])

        self.assertEqual(12, len(all_mentioned_roots))
        self.assertEqual(11, len(blocker_roots))
        self.assertEqual({"RGAP-PH02-003"}, all_mentioned_roots - blocker_roots)
        self.assertEqual(165, summary["use_case_gap_pairs"])

        scoped_function_rows = [
            row for row in active_rows if "RGAP-PH02-003" in row.get("use_case_id", "")
        ]
        self.assertEqual(7, len(scoped_function_rows))
        for row in scoped_function_rows:
            with self.subTest(requirement_id=row["requirement_id"]):
                self.assertIn("FN-ORD-CHECKOUT", row["use_case_id"])
                findings = [category for category, _message in validator.strict_ready_findings(row)]
                self.assertNotIn("use_case", findings)

    def test_none_recorded_is_not_an_open_decision(self):
        findings = validator.strict_ready_findings({
            "requirement_id": "SREQ-PH01-TEST-001",
            "status": "DRAFT",
            "open_decisions": "none recorded",
        })

        self.assertNotIn("decision", [category for category, _message in findings])

    def test_summary_counts_unique_ids_by_level_even_with_structural_duplicates(self):
        rows = [
            {"requirement_id": "REQ-TEST-001", "level": "main", "status": "DRAFT"},
            {"requirement_id": "REQ-TEST-001", "level": "main", "status": "DRAFT"},
            {"requirement_id": "", "level": "sub", "status": "DRAFT"},
            {"requirement_id": "REQ-TEST-002", "level": "main", "status": "DRAFT"},
            {"requirement_id": "REQ-TEST-002", "level": "sub", "status": "DRAFT"},
        ]

        summary = validator.summarize_strict_ready(rows)

        self.assertEqual(2, summary["active_rows"])
        self.assertEqual({"main": 1, "sub": 0, "other": 1}, summary["active_rows_by_level"])
        self.assertEqual(
            {"main": 1, "sub": 0, "other": 1},
            summary["category_level_counts"]["status"],
        )

    def test_cli_summary_is_opt_in_and_preserves_failure_status(self):
        command = [sys.executable, str(SCRIPT), "--check", "--strict-ready"]
        detailed = subprocess.run(command, cwd=SCRIPT.parents[2], capture_output=True, text=True, check=False)
        summary = subprocess.run(command + ["--summary"], cwd=SCRIPT.parents[2], capture_output=True, text=True, check=False)

        self.assertEqual(1, detailed.returncode)
        self.assertTrue(detailed.stdout.startswith("Strict-ready count:"))
        self.assertIn("ERROR:", detailed.stdout)
        self.assertNotIn("Strict-ready summary", detailed.stdout)
        expected_failure_summary = "835 strict-ready predicate findings across 268 unique active requirement IDs"
        self.assertIn(expected_failure_summary, detailed.stdout)
        self.assertIn("categories overlap; not a count of unique upstream issues", detailed.stdout)
        self.assertIn("additional validation errors=0; total errors=835", detailed.stdout)
        self.assertEqual(1, summary.returncode)
        self.assertIn("Strict-ready summary", summary.stdout)
        self.assertNotIn("ERROR:", summary.stdout)
        self.assertIn(expected_failure_summary, summary.stdout)
        self.assertIn("additional validation errors=0; total errors=835", summary.stdout)

    def test_current_readiness_report_matches_cycle21_counts_and_preserves_history(self):
        summary = validator.summarize_strict_ready(self.rows)
        active_counts = {
            category: sum(level_counts.values())
            for category, level_counts in summary["category_level_counts"].items()
        }
        report_path = SCRIPT.parents[1] / "validation" / "requirements-coverage-matrix.md"
        report = report_path.read_text(encoding="utf-8")
        readiness_report = (SCRIPT.parents[1] / "validation" / "requirements-readiness-report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Historical Cycle 11 strict-ready reconciliation", readiness_report)
        self.assertIn("historical strict-ready total was **871 predicate findings", readiness_report)
        self.assertNotIn("Current strict-ready is **871", readiness_report)
        heading = "## Current multi-path/readiness reconciliation — Cycle 21"
        self.assertIn(heading, report)
        current_section = report.split(heading, 1)[1].split("\n## ", 1)[0]
        self.assertIn("## Historical strict-ready reconciliation (cycle 17 source baseline)", report)
        self.assertIn(
            f"Active strict-ready is **FAIL, {summary['predicate_occurrences']} overlapping predicate findings "
            f"across {summary['unique_affected_rows']} unique active rows**",
            current_section,
        )
        self.assertIn(
            f"status={active_counts['status']}, use_case={active_counts['use_case']}, "
            f"decision={active_counts['decision']}, verification={active_counts['verification']}",
            current_section,
        )
        self.assertIn("41 `RUNTIME_SELECTABLE`", current_section)
        self.assertIn("0 `IMPLEMENTED_MULTI_PATH`", current_section)
        self.assertIn("0 `DESIGN_REVIEW_REQUIRED`", current_section)
        self.assertIn("All 41 design-selectable scopes have complete selector contracts", current_section)
        self.assertIn("103 source-supported selectable path entries", current_section)
        self.assertIn("12 RGAP IDs are mentioned in active use-case fields, but 11 roots produce unresolved use-case blockers", current_section)
        self.assertIn("12/12 linked rows", current_section)
        self.assertIn("No requirement, decision, approval, or implementation status was changed", current_section)

        release_audit_path = SCRIPT.parents[1] / "validation" / "release-status-audit.md"
        release_audit = release_audit_path.read_text(encoding="utf-8")
        self.assertIn("835 overlapping predicate findings across 268 unique active requirement rows", release_audit)
        self.assertNotIn("871 active blocker occurrences", release_audit)

    def test_diagnostic_indexes_preserve_historical_and_validate_current_source(self):
        checker = SCRIPT.parents[1] / "validation" / "validate_strict_ready_diagnostic_indexes.py"
        result = subprocess.run(
            [sys.executable, str(checker)],
            cwd=SCRIPT.parents[2],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: historical Cycle 07/08 indexes retain their recorded source snapshot", result.stdout)
        self.assertIn("PASS: historical Cycle 13 indexes retain their recorded 6d0d372 source snapshot", result.stdout)
        self.assertIn("PASS: immutable Cycle 15 indexes match their recorded bb9a3e1 source snapshot", result.stdout)
        self.assertIn("PASS: immutable Cycle 16 indexes match their recorded f56df97 source snapshot", result.stdout)
        self.assertIn("PASS: historical Cycle 17 indexes match the e1afb36 source snapshot", result.stdout)
        self.assertIn("PASS: current Cycle 18 indexes match the live structurally valid source inputs", result.stdout)
        self.assertIn("predicate_findings=845", result.stdout)
        self.assertIn("predicate_findings=840", result.stdout)
        self.assertIn("predicate_findings=835", result.stdout)
        self.assertIn(
            "source_inputs_sha256=c556587077de798cd764092f3a56361a73b19beda7c975ca7e7dff6e9a2f7118",
            result.stdout,
        )
        self.assertIn("actual_input_snapshot=e1afb3623aa07fd47b3d609f7b3e67bdcf6ffead", result.stdout)
        self.assertIn("c081c2e85a288a6b365b83a5bd46311613fc84cacb209e5f8575091127f37c7f", result.stdout)

    def test_retired_rows_remain_structural_but_do_not_block_active_strict_ready(self):
        errors = self.validate_copy(strict_ready=True)
        retired_ids = {
            row["requirement_id"] for row in self.rows if row["status"] == "RETIRED"
        }
        for requirement_id in retired_ids:
            self.assertFalse(any(requirement_id in error for error in errors))
        self.assertTrue(any("SREQ-PH01-INST-001" in error for error in errors))

    def test_unregistered_retirement_cannot_bypass_strict_ready(self):
        def change(rows):
            self.find(rows, "SREQ-PH01-INST-001")["status"] = "RETIRED"

        errors = self.validate_copy(change, strict_ready=True)
        self.assertTrue(any("RETIRED status requires an approved historical retirement record" in error for error in errors))

    def test_retirement_evidence_reference_requires_existing_anchor(self):
        self.assertIsNone(validator.validate_evidence_ref(
            "acc-architecture/validation/atomicity-review-report.md#cycle-10-classification-register"
        ))
        self.assertIn("target does not exist", validator.validate_evidence_ref(
            "acc-architecture/validation/does-not-exist.md#evidence"
        ))
        self.assertIn("anchor does not exist", validator.validate_evidence_ref(
            "acc-architecture/validation/atomicity-review-report.md#missing-anchor"
        ))

    def test_retirement_successors_reject_duplicate_self_missing_and_retired_ids(self):
        cases = (
            (lambda record: record.update(successor_ids=["SREQ-PH01-INST-009", "SREQ-PH01-INST-009"]), "duplicate successor_id"),
            (lambda record: record.update(successor_ids=["SREQ-PH01-INST-005"]), "cannot be its own successor"),
            (lambda record: record.update(successor_ids=["SREQ-PH99-OTHER-001"]), "is not an existing requirement row"),
            (lambda record: record.update(successor_ids=["SREQ-PH01-AUTH-001"]), "successor SREQ-PH01-AUTH-001 is also RETIRED"),
        )
        original = json.loads(validator.RETIREMENT_REGISTRY.read_text(encoding="utf-8"))
        for mutate, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temporary:
                data = copy.deepcopy(original)
                mutate(data["records"][0])
                retirement_path = Path(temporary) / "retired-requirements.json"
                retirement_path.write_text(json.dumps(data), encoding="utf-8")
                with patch.object(validator, "RETIREMENT_REGISTRY", retirement_path):
                    errors = validator.validate(copy.deepcopy(self.rows), list(self.load_errors), require_rows=True)
                self.assertTrue(any(expected in error for error in errors), "\n".join(errors))

    def test_parent_link_must_stay_within_phase_and_requirement_document(self):
        def cross_phase(rows):
            self.find(rows, "SREQ-PH01-INST-001")["parent_requirement_id"] = "REQ-PH02-LISTING-INGESTION"

        phase_errors = self.validate_copy(cross_phase)
        self.assertTrue(any("parent REQ-PH02-LISTING-INGESTION belongs to a different phase" in error for error in phase_errors))

        def cross_document(rows):
            self.find(rows, "SREQ-PH01-INST-001")["parent_requirement_id"] = "REQ-PH01-IDENTITY-AND-TRUST"

        document_errors = self.validate_copy(cross_document)
        self.assertTrue(any("parent REQ-PH01-IDENTITY-AND-TRUST belongs to a different requirement document" in error for error in document_errors))

    def test_duplicate_approval_evidence_records_fail_instead_of_last_record_wins(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            approvers_path = root / "authorized-approvers.json"
            approvals_path = root / "requirement-approval-records.json"
            verifications_path = root / "requirement-verification-records.json"
            approvers_path.write_text(json.dumps({"approvers": [
                {"identity": "owner@example.org", "active": True},
                {"identity": "OWNER@example.org", "active": False},
            ]}), encoding="utf-8")
            approvals_path.write_text(json.dumps({"records": [
                {"requirement_id": "SREQ-PH01-INST-001"},
                {"requirement_id": "SREQ-PH01-INST-001"},
            ]}), encoding="utf-8")
            verifications_path.write_text(json.dumps({"records": [
                {"requirement_id": "SREQ-PH01-INST-001"},
                {"requirement_id": "SREQ-PH01-INST-001"},
            ]}), encoding="utf-8")
            with (
                patch.object(validator, "APPROVER_REGISTRY", approvers_path),
                patch.object(validator, "APPROVAL_RECORDS", approvals_path),
                patch.object(validator, "VERIFICATION_RECORDS", verifications_path),
            ):
                errors = validator.validate(copy.deepcopy(self.rows), list(self.load_errors), require_rows=True)

        self.assertTrue(any("authorized-approvers.json contains duplicate identity" in error for error in errors))
        self.assertTrue(any("requirement-approval-records.json contains duplicate requirement_id" in error for error in errors))
        self.assertTrue(any("requirement-verification-records.json contains duplicate requirement_id" in error for error in errors))

    def test_authorized_approver_lookup_uses_normalized_identity(self):
        row = copy.deepcopy(self.find(self.rows, "SREQ-PH01-INST-001"))
        row["status"] = "ACCEPTED"
        identity = "owner@example.org"
        content_hash = validator.requirement_content_hash(row)
        errors = []
        approvers = validator._index_unique_records(
            [{"identity": " Owner@Example.org ", "active": True}],
            "identity",
            "synthetic authorized-approvers.json",
            errors,
        )
        approval = {
            "approver_identity": identity,
            "authority_role": "Synthetic test role",
            "decision_scope": "Synthetic validator test only",
            "approval_reference": "acc-architecture/validation/requirements-readiness-report.md",
            "approved_at": "2026-11-22T09:30:00+03:00",
            "approved_baseline": content_hash,
            "content_hash": content_hash,
        }
        verification = {
            "state": "EXECUTED",
            "result": "PASS",
            "subject_hash": content_hash,
            "executed_at": "2026-11-22T09:30:00+03:00",
            "reviewer_identity": "reviewer@example.org",
            "artifact_ref": "acc-architecture/validation/requirements-readiness-report.md",
        }

        validator._validate_acceptance_claim(
            row,
            approvers,
            {row["requirement_id"]: approval},
            {row["requirement_id"]: verification},
            errors,
        )

        self.assertEqual([], errors)
        self.assertIn("owner@example.org", approvers)

        verification["reviewer_identity"] = "OWNER@EXAMPLE.ORG"
        independent_review_errors = []
        validator._validate_acceptance_claim(
            row,
            approvers,
            {row["requirement_id"]: approval},
            {row["requirement_id"]: verification},
            independent_review_errors,
        )
        self.assertTrue(any("requires an independent reviewer_identity" in error
                            for error in independent_review_errors))

    def test_accepted_status_requires_authority_and_execution_records(self):
        def change(rows):
            self.find(rows, "SREQ-PH01-INST-001")["status"] = "ACCEPTED"

        errors = self.validate_copy(change)
        self.assertTrue(any("ACCEPTED claim requires a matching requirement-approval-records.json entry" in error for error in errors))

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
