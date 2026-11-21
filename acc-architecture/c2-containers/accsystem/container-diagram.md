# ACCSystem Container Diagram — Canonical View Reference
**Viewpoint:** C2 — ACCSystem Platform internal containers and their primary relationships
**Canonical diagram:** [ACCSystem C2 container view](../../c1-context/landscape.md)
**Audience:** Architects and developers

> [!NOTE]
> The canonical C2 diagram is retained at the existing `c1-context/landscape.md` path to match the repository's current organization. This file remains as the C2 entry point under `c2-containers/accsystem/` and must not define a competing container graph.

> [!NOTE]
> The C1 black-box context view, with ACCSystem beside its actors and external systems, is embedded in [`c1-context/systems/SYS-ACCSYSTEM.md`](../../c1-context/systems/SYS-ACCSYSTEM.md).

## Scope and conventions
- The canonical C2 view shows the 17 registered ACCSystem containers inside the `SYS-ACCSYSTEM` boundary.
- Selected clients and external systems are shown only to make container entry/exit relationships readable; they do not turn the C2 view into a C1 context diagram.
- Arrows show the control/data-flow initiator direction. Responses, callbacks, and events are shown only when explicitly labelled.
- Individual `CNT-*` files remain authoritative for each container's detailed responsibility and collaborator record.
