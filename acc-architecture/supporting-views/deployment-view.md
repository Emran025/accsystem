# Deployment View — ACC Ecosystem

**Status:** PROPOSED ARCHITECTURAL BASELINE — owner decisions applied; infrastructure/provider values remain configurable.

## 1. Boundary and ownership

ACCore is institution-controlled ERP software. Each institution may deploy it as one integrated package or as separate Backend and Frontend applications; packaging is a release option, not a platform ownership decision. The ACCore Backend may run on-premises or in a public cloud managed by the institution and may be internet-reachable where permitted. ACCSystem hosts the marketplace, order, payment-record, license, and platform data required for e-commerce. ACCSystem never becomes the source of truth for ACCore product or inventory data.

ACCore uses MySQL under the current owner direction. ACCSystem relational storage may use PostgreSQL or MySQL as temporary alternatives; the engine is not an architectural contract. Every bounded context owns its schema and migrations. No cross-context database access is permitted, including within a co-hosted deployment unit.

## 2. Connectivity baseline

The default for institutions behind firewalls is an outbound-initiated authenticated connector from ACCore to ACCSystem, using polling/long-polling or a persistent authenticated channel selected by operations. A protected inbound API is an optional deployment mode when the institution permits it. Both modes implement the same versioned connector contract, idempotency keys, correlation IDs, Outbox/Inbox, and query-by-reservation-ID operations.

When the connector is interrupted, ACCore local operations may continue, but ACCSystem marks the institution `CONNECTIVITY_UNAVAILABLE`; its listings are removed from search/promotion or shown explicitly unavailable. An in-flight reservation with no confirmed outcome is `UNKNOWN`, never successful by timeout. The saga retries and reconciles by idempotency key. No payment authorization is started until every required reservation is confirmed.

## 3. Logical contexts and deployment units

The 17 ACCSystem bounded contexts remain distinct owners of data and contracts. The proposed initial grouping is six deployment units: Commerce (catalog/search/offer/cart/orders), Fulfilment (payment/delivery/notifications), Institution Integration (integration/event bus), Platform Management (software catalog/license/platform administration), Platform Access (gateway/identity/institution registry), and Observability (audit). Co-hosting is an operational packaging choice and does not merge ownership. Extraction is permitted when measured load, security isolation, or operational evidence requires it; independent deployability remains a requirement of the logical contexts.

## 4. Technology decision posture

| Capability | Current posture | Required gate |
|---|---|---|
| ACCSystem relational database | PostgreSQL or MySQL temporary alternatives | migration/portability assessment before final selection |
| ACCore database | MySQL owner direction | institution release compatibility verification |
| Message broker | unspecified; choose a durable at-least-once broker baseline through platform review | ordering, replay, DLQ, schema evolution, operations test |
| Search engine | unspecified; choose a versioned index baseline through platform review | reindex, freshness, tenant isolation, recovery test |
| Orchestrator/cloud | not imposed | capacity, security, residency, cost, and DR review |

Changing the ACCSystem database or broker later is not cost-free: migrations, contract compatibility, replay semantics, operational tooling, and performance characteristics must be assessed.

## 5. ACCore release integrity and provenance

The platform records release ID, semantic version, supported package form, source revision, build inputs, builder identity, build timestamp, dependency lock/reference, SBOM reference, artifact digest, and release signature. A SHA-256 digest detects artifact changes; it does not prove source-code integrity or detect an altered source/build process. Releases therefore require signed provenance/attestation from a trusted build pipeline, with verification before publication. ACCore reports its deployed release ID, source/build fingerprint, and configuration fingerprint through a signed health/status exchange. A mismatch or local modification generates a platform notification and engineering audit event; the institution remains responsible for its deployment and local modifications, while the platform owns release metadata, signing policy, and verification tooling.

## 6. Operational gates

Availability, latency, workload, capacity, RTO/RPO, retention, residency, PCI scope, and provider capabilities are controlled parameters, not invented targets. Production launch requires assigned owners, measured definitions, monitoring, runbooks, backup/restore evidence, and legal/provider/security review where applicable. This document does not certify production readiness.
