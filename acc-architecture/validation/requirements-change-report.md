# تقرير تغييرات دورة تقوية المتطلبات

**Cycle ID:** ARH-2026-11-21-C1<br>
**Base commit:** `a8f38d19188588eadaa68fc6142a20b9983d5b58`<br>
**Final implementation commit:** `0c37461b5c4a6faa5cbbcb3f92155affccf3f69c` (pushed to `origin/main`).<br>
**Push target:** `origin/main` وفق التفويض؛ بدون force push.

## التغييرات ضمن النطاق

- `acc-architecture/execution-phases/validate_requirements.py`: توسيع المدقق للتحقق من الممثلين والوظائف المسجلة، ربط TBD بـRGAP موثق، مطابقة صفوف metadata/sub-requirement/related/AC بين CSV والوثائق، اشتراط AC للـSREQ، إضافة `--strict-ready`، وحصر قراءة الوثائق داخل مجلد المرحلة مع معالجة أخطاء القراءة.
- `acc-architecture/execution-phases/tests/test_validate_requirements.py`: 9 اختبارات regression للـbaseline ومراجع actor/function وTBD/AC والمزامنة وstrict-ready والسجل الفارغ ورفض مسار الوثيقة خارج المرحلة.
- `acc-architecture/execution-phases/README.md`: تحديث حالة PH-01..PH-04 إلى مسودات موجودة غير معتمدة وتصحيح عبارة السجل الفارغ؛ PH-05 يبقى بلا متطلبات.
- `acc-architecture/validation/atomicity-review-report.md`: نتائج وتصنيفات الذرية لكل 208 SREQ.
- `acc-architecture/validation/requirements-coverage-matrix.md`: تغطية المراحل والوظائف والممثلين والمواقع والحاويات والواجهات والـAC والفجوات.
- `acc-architecture/validation/requirements-readiness-report.md`: يوضح الموانع وما لم يثبت، دون إعلان جاهزية.
- `acc-architecture/validation/requirements-change-report.md`: هذا السجل.

لم تُعدّل application code أو ملفات خارج `acc-architecture/`، ولم تُعدّل وثائق المتطلبات أو CSV/ADR/architecture-manifest/validation-status في هذه الدورة.

## أرقام السجل والمراجعة

- السجل: 253 صفاً (45 main و208 SREQ). PH-01: 15/77، PH-02: 9/45، PH-03: 13/59، PH-04: 8/27؛ لا صفوف PH-05.
- تصنيفات SREQ: `ATOMIC` 30، `SPLIT_REQUIRED` 17، `MERGE_CANDIDATE` 5، `ARCHITECTURAL_CONSTRAINT` 32، `POLICY_RULE` 33، `ACCEPTANCE_CRITERION_ONLY` 3، `NEEDS_USE_CASE` 41، `DUPLICATE` 1، `OUT_OF_PHASE` 0، `BLOCKED_BY_OWNER_DECISION` 46. صُنفت جميع المتطلبات الفرعية الـ208 وربط كل تصنيف بصف السجل.
- PH-04 لديها 0 SREQ مصنفة `SPLIT_REQUIRED`؛ وصفت المراجعة 8 متطلبات رئيسية فيها بأنها مركبة على مستوى REQ. هذان مستويان مختلفان.
- الحالات: 203 `DRAFT` و50 `OWNER_REVIEW`، و0 `ACCEPTED`. عدد 167 صفاً بها `TBD` موثقاً بفجوات RGAP، و186 صفاً بها قرارات مفتوحة. جميع 208 SREQ لها مراجع تحقق مخططة و244 مرجع AC فريد؛ التخطيط لا يثبت التنفيذ.
- 7/7 وظائف مسجلة تظهر في نص السجل، و6/10 واجهات مسجلة تظهر مباشرة في CSV؛ لا يستنتج من ذلك اكتمال التغطية الدلالية أو التنفيذ.

## التحقق

- مدقق المتطلبات `--check` و`--check --require-rows`: نجحا على 253 صفاً. الاستعلام `--phase PH-01` أعاد 92 صفاً، و`--phase PH-02 --location SYS-ACCORE` أعاد 30، و`--container CNT-ACC-CATALOG` أعاد 20.
- `--check --strict-ready`: فشل كما ينبغي لمسودات غير جاهزة، وسجّل 814 مخالفة لبوابات الجاهزية؛ هذا ليس فشلاً في الفحص البنيوي ولا يثبت الجاهزية.
- `python3 -m unittest discover -s acc-architecture/execution-phases/tests -v`: 9/9 اختبارات ناجحة. `python3 -m unittest discover -s architecture-assistant/tests -v`: 65/65 اختباراً ناجحاً.
- `validate_architecture.py`: exit 0؛ فحوص بنيوية/سجلية على 4 مستويات فقط، دون شهادة دلالية أو أمنية أو مطابقة schema كاملة.
- `validate_artifact_depth.py`: exit 0؛ 88 مراجعة، 0 incomplete و0 findings، مع الحالة `STRUCTURE_PRESENT_REQUIRES_HUMAN_REVIEW`؛ لا يحل محل المراجعة البشرية.
- `validate_consistency_artifacts.py`: exit 0؛ 65/65 سجلاً و0 findings، مع الحالة `STRUCTURAL_RECORDS_PRESENT_REQUIRES_SEMANTIC_REVIEW`.
- `validate_traceability.py` و`validate_references.py`: exit 0. `validate_diagrams.py`: exit 0، render/check لـ55 كتلة Mermaid؛ صحة C4 الدلالية وموافقة المالك غير متحققتين.
- `validate_release_status.py`: exit 0؛ `Gate7=IN_PROGRESS` و`manifest=IN_PROGRESS` و0 findings مفتوحة في التدقيق المحدود، لا اعتماد أو جاهزية. `generate_coverage_report.py`: exit 0؛ C1 15/7/8، C2 40/17/23، C3 35/35/0، DECISION 22/22/0 (الإجمالي/التقسيم المكتمل/الاستثناءات غير المكتملة).
- `/home/ubuntu/work/acc-architecture-handoff/run-remaining-validations.sh`: تعذر التشغيل، الملف غير موجود (`No such file or directory`). و`/home/ubuntu/work/acc-architecture-handoff/audit-remaining-registries-links.py`: تعذر التشغيل، الملف غير موجود في المسار المحدد (خطأ فتح الملف). لم يُدّع تشغيلهما؛ شُغّلت بدائل architecture-assistant أعلاه.
- `git diff --check` و`git diff --cached --check`: ينجحان بعد آخر تحديث للتقرير وإصلاح تنسيق Markdown؛ لا توجد whitespace errors قبل commit.

## Findings المتبقية

17 SREQ تحتاج تفكيكاً، و5 مرشحة للدمج، وواحدة مكررة وفق المراجعة. توجد 167 إحالة TBD موثقة، و186 صفاً بقرارات مفتوحة، و208 SREQ لها تحقق مخطط غير منفذ. تبقى هذه findings معلنة وليست أخطاءً بنيوية مغلقة. لا توجد صفوف Accepted، لذلك الحزمة غير جاهزة كخط أساس للتنفيذ.

## الخطوة التالية

تتطلب الدورة التالية مراجعة قرارات المالك، واستكمال Use Cases/الفجوات الموثقة، ومعالجة 17 حالة `SPLIT_REQUIRED` و5 `MERGE_CANDIDATE` وحالة `DUPLICATE` مع حفظ علاقات المتطلبات ومعايير القبول. لا تُعلن الجاهزية قبل إغلاق هذه البوابات وتنفيذ التحقق وقبول أصحاب القرار؛ تبقى القرارات والسياسات غير المحسومة لدى مالكيها.


## نتائج التحقق بعد دفع commit الدورة

- بعد الدفع، أعاد `git fetch origin main` النتيجة `HEAD == origin/main == 0c37461b5c4a6faa5cbbcb3f92155affccf3f69c`، مع divergence `0/0`.
- بعد الدفع، نجح `--check` و`--check --require-rows` على 253 صفاً، وأعادت الاستعلامات 92/30/20 صفاً. نجحت اختبارات المدقق المخصص 9/9 واختبارات architecture-assistant 65/65.
- بعد الدفع، خرجت validators المعمارية البديلة جميعها برمز 0: architecture، artifact depth، consistency، traceability، references، diagrams، release status، وتقرير التغطية. تبقى نتائج artifact depth/consistency مشروطة بالمراجعة البشرية/الدلالية، وrenderer لا يثبت صحة C4 الدلالية أو موافقة المالك.
- بعد الدفع، بقي `--check --strict-ready` فاشلاً على 814 مخالفة متوقعة لبوابات الجاهزية؛ الحزمة ما تزال مسودة وغير جاهزة للتنفيذ. نجح `git diff --check`.


## Cycle 2: ARH-2026-11-21-C2

**Base commit:** `ea00eb2816722e20a976d6a842c7aaa9c669638c` (`origin/main` بعد fetch عند بدء الدورة الثانية).
**Implementation commit:** `3371089ea74324e1a0a0414471260784bccc836a` (commit محتوى الدورة؛ يليه commit توثيقي لتثبيت هذا المرجع).
**Push target:** `origin/main` وفق التفويض؛ دون force push.

### التغييرات

- `acc-architecture/execution-phases/requirements-registry.csv`: أُبقي `SREQ-PH01-AUD-001` بمعياره الأصلي بحالة `RETIRED`، وأضيفت سبعة SREQ ذرية DRAFT بمعايير قبول فريدة AUD-007..013؛ لكل منها `UNKN-002` و`TBD (RGAP-PH01-005)` كما بقيت الفجوات مفتوحة.
- `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-AUDIT-TRAIL.md`: تحديث سجل الصفوف والـAC والتتبع، مع سجل حفظ صريح. خريطة الممثلين وحاويات C2 للصفوف الجديدة موروثة من الصف المجمّع ولا تدعي ربطاً خاصاً بكل عملية.
- `atomicity-review-report.md`, `requirements-coverage-matrix.md`, `requirements-readiness-report.md`: تحديث تصنيفات 23 finding ومجاميع الدورة والتغطية والجاهزية. لم يثبت دمج آمن؛ DOP-004 وحده بقي مرشحاً؛ DEN-003 غير مثبت التكرار وبقي محجوباً بـODEC-010.

### counts القابلة لإعادة الحساب

- المتطلبات الرئيسية: 45 (بدون تغيير). SREQ: 208 → 215؛ إجمالي صفوف السجل: 253 → 260.
- حالة AUD-001: صف تاريخي واحد RETIRED + سبعة DRAFT ذرية؛ لم تُحذف capability أو فئة عملية.
- التدقيق الذري: ATOMIC 30 → 39؛ تصنيف SPLIT_REQUIRED في السجل 17 → 18 (واحد تاريخي متقاعد تفكيكه مكتمل؛ 17 finding حي متبقٍ). المرشحون للدمج 5 → 1، والتكرار غير المثبت 1 → 0، مع DEN-003 محجوب بقرار مالك.
- `TBD` في use_case_id: 167 → 174؛ فجوات Use Case لم تُغلق. الصفوف ذات القرارات المفتوحة: 186 → 193 (60 معرف قرار/بوابة فريداً).
- C4 binding المفقود: 0 → 0 حسب المدقق البنيوي؛ جميع الصفوف الجديدة ورثت مجموعة الحاويات المعلنة في الصف المصدر، والتخصيص الدلالي لكل عملية لا يزال غير مثبت.
- AC فريد: 244 → 251؛ SREQ ذات مراجع AC والتحقق المخطط: 208/208 → 215/215. لا معيار أو اختبار وظيفي تم تنفيذه في هذه الدورة.

### نتائج التحقق

- المدقق المخصص: نجح `--check --require-rows` على 260 صفاً؛ استعلام `--phase PH-01` أعاد 99 صفاً، و`--phase PH-02 --location SYS-ACCORE` أعاد 30، و`--container CNT-ACC-CATALOG` أعاد 20.
- `--check --strict-ready`: فشل على 842 مخالفة متوقعة لبوابات الجاهزية المفتوحة؛ لا توجد صفوف `ACCEPTED` ولا يُعد ذلك نجاحاً أو فشلاً في التحقق البنيوي.
- الاختبارات: 9/9 في `acc-architecture/execution-phases/tests` و65/65 في `architecture-assistant/tests` نجحت.
- Validators المعمارية البديلة: `validate_architecture.py` exit 0 (4 مستويات بنيوية فقط، دون اعتماد دلالي/أمني/schema/renderer)؛ `validate_artifact_depth.py` exit 0 (88 reviewed، 0 incomplete، 0 findings، والحالة تتطلب مراجعة بشرية)؛ `validate_consistency_artifacts.py` exit 0 (65/65، 0 findings، مع بقاء المراجعة الدلالية مطلوبة).
- `validate_traceability.py` و`validate_references.py`: exit 0. `validate_diagrams.py`: PASS لـ55 كتلة Mermaid؛ صحة C4 الدلالية وموافقة المالك غير متحققتين. `validate_release_status.py`: متسق، Gate7 وmanifest كلاهما `IN_PROGRESS` و0 findings ضمن نطاق التدقيق المحدود.
- `generate_coverage_report.py`: exit 0؛ C1 15/7/8، C2 40/17/23، C3 35/35/0، DECISION 22/22/0 (in-scope / decomposition-complete / exceptions-not-complete). التقرير يصف حالات registry/decomposition فقط وليس الاكتمال الدلالي.
- `/home/ubuntu/work/acc-architecture-handoff/run-remaining-validations.sh` و`/home/ubuntu/work/acc-architecture-handoff/audit-remaining-registries-links.py` غير موجودين؛ لم يُدّع تشغيلهما، واستُخدمت بدائل `architecture-assistant/scripts/` المتاحة.
- `git -c core.whitespace=cr-at-eol diff --check`: نجح؛ عوملت CRLF الأصلي في CSV كجزء من نهاية السطر دون إعادة تنسيق الملف.

### البوابات التي بقيت مفتوحة والخطوة التالية

تظل `RGAP-PH01-005` و`RGAP-PH01-004` و`UNKN-002` و`ODEC-010` وغيرها مفتوحة. لا توجد صفوف `ACCEPTED`، ولا تُعد الحزمة جاهزة للتنفيذ. الدورة التالية تعالج findings الحية وفق الأدلة والقرارات المتاحة فقط.


## Cycle 3: ARH-2026-11-21-C3

**Base commit:** `254d43bb239dcf2849e01818855751133e8154f0` (`origin/main` بعد fetch عند بدء الدورة الثالثة).<br>
**Implementation commit:** سيُسجل بعد إنشاء commit التغيير.<br>
**Push target:** `origin/main` وفق التفويض الصريح السابق؛ بلا force push.

### التغييرات ضمن النطاق

- `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-IDENTITY-AND-TRUST.md`: فُكك `SREQ-PH01-AUTH-001` إلى AUTH-007 (التحقق من بيانات الاعتماد) وAUTH-008 (إصدار الرموز وclaims). احتُفظ بالصف الأصلي ومعياريه بحالة `RETIRED` مع ملاحظة الحفظ، وبقيت بوابات ADR-022/IC-002 وفجوة `RGAP-PH01-005` مفتوحة.
- `acc-architecture/execution-phases/phase-01-platform-foundation/REQ-PH01-LICENSE-LIFECYCLE.md`: فُكك `SREQ-PH01-LIC-001` إلى LIC-007 (رفض طلب غير مؤهل دون إنشاء سجل ترخيص) وLIC-008 (إنشاء سجل ترخيص مؤسسي بحالة `ISSUED`). حُفظ الصف الأصلي ومعياراه بحالة `RETIRED`، وظلت `UNKN-003` و`ODEC-011` و`ADR-017-GATE` وRGAP قائمة دون حسم.
- `acc-architecture/execution-phases/requirements-registry.csv`: أُضيفت 4 SREQ جديدة بمعايير AC فريدة ومراجع تحقق مخططة، ورُبطت بالمتطلبات والفجوات والقرارات القائمة؛ لم يُحذف أي صف أو capability أو state أو flow أو alternative.
- `acc-architecture/validation/atomicity-review-report.md`, `requirements-coverage-matrix.md`, `requirements-readiness-report.md`: عُدلت التصنيفات والمجاميع والتغطية والجاهزية لهذه الدورة، مع إبقاء DOP-004 مرشح دمج وDEN-003 محجوباً بقرار `ODEC-010`.
- `acc-architecture/validation/requirements-change-report.md`: هذا سجل الدورة الثالثة؛ ستضاف نتيجة الدفع بعد إتمامه.

### الأعداد القابلة لإعادة الحساب

- إجمالي السجل 260 → 264 صفاً: 45 متطلباً رئيسياً ثابتة، و215 → 219 SREQ. PH-01 صار 15 REQ و88 SREQ. الحالات الحالية: 211 `DRAFT` و50 `OWNER_REVIEW` و3 `RETIRED` و0 `ACCEPTED`.
- صُنفت 219/219 SREQ في سجل الذرية التفصيلي بلا صفوف ناقصة أو معرفات مكررة: `ATOMIC` 43، `SPLIT_REQUIRED` 18 (3 مصادر تاريخية متقاعدة بعد إتمام تفكيكها و15 finding حيّة)، `MERGE_CANDIDATE` 1، `ARCHITECTURAL_CONSTRAINT` 32، `POLICY_RULE` 33، `ACCEPTANCE_CRITERION_ONLY` 3، `NEEDS_USE_CASE` 42، `DUPLICATE` 0، `OUT_OF_PHASE` 0، `BLOCKED_BY_OWNER_DECISION` 47. جرى التحقق آلياً من وجود جميع SREQ الـ219 في جدول التقرير دون نقص أو تكرار.
- TBD في `use_case_id`: 174 → 178 (PH-01: 96؛ PH-02: 12؛ PH-03: 35؛ PH-04: 35). صفوف السجل ذات القرارات المفتوحة: 193 → 197؛ عدد المعرفات الفريدة 60. لم تُغلق فجوة Use Case.
- C4 bindings المفقودة حسب المدقق البنيوي: 0 → 0. الممثلون و6 مواقع C1 و29 حاوية C2 مرجعية سليمة بحسب المدقق؛ ذلك لا يثبت ملاءمة الإسناد الدلالية للعملية.
- SREQ ذات AC ومراجع تحقق مخططة: 219/219؛ معرّفات AC الفريدة في السجل 255. جميع نتائج التحقق الوظيفي ما زالت غير منفذة.
- أعاد الاستعلام `--phase PH-01` عدد 103 صفوف، و`--phase PH-02 --location SYS-ACCORE` عدد 30، و`--container CNT-ACC-CATALOG` عدد 20.

### نتائج التحقق

- `validate_requirements.py --check` و`--check --require-rows`: PASS على 264 صفاً. الاستعلامات الثلاثة خرجت برمز 0 وأعادت 103/30/20. اختبارات `acc-architecture/execution-phases/tests`: 9/9 ناجحة.
- `--check --strict-ready`: FAIL متوقع بعدد 858 مخالفة؛ ما زالت صفوف Draft/Owner Review وTBD والقرارات المفتوحة والتحقق المخطط تمنع الجاهزية. لا يعد ذلك PASS ولا خطأ بنيوياً؛ لا توجد صفوف `ACCEPTED`.
- اختبارات `architecture-assistant/tests`: 65/65 ناجحة. مدققات `validate_architecture.py`, `validate_artifact_depth.py`, `validate_consistency_artifacts.py`, `validate_traceability.py`, `validate_references.py`, `validate_diagrams.py`, `validate_release_status.py` وتقرير `generate_coverage_report.py` خرجت جميعها برمز 0 بعد تمرير مجلد `acc-architecture` كوسيط. العمق: 88 reviewed و0 incomplete/findings مع اشتراط مراجعة بشرية؛ الاتساق: 65/65 مع اشتراط مراجعة دلالية؛ المخططات: 55 Mermaid؛ حالة الإصدار `IN_PROGRESS`؛ تقرير التغطية يصف حالات registry/decomposition فقط.
- أعيد التحقق من غياب `/home/ubuntu/work/acc-architecture-handoff/run-remaining-validations.sh` و`/home/ubuntu/work/acc-architecture-handoff/audit-remaining-registries-links.py`؛ المجلد غير موجود، لذلك لم يُدّع تشغيلهما. استُخدمت بدائل architecture-assistant المتاحة أعلاه.
- `git diff --name-only` أظهر الملفات السبعة أعلاه فقط وكلها تحت `acc-architecture/`. الأمر الخام `git diff --check` يعتبر CR في أسطر CSV ذات CRLF مسافات زائدة؛ بعد اعتماد CRLF كنهاية السطر (`git -c core.whitespace=cr-at-eol diff --check`) ينجح الفحص. لم تُحوّل نهايات CSV الأصلية.

### إعادة تقييم البوابات والخطوة التالية

أُعيد تقييم 17 finding تفكيك حية من الدورة السابقة؛ اكتمل تفكيك AUTH-001 وLIC-001، وبقيت 15 حالة `SPLIT_REQUIRED` حيّة. لم يُنفذ merge: DOP-004 ما زال `MERGE_CANDIDATE` لأن تداخل المؤشرات الجزئي مع DEX-001 لا يثبت التكافؤ مع المقاييس التشغيلية أو DOP-003؛ وظل DEN-003 غير مثبت التكرار ومحجوباً بـ`ODEC-010`. لا تزال فجوات Use Case وقرارات أصحاب المصلحة والسياسات دون حسم، ولا تثبت validators دلالية المتطلبات أو التنفيذ أو الأمن أو قبول المالك. الدورة التالية تراجع findings الـ15 المتبقية بالأدلة نفسها، مع إبقاء كل بوابة مالك مفتوحة إلى حين قرار موثق.
