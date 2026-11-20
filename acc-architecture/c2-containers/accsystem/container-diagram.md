# ACCSystem Container Diagram

**Viewpoint:** C2 — ACCSystem Platform internal containers and their primary relationships  
**Audience:** Architects and developers  
**Label convention:** `CONFIRMED` = sourced from idea.md | `ASSUMPTION` = inferred | `UNKNOWN` = open

**Relationship to the registry overlay:** This is the separate detailed C2 view for ACCSystem. It adds selected client/system and external context around the internal containers and shows a broader set of primary relationships. The registry-derived [overlay view](../../c1-context/c4-context-and-container-overlays.md#c2-sys-accsystem--containers-of-accsystem-platform) is retained separately; neither view is declared authoritative over the other, and the choice between complementary views or an accepted reconciliation remains an owner/architecture gate.

---

## Container Diagram

```mermaid
flowchart LR
    %% External Clients
    ACE["CNT-ACE-MOBILEAPP\nACCommerce App"]
    ACR_COM["CNT-ACR-COMMERCE\nACCore Commerce\nWorkspace"]
    ACM_PUB["CNT-ACM-PUBLIC\nACManagement\nPublic Portal"]
    ACM_ADM["CNT-ACM-ADMIN\nACManagement\nAdmin Console"]
    AMD_SUP["CNT-AMD-SUPERVISOR\nACCMared Supervisor"]
    AMD_COU["CNT-AMD-COURIER\nACCMared Courier"]

    %% External Systems
    EXT_PAY["EXT-PAYMENT-PROVIDER\nExternal Payment\nProvider"]
    EXT_CDN["EXT-PACKAGE-CDN\nSoftware Package CDN"]

    %% ACCore Integration
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

    %% Client → Gateway
    ACE --> GW
    ACR_COM --> GW
    ACM_PUB --> GW
    ACM_ADM --> GW
    AMD_SUP --> GW
    AMD_COU --> GW

    %% Gateway → Services
    GW --> IDN
    GW --> CAT
    GW --> SRC
    GW --> CART
    GW --> ORD
    GW --> DEL
    GW --> SCAT
    GW --> LIC
    GW --> PADM

    %% Auth on every request
    IDN --> REG

    %% Commerce flow
    CART --> OFF
    CART --> ORD
    ORD --> INT
    ORD --> PAY
    ORD --> DEL
    ORD --> BUS

    %% Integration
    INT --> CAT
    INT --> REG
    ACR_CON --> INT
    INT --> ACR_CON

    %% Catalog → Search
    CAT --> SRC

    %% Payment
    PAY --> EXT_PAY
    EXT_PAY --> PAY

    %% Delivery
    DEL --> AMD_SUP
    DEL --> AMD_COU

    %% Platform Management
    SCAT --> EXT_CDN
    PADM --> IDN
    LIC --> BUS

    %% Event Bus consumers
    BUS --> ORD
    BUS --> PAY
    BUS --> DEL
    BUS --> INT
    BUS --> LIC
    BUS --> NOT
    BUS --> AUD
```

---

## Notes

- All client connections to ACCSystem pass through CNT-ACC-APIGATEWAY (HTTPS/TLS)
- CNT-ACC-IDENTITY validates tokens on every authenticated request (not shown on every arrow for clarity)
- CNT-ACC-AUDIT receives observability signals from all services (not shown for clarity)
- CNT-ACC-EVENTBUS is the shared async backbone; services publish/subscribe via Outbox/Inbox pattern
- ACCore integration is bidirectional: ACCore publishes product events; ACCSystem sends reservation requests and order confirmations

**Technology:** UNKNOWN — container orchestration platform not selected. OWNER_UNASSIGNED.

> [!NOTE]
> This diagram shows logical relationships, not deployment topology. Deployment topology in `supporting-views/deployment-view.md`.
