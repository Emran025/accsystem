# مراجعة ذرّية ودلالية لمتطلبات PH-01 إلى PH-04

**الدورة:** ARH-2026-11-21-C12<br>
**الأساس:** `3fc3f0de5ca646ee0d6b86d72404936d8849f795` (`origin/main` عند بدء الدورة الثانية عشرة)<br>**الدورة السابقة:** ARH-2026-11-21-C11؛ تفاصيلها محفوظة أدناه وفي تاريخ Git.<br>
**حدود العدّ:** التصنيف أدناه يخص صفوف `SREQ` فقط؛ المتطلبات الرئيسية ليست داخلة في مجاميع الذرية الفرعية.<br>
**تنبيه:** هذا سجل مراجعة للمسودات، وليس اعتماداً أو دليلاً على التنفيذ أو نجاح الاختبارات.

## النتيجة الإجمالية

يعرض السجل تصنيف **233 من 233** صف SREQ. أعادت Cycle 12 تقييم findings التفكيك السبعة الحية بصورة مستقلة ثم وُحّدت النتائج دون إخفاق؛ بقيت جميعها `SPLIT_REQUIRED`، و`PAY-002` ما زال `OWNER_BLOCKED` أيضاً. لم تدعم الأدلة المتاحة أي تعديل على المتطلبات أو AC أو صفوف registry أو إنشاء child IDs أو إعادة تصنيف. الأعداد الحالية: `ATOMIC` 58 و`SPLIT_REQUIRED` 17 (عشرة مصادر تاريخية متقاعدة وسبعة findings حية) و`MERGE_CANDIDATE` واحد. لا دمج مثبت؛ DOP-004 مرشح غير محسوم وDEN-003 غير مؤكد التكرار ومحجوب بـODEC-010. لا قرار مالك أو اعتماد جديد؛ التحقق الوظيفي غير منفذ.

## إعادة التقييم في Cycle 12

اكتملت سبع مراجعات مستقلة، واحدة لكل finding، وتوليفها دون إخفاق. لم يظهر عقد معتمد أو قرار مالك أو نتيجة اختبار قبول SREQ منفذة جديدة؛ لذلك لا يوجد أساس لتغيير صياغة requirement أو AC أو registry أو التصنيف أو إنشاء child IDs. يوجز الجدول استمرار حدود السلوك والبوابات المفتوحة:

| SREQ | نتيجة Cycle 12 | الدليل والبوابة التي بقيت مفتوحة |
|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` | استرجاع إعدادات الموصل يظل متميزاً عن إصدار/حماية مرجع الاعتماد؛ الحماية موصوفة كافتراض، وطريقة المصادقة والعقد لا تزالان غير معتمدتين. تبقى `ADR-015-GATE`, `RP-16`, `RGAP-PH01-001/005/006` ومراجعة الأمن/العقد مفتوحة. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` | receipt/claim ومنع الأثر المكرر يختلفان عن استرداد المعالجة الجارية/الجزئية. تظل دلالات ACK ونطاق المفتاح والاحتفاظ وreconciliation غير معتمدة تحت `ADR-022-GATE`؛ اختبارات duplicate/crash/recovery مخططة فقط. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` | ثبات مفتاح idempotency لا يحسم دورة Outbox والقبول/الرفض/النتيجة النهائية وإعادة المحاولة. تبقى قرارات `PUB-005/006` وعقد `IF-ACR-PUBLISH-EVENT` ومتى يصدر `listing_id` غير محسومة. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` | الرفض قبل القبول يختلف عن فشل التسليم/المزامنة بعد القبول؛ `AC-PH02-REC-004-01` يثبت FAILED/resubmission فقط، لا تسجيل الرفض وقنوات ظهوره لـoperations وACCore. تبقى `PUB-005/006` والعقد والاختبارات مفتوحة. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` | التحقق من الأهلية والسعر/الكمية يظل متميزاً عن إنشاء session ناجحة ولقطات السعر/التوفر/التسليم/السياسة. تبقى `UNKN-006`, `ODEC-003/009`, `RGAP-PH02-003/009` وحدود الجلسة مفتوحة؛ TTL غير معروف. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` | إسقاط البيانات للمستلم/الدور يختلف عن at-least-once dispatch وACK/retry/recovery. لا schema أو cardinality أو disclosure أو ACK semantics معتمدة؛ تبقى `ADR-019-GATE`, `RP-04` و`IF-ACC-ORDER-CONFIRM` مفتوحة، ويظل accounting trigger ضمن `CNF-006` منفصلاً. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED`; `OWNER_BLOCKED` | اكتمال allocation لكل SellerOrder لا يقرر cardinality لمحاولات provider المجمعة أو المنفصلة. تبقى `ADR-016-GATE`, `ASSUM-003`, `RGAP-PH03-003` وسياسات Finance/Legal/provider بلا اعتماد؛ لا اختيار provider أو دمج مع `PAY-003`. |

لا تعني مراجعة الوثائق أو اجتياز validators تنفيذ السلوك أو نجاح اختبار قبول. تبقى قيود الحفظ كما هي: `ORD-001` متميز عن `ORD-002` وعن `ORD-007/008`؛ ولا يُستنتج OAuth/mTLS أو TTL أو settlement/commission/refund أو provider behavior. تفاصيل مراجعة Cycle 11 محفوظة أدناه.

## إعادة التقييم في Cycle 11

فحص سبعة مراجعين مستقلين صفوف registry ووثائقها ومعاييرها وأدلة المعمارية/القرارات، ثم جُمعت النتائج دون إخفاق. بقيت التصنيفات السبعة `SPLIT_REQUIRED`؛ لا يوجد دليل يبرر تغيير المصدر أو AC أو registry أو إنشاء child IDs. الحدود التالية تشرح سبب بقاء كل finding مفتوحاً ولا تفوض اختيار التفكيك أو السياسة:

| SREQ | النتيجة | حدود السلوك والأدلة والبوابة المفتوحة |
|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` | استرجاع تكوين الموصل للمؤسسة متميز عن إنشاء/حماية مرجع الاعتماد وآثاره الأمنية. `AC-PH01-INST-004-01/02` لا تعتمد طريقة مصادقة أو عقد إصدار/تدوير/إلغاء. تبقى `ADR-015-GATE`, `RP-16`, `RGAP-PH01-001/005/006` ومراجعات الأمن/العقد مفتوحة؛ لا نفترض OAuth/mTLS أو child IDs. المصدر: `REQ-PH01-INSTITUTION-LIFECYCLE` §§3–6 و`ADR-015`. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` | receipt/claim ومنع أثر مكرر ونتيجة duplicate المكتمل تختلف عن الاسترداد لقيد المعالجة/الآثار الجزئية. معنى ACK ونطاق المفتاح وحالة receiver والاحتفاظ/reconciliation غير معتمدة. تبقى `ADR-022-GATE` واختبارات duplicate/crash/recovery مخططة لا منفذة. المصدر: `REQ-PH01-MESSAGE-RELIABILITY` §§3–6 و`ADR-022` و`IF-ACC-ORDER-CONFIRM` §2A. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` | ثبات مفتاح idempotency متميز عن دورة Outbox/receipt/acceptance/rejection/retry. `PUB-005` لا يحسم durable acceptance مقابل النتيجة النهائية، `listing_id`، duplicate/in-progress/uncertain، أو تصحيح الرفض؛ ACs والاختبارات مخططة فقط. المصدر: `REQ-PH02-PRODUCT-PUBLICATION` §§3–6 و`FN-INT-PUBLISH` و`IF-ACR-PUBLISH-EVENT`. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` | الرفض قبل القبول وفشل التسليم بعد القبول/الاسترداد نتائج وحالات مختلفة. `AC-PH02-REC-004-01` يغطي FAILED/resubmission فقط ولا يثبت تسجيل/رؤية الرفض من العمليات وACCore. تبقى `PUB-005/006` وعقد الاستجابة وقنوات الرؤية والاختبارات مفتوحة. المصدر: `REQ-PH02-PUBLICATION-RECOVERY` §§3–5 و`FN-INT-PUBLISH` §7. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` | أهلية المشتري/التحقق من التوفر والسعر/الكمية منفصلة عن إنشاء session ناجحة ولقطات التوفر والسعر والتسليم ونسخة السياسة. `AC-01` يغطي تغير السعر/الكمية فقط و`AC-02` يؤجل نموذج اللقطة؛ تبقى `UNKN-006`, `ODEC-009`, `ODEC-003`, `RGAP-PH02-003/009` وعقد checkout/session/TTL مفتوحة. المصدر: `REQ-PH02-CHECKOUT-PREPARATION` §§3–6 و`FN-ORD-CHECKOUT`. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` | صلاحية المستلم/الدور وإسقاط البيانات المعزول منفصلان عن الإرسال at-least-once وACK/retry/receiver recovery. لم يُعتمد schema أو cardinality أو disclosure أو ACK semantics؛ يبقى accounting trigger `CNF-006` منفصلاً. المصدر: `REQ-PH03-ORDER-CONFIRMATION` §§3–6 و`IF-ACC-ORDER-CONFIRM` §2A و`ADR-019-GATE`/`RP-04`. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED`; `OWNER_BLOCKED` | اكتمال allocation لكل SellerOrder منفصل عن سياسة أهلية/cardinality محاولة provider مجمعة أو منفصلة. تبقى `ADR-016-GATE`, `ASSUM-003`, `RGAP-PH03-003` وسياسات Finance/Legal/provider مفتوحة؛ لا اختيار provider ولا دمج مع `PAY-003`. المصدر: `REQ-PH03-PAYMENT-ORCHESTRATION` §§3–6 و`FN-PAY-AUTHORIZE` و`ADR-016`. |

لا يضيف وجود function أو interface في registry دليلاً على التنفيذ؛ ولم يُنفذ أي اختبار SREQ أو يحصل اعتماد مالك جديد. تبقى عضوية `ADM-001` وبوابات lifecycle/policy للترخيص ونقص قبول `REC-004`/`CHK-003` ظاهرة. يُحفظ `ORD-001` منفصلاً عن `ORD-002` وعن تفكيك `ORD-007/008`. لم يُستنتج OAuth/mTLS أو TTL أو settlement/commission/refund أو provider behavior.

## إعادة التقييم في Cycle 9

اكتملت المراجعات السبعة المستقلة دون إخفاق، ثم وُحّدت النتائج. بقيت حدود السلوك/الاختبار والبوابات كما هي؛ لم يظهر دليل جديد يغلق عقداً أو قرار مالك أو اختبار قبول منفذاً يبرر تغييراً في المصدر أو السجل.

| SREQ | التصنيف الحالي | نتيجة Cycle 9 والبوابة المفتوحة |
|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` | لا تعديل؛ `ADR-015-GATE` و`RP-16`، وحدود العقد/الأمن وربط الوظيفة/Use Case غير محسومة. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` | لا تعديل؛ `ADR-022-GATE` وعقد receiver وACK/key/recovery/retention واختبار duplicate delivery مفتوحة. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` | لا تعديل؛ `PUB-005` و`IF-ACR-PUBLISH-EVENT` لم تحسما receipt/listing ID وduplicate/rejection/retry semantics. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` | لا تعديل؛ `PUB-005/006` وحالة الرفض/الفشل وقنوات الرؤية والقبول غير مكتملة. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` | لا تعديل؛ عقد جلسة checkout وTTL/state وsnapshot/policy boundary وACs ما زالت مفتوحة. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` | لا تعديل؛ recipient/role projection وعقد ACK/retry/recovery وpartial-effect evidence مفتوحة؛ يبقى accounting trigger منفصلاً ضمن CNF-006. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED` | لا تعديل؛ `OWNER_BLOCKED` حتى قرارات provider/cardinality والسياسة المالية والعقد؛ يبقى منفصلاً عن PAY-003 دون child IDs. |

تبقى قيود الحفظ السابقة: لا يُخلط `ORD-001` مع `ORD-002` أو `ORD-007/008`؛ ولا تغيير في عضوية `ADM-001` أو lifecycle/policy الترخيص. ولا استنتاج لـOAuth/mTLS أو TTL أو settlement/commission/refund أو provider behavior. لا اختبار SREQ منفذ أو `ACCEPTED` جديد.

## إعادة التقييم في Cycle 10

اكتملت المراجعات السبعة المستقلة، واحد لكل finding، ثم وُحّدت نتائجها دون إخفاق. لم يظهر عقد معتمد أو قرار مالك أو اختبار قبول منفذ جديد يبرر تغييراً في المصدر أو AC أو السجل أو التصنيف؛ لا child IDs جديدة ولا دمج.

| SREQ | نتيجة Cycle 10 | البوابة أو الدليل غير المغلق |
|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` بلا تغيير | `ADR-015-GATE` و`RP-16` وأدلة RGAP/العقد/الأمن لا تحسم حدود تهيئة الموصل وإصدار/حماية بيانات الاعتماد؛ لا نفترض OAuth أو mTLS. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` بلا تغيير | `ADR-022-GATE`: عقد receiver وACK/key/recovery/retention ونتائج منع الأثر المكرر لم تُعتمد أو تُختبر. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` بلا تغيير | عقد `PUB-005` وإيصال النشر ووقت/معنى `listing_id` ودلالات التكرار والرفض وإعادة المحاولة ما زالت غير محسومة. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` بلا تغيير | `PUB-005/006`: قبول الرفض قبل الإرسال مقابل فشل التسليم/الاسترداد وقنوات إظهار الرفض غير مكتمل. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` بلا تغيير | `UNKN-006` و`ODEC-009` و`ODEC-003`/`ADR-016` و`RGAP-PH02-003/009` مفتوحة؛ TTL للجلسة يظل غير معروف، وحدود snapshot/policy والقبول غير مثبتة. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` بلا تغيير | `ADR-019-GATE`/`RP-04` وعقد `IF-ACC-ORDER-CONFIRM` §2A لا يحسمون recipient/role projection وACK/retry/recovery؛ accounting trigger يبقى منفصلاً ضمن `CNF-006`. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED` و`OWNER_BLOCKED` | `ADR-016-GATE` و`ASSUM-003` و`RGAP-PH03-003` مفتوحة؛ اكتمال allocation لا يحسم سياسة provider أو cardinality لمحاولاته. |

تبقى عضوية المؤسسات في `ADM-001` وبوابات lifecycle/policy للترخيص ظاهرة ومفتوحة. يُحفظ `ORD-001` كـ`RETIRED` ومتميزاً عن `ORD-002` وعن تقسيم `ORD-007/008`. يظل `DOP-004` مرشح دمج غير مثبت و`DEN-003` غير مؤكد التكرار ومحجوباً بـ`ODEC-010`. لا استنتاج لـOAuth/mTLS أو TTL أو settlement/commission/refund أو provider behavior؛ مراجع التحقق المخططة لا تثبت التنفيذ.

| المرحلة | SREQ | ATOMIC | SPLIT_REQUIRED | MERGE_CANDIDATE | ARCHITECTURAL_CONSTRAINT | POLICY_RULE | ACCEPTANCE_CRITERION_ONLY | NEEDS_USE_CASE | DUPLICATE | OUT_OF_PHASE | BLOCKED_BY_OWNER_DECISION |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PH-01 — تأسيس المنصة | 98 | 25 | 10 | 0 | 13 | 14 | 3 | 22 | 0 | 0 | 11 |
| PH-02 — الكتالوج والاكتشاف والحجز | 47 | 16 | 4 | 0 | 8 | 10 | 0 | 1 | 0 | 0 | 8 |
| PH-03 — المخزون والطلبات والدفع وأحداث التسليم الخارجية | 61 | 10 | 3 | 0 | 8 | 6 | 0 | 18 | 0 | 0 | 16 |
| PH-04 — التسليم الداخلي عبر ACCMared | 27 | 7 | 0 | 1 | 3 | 3 | 0 | 1 | 0 | 0 | 12 |
| **الإجمالي** | **233** | **58** | **17** | **1** | **32** | **33** | **3** | **42** | **0** | **0** | **47** |

## سجل التصنيف الكامل

كل صف أدناه يعرض التصنيف الحالي لـSREQ واحد بعد مراجعة Cycle 10؛ لم يتغير أي تصنيف عن Cycle 9. تحتفظ المصادر المفككة بحالتها التاريخية `RETIRED` وتصنيف `SPLIT_REQUIRED`؛ يبلغ عددها عشرة، مع سبعة findings حية حالياً.

| المرحلة | SREQ | المتطلب الرئيسي | العنوان | التصنيف | وثيقة المصدر |
|---|---|---|---|---|---|
| PH-01 | `SREQ-PH01-INST-001` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Unique stable institution ID | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-002` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Activation status | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-003` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Institution lookup for platform services | `NEEDS_USE_CASE` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-004` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Integration configuration and credential issuance | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-005` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Credential rotation without disruption | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-006` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Institution deactivation | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-009` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Credential rotation transition | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-INST-010` | `REQ-PH01-INSTITUTION-LIFECYCLE` | Revoked credential rejection | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-INSTITUTION-LIFECYCLE.md` |
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
| PH-01 | `SREQ-PH01-ADM-007` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | Platform account state enforcement | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
| PH-01 | `SREQ-PH01-ADM-008` | `REQ-PH01-ADMIN-ACCESS-CONTROL` | Platform account lifecycle event publication | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-ADMIN-ACCESS-CONTROL.md` |
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
| PH-01 | `SREQ-PH01-LIC-009` | `REQ-PH01-LICENSE-LIFECYCLE` | Audit record for license state changes | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-010` | `REQ-PH01-LICENSE-LIFECYCLE` | Revocation is terminal | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-011` | `REQ-PH01-LICENSE-LIFECYCLE` | License event delivery to ACCore | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LIC-012` | `REQ-PH01-LICENSE-LIFECYCLE` | Suspension restricts licensed modules | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md` |
| PH-01 | `SREQ-PH01-LICV-001` | `REQ-PH01-LICENSE-VALIDATION` | Online institutional validation | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-002` | `REQ-PH01-LICENSE-VALIDATION` | Authenticated, scoped, no ERP data | `ARCHITECTURAL_CONSTRAINT` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
| PH-01 | `SREQ-PH01-LICV-003` | `REQ-PH01-LICENSE-VALIDATION` | Offline local verification | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-VALIDATION.md` |
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
| PH-01 | `SREQ-PH01-MSG-007` | `REQ-PH01-MESSAGE-RELIABILITY` | Retry preserves idempotency key | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
| PH-01 | `SREQ-PH01-MSG-008` | `REQ-PH01-MESSAGE-RELIABILITY` | Dead-letter classification and safe replay | `ATOMIC` | `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-MESSAGE-RELIABILITY.md` |
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
| PH-02 | `SREQ-PH02-ING-007` | `REQ-PH02-LISTING-INGESTION` | Idempotent listing application | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
| PH-02 | `SREQ-PH02-ING-008` | `REQ-PH02-LISTING-INGESTION` | Ignore stale listing versions | `ATOMIC` | `acc-architecture/execution-phases/phase-02-catalog-discovery-reservation/REQ-PH02-LISTING-INGESTION.md` |
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
| PH-03 | `SREQ-PH03-ORD-001` | `REQ-PH03-ORDER-AGGREGATE` | Split by seller (retired source; decomposed in Cycle 7) | `SPLIT_REQUIRED` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-002` | `REQ-PH03-ORDER-AGGREGATE` | Idempotent order creation | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-003` | `REQ-PH03-ORDER-AGGREGATE` | State machine enforcement | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-004` | `REQ-PH03-ORDER-AGGREGATE` | Parent state is aggregate | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-005` | `REQ-PH03-ORDER-AGGREGATE` | Append-only history atomic with outbox | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-006` | `REQ-PH03-ORDER-AGGREGATE` | Policy and currency snapshot references | `BLOCKED_BY_OWNER_DECISION` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-007` | `REQ-PH03-ORDER-AGGREGATE` | Atomic aggregate and outbox creation | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
| PH-03 | `SREQ-PH03-ORD-008` | `REQ-PH03-ORDER-AGGREGATE` | Duplicate-safe split replay | `ATOMIC` | `acc-architecture/execution-phases/phase-03-inventory-order-payment-delivery-events/REQ-PH03-ORDER-AGGREGATE.md` |
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

### Findings التفكيك المفتوحة والمصدر المفكك في Cycle 7

أكدت إعادة تقييم Cycle 7 بقاء **سبعة** findings حية `SPLIT_REQUIRED`. جرى تفكيك `ORD-001` المدعوم بالأدلة وحُفظ كسجل تاريخي؛ لا تُغلق بقية findings بإعادة تسمية شكلية، ويلزم حسم فجوات الأدلة/القبول أو قرارات العقد قبل أي تفكيك إضافي. أعيد تصنيف `SREQ-PH01-LICV-003` إلى `ATOMIC` في Cycle 5، لكن فجوة معيار القبول والسياسات المرتبطة به لا تزال مانعاً مستقلاً للجاهزية.

| المرحلة | SREQ | العنوان | الحالة الحالية والسبب المتبقي |
|---|---|---|---|
| PH-01 | `SREQ-PH01-INST-004` | Integration configuration and credential issuance | `OWNER_BLOCKED`: criterion حماية الأسرار موصوف في المصدر كافتراض غير معتمد، وقرار المصادقة/الأمن وواجهة السجل ما زالا مفتوحين (`ADR-015-GATE`, `RP-16`, `RGAP-PH01-001`). لم يُنشأ child غير مدعوم. |
| PH-01 | `SREQ-PH01-MSG-002` | Idempotent inbox | `OWNER_BLOCKED`: معيار القبول لا يثبت جميع جوانب استقبال الرسالة والأثر مرة واحدة وإرجاع outcome المسجل؛ تبقى `ADR-022-GATE` مفتوحة. |
| PH-02 | `SREQ-PH02-PUB-004` | Reliable submission | `OWNER_BLOCKED`: key/receipt وmeaning لحالات القبول/الرفض لا تزال متشابكة مع contract response غير المكتمل؛ تبقى `PUB-005` مفتوحة. |
| PH-02 | `SREQ-PH02-REC-004` | Failed publication visibility | `OWNER_BLOCKED`: المعيار الحالي لا يثبت رؤية الرفض والفشل لكل من العمليات وACCore؛ `PUB-005` مفتوح. |
| PH-02 | `SREQ-PH02-CHK-003` | Checkout validation and snapshots | `OWNER_BLOCKED`: الأهلية/التوفر/اللقطات وإصدارات السياسات لا تملك معايير كاملة؛ تبقى `ODEC-003`, `UNKN-006`, `ODEC-009` مفتوحة، ولم تُختر ضريبة أو عملة أو delivery model. |
| PH-03 | `SREQ-PH03-CNF-005` | Recipient-scoped handoff | `OWNER_BLOCKED`: routing, recipient/role-authorized projection, and at-least-once delivery lack complete acceptance coverage; `ADR-019-GATE`/`RP-04` remain open. |
| PH-03 | `SREQ-PH03-ORD-001` | Split by seller | `RETIRED` source; original statement and `AC-PH03-ORD-001-01` preserved. Cycle 7 evidence supports separate draft children `ORD-007` (local aggregate/outbox transaction) and `ORD-008` (duplicate-safe repeated/concurrent replay). `ODEC-003` and contract approval remain open; keep it distinct from `ORD-002`. |
| PH-03 | `SREQ-PH03-PAY-002` | Per-SellerOrder allocation | `OWNER_BLOCKED`: allocation data and conditional provider aggregation remain distinct; provider support and financial policy are unresolved (`ADR-016-GATE`, `ASSUM-003`). |

### تفكيك مدعوم بالأدلة في Cycle 7

| المتطلب الجديد | AC | الحد المستقل والأدلة | القيد المتبقي |
|---|---|---|---|
| `SREQ-PH03-ORD-007` — Atomic aggregate and outbox creation | `AC-PH03-ORD-007-01` | ParentOrder واحد وSellerOrder لكل بائع وأحداث SellerOrderCreated تحفظ جميعاً في معاملة محلية واحدة أو لا يُحفظ أي منها؛ `CMP-ORD-MULTISELLER` §§19–20, 25–26 و`FN-ORD-CHECKOUT` §§11–12, 28, 34. | `ODEC-003`, `IC-002`, `ADR-021-GATE` و`RGAP-PH02-004` مفتوحة؛ schema reference غير معتمد والاختبار مخطط. |
| `SREQ-PH03-ORD-008` — Duplicate-safe split replay | `AC-PH03-ORD-008-01` | إعادة الطلب أو محاولته بالتوازي تعيد ParentOrder وSellerOrders القائمة دون سجلات طلب أو outbox مكررة؛ `CMP-ORD-MULTISELLER` §§25–26, 30–36 و`FN-ORD-CHECKOUT` §48 و`ADR-013` §§3–4. | عقد الاستجابة/schema غير معتمد والاختبار مخطط؛ تبقى `ODEC-003`, `IC-002`, `ADR-021-GATE` و`RGAP-PH02-004` مفتوحة. |

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

## نتيجة إعادة التقييم في Cycle 4

| SREQ | توصية المراجعة | قرار Cycle 4 | الإجراء/الحالة والدليل المتبقي |
|---|---|---|---|
| `SREQ-PH01-INST-004` | SPLIT_REQUIRED | بقي مفتوحاً | criterion حماية الأسرار مصدره افتراض غير ratified؛ لا child ولا سياسة مصادقة/تخزين جديدة. |
| `SREQ-PH01-INST-005` | SPLIT_REQUIRED | فُكك إلى INST-009 وINST-010 | حُفظ المصدر ومعياره؛ الاستمرارية ومدة الانتقال وآلية الإلغاء ليست مثبتة؛ `ADR-015-GATE`/`RP-16` باقيتان. |
| `SREQ-PH01-ADM-001` | SPLIT_REQUIRED | فُكك إلى ADM-007 وADM-008 | حُفظ المصدر ومعياراه؛ سلوك institution membership باقٍ فجوة blocking في `RGAP-PH01-003` بلا function/use-case ID. |
| `SREQ-PH01-LIC-004` | SPLIT_REQUIRED | فُكك إلى LIC-009 وLIC-010 | حُفظ المصدر ومعياراه؛ أفعال renewal/suspension/revocation/expiry لم تتحول إلى state graph أو سياسة؛ `UNKN-003`/`LIC-001` مفتوحتان. |
| `SREQ-PH01-LIC-005` | SPLIT_REQUIRED | فُكك إلى LIC-011 وLIC-012 | حُفظ المصدر ومعياراه؛ evidence يثبت Outbox/Inbox وrestriction على LicenseSuspended فقط، لا باقي event mapping أو restoration/window. |
| `SREQ-PH01-LICV-003` | SPLIT_REQUIRED | بقي مفتوحاً | معيار workflow/grant bounds غير مكتمل؛ لا reclassification ولا توسيع AC قبل evidence/review. |
| `SREQ-PH01-MSG-002` | SPLIT_REQUIRED | بقي مفتوحاً | AC غير كافٍ لكل outcomes؛ لا atomic reclassification ولا اعتماد. |
| `SREQ-PH01-MSG-003` | SPLIT_REQUIRED | فُكك إلى MSG-007 وMSG-008 | حُفظ المصدر ومعياره؛ child retry criterion مخطط ومشتق من المصدر، ولم يُنفذ؛ `IC-004`/`ADR-022-GATE` باقيتان. |
| `SREQ-PH02-CHK-003` | SPLIT_REQUIRED | بقي مفتوحاً | Acceptance evidence incompleta; policies and owner decisions remain open; no values selected. |
| `SREQ-PH02-ING-004` | SPLIT_REQUIRED | فُكك إلى ING-007 وING-008 | حُفظ المصدر ومعياره؛ `PUB-005` receipt/duplicate response و`PUB-001` ordering باقيتان. |
| `SREQ-PH02-PUB-004` | SPLIT_REQUIRED | بقي مفتوحاً | Atomic reclassification proposal rejected; response contract semantics remain under `PUB-005`. |
| `SREQ-PH02-REC-004` | SPLIT_REQUIRED | بقي مفتوحاً | Acceptance evidence proves FAILED visibility only; rejection visibility/channels unresolved under `PUB-005`. |
| `SREQ-PH03-CNF-005` | SPLIT_REQUIRED | بقي مفتوحاً | Atomic reclassification unsupported by current AC; `ADR-019-GATE`/`RP-04` remain. |
| `SREQ-PH03-ORD-001` | SPLIT_REQUIRED | بقي مفتوحاً | No merge or reassignment to `ORD-002`; key/scope equivalence unproven, `ODEC-003` remains. |
| `SREQ-PH03-PAY-002` | SPLIT_REQUIRED | بقي مفتوحاً | Atomic reclassification proposal unsupported; provider aggregation and financial owner policies unresolved. |

**النتيجة:** من 15 finding، أُنجزت ستة decompositions مدعومة، وبقيت تسعة `SPLIT_REQUIRED` مفتوحة؛ لم يُعد تصنيف أي finding إلى `ATOMIC` ولم يُنفذ merge. لا حزمة مراجعة تحتوي حكماً نهائياً منفصلاً عن تصنيف Cycle 3، وهذه القرارات تركيب أدلة وليست owner approval.

## نتيجة إعادة التقييم في Cycle 5

أُعيد تقييم findings التسعة الحية المتبقية بأدلة مستقلة. لم تتغير متطلبات المصدر أو صفوف CSV، ولم تُنشأ children أو معرفات جديدة، ولم يُتخذ قرار مالك أو دمج.

| SREQ | التصنيف بعد المراجعة | نتيجة Cycle 5 والإجراء المدعوم |
|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` | تكوين موصل المؤسسة وإصدار/تخزين مرجع الاعتماد لهما outcome onboarding واحد، لكن معايير التخزين/الإتاحة منفصلة ولا يكفي دليل الحماية لأنه افتراض غير ratified. تبقى `ADR-015-GATE`, `RP-16`, `RGAP-PH01-001/005/006` مفتوحة؛ لا اختيار OAuth/mTLS ولا schema/function ID. |
| `SREQ-PH01-LICV-003` | `ATOMIC` | predicates التوقيع والهوية والمنح والتحقق بلا شبكة تحدد نتيجة تحقق offline واحدة؛ لا حالات أو عقود مستقلة لكل predicate. لا split. مع ذلك `AC-PH01-LICV-003-01` لا يثبت workflow/grant bounds أو عدم إجراء network call، وتظل `UNKN-009`, `ODEC-014`, `LIC-001` حول strategy/TTL/grace مفتوحة؛ reclassification ليست اكتمالاً للقبول أو اعتماداً. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` | receipt/claim، منع تكرار الأثر، واستجابة duplicate المكتمل/قيد المعالجة لها حالات واختبارات مستقلة؛ لا split IDs حتى اعتماد state/ACK/key/recovery/retention contract تحت `ADR-022-GATE` و`RGAP-PH01-005`. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` | ثبات idempotency key منفصل عن lifecycle/تصنيف النتيجة، لكن معنى receipt والـin-progress duplicate والرفض النهائي غير محسوم تحت `PUB-005`؛ أبقِ العبارة وACs دون تغيير حتى اعتماد contract. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` | الرفض قبل القبول وفشل التوصيل/recovery نتيجتان ومسارا اختبار مستقلان؛ تبقى visibility/representation وreceipt مقابل final result وretry/reconciliation والسياسات تحت `PUB-005/006` غير محسومة. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` | رفض checkout بعد validation ونجاح snapshots/policy versions لهما outcomes واختبارات مختلفة؛ tax/currency/delivery model وsnapshot/API/order boundary وsession TTL غير مقرة (`UNKN-006`, `ODEC-009`, `ODEC-003`, `RGAP-PH02-*`). لا children/fields جديدة. |
| `SREQ-PH03-ORD-001` | `SPLIT_REQUIRED` | دليل component والـAC يميز الإنشاء المحلي atomic لـParentOrder/SellerOrders/outbox عن duplicate-safe replay؛ يمكن اقتراح split مستقبلي مع حفظ AC/history. لا merge أو reassignment إلى `ORD-002`، ولا children IDs؛ يبقى `ODEC-003` وAPI contract gate مفتوحين. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` | recipient/role-scoped disclosure نتيجة أمن/بيانات مستقلة عن at-least-once dispatch/retry/idempotent receiver effect؛ لا child IDs قبل حسم projection/cardinality/roles/ACK/key semantics تحت `ADR-019-GATE` و`RP-04`. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED` | اكتمال allocation لكل SellerOrder منفصل عن aggregate-vs-separate provider attempt eligibility، والأخيرة تتداخل مع `PAY-003`. لا split نهائي قبل provider capability وFinance/Legal/institution policy gates؛ تبقى `ADR-016-GATE`, `ASSUM-003`, `RGAP-PH03-003` مفتوحة. |

**الأعداد بعد Cycle 5:** أُعيد تقييم 9 findings (قبل: ATOMIC 55، SPLIT_REQUIRED 18 = 9 تاريخية + 9 حية؛ بعد: ATOMIC 56، SPLIT_REQUIRED 17 = 9 تاريخية + 8 حية؛ `MERGE_CANDIDATE` 1). بقي السجل 276 صفاً (45 main و231 SREQ)، وTBD use_case_id 188، والصفوف ذات القرارات المفتوحة 207، والـC4 bindings المفقودة بنيوياً 0. لا يتغير حكم عدم الجاهزية. لا يُثبت هذا التصنيف موافقة مالك أو تنفيذ/نجاح اختبار.

لم يتغير `SREQ-PH04-DOP-004`: يظل merge candidate دون إثبات equivalence؛ ولم يتغير `SREQ-PH04-DEN-003`: ليس duplicate مؤكداً ويظل محجوباً بـ`ODEC-010`.

## نتيجة إعادة التقييم في Cycle 6

أُعيد تقييم كل واحد من findings الثمانية الحية بواسطة مراجع مستقل ثم جرى توحيد النتائج. لم يظهر دليل تنفيذ أو قرار مالك جديد، ولم تُعدّل المتطلبات أو ACs أو صفوف CSV أو المعمارية. تبقى الحدود التالية مفاهيمية فقط، لا تفويضاً لإنشاء child IDs أو تغيير السجل:

| SREQ | التصنيف بعد Cycle 6 | نتيجة الأدلة والإجراء |
|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` | يجمع إعداد/إتاحة تكوين الموصل مع إصدار/حماية مرجع الاعتماد؛ `ADR-015-GATE`, `RP-16`, `RGAP-PH01-001/005/006` وعقد secret-management/schema غير محسومة. لا اختيار OAuth/mTLS أو تخزين ولا children. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` | receipt/claim، منع تكرار الأثر، وسلوك duplicate المكتمل/قيد المعالجة نتائج قابلة للاختبار منفصلة؛ state/ACK/key/recovery/retention و`ADR-022-GATE` ما زالت غير مكتملة. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` | ثبات المفتاح يختلف عن دورة receipt/acceptance/rejection والحالات؛ ترتيب المفتاح ومعنى القبول والتصنيف النهائي/المؤقت/غير المحسوم تحت `PUB-005` غير معتمدة. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` | الرفض قبل القبول وفشل التوصيل بعده مساران مختلفان؛ `AC-PH02-REC-004-01` يثبت وجود حالة FAILED وإتاحة resubmission فقط، لا ظهور الرفض أو الرؤية لكل من operations وACCore. لا children قبل تحديد channels/state contract تحت `PUB-005`. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` | يجمع eligibility والتوفر/السعر/الكمية والتسليم ولقطات السياسات. `AC-PH02-CHK-003-01` يغطي تغير السعر/الكمية؛ و`-02` يؤجل tax/currency/delivery. تبقى `UNKN-006`, `ODEC-009`, `ODEC-003` وعقد checkout/session مفتوحة. |
| `SREQ-PH03-ORD-001` | `SPLIT_REQUIRED` | الأدلة تميز إنشاء ParentOrder/SellerOrders/outbox في معاملة محلية عن duplicate-safe replay؛ هذا حد مستقبلي فقط. يبقى منفصلاً عن `ORD-002`؛ لا key/scope equivalence مثبتة و`ODEC-003` وعقد API مفتوحان. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` | recipient/role authorization وprojection متميزان عن at-least-once dispatch وreceiver recovery/idempotency؛ schema/roles/ACK/retry تحت `ADR-019-GATE` و`RP-04` ما زالت مقترحة أو مفتوحة. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED` | اكتمال سجل allocation لكل SellerOrder يختلف عن أهلية/عدد محاولات provider؛ الأخيرة تتداخل مع `PAY-003`. العقد `RGAP-PH03-003` و`ADR-016-GATE` و`ASSUM-003` وسياسات provider/Finance مفتوحة. |

**الأعداد بعد Cycle 6:** لم يتغير التصنيف عن Cycle 5: `ATOMIC` 56، `SPLIT_REQUIRED` 17 (9 مصادر تاريخية `RETIRED` و8 findings حية)، `MERGE_CANDIDATE` 1، `DUPLICATE` المؤكد 0. السجل 276 صفاً (45 REQ رئيسية و231 SREQ)، وTBD use_case_id 188، والصفوف ذات القرارات المفتوحة 207، والـC4 bindings المفقودة بنيوياً 0. لا صفوف `ACCEPTED` ولا اختبارات SREQ منفذة مثبتة.

ظلت عضوية المؤسسات في `ADM-001` وبوابات lifecycle/policy للترخيص مفتوحة؛ لا مراجعة هنا أغلقتها. بقي DOP-004 مرشح دمج غير مثبت، وDEN-003 غير مؤكد التكرار ومحجوباً بـ`ODEC-010`. الجاهزية لا تتحسن بمجرد إعادة التقييم، و`strict-ready` يبقى حاجزاً إلى أن تُغلق أدلته وقراراته.

## حدود المرحلة وملاحظات التدقيق

- **PH-04:** لا يوجد أي SREQ ضمن 27 مصنفاً `SPLIT_REQUIRED` في المراجعة التفصيلية؛ لكن ملفات المرحلة الثمانية تحمل ملاحظات منفصلة على اتساع المتطلبات الرئيسية. لا ينبغي خلط عدّ المستوى الرئيسي بعدّ SREQ.
- **PH-05:** لا صفوف في السجل، ولا أضيف هنا أي متطلب لها.
- لا يثبت وجود معايير قبول ومراجع تحقق أن المعايير قابلة للتفنيد أو أن الاختبارات نُفذت. جميع مراجع تحقق SREQ الحالية موسومة `planned`.
- ظلت بدائل المعمارية وقرارات المالك وحالات UNKNOWN والسياسات المالية/الأمنية غير المحسومة كما هي؛ التقرير يسجل فجواتها ولا يحسمها.

## طريقة إعادة التحقق

إحصاءات الصفوف قابلة لإعادة الحساب من `execution-phases/requirements-registry.csv`. معرفات وتصنيفات الذرية مستندة إلى مراجعات SREQ التفصيلية المرحلية؛ ولم يُستخدم أي ملخص PH-04 سابق خلط تصنيف المتطلبات الرئيسية بالفرعية.

## نتيجة إعادة التقييم في Cycle 8

أُعيد تقييم كل واحد من findings التفكيك السبعة الحية بصورة مستقلة. لا يوجد تعارض جوهري في النتيجة المجمعة: تبقى الصفوف السبعة `SPLIT_REQUIRED`؛ لا تدعم الأدلة إعادة التصنيف إلى `ATOMIC` أو الدمج أو إنشاء معرفات أبناء. وجدت المراجعات حدوداً سلوكية واختبارية مستقلة، لكنها لم تجد عقوداً أو موافقات مالك أو أدلة قبول منفذة تكفي لتثبيت متطلبات فرعية جديدة.

| SREQ | التصنيف بعد Cycle 8 | الحدود والأدلة المميزة | ما يمنع التغيير الآن |
|---|---|---|---|
| `SREQ-PH01-INST-004` | `SPLIT_REQUIRED` | إنشاء/استرجاع تكوين موصل المؤسسة منفصل عن حماية السر وعدم كشفه؛ وثيقة `REQ-PH01-INSTITUTION-LIFECYCLE` ومعيارا `AC-PH01-INST-004-01/02` و`CNT-ACC-INSTREG`/`CNT-ACC-INTEGRATION`. | حماية التخزين افتراض غير معتمد؛ `ADR-015-GATE`, `RP-16`, `RGAP-PH01-001/005/006` وعقود Registry/connector ما زالت مفتوحة. لا اختيار OAuth/mTLS أو child IDs. |
| `SREQ-PH01-MSG-002` | `SPLIT_REQUIRED` | الاستلام/claim الدائم، منع تكرار الأثر، ونتيجة duplicate المكتمل مقابل الاسترداد لقيد المعالجة؛ `REQ-PH01-MESSAGE-RELIABILITY` و`interface-contracts.md` §8. | حالة receiver وACK ومعنى المفتاح المحدد والاسترداد/الاحتفاظ/النتيجة المسجلة تحت `ADR-022-GATE` غير مكتملة؛ الاختبارات مخططة فقط. |
| `SREQ-PH02-PUB-004` | `SPLIT_REQUIRED` | ثبات مفتاح التسليم/التكرار الآمن منفصل عن انتقال Outbox حسب القبول/الرفض وتصنيف retry؛ `REQ-PH02-PRODUCT-PUBLICATION`, `FN-INT-PUBLISH`, `CMP-CON-PUBLISHER`. | `PUB-005` وعقد `IF-ACR-PUBLISH-EVENT` لم يحسما receipt مقابل queued/in-progress/uncertain، توقيت `listing_id`، أو إعادة المحاولة/الرفض النهائي. |
| `SREQ-PH02-REC-004` | `SPLIT_REQUIRED` | الرفض قبل الإرسال مسار مستقل عن الفشل بعد الإرسال والاسترداد؛ `FN-INT-PUBLISH` يميز `REJECTED` عن `FAILED`. | المعيار الحالي يثبت حالة FAILED وإعادة الإرسال فقط؛ لا يثبت رفضاً مسجلاً أو ظهوره لـoperations وACCore. `PUB-005/006` وقنوات الظهور مفتوحة. |
| `SREQ-PH02-CHK-003` | `SPLIT_REQUIRED` | رفض التحقق عند تغيّر السعر/الكمية منفصل عن نتيجة الجلسة الناجحة ولقطات السياسات؛ `REQ-PH02-CHECKOUT-PREPARATION`, `FN-ORD-CHECKOUT`. | `AC-PH02-CHK-003-02` يؤجل حقول tax/currency/delivery؛ `UNKN-006`, `ODEC-009`, `ODEC-003`, `RGAP-PH02-003/009` وTTL للجلسة والعقد مفتوحة. |
| `SREQ-PH03-CNF-005` | `SPLIT_REQUIRED` | صلاحية المستلم/إسقاط البيانات حسب المؤسسة والدور منفصلة عن الإرسال غير المتزامن والتسليم المتكرر واسترداد receiver؛ `IF-ACC-ORDER-CONFIRM`, `CMP-INT-ORDERNOTIFY`, `CMP-CON-ORDERRECEIVER`. | schema الأدوار والمستلمين، ACK/key/retry/recovery مفتوحة؛ `ADR-019-GATE` و`RP-04` لا يحسمان authority/المعنى المالي. |
| `SREQ-PH03-PAY-002` | `SPLIT_REQUIRED`؛ `OWNER_BLOCKED` | اكتمال allocation واحدة لكل SellerOrder منفصل عن اختيار provider attempt مجمّع أو منفصل؛ `FN-PAY-AUTHORIZE`, `CMP-PAY-ORCHESTRATOR`, و`ADR-016`. | provider capability/cardinality، سياسات مالية، `ASSUM-003`, `ODEC-005`, `ADR-016/017-GATE` و`RGAP-PH03-003` مفتوحة؛ لا دمج مع `PAY-003` ولا اختيار settlement/commission/refund/provider. |

**الأعداد بعد Cycle 8:** لم تتغير عن Cycle 7: 233 SREQ، منها 58 `ATOMIC`، و17 `SPLIT_REQUIRED` (10 مصادر تاريخية و7 findings حية)، و1 `MERGE_CANDIDATE`، و0 `DUPLICATE` مؤكداً. لم تتغير صفوف registry أو AC؛ تبقى 188 إحالة `TBD` في `use_case_id`، و209 صفوف بقرارات مفتوحة، ولا توجد صفوف `ACCEPTED` أو اختبارات SREQ منفذة مثبتة.

لم تُراجع بوابات `ADM-001` membership أو lifecycle/policy للترخيص كجزء مستقل من هذه المجموعة، ولا تُعد مغلقة. بقي `DOP-004` مرشح دمج غير مثبت، و`DEN-003` غير مؤكد التكرار ومحجوباً بـ`ODEC-010`. لا تحسّن إعادة التقييم وحدها الجاهزية.
