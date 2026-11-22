# ACC Ecosystem — Dynamic View: Multi-Seller Purchase Flow

**Status:** PROPOSED MVP BASELINE — multi-seller and multi-category carts are required.

## Rules
A cart is grouped by seller/institution into one ParentOrder and one SellerOrder per seller. ACCore owns inventory. Reservation requests run concurrently where safe and each has a stable scoped request/idempotency key; reservation-ID assignment remains an institution/API contract gate. Payment is blocked until every required reservation is authoritatively accepted and other guards hold. `UNKNOWN` never means rejection and never authorizes an unsafe release.

## Sequence
```mermaid
sequenceDiagram
    autonumber
  participant B as Buyer
  participant C as CartCheckout
  participant O as ParentSaga
  participant S as Splitter
  participant I as IntegrationRelay
  participant A1 as SellerACCore1
  participant A2 as SellerACCore2
  participant P as PaymentOrchestrator
  participant E as Provider
  participant X as OutboxEventBus
  participant D as Delivery

    B->>C: Create checkout with cart and delivery/payment details
    C->>C: Snapshot prices, tax lines, currencies, delivery and policy versions
    B->>O: Submit checkout with idempotency key
    O->>S: Create ParentOrder and group lines by seller
    S-->>O: ParentOrder + SellerOrder[1..N] persisted with outbox
    par Reservation per seller
        O->>I: Reserve SellerOrder[1] (stable scoped request key)
        I->>A1: Atomic local reserve at ACCore
        A1-->>I: ACCEPTED / REJECTED / UNKNOWN / authoritative EXPIRED
        I-->>O: SellerOrder[1] outcome
    and
        O->>I: Reserve SellerOrder[2..N] (stable scoped request keys)
        I->>A2: Atomic local reserve at ACCore
        A2-->>I: ACCEPTED / REJECTED / UNKNOWN / authoritative EXPIRED
        I-->>O: SellerOrder[2..N] outcomes
    end
    alt Definitive rejection or authoritative expiry
        O->>O: Block checkout, reconcile other in-flight outcomes under UNKNOWN guard
        O->>I: Release only eligible confirmed accepted holds when guards permit
        I-->>O: RELEASED or release UNKNOWN
        alt All required outcomes and compensation resolved
            O->>X: ParentOrderFailed or eligible expiry via durable outbox
        else Any required result remains UNKNOWN or pending
            O->>O: Retain recovery/review work, do not announce final closure
        end
    else Any UNKNOWN
        O->>O: ParentOrder ReservationUnknown, query where the institution contract supports it, otherwise wait/escalate and reconcile, with no payment or unsafe release
    else All required reservations accepted
        O->>P: Create per-SellerOrder payment allocations
        alt Compatible policy group and provider supports aggregation
            P->>E: One aggregated buyer transaction with seller allocations
        else Incompatible policies or provider limitation
            P->>E: Separate payment attempts per SellerOrder
        end
        E-->>P: AUTHORIZED / CAPTURED / DECLINED / UNKNOWN
        alt Definitive payment failure
            P-->>O: PaymentFailed
            O->>O: Reconcile other in-flight payment and reservation effects
            O->>I: Compensate eligible confirmed holds when guards permit
            alt Required compensation settled
                O->>X: ParentOrderFailed via durable outbox
            else Compensation or another effect UNKNOWN
                O->>O: Keep recovery pending and escalate per policy
            end
        else Payment unknown
            P-->>O: PaymentUnknown
            O->>O: Reconcile without repeating financial effect or releasing unknown hold
        else All required allocations definitively successful and holds still accepted
            O->>O: Recheck all confirmation guards, persist immutable snapshots and CONFIRMED transition
            O->>X: OrderConfirmed(parent + seller orders) in same local transaction/outbox
            X->>D: Create applicable seller-scoped physical shipments
            X->>P: Evaluate approved later capture per allocation, skip already captured and reconcile UNKNOWN
        else Authoritative hold expiry or other guard fails during payment
            O->>O: Block confirmation, reconcile payment and peers, keep compensation pending until settled
        end
    end
```

## State and accounting rules

| Level | Required record |
|---|---|
| ParentOrder | aggregated product/tax/delivery totals by currency, policy snapshot IDs, seller-order references, overall state |
| SellerOrder | seller lines, price/tax/delivery/commission allocations, transaction currency, exchange source/time if converted, reservation/payment references, seller policy |
| Payment | per SellerOrder allocation and idempotency key; aggregated buyer transaction only with compatible policy support |
| Ledger | separate capture/collection, seller credit/transfer, commission payable, settlement, and manual-payment postings |

`OrderConfirmed` is committed with the order snapshot and outbox entry atomically in ACCSystem. If the relay is unavailable, the outbox retries; the committed order is not silently undone. Delivery-provider collection of funds is separate from delivery-charge collection and is not included in core payment unless explicitly configured.
