# CMP-ORD-MULTISELLER — Multi-Seller Order Splitter

**Component ID:** CMP-ORD-MULTISELLER  
**Parent:** CNT-ACC-ORDERS  
**Status:** PROPOSED MVP BASELINE — multi-seller support is required in MVP; owner direction is recorded in ADR-016.

## Responsibility and boundary
When a validated cart contains products from multiple sellers/categories, this component creates one `ParentOrder` and one `SellerOrder` per seller/institution. It owns grouping, stable seller-order identifiers, and the atomic local write of the parent, seller orders, and `SellerOrderCreated` outbox events. Reservation, payment, delivery, and inventory business logic remain in their owning domains.

## Coherent execution pattern
The Parent Saga Coordinator owns the overall checkout. It starts one reservation sub-operation per SellerOrder, concurrently where safe. Each sub-operation has its own reservation ID, idempotency key, state, and correlation link. Payment authorization is blocked until every required reservation has a definitive success or definitive rejection. A definitive rejection releases only holds confirmed to have succeeded and fails checkout by default. `UNKNOWN` is neither success nor rejection and is reconciled by reservation ID/idempotency key without an unsafe release.

## Data and transaction boundaries
The splitter writes ParentOrder + all SellerOrders + their outbox records in one local ACCSystem database transaction. It does not span a transaction into ACCore. The parent coordinator persists saga state separately and coordinates the distributed steps with Outbox/Inbox and at-least-once delivery. A duplicate split request returns the existing seller orders.

Each SellerOrder contains its own item snapshot, seller, reservation ID/state, payment allocation reference, tax/delivery/commission snapshot references, and fulfillment state. The safe payment baseline is one payment record and ledger allocation per SellerOrder/seller. An aggregated buyer-facing transaction is allowed only when the provider supports compatible policy groups; otherwise separate payment attempts are used. Capture is controlled per seller/agreement policy.

## Acceptance tests (MVP)

| Scenario | Expected result |
|---|---|
| One seller | One SellerOrder is created through the same splitter path. |
| Multiple sellers/categories | N SellerOrders are created with no cross-seller line mixing. |
| Concurrent split retry | Existing ParentOrder/SellerOrders are returned; no duplicates. |
| One reservation rejected | Confirmed successful holds are released; checkout fails; payment is not authorized. |
| Reservation response unknown | SellerOrder enters `ReservationUnknown`; no release or payment until reconciled. |
| Last-unit race | ACCore conditional update/lock allows at most one successful reservation. |
| Outbox publish failure | Order transaction remains committed; relay retries the persisted outbox event. |
| Incompatible seller capture policies | Use separate payment attempts or block checkout by policy; never silently force one mode. |

**References:** ADR-016, ADR-017, FN-ORD-RESERVE, CMP-ORD-SAGA, CMP-ORD-STATEMACHINE.
