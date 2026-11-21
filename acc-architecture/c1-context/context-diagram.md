# C1 System Context — ACCSystem Platform

**System:** `SYS-ACCSYSTEM` — ACCSystem Platform
**Viewpoint:** C1 — System Context
**Canonical view:** This is the single canonical C1 context diagram for ACCSystem.

> ACCSystem is shown as one black-box software system. This C1 view shows its people, client systems, and external providers; it does not expose any internal containers or C3 components. The system boundary and direct relationships are drawn from [`SYS-ACCSYSTEM.md`](systems/SYS-ACCSYSTEM.md). The internal container decomposition belongs in [the canonical C2 diagram](../c2-containers/accsystem/container-diagram.md).

```mermaid
flowchart LR
    BUYER["ACT-INDIVIDUAL\nIndividual Buyer"]
    EMP["ACT-INST-EMPLOYEE\nInstitution Employee / Seller"]
    IADMIN["ACT-INST-ADMIN\nInstitution Administrator"]
    PADMIN["ACT-PLATFORM-ADMIN\nPlatform Administrator"]
    SUPPORT["ACT-SUPPORT-STAFF\nPlatform Support Staff"]
    SUP["ACT-DELIVERY-SUPERVISOR\nDelivery Supervisor"]
    COURIER["ACT-COURIER\nCourier / Delivery Agent"]
    VISITOR["ACT-VISITOR\nPublic Portal Visitor"]
    COM["SYS-ACCOMMERCE\nACCommerce"]
    CORE["SYS-ACCORE\nACCore per institution"]
    MGT["SYS-ACMANAGEMENT\nACManagement Portal"]
    MS["SYS-ACCMARED-SUP\nACCMared Supervisor"]
    MC["SYS-ACCMARED-COU\nACCMared Courier"]
    PAY["EXT-PAYMENT-PROVIDER\nExternal Payment Provider"]
    CDN["EXT-PACKAGE-CDN\nSoftware Package CDN"]
    ACC["SYS-ACCSYSTEM\nACCSystem Platform\nBlack-box system"]

    BUYER -->|browse, cart, checkout, tracking| COM
    COM -->|catalog, cart, checkout, order APIs| ACC
    EMP -->|institution product and order work| CORE
    IADMIN -->|ERP and marketplace administration| CORE
    PADMIN -->|platform administration and license issuance| MGT
    SUPPORT -->|scoped support sessions| MGT
    SUP -->|dispatch and delivery monitoring| MS
    COURIER -->|task status and proof of delivery| MC
    VISITOR -->|public catalog and downloads| MGT
    CORE -->|publication events and license validation| ACC
    ACC -->|reservation/order commands; mode policy-gated| CORE
    MGT -->|public, license, admin, and support APIs| ACC
    MS -->|dispatch and status events| ACC
    MC -->|task and status APIs| ACC
    ACC -->|authorization, capture, and refund| PAY
    PAY -->|payment webhooks| ACC
    ACC -->|signed package distribution| CDN
```

> **Arrow convention and approval:** This drawing follows the reversible technical convention recorded in ADR-020 (arrows indicate the interaction initiator, not exclusive data flow). ADR-020 remains `OWNER-REVIEW-REQUIRED` and `NOT STAKEHOLDER-APPROVED`; this diagram does not imply approval. ACCore connectivity mode remains policy-gated under ADR-015.

**Coverage at this level:** one ACCSystem black-box system, eight people/actor nodes, and seven external system/service nodes. There are no `CNT-*` containers or `CMP-*` components in this C1 diagram.
