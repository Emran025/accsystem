# C1 — System Context views

## First view: ACCSystem as one black-box system

Start with the canonical [ACCSystem C1 System Context](context-diagram.md). It shows ACCSystem as a single system, with its people, client systems, and external providers. It contains no internal containers or components.

The source record for its system boundary, actors, external systems, and C2 inventory is [`systems/SYS-ACCSYSTEM.md`](systems/SYS-ACCSYSTEM.md). The canonical C2 view is now [`../c2-containers/accsystem/container-diagram.md`](../c2-containers/accsystem/container-diagram.md).

## Other ecosystem context views

The remaining registry-derived system contexts are collected in [`c4-context-and-container-overlays.md`](c4-context-and-container-overlays.md): `SYS-ACCECOSYSTEM`, `SYS-ACCORE`, `SYS-ACCOMMERCE`, `SYS-ACMANAGEMENT`, `SYS-ACCMARED-SUP`, and `SYS-ACCMARED-COU`. The ACCSystem section in that file links back to the canonical diagram above rather than maintaining a competing copy.

## C1/C2 boundary

C1 shows one software system with people and directly interacting systems. C2 opens that system boundary to show its applications/data stores and their relationships. For ACCSystem, the canonical C2 graph is maintained only in the C2 file linked above; registry-derived overlays are explicitly cross-checks, not competing authoritative graphs.
