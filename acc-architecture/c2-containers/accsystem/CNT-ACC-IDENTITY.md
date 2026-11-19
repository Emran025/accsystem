# CNT-ACC-IDENTITY — Identity & Access

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Selected

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-IDENTITY |
| **Purpose** | Manages platform user authentication, session lifecycle, role-based access control, and institution membership mapping for all ACCSystem users and service accounts. |
| **Scope Boundary** | Owns platform identity, auth, roles, and sessions. Does NOT own institution-local ERP users (those remain in CNT-ACR-ORGUSERS). License entitlements are owned by CNT-ACC-LICENSE, not Identity. |

CONFIRMED (idea.md §3.1): "Identity & Access — هوية مستخدمي ACCSystem، المصادقة، حالات الحسابات، العضويات، الأدوار والصلاحيات، جلسات الخدمة والرموز."
CONFIRMED (idea.md §14, ADR-010): "فصل Software Catalog وLicense Management وIdentity."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-APIGATEWAY | Inbound | Requests token validation and user identity on every authenticated request |
| CNT-ACC-PLATFORMADMIN | Inbound | Requests role changes, account lifecycle, JIT access grants |
| CNT-ACC-INSTREG | Outbound | Checks institution existence for membership validation |
| CNT-ACC-AUDIT | Outbound | Publishes all auth events, session events, role changes |
| CNT-ACC-EVENTBUS | Outbound | Publishes PlatformUserActivated/Suspended/Reactivated, PlatformRoleGranted/Revoked events |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Auth protocol | CONFIRMED (idea.md §9) | OAuth 2.0 Client Credentials for service-to-service |
| Token format | UNKNOWN | JWT or opaque — not specified. OWNER_UNASSIGNED. |
| MFA | CONFIRMED (idea.md §9) | Required for platform admin and support accounts |
| Encryption | CONFIRMED (idea.md §9) | Sensitive data encrypted at rest; TLS in transit |

---

## 4. Data Owned

- Platform user accounts (identity, status, contact)
- Institution membership records (which platform users belong to which institution)
- Role and permission assignments
- Session records and token blacklist
- Authentication audit events

Does NOT own: ERP-local user records (ACCore), license entitlements (CNT-ACC-LICENSE).

CONFIRMED (idea.md §3.1): "حسابات المنصة وعضوياتها وأدوارها وسجلات المصادقة؛ ولا يملك مستخدمي ERP المحليين."

---

## 5. Interfaces

- Provides: Token validation endpoint (consumed by CNT-ACC-APIGATEWAY)
- Provides: Role/permission lookup for downstream authorization checks
- Consumes: No external auth providers specified (UNKNOWN — SSO/SAML integration possibility not stated in idea.md)
- Event: Publishes to CNT-ACC-EVENTBUS on user lifecycle and role changes

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Identity service down | Gateway rejects all authenticated requests; public endpoints remain available |
| Token store unavailable | Cannot validate tokens; requests fail-closed (reject) |
| Token replay attack | Token blacklist checked on every validation; short token TTL limits exposure — CONFIRMED (idea.md §9) |
| Stale session | Session revocation propagated to blacklist; new requests re-validate |

---

## 7. Security

- CONFIRMED (idea.md §9): MFA for admin accounts; least-privilege; RBAC/ABAC
- CONFIRMED (idea.md §11, ADR-011): All admin and support privilege grants logged in audit trail
- CONFIRMED (idea.md §9): Token storage must be secure in client apps; no secrets embedded in mobile apps
- CONFIRMED (idea.md §9): "فصل استحقاق المنتج عن صلاحيات المستخدم" — License ≠ permission

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Auth success rate, token validation latency. Targets: UNKNOWN |
| Scaling | Critical path — every request hits Identity for token validation; high throughput required |
| Risk | Single point of failure for all authenticated access; must be highly available |

---

## 9. C3 Disposition

**SELECTED for C3 decomposition.** Components:
- CMP-IDN-AUTH — Authentication Service
- CMP-IDN-RBAC — Role & Permission Manager
- CMP-IDN-SESSION — Session & Token Manager
- CMP-IDN-TENANCY — Tenant/Institution Membership Manager

See: `c3-components/CNT-ACC-IDENTITY/`
