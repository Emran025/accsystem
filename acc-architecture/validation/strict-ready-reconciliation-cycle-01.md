# Strict-ready reconciliation — Cycle 01

**Baseline:** `aba3562cd4690e3011e383d1c2aa4f5f75fd45e6`
**Scope:** `acc-architecture/` only; PH-01 through PH-04; no application code and no PH-05 requirements.
**Decision:** The package remains **not ready**. This cycle closes only a validator/governance defect for historical `RETIRED` rows; it does not promote active requirements or claim implementation, approval, security, or production evidence.

## Baseline blocker reconciliation

The exact pre-edit validator output contains **908 occurrence records** across **278 registry rows**. The categories are: status **278**, Use Case placeholder **188**, open decision **209**, and planned verification **233**. These overlap and therefore are not distinct row counts. The complete occurrence ledger is [`strict-ready-blocker-ledger-cycle-01.csv`](strict-ready-blocker-ledger-cycle-01.csv).

There are 10 historical `RETIRED` rows. Their status, placeholder, open-decision, and planned-verification values are preserved as historical source data. They are not active delivery obligations and are therefore excluded from active strict-ready predicates after this cycle's validator/governance repair. All structural/reference/document checks still apply. Active `DRAFT`, `PROPOSED`, and `OWNER_REVIEW` rows remain fail-closed.

## Three-lens peer review

### Standards and domain fit

ISO/IEC/IEEE 29148:2018 supports lifecycle requirements management, requirement quality, and traceability; it does not authorize changing a draft to accepted without evidence or approval. NIST SP 800-63B-4 is relevant to authentication and authenticator lifecycle requirements, but it cannot substitute for this system's security decision or execution evidence. OWASP ASVS 5.0.0 supports versioned security verification, trusted-layer authorization, and cross-tenant controls; it does not turn a structural registry pass into a security result. The standards evidence is recorded in [`strict-ready-standards-research.md`](strict-ready-standards-research.md).

The domain review found no active blocker that can be honestly closed by a documentation-only delegated decision. `SREQ-PH03-PAY-002` remains owner-blocked by provider and financial policy questions. Credential mode/protection (`INST-004`), message semantics (`MSG-002`), publication/recovery contracts (`PUB-004`/`REC-004`), checkout snapshots (`CHK-003`), and recipient projection/recovery (`CNF-005`) remain open.

### Architecture and traceability

The current registry contains 45 main rows and 233 SREQ rows: PH-01 **113**, PH-02 **56**, PH-03 **74**, and PH-04 **35**. The 188 `TBD` Use Case values are RGAP-backed traceability gaps, not malformed references. They must not be replaced with guessed function IDs. The seven live atomicity findings remain distinct; the ten retired source rows remain retained historical records. No duplicate was confirmed and no requirement was deleted or merged in this cycle.

### Adversarial security and testability

The repository contains documentation and validators, not ACCSystem/ACCore runtime implementations or provider integrations. The 9 execution-phase tests and 65 architecture-assistant tests validate tooling and structural behavior; they do not prove tenant isolation, webhook replay resistance, payment safety, delivery behavior, or functional acceptance. All 233 SREQ verification references were planned at baseline. No active row may be closed on the basis of a planned test, a structural validator result, or a stale implementation report.

The main counterargument was that delegated authority should allow routine choices such as OAuth versus mTLS, checkout TTL, idempotency scope, or payment allocation policy to be selected locally. The reviewers rejected that closure because the repository still links those choices to external contracts, security/Finance/Legal gates, or missing Use Cases; choosing one would fabricate authority and alter behavior. A second counterargument was that `RETIRED` must remain a strict-ready failure because it is not `ACCEPTED`. The resolved disagreement is that `RETIRED` remains non-accepted and structurally checked, but is excluded from active readiness predicates because governance defines it as historical source provenance; no active status gate was weakened.

## Repair applied

The validator now applies active strict-ready predicates only when `status != RETIRED`. This is a semantics correction justified by the governance lifecycle definition, not a readiness bypass. The regression suite adds a test proving that retired rows remain structurally checked but do not emit active strict-ready errors, while an active draft still does. The post-repair strict-ready run is still **FAIL, 871 errors**: 268 active status gates, 180 active Use Case placeholders, 200 active open-decision occurrences, and 223 active planned-verification occurrences.

No registry row, source requirement statement, acceptance criterion, Use Case ID, ADR status, owner decision, contract, or verification result was fabricated or promoted.

## Residual exceptions and narrow owner actions

After the lifecycle repair, active rows still require: authoritative Use Case/function artifacts for 180 placeholder occurrences; resolution of 200 active open-decision occurrences; executable, truthful verification results for 223 active planned references; and `ACCEPTED` status with corresponding approval/evidence for 268 active rows. The narrowest next actions are to obtain the seven live contract/decision packages, complete the RGAP Use Case artifacts (especially PH-04), execute scoped acceptance tests with retained evidence, and then update each Markdown/CSV row atomically. `PAY-002` additionally requires provider and Finance/Legal/institution decisions; no local documentation choice can close it.

## References

[1]: https://standards.ieee.org/standard/29148-2018.html "IEEE SA - IEEE/ISO/IEC 29148-2018"
[2]: https://csrc.nist.gov/pubs/sp/800/63/b/4/final "NIST SP 800-63B-4 Digital Identity Guidelines"
[3]: https://asvs.owasp.org/ "OWASP Application Security Verification Standard overview"
[4]: https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md "OWASP ASVS 5.0 V8 Authorization"
