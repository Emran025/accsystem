"""Regression tests for multi-path design, selector contracts, and independent gates."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
VALIDATION_DIR = TEST_DIR.parents[1] / "validation"
sys.path.insert(0, str(VALIDATION_DIR))
import validate_multi_path_readiness as multipath  # noqa: E402
import multi_path_selector_reference as selector  # noqa: E402

REGISTER_PATH = VALIDATION_DIR / "multi-path-readiness-register.json"


def find_scope(data: dict, reference: str, scope_id: str | None = None) -> dict:
    record = next(item for item in data["records"] if item["reference"] == reference)
    return next(
        scope for scope in record["multi_path_scopes"]
        if scope_id is None or scope["scope_id"] == scope_id
    )


def gate_refs(scope: dict) -> dict[str, str]:
    return {gate: f"test-evidence:{index}" for index, gate in enumerate(scope["separate_gates"], 1)}


def eligibility_refs(path_ids: set[str]) -> dict[str, str]:
    return {path_id: f"test-eligibility:{index}" for index, path_id in enumerate(sorted(path_ids), 1)}


class MultiPathReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
        cls.rows = multipath.active_rows()

    def mutated_scope(self):
        data = copy.deepcopy(self.data)
        record = next(item for item in data["records"] if item["multi_path_scopes"])
        return data, record, record["multi_path_scopes"][0]

    def test_current_register_passes_and_reports_design_not_implementation(self):
        errors, counts = multipath.validate_register(copy.deepcopy(self.data), copy.deepcopy(self.rows))
        self.assertEqual([], errors)
        self.assertEqual(61, counts["distinct_open_reference_roots"])
        self.assertEqual(37, counts["references_with_multi_path_scopes"])
        self.assertEqual(41, counts["multi_path_scope_count"])
        self.assertEqual(41, counts["runtime_selectable_scope_count"])
        self.assertEqual(0, counts["implemented_multi_path_scope_count"])
        self.assertEqual(0, counts["design_review_required_scope_count"])
        self.assertEqual(0, counts["review_link_discrepancy_count"])
        self.assertEqual(41, counts["complete_selector_contract_count"])
        self.assertEqual(103, counts["active_selectable_path_count"])
        self.assertEqual(1, counts["deferred_path_count"])
        self.assertEqual(1, counts["orthogonal_configuration_dimension_count"])
        self.assertEqual(1, counts["excluded_source_option_count"])

    def test_strict_ready_counts_remain_independent_of_design_validator(self):
        sys.path.insert(0, str(TEST_DIR.parents[0]))
        import validate_requirements as requirements  # noqa: E402

        before = requirements.summarize_strict_ready(self.rows)
        errors, _counts = multipath.validate_register(copy.deepcopy(self.data), copy.deepcopy(self.rows))
        after = requirements.summarize_strict_ready(self.rows)
        self.assertEqual([], errors)
        self.assertEqual(before, after)
        self.assertEqual(835, after["predicate_occurrences"])
        self.assertEqual(268, after["unique_affected_rows"])

    def test_design_check_fails_if_required_fields_are_missing(self):
        mutations = (
            ("shared_contract", ""),
            ("selection_context", ""),
            ("source_acceptance_criteria", []),
            ("failure_recovery_audit_security", []),
            ("separate_gates", []),
            ("global_invariant_refs", []),
            ("selection_contract", {}),
        )
        for field, empty_value in mutations:
            with self.subTest(field=field):
                data, _record, scope = self.mutated_scope()
                scope[field] = empty_value
                errors, _counts = multipath.validate_register(data, copy.deepcopy(self.rows))
                self.assertTrue(any(field.replace("_", " ") in error or field in error for error in errors), errors)

    def test_selector_contract_must_be_complete_and_match_every_path(self):
        data, _record, scope = self.mutated_scope()
        scope["selection_contract"]["selectable_path_ids"] = scope["selection_contract"]["selectable_path_ids"][:-1]
        errors, _counts = multipath.validate_register(data, copy.deepcopy(self.rows))
        self.assertTrue(any("allowlist must exactly preserve" in error for error in errors), errors)

        data, _record, scope = self.mutated_scope()
        scope["selection_contract"]["design_status"] = "INCOMPLETE"
        errors, _counts = multipath.validate_register(data, copy.deepcopy(self.rows))
        self.assertTrue(any("RUNTIME_SELECTABLE requires a complete" in error for error in errors), errors)

        data, _record, scope = self.mutated_scope()
        scope["selection_contract"]["reference_selector_inputs"]["required"] = []
        errors, _counts = multipath.validate_register(data, copy.deepcopy(self.rows))
        self.assertTrue(any("reference selector inputs must define" in error for error in errors), errors)

    def test_acceptance_criteria_are_mapped_to_applicable_paths_not_blindly_copied(self):
        scope = find_scope(self.data, "ADR-015-GATE", "adr-015-scope-01")
        outbound = next(path for path in scope["paths"] if path["path_id"].endswith("path-01"))
        inbound = next(path for path in scope["paths"] if path["path_id"].endswith("path-04"))
        outbound_ids = {item["criterion"] for item in outbound["acceptance_criteria"]}
        inbound_ids = {item["criterion"] for item in inbound["acceptance_criteria"]}
        self.assertTrue(any(item.startswith("AC-PH01-CONN-002-01:") for item in outbound_ids))
        self.assertFalse(any(item.startswith("AC-PH01-CONN-002-02:") for item in outbound_ids))
        self.assertTrue(any(item.startswith("AC-PH01-CONN-002-02:") for item in inbound_ids))
        self.assertFalse(any(item.startswith("AC-PH01-CONN-002-01:") for item in inbound_ids))
        scenario = scope["cross_path_verification_scenarios"][0]
        self.assertIn("both connectivity modes", scenario["criterion"])
        self.assertEqual("PLANNED_OR_SOURCE_DEFINED_NOT_EXECUTED", scenario["execution_status"])

        data = copy.deepcopy(self.data)
        mutated = find_scope(data, "ADR-015-GATE", "adr-015-scope-01")
        mapped = next(item for item in mutated["acceptance_criteria_applicability"] if item["criterion"].startswith("AC-PH01-CONN-002-02:"))
        mapped["applies_to_path_ids"] = [mutated["paths"][0]["path_id"]]
        errors, _counts = multipath.validate_register(data, copy.deepcopy(self.rows))
        self.assertTrue(any("path acceptance criteria must exactly match" in error for error in errors), errors)

    def test_odec001_keeps_connectivity_separate_from_hosting_and_packaging(self):
        scope = find_scope(self.data, "ODEC-001")
        self.assertEqual(2, len(scope["paths"]))
        self.assertEqual(2, len(scope["selection_contract"]["selectable_path_ids"]))
        orthogonal = scope["orthogonal_configuration_dimensions"][0]
        self.assertEqual("odec-001-scope-01-path-03", orthogonal["former_path_id"])
        self.assertFalse(orthogonal["selectable_by_connectivity_selector"])
        self.assertEqual("NOT_DEFINED_BY_SOURCE", orthogonal["deployment_acceptance_status"])
        self.assertIn("on-premises", orthogonal["source_description"])
        self.assertIn("Backend and Frontend", orthogonal["source_description"])
        outbound = next(path for path in scope["paths"] if path["path_id"].endswith("path-01"))
        inbound = next(path for path in scope["paths"] if path["path_id"].endswith("path-02"))
        outbound_criteria = {item["criterion"] for item in outbound["acceptance_criteria"]}
        inbound_criteria = {item["criterion"] for item in inbound["acceptance_criteria"]}
        self.assertTrue(any(item.startswith("AC-PH01-CONN-002-01:") for item in outbound_criteria))
        self.assertFalse(any(item.startswith("AC-PH01-CONN-002-01:") for item in inbound_criteria))
        self.assertTrue(any(item.startswith("AC-PH01-CONN-002-02:") for item in inbound_criteria))
        self.assertFalse(any(item.startswith("AC-PH01-CONN-002-02:") for item in outbound_criteria))
        self.assertEqual(1, len(scope["cross_path_verification_scenarios"]))

    def test_financial_commitment_remains_deferred_and_not_selectable(self):
        scope = find_scope(self.data, "RP-04", "rp-04-scope-02")
        deferred = scope["deferred_paths"][0]
        self.assertIn("FinancialCommitment", deferred["source_description"])
        self.assertEqual("DEFERRED_NOT_SELECTABLE", deferred["selection_status"])
        self.assertNotIn(deferred["path_id"], scope["selection_contract"]["selectable_path_ids"])
        self.assertIn("future ADR", deferred["deferral_reason"])

    def test_cycle23_lic001_acceptance_criteria_follow_the_validation_path(self):
        scope = find_scope(self.data, "LIC-001", "lic-001-scope-01")
        paths = {path["path_id"]: path for path in scope["paths"]}
        offline_id = "lic-001-scope-01-path-01"
        online_id = "lic-001-scope-01-path-02"
        self.assertEqual({offline_id, online_id}, set(paths))

        mappings = scope["acceptance_criteria_applicability"]

        def one_mapping(prefix):
            matches = [item for item in mappings if item["criterion"].startswith(prefix)]
            self.assertEqual(1, len(matches), prefix)
            return matches[0]

        offline_only = (
            "AC-PH01-LICV-003-01:",
            "AC-PH01-LICV-004-01:",
            "AC-PH01-LICV-004-02:",
            "CMP-CON-LICENSECHECK offline verification:",
        )
        offline_criteria = {item["criterion"] for item in paths[offline_id]["acceptance_criteria"]}
        online_criteria = {item["criterion"] for item in paths[online_id]["acceptance_criteria"]}
        for prefix in offline_only:
            with self.subTest(prefix=prefix):
                item = one_mapping(prefix)
                self.assertEqual("PATH_SPECIFIC", item["classification"])
                self.assertEqual([offline_id], item["applies_to_path_ids"])
                self.assertIn(item["criterion"], offline_criteria)
                self.assertNotIn(item["criterion"], online_criteria)

        for prefix in ("AC-PH01-LICV-005-01:", "FN-LIC-VALIDATE Q1/Q2:"):
            with self.subTest(prefix=prefix):
                item = one_mapping(prefix)
                self.assertEqual("SHARED_CONTRACT", item["classification"])
                self.assertEqual([offline_id, online_id], item["applies_to_path_ids"])
                self.assertIn(item["criterion"], offline_criteria)
                self.assertIn(item["criterion"], online_criteria)

        fallback = one_mapping("FN-LIC-VALIDATE fallback behavior:")
        self.assertEqual("CROSS_PATH_SCENARIO", fallback["classification"])
        self.assertEqual([], fallback["applies_to_path_ids"])
        self.assertEqual(
            {fallback["criterion"]},
            {item["criterion"] for item in scope["cross_path_verification_scenarios"]},
        )
        self.assertEqual("PLANNED_OR_SOURCE_DEFINED_NOT_EXECUTED", fallback["execution_status"])

        issuance_prefix = "AC-PH01-LICV-005-02:"
        self.assertFalse(any(item.startswith(issuance_prefix) for item in scope["source_acceptance_criteria"]))
        self.assertFalse(any(item["criterion"].startswith(issuance_prefix) for item in mappings))
        self.assertFalse(any(item.startswith(issuance_prefix) for item in offline_criteria | online_criteria))
        requirement = (TEST_DIR.parent / "phase-01-platform-foundation" / "REQ-PH01-LICENSE-VALIDATION.md").read_text(encoding="utf-8")
        self.assertIn("AC-PH01-LICV-005-02", requirement)
        self.assertEqual("RUNTIME_SELECTABLE", scope["design_status"])
        self.assertEqual("NOT_EVIDENCED", scope["runtime_implementation_status"])
        self.assertTrue(all(item["execution_status"] == "PLANNED_OR_SOURCE_DEFINED_NOT_EXECUTED" for item in mappings))

    def test_rp16_all_links_are_reconciled_and_auth_paths_remain_separately_gated(self):
        record = next(item for item in self.data["records"] if item["reference"] == "RP-16")
        scope = record["multi_path_scopes"][0]
        reconciliation = record["source_reconciliation"]
        self.assertEqual(12, len(record["linked_requirement_ids"]))
        self.assertEqual({"DRAFT"}, set(record["linked_requirement_statuses"].values()))
        self.assertEqual(3, len(record["initial_review_reported_impact_ids"]))
        self.assertEqual(12, len(record["review_reported_impact_ids"]))
        self.assertEqual([], record["unreviewed_linked_requirement_ids"])
        self.assertEqual("RECONCILED_ALL_LINKED_ROWS", reconciliation["status"])
        self.assertEqual(12, len(reconciliation["reviewed_linked_requirement_ids"]))
        self.assertEqual({"SREQ-PH01-CONN-003", "SREQ-PH01-INST-010"}, set(reconciliation["direct_relevance_ids"]))
        self.assertEqual(10, len(reconciliation["partial_relevance_ids"]))
        self.assertEqual([], reconciliation["unsupported_ids"])
        self.assertIn("SREQ-PH01-CONN-003", record["linked_requirement_ids"])
        self.assertEqual({"SREQ-PH01-CONN-003", "SREQ-PH01-CONN-004"}, set(scope["requirement_ids"]))
        self.assertEqual("RUNTIME_SELECTABLE", scope["design_status"])
        self.assertEqual("COMPLETE", scope["selection_contract"]["design_status"])
        self.assertEqual("NOT_EVIDENCED", scope["runtime_implementation_status"])
        self.assertTrue(any("owner/security approval" in gate.lower() for gate in scope["separate_gates"]))
        self.assertTrue(any("OpenAPI/AsyncAPI" in gate for gate in scope["separate_gates"]))
        excluded = scope["excluded_source_options"][0]
        self.assertIn("API keys", excluded["source_description"])
        self.assertNotIn(excluded["former_path_id"], scope["selection_contract"]["selectable_path_ids"])

    def test_implemented_status_requires_executed_evidence(self):
        data, _record, scope = self.mutated_scope()
        scope["design_status"] = "IMPLEMENTED_MULTI_PATH"
        errors, _counts = multipath.validate_register(data, copy.deepcopy(self.rows))
        self.assertTrue(any("requires linked implementation evidence" in error for error in errors), errors)

    def test_reference_selector_fails_closed_for_review_blockers_and_missing_gates(self):
        rp16 = copy.deepcopy(find_scope(self.data, "RP-16"))
        rp16_paths = set(rp16["selection_contract"]["selectable_path_ids"])
        self.assertEqual("NONE", rp16["selection_contract"]["source_default"]["kind"])
        blocked = selector.resolve_path(
            rp16,
            context_level="organization",
            context_id="test-institution",
            eligible_path_ids=rp16_paths,
            eligibility_evidence_refs=eligibility_refs(rp16_paths),
            gate_evidence_refs=gate_refs(rp16),
            resolution_evidence_ref="test-resolution",
        )
        self.assertEqual("BLOCKED", blocked["status"])
        for path_id in sorted(rp16_paths):
            selected = selector.resolve_path(
                rp16,
                context_level="organization",
                context_id="test-institution",
                eligible_path_ids={path_id},
                eligibility_evidence_refs=eligibility_refs({path_id}),
                gate_evidence_refs=gate_refs(rp16),
                resolution_evidence_ref="test-resolution",
                requested_path_id=path_id,
            )
            self.assertEqual("SELECTED", selected["status"])
            self.assertEqual(path_id, selected["selected_path_id"])

        missing_rp16_gates = gate_refs(rp16)
        missing_rp16_gates.pop(next(iter(missing_rp16_gates)))
        blocked_missing_rp16_gate = selector.resolve_path(
            rp16,
            context_level="organization",
            context_id="test-institution",
            eligible_path_ids=rp16_paths,
            eligibility_evidence_refs=eligibility_refs(rp16_paths),
            gate_evidence_refs=missing_rp16_gates,
            resolution_evidence_ref="test-resolution",
            requested_path_id=sorted(rp16_paths)[0],
        )
        self.assertEqual("BLOCKED", blocked_missing_rp16_gate["status"])

        scope = copy.deepcopy(find_scope(self.data, "ADR-015-GATE", "adr-015-scope-02"))
        scope_paths = set(scope["selection_contract"]["selectable_path_ids"])
        missing_gate_refs = gate_refs(scope)
        missing_gate_refs.pop(next(iter(missing_gate_refs)))
        blocked = selector.resolve_path(
            scope,
            context_level="organization",
            context_id="test-institution",
            eligible_path_ids=scope_paths,
            eligibility_evidence_refs=eligibility_refs(scope_paths),
            gate_evidence_refs=missing_gate_refs,
            resolution_evidence_ref="test-resolution",
            requested_path_id=next(iter(scope_paths)),
        )
        self.assertEqual("BLOCKED", blocked["status"])

    def test_reference_selector_requires_explicit_selection_for_configured_paths(self):
        scope = copy.deepcopy(find_scope(self.data, "ADR-015-GATE", "adr-015-scope-02"))
        allowed = set(scope["selection_contract"]["selectable_path_ids"])
        blocked = selector.resolve_path(
            scope,
            context_level="organization",
            context_id="institution-1",
            eligible_path_ids=allowed,
            eligibility_evidence_refs=eligibility_refs(allowed),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="policy-review:42",
        )
        self.assertEqual("BLOCKED", blocked["status"])
        selected = selector.resolve_path(
            scope,
            context_level="organization",
            context_id="institution-1",
            eligible_path_ids=allowed,
            eligibility_evidence_refs=eligibility_refs(allowed),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="policy-review:42",
            requested_path_id=next(iter(allowed)),
        )
        self.assertEqual("SELECTED", selected["status"])
        self.assertIn(selected["selected_path_id"], allowed)
        self.assertEqual(len(scope["separate_gates"]), len(selected["audit"]["gate_evidence_refs"]))
        self.assertEqual(len(allowed), len(selected["audit"]["eligibility_evidence_refs"]))

    def test_reference_selector_never_falls_back_from_an_ineligible_choice(self):
        scope = copy.deepcopy(find_scope(self.data, "ADR-015-GATE", "adr-015-scope-02"))
        allowed = scope["selection_contract"]["selectable_path_ids"]
        blocked = selector.resolve_path(
            scope,
            context_level="organization",
            context_id="institution-1",
            eligible_path_ids={allowed[1]},
            eligibility_evidence_refs=eligibility_refs({allowed[1]}),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="policy-review:43",
            requested_path_id=allowed[0],
        )
        self.assertEqual("BLOCKED", blocked["status"])
        self.assertIn("not eligible", blocked["reason"])

    def test_source_default_requires_independent_default_approval(self):
        scope = copy.deepcopy(find_scope(self.data, "RP-01"))
        allowed = set(scope["selection_contract"]["selectable_path_ids"])
        args = dict(
            context_level="organization",
            context_id="institution-1",
            eligible_path_ids=allowed,
            eligibility_evidence_refs=eligibility_refs(allowed),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="onboarding:contract-review",
        )
        blocked = selector.resolve_path(scope, **args)
        self.assertEqual("BLOCKED", blocked["status"])
        selected = selector.resolve_path(scope, **args, source_default_approval_ref="approval-record:external")
        self.assertEqual("SELECTED", selected["status"])
        self.assertEqual(scope["selection_contract"]["source_default"]["path_id"], selected["selected_path_id"])

    def test_partial_or_proposed_direction_default_does_not_auto_select(self):
        scope = copy.deepcopy(find_scope(self.data, "ADR-015-GATE", "adr-015-scope-01"))
        allowed = set(scope["selection_contract"]["selectable_path_ids"])
        blocked = selector.resolve_path(
            scope,
            context_level="organization",
            context_id="institution-1",
            eligible_path_ids=allowed,
            eligibility_evidence_refs=eligibility_refs(allowed),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="onboarding:connectivity-review",
        )
        self.assertEqual("BLOCKED", blocked["status"])

    def test_condition_based_selector_needs_one_unambiguous_source_eligible_path(self):
        scope = copy.deepcopy(find_scope(self.data, "LIC-001"))
        allowed = scope["selection_contract"]["selectable_path_ids"]
        one = selector.resolve_path(
            scope,
            context_level="operation",
            context_id="license-check-1",
            eligible_path_ids={allowed[0]},
            eligibility_evidence_refs=eligibility_refs({allowed[0]}),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="license-state-evidence:1",
        )
        self.assertEqual("SELECTED", one["status"])
        ambiguous = selector.resolve_path(
            scope,
            context_level="operation",
            context_id="license-check-2",
            eligible_path_ids=set(allowed),
            eligibility_evidence_refs=eligibility_refs(set(allowed)),
            gate_evidence_refs=gate_refs(scope),
            resolution_evidence_ref="license-state-evidence:2",
        )
        self.assertEqual("BLOCKED", ambiguous["status"])

    def test_finance_and_security_evidence_gates_are_not_replaced_by_path_selection(self):
        record = next(item for item in self.data["records"] if item["reference"] == "ADR-016-GATE")
        settlement = next(scope for scope in record["multi_path_scopes"] if scope["scope_id"].endswith("scope-02"))
        gates = " ".join(settlement["separate_gates"]).lower()
        self.assertIn("finance", gates)
        self.assertIn("legal", gates)
        self.assertIn("approval", gates)
        invariant_ids = {item["id"] for item in self.data["global_invariants"]}
        self.assertIn("NFR-009", invariant_ids)
        self.assertIn("NFR-006 / CON-004", invariant_ids)
        self.assertIn("CON-005 / NFR-004", invariant_ids)
        errors, _counts = multipath.validate_register(copy.deepcopy(self.data), copy.deepcopy(self.rows))
        self.assertEqual([], errors)

    def test_cycle22_reviewed_scopes_preserve_exact_path_contract_and_fail_closed_evidence(self):
        expectations = (
            ("ADR-004-GATE", "adr-004-scope-01", ["adr-004-scope-01-path-01", "adr-004-scope-01-path-02", "adr-004-scope-01-path-03"], "operation", "NONE", None),
            ("ADR-008-GATE", "adr-008-scope-01", ["adr-008-scope-01-path-01", "adr-008-scope-01-path-02"], "workflow", "NONE", None),
            ("ADR-016-GATE", "adr-016-scope-01", [f"adr-016-scope-01-path-{i:02d}" for i in range(1, 6)], "transaction", "NONE", None),
            ("ADR-016-GATE", "adr-016-scope-02", [f"adr-016-scope-02-path-{i:02d}" for i in range(1, 5)], "organization", "NONE", None),
            ("ADR-017-GATE", "adr-017-scope-01", ["adr-017-scope-01-path-01", "adr-017-scope-01-path-02"], "transaction", "NONE", None),
            ("ADR-018-GATE", "adr-018-scope-01", ["adr-018-scope-01-path-01", "adr-018-scope-01-path-02"], "organization", "PATH", "adr-018-scope-01-path-01"),
            ("LIC-002", "lic-002-scope-01", ["lic-002-scope-01-path-01", "lic-002-scope-01-path-02", "lic-002-scope-01-path-03"], "operation", "NONE", None),
            ("IC-003", "ic-003-scope-01", ["ic-003-scope-01-path-01", "ic-003-scope-01-path-02"], "organization", "NONE", None),
            ("IC-006", "ic-006-scope-01", ["ic-006-scope-01-path-01", "ic-006-scope-01-path-02"], "organization", "PATH", "ic-006-scope-01-path-01"),
        )
        for reference, scope_id, expected_paths, level, default_kind, default_path in expectations:
            with self.subTest(reference=reference, scope_id=scope_id):
                scope = find_scope(self.data, reference, scope_id)
                contract = scope["selection_contract"]
                paths = set(expected_paths)
                self.assertEqual(expected_paths, [item["path_id"] for item in scope["paths"]])
                self.assertEqual(expected_paths, contract["selectable_path_ids"])
                self.assertEqual(level, contract["selection_level"])
                self.assertEqual(default_kind, contract["source_default"]["kind"])
                self.assertEqual(default_path, contract["source_default"].get("path_id"))
                self.assertEqual("RUNTIME_SELECTABLE", scope["design_status"])
                self.assertEqual("NOT_EVIDENCED", scope["runtime_implementation_status"])

                full_args = dict(
                    context_level=level,
                    context_id=f"cycle22:{scope_id}",
                    eligible_path_ids=paths,
                    eligibility_evidence_refs=eligibility_refs(paths),
                    gate_evidence_refs=gate_refs(scope),
                    resolution_evidence_ref="synthetic-review-fixture:selection",
                )
                for path_id in expected_paths:
                    selected = selector.resolve_path(scope, **full_args, requested_path_id=path_id)
                    self.assertEqual("SELECTED", selected["status"], selected)
                    self.assertEqual(path_id, selected["selected_path_id"])

                    missing_path_evidence = dict(full_args["eligibility_evidence_refs"])
                    missing_path_evidence.pop(path_id)
                    blocked_missing_path_evidence = selector.resolve_path(
                        scope,
                        **(full_args | {"eligibility_evidence_refs": missing_path_evidence}),
                        requested_path_id=path_id,
                    )
                    self.assertEqual("BLOCKED", blocked_missing_path_evidence["status"])

                    ineligible = paths - {path_id}
                    blocked_ineligible = selector.resolve_path(
                        scope,
                        **(full_args | {
                            "eligible_path_ids": ineligible,
                            "eligibility_evidence_refs": eligibility_refs(ineligible),
                        }),
                        requested_path_id=path_id,
                    )
                    self.assertEqual("BLOCKED", blocked_ineligible["status"])

                ambiguous = selector.resolve_path(scope, **full_args)
                self.assertEqual("BLOCKED", ambiguous["status"])
                self.assertIsNone(ambiguous["selected_path_id"])

                if default_path:
                    approved_default = selector.resolve_path(
                        scope, **full_args, source_default_approval_ref="synthetic-review-fixture:default-approval"
                    )
                    self.assertEqual("SELECTED", approved_default["status"])
                    self.assertEqual(default_path, approved_default["selected_path_id"])

                for gate in scope["separate_gates"]:
                    missing_gate_refs = gate_refs(scope)
                    missing_gate_refs.pop(gate)
                    blocked_missing_gate = selector.resolve_path(
                        scope,
                        **(full_args | {"gate_evidence_refs": missing_gate_refs}),
                        requested_path_id=expected_paths[0],
                    )
                    self.assertEqual("BLOCKED", blocked_missing_gate["status"], gate)

                blocked_without_resolution = selector.resolve_path(
                    scope, **(full_args | {"resolution_evidence_ref": ""}), requested_path_id=expected_paths[0]
                )
                self.assertEqual("BLOCKED", blocked_without_resolution["status"])

                wrong_context = selector.resolve_path(
                    scope, **(full_args | {"context_level": "deployment"}), requested_path_id=expected_paths[0]
                )
                self.assertEqual("BLOCKED", wrong_context["status"])

                if contract["resolution_mode"] == "CONDITION_BASED":
                    for path_id in expected_paths:
                        one_condition = selector.resolve_path(
                            scope,
                            **(full_args | {
                                "eligible_path_ids": {path_id},
                                "eligibility_evidence_refs": eligibility_refs({path_id}),
                            }),
                        )
                        self.assertEqual("SELECTED", one_condition["status"])
                        self.assertEqual(path_id, one_condition["selected_path_id"])

        errors, counts = multipath.validate_register(copy.deepcopy(self.data), copy.deepcopy(self.rows))
        self.assertEqual([], errors)
        self.assertEqual(0, counts["implemented_multi_path_scope_count"])


if __name__ == "__main__":
    unittest.main()
