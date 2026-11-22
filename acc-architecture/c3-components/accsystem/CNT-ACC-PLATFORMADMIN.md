# CNT-ACC-PLATFORMADMIN — Platform Administration & Support

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception (Conditional)

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-PLATFORMADMIN |
| **Purpose** | Manages platform user lifecycle, admin/support privilege grants, approval workflows, and JIT (just-in-time) scoped support access. Acts as the workflow layer between ACManagement admin console and the Identity & Access service. |
| **Scope Boundary** | Owns approval workflows, privilege grant requests, support session scope definitions, and their audit trail. The actual identity/permission records live in CNT-ACC-IDENTITY. |

CONFIRMED (idea.md §3.1): "Platform Administration & Support — إدارة دورة حياة مستخدمي ACCSystem وعضويات الوصول والأدوار المركزية."
CONFIRMED (idea.md §14, ADR-011): "حسابات مسؤولي ACCSystem والدعم وإمكانية الوصول إلى بيانات مؤسسة تخضع لأقل صلاحية وموافقة/تفويض ونطاق زمني وسجل تدقيق."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACM-ADMIN | Inbound | Admin console triggers user management and privilege workflows |
| CNT-ACC-IDENTITY | Outbound | Applies role changes, account lifecycle changes after approval |
| CNT-ACC-INSTREG | Outbound | Institution context for scoped support access |
| CNT-ACC-EVENTBUS | Outbound | Publishes PlatformRoleGranted/Revoked, SupportAccessGranted/Expired/Revoked events |
| CNT-ACC-AUDIT | Outbound | Logs all privilege grant, approval, and support session events |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Approval workflow | UNKNOWN | Workflow engine or state machine — not specified. OWNER_UNASSIGNED. |

---

## 4. Data Owned

- Privilege grant requests and their approval state
- Support session records: `{session_id, staff_id, institution_id, purpose, scope, granted_at, expires_at, status}`
- Role assignment audit trail

Does NOT own: identity records (CNT-ACC-IDENTITY), license records (CNT-ACC-LICENSE).

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Approval workflow unavailable | Pending grants remain pending; no automatic escalation |
| Support session not expired on timeout | Scheduled cleanup job revokes expired sessions; alert ops |

---

## 6. Security

- CONFIRMED (idea.md §7.7, §9): MFA required for admin accounts; least-privilege; approval required for privilege escalation
- CONFIRMED (idea.md §9): "وصول الدعم — جلسات دعم مؤقتة ومحدودة بالمؤسسة والوظيفة والغرض"
- CONFIRMED (idea.md §11): Platform Admin & Support Audit monitored: "منح/سحب أدوار الامتياز، الموافقات المعلقة"

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Support session availability and response time for privilege grants. Targets: UNKNOWN |
| Risk | Open decision (§12): support session policy (per-session consent vs. pre-authorized) — OWNER_UNASSIGNED |

---

## 8. C3 Disposition

**EXCEPTION (Conditional):** Key security controls documented in `supporting-views/security-view.md`. C3 conditional — revisit when approval workflow engine and JIT-access implementation are planned (Phase 1).
