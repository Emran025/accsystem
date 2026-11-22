# C2 System container  — ACCSystem Platform

**System:** `SYS-ACCSYSTEM` — ACCSystem Platform
**Viewpoint:** C2 — System container 
**Canonical view:** This is the single canonical C2 context diagram for ACCSystem.

> ACCSystem is shown as one black-box software system. This C2 view shows its people, client systems, and external providers; it does not expose any internal containers or C3 components. The system boundary and direct relationships are drawn from [`SYS-ACCSYSTEM.md`](systems/SYS-ACCSYSTEM.md). The internal container decomposition belongs in [the canonical C2 diagram](../c2-containers/accsystem/container-diagram.md).


```mermaid
flowchart LR
    
    EMP["ACT-INST-EMPLOYEE\nInstitution Employee / Seller"]
    IADMIN["ACT-INST-ADMIN\nInstitution Administrator"]

    BUYER["ACT-INDIVIDUAL\nIndividual Buyer"]
    PADMIN["ACT-PLATFORM-ADMIN\nPlatform Administrator"]
    SUPPORT["ACT-SUPPORT-STAFF\nPlatform Support Staff"]
    SUP["ACT-DELIVERY-SUPERVISOR\nDelivery Supervisor"]
    COURIER["ACT-COURIER\nCourier / Delivery Agent"]
    VISITOR["ACT-VISITOR\nPublic Portal Visitor"]

    subgraph SYSTEMS["External Software Systems & Services"]
        direction LR
            COM["SYS-ACCOMMERCE\nACCommerce"]
            CORE["SYS-ACCORE\nACCore per institution"]
            MGT["SYS-ACMANAGEMENT\nACManagement Portal"]
            MS["SYS-ACCMARED-SUP\nACCMared Supervisor"]
            MC["SYS-ACCMARED-COU\nACCMared Courier"]
            ACC["SYS-ACCSYSTEM\nACCSystem Platform\nBlack-box system"]
    end

    CDN["EXT-PACKAGE-CDN\nSoftware Package CDN"]
    PAY["EXT-PAYMENT-PROVIDER\nExternal Payment Provider"]


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
    ACC -->|signed package distribution| CDN
    PAY -->|payment webhooks| ACC
    ACC -->|authorization, capture, and refund| PAY
```

> **Arrow convention and approval:** This drawing follows the reversible technical baseline recorded in ADR-020: arrows indicate the **logical interaction initiator**, not exclusive data flow or physical network-connection initiation. Responses/callbacks may flow back; ACCore transport remains separately policy-gated under ADR-015 (outbound-initiated default for firewalled institutions, protected inbound optional). ADR-020 remains `OWNER-REVIEW-REQUIRED` and `NOT STAKEHOLDER-APPROVED`; this diagram does not imply approval.

**Coverage at this level:** one ACCSystem black-box system, eight people/actor nodes, and seven external system/service nodes. There are no `CNT-*` containers or `CMP-*` components in this C2 diagram.
