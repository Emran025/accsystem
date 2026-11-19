# CNT-ACC-ORDERS — Component Diagram

```mermaid
flowchart TD
    subgraph ORD["CNT-ACC-ORDERS — Order Management"]
      SPLIT["CMP-ORD-MULTISELLER\nParent/Seller splitter"]
      SAGA["CMP-ORD-SAGA\nParent Saga Coordinator"]
      SM["CMP-ORD-STATEMACHINE\nParent + Seller states"]
      SNAP["CMP-ORD-SNAPSHOT\nImmutable commercial snapshots"]
      CANCEL["CMP-ORD-CANCEL\nCancellation/returns"]
    end
    CHECKOUT["Cart & Checkout"] --> SPLIT
    SPLIT -->|"ParentOrder + SellerOrders + outbox"| SAGA
    SAGA -->|"concurrent reservation sub-operations"| RES["CMP-INT-RESERVATION"]
    RES -->|"one reservation ID/key per SellerOrder"| ACC["Seller ACCore instances"]
    SAGA -->|"payment allocations / policy"| PAY["CMP-PAY-ORCHESTRATOR"]
    SAGA --> SM
    SAGA --> SNAP
    SAGA --> BUS["Outbox / Event Bus"]
    BUS --> DEL["Delivery"]
    CANCEL --> SAGA
    CANCEL --> RES
    CANCEL --> PAY
```

The Parent Saga Coordinator persists one parent workflow and seller-scoped sub-operation state. It waits for every required reservation, compensates confirmed holds after definitive rejection, preserves UNKNOWN outcomes, and blocks payment until safe resolution.
