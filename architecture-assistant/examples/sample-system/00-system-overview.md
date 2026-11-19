# ParcelFlow — system overview

## Purpose and evidence boundary

`SYS-PARCELFLOW` is an illustrative system that coordinates a merchant's shipment-booking request and delivery of a shipping label. The documented sample workflow is intentionally bounded: a merchant operator submits shipment data, the API validates it, requests a booking from an external carrier, persists a booking result, and makes a label/status available through the web experience. This description is an example for architecture-documentation depth, not a confirmed product specification or production recommendation.

The available sample evidence identifies a web application (`CNT-WEB`), shipment API (`CNT-API`), parcel store (`CNT-DB`), and external carrier (`EXT-CARRIER`). The actor is the merchant operator. The sample does not identify a real customer, delivery provider, source repository, team structure, traffic, jurisdiction, retention rules, service objectives, cloud provider, or production topology. All such details remain `UNKNOWN`; technology and behavioral proposals must not be presented as facts.

## Business capabilities in the declared sample scope

| Capability | Primary actor/system | Expected outcome | Evidence/status |
|---|---|---|---|
| Enter shipment details | Merchant operator via `CNT-WEB` | A candidate shipment request is submitted for validation | Sample scope; details illustrative |
| Validate shipment request | `CNT-API` / `FN-ORDER-001` | Valid input is normalized; invalid fields are reported before external side effects | Function contract and sample rules |
| Request carrier booking | `CNT-API` → `EXT-CARRIER` | Booking result or an explicit failure is returned | Integration is identified; timeout/idempotency/compensation remain unresolved |
| Persist and retrieve booking state | `CNT-API` ↔ `CNT-DB` | The accepted booking state can be represented and later viewed | Store is identified; consistency and schema are illustrative/unknown |
| Present outcome to operator | `CNT-WEB` | Operator sees a booking outcome and can retrieve a label when one exists | Sample capability; authorization and UX details unresolved |

## System boundary and exclusions

Inside the sample boundary are the merchant-facing web workflow, shipment API orchestration, and parcel/booking records. The carrier is external: its internals are not modeled, only the integration contract. Billing settlement, warehouse management, merchant identity administration, carrier operations, route optimization and a customer-facing tracking portal are excluded from this sample unless later evidence brings them into scope. An exclusion does not imply those concerns are unnecessary in a real system.

The sample's C1/C2 baseline views and known relationships are in [`c1-context/context-diagram.md`](c1-context/context-diagram.md) and [`c2-containers/container-diagram.md`](c2-containers/container-diagram.md). Component and function identifiers are maintained in the registry; see [`registry/architecture-manifest.json`](registry/architecture-manifest.json) and [`functions/function-catalog.md`](functions/function-catalog.md).

## Quality and operational questions not answered by the sample

No numeric availability, latency, throughput, durability, recovery-time, recovery-point, accessibility, privacy, or security targets are supplied. The design therefore cannot claim to be scalable, highly available, compliant, secure, costed, or production-ready. Required discovery includes expected volumes and peaks, tenant isolation, identity and authorization, address/PII classification, label retention, carrier SLA and rate limits, duplicate submission behavior, support/on-call ownership, disaster recovery, and test evidence.

## Reading this example

Treat `ASSUMPTION` and `PROPOSED` statements as discussion inputs rather than stakeholder commitments. Each unknown should be resolved from a named source or stakeholder, assigned an owner/action, and given a revisit trigger before a real implementation decision. The detailed booking flow and function contract are intentionally longer than a representative summary so they demonstrate the expected treatment of behavior, side effects, failure semantics and gaps.
