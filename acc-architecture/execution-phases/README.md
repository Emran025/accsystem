# Execution Phases — ACC Ecosystem

**Document role:** phase-boundary definition only  
**Status:** PROPOSED BASELINE — requires product, architecture, security, operations, finance and institutional review  
**Scope:** defines where each of the four implementation phases starts and ends, what product increment it produces, and what must be true before the next phase begins. It does **not** define the functional requirements, API schemas, event schemas, database schemas, or implementation tasks belonging to each phase.

## 1. Purpose and relationship to the architecture

This document partitions the current ACC Ecosystem architecture into four executable product increments. It is a boundary document, not a second requirements catalogue. The requirements for each phase will later be derived from the existing functions, containers, components, ADRs, interface contracts, data views and validation evidence.

The phase partition is deliberately aligned with the architecture's ownership boundaries:

- ACCSystem platform foundation and institution connectivity;
- ACCore product/catalog ownership, ACCSystem publication and buyer discovery/reservation;
- inventory, order, payment, settlement boundary and externally sourced delivery events;
- ACCMared-managed internal fulfillment and delivery operations.

A capability may be designed earlier than the phase in which it becomes operationally enabled. For example, a boundary or state vocabulary may be defined in an earlier phase while a provider-specific activation remains gated until a later phase. This document does not convert a proposed or owner-gated decision into an approved requirement.

## 2. Chosen lifecycle pattern

The project uses a **phase-gated incremental lifecycle with a V-model/Waterfall-style execution loop inside each phase**:

```text
Phase entry baseline
  → scope and stakeholder confirmation
  → architecture and state baseline
  → requirements and contract definition
  → design and implementation
  → verification, integration and operational review
  → phase product / pilot increment
  → gate decision
  → next phase or controlled rework
```

This is not a claim that the whole product is a single waterfall. Each phase produces a usable, inspectable increment and can expose evidence that requires a bounded correction to an earlier phase. The phase boundary remains controlled: later work must not silently expand an earlier phase's scope, and unresolved external decisions remain explicit gates.

The method is selected because the system has cross-institution contracts, payment and inventory effects, security boundaries and operational approvals that benefit from explicit entry/exit evidence. It also preserves incremental delivery: a phase can produce a bounded product without waiting for ACCMared or every financial policy to be complete.

The governing rule is **evidence-based progression**, not calendar progression. A phase may proceed only when its entrance evidence is satisfied and its exit product has passed the agreed verification and review criteria. A failed gate means remediate, defer, or stop; it does not mean hide the gap or redefine the phase after the fact.

## 3. Phase 1 — Platform Foundation and Trust Boundaries

### Starts when

The architecture baseline, system actors, institution boundary, ownership model and initial governance route are available for review. The phase begins before marketplace product publication and before transactional checkout is enabled.

### Includes

The platform capabilities and boundaries needed by every later phase:

- institution identity, tenant boundary and institution lifecycle;
- institutional licensing, entitlement and capability-gating foundation;
- user identity, authentication, authorization, roles and support scope;
- security boundaries, auditability and sensitive-operation traceability;
- ACCSystem–ACCore integration boundary and approved connectivity options;
- credential/reference handling, transport protection, replay/idempotency identity and correlation context;
- Outbox/Inbox and at-least-once delivery foundations;
- policy and owner-gate mechanism for unresolved operational, provider, security and governance choices;
- baseline observability, recovery ownership and environment/bootstrap controls needed by later phases.

### Explicitly does not include

Product catalog publication, buyer search, cart checkout, inventory reservation execution, payment capture, settlement activation, shipment tracking, or ACCMared dispatch operations. Those later capabilities may be modelled as consumers of Phase 1 boundaries but are not enabled by this phase.

### Ends when

The platform can establish and audit the identity, tenant, licensing, authorization and protected integration context required by later phase products, and the unresolved security/connectivity/governance choices have named owners and activation conditions. The phase product is a **trusted platform foundation increment**, not a marketplace or payment product.

### Gate to Phase 2

Entry to Phase 2 requires an agreed actor/tenant and ownership baseline, a reviewed license and authorization lifecycle, a reviewed security/integration boundary, recoverable message identity rules, and a recorded disposition for external gates. Structural documentation checks alone are not sufficient evidence of security or operational approval.

## 4. Phase 2 — Catalog, Discovery and Reservation

### Starts when

Phase 1's identity, institution scope, licensing and protected data-transport boundaries are available to the product/catalog flows, with ACCore remaining authoritative for institution-owned product and inventory decisions.

### Includes

The product-to-reservation path, without financial completion:

- local institution product-master and catalog preparation boundary;
- publishable product projection and versioned publication to ACCSystem;
- listing ingestion, validation, withdrawal and publication recovery boundary;
- catalog browsing, search, product detail and buyer access for institution and individual channels;
- availability and service-availability presentation, including stale, unavailable, offline and policy-controlled visibility states;
- cart/checkout preparation up to the reservation boundary;
- seller-scoped reservation request, accepted/rejected/unknown/authoritatively expired outcomes;
- reservation identity, duplicate handling, safe release boundary and reconciliation handoff.

### Explicitly does not include

Payment authorization or capture, refunds, seller credit, commission, settlement, financial ledger posting, final order confirmation, external shipment tracking, or ACCMared internal delivery management. A reservation may be represented as a prerequisite and its later consumer may be modelled, but Phase 2 does not financially commit an order.

### Ends when

An institution can prepare and publish an authoritative product projection, buyers can discover and view it through the approved channels, and the product-to-reservation journey reaches a durable, scoped outcome without unsafe assumptions about stale availability, timeout or connectivity loss. The phase product is a **catalog-and-reservation increment**, not a payment or fulfillment increment.

### Gate to Phase 3

Entry to Phase 3 requires a reviewed publication/discovery boundary, canonical visibility and reservation vocabulary, duplicate and UNKNOWN handling, reconciliation ownership, and an accepted end-to-end product-to-reservation demonstration or equivalent evidence. Payment and settlement policy gates remain separate; passing this gate does not approve financial activation.

## 5. Phase 3 — Inventory, Order, Payment and External Delivery Events

### Starts when

Phase 2 can produce a safe reservation outcome and the platform can preserve the identity and evidence required to coordinate inventory, order and payment effects. The phase starts with authoritative stock/inventory integration and may use an external institution or carrier system for delivery execution.

### Includes

The transactional and externally observable fulfillment path:

- inventory availability intake and institution-owned warehouse/storage references;
- stock, reservation, commitment and reconciliation boundaries;
- ParentOrder, SellerOrder, order-line and immutable commercial/policy snapshots;
- payment allocation and PaymentAttempt lifecycle;
- authorization, approved capture modes, void, refund-operation boundary and payment reconciliation;
- seller-credit, commission, settlement and ledger boundary without inventing their owner policy;
- confirmation guards requiring the applicable reservation and payment outcomes;
- order cancellation/return coordination across known stock and financial effects;
- external or institution-owned shipment/tracking event intake;
- buyer-facing order, payment, exception and delivery-status visibility in ACCommerce and approved institution channels;
- delivery event normalization where execution is performed by a third-party platform or an institution's own system.

### Explicitly does not include

ACCMared-owned courier dispatch, supervisor work queues, internal route assignment, internal courier application workflows, or institution-wide internal delivery operations. External tracking events may be consumed, but Phase 3 does not require ACCSystem to own the physical delivery execution.

### Ends when

A bounded transaction can progress from authoritative inventory/reservation through scoped order and payment state to confirmation and externally supplied delivery-status events, with reconciliation and buyer visibility. The phase product is an **order/payment/external-delivery-event increment**. It is not a claim that provider, Finance, Legal, institution or production approvals have been granted.

### Gate to Phase 4

Entry to Phase 4 requires a reviewed payment and financial-effect boundary, executable or otherwise evidenced reconciliation scenarios for the selected pilot integrations, a stable shipment/event identity model, and an accepted decision about which delivery effects remain external versus which are delegated to ACCMared. Provider capabilities, settlement policy, security review and operational readiness must be separately approved before real-money production activation.

## 6. Phase 4 — ACCMared Internal Delivery Operations

### Starts when

Phase 3 can create the shipment/delivery work boundary and expose the order, destination, inventory and exception context required by internal fulfillment. The institution has chosen to operate delivery through ACCMared rather than relying only on an external or institution-owned delivery system.

### Includes

The institution-managed physical delivery product:

- internal shipment and delivery-job ownership;
- warehouse/pickup handoff and delivery-zone context;
- supervisor queue, dispatch, assignment, prioritization and exception management;
- courier identity, acceptance, pickup, transit and delivery-attempt operations;
- proof-of-delivery and permitted location/evidence handling;
- offline courier synchronization if enabled by the approved capability scope;
- failed delivery, return, cancellation and rescheduling operations;
- delivery status propagation back to orders, buyer channels, audit and reconciliation;
- operational metrics, SLA handling, support and runbooks for internal delivery.

### Explicitly does not include

Changing ACCore ownership of inventory, redefining payment/settlement policy, replacing the Phase 3 financial ledger boundary, or assuming that every institution must use ACCMared. External delivery remains a supported alternative where the institution has not selected internal ACCMared operations.

### Ends when

A selected institution can manage an internal delivery job from assignment through pickup, transit, delivery attempt and final delivered/failed/returned outcome, with evidence and status propagated to the appropriate order and buyer boundaries. The phase product is an **ACCMared internal-delivery increment**.

### Final phase gate

The final gate requires institution operations, security/privacy, delivery ownership and support readiness; verified status propagation; proof-of-delivery and exception handling evidence; and a clear coexistence rule between ACCMared-managed and externally managed delivery. It does not retroactively approve unresolved financial, legal, provider or retention decisions.

## 7. Cross-phase boundary rules

1. A later phase may consume an earlier phase's boundary only through the identity, ownership and state contract established at the earlier gate.
2. A later phase may not silently make an earlier phase responsible for a capability that was explicitly excluded from its boundary.
3. `UNKNOWN`, pending review, external approval and provider capability gaps remain visible across phase boundaries; they are not converted into success by phase completion.
4. Every phase must preserve the valid alternatives already present in the architecture, including aggregate versus separate payment attempts, authorize-then-capture versus approved immediate capture, manual/external payment where supported, external versus ACCMared delivery, and institution-specific connectivity modes.
5. A phase product is an increment that can be inspected and piloted within its boundary. It is not automatically a production release.
6. Functional requirements, use cases, state transitions, data models, event requirements, acceptance criteria and API contracts will be created under later approved planning documents. They are intentionally out of scope for this README.

## 8. Phase planning template for later documents

Each later phase-specific requirements document should use the same lifecycle sequence without expanding this boundary README:

```text
phase boundary
→ capability inventory
→ function inventory
→ requirements
→ use cases and state model
→ data and event model
→ security and ownership review
→ contract/API design
→ implementation increment
→ verification and integration evidence
→ operational/readiness review
→ gate decision
```

## 9. Current status

This four-phase partition is a proposed execution boundary. The current architecture registry and existing five-step roadmap remain authoritative for their own purposes until this phase plan is reviewed and accepted. No API document, functional requirement, provider choice, accounting policy or production commitment is created by this README.

## 10. Requirements package structure

The detailed requirements package is deliberately kept separate from this boundary document. The mandatory decomposition, identifier rules, application/location tables, C4-container binding rules, and machine-checkable registry are defined in [`requirements-governance.md`](requirements-governance.md).

The five reserved phase folders are:

| Phase | Folder | Current status |
|---|---|---|
| PH-01 | [`phase-01-platform-foundation/`](phase-01-platform-foundation/) | Requirement package not started |
| PH-02 | [`phase-02-catalog-discovery-reservation/`](phase-02-catalog-discovery-reservation/) | Requirement package not started |
| PH-03 | [`phase-03-inventory-order-payment-delivery-events/`](phase-03-inventory-order-payment-delivery-events/) | Requirement package not started |
| PH-04 | [`phase-04-accmared-internal-delivery/`](phase-04-accmared-internal-delivery/) | Requirement package not started |
| PH-05 | [`phase-05-intelligence-personalization/`](phase-05-intelligence-personalization/) | Future-only boundary; no requirements allowed |

The initial machine-readable registry is [`requirements-registry.csv`](requirements-registry.csv), and its structural checker is [`validate_requirements.py`](validate_requirements.py). The empty registry is intentional until the first requirement package is elicited and reviewed.

## References

[1]: https://www.nasa.gov/reference/3-0-nasa-program-project-life-cycle/ "NASA Systems Engineering Handbook — Program/Project Life Cycle"

[2]: https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_7123_001B_\&page_name=Chapter5 "NASA Systems Engineering — Life-cycle and Technical Reviews"

[3]: https://www.iso.org/standard/90219.html "ISO/IEC/IEEE 12207:2026 — Software life cycle processes"

[4]: https://sebokwiki.org/wiki/INCOSE_Systems_Engineering_Handbook "SEBoK — INCOSE Systems Engineering Handbook"
