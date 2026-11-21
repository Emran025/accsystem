# مصفوفة تغطية متطلبات PH-01 إلى PH-04

**الدورة:** ARH-2026-11-21-C15<br>**الأساس:** `3aedcffcc743b596356128a5337cba883d90fa32` (`origin/main` عند بدء الدورة الخامسة عشرة)<br>
**مصادر الربط:** `requirements-registry.csv`، `registry/functions.json`، `registry/interfaces.json`، `registry/elements.json`، ومراجعات الذرية المرحلية.<br>
**ملاحظة:** هذه مصفوفة تغطية مرجعية/اسمية؛ ليست إثباتاً بأن وظيفة أو قناة أو حاوية مطبقة فعلياً.

## ملخص التغطية لكل مرحلة

| المرحلة | REQ رئيسية | SREQ | الحالة DRAFT / OWNER_REVIEW | TBD في function/use_case | صفوف بقرارات مفتوحة | SREQ بتحقق مخطط | AC refs (فريدة) | SYS locations | C2 containers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PH-01 — تأسيس المنصة | 15 | 98 | 94 / 11 | 106 | 82 | 98 | 125 (125) | 3 | 13 |
| PH-02 — الكتالوج والاكتشاف والحجز | 9 | 47 | 49 / 6 | 12 | 42 | 47 | 56 (56) | 3 | 18 |
| PH-03 — المخزون والطلبات والدفع وأحداث التسليم الخارجية | 13 | 61 | 54 / 19 | 35 | 60 | 61 | 61 (61) | 3 | 19 |
| PH-04 — التسليم الداخلي عبر ACCMared | 8 | 27 | 21 / 14 | 35 | 25 | 27 | 28 (28) | 3 | 11 |

## Cycle 15 update

- اكتملت سبع مراجعات مستقلة للـfindings الحية ثم التوليف دون إخفاق. بقيت `SREQ-PH01-INST-004`, `SREQ-PH01-MSG-002`, `SREQ-PH02-PUB-004`, `SREQ-PH02-REC-004`, `SREQ-PH02-CHK-003`, `SREQ-PH03-CNF-005` و`SREQ-PH03-PAY-002` جميعها `SPLIT_REQUIRED`؛ `PAY-002` وحده إضافياً `OWNER_BLOCKED`. `REC-004` يظل دون `OWNER_BLOCKED` رغم بوابات قبوله ونشره المفتوحة.
- لم يظهر عقد معتمد أو قرار مالك محلول أو قبول SREQ منفذ أو source change يبرر تعديل المتطلبات أو AC أو صفوف registry أو التصنيفات أو إضافة child IDs. بقيت الأعداد كما هي: 278 صفاً (45 رئيسياً و233 SREQ)، 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`؛ 188 `TBD` في `use_case_id` و209 صفوف بقرارات مفتوحة و270 AC IDs فريدة و29 حاوية C2؛ لكل SREQ AC ومرجع تحقق مخطط، ولا binding مفقود بنيوياً.
- لا تُستنتج بدائل أو سياسات ولا تضاف PH-05؛ تبقى Use Case gaps وقرارات المالك والقبول واضحة. لا تغيير في سجل CSV (279 سطر CRLF، وصفر bare LF)، ولا تثبت التغطية الاسمية/البنيوية التنفيذ أو اكتمالاً دلالياً. يظل `ORD-001` متميزاً عن `ORD-002` و`ORD-007/008`.

## Cycle 14 update

- اكتملت سبع مراجعات مستقلة للـfindings الحية دون إخفاق. بقيت `SREQ-PH01-INST-004`, `SREQ-PH01-MSG-002`, `SREQ-PH02-PUB-004`, `SREQ-PH02-REC-004`, `SREQ-PH02-CHK-003`, `SREQ-PH03-CNF-005` و`SREQ-PH03-PAY-002` كلها `SPLIT_REQUIRED`؛ `PAY-002` وحده إضافياً `OWNER_BLOCKED`. `REC-004` لديه بوابات قبول/نشر مفتوحة لكنه ليس `OWNER_BLOCKED`.
- لم يظهر عقد معتمد أو قرار مالك محلول أو قبول SREQ منفذ يدعم تغيير المتطلبات أو AC أو صفوف السجل أو التصنيفات أو إضافة child IDs. أعداد التغطية لا تتغير: 278 صفاً (45 رئيسياً و233 SREQ)، 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`؛ 188 `TBD` في `use_case_id`، و209 صفوف بقرارات مفتوحة، و270 AC IDs فريدة و29 حاوية C2؛ لا binding مفقود بنيوياً، ولكل SREQ AC ومرجع تحقق مخطط.
- بقيت فجوات Use Case وقرارات المالك والقبول ظاهرة؛ لا تُستنتج بدائل أو سياسات ولا تضاف PH-05. يظل `ORD-001` متميزاً عن `ORD-002` و`ORD-007/008`. CSV غير متغير ومحفوظ بـ279 سطر CRLF وصفر bare LF. التغطية الاسمية/الهيكلية لا تثبت التنفيذ أو اكتمالاً دلالياً.

## Cycle 13 update

- أعادت سبع مراجعات مستقلة تقييم findings التفكيك الحية ثم وُحّدت دون إخفاق. بقيت `SREQ-PH01-INST-004`, `SREQ-PH01-MSG-002`, `SREQ-PH02-PUB-004`, `SREQ-PH02-REC-004`, `SREQ-PH02-CHK-003`, `SREQ-PH03-CNF-005` و`SREQ-PH03-PAY-002` كلها `SPLIT_REQUIRED`؛ `PAY-002` وحده يظل أيضاً `OWNER_BLOCKED`. لا دليل جديد يدعم تغيير requirement أو AC أو registry أو التصنيف أو إنشاء child IDs.
- أعيد التحقق من السجل: **278** صفاً (45 REQ رئيسية و233 SREQ)، 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`. بقيت `TBD` في `use_case_id` عند 188، والصفوف ذات القرارات المفتوحة عند 209 (60 مرجع قرار/بوابة فريداً باستثناء مرجع RGAP المنفصل)، ومعرفات AC الفريدة عند 270 وحاويات C2 عند 29؛ لا binding مفقود بنيوياً، ولكل SREQ AC ومرجع تحقق مخطط.
- لا تغير في الصفوف أو الخيارات أو معرفات الوظائف/Use Cases أو أدلة المصدر منذ Cycle 12؛ لم تُضف متطلبات PH-05. تبقى فجوات Use Case وقرارات المالك والقبول ظاهرة، ولا تعني التغطية المرجعية أو فحوص البنية نجاحاً وظيفياً. يظل `ORD-001` متميزاً عن `ORD-002` و`ORD-007/008`.

## Cycle 12 update

- أعادت سبع مراجعات مستقلة تقييم findings التفكيك الحية، واحدة لكل finding، ثم وُحّدت دون إخفاق. بقيت `SREQ-PH01-INST-004`, `SREQ-PH01-MSG-002`, `SREQ-PH02-PUB-004`, `SREQ-PH02-REC-004`, `SREQ-PH02-CHK-003`, `SREQ-PH03-CNF-005` و`SREQ-PH03-PAY-002` كلها `SPLIT_REQUIRED`؛ يظل `PAY-002` أيضاً `OWNER_BLOCKED`. لا دليل جديد يدعم تغيير requirement أو AC أو registry أو التصنيف أو إنشاء child IDs.
- أُعيد حساب السجل غير المتغير: **278** صفاً (45 REQ رئيسية و233 SREQ)، منها 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`. بقيت `TBD` في `use_case_id` عند 188؛ والصفوف ذات القرارات المفتوحة عند 209 (60 مرجع قرار/بوابة فريداً باستثناء مرجع RGAP المنفصل). توجد 270 AC IDs فريدة و29 حاوية C2 فريدة، ولا binding مفقود بنيوياً؛ لكل SREQ وعددها 233 AC ومرجع تحقق مخطط، لا دليل تنفيذ.
- لم تتغير خيارات أو صفوف السجل أو معرفات الوظائف/Use Cases؛ لا توجد متطلبات PH-05. يحافظ التقييم على `ORD-001` متميزاً عن `ORD-002` وعن مسودتي `ORD-007/008`، وتبقى فجوات Use Case وقرارات المالك والقبول ظاهرة. CSV محفوظ بـ279 سطر CRLF وصفر bare LF.

## Cycle 2 update (historical)

- أضيفت سبعة متطلبات DRAFT ذرية للتدقيق، وحُفظ `SREQ-PH01-AUD-001` بمعياره الأصلي كصف تاريخي `RETIRED`؛ إجمالي السجل الآن 260 صفاً (45 REQ رئيسية و215 SREQ).
- لم يُغلق أي Use Case gap: زاد عدد TBD من 167 إلى 174 بسبب الصفوف الجديدة التي تشير صراحة إلى `RGAP-PH01-005`. بقي عدد C4 bindings المفقودة صفرياً وفق المدقق الهيكلي؛ مجموعة C2 لكل صف جديد موروثة من السجل المجمّع ويظل توزيعها لكل عملية غير مثبت دلالياً.
- زادت الصفوف ذات القرارات المفتوحة من 186 إلى 193 بسبب إبقاء `UNKN-002` على كل صف جديد. لم يُنفذ أي merge؛ بقي `ODEC-010` مفتوحاً.

## Cycle 3 update

- أُعيد تقييم 17 finding تفكيكية حية؛ فُكك `SREQ-PH01-AUTH-001` إلى AUTH-007 وAUTH-008، وفُكك `SREQ-PH01-LIC-001` إلى LIC-007 وLIC-008. احتُفظ بكل صف أصلي ومعاييره بحالة `RETIRED`، وأُضيفت أربعة صفوف DRAFT بمعايير قبول فريدة، مع الإبقاء على روابط المتطلبات والقرارات والفجوات.
- أصبح السجل 264 صفاً: 45 REQ رئيسية و219 SREQ. PH-01 يضم 15 REQ و88 SREQ؛ تغير العدد DRAFT/OWNER_REVIEW في PH-01 إلى 89/11، مع 3 صفوف SREQ تاريخية `RETIRED` ضمن إجمالي المرحلة.
- ارتفع عدد TBD في `use_case_id` من 174 إلى 178 (PH-01: 96؛ PH-02: 12؛ PH-03: 35؛ PH-04: 35). بقيت قرارات المالك مفتوحة في 197 صفاً، مع 60 معرف قرار/بوابة فريداً؛ ولم يُغلق C4 binding مفقود وفق المدقق الهيكلي (0).
- أصبحت كل SREQ الـ219 تحمل AC ومرجع تحقق مخططاً؛ عدد معرّفات AC الفريدة 255. الخطة لا تثبت تنفيذ اختبار أو صلاحية دلالية، ومجموعة C2 الموروثة للصفوف الجديدة لا تثبت التخصيص الدلالي لكل عملية.
- بقي DOP-004 مرشح دمج دون إثبات تكافؤه مع DEX-001 أو DOP-003، وبقي DEN-003 محجوباً بـ`ODEC-010`؛ لم ينفذ دمج أو حذف.

## Cycle 4 update

- أُعيد تقييم 15 finding حية؛ فُككت ستة مصادر مدعومة إلى 12 صفاً جديداً، وحُفظت المصادر ومعاييرها الأصلية كـ`RETIRED`. بقيت تسعة findings `SPLIT_REQUIRED` مفتوحة؛ لم يُعد تصنيف غير محسوم إلى `ATOMIC` ولم يُنفذ دمج.
- السجل الآن 276 صفاً: 45 REQ رئيسية و231 SREQ؛ PH-01: 15 REQ/98 SREQ، PH-02: 9 REQ/47 SREQ، PH-03: 13 REQ/59 SREQ، PH-04: 8 REQ/27 SREQ.
- الحالات: 217 `DRAFT`، 50 `OWNER_REVIEW`، 9 `RETIRED`، 0 `ACCEPTED`. أصبح `TBD` في `use_case_id` 188؛ والقرارات المفتوحة موجودة في 207 صفاً من السجل، مع بقاء معرفات القرار كما هي.
- كل SREQ له AC ومرجع تحقق مخطط (231/231); معرّفات AC الفريدة 268. لا يثبت ذلك صلاحية المعايير أو تنفيذ الاختبارات. C4 bindings المفقودة بنيوياً: 0؛ مجموعة الحاويات الجديدة موروثة ولا تثبت تخصيصاً دلالياً.
- بقيت حماية أسرار INST-004، عضوية المؤسسات في ADM-001، lifecycle/propagation semantics للترخيص، response contract لـPUB-004/REC-004، قبول checkout، recipient projection، ORD-001/ORD-002 equivalence وسياسات PAY-002 مفتوحة. لا function/use-case ID أو owner decision جديد اختُرع.

## Cycle 5 update

- أُعيد تقييم تسعة findings حية بصورة مستقلة. أعيد تصنيف `SREQ-PH01-LICV-003` إلى `ATOMIC` لأن signature/identity/grant/offline predicates تحقق نتيجة تحقق محلية واحدة؛ بقيت فجوة AC لتغطية workflow/grant bounds وعدم إجراء network call، وبقيت `UNKN-009` و`ODEC-014` و`LIC-001` مفتوحة. ظلت findings الثمانية الأخرى `SPLIT_REQUIRED`؛ لا child IDs أو function/use-case IDs جديدة ولا تغييرات في requirements/registry rows.
- بقي السجل 276 صفاً (45 رئيسياً و231 SREQ)، دون تغيير في حالات الصفوف. تغير تصنيف الذرية فقط: `ATOMIC` من 55 إلى 56 و`SPLIT_REQUIRED` من 18 إلى 17 (9 مصادر تاريخية `RETIRED` و8 findings حية)؛ بقي `MERGE_CANDIDATE` واحداً. ظل `TBD` في use_case_id 188، وصفوف القرارات المفتوحة 207، وSREQ ذات AC/مرجع تحقق مخطط 231/231، ومعرفات AC الفريدة 268، وC4 bindings المفقودة بنيوياً 0.
- `SREQ-PH03-ORD-001` يبقى منفصلاً عن `ORD-002`: تدعم الأدلة توصية بتقسيم مستقبلي بين إنشاء الطلبات محلياً وإعادة المحاولة idempotently، دون إنشاء IDs أو تغيير الصف؛ بقي `ODEC-003` مفتوحاً. ظلت membership في ADM-001 وبوابات lifecycle/propagation للترخيص وفجوات REC-004 وCHK-003 كما هي. بقي DOP-004 مرشح دمج غير مثبت، وDEN-003 غير مؤكد التكرار ومحجوباً بـ`ODEC-010`.

## Cycle 6 update

- أُعيدت مراجعة findings الثمانية الحية `SPLIT_REQUIRED` بصورة مستقلة، ثم وُحّدت النتائج. بقيت كلها دون تغيير: الأدلة الحالية لا تبرر إعادة تصنيف أو إنشاء child IDs، ولا توجد قرارات مالك أو أدلة تنفيذ جديدة.
- لم تتغير المتطلبات أو ACs أو CSV: السجل 276 صفاً (45 رئيسياً، 231 SREQ)؛ الحالات 217 `DRAFT`، و50 `OWNER_REVIEW`، و9 `RETIRED`، و0 `ACCEPTED`. تصنيف الذرية 56 `ATOMIC`، و17 `SPLIT_REQUIRED` (9 مصادر تاريخية و8 findings حية)، و1 `MERGE_CANDIDATE`، و0 `DUPLICATE` مؤكد.
- بقيت `TBD` في `use_case_id` عند 188، والصفوف ذات قرارات مفتوحة عند 207 (60 معرف قرار/بوابة فريداً)، وSREQ ذات AC ومراجع تحقق مخططة 231/231، ومعرفات AC الفريدة 268، وC4 bindings المفقودة بنيوياً 0. جميع أرقام التغطية كما في Cycle 5؛ لا تثبت التنفيذ أو دلالات الربط.
- أبرز فجوات القبول/العقد ما زالت قائمة: `REC-004` يثبت FAILED/resubmission ولا يثبت ظهور الرفض أو رؤيته من operations وACCore؛ قبول `CHK-003` غير مكتمل. يظل `ORD-001` منفصلاً عن `ORD-002`، مع احتمال حد مفاهيمي مستقبلي بين الإنشاء المحلي وduplicate-safe replay، دون IDs؛ `ODEC-003` وعقد API مفتوحان. تبقى عضوية ADM-001 وبوابات lifecycle/policy للترخيص مفتوحة؛ DOP-004 غير مثبت كدمج، وDEN-003 محجوباً بـ`ODEC-010`.
- التغييرات في هذه الدورة تقريرية فقط: تقارير التحقق الأربعة تحت `acc-architecture/validation/`؛ لم تتغير عناصر التغطية أو registry rows.

## Cycle 7 update

- أعادت المراجعة المستقلة تقييم findings الثمانية الحية: بقيت سبعة `SPLIT_REQUIRED`؛ والأدلة تدعم تفكيك `SREQ-PH03-ORD-001` إلى `ORD-007` للمعاملة المحلية الذرية لإنشاء ParentOrder/SellerOrders/outbox و`ORD-008` لإعادة المحاولة المكررة/المتزامنة. حُفظ المصدر ومعياره الأصلي كـ`RETIRED`. يبقى `ORD-002` مستقلاً؛ لم يُنشأ أي function/use-case ID ولم يُحسم owner gate.
- ارتفع السجل من 276 إلى 278 صفاً (45 رئيسياً و233 SREQ): الحالات الحالية 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`. PH-03 يضم 61 SREQ، و54/19 `DRAFT`/`OWNER_REVIEW`، و35 TBD، و60 صفاً بقرارات مفتوحة، و61 SREQ بتحقق مخطط و61 AC مرجعاً فريداً في المرحلة.
- تغيرت الذرية من 56 إلى 58 `ATOMIC`؛ بقي `SPLIT_REQUIRED` عند 17 (10 مصادر تاريخية متقاعدة و7 findings حية)، و`MERGE_CANDIDATE` واحد و0 `DUPLICATE` مؤكد. بقي TBD في `use_case_id` عند 188؛ ارتفعت صفوف القرارات المفتوحة 207→209 مع 60 مرجع قرار/بوابة فريداً؛ ارتفعت AC IDs الفريدة 268→270. جميع 233 SREQ لها AC ومرجع تحقق مخطط، وC4 bindings المفقودة بنيوياً 0؛ هذا لا يثبت التنفيذ أو الدلالة.
- تظل عضوية `ADM-001` وبوابات lifecycle/policy للترخيص، قبول `REC-004` و`CHK-003`، وعقد `ORD-007/008` و`ODEC-003` مفتوحة. `DOP-004` مرشح غير مثبت و`DEN-003` محجوب بـ`ODEC-010`. فشل strict-ready المتوقع ما زال قائماً؛ نتائج validators البنيوية لا تعني جاهزية.

## Cycle 8 update

- أُعيد تقييم findings التفكيك السبعة الحية بصورة مستقلة ثم وُحّدت النتائج. بقيت كلها `SPLIT_REQUIRED`؛ لا child IDs أو إعادة تصنيف أو merge مدعوم بالدليل المتاح. `PAY-002` مسدود أيضاً بقرارات المالك، مع بقاء تصنيفه `SPLIT_REQUIRED`.
- الحدود الاختبارية باقية: `INST-004` configuration retrieval مقابل سرية الأسرار؛ `MSG-002` receipt/claim مقابل once-only effect وduplicate recovery؛ `PUB-004` ثبات المفتاح مقابل lifecycle الاستجابة/Outbox؛ `REC-004` الرفض السابق للإرسال مقابل failure/recovery؛ `CHK-003` validation failure مقابل snapshot الناجح؛ `CNF-005` recipient/role projection مقابل dispatch/recovery؛ `PAY-002` allocation completeness مقابل aggregate/separate provider attempts.
- لم تتغير المتطلبات أو ACs أو الصفوف. السجل يبقى 278 صفاً (45 رئيسياً و233 SREQ): 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`. الذرية 58 `ATOMIC` و17 `SPLIT_REQUIRED` (10 مصادر متقاعدة و7 findings حية)، و1 `MERGE_CANDIDATE`؛ تبقى `TBD` عند 188 والصفوف ذات قرارات مفتوحة عند 209 (60 مرجع قرار/بوابة فريداً، باستثناء RGAP المنفصل). معرفات AC الفريدة 270، وحاويات C2 الفريدة 29، والـC4 bindings المفقودة بنيوياً 0.
- بوابات كل finding وتفاصيل gaps مسجلة في مراجعة الذرية. جميع مراجع التحقق تظل مخططة؛ لا owner gate أُغلق ولا اختبار SREQ نُفذ أو قُبل في هذه الدورة.

## Cycle 9 update

- أعادت سبعة مراجعين مستقلين فحص findings الحية على الأساس `5ff34b84f80327e696c60c265615f48706143d73`؛ اكتملت المراجعات السبعة ثم التوليف دون إخفاق. التصنيفات بقيت كما في Cycle 8، ولم تدعم الأدلة تغييراً في المتطلبات أو AC أو registry أو إنشاء child IDs.
- أُعيد حساب السجل: 278 صفاً (45 REQ و233 SREQ)، منها 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`؛ 188 `TBD` في `use_case_id` و209 صفوف بقرارات مفتوحة (60 مرجعاً فريداً باستثناء `RGAP-PH02-004`)؛ 270 AC IDs فريدة و29 حاوية C2؛ لا missing C4 binding بنيوي. لكل SREQ AC ومرجع تحقق مخطط (233/233)، وليس ذلك دليلاً على التنفيذ.
- بقيت `INST-004`, `MSG-002`, `PUB-004`, `REC-004`, `CHK-003`, `CNF-005` و`PAY-002` مصنفة `SPLIT_REQUIRED`؛ `PAY-002` يظل `OWNER_BLOCKED`. تفاصيل الحدود والبوابات في مراجعة الذرية. يظل `ORD-001` محفوظاً ومتميزاً عن `ORD-002` و`ORD-007/008`، وعضوية `ADM-001` وبوابات lifecycle/policy الترخيص و`REC-004`/`CHK-003` غير محسومة. `DOP-004` لا يزال merge candidate غير مثبت و`DEN-003` محجوباً بـ`ODEC-010`.

## Cycle 10 update

- أُعيدت مراجعة findings التفكيك السبعة الحية بصورة مستقلة، ثم وُحّدت النتائج دون إخفاق. بقيت جميعها `SPLIT_REQUIRED`، و`PAY-002` كذلك `OWNER_BLOCKED`؛ لا أدلة جديدة تدعم تعديل requirement أو AC أو registry أو إنشاء IDs أو تغيير التصنيف.
- إعادة الحساب من السجل الحالي: 278 صفاً (45 REQ رئيسية و233 SREQ)، منها 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`. تصنيف الذرية 58 `ATOMIC` و17 `SPLIT_REQUIRED` (10 مصادر متقاعدة و7 findings حية) و1 `MERGE_CANDIDATE` و0 `DUPLICATE` مؤكد.
- بقيت `TBD` في `use_case_id` عند 188؛ و209 صفوف بقرارات مفتوحة، مع 60 مرجع قرار/بوابة مميزاً بعد استثناء `RGAP-PH02-004`. توجد 270 AC IDs فريدة و29 حاوية C2 فريدة، ولا missing C4 binding بنيوي. لكل SREQ وعددها 233 معيار قبول ومرجع تحقق مخطط (233/233)، وليس ذلك دليلاً على التنفيذ.
- لا تغيير في خيارات المعمارية أو الحالات أو التدفقات أو ADR أو معرفات الوظائف/حالات الاستخدام؛ تبقى عضوية `ADM-001` وبوابات lifecycle/policy الترخيص، وقيود `ORD-001` المتميزة عن `ORD-002` و`ORD-007/008`، ونقص أدلة `REC-004`/`CHK-003` كما هي. يوضح تقرير الذرية بوابات findings السبعة؛ يظل TTL الخاص بـ`CHK-003` مجهولاً ولا تُستنتج سياسة OAuth/mTLS أو settlement/commission/refund أو provider.

## Cycle 11 update

- أُعيد تقييم findings التفكيك السبعة الحية كلٌّ بمراجع مستقل، ثم جُمعت النتائج دون إخفاق. بقيت كلها `SPLIT_REQUIRED`، و`PAY-002` بقي `OWNER_BLOCKED`؛ لا يدعم الدليل الحالي تغيير requirement أو AC أو registry أو التصنيف أو إنشاء child IDs.
- أُعيد الحساب من CSV غير المتغير: 278 صفاً (45 REQ رئيسية و233 SREQ)، منها 218 `DRAFT` و50 `OWNER_REVIEW` و10 `RETIRED` و0 `ACCEPTED`. الذرية: 58 `ATOMIC` و17 `SPLIT_REQUIRED` (10 مصادر متقاعدة و7 findings حية) و1 `MERGE_CANDIDATE` و0 `DUPLICATE` مؤكداً.
- بقيت `TBD` في `use_case_id` عند 188؛ و209 صفوف بقرارات مفتوحة، مع 60 مرجع قرار/بوابة فريداً بعد استثناء `RGAP-PH02-004`. توجد 270 AC IDs فريدة و29 معرف C2 فريداً، ولا missing C4 binding بنيوي. لكل SREQ وعددها 233 AC ومرجع تحقق مخطط (233/233)، لا دليل تنفيذ.
- لا قرار مالك أو اختبار قبول SREQ منفذ أُضيف. تبقى عضوية `ADM-001` وبوابات lifecycle/policy الترخيص و`REC-004`/`CHK-003` كما هي؛ يحفظ `ORD-001` متميزاً عن `ORD-002` و`ORD-007/008`. لا يُستنتج OAuth/mTLS أو TTL أو سياسات settlement/commission/refund/provider. تفاصيل بوابات findings في تقرير الذرية.

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
- توجد **188** صفاً في الحزمة تحمل `TBD` في حقل `use_case_id` (PH-01: 106، PH-02: 12، PH-03: 35، PH-04: 35). جميعها تقابل فجوات RGAP مذكورة في وثائق المتطلبات؛ لا تُخترع لها معرفات FN أو Use Case في هذا التقرير.
- PH-04 يفتقر إلى وظيفة مسجلة للشحن/التوجيه/السائق/POD وفق مراجعة RGAP-PH04-001. كما توجد فجوات مستخدم في مراجعات PH-02 وPH-03؛ راجع أقسام فجوات العقود والتتبع.

## الممثلون والمواقع والحاويات

- الممثلون المشار إليهم: 8 (`ACT-COURIER`, `ACT-DELIVERY-SUPERVISOR`, `ACT-INDIVIDUAL`, `ACT-INST-ADMIN`, `ACT-INST-EMPLOYEE`, `ACT-PLATFORM-ADMIN`, `ACT-SUPPORT-STAFF`, `ACT-VISITOR`). أظهر المدقق تطابق معرفاتهم/أنواعهم مع C1 الحالي.
- مواقع C1 المباشرة: 6 (`SYS-ACCMARED-COU`, `SYS-ACCMARED-SUP`, `SYS-ACCOMMERCE`, `SYS-ACCORE`, `SYS-ACCSYSTEM`, `SYS-ACMANAGEMENT`).
- حاويات C2 المذكورة مباشرة في السجل: 29 معرفاً. لا توجد مخالفة ربط بنيوي لصفوف السجل؛ المدقق تحقق من المستوى والنوع وparent ضمن المواقع المدرجة. هذا لا يثبت اكتمال التغطية الدلالية أو التنفيذ.
- لكل SREQ معايير قبول ومراجع تحقق في السجل: 233/233؛ مجموع معرفات AC الفريدة 270. يحتفظ السجل بمعايير الصفوف التاريخية المتقاعدة AUD-001 وAUTH-001 وLIC-001 وORD-001، وللصفوف الجديدة AUD-007..013 وAUTH-007..008 وLIC-007..008 وORD-007/008 معايير فريدة. المراجع مخططة وليست نتائج تنفيذ.

## الواجهات والأحداث

- يحتوي سجل الواجهات على 10 معرفاً؛ تظهر 6 معرفات في CSV: `IF-ACC-CATALOG-QUERY`, `IF-ACC-EVENT-ENVELOPE`, `IF-ACC-LICENSE-VALIDATE`, `IF-ACC-ORDER-CONFIRM`, `IF-ACC-ORDER-CREATE`, `IF-ACC-PAYMENT-WEBHOOK`.
- واجهات مسجلة دون ذكر مباشر في CSV: `IF-ACC-RESERVE-SAGA`, `IF-ACC-SOFTDL`, `IF-ACR-PUBLISH-EVENT`, `IF-ACR-RESERVATION-RESP`. يلزم قرار مالك/تتبع يحدد هل هي خارج نطاق PH-01–PH-04 أم فجوة ربط؛ عدم ذكرها في CSV لا يثبت غيابها من وثائق المعمارية.

## فجوات RGAP الظاهرة

- **PH-01:** `RGAP-PH01-005`, `RGAP-PH01-006`, `RGAP-PH01-007`, `RGAP-PH01-008`, `RGAP-PH01-010`
- **PH-02:** `RGAP-PH02-001`, `RGAP-PH02-003`
- **PH-03:** `RGAP-PH03-001`, `RGAP-PH03-002`, `RGAP-PH03-004`, `RGAP-PH03-007`
- **PH-04:** `RGAP-PH04-001`

## قرارات مفتوحة وحالة الصفوف

- الحالة الحالية: 218 صفاً `DRAFT` و50 `OWNER_REVIEW` و10 صفوف `RETIRED`؛ لا توجد صفوف `ACCEPTED` أو `PROPOSED`.
- قرارات مفتوحة غير فارغة: 209 صفوف (منها 60 معرف قرار/بوابة فريداً، باستثناء مرجع RGAP المنفصل). لا تُحسب هذه القرارات كاعتماد.
- PH-05 غير موجودة في السجل (0 صف).
