# System Context (C1) — ParcelFlow

Scope: one software system and directly connected people/external systems. Audience: business and technical stakeholders. Relationship labels show business intent, not protocol details.

```mermaid
flowchart LR
 M["Person: ACT-MERCHANT<br/>Merchant operator"] -->|creates shipment| S["Software system: SYS-PARCELFLOW<br/>ParcelFlow — creates and tracks shipments"]
 S -->|requests booking and label| X["External software system: EXT-CARRIER<br/>Carrier service — books and returns label"]
```

## Diagram key

- Person = a human role interacting with the in-scope software system.
- Software system = ParcelFlow, the system of interest.
- External software system = a dependency outside ParcelFlow ownership.
- Arrow = one-way business interaction in the arrow direction.
