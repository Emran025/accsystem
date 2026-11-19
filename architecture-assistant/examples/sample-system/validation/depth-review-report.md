# Artifact-depth outline review

Overall: **BLOCKED_FOR_CONTENT_REVIEW**

This heuristic checks visible topic coverage and common unresolved placeholders only. It does not judge whether claims are correct, sufficiently specific, evidence-backed, internally consistent, secure, or implementation-ready. A structurally present outline always requires expert semantic review.

Documents reviewed: 19; incomplete outlines: 14; registry/path findings: 0.

| Level | IDs | Document | Outline status | Missing topics | Placeholder markers |
|---|---|---|---|---|---|
| C2 | CNT-API | `c2-containers/containers/CNT-API.md` | STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW | None | None |
| C2 | CNT-DB | `c2-containers/containers/CNT-DB.md` | INCOMPLETE_OUTLINE | explicit boundary/non-responsibilities, interfaces and dependencies, security/trust, operations/reliability, failure behavior, open risks/owner/action | None |
| C2 | CNT-WEB | `c2-containers/containers/CNT-WEB.md` | INCOMPLETE_OUTLINE | explicit boundary/non-responsibilities, interfaces and dependencies, open risks/owner/action | None |
| C3 | CMP-API-BOOKING | `c3-components/containers/CNT-API/components/CMP-API-BOOKING.md` | INCOMPLETE_OUTLINE | interfaces/collaborators, behavior/rules/state, failure/security/operations, verification/tests, unknowns/traceability | None |
| C3 | CMP-API-REPOSITORY | `c3-components/containers/CNT-API/components/CMP-API-REPOSITORY.md` | INCOMPLETE_OUTLINE | interfaces/collaborators, behavior/rules/state, failure/security/operations, verification/tests, unknowns/traceability | None |
| C3 | CMP-API-VALIDATION | `c3-components/containers/CNT-API/components/CMP-API-VALIDATION.md` | INCOMPLETE_OUTLINE | interfaces/collaborators, behavior/rules/state, failure/security/operations, verification/tests, unknowns/traceability | None |
| C3 | CMP-WEB-FORM | `c3-components/containers/CNT-WEB/components/CMP-WEB-FORM.md` | INCOMPLETE_OUTLINE | interfaces/collaborators, behavior/rules/state, failure/security/operations, verification/tests, unknowns/traceability | None |
| C3 | CMP-WEB-STATUS | `c3-components/containers/CNT-WEB/components/CMP-WEB-STATUS.md` | INCOMPLETE_OUTLINE | interfaces/collaborators, data and side effects, failure/security/operations, verification/tests, unknowns/traceability | None |
| C4 | CODE-API-ORCHESTRATOR | `c4-code/modules/booking-service.md` | INCOMPLETE_OUTLINE | responsibility and behavior, interfaces and dependencies, failure/security considerations, tests/verification, unknowns and related IDs | None |
| C4 | CODE-WEB-STATUS | `c4-code/modules/booking-status.md` | INCOMPLETE_OUTLINE | responsibility and behavior, interfaces and dependencies, data/state/side effects, tests/verification, unknowns and related IDs | None |
| C4 | CODE-WEB-FORM | `c4-code/modules/shipment-form.md` | INCOMPLETE_OUTLINE | responsibility and behavior, failure/security considerations, tests/verification, unknowns and related IDs | None |
| C4 | CODE-API-REPO | `c4-code/modules/shipment-repository.md` | INCOMPLETE_OUTLINE | responsibility and behavior, interfaces and dependencies, failure/security considerations, tests/verification, unknowns and related IDs | None |
| C4 | CODE-API-VALIDATOR | `c4-code/modules/shipment-validator.md` | INCOMPLETE_OUTLINE | responsibility and behavior, interfaces and dependencies, data/state/side effects, tests/verification, unknowns and related IDs | None |
| DECISION | ADR-001 | `decisions/adr/ADR-001.md` | STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW | None | None |
| DECISION | ADR-002 | `decisions/adr/ADR-002.md` | STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW | None | None |
| DECISION | ADR-003 | `decisions/adr/ADR-003.md` | STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW | None | None |
| FUNCTION | FN-ORDER-001 | `functions/specifications/FN-ORDER-001.md` | STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW | None | None |
| FUNCTION | FN-ORDER-002 | `functions/specifications/FN-ORDER-002.md` | INCOMPLETE_OUTLINE | processing and normal/alternate behavior | None |
| INTERFACE | IF-CARRIER-001 | `interfaces/integrations/carrier-booking.md` | INCOMPLETE_OUTLINE | compatibility/delivery semantics, tests/monitoring/unknowns | None |

## Required next step

Expand each incomplete artifact using its family template. For genuinely unknown topics, record the unknown, impact, evidence/action, accountable owner or assignment action, and revisit trigger; do not add filler. Reconcile requirements, assumptions, decisions, interfaces, diagrams, deployment and open issues. This report is not a substitute for the final semantic/consistency audit.
