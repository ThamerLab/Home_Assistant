# 💡 Outdoor Light — Abnormal State Alert

<p align="center">
  <img src="../../../assets/outdoor-alert.svg" alt="Outdoor Light Abnormal State Alert" width="100%">
</p>

هذا الـBlueprint لا يفرض حالة اللمبة باستمرار. دوره مراقبة التناقض بين **حالة الإنارة** و**ارتفاع الشمس** وإعطاؤك قرار Fix أو Keep.

## الحالات التي تعتبر غير طبيعية

مع Threshold افتراضي = 5°:

- الشمس أقل من 5° + اللمبة `off`.
- الشمس أعلى من 5° + اللمبة `on`.

يجب أن يستمر التناقض كامل مدة **Mismatch Duration** قبل إرسال التنبيه.

## المدخلات

| Input | الافتراضي | الوظيفة |
|---|---:|---|
| Outdoor Light | — | اللمبة التي تراقبها |
| Sun Elevation Threshold | 5° | حد الليل/النهار |
| Mismatch Duration | 30 دقيقة | مدة استمرار الحالة قبل التنبيه |
| Notification Tag | outside_light_attention | لمنع تكدس تنبيهات نفس النسخة |
| Device to Notify | — | جهاز Companion App |

## التنفيذ خطوة بخطوة

### 1. Template Trigger

يتحول Template من False إلى True عندما تظهر إحدى الحالتين غير الطبيعية.

ثم يجب أن يبقى True مدة Mismatch Duration.

### 2. تحديد نوع المشكلة

بعد الـTrigger يحدد:

- `night_off`
- أو `day_on`
- أو `resolved` إذا اختفت المشكلة قبل تنفيذ الخطوات.

### 3. إنشاء أزرار فريدة

ينشئ Action IDs باستخدام `context.id`:

- Fix
- Keep

هذا يمنع Notification قديم من إرسال Action ID ثابت إلى تشغيل أحدث.

### 4. إرسال Actionable Notification

لو Night + Off:

- **Turn it on**
- **Keep it off**

لو Day + On:

- **Turn it off**
- **Keep it on**

### 5. الانتظار

ينتظر حتى 6 ساعات لأي من:

- Fix.
- Keep.
- اختفاء الحالة غير الطبيعية من نفسها.

### 6. إذا ضغطت Fix

قبل التحكم في اللمبة يعيد التحقق من **الحالة الحالية** ومن Elevation الحالية.

مثال:

إذا وصلك تنبيه Night + Off ثم ضغطت Fix بعد وقت طويل، لن يشغل اللمبة إلا إذا ما زالت الشمس تحت الحد واللمبة ما زالت Off.

### 7. إذا ضغطت Keep

لا يغير اللمبة. يمسح Notification فقط.

وبما أن Template Trigger يحتاج انتقال False→True جديد، لن يعيد الإزعاج باستمرار لنفس الحالة المستمرة.

### 8. إذا انحلت المشكلة وحدها

يمسح التنبيه ولا يغير شيئًا.

## Restart / Reload

مثل أي Trigger يستخدم `for:` في Home Assistant، المؤقت الجاري لا يستمر عبر Restart أو Reload. إذا بقيت الحالة غير الطبيعية، يبدأ احتساب المدة من جديد بعد استعادة الحالة والتتبع.

## لماذا هو منفصل عن Dusk-to-Dawn؟

الفصل مهم:

- Dusk-to-Dawn = تنفيذ الجدول.
- Abnormal State Alert = مراقبة الاستثناء واحترام قرارك اليدوي.

بهذا ما يصير Watchdog يعكس قرارًا يدويًا بدون إذنك.

## اختبار آمن

1. أنشئ نسخة على Light تجريبية.
2. ضع Mismatch Duration على 5 دقائق.
3. اجعل الحالة مخالفة للوقت الحالي.
4. تأكد من وصول التنبيه.
5. اختبر Keep: لا يجب أن تتغير اللمبة.
6. اختبر Fix: يجب أن يطبق الحالة المتوقعة فقط إذا ما زال الظرف الحالي مطابقًا.
7. غيّر حالة اللمبة يدويًا أثناء ظهور التنبيه وتأكد أنه يُغلق بدون تغيير إضافي.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/lighting/outside_light_attention.yaml
```

[![Import Outdoor Light Alert](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_light_attention.yaml)
