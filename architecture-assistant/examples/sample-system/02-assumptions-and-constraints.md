# ParcelFlow — assumptions, constraints and evidence gaps

## Confirmed sample-fixture facts

The fixture defines `SYS-PARCELFLOW`, `ACT-MERCHANT`, `CNT-WEB`, `CNT-API`, `CNT-DB`, and external `EXT-CARRIER`. Its illustrative function `FN-ORDER-001` validates shipment request fields and says malformed requests should be rejected before side effects. These are facts about the example package only; they are not evidence about a deployed product.

## Assumptions and proposals

| ID | Assumption/proposal | Why used for the fixture | Consequence if false | Evidence/owner | Revisit trigger |
|---|---|---|---|---|---|
| `ASM-01` | A merchant operator is the primary sample user. | The sample workflow needs a human actor. | Tenant, role, identity and UX boundaries may change. | `01-scope-and-requirements.md`; appoint product owner. | Discovery of additional actor types or delegated access. |
| `ASM-02` | The API validates input before external booking. | Prevents malformed requests from causing external side effects. | Validation may need carrier-specific rules or asynchronous correction. | `FN-ORDER-001`; confirm carrier contract. | Carrier schema or business rules change. |
| `ASM-03` | Booking outcomes are persisted in `CNT-DB`. | The user-facing status must be retrievable after submission. | Persistence design, consistency and recovery may differ. | `CNT-DB` and sample booking flow; appoint data owner. | Data ownership or retention requirements are known. |
| `ASM-04` | The browser/API and API/carrier examples use HTTPS-style JSON interactions. | A concrete illustrative contract is needed for diagrams. | Protocol, schema, trust boundary, retries and mapping may be different. | Example only; obtain actual API/carrier specifications. | Real provider integration is selected. |
| `ASM-05` | A coarse-grained API with internal modules is preferable to splitting services at this evidence-poor stage. | No independent teams, release cadences or SLOs are evidenced. | Team autonomy or isolation requirements may justify extraction. | `ADR-003` is `PROPOSED`, not accepted. | Evidence of independent deployment/scaling/security boundary and operating readiness. |

## Constraints

No externally imposed legal, regulatory, organizational, technology, cloud, budget, availability, latency, throughput or delivery-date constraint is supplied. The architecture must not invent one. The only current boundary constraint is that carrier internals remain external and are represented through an integration contract. If the real system processes personal addresses or regulated data, the appropriate privacy/security review remains an unresolved prerequisite.

## Decisions not made

The sample does not establish a programming language, framework, cloud/provider, deployment topology, database product/schema, message broker, authentication provider, observability vendor, data residency, or production SLO. `ADR-002` proposes a technology choice for illustration; `ADR-003` proposes a coarse-grained style based on missing evidence. Neither is a stakeholder-approved implementation decision.

## Required evidence before implementation readiness

1. Product-approved field and lifecycle rules, including units, supported parcel classes, cancellation/correction and terminal states.
2. Carrier API contract: authentication, versioning, idempotency, rate limits, payload, response/errors, timeouts, retryability, label retrieval and support/escalation.
3. Identity and tenancy model: actors, permissions, ownership, audit and service-to-service trust.
4. Data classification, retention/deletion, encryption, residency, backup/restore and recovery objectives.
5. Workload and quality targets: average/peak requests, burst behavior, latency/availability, SLI/SLO, RTO/RPO and cost envelope.
6. Operational model: accountable team, deployment/on-call, alert/runbook, rollback, incident response and test environments.

These items are not silently waived. They remain open discovery actions with `OWNER_UNASSIGNED` until the project appoints accountable owners. Any decision that depends on them must remain `PROPOSED`, conditional or blocked as appropriate.
