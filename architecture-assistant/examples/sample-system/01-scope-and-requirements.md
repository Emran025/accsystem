# ParcelFlow — scope and requirements

## Status and interpretation

This is an illustrative architecture fixture, not an approved customer requirement set. The sample's core scope is shipment request intake, validation, carrier booking, persistence of booking outcome, and label/status presentation to a merchant operator. Any requirement below that extends beyond those stated capabilities is marked as a discovery item, not an established commitment.

## Actors and boundary

| Actor/system | Type | In-scope responsibility | Evidence/status |
|---|---|---|---|
| Merchant operator | Human actor | Submit shipment details and view booking outcome | Illustrative sample actor; authentication/roles unknown |
| `CNT-WEB` | Internal container | Present shipment entry/status workflow | In scope; detailed behavior is illustrative |
| `CNT-API` | Internal container | Validate request, coordinate booking/status operations | In scope; details in container/function records |
| `CNT-DB` | Internal data store | Persist booking/parcel records | In scope; schema and durability requirements unknown |
| `EXT-CARRIER` | External system | Accept booking requests and return carrier outcome/label | External boundary; internals excluded; contract unresolved |

In scope: merchant-facing shipment request workflow, field validation, booking orchestration, storing booking outcome, and retrieving/presenting the resulting status/label. Excluded in this sample: carrier internal services, billing settlement, warehouse management, route optimization and identity-provider implementation. Owner/team, deployment environments and operating jurisdictions are unresolved.

## Functional requirements (illustrative)

| ID | Requirement | Trigger/actor | Acceptance evidence | Status/open point |
|---|---|---|---|---|
| `FR-01` | The operator can submit a shipment request containing origin, destination and parcel dimensions. | Merchant operator via `CNT-WEB` | A request reaches `CNT-API` with the submitted values; field model and units must be confirmed. | `ASSUMPTION`; required fields/units/limits need product confirmation. |
| `FR-02` | The API rejects malformed or incomplete requests before invoking the carrier. | `CNT-API` | Invalid input returns field-specific validation errors and causes no carrier or persistence side effect. | Sample rule; error envelope and normalization details unresolved. |
| `FR-03` | A valid request can initiate a carrier booking and surface the resulting booking outcome. | `CNT-API` → `EXT-CARRIER` | Success/failure is correlated to the original request and displayed to the operator. | Core sample capability; carrier contract and duplicate behavior unresolved. |
| `FR-04` | The booking outcome is persisted and can be retrieved for display. | API and web workflow | A later retrieval returns the same authoritative booking state and label reference when available. | Sample capability; transaction, consistency, retention and authorization need definition. |

Acceptance statements are example-level only. Before implementation, assign a requirement owner and confirm payload fields, dimension units, address formats, supported parcel types, error taxonomy, booking lifecycle, label format/storage, and what the operator may do after a failure.

## Quality attributes and constraints

No numeric non-functional targets are supplied. Availability, latency, peak/average load, data-loss tolerance, recovery objectives, carrier timeouts, rate limits, privacy/regulatory classification, retention, auditability, accessibility, supported browsers, cost envelope, and operational support are all `UNKNOWN`. Do not convert these unknowns into default production targets. For each, obtain a business owner, measurement method and target before declaring operational readiness.

The sample assumes only that the browser-facing flow uses HTTPS/JSON, the API communicates with the carrier over an HTTPS-style request, and the service persists through `CNT-DB`; these are illustrative interface choices, not production facts. Language/framework and deployment are not fixed. The proposed Python choice in `ADR-002` remains unaccepted.

## Open questions and decision owners

| Question | Design/business impact | Resolution evidence | Owner/action | Revisit trigger |
|---|---|---|---|---|
| What are valid address fields and parcel units/ranges? | API validation, data schema and carrier mapping | Product acceptance criteria and carrier contract | `OWNER_UNASSIGNED` — appoint product/API owner | Before final API contract |
| What identity/roles may create, view, cancel or retry a booking? | Authorization, tenant isolation and audit | Identity architecture and role model | Appoint security/product owner | Before external pilot |
| How should timeout/duplicate carrier requests behave? | Duplicate charges/labels, state consistency and recovery | Carrier idempotency contract and failure tests | Appoint integration owner | Before booking implementation |
| What retention and deletion apply to addresses and labels? | Privacy, storage, backup and user rights | Data classification and jurisdiction review | Appoint data/privacy owner | Before production data collection |
| What availability, latency and recovery objectives are required? | Deployment, scaling, monitoring and cost | Workload/SLO workshop | Appoint service owner | Before deployment architecture approval |

The current scope is therefore `PARTIAL` for implementation planning: the illustrative business flow is modeled, while contractual, security, operational and compliance requirements are not yet evidenced.
