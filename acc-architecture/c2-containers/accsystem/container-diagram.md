# ACCSystem — Container Diagram
**Viewpoint:** C2 — ACCSystem Platform internal containers and their primary relationships
**Canonical location:** `c2-containers/accsystem/container-diagram.md` — ACCSystem C2 container view.
**Audience:** Architects and developers
**Label convention:** `CONFIRMED` = sourced from idea.md | `ASSUMPTION` = inferred | `UNKNOWN` = open

> [!NOTE]
> **C2 scope:** This is the internal container decomposition of `SYS-ACCSYSTEM`. Selected client and external-system nodes are shown only to make container entry/exit relationships readable; this is not the C1 black-box context view. The C1 black-box context is the separate canonical [`c1-context/context-diagram.md`](../../c1-context/context-diagram.md).

> [!NOTE]
> **Arrow convention:** Arrows show the control/data-flow initiator direction. Responses, callbacks, and events may flow in either direction and are shown only when explicitly labelled. This remains a reversible technical baseline; ADR-020 owner review is required and stakeholder approval has not been recorded.

## Container Diagram
```mermaid
flowchart LR
    ACE["CNT-ACE-MOBILEAPP\nACCommerce App"]
    ACR_COM["CNT-ACR-COMMERCE\nACCore Commerce\nWorkspace"]
    ACM_PUB["CNT-ACM-PUBLIC\nACManagement\nPublic Portal"]
    ACM_ADM["CNT-ACM-ADMIN\nACManagement\nAdmin Console"]
    AMD_SUP["CNT-AMD-SUPERVISOR\nACCMared Supervisor"]
    AMD_COU["CNT-AMD-COURIER\nACCMared Courier"]
    EXT_PAY["EXT-PAYMENT-PROVIDER\nExternal Payment\nProvider"]
    EXT_CDN["EXT-PACKAGE-CDN\nSoftware Package CDN"]
    ACR_CON["CNT-ACR-CONNECTOR\nPlatform Connector\n(ACCore)"]

    subgraph ACCSYSTEM["SYS-ACCSYSTEM — ACCSystem Platform"]
        GW["CNT-ACC-APIGATEWAY\nAPI Gateway / BFF"]
        IDN["CNT-ACC-IDENTITY\nIdentity & Access"]
        REG["CNT-ACC-INSTREG\nInstitution Registry"]
        INT["CNT-ACC-INTEGRATION\nInstitution Integration\nGateway"]
        CAT["CNT-ACC-CATALOG\nCatalog & Publication"]
        SRC["CNT-ACC-SEARCH\nSearch & Discovery"]
        OFF["CNT-ACC-OFFER\nOffer / Price /\nAvailability"]
        CART["CNT-ACC-CART\nCart & Checkout"]
        ORD["CNT-ACC-ORDERS\nOrder Management"]
        PAY["CNT-ACC-PAYMENT\nPayment\nOrchestration"]
        DEL["CNT-ACC-DELIVERY\nDelivery Management"]
        NOT["CNT-ACC-NOTIFICATIONS\nNotifications"]
        AUD["CNT-ACC-AUDIT\nAudit & Observability"]
        SCAT["CNT-ACC-SOFTCAT\nSoftware Catalog &\nRelease Distribution"]
        LIC["CNT-ACC-LICENSE\nLicense & Entitlement\nManagement"]
        PADM["CNT-ACC-PLATFORMADMIN\nPlatform Administration\n& Support"]
        BUS["CNT-ACC-EVENTBUS\nEvent Bus /\nMessage Broker"]
    end

    ACE --> GW
    ACR_COM --> GW
    ACM_PUB --> GW
    ACM_ADM --> GW
    AMD_SUP --> GW
    AMD_COU --> GW
    GW --> IDN
    GW --> CAT
    GW --> SRC
    GW --> CART
    GW --> ORD
    GW --> DEL
    GW --> SCAT
    GW --> LIC
    GW --> PADM
    IDN --> REG
    CART --> OFF
    CART --> ORD
    ORD --> INT
    ORD --> PAY
    ORD --> DEL
    ORD --> BUS
    INT --> CAT
    INT --> REG
    ACR_CON --> INT
    INT --> ACR_CON
    CAT --> SRC
    PAY --> EXT_PAY
    EXT_PAY --> PAY
    DEL --> AMD_SUP
    DEL --> AMD_COU
    SCAT --> EXT_CDN
    PADM --> IDN
    LIC --> BUS
    BUS --> ORD
    BUS --> PAY
    BUS --> DEL
    BUS --> INT
    BUS --> LIC
    BUS --> NOT
    BUS --> AUD
```

## Container inventory
The diagram covers the 17 registered ACCSystem containers. Individual `CNT-*` records remain the source for each container's responsibility, collaborators, ownership, and decomposition status.

| Container ID | Name | C3 status |
|---|---|---|
| CNT-ACC-APIGATEWAY | API Gateway / BFF | EXCEPTION |
| CNT-ACC-IDENTITY | Identity & Access | SELECTED |
| CNT-ACC-INSTREG | Institution Registry | EXCEPTION |
| CNT-ACC-INTEGRATION | Institution Integration Gateway | SELECTED |
| CNT-ACC-CATALOG | Catalog & Publication | SELECTED |
| CNT-ACC-SEARCH | Search & Discovery | EXCEPTION |
| CNT-ACC-OFFER | Offer / Price / Availability | EXCEPTION |
| CNT-ACC-CART | Cart & Checkout | EXCEPTION |
| CNT-ACC-ORDERS | Order Management | SELECTED |
| CNT-ACC-PAYMENT | Payment Orchestration | SELECTED |
| CNT-ACC-DELIVERY | Delivery Management | EXCEPTION |
| CNT-ACC-NOTIFICATIONS | Notifications | EXCEPTION |
| CNT-ACC-AUDIT | Audit & Observability | EXCEPTION |
| CNT-ACC-SOFTCAT | Software Catalog & Release Distribution | EXCEPTION |
| CNT-ACC-LICENSE | License & Entitlement Management | SELECTED |
| CNT-ACC-PLATFORMADMIN | Platform Administration & Support | EXCEPTION |
| CNT-ACC-EVENTBUS | Event Bus / Message Broker | EXCEPTION |

## Notes and evidence limits
- All client connections to ACCSystem pass through `CNT-ACC-APIGATEWAY`.
- `CNT-ACC-IDENTITY` validates tokens on authenticated requests; repeated request-level edges are omitted for readability.
- `CNT-ACC-EVENTBUS` is the shared asynchronous backbone; services publish/subscribe through the documented Outbox/Inbox patterns.
- ACCore integration is bidirectional at the capability level; concrete transport and authentication mode remain policy-gated under ADR-015.
- This diagram represents logical relationships, not deployment topology or implementation readiness.

**Sources:** `registry/decomposition-map.json`, `c1-context/systems/SYS-ACCSYSTEM.md`, individual `c2-containers/accsystem/CNT-*.md` records, ADR-005, ADR-012, ADR-015, and ADR-020.
