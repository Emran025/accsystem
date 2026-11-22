# C4 Diagram Overlay — Registry-Driven C1 Portfolio and C2 Overlays

**Status:** PROPOSED documentation overlay on ACC Final-v3; Mermaid source only. The registry and source documents are authoritative. This file does not change system membership or ownership.

**C1 scope note:** The portfolio diagram below uses the registered system nodes directly. It is a landscape view, not an approval of a new ownership or transport relationship. The separate focal-system context sections are intentionally partial views of their named system and must be read with their cited source records.

## Evidence and modeling notes

- Canonical IDs come from `registry/elements.json`; registered systems, containers, and components are not inferred from folder names.
- `SYS-ACCECOSYSTEM` is the portfolio/landscape boundary; the six named operational ACC systems are shown as separate C1 boundaries.
- ACCore is institution-controlled and owns ERP/inventory master data. ACCSystem owns marketplace records and projections/snapshots only.
- Logical relationships are labeled only where the source views/specifications document them; concrete transport is left unspecified unless documented.
- A relationship shown as `logical integration` is not a synchronous or deployment guarantee.

> [!NOTE]
> **Arrow convention:** Arrows show the **logical interaction initiator**. An arrow from A to B means A initiates the request or message to B; it does not specify physical network-connection initiation. Response data, callbacks, and events may flow in either direction and are not separately depicted unless explicitly labelled. Transport mode is governed separately by ADR-015 and institution policy. This is the reversible technical baseline in ADR-020, not stakeholder approval; owner review remains open.

## C1 — System Landscape

### C1-PORTFOLIO — ACC Ecosystem Portfolio

```mermaid
flowchart LR
  subgraph ECO["SYS-ACCECOSYSTEM — ACC Ecosystem Portfolio"]
    SYS_ACCSYSTEM["SYS-ACCSYSTEM\nACCSystem Platform"]
    SYS_ACCORE["SYS-ACCORE\nACCore (per-institution ERP)"]
    SYS_ACCOMMERCE["SYS-ACCOMMERCE\nACCommerce"]
    SYS_ACMANAGEMENT["SYS-ACMANAGEMENT\nACManagement Portal"]
    SYS_ACCMARED_SUP["SYS-ACCMARED-SUP\nACCMared Supervisor"]
    SYS_ACCMARED_COU["SYS-ACCMARED-COU\nACCMared Courier"]
  end
  ACT["ACTORS — buyers, institution users, platform/support, delivery roles"]
  PAY["EXT-PAYMENT-PROVIDER — external payment provider(s)"]
  CDN["EXT-PACKAGE-CDN — package CDN/object storage"]
  ACT -->|documented user interactions| SYS_ACCOMMERCE
  SYS_ACCOMMERCE -->|marketplace/order logical integration| SYS_ACCSYSTEM
  SYS_ACCSYSTEM -->|connector/API/event logical integration| SYS_ACCORE
  SYS_ACCSYSTEM -->|platform management interfaces| SYS_ACMANAGEMENT
  SYS_ACCSYSTEM -->|delivery/order interfaces| SYS_ACCMARED_SUP
  SYS_ACCSYSTEM -->|delivery/order interfaces| SYS_ACCMARED_COU
  SYS_ACCSYSTEM -->|payment interface| PAY
  SYS_ACMANAGEMENT -->|software distribution links| CDN
```

**Sources:** `registry/elements.json`, `registry/decomposition-map.json`, `decisions/ADR-001.md`, `ADR-002.md`, `ADR-004.md`, `ADR-005.md`, `ADR-008.md`, `ADR-009.md`, `supporting-views/interface-contracts.md`.

### C1-SYS-ACCECOSYSTEM — ACC Ecosystem Portfolio context

```mermaid
flowchart LR
  SYS_ACCECOSYSTEM["SYS-ACCECOSYSTEM\nACC Ecosystem Portfolio"]
  ACT["ACTORS — registry-listed human actors"]
  AS["SYS-ACCSYSTEM — ACCSystem Platform"]
  CORE["SYS-ACCORE — ACCore (per-institution ERP)"]
  COM["SYS-ACCOMMERCE — ACCommerce"]
  MGT["SYS-ACMANAGEMENT — ACManagement Portal"]
  MS["SYS-ACCMARED-SUP — ACCMared Supervisor"]
  MC["SYS-ACCMARED-COU — ACCMared Courier"]
  PAY["EXT-PAYMENT-PROVIDER — External Payment Provider(s)"]
  CDN["EXT-PACKAGE-CDN — Software Package CDN/Object Storage"]
  SYS_ACCECOSYSTEM --> SYS_ACCSYSTEM
  SYS_ACCECOSYSTEM --> SYS_ACCORE
  SYS_ACCECOSYSTEM --> SYS_ACCOMMERCE
  SYS_ACCECOSYSTEM --> SYS_ACMANAGEMENT
  SYS_ACCECOSYSTEM --> SYS_ACCMARED_SUP
  SYS_ACCECOSYSTEM --> SYS_ACCMARED_COU
  ACT --> SYS_ACCECOSYSTEM
  SYS_ACCSYSTEM --> PAY
  MGT --> CDN
```
**System:** `SYS-ACCECOSYSTEM` — `ACC Ecosystem Portfolio`. **Status:** `PRESENT-INCOMPLETE` (literal coverage only; semantic/owner review remains open). **Source:** `00-discovery/discovery-report.md`.

### C1-SYS-ACCSYSTEM — ACCSystem Platform context
The canonical single-system context is [`context-diagram.md`](context-diagram.md). This section links to that black-box view rather than maintaining a second C1 diagram. The boundary, actor, and external-system records remain in [`systems/SYS-ACCSYSTEM.md`](systems/SYS-ACCSYSTEM.md). **Status:** scope and registry coverage are recorded; owner review of arrow semantics remains open.

### C1-SYS-ACCORE — ACCore (per-institution ERP) context

```mermaid
flowchart LR
  SYS_ACCORE["SYS-ACCORE\nACCore (per-institution ERP)"]
  ACT["ACTORS — relevant registry-listed roles"]
  AS["SYS-ACCSYSTEM — ACCSystem Platform"]
  COM["SYS-ACCOMMERCE — ACCommerce"]
  MGT["SYS-ACMANAGEMENT — ACManagement Portal"]
  MS["SYS-ACCMARED-SUP — ACCMared Supervisor"]
  MC["SYS-ACCMARED-COU — ACCMared Courier"]
  PAY["EXT-PAYMENT-PROVIDER — External Payment Provider(s)"]
  CDN["EXT-PACKAGE-CDN — Software Package CDN/Object Storage"]
  SYS_ACCORE -->|institution-controlled connector/API/event integration| AS
  SYS_ACCORE -->|institution users and ERP operations| ACT
```
**System:** `SYS-ACCORE` — `ACCore (per-institution ERP)`. **Status:** `PRESENT-INCOMPLETE` (literal coverage only; semantic/owner review remains open). **Source:** `c1-context/systems/SYS-ACCORE.md`.

### C1-SYS-ACCOMMERCE — ACCommerce context

```mermaid
flowchart LR
  SYS_ACCOMMERCE["SYS-ACCOMMERCE\nACCommerce"]
  ACT["ACTORS — relevant registry-listed roles"]
  AS["SYS-ACCSYSTEM — ACCSystem Platform"]
  CORE["SYS-ACCORE — ACCore (per-institution ERP)"]
  MGT["SYS-ACMANAGEMENT — ACManagement Portal"]
  MS["SYS-ACCMARED-SUP — ACCMared Supervisor"]
  MC["SYS-ACCMARED-COU — ACCMared Courier"]
  PAY["EXT-PAYMENT-PROVIDER — External Payment Provider(s)"]
  CDN["EXT-PACKAGE-CDN — Software Package CDN/Object Storage"]
  ACT -->|buyer interaction| SYS_ACCOMMERCE
  SYS_ACCOMMERCE -->|marketplace/order logical integration| AS
```
**System:** `SYS-ACCOMMERCE` — `ACCommerce`. **Status:** `PRESENT-INCOMPLETE` (literal coverage only; semantic/owner review remains open). **Source:** `c1-context/systems/SYS-ACCOMMERCE.md`.

### C1-SYS-ACMANAGEMENT — ACManagement Portal context

```mermaid
flowchart LR
  SYS_ACMANAGEMENT["SYS-ACMANAGEMENT\nACManagement Portal"]
  ACT["ACTORS — relevant registry-listed roles"]
  AS["SYS-ACCSYSTEM — ACCSystem Platform"]
  CORE["SYS-ACCORE — ACCore (per-institution ERP)"]
  COM["SYS-ACCOMMERCE — ACCommerce"]
  MS["SYS-ACCMARED-SUP — ACCMared Supervisor"]
  MC["SYS-ACCMARED-COU — ACCMared Courier"]
  PAY["EXT-PAYMENT-PROVIDER — External Payment Provider(s)"]
  CDN["EXT-PACKAGE-CDN — Software Package CDN/Object Storage"]
  ACT -->|admin/support interaction| SYS_ACMANAGEMENT
  SYS_ACMANAGEMENT -->|platform management interfaces| AS
  SYS_ACMANAGEMENT -->|software download links| CDN
```
**System:** `SYS-ACMANAGEMENT` — `ACManagement Portal`. **Status:** `PRESENT-INCOMPLETE` (literal coverage only; semantic/owner review remains open). **Source:** `c1-context/systems/SYS-ACMANAGEMENT.md`.

### C1-SYS-ACCMARED-SUP — ACCMared Supervisor context

```mermaid
flowchart LR
  SYS_ACCMARED_SUP["SYS-ACCMARED-SUP\nACCMared Supervisor"]
  ACT["ACTORS — relevant registry-listed roles"]
  AS["SYS-ACCSYSTEM — ACCSystem Platform"]
  CORE["SYS-ACCORE — ACCore (per-institution ERP)"]
  COM["SYS-ACCOMMERCE — ACCommerce"]
  MGT["SYS-ACMANAGEMENT — ACManagement Portal"]
  MC["SYS-ACCMARED-COU — ACCMared Courier"]
  PAY["EXT-PAYMENT-PROVIDER — External Payment Provider(s)"]
  CDN["EXT-PACKAGE-CDN — Software Package CDN/Object Storage"]
  ACT -->|delivery supervisor interaction| SYS_ACCMARED_SUP
  SYS_ACCMARED_SUP -->|delivery/order logical integration| AS
```
**System:** `SYS-ACCMARED-SUP` — `ACCMared Supervisor`. **Status:** `PRESENT-INCOMPLETE` (literal coverage only; semantic/owner review remains open). **Source:** `c1-context/systems/SYS-ACCMARED-SUP.md`.

### C1-SYS-ACCMARED-COU — ACCMared Courier context

```mermaid
flowchart LR
  SYS_ACCMARED_COU["SYS-ACCMARED-COU\nACCMared Courier"]
  ACT["ACTORS — relevant registry-listed roles"]
  AS["SYS-ACCSYSTEM — ACCSystem Platform"]
  CORE["SYS-ACCORE — ACCore (per-institution ERP)"]
  COM["SYS-ACCOMMERCE — ACCommerce"]
  MGT["SYS-ACMANAGEMENT — ACManagement Portal"]
  MS["SYS-ACCMARED-SUP — ACCMared Supervisor"]
  PAY["EXT-PAYMENT-PROVIDER — External Payment Provider(s)"]
  CDN["EXT-PACKAGE-CDN — Software Package CDN/Object Storage"]
  ACT -->|courier interaction| SYS_ACCMARED_COU
  SYS_ACCMARED_COU -->|delivery/order logical integration| AS
```
**System:** `SYS-ACCMARED-COU` — `ACCMared Courier`. **Status:** `PRESENT-INCOMPLETE` (literal coverage only; semantic/owner review remains open). **Source:** `c1-context/systems/SYS-ACCMARED-COU.md`.

## C2 — Container views

Each view is registry-derived. Containers are shown inside the owning system boundary; a co-deployment or shared platform does not imply shared data ownership.
### C2-SYS-ACCSYSTEM — containers of ACCSystem Platform

This overlay is a **registry-derived cross-check**, not a competing canonical graph. It shows the 17 registered ACCSystem containers and a limited set of source-supported logical interactions. The canonical ACCSystem C2 container graph, including its original relationships and supporting external/client context, is [`../c2-containers/accsystem/container-diagram.md`](../c2-containers/accsystem/container-diagram.md). The overlay's narrower relationship selection is not a claim that omitted interactions do not exist; source container records remain authoritative for detailed collaborators. Owner review of relationship semantics remains open.

```mermaid
flowchart TB
  subgraph SYS_ACCSYSTEM["SYS-ACCSYSTEM\nACCSystem Platform — system boundary"]
    CNT_ACC_APIGATEWAY["CNT-ACC-APIGATEWAY\nAPI Gateway / BFF"]
    CNT_ACC_IDENTITY["CNT-ACC-IDENTITY\nIdentity & Access"]
    CNT_ACC_INSTREG["CNT-ACC-INSTREG\nInstitution Registry"]
    CNT_ACC_INTEGRATION["CNT-ACC-INTEGRATION\nInstitution Integration Gateway"]
    CNT_ACC_CATALOG["CNT-ACC-CATALOG\nCatalog & Publication"]
    CNT_ACC_SEARCH["CNT-ACC-SEARCH\nSearch & Discovery"]
    CNT_ACC_OFFER["CNT-ACC-OFFER\nOffer / Price / Availability"]
    CNT_ACC_CART["CNT-ACC-CART\nCart & Checkout"]
    CNT_ACC_ORDERS["CNT-ACC-ORDERS\nOrder Management"]
    CNT_ACC_PAYMENT["CNT-ACC-PAYMENT\nPayment Orchestration"]
    CNT_ACC_DELIVERY["CNT-ACC-DELIVERY\nDelivery Management"]
    CNT_ACC_NOTIFICATIONS["CNT-ACC-NOTIFICATIONS\nNotifications"]
    CNT_ACC_AUDIT["CNT-ACC-AUDIT\nAudit & Observability"]
    CNT_ACC_SOFTCAT["CNT-ACC-SOFTCAT\nSoftware Catalog & Release Distribution"]
    CNT_ACC_LICENSE["CNT-ACC-LICENSE\nLicense & Entitlement Management"]
    CNT_ACC_PLATFORMADMIN["CNT-ACC-PLATFORMADMIN\nPlatform Administration & Support"]
    CNT_ACC_EVENTBUS["CNT-ACC-EVENTBUS\nEvent Bus / Message Broker"]
  end
  CNT_ACC_APIGATEWAY -->|documented logical interaction| CNT_ACC_IDENTITY
  CNT_ACC_APIGATEWAY -->|documented logical interaction| CNT_ACC_CART
  CNT_ACC_CATALOG -->|documented logical interaction| CNT_ACC_SEARCH
  CNT_ACC_CART -->|documented logical interaction| CNT_ACC_ORDERS
  CNT_ACC_ORDERS -->|documented logical interaction| CNT_ACC_INTEGRATION
  CNT_ACC_ORDERS -->|documented logical interaction| CNT_ACC_PAYMENT
  CNT_ACC_ORDERS -->|documented logical interaction| CNT_ACC_DELIVERY
  CNT_ACC_ORDERS -->|documented logical interaction| CNT_ACC_EVENTBUS
  CNT_ACC_CATALOG -->|documented logical interaction| CNT_ACC_EVENTBUS
  CNT_ACC_LICENSE -->|documented logical interaction| CNT_ACC_EVENTBUS
```
**Scope:** `SYS-ACCSYSTEM`. **Registry containers:** 17. **Source basis:** each container `doc` in `registry/elements.json`; relationships are limited to documented logical interactions.

### C2-SYS-ACCORE — containers of ACCore (per-institution ERP)

```mermaid
flowchart TB
  subgraph SYS_ACCORE["SYS-ACCORE\nACCore (per-institution ERP) — system boundary"]
    CNT_ACR_PRODUCTMASTER["CNT-ACR-PRODUCTMASTER\nProduct Master (ACCore)"]
    CNT_ACR_INVENTORY["CNT-ACR-INVENTORY\nInventory & Warehousing (ACCore)"]
    CNT_ACR_SALES["CNT-ACR-SALES\nSales & Procurement (ACCore)"]
    CNT_ACR_FINANCE["CNT-ACR-FINANCE\nFinance / Accounting (ACCore)"]
    CNT_ACR_ORGUSERS["CNT-ACR-ORGUSERS\nOrganization & Users (ACCore)"]
    CNT_ACR_COMMERCE["CNT-ACR-COMMERCE\nCommerce Workspace (ACCore)"]
    CNT_ACR_CONNECTOR["CNT-ACR-CONNECTOR\nPlatform Connector (ACCore)"]
    CNT_ACR_OUTBOX["CNT-ACR-OUTBOX\nOutbox / Inbox (ACCore)"]
  end
  CNT_ACR_COMMERCE -->|documented logical interaction| CNT_ACR_PRODUCTMASTER
  CNT_ACR_COMMERCE -->|documented logical interaction| CNT_ACR_INVENTORY
  CNT_ACR_CONNECTOR -->|documented logical interaction| CNT_ACR_OUTBOX
  CNT_ACR_CONNECTOR -->|documented logical interaction| CNT_ACR_INVENTORY
  CNT_ACR_CONNECTOR -->|documented logical interaction| CNT_ACR_SALES
```
**Scope:** `SYS-ACCORE`. **Registry containers:** 8. **Source basis:** each container `doc` in `registry/elements.json`; relationships are limited to documented logical interactions.

### C2-SYS-ACCOMMERCE — containers of ACCommerce

```mermaid
flowchart TB
  subgraph SYS_ACCOMMERCE["SYS-ACCOMMERCE\nACCommerce — system boundary"]
    CNT_ACE_MOBILEAPP["CNT-ACE-MOBILEAPP\nACCommerce Mobile / Web App"]
  end
```
**Scope:** `SYS-ACCOMMERCE`. **Registry containers:** 1. **Source basis:** each container `doc` in `registry/elements.json`; relationships are limited to documented logical interactions.

### C2-SYS-ACMANAGEMENT — containers of ACManagement Portal

```mermaid
flowchart TB
  subgraph SYS_ACMANAGEMENT["SYS-ACMANAGEMENT\nACManagement Portal — system boundary"]
    CNT_ACM_PUBLIC["CNT-ACM-PUBLIC\nACManagement Public Portal"]
    CNT_ACM_ADMIN["CNT-ACM-ADMIN\nACManagement Protected Admin Console"]
  end
  CNT_ACM_PUBLIC -->|documented logical interaction| CNT_ACM_ADMIN
```
**Scope:** `SYS-ACMANAGEMENT`. **Registry containers:** 2. **Source basis:** each container `doc` in `registry/elements.json`; relationships are limited to documented logical interactions.

### C2-SYS-ACCMARED-SUP — containers of ACCMared Supervisor

```mermaid
flowchart TB
  subgraph SYS_ACCMARED_SUP["SYS-ACCMARED-SUP\nACCMared Supervisor — system boundary"]
    CNT_AMD_SUPERVISOR["CNT-AMD-SUPERVISOR\nACCMared Supervisor Desktop App"]
  end
```
**Scope:** `SYS-ACCMARED-SUP`. **Registry containers:** 1. **Source basis:** each container `doc` in `registry/elements.json`; relationships are limited to documented logical interactions.

### C2-SYS-ACCMARED-COU — containers of ACCMared Courier

```mermaid
flowchart TB
  subgraph SYS_ACCMARED_COU["SYS-ACCMARED-COU\nACCMared Courier — system boundary"]
    CNT_AMD_COURIER["CNT-AMD-COURIER\nACCMared Courier Mobile App"]
  end
```
**Scope:** `SYS-ACCMARED-COU`. **Registry containers:** 1. **Source basis:** each container `doc` in `registry/elements.json`; relationships are limited to documented logical interactions.

## Registry and source links

- Registry: `registry/elements.json`, `registry/decomposition-map.json`, `registry/architecture-manifest.json`.
- Ownership and boundaries: `decisions/ADR-001.md`, `ADR-002.md`, `ADR-004.md`, `ADR-008.md`, `ADR-009.md`.
- Commerce invariants: `functions/specs/FN-ORD-CHECKOUT.md`, `FN-ORD-RESERVE.md`, `FN-PAY-AUTHORIZE.md`, `supporting-views/dynamic-purchase-flow.md`.
- Existing C3 views remain in their canonical paths under `c3-components/`; their IDs are checked in the coverage matrix.
