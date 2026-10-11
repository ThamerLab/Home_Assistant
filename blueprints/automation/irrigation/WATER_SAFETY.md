# 🚨 Long-running Water Safety Watchdog — Detailed Guide

<p align="center">
  <img src="../../../assets/water-safety.svg" alt="Long-running Water Safety Watchdog" width="100%">
</p>

هذا الـBlueprint طبقة أمان مستقلة للصمامات أو مصادر الماء التي تظهر كـ `switch`. لا يشغّل الماء من نفسه؛ فقط يراقب التشغيل الطويل ويتدخل بعد موافقة المستخدم.

## الهدف

إذا بقي أي Switch مختار في حالة `on` أطول من الحد:

- يرسل تنبيهًا Critical.
- يعرض **Stop all** و **Keep running**.
- إذا اخترت Stop، يطفئ الجميع ويتحقق من حالة `off`.
- إذا اخترت Keep، يعمل Snooze مؤقتًا ثم يسمح للمراقبة بالعودة.
- إذا أُطفئت الصمامات يدويًا أثناء ظهور التنبيه، يغلق التنبيه.

## المدخلات

| Input | الافتراضي | الوظيفة |
|---|---:|---|
| Water / Irrigation Switches | — | Switch واحد أو أكثر للمراقبة |
| Alert After | 10 دقائق | المدة التي تعتبر تشغيلًا طويلًا |
| Snooze After Keep | 30 دقيقة | فترة منع إعادة التنبيه بعد Keep |
| Notification Tag | long_running_water | يسمح بفصل إشعارات أكثر من نسخة |
| Device to Notify | — | جهاز Companion App الذي يستقبل التنبيه |

## التنفيذ خطوة بخطوة

### 1. Triggers الأساسية

هناك ثلاث طرق للدخول:

1. صمام ينتقل إلى ON ويبقى كذلك مدة **Alert After**.
2. Watchdog كل 5 دقائق.
3. Home Assistant Startup.

الـTrigger الدوري وStartup موجودان كطبقة احتياطية لأن `for:` لا يحتفظ بمؤقته عبر Restart/Reload.

### 2. التحقق من التشغيل الطويل

في Trigger الصمام المباشر، الشرط يعتبر المدة قد تحققت.

في Watchdog/Startup:

- يقرأ كل Switch.
- يفحص `last_changed`.
- يقارن عمر حالة ON بالحد المطلوب.
- لا يكمل إذا لم يجد صمامًا تجاوز المدة.

### 3. إنشاء Action IDs فريدة

عند كل تشغيل ينشئ:

- `WATER_STOP_<context.id>`
- `WATER_KEEP_<context.id>`

السبب: زر من Notification قديم لا يُفترض أن يتحكم في تشغيل أحدث.

### 4. إرسال Critical Notification

الرسالة تعرض أسماء الصمامات التي ما زالت ON والمدة التقريبية لكل واحد.

تحتوي على:

- 🛑 **Stop all**
- 💧 **Keep running**

وتضع Notification Tag ثابتًا تختاره أنت بحيث يستبدل التنبيه الجديد القديم لنفس النسخة.

### 5. انتظار قرار المستخدم

ينتظر حتى 5 دقائق لأي واحد من:

- Stop.
- Keep.
- جميع الصمامات أصبحت OFF من نفسها/يدويًا.

### 6. عند Stop all

- يرسل `switch.turn_off` لجميع الصمامات.
- ينتظر حتى 15 ثانية.
- النجاح لا يعتمد على اكتمال Service Call فقط؛ يجب أن تكون جميع الحالات `off`.
- عند النجاح يرسل Confirmation.
- إذا لم يؤكد Home Assistant الإيقاف، يرسل Critical failure جديد.

### 7. عند Keep running

- يمسح التنبيه القديم.
- يرسل رسالة تؤكد أن التشغيل سيستمر.
- ينتظر مدة Snooze.

خلال هذه الفترة الأوتوميشن في `mode: single`، لذلك لا ينشئ تنبيهات مكررة.

بعد انتهاء الـSnooze، يصبح الأوتوميشن حرًا؛ الـWatchdog الدوري يستطيع إعادة التنبيه إذا استمر الماء.

### 8. إذا أطفأت الماء يدويًا

Trigger داخلي يراقب أن جميع الصمامات أصبحت `off`، ثم يمسح التنبيه دون إرسال أمر إضافي.

### 9. إذا تجاهلت التنبيه

بعد خمس دقائق ينتهي انتظار الأزرار، **لكن التنبيه لا يُمسح تلقائيًا**. يبقى ظاهرًا، وبعد عودة الـWatchdog يمكن أن يحل تنبيه حديث بنفس الـTag محله.

## Restart / Reload

Home Assistant لا يحفظ زمن `for:` عبر Restart. الـWatchdog وStartup يقللان المشكلة، لكن هناك حد مهم:

إذا أعيد إنشاء حالة الكيان بعد Restart فإن `last_changed` قد يبدأ من وقت جديد، وبالتالي لا يمكن ضمان معرفة مدة التشغيل قبل إعادة التشغيل.

لهذا، للصمامات الحساسة استخدم أيضًا:

- Hardware Auto-Close إن توفر.
- Flow Sensor مستقل.
- حد تشغيل داخلي في جهاز الصمام إن كان يدعم ذلك.

## Critical Notification

الـBlueprint يرسل Payload الخاص بـCritical على iOS. ظهور التنبيه كـCritical يعتمد أيضًا على صلاحيات Companion App ونظام التشغيل.

## ما الذي يتم التحقق منه؟

**يتم التحقق:** أن Home Assistant يرى جميع الـSwitches المختارة `off`.

**لا يمكن لهذا الـBlueprint وحده إثبات:** أن الماء توقف فعليًا خلف الصمام. التأكد الفيزيائي يحتاج Flow Sensor أو Feedback مستقل.

## اختبار آمن

1. استخدم Switch تجريبي أو صمام تحت المراقبة.
2. ضع Alert After على 5 دقائق.
3. انتظر التنبيه.
4. جرّب Keep.
5. أعد الاختبار واضغط Stop.
6. تحقق يدويًا أن الماء توقف.
7. افصل جهازًا/اجعله غير متاح في اختبار مراقب للتأكد أن Failure Alert يظهر.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/irrigation/long_running_water_safety.yaml
```

[![Import Water Safety Watchdog](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Flong_running_water_safety.yaml)
