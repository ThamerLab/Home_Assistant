# 🌙 Outdoor Lights — Dusk to Dawn

<p align="center">
  <img src="../../../assets/outdoor-dusk-dawn.svg" alt="Outdoor Lights Dusk to Dawn" width="100%">
</p>

Blueprint للتحكم في الإنارة الخارجية عند **عبور ارتفاع الشمس** حدًا تختاره، وليس بناءً على وقت ثابت.

## المدخلات

| Input | الافتراضي | الوظيفة |
|---|---:|---|
| Outdoor Light | — | كيان `light` المراد التحكم فيه |
| Sun Elevation Threshold | 5° | الحد الذي يفصل منطق المساء/النهار |
| Notification Devices | لا يوجد | أجهزة تتلقى خطأ عدم استجابة اللمبة |

## التنفيذ خطوة بخطوة

### المساء

1. يراقب `sun.sun` وAttribute اسمها `elevation`.
2. عندما تنزل القيمة من أعلى الحد إلى أسفله، يعمل Trigger `dusk`.
3. يرسل `light.turn_on`.
4. ينتظر حتى 10 ثوانٍ لتأكيد أن اللمبة أصبحت `on`.
5. إذا لم تتأكد:
   - ينتظر 5 ثوانٍ.
   - يعيد `light.turn_on` مرة واحدة.
   - ينتظر تأكيدًا آخر حتى 10 ثوانٍ.
6. إذا لم تتأكد بعد المحاولة الثانية:
   - ينشئ Persistent Notification.
   - يرسل Push Notification للأجهزة المختارة.

### الصباح

نفس الخطوات، لكن عند ارتفاع الشمس فوق الحد:

- `light.turn_off`
- تحقق `off`
- Retry واحد
- تنبيه إذا لم يتأكد الإطفاء.

## لماذا لا يوجد Trigger عند Home Assistant Startup؟

متعمد.

لو شغلت اللمبة يدويًا نهارًا أو طفيتها يدويًا ليلًا، لا نريد Restart لـHome Assistant أن يلغي قرارك فورًا.

الأوتوميشن يتصرف فقط عند **عبور الشمس للحد** مرة أخرى.

## ماذا يعني Manual Priority؟

- إذا الأوتوميشن شغّل اللمبة مساءً وبعدها أنت طفيتها، تبقى مطفأة.
- إذا الأوتوميشن طفاها صباحًا وبعدها أنت شغلتها، تبقى شغالة.
- لا يوجد Loop يجبرها باستمرار.

إذا أردت فقط أن تُنَبَّه عند هذا الاختلاف بدون إجبار، استخدم معه:
[Outdoor Light — Abnormal State Alert](./ABNORMAL_STATE_ALERT.md).

## حدود التصميم

- Numeric-state trigger يعمل عند عبور الحد، وليس عند مجرد وجود الشمس تحت/فوق الحد بعد Reload.
- الاعتماد على `sun.sun` يفترض أن Location/Timezone في Home Assistant صحيحة.
- حالة `on/off` تؤكد ما يبلغه التكامل، وليس بالضرورة قياس الضوء فعليًا.

## اختبار آمن

1. استخدم نسخة تجريبية وحدًا قريبًا من Elevation الحالية أو Light تجريبية.
2. راقب Trace عند عبور الحد.
3. تحقق من First Attempt.
4. جرّب جهازًا غير مستجيب في بيئة آمنة للتأكد من Retry + Failure Notification.
5. بعد نجاح الاختبار اختر اللمبة الخارجية الفعلية.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/lighting/outside_lights_dusk_dawn.yaml
```

[![Import Dusk to Dawn](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_lights_dusk_dawn.yaml)
