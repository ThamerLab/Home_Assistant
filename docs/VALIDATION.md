# Validation

## Status

**PENDING on audit branch**

لا يتم دمج تغييرات الـBlueprints إلى `main` حتى تمر الاختبارات الآتية.

## ما الذي نختبره؟

### 1. Static repository validation

- كل YAML يمكن Parse له.
- كل ملف Blueprint يحتوي `name` و`domain`.
- كل Blueprint من ThamerLab يحتوي `author` و`source_url` و`homeassistant.min_version`.
- كل `!input` مستخدم معرف داخل `blueprint.input`.
- لا يوجد Wait بلا Timeout.
- كل Blueprint موجود في Catalog.
- لكل Blueprint **صورة مخصصة**.
- لكل Blueprint **شرح تفصيلي مخصص**.
- كل SVG صالح كـXML.
- لا توجد Entity IDs/IPs/Device IDs الخاصة بالمنزل داخل الـBlueprints العامة.

### 2. Home Assistant configuration validation

CI يبني Config اختبار، يستورد كل Blueprint مع Inputs تجريبية، ثم يشغل:

```text
python -m homeassistant --script check_config -c /config
```

داخل صورة Home Assistant المطابقة للإصدار المستهدف.

### 3. Logic audit

كل Blueprint تتم مراجعته يدويًا من ناحية:

- Trigger.
- Conditions.
- Actions.
- Wait/Timeout.
- Failure path.
- Restart behavior.
- Mode.
- منع Runs المتداخلة.
- عدم ادعاء نجاح جهاز قبل التحقق من State.

## ماذا يعني PASS؟

PASS يثبت أن ملفات الـBlueprint قابلة للتحميل والتوسيع داخل Home Assistant وأن Schema/Configuration سليمة في بيئة الاختبار.

## ماذا لا يمكن لـCI إثباته؟

لا يمكن لأي اختبار Repository أن يضمن 100% أن جهازًا ماديًا سيستجيب دائمًا، لأن ذلك يعتمد على:

- الشبكة.
- Zigbee/Wi-Fi.
- Integration/API.
- Firmware.
- State reporting.
- الكهرباء والماء والصمام نفسه.

لذلك توجد خطوات Live Test واضحة في توثيق كل Blueprint، خصوصًا الماء والإنارة والصوت.
