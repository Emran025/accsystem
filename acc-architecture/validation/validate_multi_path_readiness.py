#!/usr/bin/env python3
"""Validate multi-path architecture design independently from strict-ready status."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent
REPO_ROOT = VALIDATION_DIR.parents[1]
ARCH_ROOT = REPO_ROOT / "acc-architecture"
REGISTER_PATH = VALIDATION_DIR / "multi-path-readiness-register.json"
REGISTRY_PATH = ARCH_ROOT / "execution-phases" / "requirements-registry.csv"
DECISIONS_PATH = ARCH_ROOT / "registry" / "decisions.json"
EXPECTED_BASELINE = "47b8b08b86676233be17063e4101d17d8b27bdfa"
EXPECTED_GLOBAL_INVARIANTS = {
    "CON-003 / NFR-003",
    "CON-005 / NFR-004",
    "NFR-009",
    "NFR-006 / CON-004",
    "CON-008",
    "SCOPE-001 / FR-002 / ADR ownership sources",
}
EXPECTED_SCOPE_COUNTS = {
    "active_registry_open_reference_count": 61,
    "registered_reference_count": 61,
    "structured_reviews_available": 60,
    "manual_source_reconciliations": 1,
    "references_with_multi_path_scopes": 37,
    "multi_path_scope_count": 41,
    "runtime_selectable_scope_count": 41,
    "implemented_multi_path_scope_count": 0,
    "design_review_required_scope_count": 0,
    "review_link_discrepancy_count": 0,
    "distinct_open_reference_roots": 61,
    "complete_selector_contract_count": 41,
    "active_selectable_path_count": 103,
    "deferred_path_count": 1,
    "orthogonal_configuration_dimension_count": 1,
    "excluded_source_option_count": 1,
}
SELECTION_LEVELS = {"organization", "workflow", "transaction", "operation", "interface", "deployment"}
RESOLUTION_MODES = {"APPROVED_CONFIGURATION", "POLICY_AND_CAPABILITY", "CONDITION_BASED", "EVIDENCE_DRIVEN_CONFIGURATION"}
ACCEPTANCE_CLASSIFICATIONS = {
    "SHARED_CONTRACT", "OUTBOUND_PATH_GROUP", "INBOUND_APPROVAL_GUARD", "PATH_SPECIFIC", "CROSS_PATH_SCENARIO"
}


def active_rows(path: Path = REGISTRY_PATH) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status", "").strip() != "RETIRED"]


def split_refs(value: str) -> set[str]:
    return {
        item.strip()
        for item in re.split(r"[,;]", value or "")
        if item.strip() and item.strip().lower() not in {"none recorded", "n/a", "—", "-"}
    }


def source_digest() -> str:
    digest = hashlib.sha256()
    for relative, path in (
        ("acc-architecture/execution-phases/requirements-registry.csv", REGISTRY_PATH),
        ("acc-architecture/registry/decisions.json", DECISIONS_PATH),
    ):
        content = path.read_bytes()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(content)).encode("ascii"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_repo_path(relative: str) -> Path | None:
    candidate = (REPO_ROOT / relative).resolve()
    try:
        candidate.relative_to(ARCH_ROOT.resolve())
    except ValueError:
        return None
    return candidate


def _check_selection_contract(scope: dict, record: dict, label: str, errors: list[str]) -> None:
    contract = scope.get("selection_contract")
    if not isinstance(contract, dict):
        errors.append(f"{label}: structured selection_contract is required")
        return
    paths = scope.get("paths", [])
    path_ids = [path.get("path_id", "") for path in paths]
    if len(path_ids) != len(set(path_ids)) or any(not item for item in path_ids):
        errors.append(f"{label}: active path IDs must be present and unique")
    allowed = contract.get("selectable_path_ids", [])
    if allowed != path_ids:
        errors.append(f"{label}: selector allowlist must exactly preserve the ordered source-supported paths")
    if len(allowed) < 2:
        errors.append(f"{label}: selector must retain at least two source-supported paths")
    if contract.get("contract_version") != 1:
        errors.append(f"{label}: selection contract version must be 1")
    if contract.get("selection_level") not in SELECTION_LEVELS:
        errors.append(f"{label}: selection_level must identify an approved operational context")
    if not contract.get("selection_dimensions") or any(not str(item).strip() for item in contract.get("selection_dimensions", [])):
        errors.append(f"{label}: source-supported selection dimensions are required")
    if contract.get("resolution_mode") not in RESOLUTION_MODES:
        errors.append(f"{label}: unsupported or missing resolution_mode")
    if not contract.get("selector_boundary") or "not a production" not in contract.get("selector_boundary", "").lower():
        errors.append(f"{label}: selector must be bounded as an architecture reference, not a production API/schema")
    if not contract.get("selector_key_rule"):
        errors.append(f"{label}: selector key/context rule is required")
    elif "(scope_id, selection_level, opaque context_id)" not in contract.get("selector_key_rule", "") or "not a persisted/api key schema" not in contract.get("selector_key_rule", "").lower():
        errors.append(f"{label}: reference lookup identity must be explicit and bounded away from a production key schema")
    reference_inputs = contract.get("reference_selector_inputs", {})
    if (
        set(reference_inputs.get("required", []))
        != {"context_level", "context_id", "eligible_path_ids", "eligibility_evidence_refs", "gate_evidence_refs", "resolution_evidence_ref"}
        or set(reference_inputs.get("optional", [])) != {"requested_path_id", "source_default_approval_ref"}
        or "not production" not in reference_inputs.get("boundary", "").lower()
    ):
        errors.append(f"{label}: reference selector inputs must define context, eligibility/gate evidence, optional path/default, and non-production boundary")
    audit = contract.get("selection_audit", {})
    if (
        audit.get("required") is not True
        or audit.get("reference_only") is not True
        or audit.get("not_a_production_audit_schema") is not True
        or len(audit.get("records", [])) < 4
    ):
        errors.append(f"{label}: selection audit must be required in the reference model without claiming a production schema")
    if contract.get("shared_contract_requirement_ids") != scope.get("requirement_ids"):
        errors.append(f"{label}: selector must trace to the scope's exact shared-contract requirements")
    if contract.get("acceptance_criteria_mapping_ref") != "acceptance_criteria_applicability":
        errors.append(f"{label}: selector must reference explicit path acceptance applicability")
    if contract.get("failure_recovery_audit_security_ref") != "failure_recovery_audit_security":
        errors.append(f"{label}: selector must retain the shared failure/recovery/audit/security contract")
    if contract.get("runtime_implementation_status") != "NOT_EVIDENCED":
        errors.append(f"{label}: reference selector must not imply application implementation evidence")

    source_anchors = set(record.get("source_anchors", []))
    path_conditions = contract.get("path_conditions", [])
    condition_ids = [item.get("path_id") for item in path_conditions if isinstance(item, dict)]
    if condition_ids != path_ids:
        errors.append(f"{label}: each selectable path must have exactly one eligibility condition")
    for item in path_conditions:
        path = next((p for p in paths if p.get("path_id") == item.get("path_id")), {})
        if item.get("source_path_behavior") != path.get("source_description") or item.get("scope_condition") != scope.get("selection_context"):
            errors.append(f"{label}/{item.get('path_id')}: eligibility condition must trace to source path and scope context")
        if not item.get("eligibility_rule"):
            errors.append(f"{label}/{item.get('path_id')}: eligibility rule is required")

    default = contract.get("source_default", {})
    if default.get("kind") == "PATH":
        if default.get("path_id") not in allowed or default.get("status") not in {"SOURCE_EXPLICIT", "PROPOSED"}:
            errors.append(f"{label}: source default must be an active source-supported path and explicitly labelled")
        if not default.get("source_text") or not default.get("source_anchor_refs") or not set(default.get("source_anchor_refs", [])) <= source_anchors:
            errors.append(f"{label}: source default requires traceable source text and existing source anchors")
        if contract.get("when_no_selection") != "USE_SOURCE_PATH_DEFAULT_ONLY_AFTER_APPROVAL_AND_ALL_GATES":
            errors.append(f"{label}: source default must remain approval- and gate-controlled")
    elif default.get("kind") == "CONSTRAINT_ONLY":
        if default.get("path_id") is not None or default.get("status") != "PARTIAL" or not default.get("constraints"):
            errors.append(f"{label}: partial default may constrain a mode but cannot choose an unsupported full path")
        if not default.get("source_anchor_refs") or not set(default.get("source_anchor_refs", [])) <= source_anchors:
            errors.append(f"{label}: partial default requires traceable source anchors")
        if contract.get("when_no_selection") != "BLOCK_UNLESS_EXPLICIT_SELECTION_OR_UNAMBIGUOUS_SOURCE_CONDITION":
            errors.append(f"{label}: a partial default cannot silently resolve a path")
    elif default.get("kind") == "NONE":
        if default.get("path_id") is not None or default.get("status") != "NONE" or default.get("source_anchor_refs"):
            errors.append(f"{label}: absent source default must not carry inferred path/approval evidence")
        if contract.get("when_no_selection") != "BLOCK_UNLESS_EXPLICIT_SELECTION_OR_UNAMBIGUOUS_SOURCE_CONDITION":
            errors.append(f"{label}: missing default must fail closed")
    else:
        errors.append(f"{label}: source_default must be PATH, CONSTRAINT_ONLY, or NONE")

    if contract.get("when_ineligible") != "FAIL_CLOSED_NO_FALLBACK":
        errors.append(f"{label}: ineligible paths must fail closed without fallback")
    if contract.get("when_ambiguous") != "FAIL_CLOSED_REQUIRE_EXPLICIT_SOURCE_SUPPORTED_SELECTION":
        errors.append(f"{label}: ambiguous selections must fail closed")
    if contract.get("when_policies_conflict") != "SPLIT_ONLY_WHERE_SOURCE_EXPLICITLY_ALLOWS; OTHERWISE_BLOCK":
        errors.append(f"{label}: policy conflict handling must preserve source-limited split/block behavior")
    gate_policy = contract.get("independent_gate_policy", {})
    if (
        gate_policy.get("gate_source") != "separate_gates"
        or gate_policy.get("all_gates_required_before_activation") is not True
        or gate_policy.get("selection_does_not_close_gates") is not True
        or gate_policy.get("external_authority_and_evidence_remain_required") is not True
    ):
        errors.append(f"{label}: path selection must not replace independent owner/security/finance/legal/evidence gates")
    if scope.get("design_status") == "RUNTIME_SELECTABLE" and contract.get("design_status") != "COMPLETE":
        errors.append(f"{label}: RUNTIME_SELECTABLE requires a complete structured selector contract")
    if scope.get("design_status") == "DESIGN_REVIEW_REQUIRED" and contract.get("design_status") != "BLOCKED_BY_SOURCE_RECONCILIATION":
        errors.append(f"{label}: unreconciled scope cannot have a complete selector contract")

    mappings = scope.get("acceptance_criteria_applicability", [])
    source_criteria = scope.get("source_acceptance_criteria", [])
    mapping_criteria = [item.get("criterion") for item in mappings if isinstance(item, dict)]
    if mapping_criteria != source_criteria:
        errors.append(f"{label}: every source acceptance criterion must have one ordered applicability mapping")
    expected_by_path: dict[str, list[tuple[str, str]]] = {path_id: [] for path_id in path_ids}
    cross_criteria = set()
    for item in mappings:
        if not isinstance(item, dict):
            continue
        criterion = item.get("criterion", "")
        classification = item.get("classification")
        applies_to = item.get("applies_to_path_ids", [])
        if classification not in ACCEPTANCE_CLASSIFICATIONS:
            errors.append(f"{label}: unsupported acceptance applicability classification {classification!r}")
        if item.get("execution_status") != "PLANNED_OR_SOURCE_DEFINED_NOT_EXECUTED":
            errors.append(f"{label}: design acceptance criteria must not be represented as executed evidence")
        if not set(applies_to) <= set(path_ids):
            errors.append(f"{label}: acceptance mapping refers to a non-selectable path")
        if classification == "CROSS_PATH_SCENARIO":
            if applies_to:
                errors.append(f"{label}: cross-path scenario must not be presented as a path-specific criterion")
            cross_criteria.add(criterion)
        elif not applies_to:
            errors.append(f"{label}: non-cross-path acceptance criterion must apply to at least one selectable path")
        for path_id in applies_to:
            expected_by_path[path_id].append((criterion, classification))

    for path in paths:
        path_label = f"{label}/{path.get('path_id', '<missing-path-id>')}"
        actual = path.get("acceptance_criteria", [])
        actual_pairs = [(item.get("criterion"), item.get("applicability")) for item in actual if isinstance(item, dict)]
        if actual_pairs != expected_by_path.get(path.get("path_id"), []):
            errors.append(f"{path_label}: path acceptance criteria must exactly match source applicability")
        if not path.get("acceptance_basis"):
            errors.append(f"{path_label}: acceptance basis/limitations must be stated")
        for item in actual:
            if item.get("execution_status") != "PLANNED_OR_SOURCE_DEFINED_NOT_EXECUTED":
                errors.append(f"{path_label}: acceptance mapping cannot claim executed evidence")
    scenarios = scope.get("cross_path_verification_scenarios", [])
    scenario_text = [item.get("criterion") for item in scenarios if isinstance(item, dict)]
    if set(scenario_text) != cross_criteria or any(
        item.get("execution_status") != "PLANNED_OR_SOURCE_DEFINED_NOT_EXECUTED" for item in scenarios
    ):
        errors.append(f"{label}: scope-level cross-path scenarios must remain planned and match applicability mapping")

    extras = []
    for item in scope.get("deferred_paths", []):
        if item.get("selection_status") != "DEFERRED_NOT_SELECTABLE" or item.get("path_id") in allowed or not item.get("deferral_reason"):
            errors.append(f"{label}: deferred paths require an explicit reason and must remain outside the allowlist")
        extras.append(item.get("path_id"))
    for item in scope.get("orthogonal_configuration_dimensions", []):
        if item.get("selectable_by_connectivity_selector") is not False or item.get("former_path_id") in allowed:
            errors.append(f"{label}: orthogonal configuration dimensions must not be connectivity paths")
        extras.append(item.get("former_path_id"))
    for item in scope.get("excluded_source_options", []):
        if item.get("exclusion_status") != "SOURCE_LIMITATION_NOT_A_SELECTABLE_BEHAVIOR" or item.get("former_path_id") in allowed:
            errors.append(f"{label}: source exclusions must not be selectable paths")
        extras.append(item.get("former_path_id"))
    if len([item for item in extras if item]) != len(set(item for item in extras if item)) or set(extras) & set(allowed):
        errors.append(f"{label}: deferred, orthogonal, and excluded source item IDs must be unique and non-selectable")


def _check_scope(
    reference: str,
    record: dict,
    scope: dict,
    linked_ids: set[str],
    reported_ids: set[str],
    all_ids: set[str],
    root: Path,
    errors: list[str],
) -> None:
    label = f"{reference}/{scope.get('scope_id', '<missing-scope-id>')}"
    required_fields = (
        "source_scope", "selection_context", "shared_contract", "source_acceptance_criteria",
        "paths", "failure_recovery_audit_security", "separate_gates", "global_invariant_refs",
        "design_status", "runtime_implementation_status", "selection_contract",
        "acceptance_criteria_applicability",
    )
    for field in required_fields:
        if field not in scope or scope[field] in (None, "", []):
            errors.append(f"{label}: missing required design field {field}")

    scope_ids = set(scope.get("requirement_ids", []))
    if not scope_ids:
        errors.append(f"{label}: scope must link one or more registry requirements")
    if scope_ids - all_ids:
        errors.append(f"{label}: unknown requirement IDs {sorted(scope_ids - all_ids)}")
    if scope_ids - linked_ids:
        errors.append(f"{label}: scope requirement IDs are not linked to this reference: {sorted(scope_ids - linked_ids)}")

    paths = scope.get("paths", [])
    if not isinstance(paths, list) or len(paths) < 2:
        errors.append(f"{label}: at least two source-supported paths are required")
        paths = []
    scope_criteria = scope.get("source_acceptance_criteria", [])
    if not isinstance(scope_criteria, list) or not scope_criteria:
        errors.append(f"{label}: source-derived acceptance criteria are required")
        scope_criteria = []

    for path in paths:
        path_label = f"{label}/{path.get('path_id', '<missing-path-id>')}"
        if not path.get("source_description", "").strip():
            errors.append(f"{path_label}: path behavior/source description is required")
    _check_selection_contract(scope, record, label, errors)

    failure = scope.get("failure_recovery_audit_security", [])
    if not isinstance(failure, list) or len(failure) < 3 or any(not str(item).strip() for item in failure):
        errors.append(f"{label}: explicit failure/recovery/audit/security handling is required")
    gates = scope.get("separate_gates", [])
    if not isinstance(gates, list) or not gates or any(not str(item).strip() for item in gates):
        errors.append(f"{label}: owner/source/security/finance/evidence gates must remain separately recorded")
    if set(scope.get("global_invariant_refs", [])) != EXPECTED_GLOBAL_INVARIANTS:
        errors.append(f"{label}: global non-suppressible invariant references are missing or changed")

    status = scope.get("design_status")
    if status == "RUNTIME_SELECTABLE":
        if scope_ids - reported_ids:
            errors.append(f"{label}: runtime-selectable scope includes rows not assessed by its review")
        if scope.get("reconciliation_required"):
            errors.append(f"{label}: unresolved review reconciliation cannot be runtime-selectable")
        if scope.get("runtime_implementation_status") != "NOT_EVIDENCED":
            errors.append(f"{label}: design-only record must not imply implementation evidence")
    elif status == "DESIGN_REVIEW_REQUIRED":
        if not scope.get("reconciliation_required"):
            errors.append(f"{label}: review-required scope must state its reconciliation blocker")
        if not record.get("unreviewed_linked_requirement_ids"):
            errors.append(f"{label}: review-required status lacks a corresponding linkage discrepancy")
    elif status == "IMPLEMENTED_MULTI_PATH":
        evidence = scope.get("implementation_evidence", [])
        if not evidence:
            errors.append(f"{label}: IMPLEMENTED_MULTI_PATH requires linked implementation evidence")
        for item in evidence:
            if item.get("status") not in {"EXECUTED", "REVIEWED"} or item.get("result") != "PASS":
                errors.append(f"{label}: implementation evidence must be executed/reviewed and PASS")
            evidence_path = resolve_repo_path(item.get("path", ""))
            if evidence_path is None or not evidence_path.is_file():
                errors.append(f"{label}: implementation evidence path is missing or outside acc-architecture")
    else:
        errors.append(f"{label}: unsupported design_status {status!r}")


def validate_register(
    data: dict | None = None,
    registry_rows: list[dict[str, str]] | None = None,
    repo_root: Path = REPO_ROOT,
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    if data is None:
        data = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
    if registry_rows is None:
        registry_rows = active_rows()

    if data.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if data.get("baseline_commit") != EXPECTED_BASELINE:
        errors.append("register baseline_commit does not match the source baseline")
    if data.get("source_inputs_sha256") != source_digest():
        errors.append("source_inputs_sha256 does not match current registry/decision inputs")

    active = {row.get("requirement_id", ""): row for row in registry_rows if row.get("requirement_id")}
    expected_ref_rows: dict[str, set[str]] = {}
    for rid, row in active.items():
        for ref in split_refs(row.get("open_decisions", "")):
            expected_ref_rows.setdefault(ref, set()).add(rid)

    records = data.get("records", [])
    refs = [record.get("reference", "") for record in records]
    if len(refs) != len(set(refs)):
        errors.append("register has duplicate reference records")
    if set(refs) != set(expected_ref_rows):
        errors.append(
            "register reference coverage differs from active registry; "
            f"missing={sorted(set(expected_ref_rows) - set(refs))}; extra={sorted(set(refs) - set(expected_ref_rows))}"
        )

    decision_data = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
    decision_statuses = {item.get("id"): item.get("status", "") for item in decision_data.get("decisions", [])}
    scopes: list[dict] = []
    for record in records:
        reference = record.get("reference", "")
        linked = expected_ref_rows.get(reference, set())
        recorded_linked = set(record.get("linked_requirement_ids", []))
        if recorded_linked != linked:
            errors.append(f"{reference}: registry-linked requirement IDs do not match active source rows")
        expected_statuses = {rid: active[rid].get("status", "") for rid in linked if rid in active}
        if record.get("linked_requirement_statuses", {}) != expected_statuses:
            errors.append(f"{reference}: requirement lifecycle statuses differ from the source registry")
        reported = set(record.get("review_reported_impact_ids", []))
        if reported - linked:
            errors.append(f"{reference}: review reports requirements not linked in the active registry: {sorted(reported - linked)}")
        uncovered = linked - reported
        if set(record.get("unreviewed_linked_requirement_ids", [])) != uncovered:
            errors.append(f"{reference}: unreviewed linked-row list is not the exact source/review difference")
        if set(record.get("review_reported_ids_not_linked", [])) != reported - linked:
            errors.append(f"{reference}: review/registry discrepancy list is inconsistent")
        if reference == "RP-16":
            reconciliation = record.get("source_reconciliation", {})
            expected_initial = {"SREQ-PH01-CONN-004", "SREQ-PH01-OBS-004", "SREQ-PH01-REL-001"}
            expected_direct = {"SREQ-PH01-CONN-003", "SREQ-PH01-INST-010"}
            initial = set(record.get("initial_review_reported_impact_ids", []))
            reviewed = set(reconciliation.get("reviewed_linked_requirement_ids", []))
            direct = set(reconciliation.get("direct_relevance_ids", []))
            partial = set(reconciliation.get("partial_relevance_ids", []))
            unsupported = set(reconciliation.get("unsupported_ids", []))
            if reconciliation.get("status") != "RECONCILED_ALL_LINKED_ROWS":
                errors.append("RP-16: source reconciliation must be complete before the discrepancy is cleared")
            if initial != expected_initial:
                errors.append("RP-16: original three-row review scope must remain preserved for provenance")
            if reviewed != linked or reported != linked:
                errors.append("RP-16: current review must reconcile every active linked requirement")
            if direct != expected_direct or partial != (linked - direct) or unsupported or direct & partial:
                errors.append("RP-16: direct/partial/unsupported reconciliation must partition the 12 active links")
            artifact = resolve_repo_path(reconciliation.get("artifact_ref", "").split("#", 1)[0])
            if artifact is None or not artifact.is_file():
                errors.append("RP-16: row-by-row source reconciliation artifact must exist inside acc-architecture")
        if record.get("reference_status") not in {"OPEN", "OPEN_OWNER_CONFIRMATION_REQUIRED"}:
            errors.append(f"{reference}: open reference status was altered")
        if reference in decision_statuses and record.get("decision_register_status") != decision_statuses[reference]:
            errors.append(f"{reference}: ADR status differs from decisions.json")

        anchors = record.get("source_anchors", [])
        if not anchors:
            errors.append(f"{reference}: at least one source anchor is required")
        found_direct_trace = False
        for anchor in anchors:
            relative = str(anchor).split("#", 1)[0]
            path = resolve_repo_path(relative)
            if path is None or not path.is_file():
                errors.append(f"{reference}: source target is missing or outside acc-architecture: {relative}")
                continue
            try:
                text = path.read_text(encoding="utf-8-sig").lower()
            except (OSError, UnicodeError):
                errors.append(f"{reference}: source target cannot be read: {relative}")
                continue
            if reference.lower() in text or any(rid.lower() in text for rid in linked):
                found_direct_trace = True
        if anchors and not found_direct_trace:
            errors.append(f"{reference}: source pointers contain no direct reference/requirement trace")
        if uncovered and not any(s.get("design_status") == "DESIGN_REVIEW_REQUIRED" for s in record.get("multi_path_scopes", [])):
            errors.append(f"{reference}: uncovered linked rows must remain a design-review blocker")
        for scope in record.get("multi_path_scopes", []):
            scopes.append(scope)
            _check_scope(reference, record, scope, linked, reported, set(active), repo_root, errors)

    source = data.get("global_invariant_source", {})
    source_path = resolve_repo_path(source.get("path", ""))
    if source_path is None or not source_path.is_file():
        errors.append("global invariant source path is missing or outside acc-architecture")
        invariant_text = ""
    else:
        content = source_path.read_bytes()
        if hashlib.sha256(content).hexdigest() != source.get("sha256"):
            errors.append("global invariant source checksum differs from the repository")
        invariant_text = content.decode("utf-8-sig").lower()
    for required_id in ("CON-003", "CON-004", "CON-005", "CON-008", "NFR-003", "NFR-004", "NFR-006", "NFR-009"):
        if required_id.lower() not in invariant_text:
            errors.append(f"global invariant source does not contain {required_id}")
    invariants = data.get("global_invariants", [])
    invariant_ids = {item.get("id") for item in invariants}
    if invariant_ids != EXPECTED_GLOBAL_INVARIANTS:
        errors.append("global invariant register is missing or changing a required source/security/audit/finance safeguard")

    counts = {
        "active_registry_open_reference_count": len(expected_ref_rows),
        "registered_reference_count": len(records),
        "structured_reviews_available": sum(record.get("review_outcome") == "STRUCTURED_REVIEW_AVAILABLE" for record in records),
        "manual_source_reconciliations": sum(record.get("review_outcome") == "MANUALLY_SOURCE_RECONCILED_PRIOR_REVIEW_SCHEMA_FAILURE" for record in records),
        "references_with_multi_path_scopes": sum(bool(record.get("multi_path_scopes")) for record in records),
        "multi_path_scope_count": len(scopes),
        "runtime_selectable_scope_count": sum(scope.get("design_status") == "RUNTIME_SELECTABLE" for scope in scopes),
        "implemented_multi_path_scope_count": sum(scope.get("design_status") == "IMPLEMENTED_MULTI_PATH" for scope in scopes),
        "design_review_required_scope_count": sum(scope.get("design_status") == "DESIGN_REVIEW_REQUIRED" for scope in scopes),
        "review_link_discrepancy_count": sum(bool(record.get("unreviewed_linked_requirement_ids") or record.get("review_reported_ids_not_linked")) for record in records),
        "distinct_open_reference_roots": len(expected_ref_rows),
        "complete_selector_contract_count": sum(scope.get("selection_contract", {}).get("design_status") == "COMPLETE" for scope in scopes),
        "active_selectable_path_count": sum(len(scope.get("selection_contract", {}).get("selectable_path_ids", [])) for scope in scopes if scope.get("design_status") == "RUNTIME_SELECTABLE"),
        "deferred_path_count": sum(len(scope.get("deferred_paths", [])) for scope in scopes),
        "orthogonal_configuration_dimension_count": sum(len(scope.get("orthogonal_configuration_dimensions", [])) for scope in scopes),
        "excluded_source_option_count": sum(len(scope.get("excluded_source_options", [])) for scope in scopes),
    }
    if data.get("summary") != counts:
        errors.append(f"stored summary differs from recomputed counts: {counts}")
    if counts != EXPECTED_SCOPE_COUNTS:
        errors.append(f"recomputed counts differ from the reconciled expectation: {counts}")
    return errors, counts


def main() -> int:
    try:
        errors, counts = validate_register()
    except Exception as exc:
        print(f"FAIL: could not validate multi-path readiness register: {exc}")
        return 1
    if errors:
        print("FAIL: multi-path design validation found errors:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: multi-path design records and source links validated independently of strict-ready")
    print(
        f"  open-reference roots={counts['distinct_open_reference_roots']}; "
        f"multi-path references={counts['references_with_multi_path_scopes']}; scopes={counts['multi_path_scope_count']}"
    )
    print(
        f"  RUNTIME_SELECTABLE={counts['runtime_selectable_scope_count']}; "
        f"IMPLEMENTED_MULTI_PATH={counts['implemented_multi_path_scope_count']}; "
        f"DESIGN_REVIEW_REQUIRED={counts['design_review_required_scope_count']}"
    )
    print(
        f"  complete selector contracts={counts['complete_selector_contract_count']}; "
        f"active selectable paths={counts['active_selectable_path_count']}; "
        f"deferred={counts['deferred_path_count']}; orthogonal dimensions={counts['orthogonal_configuration_dimension_count']}; "
        f"source exclusions={counts['excluded_source_option_count']}"
    )
    print("  RP-16 source links reconciled=12/12 (2 direct, 10 partial, 0 unsupported); independent approval/evidence gates remain open.")
    print("  This design validator does not authorize or change requirement statuses, evidence, or strict-ready results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
