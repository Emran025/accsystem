# CNT-ACM-ADMIN — ACManagement Protected Admin Console

**Parent:** SYS-ACMANAGEMENT | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACM-ADMIN |
| **Purpose** | Authenticated admin web console for authorized platform users. Provides license management, platform user lifecycle management, admin/support privilege management, and JIT support session initiation — all via ACCSystem backend APIs. |
| **Scope Boundary** | Authenticated zone only. All backend operations delegated to ACCSystem services (CNT-ACC-LICENSE, CNT-ACC-PLATFORMADMIN, CNT-ACC-IDENTITY). Does NOT own any data or business logic. |

CONFIRMED (idea.md §2.1.1): "منطقة محمية للمخولين لإدارة تراخيص المنتجات والمؤسسات، واستحقاقات الوحدات."
CONFIRMED (idea.md §3.1.1): "يجب أن تكون ACManagement واجهة عميل للخدمات الإدارية، لا أن تتجاوزها."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| ACT-PLATFORM-ADMIN | Inbound | Full admin access |
| ACT-SUPPORT-STAFF | Inbound | Scoped support session initiation |
| ACT-INST-ADMIN | Inbound | Institution-scoped license management (scope: ASSUMPTION) |
| CNT-ACC-APIGATEWAY → CNT-ACC-LICENSE | Outbound | License issuance, renewal, management |
| CNT-ACC-APIGATEWAY → CNT-ACC-PLATFORMADMIN | Outbound | User lifecycle, privilege management |
| CNT-ACC-APIGATEWAY → CNT-ACC-IDENTITY | Outbound | Authentication |

---

## 3. Technology Stack

UNKNOWN — web framework not specified. OWNER_UNASSIGNED.

---

## 4. Security

CONFIRMED (idea.md §9): MFA enforced for admin accounts. Strictly separate URL paths from public portal. All operations logged via CNT-ACC-AUDIT.

---

## 5. C3 Disposition

**EXCEPTION:** Authenticated admin web console; frontend decomposition deferred. Key workflows documented in `supporting-views/security-view.md` and `supporting-views/dynamic-license-flow.md`.


---

## 6. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Backend administrative service unavailable | Informative maintenance banner displayed; form inputs preserved in browser session |
| Network disconnect during multi-step configuration wizard | Wizard state persisted in local session store; user can resume without data loss |
| Authorization token expiry | Session expiration warning dialog; re-authentication preserves current edit state |

---

## 7. Operations and Reliability

- **Deployment:** Containerized web application deployed in high-availability configuration across multiple availability zones.
- **Observability:** Real-time logging of all administrative actions with actor identity and IP address.

---

## 8. Open Risks and Decisions

- Integration of hardware security key (FIDO2 / WebAuthn) for administrative accounts — `OPEN` (`OWNER_UNASSIGNED`).
