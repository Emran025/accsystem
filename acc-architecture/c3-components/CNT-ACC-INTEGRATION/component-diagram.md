# CNT-ACC-INTEGRATION — Institution Integration Gateway — Component Diagram

**Viewpoint:** C3 — Internal components of CNT-ACC-INTEGRATION

```mermaid
flowchart LR
    EVENTBUS["CNT-ACC-EVENTBUS\nEvent Bus"]
    CATALOG["CNT-ACC-CATALOG"]
    INSTREG["CNT-ACC-INSTREG"]
    ACR_CON["CNT-ACR-CONNECTOR\n(ACCore)"]

    subgraph INT["CNT-ACC-INTEGRATION — Institution Integration Gateway"]
        GW["CMP-INT-GATEWAY\nIntegration Gateway\n(inbound routing,\nsignature validation)"]
        PUB["CMP-INT-PUBLICATION\nProduct Publication\nWorker"]
        RES["CMP-INT-RESERVATION\nReservation Relay\n(circuit breaker)"]
        NOTIFY["CMP-INT-ORDERNOTIFY\nOrder Event\nDispatcher"]
    end

    %% Inbound from ACCore
    ACR_CON -->|ProductListingPublished\nIF-ACR-PUBLISH-EVENT| GW
    ACR_CON -->|ReservationAccepted/Rejected\nIF-ACR-RESERVATION-RESP| GW

    %% Internal routing
    GW --> PUB
    GW --> RES

    %% Event Bus → Order Notify
    EVENTBUS -->|OrderConfirmed\nOrderCancelled| NOTIFY
    NOTIFY -->|IF-ACC-ORDER-CONFIRM\nasync, at-least-once| ACR_CON

    %% Publication → Catalog
    PUB -->|validated listing| CATALOG

    %% Reservation relay
    RES -->|ReservationRequested\nIF-ACC-RESERVE-SAGA| ACR_CON

    %% Registry lookups
    GW --> INSTREG
    NOTIFY --> INSTREG

    %% Event Bus subscriptions
    EVENTBUS -->|integration events| GW
    INT --> EVENTBUS
```

> [!NOTE]
> CMP-INT-GATEWAY validates inbound event signatures and routes to appropriate worker. CMP-INT-RESERVATION applies circuit breaker to ACCore outbound calls.
