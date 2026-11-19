# مراجعة مقارنة لمشاريع GitHub وتحسين مساعد التوثيق المعماري

تاريخ المراجعة: 15 نوفمبر 2026. هذه مقارنة لممارسات موثقة في عشرة مستودعات عامة بارزة، وليست ترتيباً موضوعياً لـ«أفضل مساعد في العالم». معظم المشاريع المقارنة وكلاء برمجة أو أطر تنسيق، لا مساعدات متخصصة في توثيق C4؛ لذلك نُقلت المبادئ القابلة للتكييف فقط، ولم تُعامل أرقام GitHub كدليل على صحة المعمارية.

## ما أظهرته المقارنة

تكررت في المشاريع الأقوى ممارسات فصل التخطيط عن التنفيذ أو المراجعة، وتسجيل آثار العمل، وتشغيل اختبارات حتمية، وعدم إعلان النجاح إلا بعد قراءة الدليل الفعلي. تظهر هذه المبادئ بصيغ مختلفة في [Cline وخيارات Plan/Act ونقاط الاستئناف] [1] [12] [13]، و[OpenHands ومصفوفة الاختبار وحدود مسؤوليات المنتج] [2] [14] [15]، و[Aider وخرائط السياق واختبارات lint/test] [3] [16] [17]، و[GitHub Spec Kit ومسار التوضيح والتحليل والتقارب] [4] [18] [19]، و[Superpowers واختبار التعليمات والتحقق قبل ادعاء الإنجاز] [5] [20] [21].

توضح مقارنة الأمثلة أن الحزمة المرفقة قوية أصلاً في مجالها: لديها سياسات C4 واختيار مستوى المخطط، سجلات ذات معرّفات ثابتة، تتبع وقيود على اعتماد الاستثناءات، مراحل قابلة للاستئناف، اختبارات للمدققات، وفصل بين التحقق الهيكلي والدلالي والبصري. لذلك كان التحسين الأهم ليس إضافة مزيد من قواعد الرسم، بل جعل تقارير الإطلاق نفسها قابلة للتحقق ومنع تناقضها.

## لقطة الانتشار وحالة الصيانة

الأعداد التالية لقطات GitHub مرصودة في 15 نوفمبر 2026؛ قد تتغير، ولا تقيس جودة المخرجات أو الاستخدام الفعلي بمفردها. ظهر في واجهة GitHub API نحو 93,523 نجمة لـOpenHands، و71,657 لـCline، و61,838 لـMicrosoft AutoGen، و56,657 لـGoose، و50,070 لـAider، و36,464 لـContinue، و24,238 لـRoo Code، و20,811 لـSWE-agent، و317,985 لـSuperpowers. لم أتحقق من رقم لحظي موثوق لـGitHub Spec Kit؛ صفحته الوثائقية تعرض رقماً مجتمعياً أعلى من 130 ألف نجمة في تحديث أقدم، ولذلك لم أقدمه كعداد حالي مستقل. مصادر الأرقام: واجهات GitHub API للمستودعات [22] [23] [24] [25] [26] [27] [28] [29] [30] [31].

عدد النجوم لا يعني أن المشروع يُصان أو أنه الأفضل لهذه المهمة. فـSWE-agent يوجّه المستخدمين الجدد إلى mini-swe-agent، وRoo Code مؤرشف، وMicrosoft AutoGen يعلن توقف الدعم والتوصية بالانتقال إلى Microsoft Agent Framework. كما ظهر تعارض بين وصف Continue للصيانة وبيانات التحديث/الإصدارات؛ لذا لا أعتبره نشطاً أو متوقفاً دون مراجعة أحدث. أما Goose فقد انتقل إلى Agentic AI Foundation، وهو نشط بحسب بيانات التحديث التي راجعتها، لكن أحدث إصدار ظاهر أقدم من آخر دفعة للمستودع. هذه الفروق موثقة في صفحات [SWE-agent] [6] [32] و[Roo Code] [7] [33] و[AutoGen] [8] [34] و[Continue] [9] [35] و[Goose] [10] [36].

## الفجوة الحقيقية التي اكتُشفت في الحزمة

في عينة ACC Ecosystem داخل الأرشيف، كان ملف `validation/validation-status.md` يعلن أن Gate 7 اجتازت، بينما سجل التتبع نفسه يذكر أن Gate 7 معلنة PASSED رغم وجود موانع تحقق، وأن حالة مرحلة التحقق في manifest ما زالت IN_PROGRESS. كذلك يضع تقرير العمق جميع الوثائق الـ65 التي راجعها في `INCOMPLETE_OUTLINE`، ويعلن فحص الاتساق أن الحالة `BLOCKED` وأن عدد المعرّفات الممثلة في مصفوفة المخططات هو 0 من أصل 78؛ كما كانت ملفات سجل الاتساق ومصفوفة تغطية المخططات وتقرير المراجعة النهائي مفقودة.

إضافة إلى ذلك، أظهر المدقق الهيكلي 18 حالة استثناء لا يحق للمساعد اعتمادها بنفسه. لم أُخفِ هذه النتائج ولم أُنشئ موافقات أو سجلات شكلية لسدها. صححت فقط حالة Gate 7 في التقرير والـmanifest إلى `BLOCKED`، واحتفظت بالنواقص كي تبقى واضحة للمستخدم التالي. هذه الحالة المحددة تعني أن المثال الموجود في الحزمة **ليس إصداراً معمارياً معتمداً** حتى تُعالج الموانع.

## التحسينات المطبقة

أضفت `scripts/validate_release_status.py` ليفحص اتساق Gate 7 مع manifest، ويرفض نجاح الإطلاق إذا بقيت موانع BLOCKER/MAJOR أو تقارير عمق/اتساق محجوبة أو ملفات الإطلاق الأساسية ناقصة. الفحص يميز بوضوح بين «حالات التقارير متسقة» وبين «المعمارية اجتازت»؛ لذلك قد تكون نتيجة المدقق `CONSISTENT` بينما يظل Gate 7 `BLOCKED`، وهذا ما حدث في المثال. الأداة لا تدعي الحكم على صحة النطاق أو الرسم.

أضفت ستة اختبارات سلبية/إيجابية لرفض PASS الزائف، واختلاف manifest عن Gate 7، ونقص سجل أو مصفوفة، مع قبول حالة BLOCKED المتسقة. كما حدّثت عقد التشغيل والجودة والـworkflow وprompt المراجعة النهائية وREADME لفرض تشغيل المدقق بعد تحديث التقارير. أضيفت نقطة خطة تغيير موجزة تربط الملفات والمعرفات والمصادر والمخاطر والفحوص، وسجل checkpoint أكثر قابلية للاستئناف.

وأبقيت تحسين المخططات من المراجعة السابقة ضمن الحزمة: إنشاء/تحديث مخطط فعلي في كل مرحلة، وتسليم ملفات الرسم النهائية مع فهرس وتقسيمات عند التوسع، من دون إجبار المساعد على إنتاج C3/C4 غير لازمة. المبدأ متوافق مع C4 الرسمي: C1 وC2 خط أساس موصى به، والمكونات والكود تُستخدم حين تضيف قيمة [11].

## نتائج التحقق بعد التعديل

نجحت مجموعة اختبارات الحزمة: **57 اختباراً**. وعلى عينة ACC Ecosystem، أعاد `validate_architecture.py` الحالة `BLOCKED` بسبب 18 استثناء غير مخوّل؛ وأعاد `validate_artifact_depth.py` الحالة `BLOCKED_FOR_CONTENT_REVIEW` مع 65 من 65 وثيقة ذات مخطط محتوى غير مكتمل؛ وأعاد `validate_consistency_artifacts.py` الحالة `BLOCKED` مع 81 نتيجة و0/78 معرفاً في مصفوفة التغطية. أخيراً، أعاد مدقق اتساق الحالات `CONSISTENT` لأن Gate 7 والـmanifest كلاهما `BLOCKED`، لكنه سجّل 99 ملاحظة مفتوحة؛ **هذا لا يعني أن الإصدار اجتاز**. لم تُجرَ مراجعة دلالية أو مراجعة بصرية نهائية للمخططات، وتبقى غير متحققة.

## الأولويات التالية

الخطوة التالية لتحسين الحزمة هي معالجة سجل التتبع والاستثناءات بموافقة أصحاب الصلاحية، ثم إنشاء سجل الاتساق ومصفوفة تغطية فعلية تربط كل معرف بمخططه أو بتصرف موثق، واستكمال محتوى الوثائق الذي كشف عنه فحص العمق. بعدها تُعاد المدققات والمراجعة الدلالية والبصرية. لا أوصي بتغيير حالة Gate 7 إلى PASSED قبل ظهور أدلة هذه الأعمال في الملفات.

## المراجع

[1]: https://github.com/cline/cline "Cline repository"
[2]: https://github.com/OpenHands/OpenHands "OpenHands repository"
[3]: https://github.com/Aider-AI/aider "Aider repository"
[4]: https://github.com/github/spec-kit "GitHub Spec Kit repository"
[5]: https://github.com/obra/superpowers "Superpowers repository"
[6]: https://github.com/SWE-agent/SWE-agent "SWE-agent repository"
[7]: https://github.com/RooVetGit/Roo-Code "Roo Code repository"
[8]: https://github.com/microsoft/autogen "Microsoft AutoGen repository"
[9]: https://github.com/continuedev/continue "Continue repository"
[10]: https://github.com/block/goose "Goose repository"
[11]: https://c4model.com/diagrams "C4 model diagrams"
[12]: https://docs.cline.bot/core-workflows/plan-and-act "Cline Plan and Act"
[13]: https://docs.cline.bot/core-workflows/checkpoints "Cline checkpoints"
[14]: https://github.com/OpenHands/OpenHands/blob/main/docs/TESTING_MATRIX.md "OpenHands testing matrix"
[15]: https://github.com/OpenHands/OpenHands/blob/main/docs/architecture.md "OpenHands architecture"
[16]: https://aider.chat/docs/repomap.html "Aider repository map"
[17]: https://aider.chat/docs/usage/lint-test.html "Aider lint and test"
[18]: https://github.github.com/spec-kit/quickstart.html "GitHub Spec Kit quickstart"
[19]: https://github.github.com/spec-kit/guides/agentic-sdlc.html "GitHub Spec Kit agentic SDLC"
[20]: https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md "Superpowers writing skills"
[21]: https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md "Superpowers verification before completion"
[22]: https://api.github.com/repos/cline/cline "Cline GitHub repository API"
[23]: https://api.github.com/repos/OpenHands/OpenHands "OpenHands GitHub repository API"
[24]: https://api.github.com/repos/microsoft/autogen "Microsoft AutoGen GitHub repository API"
[25]: https://api.github.com/repos/block/goose "Goose GitHub repository API"
[26]: https://api.github.com/repos/Aider-AI/aider "Aider GitHub repository API"
[27]: https://api.github.com/repos/continuedev/continue "Continue GitHub repository API"
[28]: https://api.github.com/repos/RooVetGit/Roo-Code "Roo Code GitHub repository API"
[29]: https://api.github.com/repos/SWE-agent/SWE-agent "SWE-agent GitHub repository API"
[30]: https://api.github.com/repos/obra/superpowers "Superpowers GitHub repository API"
[31]: https://github.com/github/spec-kit "GitHub Spec Kit repository"
[32]: https://github.com/SWE-agent/SWE-agent/blob/main/README.md "SWE-agent maintenance status"
[33]: https://github.com/RooVetGit/Roo-Code "Roo Code repository status"
[34]: https://github.com/microsoft/autogen/blob/main/README.md "Microsoft AutoGen maintenance notice"
[35]: https://github.com/continuedev/continue/blob/main/README.md "Continue maintenance statement"
[36]: https://github.com/block/goose/blob/main/README.md "Goose project status"
