# CNT-ACC-INTEGRATION — Institution Integration Gateway — Component Diagram

**Viewpoint:** C3 — Internal components of CNT-ACC-INTEGRATION
**Status:** DRAFT | Relationships are limited to documented collaborator/interface evidence; transport and event contracts remain open where noted.

```mermaid
flowchart LR
    EVENTBUS["CNT-ACC-EVENTBUS\nEvent Bus"]
    CATALOG["CNT-ACC-CATALOG"]
    INSTREG["CNT-ACC-INSTREG"]
    IDENTITY["CNT-ACC-IDENTITY"]
    AUDIT["CNT-ACC-AUDIT"]
    ORDERS["CNT-ACC-ORDERS\n(order event publisher / reservation caller)"]
    ACR_CON["CNT-ACR-CONNECTOR\n(ACCore) "]

    subgraph INT["CNT-ACC-INTEGRATION — Institution Integration Gateway"]
        GW["CMP-INT-GATEWAY\nIntegration Gateway\n(inbound validation and routing)"]
        PUB["CMP-INT-PUBLICATION\nProduct Publication Worker"]
        RES["CMP-INT-RESERVATION\nReservation Relay"]
        NOTIFY["CMP-INT-ORDERNOTIFY\nOrder Event Dispatcher"]
    end

    %% ACCore ingress and routing
    ACR_CON -->|IF-ACR-PUBLISH-EVENT; field/schema mapping not final| GW
    ACR_CON -->|IF-ACR-RESERVATION-RESP\nresponse / trusted query; callback only if approved| GW
    GW -->|Route publication events| PUB
    GW -->|Route validated reservation outcome/query| RES
    GW -->|Order-event dispatch route listed by Gateway record\nseparate from Event Bus subscription; trigger details OPEN| NOTIFY

    %% Reservation command and result boundaries
    ORDERS -->|IF-ACC-RESERVE-SAGA\nOrders to Integration request| RES
    RES -->|Relay reservation/release command through CMP-CON-RESERVATION\nchannel, query and callback arrangement OPEN| ACR_CON

    %% Event Bus subscription and external dispatch
    EVENTBUS -->|OrderConfirmed / OrderCancelled / ReturnRequested| NOTIFY
    NOTIFY -->|IF-ACC-ORDER-CONFIRM\nlogical ACCSystem to ACCore direction; channel / ACK / schema OPEN| ACR_CON
    NOTIFY -.->|Cancellation / return routing\nconsumer mapping and channel OPEN| ACR_CON
    NOTIFY -->|Dispatch attempts and results audit| AUDIT

    %% Publication, registry, authentication, and auditing
    PUB -->|Validated listing publication work| CATALOG
    PUB -->|ProductPublicationProcessed\nworker result event; wire mapping OPEN| EVENTBUS
    GW -->|Validate institution context| INSTREG
    GW -->|Validate service credentials\nauthentication method governed by ADR-015| IDENTITY
    NOTIFY -->|Resolve institution connector context| INSTREG
    GW -->|Connection / routing decision audit| AUDIT
    GW -.->|Integration event publication path\nexact business event contract OPEN; not an audit substitute| EVENTBUS
```

`CMP-INT-GATEWAY` validates inbound credentials, institution context and payloads, then routes to workers; it does not make reservation or publication business decisions. The `Gateway → OrderNotify` routing relationship is shown separately from the documented `EventBus → OrderNotify` subscription. The gateway audit relationship is also separate from the open Integration-to-EventBus business-event path; audit events are not implicitly treated as business events.

`IF-ACC-RESERVE-SAGA` is the request from Orders to Integration, not an outgoing Integration-to-ACCore interface. `CMP-INT-RESERVATION` relays that request to `CMP-CON-RESERVATION`; the exact outgoing channel and schema remain open. Reservation statuses include `ACCEPTED`, `REJECTED`, `UNKNOWN` and authoritative `EXPIRED`; status values are not asserted as literal callback event types. The optional callback mode requires explicit institution approval under ADR-015.

`IF-ACC-ORDER-CONFIRM` expresses the logical ACCSystem-to-ACCore handoff. Outbound-initiated polling/persistent channels and optional protected inbound connectivity remain available alternatives; this diagram does not select one or finalize ACK semantics. `ProductPublicationProcessed` is a worker-level event named in its record; its final wire mapping remains open.

---

## Component Summary

| Component | ID | Responsibility |
|---|---|---|
| Integration Gateway | CMP-INT-GATEWAY | Validates inbound institution/service context and routes requests to the applicable worker |
| Product Publication Worker | CMP-INT-PUBLICATION | Maintains recoverable publication processing and routes accepted work to Catalog |
| Reservation Relay | CMP-INT-RESERVATION | Relays scoped reserve/release operations and reconciles uncertain outcomes |
| Order Event Dispatcher | CMP-INT-ORDERNOTIFY | Subscribes to order events and dispatches recipient-scoped handoffs |

---

## Traceability and Open Items

| Concern | Status |
|---|---|
| Institution identity and service credential validation | Documented; credential method is policy-selected under ADR-015 |
| Gateway to OrderNotify routing vs. EventBus subscription | Separate relationships shown; exact trigger/dispatch route remains OPEN |
| Gateway audit vs. Integration business events | Distinct relations shown; event publication contract remains OPEN |
| Reservation command leg to ACCore | Relayed by CMP-INT-RESERVATION; exact channel/schema OPEN |
| Reservation response/query/callback arrangement | Synchronous response is baseline; query/optional callback details are institution/API approval gates |
| Order confirmation channel, ACK and schema | PROPOSED / OPEN; do not infer transport from logical direction |
| Publication worker result event mapping | OPEN; no final schema asserted |

---

*Updated: 2026-11-21 | Not stakeholder-approved | Not production-ready*
