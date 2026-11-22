# Cycle 21 — RP-16 source reconciliation and blocker-count correction

**Cycle-start baseline:** `f01db3f7dbf23a04f79e9f3ae09becf929f0bc6a` on `main`. The requirements/decision source snapshot remains `47b8b08b86676233be17063e4101d17d8b27bdfa` with input digest `c556587077de798cd764092f3a56361a73b19beda7c975ca7e7dff6e9a2f7118`.

## Corrections made

The `RP-16` model previously claimed that only three active requirements were affected and that `SREQ-PH01-CONN-003` was absent. The source registry contradicts that statement: it links 12 active rows to `RP-16`, including the policy-selected OAuth/mTLS requirement `SREQ-PH01-CONN-003`. The original three-row review list is now retained as provenance, and a row-by-row source reconciliation covers all 12 links: **2 direct**, **10 partial**, and **0 unsupported**. No source link was removed.

The runtime-selectable scope is now accurately limited to `SREQ-PH01-CONN-003` (OAuth 2.0 Client Credentials or mTLS as per-institution alternatives) and the shared principal-to-institution invariant `SREQ-PH01-CONN-004`. The reference selector has no inferred default or fallback. Selection requires explicit policy-supported choice, path eligibility evidence, and evidence for each independent gate. API keys remain excluded. The selector model remains architecture-only, not a production configuration/API schema.

The validator now rejects an incomplete or mispartitioned RP-16 reconciliation and requires the row-by-row artifact inside `acc-architecture/`. It reports 41 runtime-selectable design scopes, 0 implemented multi-path scopes, 0 review scopes held for linkage reconciliation, 41 complete selector contracts, and 103 selectable path entries. The RP-16 classification change is **not** implementation evidence or an authorization to activate either authentication path.

## RGAP count reconciliation

The active `use_case_id` fields mention 12 distinct `RGAP` IDs, while only 11 roots produce unresolved strict-ready use-case blocker relations (165 requirement-to-gap pairs). `RGAP-PH02-003` appears on seven checkout rows as a qualifier on the canonical `FN-ORD-CHECKOUT` reference for steps 1–3. Those rows do not contain a use-case placeholder, so this ID is not a strict-ready use-case blocker. This distinction does not establish that the full checkout flow is specified or complete.

## Readiness and open gates

Strict-ready is unchanged: **835 overlapping predicate findings across 268 unique active requirement IDs** (status=268, use_case=165, decision=179, verification=223). The PH-01–PH-04 package is still not strict-ready or implementation-ready. No requirement, decision, approval, or implementation status was changed; no API key path, new requirement ID, Use Case ID, or PH-05 was added.

The following remain independent open gates:

- Owner/security/operations approval for the per-institution authentication policy and ADR-015 baseline.
- Executable OpenAPI/AsyncAPI connector/event schemas and approved field/type/version mapping (`IC-002`, `ADR-021-GATE`, `RGAP-PH01-006`).
- Key issuance/storage, rotation-transition policy, revocation propagation/availability, replay/idempotency tests, and credential-handling evidence.
- Planned secret-handling and release-provenance verification for `SREQ-PH01-OBS-004`, `SREQ-PH01-REL-001`, and `SREQ-PH01-REL-003`.
- Accepted requirement statuses, canonical function/use-case traceability, and executed functional acceptance evidence.

## Verification

- `validate_requirements.py --check --require-rows`: **PASS**, 278/278 rows.
- `validate_multi_path_readiness.py`: **PASS**, 61 open references; 37 multi-path references; 41 scopes; 41 runtime-selectable; 0 implemented; 0 linkage-review blockers; 41 complete selector contracts; 103 active selectable path entries.
- `validate_strict_ready_diagnostic_indexes.py`: **PASS**, historical indexes preserved and current Cycle 18 source-input digest still matches.
- `validate_requirements.py --check --strict-ready --summary`: **FAIL as required**, exit 1, 835 findings across 268 unique active rows, 0 additional validation errors.
- `unittest discover -s acc-architecture/execution-phases/tests -p 'test_*.py'`: **PASS, 66/66 tests**. The tests cover source reconciliation, selector fail-closed behavior, independent gates, exact RGAP-root counting, and report consistency. They are documentation/validator tests, not application acceptance tests.
- `git diff --check`: clean; intended changes remain within `acc-architecture/`.

See the [row-by-row RP-16 reconciliation](rp-16-source-reconciliation.md), [current coverage matrix](requirements-coverage-matrix.md), [current readiness diagnostic](requirements-readiness-report.md), and [machine-checkable multi-path register](multi-path-readiness-register.json).
