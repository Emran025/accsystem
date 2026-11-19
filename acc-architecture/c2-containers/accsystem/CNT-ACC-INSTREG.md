# CNT-ACC-INSTREG — Institution Registry

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-INSTREG |
| **Purpose** | Maintains the registry of all institutions participating in the ACCSystem marketplace — their identifiers, activation status, integration configuration, and contact points. |
| **Scope Boundary** | Owns institution registration data only. Does NOT own institution ERP data, inventory, or financial records. |

CONFIRMED (idea.md §3.1): "Institution Registry — تعريف المؤسسات، معرف المؤسسة، حالة التفعيل، نقاط الاتصال، إعدادات التكامل."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-IDENTITY | Inbound | Institution existence check for membership validation |
| CNT-ACC-INTEGRATION | Inbound | Retrieves institution integration configuration (connector endpoints, auth keys) |
| CNT-ACC-PLATFORMADMIN | Inbound | Institution onboarding, activation, deactivation workflows |
| CNT-ACC-AUDIT | Outbound | Logs all institution registration changes |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Data store | UNKNOWN | Relational or document DB — not specified. OWNER_UNASSIGNED. |

---

## 4. Data Owned

- Institution record: `{platform_institution_id, name, status, activation_date, contact_points}`
- Integration configuration: connector endpoint URLs, signing keys, allowed event types
- Institution metadata: onboarding state, tier/plan (UNKNOWN: plan structure not defined)

Does NOT own: ERP data, product data, financial data, local user data.

---

## 5. Interfaces

- Provides: Institution lookup by platform_institution_id (consumed by Identity, Integration, Catalog, Orders)
- Provides: Institution registration/update API (consumed by CNT-ACC-PLATFORMADMIN)

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Registry unavailable | Integration gateway cannot validate institution; publication and reservation flows pause |
| Stale institution config | Integration uses cached config; staleness TTL to be defined (UNKNOWN) |

---

## 7. Security

- Institution signing keys stored securely, not in plaintext — ASSUMPTION
- Access to registry update API restricted to CNT-ACC-PLATFORMADMIN — CONFIRMED (idea.md §9): institution isolation
- Tenant ID validation on all requests — CONFIRMED (idea.md §9)

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Availability critical for integration flows; lookup latency should be low (cacheable) |
| Scaling | Read-heavy; caching at consumer level PROPOSAL |

---

## 9. C3 Disposition

**EXCEPTION:** Registry/CRUD service with well-understood data model; complexity does not justify C3 decomposition at this stage. Revisit trigger: if multi-tier tenancy or complex approval workflows are added.
