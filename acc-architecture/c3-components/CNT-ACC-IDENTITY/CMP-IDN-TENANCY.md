# CMP-IDN-TENANCY — Tenant/Institution Membership Manager

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-IDN-TENANCY |
| **Parent Container** | CNT-ACC-IDENTITY |
| **Purpose** | Maps platform users to their institution memberships and provides institution-scoped identity context for authorization. Ensures that institutional users (ACT-INST-EMPLOYEE, ACT-INST-ADMIN) carry the correct platform_institution_id in their tokens and that cross-institution access is blocked. |
| **Scope Boundary** | Platform-level institution membership only. Does NOT manage ACCore-local employee roles (those remain in CNT-ACR-ORGUSERS). |

CONFIRMED (idea.md §2.1.1): "وإذا احتاج موظف المؤسسة إلى هوية موحدة للسوق، تُربط هويته بعضوية منصة محددة دون نقل صلاحيات ERP المحلية."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CMP-IDN-AUTH | Inbound | Fetches institution membership claims during token issuance |
| CNT-ACC-INSTREG | Outbound | Verifies institution exists and is active |
| CNT-ACC-PLATFORMADMIN | Inbound | Manages user-institution membership assignments |
| CNT-ACC-AUDIT | Outbound | Logs membership changes |

---

## 3. Behavior, Rules, and State

**Membership resolution:**
1. Given user_id → lookup institution memberships
2. Return `{platform_institution_id, role_in_institution}` for each institution the user belongs to
3. Token embeds institution membership as claims

**Rules:**
- A user may belong to multiple institutions (ASSUMPTION: possible for support staff assigned to multiple clients)
- Institution isolation: each request must carry and verify platform_institution_id — CONFIRMED (idea.md §9)
- Membership changes logged in audit trail

---

## 4. Data

| Data | Owned |
|---|---|
| Membership records: `{user_id, platform_institution_id, role, joined_at, status}` | CMP-IDN-TENANCY |

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Membership store unavailable | Cannot issue institution-scoped tokens; institutional users cannot authenticate |
| Institution deactivated | Membership lookups return empty; user loses institutional access |

---

## 6. Security

- CONFIRMED (idea.md §9): "تحقق من tenant_id في كل طلب؛ لا تعتمد على قيمة يرسلها العميل دون تحقق من الرمز والصلاحية"
- CONFIRMED (idea.md §9): Cross-institution data exposure is explicitly listed as a risk to prevent

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Membership lookup latency (called at every login). Cacheable. Targets: UNKNOWN |


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Institution scope resolution | Valid institution token presented | Tenant context resolved; queries automatically scoped to `institution_id` |
| Cross-tenant boundary breach | Request contains institution header mismatching authenticated token | Rejection with HTTP 403 `TENANT_MISMATCH`; security audit logged |
| Platform admin super-tenant | Platform admin role token presented | Cross-tenant access permitted with mandatory audit log emission |
