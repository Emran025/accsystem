# CNT-ACC-INTEGRATION — Institution Integration Gateway — Component Diagram

**Viewpoint:** C3 — Internal components of CNT-ACC-INTEGRATION
**Status:** DRAFT | Relationships are limited to documented collaborator/interface evidence.

```mermaid
flowchart LR
    EVENTBUS["CNT-ACC-EVENTBUS\nEvent Bus"]
    CATALOG["CNT-ACC-CATALOG"]
    INSTREG["CNT-ACC-INSTREG"]
    AUDIT["CNT-ACC-AUDIT"]
    ORDERS["CNT-ACC-ORDERS\n(reservation caller)"]
    ACR_CON["CNT-ACR-CONNECTOR\n(ACCore)"]

    subgraph INT["CNT-ACC-INTEGRATION — Institution Integration Gateway"]
        GW["CMP-INT-GATEWAY\nIntegration Gateway\n(inbound routing, signature validation)"]
        PUB["CMP-INT-PUBLICATION\nProduct Publication Worker"]
        RES["CMP-INT-RESERVATION\nReservation Relay (circuit breaker)"]
        NOTIFY["CMP-INT-ORDERNOTIFY\nOrder Event Dispatcher"]
    end

    %% ACCore ingress and routing
    ACR_CON -->|ProductListingPublished / Updated / Withdrawn| GW
    ACR_CON -->|IF-ACR-RESERVATION-RESP\nResponse / trusted query; optional approved callback OPEN| GW
    GW -->|Route publication events| PUB
    GW -->|Route inbound reservation response / query| RES

    %% Reservation request is owned by Orders and enters Integration
    ORDERS -->|IF-ACC-RESERVE-SAGA\nOrders to Integration request| RES
    RES -->|Reservation request through CMP-CON-RESERVATION\nresponse/query/callback arrangement OPEN| ACR_CON

    %% Event Bus subscription is supported for OrderNotify, not Gateway
    EVENTBUS -->|OrderConfirmed / OrderCancelled / ReturnRequested| NOTIFY
    NOTIFY -->|IF-ACC-ORDER-CONFIRM\nlogical ACCSystem to ACCore direction; channel OPEN / PROPOSED| ACR_CON
    NOTIFY -.->|Cancellation / return routing\nschema and channel mapping OPEN| ACR_CON

    %% Publication and registry lookups
    PUB -->|Validated listing publication| CATALOG
    GW -->|Validate institution context| INSTREG
    NOTIFY -->|Resolve institution context| INSTREG

    %% Documented outbound audit / event-bus collaborator
    GW -->|Connection and routing decisions| AUDIT
    GW -->|Integration events; exact event contract OPEN| EVENTBUS
```

> CMP-INT-GATEWAY validates inbound event signatures and routes to the appropriate worker. Reservation status covers ACCEPTED, REJECTED, UNKNOWN and authoritative EXPIRED; response/query and optional approved callback are not claims that status values are registered event types. `IF-ACC-RESERVE-SAGA` is the request from Orders to Integration; it is not the outgoing Integration-to-ACCore interface. The documented Event Bus subscription is to CMP-INT-ORDERNOTIFY; no Event Bus-to-Gateway subscription is asserted. The exact reservation response arrangement and order-confirmation channel remain open.
