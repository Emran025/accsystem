# Architecture Style and Microservices Decision Policy

## Purpose

Choose the architecture style that fits evidenced business, domain, team and operational constraints. System size, anticipated growth, technology fashion or a request to “scale later” is not, by itself, proof that microservices are appropriate. The recommendation is an ADR proposal; only the user/stakeholders can accept it.

## Required analysis before recommending a style

Inspect available requirements, code, ownership, deployment and operations evidence. Do not pause for answers: record decision-critical questions as `UNRESOLVED` follow-up items with an owner where identifiable, and continue with a conditional recommendation. Record each finding as `CONFIRMED`, `ASSUMPTION`, `PROPOSAL` or `UNRESOLVED`, including source/owner and impact. Assess, without inventing numeric thresholds:

### Business and domain drivers

- Are there stable, well-understood bounded contexts or business capabilities with high cohesion and explicit interfaces?
- Do capabilities change at different rates, require genuinely independent releases, or have separate product/service ownership?
- Is there a demonstrated need for independent scaling, availability, security, data residency, regulatory isolation, or technology choice?
- Are domain rules/data ownership sufficiently separable? Do workflows require cross-boundary transactions or strict immediate consistency?

### Team and delivery drivers

- Can small, persistent teams own services end to end, including deployment, support and lifecycle?
- Is independent deployment a real constraint/benefit, or can modular boundaries and team autonomy be achieved within a single deployable?
- Are API contracts, compatibility/versioning, CI/CD, automated testing and environment provisioning mature enough to support many deployables?

### Operations and distributed-systems readiness

Check the existence and maturity of:

- Automated repeatable builds, deployments, rollback and configuration/secret management.
- Centralized, correlated logs, metrics, distributed tracing, alerting, service-level objectives and ownership/on-call.
- Service discovery, identity/access controls, network security, certificate/key rotation and policy enforcement.
- Resilience patterns for timeouts, retries, idempotency, backpressure, circuit breaking, partial failure and recovery.
- Contract, integration, end-to-end and failure-mode testing; local/developer test environments; dependency management.
- Data ownership per service, schema evolution, eventual consistency acceptance, event delivery guarantees, idempotent consumers, sagas/compensation and reconciliation where relevant.
- Platform/tooling and staffing to operate the expected number of services. Do not recommend an orchestrator or service mesh merely because microservices are considered.

For each area state `READY`, `GAP`, `UNKNOWN` or `NOT_APPLICABLE`, cite evidence, and explain implications. A critical `UNKNOWN` must lower confidence and trigger a question or conditional recommendation.

## Compare at least these options

1. **Modular monolith:** one deployable with explicit internal modules, dependency rules and data ownership boundaries. Usually the simpler option when independent deployment/scaling is not evidenced or boundaries are still being learned.
2. **Service-based architecture:** a small number of coarser independently deployed services organized around strong capability or trust boundaries. Evaluate when some deployment/security/scaling separation is real but very fine-grained microservices are not justified.
3. **Microservices:** multiple independently deployable services, each aligned to a cohesive business capability/bounded context, with explicit API/event contracts and owned data. Justify the number and boundary of services individually; avoid splitting by technical layer or CRUD entity.
4. **Other relevant styles:** event-driven, client-server, modular/layered, serverless or hybrid only when requirements support them. Do not force every design into the monolith-versus-microservices binary.

Compare each option on deployment autonomy, domain fit, scaling/failure isolation, consistency/data ownership, team topology, delivery/testing, security/regulatory needs, latency/network effects, operations burden, cost, migration risk and reversibility. Describe both benefits and costs; avoid arbitrary weighted scores that hide missing evidence.

## Decision rule

Recommend microservices only when the project has specific evidenced benefits that materially outweigh distributed-system and operating costs, the service boundaries are cohesive and independently owned, and critical operating capabilities are ready or an explicitly accepted enablement plan closes the gaps before production. If the case is mixed or key boundaries/readiness are unknown, prefer a modular monolith or coarse-grained services as the lower-complexity proposal, and state what evidence would change the recommendation. A large/complex system can still contain a well-modularized monolith; a small system can need separately isolated services for a demonstrated hard constraint.

The decision output must include: preferred option and status (`PROPOSED`/`ACCEPTED`), alternatives, evidence and assumptions, confidence (`HIGH`/`MEDIUM`/`LOW`) with explanation, major consequences, unresolved questions, readiness gaps and owners, affected stable IDs, migration/reversibility path, and reconsideration triggers. Never turn an unaccepted recommendation into a confirmed architecture fact.

## If microservices are proposed

Before treating the target architecture as actionable, provide:

- A capability/bounded-context map with proposed service owner, responsibility, explicit in/out scope and boundary evidence.
- Per-service data ownership and rules for avoiding shared writable databases/schemas.
- Synchronous/asynchronous interaction contracts, consistency model, failure handling, idempotency and observability requirements for critical workflows.
- Independent build/deploy/release/rollback, version compatibility, security identity/trust, production operations and cost model.
- A migration sequence where applicable, with a safe first extraction and measurable outcome; preserve an incremental path and avoid decomposing all legacy code at once.
- A deployment view for each relevant target environment and dynamic views for critical cross-service flows where they materially clarify behavior.

If these cannot be evidenced, label them unresolved and do not present the proposed microservice map as implementation-ready.

## ADR evidence base

This policy follows the trade-off framing that microservices offer independent deployment, strong module boundaries and team autonomy but introduce distribution, eventual-consistency and operational complexity. It also considers Microsoft's guidance on bounded contexts, service-owned data, end-to-end operations, testing, latency and consistency.

References:
- Martin Fowler, Microservices Guide: https://martinfowler.com/microservices/
- Martin Fowler, Microservice Prerequisites: https://martinfowler.com/bliki/MicroservicePrerequisites.html
- Microsoft Azure Architecture Center, Microservices architecture style: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices
