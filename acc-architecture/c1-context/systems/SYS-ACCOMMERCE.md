# SYS-ACCOMMERCE — ACCommerce Individual Shopping App

**Label convention:** `CONFIRMED (idea.md §X)` | `ASSUMPTION` | `PROPOSAL` | `UNKNOWN`

---

## 1. Identity

| Field | Value |
|---|---|
| **System ID** | SYS-ACCOMMERCE |
| **Parent** | SYS-ACCECOSYSTEM |
| **Role in Ecosystem** | Client application providing the individual buyer's shopping experience — browse, search, cart, checkout, order tracking, and license management via the ACCSystem platform services. |
| **Scope Boundary** | Owns: individual buyer UX and client-side state. Does NOT own: catalog data, order processing, payment logic, or license records (all backend in ACCSystem). |

CONFIRMED (idea.md §0, §2.1): "ACCommerce — تجربة الفرد للتصفح والشراء وإدارة طلباته."

---

## 2. Actors and Users

| Actor ID | Name | Interaction |
|---|---|---|
| ACT-INDIVIDUAL | Individual Buyer | Primary user — browses, searches, adds to cart, checks out, tracks orders |
| ACT-VISITOR | Public Portal Visitor | May browse catalog without authentication (unauthenticated view, if supported) |

CONFIRMED (idea.md §2.1, §7.2): Individual buyers use ACCommerce to browse and purchase from the marketplace.

---

## 3. External Systems Consumed

ACCommerce does not connect directly to external systems. All external integrations (payment, CDN) are mediated by ACCSystem.

---

## 4. Connections to Other Platform Systems

| System | Direction | Protocol | Purpose |
|---|---|---|---|
| SYS-ACCSYSTEM (via CNT-ACC-APIGATEWAY) | Outbound | HTTPS/TLS REST API | Catalog query (IF-ACC-CATALOG-QUERY), order creation (IF-ACC-ORDER-CREATE), cart, checkout, license validation, notifications |

CONFIRMED (idea.md §7.2): "يبحث الفرد عبر ACCommerce؛ وتقرأ النتائج من Search/Catalog في ACCSystem."

---

## 5. Key Responsibilities

- Browse and search the marketplace catalog
- Manage individual shopping cart
- Initiate and track checkout and order lifecycle
- View order status, delivery updates, and notifications
- Manage individual account, profile, and addresses
- View entitlements/licenses for software products purchased

**Does NOT own:**
- Product data, inventory, or pricing (source at ACCore via ACCSystem Catalog)
- Payment processing logic (at CNT-ACC-PAYMENT)
- Delivery orchestration (at CNT-ACC-DELIVERY)

---

## 6. Technology Stack / Hosting

| Aspect | Status | Note |
|---|---|---|
| Platform type | CONFIRMED (idea.md §2.1) | "تطبيق هاتف / واجهة عميل" — mobile app and/or web client |
| Technology | UNKNOWN | Specific framework/language not specified. OWNER_UNASSIGNED. Revisit: before Phase 2 implementation. |
| Distribution | UNKNOWN | App store distribution vs. progressive web app — not specified. |

---

## 7. Open Decisions Affecting This System

| Decision | Status |
|---|---|
| ACCommerce license model | CONFIRMED (idea.md §12): "الأصل أن يكون تنزيل التطبيق والتسوق الفردي متاحين دون ترخيص مؤسسي" — individual shopping requires no institutional license. Any paid subscription model is a separate business decision, UNKNOWN. |
| Shared Commerce Core with ACCore | PROPOSAL (ADR-003): ACCommerce and ACCore Commerce Workspace share the same Commerce APIs from ACCSystem. Implementation form (shared library vs. shared service) is UNKNOWN. |

---

## 8. C2 Disposition

| Container ID | Name | C3? |
|---|---|---|
| CNT-ACE-MOBILEAPP | ACCommerce Mobile/Web App | No — UI client, C3 decomposition deferred to frontend implementation planning |

See: `c2-containers/accommerce/CNT-ACE-MOBILEAPP.md`
