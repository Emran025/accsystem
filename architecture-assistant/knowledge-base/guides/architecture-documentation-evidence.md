# Evidence and architecture documentation guide

Treat source code, approved requirements and accepted ADRs as distinct evidence classes. For every claim, record its origin and confidence. A retrieved chunk is evidence only of its cited source text; retrieval rank is not an approval signal or proof of completeness. Inspect the full source where context matters.

## Architecture vocabulary

- **System boundary:** explicit inclusion/exclusion and ownership statement.
- **C1 context:** system of interest, human actors and external systems, with important interactions.
- **C2 container:** independently executable/deployable application/service or data store; not necessarily a Docker container.
- **C3 component:** coherent logical responsibility inside an applicable software container.
- **C4 code view:** meaningful code structures and their relationships; not a catalog of every trivial method.
- **Function contract:** explicit behavior for important business operations, including inputs, outputs, rules, effects and failures.
- **ADR:** a decision record with status, alternatives, rationale, trade-offs, consequences and affected IDs.
- **Decomposition exception:** explicit reason, scope, replacement evidence and approval; never an implicit omission.

## Source discipline

Keep user statements, repository evidence, assumptions, proposals and decisions separate. Do not invent third-party internals or undocumented requirements. If evidence is absent, record the unknown, describe its impact and ask a focused question. Consult project-specific decisions and current registry before reusing general guidance.