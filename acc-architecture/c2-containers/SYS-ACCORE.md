# SYS-ACCORE — ACCore (Per-Institution ERP)

**Viewpoint:** C1 System Context  
**Level:** C1 — System  
**Label convention:** `CONFIRMED (idea.md §X.X)` | `ASSUMPTION` | `PROPOSAL` | `UNKNOWN`

---

## 1. Identity

| Field | Value |
|-------|-------|
| **ID** | SYS-ACCORE |
| **Name** | ACCore (Per-Institution ERP) |
| **Role in ecosystem** | Independent, institution-owned ERP system; each institution operates its own ACCore instance with its own backend and database. ACCore is the source of truth for institution product data, inventory, sales/procurement, finance, and user/org management. It also embeds a Commerce Workspace (marketplace client) and a Platform Connector for integration with ACCSystem. |
| **Scope boundary** | Owns and operates: institution-local product master, inventory, sales & procurement, finance/accounting, organization & users, outbox/inbox messaging, commerce workspace UI, and platform connector. Does **NOT** own: marketplace product listings (ACCSystem owns the published projection), central order records (ACCSystem owns these), platform-level identity (ACCSystem Identity & Access), or any other institution's data. |

> [!IMPORTANT]
> **CONFIRMED (idea.md §4, ADR-002):** Each institution operates an **independent** ACCore instance. No cross-institution shared ERP database. ACCore is institution-owned, not platform-operated.

---

## 2. Actors and Users of This System

| Actor ID | Name | Interaction | Label |
|----------|------|-------------|-------|
| ACT-INST-EMPLOYEE | Institution Employee / Seller | Uses ACCore for ERP operations (product management, inventory, sales, procurement) and accesses the Commerce Workspace to browse/buy from the marketplace | CONFIRMED (idea.md §4.1) |
| ACT-INST-ADMIN | Institution Administrator | Manages ACCore configuration, users, roles, ERP settings; triggers license validation; accesses ACManagement for license management (via ACCSystem) | CONFIRMED (idea.md §2.1, §4.1) |

> [!NOTE]
> ACT-PLATFORM-ADMIN and ACT-SUPPORT-STAFF do **not** directly manage ACCore. Any support access to institution data requires explicit, scoped, time-limited authorization per ADR-011 and idea.md §9.

---

## 3. External Systems Consumed

| External System ID | Name | Purpose | Protocol | Label |
|-------------------|------|---------|----------|-------|
| SYS-ACCSYSTEM | ACCSystem Platform | Product publication, inventory reservation, order event receipt, license validation | REST+Events / TLS | CONFIRMED (idea.md §4.3) |

> [!NOTE]
> ACCore's **primary integration posture is outbound-initiated**: the Platform Connector (CNT-ACR-CONNECTOR) polls or pushes outbound events to ACCSystem, and initiates online calls for license validation. Where an approved deployment selects protected inbound, the Connector may expose a secure inbound endpoint for authorized commands/events; otherwise the logical boundary uses outbound polling, long-polling or a persistent channel. Authentication and certificate/token identity binding are policy-selected under ADR-015, and all modes route exclusively through the Connector. ACCSystem does **not** directly access ACCore's internal database or any internal service other than the Connector endpoint. Integration is exclusively via documented interfaces (ADR-005).

---

## 4. Connections to Other Platform Systems

| System ID | Direction | Protocol | Purpose | Label |
|-----------|-----------|----------|---------|-------|
| SYS-ACCSYSTEM (CNT-ACC-INTEGRATION) | Outbound (async events) | TLS + Event / REST | Publish ProductListingPublished/Updated/Withdrawn events; send StockAvailabilityChanged events via Outbox/Connector | CONFIRMED (idea.md §6.3, §7.1, ADR-005) |
| SYS-ACCSYSTEM (CNT-ACC-INTEGRATION) | Inbound to Connector endpoint (authorized commands/events) | TLS + REST / policy-selected OAuth 2.0 Client Credentials or mTLS | Receive ReservationRequested commands; receive OrderConfirmed events; receive return/cancellation commands — all routed via CNT-ACR-CONNECTOR inbound endpoint only; never to internal ACCore services. Exact mode is an onboarding/security gate under ADR-015. | CONFIRMED boundary; authentication mode PROPOSED/approval-required |
| SYS-ACCSYSTEM (CNT-ACC-LICENSE) | Outbound (periodic sync) | REST / TLS for validation; token-operation transport OPEN | License validation uses `IF-ACC-LICENSE-VALIDATE`; offline entitlement issuance/retrieval is a separate license-owned operation, with delivery interface/channel, receiver and acknowledgement OPEN | Validation and offline-token capability CONFIRMED (idea.md §4.3, ADR-014); delivery contract OPEN |
| SYS-ACCSYSTEM (CNT-ACC-CART / CNT-ACC-ORDERS) | Bidirectional (via Commerce Workspace) | REST/HTTPS | Institution employee browses catalog, creates cart/order through ACCSystem Commerce APIs | CONFIRMED (idea.md §4.1, ADR-003) |

---

## 5. Key Responsibilities

### What ACCore OWNS
- `CONFIRMED (idea.md §4.1)` Product Master — source of truth for all institution product definitions, attributes, images, internal codes
- `CONFIRMED (idea.md §4.1)` Inventory & Warehousing — actual inventory levels, reservations (local), warehouse movements
- `CONFIRMED (idea.md §4.1)` Sales & Procurement — local buy/sell operations, supplier records, purchase/sales orders
- `CONFIRMED (idea.md §4.1)` Finance / Accounting — journal entries, invoices, payables/receivables, financial reconciliation per institution rules
- `CONFIRMED (idea.md §4.1)` Organization & Users — institution employees, local roles, branch structure, local settings
- `CONFIRMED (idea.md §4.1)` Outbox / Inbox — transactional message reliability for integration events
- `CONFIRMED (idea.md §4.2)` Offline operational capability for local ERP functions when ACCSystem is unreachable

### What ACCore does NOT OWN
- `CONFIRMED (idea.md §3.1)` Marketplace product listings — ACCSystem owns the published projection
- `CONFIRMED (idea.md §5)` Central order records — ACCSystem Order Domain
- `CONFIRMED (idea.md §3.1)` Platform-level user identity — ACCSystem Identity & Access
- `CONFIRMED (idea.md §3.1)` Other institutions' data — zero cross-institution data sharing at DB level

---

## 6. Technology Stack / Hosting Form

| Aspect | Value | Label |
|--------|-------|-------|
| Hosting form | Per-institution independent instance; may be cloud-hosted by platform or self-hosted by institution | UNKNOWN — open decision (idea.md §12: "ACCore hosting form") |
| Backend style | Multi-module application with private database per institution | CONFIRMED (idea.md §4, §4.2, ADR-002) |
| Database isolation | Each ACCore instance has its own DB; no shared DB across institutions | CONFIRMED (idea.md §4.2) |
| Offline capability | ACCore can execute core local functions without ACCSystem connectivity; messages queued in Outbox for resend on reconnect | CONFIRMED (idea.md §4.2) |
| Specific tech stack | UNKNOWN — not specified in idea.md |

> [!WARNING]
> The hosting form (platform-hosted vs. institution self-hosted) is an **OPEN DECISION** (idea.md §12). This affects operational responsibility boundaries, SLA scope, and update/upgrade lifecycle. Must be resolved before Phase 1 institution onboarding design.
>
> - **Consequence if unresolved:** Ambiguous responsibility for security patching, backup/restore, uptime guarantees, and connectivity requirements.
> - **Resolution evidence needed:** Business model decision from project owner.
> - **Owner:** OWNER_UNASSIGNED
> - **Revisit trigger:** Before Phase 1 finalization.

---

## 7. Open Decisions Affecting This System

Sourced from idea.md §12:

| Decision | Consequence if Unresolved | Label |
|----------|--------------------------|-------|
| ACCore hosting form (cloud-hosted by platform vs. self-hosted by institution) | Ambiguous SLA, security patch, backup/restore responsibilities | UNKNOWN |
| Financial record commitment point (which order state triggers ACCore ERP journal entry) | Risk of double-entry or missing entries if trigger point is undefined | UNKNOWN |
| Offline license validation strategy (signed entitlement token vs. online-only) | Affects ACCore's ability to operate during connectivity loss | UNKNOWN — ADR-014 proposed but not finalized |
| ACCSystem offline behavior (what ACCore can do during ACCSystem outage) | Vague offline promises risk operational disruption | UNKNOWN |

---

## 8. C2 Disposition — Containers

ACCore is decomposed into **8 containers** in the C2 layer (all institution-internal; platform defines the integration boundary, not ACCore internals):

| Container ID | Name | C2 Doc | Note |
|-------------|------|--------|------|
| CNT-ACR-PRODUCTMASTER | Product Master | `c2-containers/accore/CNT-ACR-PRODUCTMASTER.md` | Source of truth for product data |
| CNT-ACR-INVENTORY | Inventory & Warehousing | `c2-containers/accore/CNT-ACR-INVENTORY.md` | Local inventory, reservations |
| CNT-ACR-SALES | Sales & Procurement | `c2-containers/accore/CNT-ACR-SALES.md` | Local buy/sell operations |
| CNT-ACR-FINANCE | Finance / Accounting | `c2-containers/accore/CNT-ACR-FINANCE.md` | Financial records per institution |
| CNT-ACR-ORGUSERS | Organization & Users | `c2-containers/accore/CNT-ACR-ORGUSERS.md` | Local employee/role management |
| CNT-ACR-COMMERCE | Commerce Workspace | `c2-containers/accore/CNT-ACR-COMMERCE.md` | Embedded marketplace client UI |
| CNT-ACR-CONNECTOR | Platform Connector | `c2-containers/accore/CNT-ACR-CONNECTOR.md` | ACCSystem integration adapter |
| CNT-ACR-OUTBOX | Outbox / Inbox | `c2-containers/accore/CNT-ACR-OUTBOX.md` | Outbox/Inbox with at-least-once delivery attempts and duplicate-safe recovery; downstream completion is not unconditional |

> [!NOTE]
> C2 decomposition of ACCore is EXCEPTION-scoped for all internal ERP modules — the platform architecture defines the **integration boundary**, not ACCore internals (which are institution-owned). CNT-ACR-CONNECTOR is IN_PROGRESS.
>
> This document does not claim 100% completeness, stakeholder approval, or production readiness.

---

*Last updated: 2026-11-15 | Source: idea.md v1.1*
