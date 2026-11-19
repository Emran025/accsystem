# Skill: architecture-style

Purpose: make a defensible architecture-style recommendation for complex systems without defaulting to microservices.

## Procedure

1. Read `policies/architecture-style-selection.md`. Gather evidence for domain/bounded contexts, change/deployment/scaling needs, teams/ownership, data consistency, security/regulatory constraints, delivery automation, observability, testing and operational readiness.
2. Do not stop to ask questions. Record decision-critical gaps as `UNKNOWN`/`UNRESOLVED`, explain confidence impact and what evidence would resolve them, and continue with a conditional recommendation.
3. Compare modular monolith, coarse-grained/service-based architecture and microservices; add another style only when evidenced. Evaluate boundary cohesion, independent release/scale, data ownership, team autonomy, network/latency/failure, consistency, testing, security, operating burden and cost. Avoid arbitrary score thresholds.
4. Recommend microservices only when concrete independent benefits outweigh distributed-system/operations costs and boundaries are cohesive and operable. If boundaries or readiness are uncertain, prefer a lower-complexity proposal and name the evidence/triggers that would change it. System size alone never qualifies.
5. Write the architecture-style ADR as `PROPOSED`, with evidence, alternatives, readiness gaps, risks, confidence, affected IDs, migration/reversibility and reconsideration triggers. Do not claim user acceptance.
6. If microservices are proposed, describe service ownership/domain/data boundaries and key API/event/failure/consistency contracts. Add the deployment and dynamic views the diagram plan selects. Leave unresolved items unresolved; do not call it implementation-ready until critical contracts and operations are addressed.

## Required output

State recommended style and ADR status, alternatives, evidence/source IDs, unknowns/readiness gaps, confidence, selected diagrams, affected IDs, next decision and gate status.
