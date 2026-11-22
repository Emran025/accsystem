# RP-16 Source Reconciliation — Cycle 21

## Result

The active requirements registry links **12 rows** to `RP-16`. The earlier review reported only three rows and incorrectly stated that `SREQ-PH01-CONN-003` was not active. A source-by-source reconciliation now covers all 12 linked rows: **2 direct**, **10 partial**, and **0 unsupported**. “Direct” means the requirement itself states an authentication-mode or revoked-credential behavior; “partial” means it addresses one related slice without representing the whole RP-16 scope. None of these classifications is implementation or approval evidence.

The only selectable authentication alternatives supported by the source are **OAuth 2.0 Client Credentials** and **mTLS**, enabled per institution under security/operations policy. They share the logical connector contract. The alternatives are modeled only for the connector authentication scope; they do not create 12 separate choices, authorize API keys, close lifecycle/release/security gates, or imply that either method is currently approved for an institution.

## Row-by-row reconciliation

| Active requirement ID | Relation to RP-16 | Source-supported impact and boundary |
|---|---|---|
| `REQ-PH01-CORE-CONNECTIVITY` | Partial | The parent includes policy-selected authentication and identity binding through `SREQ-PH01-CONN-003/004`. RP-16 does not establish every connectivity mode, health behavior, or release-trust behavior in the parent. |
| `REQ-PH01-INSTITUTION-LIFECYCLE` | Partial | The lifecycle parent covers institution setup and credential/certificate lifecycle. The authentication alternatives apply only to its integration-configuration slice; no wire schema, rotation schedule, or replay policy is approved here. |
| `REQ-PH01-OBSERVABILITY-AND-RECOVERY` | Partial | The parent has a limited overlap through secret/key handling. RP-16 does not independently establish the parent’s observability, recovery, or availability policies. |
| `REQ-PH01-RELEASE-PROVENANCE` | Partial | The source has adjacent release-integrity and signed-status concerns, but those are not additional authentication paths and their verification remains separate. |
| `SREQ-PH01-CONN-003` | **Direct** | Per-institution OAuth 2.0 Client Credentials and/or mTLS are enabled by security/operations policy and verified on inbound messages; a method not enabled for that institution is refused. This is the primary authentication-path requirement. |
| `SREQ-PH01-CONN-004` | Partial | Authenticated-principal-to-institution binding and 403 on a body/path mismatch form a shared connector invariant; this row does not itself select an authentication method. |
| `SREQ-PH01-INST-004` | Partial | Onboarding creates institution integration configuration and credential/certificate references. This does not choose a method or finalize schema and secret-handling evidence. |
| `SREQ-PH01-INST-009` | Partial | The requirement describes accepting old and new credentials during an approved transition, then only the new one. The transition policy and execution test remain open. |
| `SREQ-PH01-INST-010` | **Direct** | Authentication with a revoked integration credential/certificate is rejected. The row does not establish revocation propagation/availability or executed test evidence. |
| `SREQ-PH01-OBS-004` | Partial | Secrets stay out of source code and client bundles and support rotation. The planned secret-handling review and rotation evidence remain open. |
| `SREQ-PH01-REL-001` | Partial | Digest, signature, and required provenance verification gate release availability. This is a release-integrity requirement, not an OAuth/mTLS selector path. |
| `SREQ-PH01-REL-003` | Partial | ACCore reports signed release/source/build/configuration fingerprints and mismatches create notification/audit effects. Its API/event schema and test remain open; it does not add an authentication method. |

All 12 source rows remain `DRAFT`; their verification references remain planned or review-planned. Their links to `RP-16` are retained. The exact active-row/status linkage is recomputed by `validate_multi_path_readiness.py` against `requirements-registry.csv`.

## Narrow runtime-selectable design scope

The architecture-only selector scope is limited to `SREQ-PH01-CONN-003` and `SREQ-PH01-CONN-004`: per-institution OAuth 2.0 Client Credentials or mTLS, with identity derived from the authenticated principal and mismatch rejected. Selection is explicit, policy-backed, and fails closed if missing, ambiguous, or ineligible; no default or fallback is inferred. The selector model is not a production API, wire schema, or persisted configuration schema.

This classification means the alternatives can coexist in the design and be selected at the institution context when independent gates and evidence permit. It does **not** mean an institution has selected or enabled either option. The reference selector still requires evidence for path eligibility and every independent gate before it can return a selection.

## Gates that remain open

- Owner/security/operations approval of the per-institution method and the proposed ADR-015 baseline is not recorded.
- Executable OpenAPI/AsyncAPI contracts, field/type and version mapping, and API-governance approval remain open (`IC-002`, `ADR-021-GATE`, `RGAP-PH01-006`).
- Key issuance/storage, rotation transition policy, revocation propagation/availability, replay/idempotency tests, and credential-handling evidence remain unratified or unexecuted.
- `SREQ-PH01-OBS-004` still requires its secret-handling review and rotation evidence.
- `SREQ-PH01-REL-001` and `SREQ-PH01-REL-003` retain their release-provenance and signed-status verification requirements and planned tests.
- Requirement status acceptance, canonical use-case/function traceability, executed functional tests, and external approval evidence remain separate strict-ready/acceptance gates.

The reconciliation corrects review coverage and design traceability only. It does not change the requirements registry, decision status, owner approval, implementation status, or strict-ready result.

## Source anchors

- [`requirements-registry.csv`](../execution-phases/requirements-registry.csv#requirements-registry) — the 12 active `RP-16` links and their current statuses.
- [`REQ-PH01-CORE-CONNECTIVITY.md` §3–§6](../execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md) — `CONN-003/004`, acceptance criteria, authentication scope, and open schema/lifecycle gates.
- [`REQ-PH01-INSTITUTION-LIFECYCLE.md` §3–§6](../execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md) — onboarding and credential lifecycle requirements.
- [`REQ-PH01-OBSERVABILITY-AND-RECOVERY.md` §3–§6](../execution-phases/phase-01-platform-foundation/REQ-PH01-OBSERVABILITY-AND-RECOVERY.md) — secret-handling requirement and planned review.
- [`REQ-PH01-RELEASE-PROVENANCE.md` §3–§6](../execution-phases/phase-01-platform-foundation/REQ-PH01-RELEASE-PROVENANCE.md) — release verification and signed status exchange.
- [`ADR-015.md`](../decisions/ADR-015.md), [`CMP-INT-GATEWAY.md`](../c3-components/CNT-ACC-INTEGRATION/CMP-INT-GATEWAY.md), and the [security view](../supporting-views/security-view.md) — policy-controlled authentication alternatives, common gateway, and independent approval/security gates.
