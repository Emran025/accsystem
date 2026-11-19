# Container Diagram (C2) — ParcelFlow

Scope: ParcelFlow software system. Technology labels are proposals from sample ADRs, not accepted production decisions. Audience: developers and operations.

```mermaid
flowchart LR
 U["Person: ACT-MERCHANT<br/>Merchant operator"] -->|uses over HTTPS| W["Container: CNT-WEB Merchant Web<br/>Browser SPA; TypeScript proposed"]
 W -->|HTTPS / JSON| A["Container: CNT-API Shipment API<br/>Service; Python proposed"]
 A -->|SQL / driver protocol TBD| D[("Container: CNT-DB Parcel Store<br/>Data store; PostgreSQL proposed")]
 A -->|HTTPS; carrier contract TBD| X["External software system: EXT-CARRIER<br/>Carrier API"]
```

## Diagram key

- Rectangle = application/service container; cylinder = data-store container; external system and person are supporting elements.
- Arrow = one-way interaction; the label names protocol/technology where known. “Proposed” and “TBD” are not confirmed facts.
