# ADR Evidence Matrix — Current Review Baseline

**Status:** Current evidence index; not an approval record and not a runtime test report.

This matrix separates documented technical baselines from executed evidence and stakeholder approval. A structural validator result does not mark a contract, policy, provider, security, Finance, Legal, or institutional decision as executed or approved.

| ADR / criterion | Evidence state | Artifact or run reference | Owner / approval gate |
|---|---|---|---|
| ADR-016 — multi-seller ParentOrder/SellerOrder and payment alternatives | Technical baseline recorded; stakeholder approval not recorded | `decisions/ADR-016.md`; `registry/decisions.json` status `proposed` | Product, Finance, Legal, provider and institution review |
| ADR-018 — timeout/UNKNOWN does not authorize release or compensation | Planned contract tests; not executed | `decisions/ADR-018.md` §7; `validation/acceptance-test-plan.md` | ACCore/API/Operations approval; query, expiry and callback contract required |
| ADR-019 — `OrderConfirmed` is not a universal financial trigger | Planned contract tests; not executed | `decisions/ADR-019.md` §7 | Institution Finance/Legal approval; accounting trigger remains policy-selected |
| ADR-020 — diagram scope and arrow convention | Planned static and human review checks; not executed as an approval | `decisions/ADR-020.md` §7; C1/C2 view artifacts | Architecture owner review; view precedence remains open |
| ADR-021 — interface versioning interim policy | Structural wording present; wire-schema approval not recorded | `decisions/ADR-021.md`; interface contract governance note | API Governance and interface owners |
| ADR-022 — configurable policy registry and no hard-coded thresholds | Planned static, onboarding, and contract tests; not executed | `decisions/ADR-022.md` §7 | Named owner functions plus Operations/Finance/Legal approval of values |
| Provider webhook/reconciliation contract | External gate; not available in repository | `supporting-views/interface-contracts.md` §4; payment adapter/reconciliation specs | Provider, Security, Finance and API approval |
| ACCore reservation query/expiry/callback contract | External gate; not available in repository | `supporting-views/interface-contracts.md` §9; ADR-018 | ACCore/institution/API/Operations approval |
| Platform Settlement/Ledger boundary | Proposed and owner-unassigned | `supporting-views/financial-ledger-and-settlement.md` | Finance, Legal, provider and architecture ownership decision |

## Interpretation rule

`PASS` from structural, registry, reference, depth, or rendering validators means only that the checked artifact structure or syntax satisfied that validator. It must not be converted into `EXECUTED`, `APPROVED`, `PROVIDER-CONTRACTED`, or `PRODUCTION-READY` without a dated reproducible artifact and the applicable owner approval.
