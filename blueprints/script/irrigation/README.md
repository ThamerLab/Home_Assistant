# 💧 Manual Irrigation — Safe Timed Run

<p align="center">
  <img src="../../../assets/manual-irrigation.svg" alt="Safe Manual Irrigation Script" width="100%">
</p>

Script Blueprint لتشغيل السقاية يدويًا لمدة تختارها **عند كل تشغيل للسكريبت**، مع نفس فلسفة الأمان الأساسية: تحقق ON، فحص Flow اختياري، اكتشاف الإيقاف المبكر، ثم تحقق OFF.

## الفرق عن Smart Irrigation

- Smart Irrigation يبدأ بجدول.
- Manual Irrigation يبدأ عندما أنت تشغل السكربت.
- حقل **مدة التشغيل** يظهر عند تشغيل السكربت من Home Assistant.

## المدخلات عند إنشاء السكربت

| Input | الوظيفة |
|---|---|
| Irrigation Valves | الصمامات التي يتحكم بها السكربت |
| Flow Sensors | حساسات اختيارية، ويفضل m³/h |
| Stop If Any Sensor Has No Flow | No-Flow protection |
| Do Not Start If Already ON | يمنع أخذ السيطرة على تشغيل موجود |
| Valve Startup Verification | مهلة تأكيد ON |
| Notification Devices | أجهزة تنبيه اختيارية |

## الحقل عند كل تشغيل

**مدة التشغيل:** من 1 إلى 120 دقيقة، الافتراضي 10.

## التنفيذ خطوة بخطوة

1. يقرأ مدة التشغيل المطلوبة.
2. إذا كان خيار Block مفعّلًا وأي صمام مختار ON أصلًا:
   - لا يلمس الصمام.
   - يبلغك أن التشغيل لم يبدأ.
3. يرسل ON لكل الصمامات.
4. ينتظر حتى مهلة Startup Verification لتأكيد أن الجميع ON.
5. إذا لم يتأكد:
   - يرسل OFF للجميع.
   - يبلغ Failure.
   - ينهي السكربت.
6. يرسل Start Notification.
7. ينتظر دقيقة.
8. يتأكد أن الجميع ما زال ON.
9. يقرأ كل Flow Sensor.
10. إذا No-Flow مفعّل وأي حساس غير متاح أو `<=0`:
    - يرسل OFF للجميع.
    - يبلغ Failure.
11. ينتظر بقية المدة، مع Trigger لاكتشاف انتقال أي صمام من ON إلى OFF.
12. إذا انطفأ صمام مبكرًا:
    - يطفئ البقية.
    - يبلغ Manual/Early Stop.
13. عند اكتمال الوقت:
    - يرسل OFF للجميع.
14. ينتظر حتى 15 ثانية لتأكيد أن الجميع OFF.
15. إذا لم يتأكد:
    - يبلغ Shutdown Failure.
16. إذا نجح:
    - يرسل Completion Notification.
    - إذا لديك Flow Sensors يعرض Estimate للاستهلاك.

## تقدير الماء

مثل Smart Irrigation، الحساب مبني على **عينة بعد دقيقة واحدة**:

```text
Estimated liters =
  sampled total flow (m³/h)
  × runtime hours
  × 1000
```

ليس عداد استهلاك فعلي.

## أهم حد أمان: Restart

إذا أُعيد تشغيل Home Assistant أثناء Delay/Wait في السكربت، ينتهي سياق التشغيل ولا توجد ضمانة أن خطوة OFF النهائية ستُنفّذ.

لذلك استخدم معه دائمًا للصمامات الحقيقية:

- [Long-running Water Safety Watchdog](../../automation/irrigation/WATER_SAFETY.md)
- Hardware Auto-Close إذا كان جهازك يدعمه.

## اختبار آمن

1. استورد السكربت.
2. اختر صمامًا تحت المراقبة.
3. شغله لمدة دقيقة واحدة.
4. تأكد من ON ثم OFF.
5. جرّب إطفاء الصمام يدويًا أثناء التشغيل.
6. اختبر Flow failure بشكل مراقب.
7. لا تعتمد مدة طويلة قبل نجاح كل الاختبارات.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/script/irrigation/manual_irrigation_safe_run.yaml
```

[![Import Manual Irrigation](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fscript%2Firrigation%2Fmanual_irrigation_safe_run.yaml)
