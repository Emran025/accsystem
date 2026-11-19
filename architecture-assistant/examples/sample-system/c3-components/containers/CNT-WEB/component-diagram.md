# Component Diagram (C3) — CNT-WEB Merchant Web

Scope: components inside the browser application; CNT-API is a supporting container. Technology: TypeScript SPA is proposed; framework and component-level implementation are unresolved. Audience: architects and developers.

```mermaid
flowchart LR
 F["Component: CMP-WEB-FORM<br/>Captures shipment input and submits API request"] -->|HTTPS / JSON request| A["Container: CNT-API<br/>Shipment API"]
 A -->|booking state / label response| S["Component: CMP-WEB-STATUS<br/>Renders status and label link"]
```

## Diagram key

- Component = logical responsibility inside CNT-WEB; proposed technology is TypeScript SPA.
- Container = supporting separately running application/service.
- Arrows are one-way interactions; the HTTP contract's exact paths/status codes remain unresolved.
