# ✅ Validation

## Status

**MERGE GATE ACTIVE**

لا يتم دمج أي تغيير في الـBlueprints إلى `main` إلا إذا نجح **آخر Commit في الـPR** في الاختبارين الآتيين:

1. **Repository policy & static validation**
2. **Home Assistant 2026.9.4 config check**

Workflow:
`.github/workflows/validate-blueprints.yml`

الـCI يعاد تلقائيًا عند أي تعديل على Blueprints أو Docs أو Assets أو Tests، لذلك النجاح في Commit قديم لا يكفي لدمج Commit أحدث.

## 1. Static repository validation

الملف:
`tests/validate_repo.py`

يفحص تلقائيًا:

- كل Blueprint YAML يمكن Parse له مع دعم `!input`.
- عدد الـBlueprints الفعلي يطابق Validation map.
- `blueprint.name` موجود.
- `blueprint.domain` صحيح: automation أو script.
- `description` موجود.
- `author` موجود.
- `source_url` يشير إلى نفس الملف داخل هذا المستودع.
- `homeassistant.min_version` موجود بصيغة `X.Y.Z`.
- كل `!input` مستخدم معرف داخل `blueprint.input`.
- لا يوجد `wait_template` أو `wait_for_trigger` بدون Timeout.
- Blueprints المياه والإنارة لا تستخدم `mode: restart`.
- Template Trigger لا يستخدم Variable متاح فقط وقت Actions؛ أي قيمة مطلوبة عند إنشاء الـTrigger يجب أن تأتي عبر `trigger_variables`.
- كل Blueprint له **صورة مخصصة وفريدة**.
- كل صورة SVG قابلة للـXML parsing.
- كل Blueprint له **شرح مخصص**.
- الشرح يذكر ملف الـBlueprint نفسه.
- الشرح يضم الصورة المخصصة.
- الشرح يحتوي قسمًا خطوة بخطوة وبحد أدنى كافٍ من التفاصيل.
- كل Blueprint مذكور في Root README.
- كل Blueprint مذكور في Blueprint Catalog.
- الروابط والصور المحلية داخل ملفات Markdown تشير إلى ملفات موجودة فعليًا.
- لا توجد أنماط البيانات المنزلية الخاصة المعروفة داخل ملفات النص العامة، مثل LAN IPs أو أسماء كيانات المنزل الخاصة أو عناوين العمل الخاصة.
- لا يوجد `hacs.json` مضلل؛ هذا المستودع Blueprint collection وليس HACS repository type.

## 2. Home Assistant configuration validation

CI ينشئ Config اختبار في:

`tests/ha_config/`

ثم ينسخ كل Blueprints تحت المسارات التي يتوقعها Home Assistant ويُنشئ Instances تجريبية لكل Blueprint.

التغطية تشمل:

- Smart Irrigation — Sun mode.
- Smart Irrigation — Custom time.
- Smart Irrigation — Fixed interval.
- Long-running Water Safety.
- Outdoor Dusk to Dawn.
- Outdoor Abnormal State Alert.
- Zone Exit Notification.
- Quran Sunrise & Sunset.
- Available Updates.
- Quran Safe Toggle Script.
- Manual Irrigation Script.

بعدها يشغل Home Assistant Core **2026.9.4** نفسه:

```text
python -m homeassistant --script check_config -c /config
```

داخل:

```text
ghcr.io/home-assistant/home-assistant:2026.9.4
```

هذا يفحص تحميل الـBlueprints وتوسيع Inputs وبناء الأوتوميشنات والسكريبتات في Config حقيقي لـHome Assistant.

## 3. Manual logic audit

الـCI لا يفهم نية الأوتوميشن وحده، لذلك تمت مراجعة المنطق يدويًا أيضًا من ناحية:

- Trigger semantics.
- Trigger-time variables مقابل action-time variables.
- Conditions.
- Actions.
- Waits وTimeouts.
- Failure paths.
- Retry behavior.
- Restart/Reload behavior.
- Automation mode.
- منع Runs المتداخلة.
- عدم اعتبار Service Call نجاحًا قبل State verification عندما تكون الحالة حساسة.
- خطر ترك صمام ماء ON.
- عدم إجبار اللمبة الخارجية على عكس قرار يدوي بعد Restart.
- عدم اعتبار أي `playing` دليلًا أن نفس Quran URI هو الذي يعمل.
- عدم الاعتماد على اسم Update لتحديد الأولوية.

## 4. Documentation gate

السياسة الآن:

> **لا Blueprint بدون صورة مخصصة + شرح مخصص + خطوات تنفيذ + حدود + طريقة اختبار + Import URL.**

إذا أضيف Blueprint جديد إلى `blueprints/**/*.yaml` بدون إدخاله في Validation map أو بدون صورة/شرح، يفشل الـCI.

## ماذا يعني PASS؟

PASS يعني أن نسخة الـRepository المختبرة:

- سليمة YAML/XML.
- مطابقة لقواعد Blueprint الداخلية للمشروع.
- قابلة للتحميل والتوسيع داخل Home Assistant 2026.9.4 Config test.
- لا تحتوي الأخطاء البنيوية التي تغطيها الاختبارات.
- جميع Blueprints المشمولة لها Docs وصور سليمة وروابط محلية غير مكسورة.

## ماذا لا يعني PASS؟

**لا يوجد اختبار GitHub يستطيع ضمان استجابة الأجهزة المادية بنسبة 100%.**

أمثلة لا يستطيع CI إثباتها:

- هل صمام المياه أغلق ميكانيكيًا فعلًا رغم أن State أصبحت OFF.
- هل Zigbee mesh وصل الأمر للجهاز في كل مرة.
- هل Wi-Fi انقطع لحظة التشغيل.
- هل AirPlay/Chromecast/Music Assistant player خرج منه صوت فعلي.
- هل GPS حدّث موقع Person في الوقت المتوقع.
- هل Firmware لجهاز معين يتصرف بطريقة مختلفة.

لهذا كل Blueprint حساس يحتوي **Live Test Checklist** قبل الاعتماد الفعلي.

## قاعدة الدمج

الترتيب الصحيح دائمًا:

```text
Edit
→ Static validation
→ Home Assistant check_config
→ Review diff
→ Latest commit must be green
→ Merge
```

لا يتم تجاوز هذه القاعدة لمجرد أن إصدارًا سابقًا من نفس PR كان ناجحًا.
