"""Fail-closed reference selector for architecture review; not ACCSystem runtime code."""
from __future__ import annotations

from typing import Any


def _blocked(reason: str) -> dict[str, Any]:
    return {"status": "BLOCKED", "reason": reason, "selected_path_id": None, "audit": {}}


def resolve_path(
    scope: dict[str, Any],
    *,
    context_level: str,
    context_id: str,
    eligible_path_ids: set[str],
    eligibility_evidence_refs: dict[str, str],
    gate_evidence_refs: dict[str, str],
    resolution_evidence_ref: str,
    requested_path_id: str | None = None,
    source_default_approval_ref: str | None = None,
) -> dict[str, Any]:
    """Resolve one architecture path only when selection and all gates are evidenced.

    ``eligible_path_ids`` and evidence references are supplied by the calling review
    harness; this reference model cannot verify their external truth. It is not a
    production selector, wire schema, or approval authority.
    """
    contract = scope.get("selection_contract", {})
    if scope.get("design_status") != "RUNTIME_SELECTABLE" or contract.get("design_status") != "COMPLETE":
        return _blocked("scope design is not fully reconciled and runtime-selectable")
    if contract.get("runtime_implementation_status") != "NOT_EVIDENCED":
        return _blocked("reference selector cannot imply or substitute implementation evidence")
    if context_level != contract.get("selection_level") or not context_id.strip():
        return _blocked("selection context is missing or does not match the contract")
    if not resolution_evidence_ref.strip():
        return _blocked("selection decision/condition evidence reference is required")

    required_gates = set(scope.get("separate_gates", []))
    if not required_gates or any(not gate_evidence_refs.get(gate, "").strip() for gate in required_gates):
        return _blocked("every independent gate requires its own external evidence reference")

    allowed = set(contract.get("selectable_path_ids", []))
    if len(allowed) < 2:
        return _blocked("contract does not contain at least two source-supported selectable paths")
    if eligible_path_ids - allowed:
        return _blocked("eligibility input contains a path outside the source-supported allowlist")
    if set(eligibility_evidence_refs) != eligible_path_ids or any(
        not str(ref).strip() for ref in eligibility_evidence_refs.values()
    ):
        return _blocked("every eligible path requires its own non-empty source/condition evidence reference")
    eligible = eligible_path_ids & allowed
    if requested_path_id is not None:
        if requested_path_id not in allowed:
            return _blocked("requested path is not in this scope's source-supported allowlist")
        if requested_path_id not in eligible:
            return _blocked("requested path is not eligible in the supplied operational context")
        selected = requested_path_id
        reason = "explicit source-supported selection; eligibility and all independent gates evidenced"
    else:
        source_default = contract.get("source_default", {})
        default_path_id = source_default.get("path_id")
        if (
            default_path_id
            and default_path_id in eligible
            and source_default_approval_ref
            and source_default_approval_ref.strip()
        ):
            selected = default_path_id
            reason = "source-stated default applied only after external approval and all independent gates"
        elif contract.get("resolution_mode") == "CONDITION_BASED" and len(eligible) == 1:
            selected = next(iter(eligible))
            reason = "exactly one source-defined condition is evidenced; no ambiguous fallback"
        elif not eligible:
            return _blocked("no source-supported path is eligible in this context")
        else:
            return _blocked("no explicit selection or approved source default; do not infer from availability")

    return {
        "status": "SELECTED",
        "reason": reason,
        "selected_path_id": selected,
        "audit": {
            "scope_id": scope.get("scope_id"),
            "context_level": context_level,
            "context_id": context_id,
            "resolution_evidence_ref": resolution_evidence_ref,
            "eligibility_evidence_refs": {path_id: eligibility_evidence_refs[path_id] for path_id in sorted(eligible)},
            "gate_evidence_refs": {gate: gate_evidence_refs[gate] for gate in sorted(required_gates)},
            "source_default_approval_ref": source_default_approval_ref,
        },
    }
