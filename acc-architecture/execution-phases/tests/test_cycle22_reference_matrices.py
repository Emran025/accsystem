"""Cycle 22 architecture-reference matrices; not ACCSystem/ACCore runtime tests.

All evidence in this module is synthetic test input. Passing these tests proves only
that the documented reference decision rules are internally consistent; it does not
prove provider capability, external approval, production contracts, or implementation.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ARCH_DIR = TEST_DIR.parents[1]
VALIDATION_DIR = ARCH_DIR / "validation"
sys.path.insert(0, str(VALIDATION_DIR))
import multi_path_selector_reference as selector  # noqa: E402

REGISTER_PATH = VALIDATION_DIR / "multi-path-readiness-register.json"
ASSUM003_PATHS = {
    "aggregate": "assum-003-scope-01-path-01",
    "separate": "assum-003-scope-01-path-02",
}
IC003_PATHS = {
    "adapter": "ic-003-scope-01-path-01",
    "reconciliation": "ic-003-scope-01-path-02",
}
IC006_PATHS = {
    "synchronous": "ic-006-scope-01-path-01",
    "callback": "ic-006-scope-01-path-02",
}


ALLOCATION_FIELDS = {
    "seller/order allocation identity",
    "amount and currency",
    "tax/delivery basis",
    "policy snapshot",
    "correlation identity",
    "operation-scoped idempotency identity",
}
SCOPED_PROVIDER_REFERENCE_FIELDS = {
    "payment_attempt_id",
    "seller_order_id",
    "allocation_id",
}
WEBHOOK_SCOPING_FIELDS = {
    "provider reference",
    "payment_attempt_id",
    "seller_order_id",
    "allocation_id",
    "operation identity",
}
ACCEPTED_RESERVATION_FIELDS = {
    "reservation reference",
    "confirmed price",
    "confirmed quantity",
    "expiry",
}


def _scope(data: dict, reference: str, scope_id: str) -> dict:
    record = next(item for item in data["records"] if item["reference"] == reference)
    return next(item for item in record["multi_path_scopes"] if item["scope_id"] == scope_id)


def _assum003_reference_selection(
    *,
    policies_compatible: bool | None,
    aggregate_allocation_capability: bool | None,
    separate_attempt_capability: bool | None,
    gates_evidenced: bool,
    allocation_fields: set[str],
    retry_idempotency_identity_stable: bool,
    provider_reference_scope: set[str],
) -> str | None:
    """Return a source-supported path ID, or None to block/defer this reference case."""
    if not gates_evidenced or policies_compatible is None:
        return None
    if not ALLOCATION_FIELDS <= allocation_fields:
        return None
    if not retry_idempotency_identity_stable:
        return None
    if not SCOPED_PROVIDER_REFERENCE_FIELDS <= provider_reference_scope:
        return None
    if policies_compatible and aggregate_allocation_capability is True:
        return ASSUM003_PATHS["aggregate"]
    if separate_attempt_capability is True:
        return ASSUM003_PATHS["separate"]
    return None


def _ic003_reference_event(
    *,
    provider_profile_evidenced: bool,
    independent_gates_evidenced: bool,
    signature_valid: bool,
    approved_timestamp_check_passed: bool,
    event_known: bool,
    mapping_fields: set[str],
    incoming_event_id: str = "test-provider-event",
    durably_recorded_event_id: str | None = None,
    durable_completed_result: bool = False,
) -> dict[str, object]:
    """Model reference outcomes without defining a provider wire/ACK schema."""
    result: dict[str, object] = {
        "state_mutation": False,
        "reconciliation_required": False,
        "acknowledge_as_completed_duplicate": False,
    }
    if not provider_profile_evidenced or not independent_gates_evidenced:
        result["outcome"] = "BLOCKED_NO_MUTATION"
        return result
    if not signature_valid or not approved_timestamp_check_passed:
        result["outcome"] = "REJECT_NO_MUTATION_SECURITY_ALERT"
        return result
    duplicate_event = (
        durably_recorded_event_id is not None
        and incoming_event_id == durably_recorded_event_id
    )
    if duplicate_event:
        if durable_completed_result:
            result["outcome"] = "DURABLE_DUPLICATE_NO_EFFECT"
            result["acknowledge_as_completed_duplicate"] = True
        else:
            result["outcome"] = "RECOVERY_REQUIRED_NO_MUTATION"
        return result
    if not event_known:
        result["outcome"] = "UNKNOWN_EVENT_NO_STATE_CHANGE"
        return result
    if not WEBHOOK_SCOPING_FIELDS <= mapping_fields:
        result["outcome"] = "UNKNOWN_SCOPED_RECONCILIATION"
        result["reconciliation_required"] = True
        return result
    result["outcome"] = "APPLY_ONE_SCOPED_OPERATION"
    result["state_mutation"] = True
    return result


def _ic006_callback_path_eligible(
    *,
    explicitly_requested: bool,
    callback_approved: bool,
    adr015_institution_approval: bool,
    rp03_delivery_contract_approved: bool,
) -> bool:
    """Callback is eligible only when explicitly requested and all named gates hold."""
    return bool(
        explicitly_requested
        and callback_approved
        and adr015_institution_approval
        and rp03_delivery_contract_approved
    )


def _ic006_reference_outcome(
    *,
    delivery_path_id: str,
    response_status: str | None,
    possible_dispatch: bool,
    authoritative_expiry_evidence: bool,
    accepted_fields: set[str],
    all_required_holds_and_guards_satisfied: bool,
    prior_state: str | None = None,
    same_idempotency_identity: bool = True,
) -> dict[str, object]:
    """Model shared reservation semantics for either delivery path, not runtime code."""
    if delivery_path_id not in IC006_PATHS.values():
        return {"state": "BLOCKED_UNSUPPORTED_REFERENCE_PATH", "payment_allowed": False, "release_allowed": False, "repeat_reservation": False}
    canonical = {"ACCEPTED", "REJECTED", "UNKNOWN", "EXPIRED"}
    if response_status is not None and response_status not in canonical:
        return {"state": "INVALID_CONTRACT_VALUE", "payment_allowed": False, "release_allowed": False, "repeat_reservation": False}
    if response_status is None:
        state = "UNKNOWN" if possible_dispatch else "NO_DISPATCH_EVIDENCED"
    elif response_status == "EXPIRED" and not authoritative_expiry_evidence:
        state = "UNKNOWN"
    else:
        state = response_status

    if state == "ACCEPTED" and not ACCEPTED_RESERVATION_FIELDS <= accepted_fields:
        state = "UNKNOWN"
    repeated_unknown_resolution = prior_state == "UNKNOWN" and state == "ACCEPTED"
    duplicate = prior_state is not None and same_idempotency_identity
    return {
        "delivery_path_id": delivery_path_id,
        "state": state,
        "payment_allowed": state == "ACCEPTED" and all_required_holds_and_guards_satisfied,
        "release_allowed": False if state == "UNKNOWN" else None,
        "repeat_reservation": False if state == "UNKNOWN" or repeated_unknown_resolution or duplicate else None,
    }


class Cycle22ReferenceMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))

    def test_assum003_four_policy_capability_combinations(self):
        """Aggregation is conditional; otherwise use evidenced separate attempts."""
        cases = (
            (True, True, ASSUM003_PATHS["aggregate"]),
            (True, False, ASSUM003_PATHS["separate"]),
            (False, True, ASSUM003_PATHS["separate"]),
            (False, False, ASSUM003_PATHS["separate"]),
        )
        for compatible, aggregate_capable, expected_path in cases:
            with self.subTest(compatible=compatible, aggregate_capable=aggregate_capable):
                result = _assum003_reference_selection(
                    policies_compatible=compatible,
                    aggregate_allocation_capability=aggregate_capable,
                    separate_attempt_capability=True,
                    gates_evidenced=True,
                    allocation_fields=set(ALLOCATION_FIELDS),
                    retry_idempotency_identity_stable=True,
                    provider_reference_scope=set(SCOPED_PROVIDER_REFERENCE_FIELDS),
                )
                self.assertEqual(expected_path, result)

        scope = _scope(self.data, "ASSUM-003", "assum-003-scope-01")
        self.assertEqual("transaction", scope["selection_contract"]["selection_level"])
        self.assertEqual("NONE", scope["selection_contract"]["source_default"]["kind"])
        self.assertEqual("NOT_EVIDENCED", scope["runtime_implementation_status"])

    def test_assum003_blocks_missing_gate_fields_capability_or_ambiguous_policy(self):
        base = dict(
            policies_compatible=True,
            aggregate_allocation_capability=True,
            separate_attempt_capability=True,
            gates_evidenced=True,
            allocation_fields=set(ALLOCATION_FIELDS),
            retry_idempotency_identity_stable=True,
            provider_reference_scope=set(SCOPED_PROVIDER_REFERENCE_FIELDS),
        )
        mutations = (
            {"gates_evidenced": False},
            {"policies_compatible": None},
            {"aggregate_allocation_capability": False, "separate_attempt_capability": False},
            {"allocation_fields": ALLOCATION_FIELDS - {"policy snapshot"}},
            {"retry_idempotency_identity_stable": False},
            {"provider_reference_scope": {"order_id"}},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                args = dict(base)
                args.update(mutation)
                self.assertIsNone(_assum003_reference_selection(**args))

        # A compatible policy is not enough: unverified/missing aggregate support cannot enable aggregation.
        self.assertEqual(
            ASSUM003_PATHS["separate"],
            _assum003_reference_selection(
                **(base | {"aggregate_allocation_capability": None})
            ),
        )

    def test_ic003_rejects_invalid_security_evidence_before_mutation(self):
        base = dict(
            provider_profile_evidenced=True,
            independent_gates_evidenced=True,
            signature_valid=True,
            approved_timestamp_check_passed=True,
            event_known=True,
            mapping_fields=set(WEBHOOK_SCOPING_FIELDS),
        )
        for change in ({"signature_valid": False}, {"approved_timestamp_check_passed": False}):
            with self.subTest(change=change):
                result = _ic003_reference_event(**(base | change))
                self.assertEqual("REJECT_NO_MUTATION_SECURITY_ALERT", result["outcome"])
                self.assertFalse(result["state_mutation"])

    def test_ic003_unmappable_or_order_only_event_is_unknown_for_reconciliation(self):
        base = dict(
            provider_profile_evidenced=True,
            independent_gates_evidenced=True,
            signature_valid=True,
            approved_timestamp_check_passed=True,
            event_known=True,
            mapping_fields=set(WEBHOOK_SCOPING_FIELDS),
        )
        for mapping in (set(), {"order_id"}, WEBHOOK_SCOPING_FIELDS - {"allocation_id"}):
            with self.subTest(mapping=mapping):
                result = _ic003_reference_event(**(base | {"mapping_fields": set(mapping)}))
                self.assertEqual("UNKNOWN_SCOPED_RECONCILIATION", result["outcome"])
                self.assertTrue(result["reconciliation_required"])
                self.assertFalse(result["state_mutation"])

    def test_ic003_duplicate_requires_durable_completion_and_distinct_events_are_not_collapsed(self):
        base = dict(
            provider_profile_evidenced=True,
            independent_gates_evidenced=True,
            signature_valid=True,
            approved_timestamp_check_passed=True,
            event_known=True,
            mapping_fields=set(WEBHOOK_SCOPING_FIELDS),
            incoming_event_id="test-provider-event-A",
        )
        pending = _ic003_reference_event(**(base | {
            "durably_recorded_event_id": "test-provider-event-A",
            "durable_completed_result": False,
        }))
        self.assertEqual("RECOVERY_REQUIRED_NO_MUTATION", pending["outcome"])
        self.assertFalse(pending["acknowledge_as_completed_duplicate"])
        completed = _ic003_reference_event(**(base | {
            "durably_recorded_event_id": "test-provider-event-A",
            "durable_completed_result": True,
        }))
        self.assertEqual("DURABLE_DUPLICATE_NO_EFFECT", completed["outcome"])
        self.assertTrue(completed["acknowledge_as_completed_duplicate"])
        self.assertFalse(completed["state_mutation"])

        # Different provider event identities represent distinct lifecycle events, not duplicates.
        distinct = _ic003_reference_event(**(base | {
            "incoming_event_id": "test-provider-event-B",
            "durably_recorded_event_id": "test-provider-event-A",
        }))
        self.assertEqual("APPLY_ONE_SCOPED_OPERATION", distinct["outcome"])
        self.assertTrue(distinct["state_mutation"])

    def test_ic003_missing_provider_profile_or_gate_blocks_without_fallback(self):
        base = dict(
            provider_profile_evidenced=True,
            independent_gates_evidenced=True,
            signature_valid=True,
            approved_timestamp_check_passed=True,
            event_known=True,
            mapping_fields=set(WEBHOOK_SCOPING_FIELDS),
        )
        for change in ({"provider_profile_evidenced": False}, {"independent_gates_evidenced": False}):
            with self.subTest(change=change):
                result = _ic003_reference_event(**(base | change))
                self.assertEqual("BLOCKED_NO_MUTATION", result["outcome"])
                self.assertFalse(result["state_mutation"])

    def test_ic006_callback_is_not_eligible_without_explicit_request_and_all_gates(self):
        scope = _scope(self.data, "IC-006", "ic-006-scope-01")
        self.assertEqual("organization", scope["selection_contract"]["selection_level"])
        self.assertEqual("PATH", scope["selection_contract"]["source_default"]["kind"])
        self.assertEqual(IC006_PATHS["synchronous"], scope["selection_contract"]["source_default"]["path_id"])
        self.assertEqual("NOT_EVIDENCED", scope["runtime_implementation_status"])

        for callback in (False, True):
            for adr015 in (False, True):
                for rp03 in (False, True):
                    with self.subTest(callback=callback, adr015=adr015, rp03=rp03):
                        self.assertEqual(
                            callback and adr015 and rp03,
                            _ic006_callback_path_eligible(
                                explicitly_requested=True,
                                callback_approved=callback,
                                adr015_institution_approval=adr015,
                                rp03_delivery_contract_approved=rp03,
                            ),
                        )
        self.assertFalse(
            _ic006_callback_path_eligible(
                explicitly_requested=False,
                callback_approved=True,
                adr015_institution_approval=True,
                rp03_delivery_contract_approved=True,
            )
        )

    def test_ic006_unknown_timeout_blocks_payment_release_and_repeat_effect_for_both_paths(self):
        for path_id in IC006_PATHS.values():
            with self.subTest(path_id=path_id):
                result = _ic006_reference_outcome(
                    delivery_path_id=path_id,
                    response_status=None,
                    possible_dispatch=True,
                    authoritative_expiry_evidence=False,
                    accepted_fields=set(ACCEPTED_RESERVATION_FIELDS),
                    all_required_holds_and_guards_satisfied=True,
                    prior_state=None,
                )
                self.assertEqual("UNKNOWN", result["state"])
                self.assertFalse(result["payment_allowed"])
                self.assertFalse(result["release_allowed"])
                self.assertFalse(result["repeat_reservation"])

    def test_ic006_expiry_is_authoritative_and_accepted_requires_source_fields(self):
        elapsed_only = _ic006_reference_outcome(
            delivery_path_id=IC006_PATHS["synchronous"],
            response_status="EXPIRED",
            possible_dispatch=True,
            authoritative_expiry_evidence=False,
            accepted_fields=set(ACCEPTED_RESERVATION_FIELDS),
            all_required_holds_and_guards_satisfied=True,
        )
        self.assertEqual("UNKNOWN", elapsed_only["state"])
        self.assertFalse(elapsed_only["payment_allowed"])

        authoritative = _ic006_reference_outcome(
            delivery_path_id=IC006_PATHS["synchronous"],
            response_status="EXPIRED",
            possible_dispatch=True,
            authoritative_expiry_evidence=True,
            accepted_fields=set(ACCEPTED_RESERVATION_FIELDS),
            all_required_holds_and_guards_satisfied=True,
        )
        self.assertEqual("EXPIRED", authoritative["state"])

        incomplete_accepted = _ic006_reference_outcome(
            delivery_path_id=IC006_PATHS["synchronous"],
            response_status="ACCEPTED",
            possible_dispatch=True,
            authoritative_expiry_evidence=False,
            accepted_fields=ACCEPTED_RESERVATION_FIELDS - {"reservation reference"},
            all_required_holds_and_guards_satisfied=True,
        )
        self.assertEqual("UNKNOWN", incomplete_accepted["state"])
        self.assertFalse(incomplete_accepted["payment_allowed"])

    def test_ic006_unknown_to_accepted_does_not_repeat_and_payment_needs_all_guards(self):
        resolved_by_path = []
        for path_id in IC006_PATHS.values():
            resolved = _ic006_reference_outcome(
                delivery_path_id=path_id,
                response_status="ACCEPTED",
                possible_dispatch=True,
                authoritative_expiry_evidence=False,
                accepted_fields=set(ACCEPTED_RESERVATION_FIELDS),
                all_required_holds_and_guards_satisfied=True,
                prior_state="UNKNOWN",
                same_idempotency_identity=True,
            )
            self.assertEqual("ACCEPTED", resolved["state"])
            self.assertTrue(resolved["payment_allowed"])
            self.assertFalse(resolved["repeat_reservation"])
            resolved_by_path.append({key: value for key, value in resolved.items() if key != "delivery_path_id"})
        self.assertEqual(resolved_by_path[0], resolved_by_path[1])

        blocked_payment = _ic006_reference_outcome(
            delivery_path_id=IC006_PATHS["synchronous"],
            response_status="ACCEPTED",
            possible_dispatch=True,
            authoritative_expiry_evidence=False,
            accepted_fields=set(ACCEPTED_RESERVATION_FIELDS),
            all_required_holds_and_guards_satisfied=False,
        )
        self.assertFalse(blocked_payment["payment_allowed"])


if __name__ == "__main__":
    unittest.main()
