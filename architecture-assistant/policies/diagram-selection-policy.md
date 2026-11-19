# Diagram Selection and Coverage Policy

## Objective

Analyze the whole stated system scope without producing diagrams merely to satisfy a level count. The assistant must inventory all in-scope systems, containers and known boundaries, then select views that answer a named stakeholder question. A diagram not selected is not a forgotten diagram: its applicability and reason are recorded in the diagram plan.

C4 has four static-structure views—system context, container, component and code—and three supporting views—system landscape, dynamic and deployment. C4 is notation/tool independent. Apply the repository's supported notation, preserve stable registry IDs, and follow the selected renderer's syntax.

## Priority tiers

### Essential baseline

For each software system in scope, produce:

- A scoped system-context view (C1) with the system of interest, directly connected people and external software systems, and important interactions.
- A container view (C2) of the software system showing applications and data stores, responsibilities, major technologies and labeled communication protocols.
- A diagram-selection plan that records every official C4 view and relevant non-C4 view as `REQUIRED`, `SELECTED`, `CONDITIONAL`, `NOT_SELECTED` or `UNRESOLVED`, with rationale, evidence/source, owner/audience and status.
- A complete structured inventory and traceability map. Diagrams are views of that inventory, not substitutes for it.

For a portfolio or enterprise scope containing multiple systems, create a system-landscape view as part of the baseline. Also create one context view per focal system where system-level boundaries differ.

### Conditional, chosen by evidence

Produce these when they answer a real question or address evidenced complexity/risk; otherwise record a short reason for not producing them:

- **Component (C3):** select containers with complex or business-critical internals, unclear responsibilities, multiple teams, important integration/security boundaries, or a need for implementation planning. For very large systems, prioritize high-risk/high-change containers first, then disclose remaining coverage and phase plan. Do not imply the detailed views are exhaustive if they are not.
- **Deployment:** produce one view per relevant environment when infrastructure, network/trust boundaries, scaling, availability, disaster recovery, deployment, or operations are in scope. A production deployment view is usually important when production topology is known. Do not invent nodes or topology.
- **Dynamic:** select specific use cases where interactions are non-obvious or safety/business critical, such as multi-service orchestration, asynchronous choreography, retries, idempotency, compensations, or failure recovery. Name the use case and scope. Do not draw a sequence for every operation.
- **System landscape:** use for a collection of systems/enterprise/department scope, shared platforms, or ecosystem dependencies that cannot be understood in one system-context view.

### Optional, focused detail

- **Code (C4):** create only for important/complex components where code-level structure is known and useful for design/review. Keep it focused on code elements that tell the relevant story; prefer generated/on-demand views for routine code. A function contract/catalog is useful but is not itself a C4 code diagram.
- Additional concern-specific views (e.g. data lifecycle, trust boundaries/threat model, event catalog, resilience, sequence or state views) are not automatically C4 diagrams. Add them when a requirement, risk, or decision needs them; link them to stable IDs and state the specific question they answer.

## Required diagram quality checks

Every diagram must stand alone sufficiently for its intended audience and include:

- A title that names diagram type and scope; an explicit system/container/component/environment boundary where relevant.
- A legend/key for shapes, colors, line styles and abbreviations used.
- Explicit type and concise responsibility for each element. C2/C3 elements state their technology when known; unknown/proposed choices are labeled as such. C1 avoids low-level protocols/technology unless essential to explain the context.
- Unidirectional, labeled relationships whose labels describe intent/data; container-to-container links state protocol/technology when known.
- Stable IDs that match the registry, correct direction and boundaries, and links to detailed records.
- A renderer/parser check where available. If not run, record `NOT_VERIFIED`; never report visual or syntactic correctness based only on regex/ID checks.

## Selection algorithm

1. Establish the user's decision goal, system/portfolio scope, audiences and known source evidence.
2. Create the diagram plan before drawing. Evaluate all seven C4 views plus relevant concern views; set priority and applicability with reasons and evidence.
3. Create essential baseline views first. On large scopes, partition by system/domain/container and provide a landscape or index/overview so no partition is mistaken for the whole.
4. Select conditional/optional views by complexity, criticality, uncertainty, change coupling, cross-boundary interactions and the stakeholder question—not by arbitrary element-count thresholds.
5. Keep registries authoritative. Reconcile every included node/edge with IDs and evidence; explicitly mark unknowns and excluded scope.
6. Validate syntax/rendering when possible, then inspect the rendered view for readability and compare it with the records. Re-open affected selections and gates after material architecture changes.

## Large-system completeness

A large system needs layered navigation, not one unreadable diagram. Maintain a portfolio/system map, per-system contexts and container inventories, and focused deeper diagrams for selected high-value areas. Report which areas are fully analyzed, partially analyzed, unresolved or deferred, with rationale, evidence gaps, owner and next action. Never call a phased/representative view complete, and never let a high coverage percentage hide named omissions.
