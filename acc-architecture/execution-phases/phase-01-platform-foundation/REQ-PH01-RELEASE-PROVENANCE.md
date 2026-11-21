# REQ-PH01-RELEASE-PROVENANCE — Release integrity and ACCore provenance

**Document ID:** REQ-PH01-RELEASE-PROVENANCE  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-RELEASE-PROVENANCE |
| Phase ID | PH-01 |
| Title | Release integrity and ACCore provenance |
| Statement | Platform software releases are published as Available only after digest, signature and applicable provenance verification, and deployed ACCore fingerprint mismatches are reported and audited. |
| Actors | ACT-PLATFORM-ADMIN, ACT-INST-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACCORE |
| Primary C4 containers | CNT-ACC-SOFTCAT, CNT-ACC-AUDIT, CNT-ACR-CONNECTOR, CNT-ACC-INTEGRATION |
| Related function/use case | TBD (RGAP-PH01-008) |
| Status | DRAFT |
| Evidence | NFR-008; CON-010; FR-007 AC1/AC3; ADR-015; deployment-view.md §5; acceptance-test-plan.md item 10; scope-and-requirements.md §8 step 1 |

## 2. Scope boundary and phase handoffs

- Software catalog and release distribution (FR-007) is distinct from the marketplace product catalog (PH-02).
- Owner gate (RGAP-PH01-011): FR-007 steps for public portal display, visitor download-link issuance, signed time-limited URLs and withdrawn-release link disablement have no phase placement in execution-phases/README.md. They are NOT placed in PH-01 or PH-02 here; they involve CNT-ACM-PUBLIC, EXT-PACKAGE-CDN, IF-ACC-SOFTDL and IC-009. Placement requires an owner decision.
- Only integrity/provenance verification, release record content and fingerprint reporting are placed in PH-01, supported by roadmap step 1 and ADR-015.

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-REL-001 | REQ-PH01-RELEASE-PROVENANCE | A release cannot be marked Available unless its SHA-256 digest, signature and required provenance attestation verify, and a failure is recorded with its reason. | A release is submitted for publication. | Only fully verified releases become Available. | SYS-ACCSYSTEM | CNT-ACC-SOFTCAT, CNT-ACC-AUDIT | AC-PH01-REL-001-01, AC-PH01-REL-001-02 | TEST (planned): publish workflow verification test | DRAFT | RP-16 |
| SREQ-PH01-REL-002 | REQ-PH01-RELEASE-PROVENANCE | Each release record holds version, channel, checksum and signature reference plus provenance fields (release ID, source revision, builder identity, build timestamp, dependency/SBOM reference, artifact digest). | A release record is created. | Required fields are present. | SYS-ACCSYSTEM | CNT-ACC-SOFTCAT | AC-PH01-REL-002-01 | TEST (planned): record schema test | DRAFT | none recorded |
| SREQ-PH01-REL-003 | REQ-PH01-RELEASE-PROVENANCE | ACCore reports its deployed release, source/build and configuration fingerprints through a signed status exchange, and a mismatch produces a platform notification and an audit event. | ACCore reports or a mismatch is detected. | Notification and audit event exist. | SYS-ACCORE, SYS-ACCSYSTEM | CNT-ACR-CONNECTOR, CNT-ACC-INTEGRATION, CNT-ACC-AUDIT | AC-PH01-REL-003-01 | TEST (planned): mismatch alert test | DRAFT | ADR-015-GATE, RP-16 |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-REL-001 | Verification before Available | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-008) | NFR-008; FR-007 AC3; CON-010 |
| SREQ-PH01-REL-002 | Release record content | ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-008) | FR-007 AC1; deployment-view §5 |
| SREQ-PH01-REL-003 | Fingerprint reporting and mismatch | ACT-INST-ADMIN | TBD (RGAP-PH01-008) | ADR-015; deployment-view §5 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-REL-001-01 | SREQ-PH01-REL-001 | Failed digest, signature or provenance verification leaves the release non-Available and recorded. | RGAP-PH01-008 | acceptance-test-plan.md item 10 | NFR-008; FR-007 AC3; CON-010 |
| AC-PH01-REL-001-02 | SREQ-PH01-REL-001 | Every Available release has verified checksum and signature on record. | RGAP-PH01-008 | NFR-008 | NFR-008; FR-007 AC3; CON-010 |
| AC-PH01-REL-002-01 | SREQ-PH01-REL-002 | A record lacking a required field is rejected. | RGAP-PH01-008 | FR-007 AC1; deployment-view §5 | FR-007 AC1; deployment-view §5 |
| AC-PH01-REL-003-01 | SREQ-PH01-REL-003 | A mismatch raises an auditable notification; the institution response is policy-gated, not assumed. | RGAP-PH01-008 | deployment-view §5; ADR-015 | ADR-015; deployment-view §5 |

## 5. Alternate paths, failure, exception and uncertainty handling

- A SHA-256 digest alone does not prove source integrity; provenance attestation is required by the source.
- Integrity check failure: release is not published; platform team alerted.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| RP-16 | Institutional auth mode, executable API/event schemas, key lifecycle and replay tests not ratified. | SREQ-PH01-REL-001, SREQ-PH01-REL-003 |
| ADR-015-GATE | ADR-015 per-institution auth mode, connectivity mode and release trust are proposed baselines pending owner/security approval. | SREQ-PH01-REL-003 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-008 | No function spec or interface for release-provenance verification or the signed fingerprint health/status exchange (IF-ACC-SOFTDL §7.5 covers only download integrity). | Recorded here; deployment-view.md §5 and ADR-015 are the only sources. |

## 7. Traceability sources

- 01-scope/scope-and-requirements.md FR-007, NFR-008
- decisions/ADR-015.md
- supporting-views/deployment-view.md §5
- validation/acceptance-test-plan.md item 10

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
