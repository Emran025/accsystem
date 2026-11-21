# CNT-ACC-ORDERS — Component Diagram

```mermaid
flowchart TD
    subgraph ORD["CNT-ACC-ORDERS — Order Management"]
        SPLIT["CMP-ORD-MULTISELLER\nParent / Seller splitter"]
        SAGA["CMP-ORD-SAGA\nParent Saga Coordinator"]
        SM["CMP-ORD-STATEMACHINE\nParent + Seller states"]
        SNAP["CMP-ORD-SNAPSHOT\nImmutable commercial snapshots"]
        CANCEL["CMP-ORD-CANCEL\nCancellation / returns"]
    end

    CART["CNT-ACC-CART\nCart & Checkout"]
    RES["CMP-INT-RESERVATION\n(Integration reservation relay)"]
    ACCORE["CMP-CON-RESERVATION\n(Seller ACCore reservation handler)"]
    PAY["CMP-PAY-ORCHESTRATOR\n(Payment domain)"]
    PAYREF["CMP-PAY-REFUND\n(Payment domain)"]
    DELIVERY["CNT-ACC-DELIVERY\n(Delivery Management)"]
    EVENTBUS["CNT-ACC-EVENTBUS\n(Event Bus)"]
    OUTBOX["Transactional Outbox\n(container mechanism)"]
    SETTLEMENT["Settlement / Ledger boundary\nScope and ownership OPEN"]

    CART -->|Checkout request| SPLIT
    SPLIT -->|ParentOrder + SellerOrders| SAGA
    SAGA -->|Concurrent reservation sub-operations| RES
    RES -->|Per-SellerOrder reservation request| ACCORE
    SAGA -->|Payment allocations / policy| PAY
    SAGA --> SM
    SAGA --> SNAP
    SAGA -->|OrderConfirmed intent| OUTBOX
    CANCEL -->|Check / request state transition| SM
    CANCEL -->|Release or cancel reservation| RES
    CANCEL -->|Void / refund| PAYREF
    CANCEL -->|Halt shipment / initiate return| DELIVERY
    CANCEL -.->|Reverse or hold seller credit / commission\nLedger boundary OPEN| SETTLEMENT
    CANCEL -->|OrderCancelled / ReturnRequested intent| OUTBOX
    OUTBOX -->|Recoverable event publication| EVENTBUS
```

The orders container owns the ParentOrder and SellerOrder orchestration; payment and delivery execution remain with their respective domains. `CNT-ACC-DELIVERY` has a documented `OrderConfirmed` container-level trigger, but the sources do not establish a C3 `CNT-ACC-EVENTBUS → CNT-ACC-DELIVERY` relationship, so no such edge is asserted here. The settlement/ledger collaborator is shown only as an OPEN boundary, not as an implemented component.

The Parent Saga Coordinator persists one parent workflow and seller-scoped sub-operation state. It waits for every required reservation, compensates confirmed holds after definitive rejection, preserves UNKNOWN outcomes, and blocks payment until safe resolution.
