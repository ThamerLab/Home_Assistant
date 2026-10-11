# 🔔 Available Updates — Daily Summary

<p align="center">
  <img src="../../../assets/updates.svg" alt="Available Updates Notification" width="100%">
</p>

Blueprint يرسل ملخصًا يوميًا فقط عندما يكون لدى Home Assistant كيان `update.*` واحد أو أكثر في حالة `on`، وهي الحالة التي تعني وجود تحديث متاح.

## لماذا Blueprint بدل Regex ثابت؟

بعض الأوتوميشنات تصنف الأولوية من اسم `friendly_name`. هذا هش لأن الأسماء تتغير حسب التكامل أو اللغة.

هنا أنت تختار بنفسك **Priority Update Entities** من الواجهة، والبقية تُدرج تلقائيًا تحت Other updates.

## المدخلات

| Input | الافتراضي | الوظيفة |
|---|---:|---|
| Notification Time | 09:30 | وقت الفحص اليومي |
| Priority Update Entities | لا يوجد | تحديثات تريد إظهارها أولًا |
| Notification Devices | — | جهاز أو عدة أجهزة Companion App |
| Notification Tag | home_assistant_updates | استبدال إشعار اليوم السابق بدل تكديسه |

## التنفيذ خطوة بخطوة

### 1. Trigger يومي

يعمل مرة في الوقت المحدد.

### 2. شرط وجود تحديث

يفحص جميع `states.update`.

إذا لم يوجد أي Entity حالتها `on`:

- ينتهي الأوتوميشن.
- لا يرسل إشعارًا فارغًا.

### 3. بناء مجموعتين

من التحديثات المتاحة فقط:

- **Priority:** أي Entity اخترتها في Priority Update Entities.
- **Other:** كل Update متاح آخر.

### 4. إنشاء الرسالة

يعرض اسم كل Update متاح تحت مجموعته.

### 5. إرسال الإشعار

يرسله لكل جهاز اخترته مع:

- عدد التحديثات في العنوان.
- Tag ثابت.
- رابط `/config/updates` لفتح شاشة التحديثات.

## ما الذي لا يفعله؟

- لا يثبت تحديثات.
- لا يضغط Update تلقائيًا.
- لا يعيد تشغيل Home Assistant.
- لا يعتبر كل تحديث Critical؛ أنت تحدد Priority بنفسك.

## اختبار

1. أنشئ Automation بالـBlueprint.
2. اختر وقتًا بعد دقائق قليلة من الوقت الحالي للاختبار.
3. تأكد أن لديك Update entity في حالة `on`.
4. تحقق أن الرسالة ظهرت ومجموعات Priority/Other صحيحة.
5. بعد ذلك أعد الوقت إلى الوقت اليومي المطلوب.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/system/available_updates_notification.yaml
```

[![Import Available Updates](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Favailable_updates_notification.yaml)
