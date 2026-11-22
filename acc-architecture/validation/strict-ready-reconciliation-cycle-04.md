# Strict-ready reconciliation — Cycle 04

**Baseline:** `fb93b00af8b39aa97f2f999b3d1d7273a6376c1c`  
**Scope:** evidence-driven reassessment of all active blockers and hardening of retirement provenance only. No active requirement was promoted, retired, or semantically rewritten.

## Three-lens review

Three independent reviews examined whether any of the 871 active blocker occurrences could be safely closed from existing repository evidence:

- **Standards/domain fit:** close 0. ISO/IEC/IEEE 29148 supports traceability but does not authorize DRAFT-to-ACCEPTED promotion. NIST SP 800-63B-4 and OWASP ASVS support security requirements and testing but cannot substitute for approval or execution evidence.
- **Architecture/traceability:** close 0. Existing function IDs are authoritative registry entries but are not approved Use Case closure evidence. Replacing RGAP-backed `TBD` references with nearby functions would invent traceability. Open contract, policy, and lifecycle gates remain genuine.
- **Adversarial security/testability:** close 0. Structural validators and unit tests do not prove runtime behavior, security, provider contracts, transaction atomicity, or acceptance. The review identified a false-acceptance surface: retirement `evidence_ref` values were required to be non-empty but their file and anchor targets were not resolved.

All reviewers confirmed the current counts: 268 status, 180 unresolved Use Case/function, 200 open-decision, and 223 planned-verification occurrences, overlapping across the 278-row registry. The 10 historical retired rows remain the only rows excluded from active predicates, with provenance preserved.

## Cycle 04 repair

The retirement validator now requires every `evidence_ref` to be a repository-relative existing file. Fragment references must resolve to an explicit HTML anchor or matching heading. A stable `cycle-10-classification-register` anchor was added to the historical atomicity report, and regression coverage now rejects missing files and anchors. Governance now documents this requirement.

This repair strengthens provenance integrity; it does not treat the evidence as approval, implementation, successor acceptance, or runtime verification. All 871 active occurrences remain open.

## Residual gates

The seven live atomicity findings remain `SPLIT_REQUIRED`: `SREQ-PH01-INST-004`, `SREQ-PH01-MSG-002`, `SREQ-PH02-PUB-004`, `SREQ-PH02-REC-004`, `SREQ-PH02-CHK-003`, `SREQ-PH03-CNF-005`, and `SREQ-PH03-PAY-002`; `PAY-002` remains additionally owner-blocked. Formal approval, authoritative Use Case artifacts, concrete contracts, implementation, security evidence, and executed acceptance remain required before any corresponding strict-ready predicates can close.
