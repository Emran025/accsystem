# Deployment View — ACC Ecosystem

**Status:** PROPOSED ARCHITECTURAL BASELINE — explicit owner directions are recorded where available; unresolved architecture, physical storage, infrastructure, and provider choices remain open or configurable.

## 1. Boundary and ownership

ACCore is institution-controlled ERP software. Each institution may deploy it as one integrated package or as separate Backend and Frontend applications; packaging is a release option, not a platform ownership decision. The ACCore Backend may run on-premises or in a public cloud managed by the institution and may be internet-reachable where permitted. ACCSystem hosts the marketplace, order, payment-record, license, and platform data required for e-commerce. ACCSystem never becomes the source of truth for ACCore product or inventory data.

ACCore uses MySQL under the current owner direction. ACCSystem relational storage may use PostgreSQL or MySQL as temporary alternatives; the engine is not an architectural contract. **Proposed logical rule under ADR-012 (which remains `PROPOSED`):** each bounded context owns its data schema and migrations, with no direct cross-context database access even inside a co-hosted deployment unit. ADR-012 leaves physical isolation `OPEN`: a dedicated schema in a shared database versus separate logical databases or instances needs an owner/operations choice; this view selects none.

**Storage decision for this review:** keep the ACCSystem physical engine unselected until migration/portability, workload, backup/restore, residency, and operations evidence is reviewed; PostgreSQL and MySQL remain valid alternatives. The proposed logical ownership rule does not choose physical partitioning, a database server/cluster arrangement, or vendor-specific DDL. ACCore's MySQL owner direction is not evidence that ACCSystem must share its engine.

## 2. Connectivity baseline

**Connectivity baseline (PROPOSED under ADR-015):** firewalled institutions default to an outbound-initiated authenticated ACCore connector; polling, long-polling or a persistent channel may be selected by operations, and protected inbound remains optional. Both modes target one logical connector contract with Outbox/Inbox, scoped idempotency and correlation. Reservation recovery requires authoritative query/reconciliation keyed by `idempotency_key` and/or `reservation_id` where the institution contract supports it, or an explicitly approved callback. The query endpoint, identifier mapping, callback mode/schema and availability remain OPEN under ADR-015/018; logical interaction arrows do not choose network initiation.

**Failure/recovery baseline (ADR-018 technical baseline; `OWNER-REVIEW-REQUIRED`, `NOT STAKEHOLDER-APPROVED`):** permitted local ACCore operations may continue during connectivity loss. Under the documented listing-availability requirement, stale or disconnected listings are hidden or marked unavailable; the exact institution status code and update contract are not selected here. A reservation without authoritative outcome remains `UNKNOWN`; no payment is authorized until every required reservation is authoritatively `ACCEPTED`. Retry only after definitive resolution or durable evidence of non-dispatch, using the same idempotency key; if no agreed query/callback channel is available, wait and escalate rather than infer an outcome.

## 3. Logical contexts and deployment units

Under the proposed ADR-012 baseline, the 17 ACCSystem bounded contexts are distinct logical owners of data and contracts. The proposed initial grouping is six deployment units: Commerce (catalog/search/offer/cart/orders), Fulfilment (payment/delivery/notifications), Institution Integration (integration/event bus), Platform Management (software catalog/license/platform administration), Platform Access (gateway/identity/institution registry), and Observability (audit). Co-hosting is an operational packaging choice and does not merge logical ownership. Physical database/schema/instance separation remains open as specified in §1. Extraction is permitted when measured load, security isolation, or operational evidence requires it; independent deployability remains a requirement of the proposed logical contexts.

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
