# ADR-{{NNN}}: Select architecture style for {{system_or_domain}}

Status/date: `PROPOSED` / `ACCEPTED` / `REJECTED` / `SUPERSEDED` · {{date}} · Decision owner: {{owner}}

## Context, goals and scope

Business capabilities/domain boundaries: {{evidence and source IDs}}. System scale/change/team/deployment context: {{evidence}}. Quality attributes and constraints: {{}}. Out-of-scope: {{}}.

## Options compared

| Option | Domain cohesion/boundaries | Independent release/scale need | Data and consistency | Team/ownership fit | Operations readiness/cost | Main risks/trade-offs |
|---|---|---|---|---|---|---|
| Modular monolith | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |
| Coarse-grained/service-based | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |
| Microservices | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |
| Other justified style | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |

## Evidence and readiness

For each area mark `READY`, `GAP`, `UNKNOWN` or `NOT_APPLICABLE`; attach source/owner and impact.

- Bounded contexts, functional cohesion and candidate ownership: {{}}
- Automated CI/CD, independent deployment/rollback and testing: {{}}
- Observability, tracing, SLOs, incident response and service ownership: {{}}
- Service identity, secrets, network/security and governance: {{}}
- Data ownership, consistency, event reliability, idempotency/sagas: {{}}
- Platform/staff/cost capacity and projected operational burden: {{}}

## Decision, confidence and rollout

Preferred option: {{}} · Confidence: `HIGH` / `MEDIUM` / `LOW` because {{}}. Status is proposal until accepted by the decision owner. Explicit benefits expected: {{}}. Costs/risks accepted: {{}}. Readiness gaps, owners and mitigation: {{}}. Migration/reversal plan and first measurable step: {{}}. Reconsider when: {{triggers}}. Questions not resolved: {{}}. Affected stable IDs/ADRs: {{}}.

If microservices are selected, include the per-service responsibility/owner/data/API/event boundary map, service-interaction views, failure/consistency contracts, and deployment/operations plan. Do not mark the style implementation-ready while critical boundaries or readiness items remain unresolved.
