# CNT-ACC-LICENSE — License & Entitlement Management

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-LICENSE |
| **Purpose** | Issues, activates, manages, and validates licenses for ACC software products. Manages institutional `ISSUED → ACTIVATED → ACTIVE` and `ACTIVE → Suspended/Expired/Revoked` lifecycles, plus marketplace post-purchase `ACTIVE` licenses and can issue short-lived signed entitlement tokens for offline validation by ACCore. |
| **Scope Boundary** | Owns license records and entitlement state. Does NOT own user identity/permissions (CNT-ACC-IDENTITY) or platform admin workflows (CNT-ACC-PLATFORMADMIN). License ≠ permission. |

CONFIRMED (idea.md §3.1): "License & Entitlement Management — إصدار التراخيص وربطها بالمؤسسة/التثبيت والمنتج، وتفعيلها وتجديدها وتعليقها وإلغاؤها."
CONFIRMED (idea.md §14, ADR-010): "فصل Software Catalog وLicense Management وIdentity."
CONFIRMED (idea.md §1.1): "فصل ترخيص استخدام المنتج عن صلاحيات إدارة المستخدمين."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-ORDERS | Inbound (via event) | OrderConfirmed event triggers license issuance for software products |
| CNT-ACM-ADMIN | Inbound | Admin console issues/renews/manages licenses via API |
| CNT-ACR-CONNECTOR / CMP-CON-LICENSECHECK | Inbound | License validation requests (IF-ACC-LICENSE-VALIDATE); token issuance/refresh is a separate license-owned operation |
| CNT-ACC-EVENTBUS | Bidirectional | Subscribes to OrderConfirmed; publishes LicenseIssued/Activated/Renewed/Suspended/Revoked/Expired |
| CNT-ACC-IDENTITY | Outbound | Validates requesting user/service identity |
| CNT-ACC-AUDIT | Outbound | Logs all license lifecycle events |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Offline token signing | CONFIRMED (idea.md §4.3, §12) | Short-lived signed entitlement credential; mechanism UNKNOWN (JWT with asymmetric key PROPOSAL) |
| Key management | UNKNOWN | Signing key management technology not specified. OWNER_UNASSIGNED. |
| License model types | UNKNOWN (idea.md §12) | Per-institution, per-seat, per-unit, capacity-based — to be defined. OWNER_UNASSIGNED. |

---

## 4. Data Owned

- License records: `{license_id, workflow, institution_id + product_code OR buyer_id + product_id, publisher_institution_id (marketplace), units/seats, status, valid_from, valid_until, grace_policy_ref}`
- Activation records: `{activation_id, license_id, installation_id, activated_at}`
- Usage tracking records (UNKNOWN: specific usage metrics captured)
- Entitlement token issuance log

CONFIRMED (idea.md §3.1): "سجلات الترخيص والاستحقاقات والتفعيلات والاستخدام وحالة الصلاحية."

---

## 5. Interfaces

- **IF-ACC-LICENSE-VALIDATE** (provider): Institutional online validation for CNT-ACR-CONNECTOR/CMP-CON-LICENSECHECK; marketplace ACCommerce branch is proposed pending API Governance.
- Provides: License issuance/management API (consumed by CNT-ACM-ADMIN)
- Publishes: License lifecycle events via IF-ACC-EVENT-ENVELOPE
- Functions: FN-LIC-ACTIVATE, FN-LIC-VALIDATE

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| License validation unavailable (online) | Use a valid scoped cached token; after expiry restrict licensed functions unless applicable grace is approved. Preserve independently permitted local ERP operation. |
| License activation fails (order confirmed but activation failed) | Retry via event reprocessing; alert ops; order remains Confirmed |
| Token signing key compromise | Emergency key rotation procedure needed (UNKNOWN: key rotation process) |

---

## 7. Security

- CONFIRMED (idea.md §9): "فصل استحقاق المنتج عن صلاحيات المستخدم"
- CONFIRMED (idea.md §4.3): License validation does not expose ERP data to ACCSystem
- CONFIRMED (idea.md §14, ADR-014): Signed tokens prevent forgery; short TTL limits offline exposure
- Admin access to license management requires ACT-PLATFORM-ADMIN role — CONFIRMED

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "تراخيص قربت من الانتهاء، فشل التفعيل والتحقق، تجاوز المقاعد/السعة، محاولات استخدام وحدات غير مرخصة، وزمن استجابة خدمة الترخيص" |
| Risk | License model types undefined (open decision §12) — OWNER_UNASSIGNED |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-LIC-ISSUANCE — License Issuance & Activation
- CMP-LIC-ENTITLEMENT — Entitlement Evaluator
- CMP-LIC-LIFECYCLE — License Lifecycle Manager
- CMP-LIC-OFFLINE — Offline Credential Issuer

See: `c3-components/CNT-ACC-LICENSE/`
