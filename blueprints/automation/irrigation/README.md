# 💧 Irrigation Blueprints

<p align="center">
  <img src="../../../assets/irrigation.svg" alt="Smart Irrigation" width="49%">
  <img src="../../../assets/water-safety.svg" alt="Water Safety Watchdog" width="49%">
</p>

يوجد في هذا القسم Blueprintان منفصلان لأن **تشغيل السقاية** و**مراقبة التشغيل الطويل** وظيفتان مختلفتان.

## 1. 🌱 Smart Irrigation

الملف:
`smart_irrigation.yaml`

المهام:

- Sunrise / Sunset.
- Custom time.
- Fixed clock interval.
- منع بدء دورة فوق تشغيل موجود.
- تحقق من ON.
- فحص كل Flow Sensor بعد دقيقة.
- No-Flow protection.
- اكتشاف إطفاء أي صمام مبكرًا.
- إيقاف نهائي + تحقق OFF.
- تقدير استهلاك اختياري.

[📖 الشرح التفصيلي خطوة بخطوة](./SMART_IRRIGATION.md)

## 2. 🚨 Long-running Water Safety Watchdog

الملف:
`long_running_water_safety.yaml`

المهام:

- مراقبة مدة ON.
- Critical Notification.
- Stop all / Keep running.
- تحقق OFF بعد Stop.
- Watchdog كل 5 دقائق + Startup fallback.
- Snooze بعد Keep.

[📖 الشرح التفصيلي خطوة بخطوة](./WATER_SAFETY.md)

> [!IMPORTANT]
> للأجهزة المائية الحقيقية يفضّل استخدام الاثنين معًا: الأول للتشغيل الطبيعي، والثاني كطبقة أمان مستقلة.
