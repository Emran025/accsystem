# مراجعة ذرّية ودلالية لمتطلبات PH-01 إلى PH-04

**الدورة:** ARH-2026-11-21-C3<br>
**الأساس:** `254d43bb239dcf2849e01818855751133e8154f0` (`origin/main` عند بدء الدورة الثالثة)<br>**الدورة السابقة:** ARH-2026-11-21-C2؛ تفاصيلها محفوظة في تاريخ Git.<br>
**حدود العدّ:** التصنيف أدناه يخص صفوف `SREQ` فقط؛ المتطلبات الرئيسية ليست داخلة في مجاميع الذرية الفرعية.<br>
**تنبيه:** هذا سجل مراجعة للمسودات، وليس اعتماداً أو دليلاً على التنفيذ أو نجاح الاختبارات.

## النتيجة الإجمالية

يعرض السجل الحالي تصنيف **219 من 219** صف SREQ بعد تفكيك AUTH-001 وLIC-001 مع حفظ المصدر التاريخي، إضافة إلى تفكيك AUD-001 في الدورة السابقة. من 17 finding تفكيك حية أُعيد تقييمها، عولج AUTH-001 وLIC-001؛ بقيت 15 حالة `SPLIT_REQUIRED` حية (ومنها MSG-002 بعد إعادة التصنيف). لم يُنفذ دمج؛ بقي DOP-004 مرشحاً واحداً دون إثبات تداخل كافٍ لدمجه، ولم تثبت ازدواجية DEN-003 فظل محجوباً بقرار ODEC-010. ظلت قرارات المالك والفجوات الأخرى مفتوحة.

| المرحلة | SREQ | ATOMIC | SPLIT_REQUIRED | MERGE_CANDIDATE | ARCHITECTURAL_CONSTRAINT | POLICY_RULE | ACCEPTANCE_CRITERION_ONLY | NEEDS_USE_CASE | DUPLICATE | OUT_OF_PHASE | BLOCKED_BY_OWNER_DECISION |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PH-01 — تأسيس المنصة | 88 | 14 | 11 | 0 | 13 | 14 | 3 | 22 | 0 | 0 | 11 |
| PH-02 — الكتالوج والاكتشاف والحجز | 45 | 14 | 4 | 0 | 8 | 10 | 0 | 1 | 0 | 0 | 8 |
| PH-03 — المخزون والطلبات والدفع وأحداث التسليم الخارجية | 59 | 8 | 3 | 0 | 8 | 6 | 0 | 18 | 0 | 0 | 16 |
| PH-04 — التسليم الداخلي عبر ACCMared | 27 | 7 | 0 | 1 | 3 | 3 | 0 | 1 | 0 | 0 | 12 |
| **الإجمالي** | **219** | **43** | **18** | **1** | **32** | **33** | **3** | **42** | **0** | **0** | **47** |

## سجل التصنيف الكامل

كل صف أدناه هو حكم تصنيفي واحد على SREQ بعينه بالحالة الراهنة بعد Cycle 3. أرقام الجدول تشمل ثلاثة صفوف تاريخية مصنفة `SPLIT_REQUIRED` رغم حالتها `RETIRED`: AUD-001 وAUTH-001 وLIC-001؛ أُنجز تفكيكها واحتُفظ بها للتتبع، ولا تدخل ضمن الـ15 finding الحي المتبقي.

| المرحلة | SREQ | المتطلب الرئيسي | العنوان | التصنيف | وثيقة المصدر |
|---|---|---|---|---|---|
| PH-01 | `SREQ-PH01-INST-001` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Unique stable institution ID | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-002` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Activation status | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-003` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Institution lookup for platform services | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-004` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Integration configuration and credential issuance | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-005` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Credential rotation without disruption | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-006` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Institution deactivation | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-AUTH-001` | `REQ-PH01-IDENTITY-AND-TRUST` | Authenticate platform users | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-007` | `REQ-PH01-IDENTITY-AND-TRUST` | Credential verification | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-008` | `REQ-PH01-IDENTITY-AND-TRUST` | Issue tokens with claims | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-002` | `REQ-PH01-IDENTITY-AND-TRUST` | MFA for privileged accounts | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-003` | `REQ-PH01-IDENTITY-AND-TRUST` | Short-lived tokens and revocation | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-004` | `REQ-PH01-IDENTITY-AND-TRUST` | Brute-force limiting | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-005` | `REQ-PH01-IDENTITY-AND-TRUST` | Fail-closed identity | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-AUTH-006` | `REQ-PH01-IDENTITY-AND-TRUST` | Link institution employee to platform membership | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md` |
| PH-01 | `SREQ-PH01-TEN-001` | `REQ-PH01-TENANT-ISOLATION` | Tenant derived from credential | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-TENANT-ISOLATION.md` |
| PH-01 | `SREQ-PH01-TEN-002` | `REQ-PH01-TENANT-ISOLATION` | Cross-tenant denial | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-TENANT-ISOLATION.md` |
| PH-01 | `SREQ-PH01-TEN-003` | `REQ-PH01-TENANT-ISOLATION` | Membership claims | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-TENANT-ISOLATION.md` |
| PH-01 | `SREQ-PH01-TEN-004` | `REQ-PH01-TENANT-ISOLATION` | Audited platform-wide access | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-TENANT-ISOLATION.md` |
| PH-01 | `SREQ-PH01-ADM-001` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | Account lifecycle administration | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-ADM-002` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | Role grant with approval | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-ADM-003` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | RBAC/ABAC authorization | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-ADM-004` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | ACManagement acts only as service client | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-ADM-005` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | Separate admin identities | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-ADM-006` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | Institution-admin console scope | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-SUP-001` | `REQ-PH01-SUPPORT-ACCESS` | Session scope | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-SUPPORT-ACCESS.md` |
| PH-01 | `SREQ-PH01-SUP-002` | `REQ-PH01-SUPPORT-ACCESS` | Authorization basis | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-SUPPORT-ACCESS.md` |
| PH-01 | `SREQ-PH01-SUP-003` | `REQ-PH01-SUPPORT-ACCESS` | Time limit and expiry | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-SUPPORT-ACCESS.md` |
| PH-01 | `SREQ-PH01-SUP-004` | `REQ-PH01-SUPPORT-ACCESS` | No privilege conferral | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-SUPPORT-ACCESS.md` |
| PH-01 | `SREQ-PH01-SUP-005` | `REQ-PH01-SUPPORT-ACCESS` | Least-privilege read-only default | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-SUPPORT-ACCESS.md` |
| PH-01 | `SREQ-PH01-SUP-006` | `REQ-PH01-SUPPORT-ACCESS` | Session events and audit | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-SUPPORT-ACCESS.md` |
| PH-01 | `SREQ-PH01-LIC-001` | `REQ-PH01-LICENSE-LIFECYCLE` | Issue institutional license | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-007` | `REQ-PH01-LICENSE-LIFECYCLE` | Reject ineligible issuance request | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-008` | `REQ-PH01-LICENSE-LIFECYCLE` | Create institutional license in ISSUED | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-002` | `REQ-PH01-LICENSE-LIFECYCLE` | Signed entitlement | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-003` | `REQ-PH01-LICENSE-LIFECYCLE` | Activation progression | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-004` | `REQ-PH01-LICENSE-LIFECYCLE` | Renew, suspend, revoke, expire | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-005` | `REQ-PH01-LICENSE-LIFECYCLE` | Propagation to ACCore | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-006` | `REQ-PH01-LICENSE-LIFECYCLE` | Entitlement is not permission | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LICV-001` | `REQ-PH01-LICENSE-VALIDATION` | Online institutional validation | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-002` | `REQ-PH01-LICENSE-VALIDATION` | Authenticated, scoped, no ERP data | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-003` | `REQ-PH01-LICENSE-VALIDATION` | Offline local verification | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-004` | `REQ-PH01-LICENSE-VALIDATION` | Expiry restricts licensed functions | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-005` | `REQ-PH01-LICENSE-VALIDATION` | Separate token issuance and refresh | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-006` | `REQ-PH01-LICENSE-VALIDATION` | Signing key custody and rotation | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-AUD-001` | `REQ-PH01-AUDIT-TRAIL` | Coverage of foundation operations | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-002` | `REQ-PH01-AUDIT-TRAIL` | Required audit fields | `ACCEPTANCE_CRITERION_ONLY` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-003` | `REQ-PH01-AUDIT-TRAIL` | Append-only and tamper-evident | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-004` | `REQ-PH01-AUDIT-TRAIL` | Audit unavailability policy | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-005` | `REQ-PH01-AUDIT-TRAIL` | Privacy-minimal payloads | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-006` | `REQ-PH01-AUDIT-TRAIL` | Restricted audit access | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-007` | `REQ-PH01-AUDIT-TRAIL` | Authentication audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-008` | `REQ-PH01-AUDIT-TRAIL` | Role-change audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-009` | `REQ-PH01-AUDIT-TRAIL` | Support-session audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-010` | `REQ-PH01-AUDIT-TRAIL` | Administrative-action audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-011` | `REQ-PH01-AUDIT-TRAIL` | Institution-change audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-012` | `REQ-PH01-AUDIT-TRAIL` | License-action audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-AUD-013` | `REQ-PH01-AUDIT-TRAIL` | Credential-change audit coverage | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md` |
| PH-01 | `SREQ-PH01-GW-001` | `REQ-PH01-GATEWAY-BOUNDARY` | TLS only | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-GATEWAY-BOUNDARY.md` |
| PH-01 | `SREQ-PH01-GW-002` | `REQ-PH01-GATEWAY-BOUNDARY` | Token verification without business logic | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-GATEWAY-BOUNDARY.md` |
| PH-01 | `SREQ-PH01-GW-003` | `REQ-PH01-GATEWAY-BOUNDARY` | Public/admin route separation | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-GATEWAY-BOUNDARY.md` |
| PH-01 | `SREQ-PH01-GW-004` | `REQ-PH01-GATEWAY-BOUNDARY` | Rate limiting | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-GATEWAY-BOUNDARY.md` |
| PH-01 | `SREQ-PH01-CONN-001` | `REQ-PH01-CORE-CONNECTIVITY` | Single logical contract | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md` |
| PH-01 | `SREQ-PH01-CONN-002` | `REQ-PH01-CORE-CONNECTIVITY` | Connectivity modes | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md` |
| PH-01 | `SREQ-PH01-CONN-003` | `REQ-PH01-CORE-CONNECTIVITY` | Policy-selected authentication | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md` |
| PH-01 | `SREQ-PH01-CONN-004` | `REQ-PH01-CORE-CONNECTIVITY` | Institution identity binding | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md` |
| PH-01 | `SREQ-PH01-CONN-005` | `REQ-PH01-CORE-CONNECTIVITY` | Schema and signature validation | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md` |
| PH-01 | `SREQ-PH01-CONN-006` | `REQ-PH01-CORE-CONNECTIVITY` | Institution connectivity state | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-CORE-CONNECTIVITY.md` |
| PH-01 | `SREQ-PH01-MSG-001` | `REQ-PH01-MESSAGE-RELIABILITY` | Atomic outbox | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-MSG-002` | `REQ-PH01-MESSAGE-RELIABILITY` | Idempotent inbox | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-MSG-003` | `REQ-PH01-MESSAGE-RELIABILITY` | Retry and dead-letter semantics | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-MSG-004` | `REQ-PH01-MESSAGE-RELIABILITY` | Per-key ordering | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-MSG-005` | `REQ-PH01-MESSAGE-RELIABILITY` | Event immutability | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-MSG-006` | `REQ-PH01-MESSAGE-RELIABILITY` | Common event envelope | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-IDEM-001` | `REQ-PH01-IDEMPOTENCY-AND-CORRELATION` | Stable scoped keys | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDEMPOTENCY-AND-CORRELATION.md` |
| PH-01 | `SREQ-PH01-IDEM-002` | `REQ-PH01-IDEMPOTENCY-AND-CORRELATION` | Correlation propagation | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDEMPOTENCY-AND-CORRELATION.md` |
| PH-01 | `SREQ-PH01-IDEM-003` | `REQ-PH01-IDEMPOTENCY-AND-CORRELATION` | Institution identity mapping | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDEMPOTENCY-AND-CORRELATION.md` |
| PH-01 | `SREQ-PH01-IDEM-004` | `REQ-PH01-IDEMPOTENCY-AND-CORRELATION` | Retention covers reconciliation | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDEMPOTENCY-AND-CORRELATION.md` |
| PH-01 | `SREQ-PH01-POL-001` | `REQ-PH01-POLICY-AND-OWNER-GATES` | Externalized thresholds | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-POLICY-AND-OWNER-GATES.md` |
| PH-01 | `SREQ-PH01-POL-002` | `REQ-PH01-POLICY-AND-OWNER-GATES` | Fail-closed activation | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-POLICY-AND-OWNER-GATES.md` |
| PH-01 | `SREQ-PH01-POL-003` | `REQ-PH01-POLICY-AND-OWNER-GATES` | Immutable policy snapshots | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-POLICY-AND-OWNER-GATES.md` |
| PH-01 | `SREQ-PH01-POL-004` | `REQ-PH01-POLICY-AND-OWNER-GATES` | Visible owner gates | `POLICY_RULE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-POLICY-AND-OWNER-GATES.md` |
| PH-01 | `SREQ-PH01-OBS-001` | `REQ-PH01-OBSERVABILITY-AND-RECOVERY` | Baseline metrics | `ACCEPTANCE_CRITERION_ONLY` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-OBSERVABILITY-AND-RECOVERY.md` |
| PH-01 | `SREQ-PH01-OBS-002` | `REQ-PH01-OBSERVABILITY-AND-RECOVERY` | Recovery objectives owned | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-OBSERVABILITY-AND-RECOVERY.md` |
| PH-01 | `SREQ-PH01-OBS-003` | `REQ-PH01-OBSERVABILITY-AND-RECOVERY` | Schema ownership and deployability | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-OBSERVABILITY-AND-RECOVERY.md` |
| PH-01 | `SREQ-PH01-OBS-004` | `REQ-PH01-OBSERVABILITY-AND-RECOVERY` | Secrets outside code | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-OBSERVABILITY-AND-RECOVERY.md` |
| PH-01 | `SREQ-PH01-REL-001` | `REQ-PH01-RELEASE-PROVENANCE` | Verification before Available | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-RELEASE-PROVENANCE.md` |
| PH-01 | `SREQ-PH01-REL-002` | `REQ-PH01-RELEASE-PROVENANCE` | Release record content | `ACCEPTANCE_CRITERION_ONLY` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-RELEASE-PROVENANCE.md` |
| PH-01 | `SREQ-PH01-REL-003` | `REQ-PH01-RELEASE-PROVENANCE` | Fingerprint reporting and mismatch | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-RELEASE-PROVENANCE.md` |
| PH-02 | `SREQ-PH02-PUB-001` | `REQ-PH02-PRODUCT-PUBLICATION` | Publishable field selection | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-PUBLICATION.md` |
| PH-02 | `SREQ-PH02-PUB-002` | `REQ-PH02-PRODUCT-PUBLICATION` | Atomic publication intent | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-PUBLICATION.md` |
| PH-02 | `SREQ-PH02-PUB-003` | `REQ-PH02-PRODUCT-PUBLICATION` | Monotonic version | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-PUBLICATION.md` |
| PH-02 | `SREQ-PH02-PUB-004` | `REQ-PH02-PRODUCT-PUBLICATION` | Reliable submission | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-PUBLICATION.md` |
| PH-02 | `SREQ-PH02-ING-001` | `REQ-PH02-LISTING-INGESTION` | Admission checks | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-ING-002` | `REQ-PH02-LISTING-INGESTION` | Pre-admission rejection leaves no listing | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-ING-003` | `REQ-PH02-LISTING-INGESTION` | Content validation | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-ING-004` | `REQ-PH02-LISTING-INGESTION` | Idempotent listing creation | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-ING-005` | `REQ-PH02-LISTING-INGESTION` | Listing identifier and receipt | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-ING-006` | `REQ-PH02-LISTING-INGESTION` | Audit of admission decisions | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-LCY-001` | `REQ-PH02-LISTING-LIFECYCLE` | Versioned update | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-LIFECYCLE.md` |
| PH-02 | `SREQ-PH02-LCY-002` | `REQ-PH02-LISTING-LIFECYCLE` | Withdrawal retains history | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-LIFECYCLE.md` |
| PH-02 | `SREQ-PH02-LCY-003` | `REQ-PH02-LISTING-LIFECYCLE` | Withdrawn listings not shown | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-LIFECYCLE.md` |
| PH-02 | `SREQ-PH02-REC-001` | `REQ-PH02-PUBLICATION-RECOVERY` | Search sync retry | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PUBLICATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-REC-002` | `REQ-PH02-PUBLICATION-RECOVERY` | Relay recovery | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PUBLICATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-REC-003` | `REQ-PH02-PUBLICATION-RECOVERY` | Index rebuild | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PUBLICATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-REC-004` | `REQ-PH02-PUBLICATION-RECOVERY` | Failed publication visibility | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PUBLICATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-DSC-001` | `REQ-PH02-PRODUCT-DISCOVERY` | Catalog query | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-DISCOVERY.md` |
| PH-02 | `SREQ-PH02-DSC-002` | `REQ-PH02-PRODUCT-DISCOVERY` | Indexed search | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-DISCOVERY.md` |
| PH-02 | `SREQ-PH02-DSC-003` | `REQ-PH02-PRODUCT-DISCOVERY` | Shared commerce core for both channels | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-DISCOVERY.md` |
| PH-02 | `SREQ-PH02-DSC-004` | `REQ-PH02-PRODUCT-DISCOVERY` | Tenant-scoped responses | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-DISCOVERY.md` |
| PH-02 | `SREQ-PH02-DSC-005` | `REQ-PH02-PRODUCT-DISCOVERY` | Multilingual listing fields | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-PRODUCT-DISCOVERY.md` |
| PH-02 | `SREQ-PH02-OFR-001` | `REQ-PH02-OFFER-AND-VISIBILITY` | Indicative snapshot with timestamp | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-OFFER-AND-VISIBILITY.md` |
| PH-02 | `SREQ-PH02-OFR-002` | `REQ-PH02-OFFER-AND-VISIBILITY` | Stock signal intake | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-OFFER-AND-VISIBILITY.md` |
| PH-02 | `SREQ-PH02-OFR-003` | `REQ-PH02-OFFER-AND-VISIBILITY` | Stale or disconnected hidden or labeled | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-OFFER-AND-VISIBILITY.md` |
| PH-02 | `SREQ-PH02-OFR-004` | `REQ-PH02-OFFER-AND-VISIBILITY` | Price from service not client | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-OFFER-AND-VISIBILITY.md` |
| PH-02 | `SREQ-PH02-OFR-005` | `REQ-PH02-OFFER-AND-VISIBILITY` | Revalidation requirement stated | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-OFFER-AND-VISIBILITY.md` |
| PH-02 | `SREQ-PH02-CHK-001` | `REQ-PH02-CHECKOUT-PREPARATION` | Buyer-scoped cart | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md` |
| PH-02 | `SREQ-PH02-CHK-002` | `REQ-PH02-CHECKOUT-PREPARATION` | Seller grouping | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md` |
| PH-02 | `SREQ-PH02-CHK-003` | `REQ-PH02-CHECKOUT-PREPARATION` | Checkout validation and snapshots | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md` |
| PH-02 | `SREQ-PH02-CHK-004` | `REQ-PH02-CHECKOUT-PREPARATION` | Idempotent checkout session | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md` |
| PH-02 | `SREQ-PH02-CHK-005` | `REQ-PH02-CHECKOUT-PREPARATION` | Stop at reservation boundary | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md` |
| PH-02 | `SREQ-PH02-CHK-006` | `REQ-PH02-CHECKOUT-PREPARATION` | Institution (B2B) checkout initiation | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-CHECKOUT-PREPARATION.md` |
| PH-02 | `SREQ-PH02-RSV-001` | `REQ-PH02-SELLER-RESERVATION` | Seller-scoped request identity | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-SELLER-RESERVATION.md` |
| PH-02 | `SREQ-PH02-RSV-002` | `REQ-PH02-SELLER-RESERVATION` | Atomic ACCore reservation | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-SELLER-RESERVATION.md` |
| PH-02 | `SREQ-PH02-RSV-003` | `REQ-PH02-SELLER-RESERVATION` | Accepted outcome content | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-SELLER-RESERVATION.md` |
| PH-02 | `SREQ-PH02-RSV-004` | `REQ-PH02-SELLER-RESERVATION` | Rejected outcome | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-SELLER-RESERVATION.md` |
| PH-02 | `SREQ-PH02-RSV-005` | `REQ-PH02-SELLER-RESERVATION` | Duplicate request | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-SELLER-RESERVATION.md` |
| PH-02 | `SREQ-PH02-RSV-006` | `REQ-PH02-SELLER-RESERVATION` | Aggregate outcome at the boundary | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-SELLER-RESERVATION.md` |
| PH-02 | `SREQ-PH02-RRC-001` | `REQ-PH02-RESERVATION-RECOVERY` | Timeout is UNKNOWN | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-RESERVATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-RRC-002` | `REQ-PH02-RESERVATION-RECOVERY` | Reconcile by key | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-RESERVATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-RRC-003` | `REQ-PH02-RESERVATION-RECOVERY` | Authoritative expiry only | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-RESERVATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-RRC-004` | `REQ-PH02-RESERVATION-RECOVERY` | Safe release of eligible holds | `POLICY_RULE` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-RESERVATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-RRC-005` | `REQ-PH02-RESERVATION-RECOVERY` | Unknown release reconciled | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-RESERVATION-RECOVERY.md` |
| PH-02 | `SREQ-PH02-RRC-006` | `REQ-PH02-RESERVATION-RECOVERY` | Escalation to review | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-RESERVATION-RECOVERY.md` |
| PH-03 | `SREQ-PH03-INV-001` | `REQ-PH03-INVENTORY-COMMITMENT` | Inventory authority stays at ACCore | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-INVENTORY-COMMITMENT.md` |
| PH-03 | `SREQ-PH03-INV-002` | `REQ-PH03-INVENTORY-COMMITMENT` | Commit on seller confirmation | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-INVENTORY-COMMITMENT.md` |
| PH-03 | `SREQ-PH03-INV-003` | `REQ-PH03-INVENTORY-COMMITMENT` | Commit failure is reconciled | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-INVENTORY-COMMITMENT.md` |
| PH-03 | `SREQ-PH03-INV-004` | `REQ-PH03-INVENTORY-COMMITMENT` | Buyer purchase does not command seller stock | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-INVENTORY-COMMITMENT.md` |
| PH-03 | `SREQ-PH03-INV-005` | `REQ-PH03-INVENTORY-COMMITMENT` | Warehouse reference handling | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-INVENTORY-COMMITMENT.md` |
| PH-03 | `SREQ-PH03-ORD-001` | `REQ-PH03-ORDER-AGGREGATE` | Split by seller | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-002` | `REQ-PH03-ORDER-AGGREGATE` | Idempotent order creation | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-003` | `REQ-PH03-ORDER-AGGREGATE` | State machine enforcement | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-004` | `REQ-PH03-ORDER-AGGREGATE` | Parent state is aggregate | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-005` | `REQ-PH03-ORDER-AGGREGATE` | Append-only history atomic with outbox | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-006` | `REQ-PH03-ORDER-AGGREGATE` | Policy and currency snapshot references | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-CNF-001` | `REQ-PH03-ORDER-CONFIRMATION` | Confirmation guards | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-CONFIRMATION.md` |
| PH-03 | `SREQ-PH03-CNF-002` | `REQ-PH03-ORDER-CONFIRMATION` | Atomic commit | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-CONFIRMATION.md` |
| PH-03 | `SREQ-PH03-CNF-003` | `REQ-PH03-ORDER-CONFIRMATION` | Immutable commercial snapshot | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-CONFIRMATION.md` |
| PH-03 | `SREQ-PH03-CNF-004` | `REQ-PH03-ORDER-CONFIRMATION` | Idempotent confirmation | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-CONFIRMATION.md` |
| PH-03 | `SREQ-PH03-CNF-005` | `REQ-PH03-ORDER-CONFIRMATION` | Recipient-scoped handoff | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-CONFIRMATION.md` |
| PH-03 | `SREQ-PH03-CNF-006` | `REQ-PH03-ORDER-CONFIRMATION` | Local record and accounting trigger | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-CONFIRMATION.md` |
| PH-03 | `SREQ-PH03-PAY-001` | `REQ-PH03-PAYMENT-ORCHESTRATION` | No payment before all holds accepted | `POLICY_RULE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PAY-002` | `REQ-PH03-PAYMENT-ORCHESTRATION` | Per-SellerOrder allocation | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PAY-003` | `REQ-PH03-PAYMENT-ORCHESTRATION` | Capture policy per seller | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PAY-004` | `REQ-PH03-PAYMENT-ORCHESTRATION` | Distinct money states | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PAY-005` | `REQ-PH03-PAYMENT-ORCHESTRATION` | Unknown payment outcome | `POLICY_RULE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PAY-006` | `REQ-PH03-PAYMENT-ORCHESTRATION` | Capture failure after confirmation | `POLICY_RULE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PAY-007` | `REQ-PH03-PAYMENT-ORCHESTRATION` | No raw card data | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-ORCHESTRATION.md` |
| PH-03 | `SREQ-PH03-PWH-001` | `REQ-PH03-PAYMENT-WEBHOOKS` | Webhook authentication | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-WEBHOOKS.md` |
| PH-03 | `SREQ-PH03-PWH-002` | `REQ-PH03-PAYMENT-WEBHOOKS` | Duplicate event handling | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-WEBHOOKS.md` |
| PH-03 | `SREQ-PH03-PWH-003` | `REQ-PH03-PAYMENT-WEBHOOKS` | Scoped mapping | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-WEBHOOKS.md` |
| PH-03 | `SREQ-PH03-PWH-004` | `REQ-PH03-PAYMENT-WEBHOOKS` | Provider isolation and breaker | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-WEBHOOKS.md` |
| PH-03 | `SREQ-PH03-PRC-001` | `REQ-PH03-PAYMENT-RECONCILIATION` | Resolve UNKNOWN | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-RECONCILIATION.md` |
| PH-03 | `SREQ-PH03-PRC-002` | `REQ-PH03-PAYMENT-RECONCILIATION` | Allocation-level matching | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-RECONCILIATION.md` |
| PH-03 | `SREQ-PH03-PRC-003` | `REQ-PH03-PAYMENT-RECONCILIATION` | Discrepancy classification | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-RECONCILIATION.md` |
| PH-03 | `SREQ-PH03-PRC-004` | `REQ-PH03-PAYMENT-RECONCILIATION` | Settlement evidence ingestion | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-PAYMENT-RECONCILIATION.md` |
| PH-03 | `SREQ-PH03-VRF-001` | `REQ-PH03-VOID-AND-REFUND` | Void vs refund distinction | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-VOID-AND-REFUND.md` |
| PH-03 | `SREQ-PH03-VRF-002` | `REQ-PH03-VOID-AND-REFUND` | Scoped idempotent operation | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-VOID-AND-REFUND.md` |
| PH-03 | `SREQ-PH03-VRF-003` | `REQ-PH03-VOID-AND-REFUND` | Refund within eligible amount | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-VOID-AND-REFUND.md` |
| PH-03 | `SREQ-PH03-VRF-004` | `REQ-PH03-VOID-AND-REFUND` | Refund failure handling | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-VOID-AND-REFUND.md` |
| PH-03 | `SREQ-PH03-CNC-001` | `REQ-PH03-CANCELLATION-COORDINATION` | Eligible cancellation requests | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-CANCELLATION-COORDINATION.md` |
| PH-03 | `SREQ-PH03-CNC-002` | `REQ-PH03-CANCELLATION-COORDINATION` | Per-SellerOrder compensation | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-CANCELLATION-COORDINATION.md` |
| PH-03 | `SREQ-PH03-CNC-003` | `REQ-PH03-CANCELLATION-COORDINATION` | Independent partial outcomes | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-CANCELLATION-COORDINATION.md` |
| PH-03 | `SREQ-PH03-CNC-004` | `REQ-PH03-CANCELLATION-COORDINATION` | Cancellation notification and handoff | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-CANCELLATION-COORDINATION.md` |
| PH-03 | `SREQ-PH03-LDG-001` | `REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY` | Append-only payment facts | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY.md` |
| PH-03 | `SREQ-PH03-LDG-002` | `REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY` | Seller credit separate from capture | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY.md` |
| PH-03 | `SREQ-PH03-LDG-003` | `REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY` | Manual or external payment recorded | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY.md` |
| PH-03 | `SREQ-PH03-LDG-004` | `REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY` | Unresolved settlement visible | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY.md` |
| PH-03 | `SREQ-PH03-SAG-001` | `REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY` | Durable saga state | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY.md` |
| PH-03 | `SREQ-PH03-SAG-002` | `REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY` | Compensation only for confirmed effects | `POLICY_RULE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY.md` |
| PH-03 | `SREQ-PH03-SAG-003` | `REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY` | Confirmation write failure | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY.md` |
| PH-03 | `SREQ-PH03-SAG-004` | `REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY` | Review state not inferred | `POLICY_RULE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY.md` |
| PH-03 | `SREQ-PH03-EXD-001` | `REQ-PH03-EXTERNAL-DELIVERY-EVENTS` | Accept external delivery events | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-EXTERNAL-DELIVERY-EVENTS.md` |
| PH-03 | `SREQ-PH03-EXD-002` | `REQ-PH03-EXTERNAL-DELIVERY-EVENTS` | Normalize to common vocabulary | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-EXTERNAL-DELIVERY-EVENTS.md` |
| PH-03 | `SREQ-PH03-EXD-003` | `REQ-PH03-EXTERNAL-DELIVERY-EVENTS` | Stable shipment identity and idempotency | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-EXTERNAL-DELIVERY-EVENTS.md` |
| PH-03 | `SREQ-PH03-EXD-004` | `REQ-PH03-EXTERNAL-DELIVERY-EVENTS` | Pending delivery visibility | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-EXTERNAL-DELIVERY-EVENTS.md` |
| PH-03 | `SREQ-PH03-BOV-001` | `REQ-PH03-BUYER-ORDER-VISIBILITY` | Authorized status view | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-BUYER-ORDER-VISIBILITY.md` |
| PH-03 | `SREQ-PH03-BOV-002` | `REQ-PH03-BUYER-ORDER-VISIBILITY` | Notifications | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-BUYER-ORDER-VISIBILITY.md` |
| PH-03 | `SREQ-PH03-BOV-003` | `REQ-PH03-BUYER-ORDER-VISIBILITY` | Correlation traceability | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-BUYER-ORDER-VISIBILITY.md` |
| PH-03 | `SREQ-PH03-MLS-001` | `REQ-PH03-SOFTWARE-LICENSE-ISSUANCE` | Issue on OrderConfirmed | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SOFTWARE-LICENSE-ISSUANCE.md` |
| PH-03 | `SREQ-PH03-MLS-002` | `REQ-PH03-SOFTWARE-LICENSE-ISSUANCE` | Idempotent per order line | `POLICY_RULE` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SOFTWARE-LICENSE-ISSUANCE.md` |
| PH-03 | `SREQ-PH03-MLS-003` | `REQ-PH03-SOFTWARE-LICENSE-ISSUANCE` | Token follow-up recoverable | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SOFTWARE-LICENSE-ISSUANCE.md` |
| PH-03 | `SREQ-PH03-MLS-004` | `REQ-PH03-SOFTWARE-LICENSE-ISSUANCE` | Buyer validation path | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-SOFTWARE-LICENSE-ISSUANCE.md` |
| PH-04 | `SREQ-PH04-DEN-001` | `REQ-PH04-DELIVERY-ENABLEMENT` | Policy-gated enablement | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-ENABLEMENT.md` |
| PH-04 | `SREQ-PH04-DEN-002` | `REQ-PH04-DELIVERY-ENABLEMENT` | Provider-agnostic boundary | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-ENABLEMENT.md` |
| PH-04 | `SREQ-PH04-DEN-003` | `REQ-PH04-DELIVERY-ENABLEMENT` | No duplicate fulfilment per SellerOrder | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-ENABLEMENT.md` |
| PH-04 | `SREQ-PH04-SHP-001` | `REQ-PH04-SHIPMENT-CREATION` | Create from OrderConfirmed | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-SHIPMENT-CREATION.md` |
| PH-04 | `SREQ-PH04-SHP-002` | `REQ-PH04-SHIPMENT-CREATION` | Idempotent creation | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-SHIPMENT-CREATION.md` |
| PH-04 | `SREQ-PH04-SHP-003` | `REQ-PH04-SHIPMENT-CREATION` | Software-only orders | `POLICY_RULE` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-SHIPMENT-CREATION.md` |
| PH-04 | `SREQ-PH04-SHP-004` | `REQ-PH04-SHIPMENT-CREATION` | Pending Delivery with retry | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-SHIPMENT-CREATION.md` |
| PH-04 | `SREQ-PH04-DSP-001` | `REQ-PH04-DELIVERY-DISPATCH` | Unassigned queue | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-DISPATCH.md` |
| PH-04 | `SREQ-PH04-DSP-002` | `REQ-PH04-DELIVERY-DISPATCH` | Courier assignment | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-DISPATCH.md` |
| PH-04 | `SREQ-PH04-DSP-003` | `REQ-PH04-DELIVERY-DISPATCH` | Reassignment | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-DISPATCH.md` |
| PH-04 | `SREQ-PH04-DSP-004` | `REQ-PH04-DELIVERY-DISPATCH` | Thin client | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-DISPATCH.md` |
| PH-04 | `SREQ-PH04-CRO-001` | `REQ-PH04-COURIER-OPERATIONS` | Scoped courier access | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-COURIER-OPERATIONS.md` |
| PH-04 | `SREQ-PH04-CRO-002` | `REQ-PH04-COURIER-OPERATIONS` | Status updates validated server-side | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-COURIER-OPERATIONS.md` |
| PH-04 | `SREQ-PH04-CRO-003` | `REQ-PH04-COURIER-OPERATIONS` | Idempotent submission | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-COURIER-OPERATIONS.md` |
| PH-04 | `SREQ-PH04-POD-001` | `REQ-PH04-PROOF-OF-DELIVERY` | POD required to complete | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-PROOF-OF-DELIVERY.md` |
| PH-04 | `SREQ-PH04-POD-002` | `REQ-PH04-PROOF-OF-DELIVERY` | Tamper-evident POD | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-PROOF-OF-DELIVERY.md` |
| PH-04 | `SREQ-PH04-POD-003` | `REQ-PH04-PROOF-OF-DELIVERY` | POD data protection | `POLICY_RULE` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-PROOF-OF-DELIVERY.md` |
| PH-04 | `SREQ-PH04-OFS-001` | `REQ-PH04-OFFLINE-COURIER-SYNC` | Encrypted local queue | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-OFFLINE-COURIER-SYNC.md` |
| PH-04 | `SREQ-PH04-OFS-002` | `REQ-PH04-OFFLINE-COURIER-SYNC` | Idempotent sync with backoff | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-OFFLINE-COURIER-SYNC.md` |
| PH-04 | `SREQ-PH04-OFS-003` | `REQ-PH04-OFFLINE-COURIER-SYNC` | Stale offline update | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-OFFLINE-COURIER-SYNC.md` |
| PH-04 | `SREQ-PH04-DEX-001` | `REQ-PH04-DELIVERY-EXCEPTIONS` | Visible delivery exceptions | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-EXCEPTIONS.md` |
| PH-04 | `SREQ-PH04-DEX-002` | `REQ-PH04-DELIVERY-EXCEPTIONS` | Cancellation halts delivery | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-EXCEPTIONS.md` |
| PH-04 | `SREQ-PH04-DEX-003` | `REQ-PH04-DELIVERY-EXCEPTIONS` | Failure not inferred | `POLICY_RULE` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-EXCEPTIONS.md` |
| PH-04 | `SREQ-PH04-DOP-001` | `REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS` | Delivery events | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS.md` |
| PH-04 | `SREQ-PH04-DOP-002` | `REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS` | Notifications to parties | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS.md` |
| PH-04 | `SREQ-PH04-DOP-003` | `REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS` | Audit of delivery operations | `ATOMIC` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS.md` |
| PH-04 | `SREQ-PH04-DOP-004` | `REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS` | Operational indicators | `MERGE_CANDIDATE` | `acc-architecture/execution-phases/phase-04-accmared-internal-delivery/REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS.md` |

## Findings ذات أولوية

### المتطلبات الفرعية التي تحتاج تفكيكاً


| المرحلة | SREQ | العنوان | ملاحظة المراجعة |
|---|---|---|---|
| PH-01 | `SREQ-PH01-INST-004` | Integration configuration and credential issuance | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-01 | `SREQ-PH01-INST-005` | Credential rotation without disruption | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-01 | `SREQ-PH01-ADM-001` | Account lifecycle administration | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-01 | `SREQ-PH01-LIC-004` | Renew, suspend, revoke, expire | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-01 | `SREQ-PH01-LIC-005` | Propagation to ACCore | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-01 | `SREQ-PH01-LICV-003` | Offline local verification | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-01 | `SREQ-PH01-MSG-002` | Idempotent inbox | يفصل تسجيل receipt قبل المعالجة عن تطبيق الأثر مرة واحدة؛ لا يوجد دمج موصى به. |
| PH-01 | `SREQ-PH01-MSG-003` | Retry and dead-letter semantics | يلزم فصل نتائج/عمليات lifecycle أو آثار المصادقة/الإصدار/النشر/الاستعادة التي يمكن اختبارها أو تشغيلها مستقلاً. |
| PH-02 | `SREQ-PH02-PUB-004` | Reliable submission | تجميع الإرسال والإقرار/التكرار؛ إنشاء/تحديث وتجاهل الإصدارات؛ رؤية الفشل وإعادة الإرسال؛ أو فحوص checkout المتعددة مع سياسات غير محسومة. |
| PH-02 | `SREQ-PH02-ING-004` | Idempotent listing creation | تجميع الإرسال والإقرار/التكرار؛ إنشاء/تحديث وتجاهل الإصدارات؛ رؤية الفشل وإعادة الإرسال؛ أو فحوص checkout المتعددة مع سياسات غير محسومة. |
| PH-02 | `SREQ-PH02-REC-004` | Failed publication visibility | تجميع الإرسال والإقرار/التكرار؛ إنشاء/تحديث وتجاهل الإصدارات؛ رؤية الفشل وإعادة الإرسال؛ أو فحوص checkout المتعددة مع سياسات غير محسومة. |
| PH-02 | `SREQ-PH02-CHK-003` | Checkout validation and snapshots | تجميع الإرسال والإقرار/التكرار؛ إنشاء/تحديث وتجاهل الإصدارات؛ رؤية الفشل وإعادة الإرسال؛ أو فحوص checkout المتعددة مع سياسات غير محسومة. |
| PH-03 | `SREQ-PH03-ORD-001` | Split by seller | يجمع كتابة split/outbox وإعادة التشغيل، أو fan-out/التسليم والصلاحيات، أو بيانات allocation متعددة القرارات؛ فصلها قبل baseline. |
| PH-03 | `SREQ-PH03-CNF-005` | Recipient-scoped handoff | يجمع كتابة split/outbox وإعادة التشغيل، أو fan-out/التسليم والصلاحيات، أو بيانات allocation متعددة القرارات؛ فصلها قبل baseline. |
| PH-03 | `SREQ-PH03-PAY-002` | Per-SellerOrder allocation | يجمع كتابة split/outbox وإعادة التشغيل، أو fan-out/التسليم والصلاحيات، أو بيانات allocation متعددة القرارات؛ فصلها قبل baseline. |

### مرشح الدمج المتبقي

لم يُنفذ دمج؛ لا يوجد دمج آمن مثبت في هذه الدورة. بقي `SREQ-PH04-DOP-004` مرشحاً دون تغيير: تتداخل بعض أسماء المؤشرات مع قائمة الرؤية الاستثنائية في DEX-001، لكن مصدر الحاوية يعرّفها كمقاييس تشغيلية ويعرّف DEX-001 كاسترجاع استثناءات؛ لا يثبت ذلك تطابق النتيجة أو البيانات، كما أن تعريفات المقاييس ونطاقها غير مكتملين. ولا يندمج ذلك مع DOP-003، الذي يغطي سجلات التدقيق لا مقاييس التشغيل.

| المرحلة | SREQ | التصنيف الحالي | ملاحظة |
|---|---|---|---|
| PH-04 | `SREQ-PH04-DOP-004` | `MERGE_CANDIDATE` | بقي دون دمج؛ لا دليل يثبت التكافؤ مع DEX-001 أو DOP-003، وتعريفات المؤشرات وعتباتها/نطاقها لا تزال مفتوحة. |

### نتيجة إعادة تقييم findings الدورة الثانية

| SREQ | التصنيف السابق | نتيجة Cycle 2 | الإجراء/الحالة |
|---|---|---|---|
| `SREQ-PH01-AUD-001` | `SPLIT_REQUIRED` | `SPLIT_REQUIRED` — أُنجز التفكيك | السجل الأصلي ومعياره محفوظان بحالة `RETIRED`؛ أضيفت سبعة صفوف ذرية DRAFT بمعايير فريدة. |
| `SREQ-PH01-MSG-002` | `MERGE_CANDIDATE` | `SPLIT_REQUIRED` | لا دمج؛ بقي تفكيك فصل تسجيل الاستلام عن تطبيق الأثر مفتوحاً. |
| `SREQ-PH01-IDEM-001` | `MERGE_CANDIDATE` | `ATOMIC` | لم يعد مرشح دمج؛ لا تغيير على صف المتطلب. |
| `SREQ-PH01-IDEM-002` | `MERGE_CANDIDATE` | `NEEDS_USE_CASE` | لا دمج؛ فجوة Use Case قائمة. |
| `SREQ-PH04-DEN-003` | `DUPLICATE` | `BLOCKED_BY_OWNER_DECISION` | التشابه غير كافٍ لإثبات التكرار؛ `ODEC-010` يبقى مفتوحاً، بلا حذف أو دمج. |
| `SREQ-PH04-DOP-003` | `MERGE_CANDIDATE` | `ATOMIC` | لا دمج؛ سلوك تدقيق العمليات يبقى مستقلاً في هذه المراجعة. |
| `SREQ-PH04-DOP-004` | `MERGE_CANDIDATE` | `MERGE_CANDIDATE` | بقي مرشحاً، دون دمج. |

من أصل 17 finding تفكيك في الدورة الأولى، أُغلق واحد فقط (AUD-001) وأعيد تصنيف MSG-002 من المرشحين؛ بقي 17 finding تفكيك حياً. لا تحسم هذه النتائج قراراً أو اعتماداً من المالك.

## نتيجة إعادة التقييم في Cycle 3

| SREQ | التصنيف السابق | قرار Cycle 3 | الإجراء/الحالة |
|---|---|---|---|
| `SREQ-PH01-AUTH-001` | `SPLIT_REQUIRED` | `SPLIT_REQUIRED` — أُنجز التفكيك | الصف والمعياران الأصليان محفوظان بحالة `RETIRED`؛ أضيف AUTH-007 وAUTH-008 كصفين ذريين DRAFT بمعيارين فريدين. معيار التدقيق التاريخي لا يتكرر على الصفوف الجديدة؛ تغطيه AUD-007. |
| `SREQ-PH01-LIC-001` | `SPLIT_REQUIRED` | `SPLIT_REQUIRED` — أُنجز التفكيك | الصف ومعياراه الأصليان محفوظان بحالة `RETIRED`؛ أضيف LIC-007 وLIC-008 كصفين ذريين DRAFT بمعيارين فريدين. بوابات UNKN-003 وODEC-011 وADR-017-GATE باقية. |
| `SREQ-PH04-DOP-004` | `MERGE_CANDIDATE` | `MERGE_CANDIDATE` | لا دمج: دليل المؤشرات التشغيلية منفصل عن التدقيق، والتقاطع الجزئي مع DEX-001 لا يثبت تطابق متطلب أو بديل صالح للدمج. تبقى تعريفات المؤشرات وعتباتها ونطاقها بحاجة إلى مراجعة. |
| `SREQ-PH04-DEN-003` | `BLOCKED_BY_OWNER_DECISION` | `BLOCKED_BY_OWNER_DECISION` | لا حذف أو دمج؛ التعايش/اختيار نطاق التسليم مرتبط بقرار `ODEC-010`، والتشابه لا يثبت التكرار. |

أعيد تقييم الـ17 finding التفكيكية الحية السابقة؛ اكتمل اثنان بحفظ المصدر وإضافة الصفوف أعلاه، وبقي 15 finding حياً دون إعادة تصنيف. لا يوجد دمج أو تكرار مؤكد، ولا تحسم هذه الدورة قرارات أصحاب المصلحة.

## حدود المرحلة وملاحظات التدقيق

- **PH-04:** لا يوجد أي SREQ ضمن 27 مصنفاً `SPLIT_REQUIRED` في المراجعة التفصيلية؛ لكن ملفات المرحلة الثمانية تحمل ملاحظات منفصلة على اتساع المتطلبات الرئيسية. لا ينبغي خلط عدّ المستوى الرئيسي بعدّ SREQ.
- **PH-05:** لا صفوف في السجل، ولا أضيف هنا أي متطلب لها.
- لا يثبت وجود معايير قبول ومراجع تحقق أن المعايير قابلة للتفنيد أو أن الاختبارات نُفذت. جميع مراجع تحقق SREQ الحالية موسومة `planned`.
- ظلت بدائل المعمارية وقرارات المالك وحالات UNKNOWN والسياسات المالية/الأمنية غير المحسومة كما هي؛ التقرير يسجل فجواتها ولا يحسمها.

## طريقة إعادة التحقق

إحصاءات الصفوف قابلة لإعادة الحساب من `execution-phases/requirements-registry.csv`. معرفات وتصنيفات الذرية مستندة إلى مراجعات SREQ التفصيلية المرحلية؛ ولم يُستخدم أي ملخص PH-04 سابق خلط تصنيف المتطلبات الرئيسية بالفرعية.
