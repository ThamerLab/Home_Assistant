# 🌱 Smart Irrigation Blueprint

<p align="center">
  <img src="../../../assets/irrigation.svg" alt="ThamerLab Smart Irrigation Blueprint" width="100%">
</p>

Blueprint عام للسقاية في Home Assistant يجمع الجدولة، مراقبة التدفق، الحماية من انقطاع الماء، حساب استهلاك تقريبي، والتنبيهات.

## أهم المزايا

- 🌅 تشغيل عند **الشروق والغروب**.
- 🕒 وقت مخصص مرة يوميًا.
- 🔁 تكرار كل عدد محدد من الساعات.
- 🚿 دعم أكثر من صمام/سويتش في نفس الدورة.
- 🌊 قراءة Flow Sensors بعد دقيقة من بدء السقاية.
- 🚨 إيقاف تلقائي إذا لم يوجد تدفق ماء.
- 🛑 اكتشاف الإيقاف اليدوي قبل نهاية المدة.
- 📱 إرسال إشعارات إلى أكثر من جهاز Home Assistant Companion.
- 💧 تقدير الاستهلاك باللتر و m³ عند استخدام حساسات بوحدة m³/h.

## المدخلات

| Input | الوصف | ملاحظات |
|---|---|---|
| **Irrigation Valves** | صمام أو أكثر من نوع `switch` | مطلوب |
| **Irrigation Duration** | مدة السقاية بالدقائق | 1–120 دقيقة |
| **Schedule Mode** | Sun / Custom / Repeat | اختر أسلوبًا واحدًا |
| **Custom Time** | وقت التشغيل اليومي | يستخدم فقط مع Custom |
| **Repeat Every X Hours** | عدد الساعات بين الدورات | يستخدم فقط مع Repeat |
| **Flow Sensors** | حساس أو أكثر للتدفق | اختياري، ويفضل m³/h |
| **Stop If No Flow Detected** | حماية من عدم وجود ماء | تعمل عند وجود Flow Sensors |
| **Notification Devices** | أجهزة mobile_app | اختياري |
| **Enable Notifications** | تشغيل/إيقاف التنبيهات | افتراضيًا مفعلة |

## كيف يعمل؟

1. ينتظر Trigger مناسب لطريقة الجدولة المختارة.
2. يشغّل جميع الصمامات المحددة.
3. بعد دقيقة يقرأ حساسات التدفق ويجمعها.
4. إذا كانت حماية No-Flow مفعلة والتدفق = 0، يوقف الصمامات فورًا ويرسل تنبيه خطأ.
5. يراقب الصمامات خلال مدة السقاية لاكتشاف الإيقاف اليدوي.
6. عند اكتمال الوقت يطفئ الصمامات.
7. يحسب الاستهلاك التقديري:

```text
Estimated m³ = Flow (m³/h) × Duration (hours)
Estimated liters = Estimated m³ × 1000
```

> [!NOTE]
> الحساب **تقديري** لأنه يعتمد على عينة التدفق المقروءة بعد الدقيقة الأولى، وليس تكامل التدفق لحظة بلحظة.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/irrigation/smart_irrigation.yaml
```

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Fsmart_irrigation.yaml)

## متطلبات موصى بها

- Home Assistant حديث.
- صمامات مياه تظهر كـ `switch`.
- Flow Sensors بوحدة `m³/h` للاستفادة من الحماية والحساب.
- Home Assistant Companion App للتنبيهات.

## ملاحظات أمان

- اختبر الـBlueprint أول مرة وأنت قريب من الصمامات.
- لا تعتمد على تقدير التدفق كعداد فوترة.
- تأكد أن الصمامات تستجيب فعليًا لأوامر الإيقاف.
