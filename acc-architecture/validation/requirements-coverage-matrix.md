# مصفوفة تغطية متطلبات PH-01 إلى PH-04

**الدورة:** ARH-2026-11-21-C2<br>**الأساس:** `ea00eb2816722e20a976d6a842c7aaa9c669638c`<br>
**مصادر الربط:** `requirements-registry.csv`، `registry/functions.json`، `registry/interfaces.json`، `registry/elements.json`، ومراجعات الذرية المرحلية.<br>
**ملاحظة:** هذه مصفوفة تغطية مرجعية/اسمية؛ ليست إثباتاً بأن وظيفة أو قناة أو حاوية مطبقة فعلياً.

## ملخص التغطية لكل مرحلة

| المرحلة | REQ رئيسية | SREQ | الحالة DRAFT / OWNER_REVIEW | TBD في function/use_case | صفوف بقرارات مفتوحة | SREQ بتحقق مخطط | AC refs (فريدة) | SYS locations | C2 containers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PH-01 — تأسيس المنصة | 15 | 84 | 87 / 11 | 92 | 70 | 84 | 110 (110) | 3 | 13 |
| PH-02 — الكتالوج والاكتشاف والحجز | 9 | 45 | 48 / 6 | 12 | 40 | 45 | 54 (54) | 3 | 18 |
| PH-03 — المخزون والطلبات والدفع وأحداث التسليم الخارجية | 13 | 59 | 53 / 19 | 35 | 58 | 59 | 59 (59) | 3 | 19 |
| PH-04 — التسليم الداخلي عبر ACCMared | 8 | 27 | 21 / 14 | 35 | 25 | 27 | 28 (28) | 3 | 11 |

## Cycle 2 update

- أضيفت سبعة متطلبات DRAFT ذرية للتدقيق، وحُفظ `SREQ-PH01-AUD-001` بمعياره الأصلي كصف تاريخي `RETIRED`؛ إجمالي السجل الآن 260 صفاً (45 REQ رئيسية و215 SREQ).
- لم يُغلق أي Use Case gap: زاد عدد TBD من 167 إلى 174 بسبب الصفوف الجديدة التي تشير صراحة إلى `RGAP-PH01-005`. بقي عدد C4 bindings المفقودة صفرياً وفق المدقق الهيكلي؛ مجموعة C2 لكل صف جديد موروثة من السجل المجمّع ويظل توزيعها لكل عملية غير مثبت دلالياً.
- زادت الصفوف ذات القرارات المفتوحة من 186 إلى 193 بسبب إبقاء `UNKN-002` على كل صف جديد. لم يُنفذ أي merge؛ بقي `ODEC-010` مفتوحاً.

## Capability / requirement areas

السجل لا يحتوي عموداً معيارياً مستقلاً للـCapability؛ تُستخدم المتطلبات الرئيسية التالية كفهرس تقريبي لمجالات الحزمة، ولا تُعاد تسميتها كقدرات معتمدة.

| المرحلة | المتطلبات الرئيسية المسجلة |
|---|---|
| PH-01 | `REQ-PH01-INSTITUTION-LIFECYCLE` — Institution identity, lifecycle and integration configuration<br>`REQ-PH01-IDENTITY-AND-TRUST` — Platform authentication, sessions and identity linking<br>`REQ-PH01-TENANT-ISOLATION` — Tenant context and cross-institution isolation<br>`REQ-PH01-ADMIN-ACCESS-CONTROL` — Platform user, role and administration control<br>`REQ-PH01-SUPPORT-ACCESS` — Scoped just-in-time support access<br>`REQ-PH01-LICENSE-LIFECYCLE` — Institutional license issuance and lifecycle<br>`REQ-PH01-LICENSE-VALIDATION` — Institutional license validation (online and offline)<br>`REQ-PH01-AUDIT-TRAIL` — Tamper-evident audit of sensitive platform operations<br>`REQ-PH01-GATEWAY-BOUNDARY` — Gateway trust boundary and public/authenticated separation<br>`REQ-PH01-CORE-CONNECTIVITY` — ACCSystem–ACCore connector boundary and connectivity options<br>`REQ-PH01-MESSAGE-RELIABILITY` — Outbox/Inbox and at-least-once delivery<br>`REQ-PH01-IDEMPOTENCY-AND-CORRELATION` — Idempotency keys, correlation and identity mapping<br>`REQ-PH01-POLICY-AND-OWNER-GATES` — Policy registry and owner-gate mechanism<br>`REQ-PH01-OBSERVABILITY-AND-RECOVERY` — Baseline observability, recovery ownership and data boundaries<br>`REQ-PH01-RELEASE-PROVENANCE` — Release integrity and ACCore provenance |
| PH-02 | `REQ-PH02-PRODUCT-PUBLICATION` — Product projection preparation and submission at ACCore<br>`REQ-PH02-LISTING-INGESTION` — Listing admission, validation and creation at ACCSystem<br>`REQ-PH02-LISTING-LIFECYCLE` — Listing update and withdrawal<br>`REQ-PH02-PUBLICATION-RECOVERY` — Publication and search-sync recovery<br>`REQ-PH02-PRODUCT-DISCOVERY` — Browsing, search and product detail for buyer channels<br>`REQ-PH02-OFFER-AND-VISIBILITY` — Indicative price/availability and visibility states<br>`REQ-PH02-CHECKOUT-PREPARATION` — Cart and checkout preparation up to the reservation boundary<br>`REQ-PH02-SELLER-RESERVATION` — Seller-scoped inventory reservation<br>`REQ-PH02-RESERVATION-RECOVERY` — Unknown outcomes, expiry, safe release and reconciliation |
| PH-03 | `REQ-PH03-INVENTORY-COMMITMENT` — Authoritative inventory and stock commitment<br>`REQ-PH03-ORDER-AGGREGATE` — ParentOrder, SellerOrder and order state<br>`REQ-PH03-ORDER-CONFIRMATION` — Order confirmation guards and handoff<br>`REQ-PH03-PAYMENT-ORCHESTRATION` — Payment allocation, authorization and capture<br>`REQ-PH03-PAYMENT-WEBHOOKS` — Provider adapter and webhook handling<br>`REQ-PH03-PAYMENT-RECONCILIATION` — Payment reconciliation<br>`REQ-PH03-VOID-AND-REFUND` — Void and refund operations<br>`REQ-PH03-CANCELLATION-COORDINATION` — Cancellation and return coordination<br>`REQ-PH03-LEDGER-SETTLEMENT-BOUNDARY` — Payment ledger and settlement boundary<br>`REQ-PH03-SAGA-COMPENSATION-AND-RECOVERY` — Checkout saga persistence, compensation and recovery<br>`REQ-PH03-EXTERNAL-DELIVERY-EVENTS` — External and institution-owned delivery event intake<br>`REQ-PH03-BUYER-ORDER-VISIBILITY` — Buyer-facing order, payment and delivery status<br>`REQ-PH03-SOFTWARE-LICENSE-ISSUANCE` — Marketplace software license issuance from confirmed orders |
| PH-04 | `REQ-PH04-DELIVERY-ENABLEMENT` — ACCMared delivery enablement and coexistence<br>`REQ-PH04-SHIPMENT-CREATION` — Shipment creation from confirmed orders<br>`REQ-PH04-DELIVERY-DISPATCH` — Supervisor dispatch and assignment<br>`REQ-PH04-COURIER-OPERATIONS` — Courier task handling and status updates<br>`REQ-PH04-PROOF-OF-DELIVERY` — Proof of delivery capture and integrity<br>`REQ-PH04-OFFLINE-COURIER-SYNC` — Offline courier queue and synchronization<br>`REQ-PH04-DELIVERY-EXCEPTIONS` — Delivery exceptions and cancellation interaction<br>`REQ-PH04-DELIVERY-STATUS-AND-OPERATIONS` — Delivery status propagation and operations |

## الوظائف وUse Case

- كتالوج الوظائف يحتوي **7** معرفات `FN-*`، وجميعها تظهر في نصوص حقول السجل (7/7): `FN-INT-PUBLISH`, `FN-LIC-ACTIVATE`, `FN-LIC-VALIDATE`, `FN-ORD-CHECKOUT`, `FN-ORD-CONFIRM`, `FN-ORD-RESERVE`, `FN-PAY-AUTHORIZE`.
- هذا الربط اسمي فقط: مرجع FN ليس بديلاً عن Use Case مكتملة بعناصر actor/trigger/precondition/outcome/alternatives/state/external effects/verification.
- توجد **174** صفاً في الحزمة تحمل `TBD` في حقل `use_case_id` (PH-01: 92، PH-02: 12، PH-03: 35، PH-04: 35). جميعها تقابل فجوات RGAP مذكورة في وثائق المتطلبات؛ لا تُخترع لها معرفات FN أو Use Case في هذا التقرير.
- PH-04 يفتقر إلى وظيفة مسجلة للشحن/التوجيه/السائق/POD وفق مراجعة RGAP-PH04-001. كما توجد فجوات مستخدم في مراجعات PH-02 وPH-03؛ راجع أقسام فجوات العقود والتتبع.

## الممثلون والمواقع والحاويات

- الممثلون المشار إليهم: 8 (`ACT-COURIER`, `ACT-DELIVERY-SUPERVISOR`, `ACT-INDIVIDUAL`, `ACT-INST-ADMIN`, `ACT-INST-EMPLOYEE`, `ACT-PLATFORM-ADMIN`, `ACT-SUPPORT-STAFF`, `ACT-VISITOR`). أظهر المدقق تطابق معرفاتهم/أنواعهم مع C1 الحالي.
- مواقع C1 المباشرة: 6 (`SYS-ACCMARED-COU`, `SYS-ACCMARED-SUP`, `SYS-ACCOMMERCE`, `SYS-ACCORE`, `SYS-ACCSYSTEM`, `SYS-ACMANAGEMENT`).
- حاويات C2 المذكورة مباشرة في السجل: 29 معرفاً. لا توجد مخالفة ربط بنيوي لصفوف السجل؛ المدقق تحقق من المستوى والنوع وparent ضمن المواقع المدرجة. هذا لا يثبت اكتمال التغطية الدلالية أو التنفيذ.
- لكل SREQ معايير قبول ومراجع تحقق في السجل: 215/215؛ مجموع مراجع AC هو 251 ومعرفاتها الفريدة 251. تضم AUD-001 التاريخي معياراً محفوظاً للمتطلب المتقاعد، ولكل صف جديد AUD-007..013 معيار فريد. المراجع مخططة وليست نتائج تنفيذ.

## الواجهات والأحداث

- يحتوي سجل الواجهات على 10 معرفاً؛ تظهر 6 معرفات في CSV: `IF-ACC-CATALOG-QUERY`, `IF-ACC-EVENT-ENVELOPE`, `IF-ACC-LICENSE-VALIDATE`, `IF-ACC-ORDER-CONFIRM`, `IF-ACC-ORDER-CREATE`, `IF-ACC-PAYMENT-WEBHOOK`.
- واجهات مسجلة دون ذكر مباشر في CSV: `IF-ACC-RESERVE-SAGA`, `IF-ACC-SOFTDL`, `IF-ACR-PUBLISH-EVENT`, `IF-ACR-RESERVATION-RESP`. يلزم قرار مالك/تتبع يحدد هل هي خارج نطاق PH-01–PH-04 أم فجوة ربط؛ عدم ذكرها في CSV لا يثبت غيابها من وثائق المعمارية.

## فجوات RGAP الظاهرة

- **PH-01:** `RGAP-PH01-005`, `RGAP-PH01-006`, `RGAP-PH01-007`, `RGAP-PH01-008`, `RGAP-PH01-010`
- **PH-02:** `RGAP-PH02-001`, `RGAP-PH02-003`
- **PH-03:** `RGAP-PH03-001`, `RGAP-PH03-002`, `RGAP-PH03-004`, `RGAP-PH03-007`
- **PH-04:** `RGAP-PH04-001`

## قرارات مفتوحة وحالة الصفوف

- الحالة: 209 صفوف `DRAFT` و50 `OWNER_REVIEW` وصف واحد `RETIRED`؛ لا توجد صفوف `ACCEPTED` أو `PROPOSED`.
- قرارات مفتوحة غير فارغة: 193 صفاً (منها 60 معرف قرار/بوابة فريداً). لا تُحسب هذه القرارات كاعتماد.
- PH-05 غير موجودة في السجل (0 صف).
