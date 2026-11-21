# REQ-PH01-GATEWAY-BOUNDARY — Gateway trust boundary and public/authenticated separation

**Document ID:** REQ-PH01-GATEWAY-BOUNDARY  
**Phase:** PH-01 — Platform Foundation and Trust Boundaries  
**Status:** DRAFT — unapproved requirement draft derived from the supplied `acc-architecture` archive (source `Emran025/accsystem`, `main`, commit `c064615`). Not stakeholder-approved, not implemented, not verified, not production-ready.  
**Governance:** `../requirements-governance.md`; phase boundary: `../README.md` (PROPOSED BASELINE).

> Identifiers `RGAP-*` are package-local gap records created by this draft to document a missing source reference; they are not architecture-registry IDs. All other IDs (`FR-*`, `NFR-*`, `CON-*`, `ADR-*`, `FN-*`, `IF-*`, `UNKN-*`, `ODEC-*`, `IC-*`, `RP-*`, `LIC-*`, `PUB-*`, `CNT-*`, `SYS-*`, `ACT-*`) are taken from the archive.

## 1. Main requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-PH01-GATEWAY-BOUNDARY |
| Phase ID | PH-01 |
| Title | Gateway trust boundary and public/authenticated separation |
| Statement | All inbound client traffic enters through a single gateway that enforces transport security, token verification, public/authenticated route separation and rate limiting without hosting business logic. |
| Actors | ACT-VISITOR, ACT-PLATFORM-ADMIN |
| Locations | SYS-ACCSYSTEM, SYS-ACMANAGEMENT |
| Primary C4 containers | CNT-ACC-APIGATEWAY, CNT-ACC-IDENTITY, CNT-ACM-ADMIN, CNT-ACC-INTEGRATION |
| Related function/use case | TBD (RGAP-PH01-005) |
| Status | DRAFT |
| Evidence | CNT-ACC-APIGATEWAY; CON-011; security-view §1 |

## 2. Scope boundary and phase handoffs

- Public portal content and software download are not enabled here (see REQ-PH01-RELEASE-PROVENANCE section 2).

## 3. Sub-requirement register

| Sub-requirement ID | Parent requirement ID | Statement | Trigger/precondition | Expected outcome | Locations | C4 containers | Acceptance criteria | Verification | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SREQ-PH01-GW-001 | REQ-PH01-GATEWAY-BOUNDARY | The gateway accepts only TLS-protected inbound connections. | A client connects. | Plaintext is refused. | SYS-ACCSYSTEM | CNT-ACC-APIGATEWAY | AC-PH01-GW-001-01 | TEST (planned): transport test | DRAFT | none recorded |
| SREQ-PH01-GW-002 | REQ-PH01-GATEWAY-BOUNDARY | The gateway verifies each authenticated request with Identity & Access and forwards the validated identity, containing no business rules and making no authorization decisions. | An authenticated request arrives. | Valid identity is forwarded or the request is rejected. | SYS-ACCSYSTEM | CNT-ACC-APIGATEWAY, CNT-ACC-IDENTITY | AC-PH01-GW-002-01 | TEST (planned): gateway routing test | DRAFT | none recorded |
| SREQ-PH01-GW-003 | REQ-PH01-GATEWAY-BOUNDARY | Public-zone routes expose no administrative API and administrative routes are distinct from public paths. | A public request targets an administrative route. | The request is refused. | SYS-ACCSYSTEM, SYS-ACMANAGEMENT | CNT-ACC-APIGATEWAY, CNT-ACM-ADMIN | AC-PH01-GW-003-01 | TEST (planned): route separation and penetration test | DRAFT | none recorded |
| SREQ-PH01-GW-004 | REQ-PH01-GATEWAY-BOUNDARY | Rate limiting applies per client and route class, and per institution for integration traffic, using policy values. | Request volume exceeds the configured limit. | Excess requests are throttled. | SYS-ACCSYSTEM | CNT-ACC-APIGATEWAY, CNT-ACC-INTEGRATION | AC-PH01-GW-004-01 | TEST (planned): rate limit test | DRAFT | ADR-022-GATE |

Related function/use case, actors and evidence per sub-requirement:

| Sub-requirement ID | Title | Actors | Related function/use case | Evidence |
|---|---|---|---|---|
| SREQ-PH01-GW-001 | TLS only | ACT-VISITOR, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CNT-ACC-APIGATEWAY §3 |
| SREQ-PH01-GW-002 | Token verification without business logic | ACT-VISITOR, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CNT-ACC-APIGATEWAY |
| SREQ-PH01-GW-003 | Public/admin route separation | ACT-VISITOR | TBD (RGAP-PH01-005) | CON-011; CNT-ACM-ADMIN §4 |
| SREQ-PH01-GW-004 | Rate limiting | ACT-VISITOR, ACT-PLATFORM-ADMIN | TBD (RGAP-PH01-005) | CNT-ACC-APIGATEWAY §6 |

## 4. Acceptance criteria

| Acceptance criterion | Proves | Criterion | API/event/UI contract reference | Scope/data/state/container reference | Source/evidence |
|---|---|---|---|---|---|
| AC-PH01-GW-001-01 | SREQ-PH01-GW-001 | Non-TLS connections are rejected. | RGAP-PH01-002 | CNT-ACC-APIGATEWAY §3 | CNT-ACC-APIGATEWAY §3 |
| AC-PH01-GW-002-01 | SREQ-PH01-GW-002 | Invalid tokens are rejected before routing; gateway holds no domain data. | RGAP-PH01-002 | CNT-ACC-APIGATEWAY §4, §7 | CNT-ACC-APIGATEWAY |
| AC-PH01-GW-003-01 | SREQ-PH01-GW-003 | Public-zone requests cannot reach admin APIs. | RGAP-PH01-002 | CON-011 | CON-011; CNT-ACM-ADMIN §4 |
| AC-PH01-GW-004-01 | SREQ-PH01-GW-004 | Over-limit requests receive 429; thresholds are policy values, none asserted. | RGAP-PH01-002 | CNT-ACC-APIGATEWAY §6; CMP-INT-GATEWAY §3.3 | CNT-ACC-APIGATEWAY §6 |

## 5. Alternate paths, failure, exception and uncertainty handling

- Gateway overload: rate limiting; backend unavailable: 503; auth service unavailable: reject authenticated, allow public per policy.

## 6. Open decisions and documented gaps

Open decisions below are preserved as the source states them; this draft does not resolve them.

| Decision / gate ID | Source meaning | Affected sub-requirements |
|---|---|---|
| ADR-022-GATE | ADR-022 numeric thresholds are owner-approval-required; no value asserted. | SREQ-PH01-GW-004 |

| Package-local gap | Missing source reference | Where recorded / resolution route |
|---|---|---|
| RGAP-PH01-005 | functions/function-catalog.md registers only seven FN-* functions; none covers the PH-01 behavior of this area. | Recorded in registry column use_case_id as TBD; route: function inventory step of the phase lifecycle (execution-phases/README.md §8). |
| RGAP-PH01-002 | No registered IF-* contract for authentication, token validation, session revocation or role lookup; token format and TTL are UNKNOWN. | Recorded in this document; CNT-ACC-IDENTITY §3/§5. Route: API Governance (IC-002) and Security owner. |

## 7. Traceability sources

- c2-containers/accsystem/CNT-ACC-APIGATEWAY.md
- supporting-views/security-view.md

---
*Draft requirement text. Verification entries describe future evidence; none has been executed for this draft.*
