# Strict-ready reconciliation standards research

**Cycle baseline:** `aba3562cd4690e3011e383d1c2aa4f5f75fd45e6`

This report records the standards used to judge whether a current strict-ready blocker is a documentation/governance defect that can be safely repaired in `acc-architecture/`, or a real implementation, approval, or external-contract gate that must remain open. It does not claim conformance or production readiness.

## Requirements lifecycle and traceability

ISO/IEC/IEEE 29148:2018 covers requirements engineering and management throughout the life cycle, defines characteristics of good requirements, and describes iterative requirements processes and information items. The current repository already follows the relevant principle by separating requirements, acceptance criteria, verification references, evidence references, and owner-gated decisions. That standard supports improving traceability and lifecycle semantics; it does **not** authorize changing a draft to accepted without approval or evidence. [1]

**Application to this cycle:** a retired source requirement is not an active implementation requirement merely because it remains in the historical registry. The safe repair is to make the validator and governance explicitly distinguish active rows from retired historical rows, while retaining the retired row and its provenance. Active `DRAFT` and `OWNER_REVIEW` rows remain blocked until the required lifecycle evidence exists.

## Authentication, credential lifecycle, and revocation

NIST SP 800-63B-4, published July 2025, defines technical requirements for authenticator assurance levels and supersedes SP 800-63B. It addresses authentication and authenticator lifecycle management, but is guidance for digital identity systems and does not itself provide this repository's product-owner approval or provider-contract evidence. [2]

**Application to this cycle:** authentication, MFA, token lifetime, refresh rotation, revocation, credential rotation, and fail-closed behavior remain requirements that need concrete design and executed verification. Routine policy choices may be recorded as architecture decisions when delegated, but an architectural decision record is not an implementation result.

## Authorization and multi-tenant security verification

OWASP ASVS 5.0.0 provides a basis for testing web-application technical security controls and recommends version-qualified requirement references. Its authorization chapter calls for documented authorization rules, trusted service-layer enforcement, immediate or mitigated authorization-change effects, and cross-tenant controls preventing operations from affecting unauthorized tenants, including administrative protections. [3] [4]

**Application to this cycle:** tenant isolation, privileged access, cross-tenant denial, and authorization changes must not be closed by replacing planned tests with prose. A verification reference becomes closed only when an executable check, review artifact, or other truthful evidence exists and its result is recorded.

## Safe disposition rule

The standards support four distinct dispositions:

1. **Validator/governance defect:** repair semantics and tests, preserving the gate's intent.
2. **Delegated routine operational decision:** record a bounded decision and rationale without claiming stakeholder approval, legal compliance, implementation, or execution evidence.
3. **Retained external or formal gate:** keep the blocker, link the exact decision/contract/approval gap, and do not fabricate closure.
4. **Executed architecture-scope verification:** only record a pass where the repository contains and runs a check whose scope matches the criterion. Structural validators do not prove runtime behavior.

This cycle uses the first disposition for `RETIRED` rows only. It does not promote active rows, invent Use Cases, close external gates, or convert planned verification into executed evidence.

## References

[1]: https://standards.ieee.org/standard/29148-2018.html "IEEE SA - IEEE/ISO/IEC 29148-2018"
[2]: https://csrc.nist.gov/pubs/sp/800/63/b/4/final "NIST SP 800-63B-4 Digital Identity Guidelines"
[3]: https://asvs.owasp.org/ "OWASP Application Security Verification Standard overview"
[4]: https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md "OWASP ASVS 5.0 V8 Authorization"
