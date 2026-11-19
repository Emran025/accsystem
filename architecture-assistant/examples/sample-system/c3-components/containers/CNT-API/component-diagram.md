# Component Diagram (C3) — CNT-API Shipment API

Scope: components inside the API container; connected data store and external carrier are supporting elements. Technology: API runtime is proposed Python; component-level implementation choices are unresolved. Audience: architects and developers.

```mermaid
flowchart LR
 V["Component: CMP-API-VALIDATION<br/>Validates and normalizes requests"] -->|valid request / field errors| B["Component: CMP-API-BOOKING<br/>Coordinates booking and workflow state"]
 B -->|reads/writes shipment state| R["Component: CMP-API-REPOSITORY<br/>Owns persistence boundary"]
 B -->|booking request / result| X["External software system: EXT-CARRIER<br/>Carrier API"]
 R -->|SQL; schema details TBD| D[("Data-store container: CNT-DB<br/>Parcel Store")]
```

## Diagram key

- Component = logical responsibility inside CNT-API; technology is unspecified at this detail level.
- External software system and data-store container are supporting elements outside the component scope.
- Arrows represent one-way calls/data flow as labeled; protocol details not evidenced remain TBD.
