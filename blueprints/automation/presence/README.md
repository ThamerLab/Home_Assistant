# 📍 Zone Exit Notification — Detailed Guide

<p align="center">
  <img src="../../../assets/zone-notification.svg" alt="Zone Exit Notification Blueprint" width="100%">
</p>

Blueprint لإرسال إشعار عندما يغادر كيان `person` منطقة `zone` محددة.

المنطق مأخوذ من Blueprint **Zone Notification** الرسمي المضمّن في Home Assistant، مع الاحتفاظ بنسبة المصدر في ملف YAML.

## الاستخدامات

- إشعار خروج فرد من المنزل.
- إشعار مغادرة طفل/سائق/عامل/عاملة لمنطقة محددة عندما يكون تتبع الموقع مفعّلًا بموافقته.
- إشعار مغادرة موظف أو مركبة من Zone إذا كان تمثيلها داخل Home Assistant مناسبًا.

الـBlueprint **لا ينشئ تتبعًا جديدًا** ولا يحصل على موقع شخص من تلقاء نفسه؛ يعتمد فقط على `person` الموجود أصلًا.

## المدخلات

| Input | الوظيفة |
|---|---|
| Person | كيان `person.*` |
| Zone | كيان `zone.*` |
| Device to notify | جهاز Companion App |

## التنفيذ خطوة بخطوة

### 1. مراقبة Person

كل تغير في حالة Person يطلق Trigger.

### 2. معرفة اسم الـZone

يقرأ اسم Zone المختارة ويخزنه في `zone_state`.

### 3. التحقق أنه **خرج** فعلًا

لا يرسل إشعارًا لمجرد أي تغير.

للـHome Zone:

- الحالة السابقة يجب أن تكون `home`.
- الحالة الجديدة يجب ألا تكون `home`.

لأي Zone أخرى:

- الحالة السابقة يجب أن تساوي اسم الـZone.
- الحالة الجديدة يجب أن تختلف عنها.

### 4. إرسال الإشعار

يرسل اسم الشخص + المنطقة التي غادرها إلى جهاز Companion App المختار.

## مثال: تنبيه خروج العاملة

1. أنشئ Device Tracker بالطريقة التي وافق الشخص على استخدامها.
2. اربطه بكيان Person.
3. استورد الـBlueprint.
4. اختر Person.
5. اختر `zone.home`.
6. اختر جوالك.
7. احفظ الأوتوميشن.

عند خروج Person من Home Zone، يصلك إشعار.

## دقة الموقع

الدقة لا يحددها هذا الـBlueprint. تعتمد على:

- هاتف الشخص.
- صلاحيات Location.
- Background refresh.
- GPS/Wi-Fi/Cell location.
- حجم Radius للـZone.
- سرعة وصول تحديث Device Tracker إلى Home Assistant.

قد يتأخر إشعار الخروج إذا كان تحديث الموقع متأخرًا.

## الخصوصية

- استخدم تتبع الموقع فقط بموافقة الشخص المعني.
- لا تضع اسم الشخص أو Device ID في هذا المستودع العام.
- إعداد Person/Tracker يبقى في Home Assistant الخاص بك.

## اختبار

1. أنشئ Zone اختبار أو استخدم Home.
2. تأكد أن Person يظهر داخلها.
3. اختبر الخروج فعليًا أو باستخدام Tracker تجريبي.
4. راجع Trace للتأكد أن `from_state` كان داخل الـZone و`to_state` خارجها.
5. تأكد من وصول التنبيه.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/presence/notify_leaving_zone.yaml
```

[![Import Zone Exit Notification](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fnotify_leaving_zone.yaml)

## المصدر

Upstream: Home Assistant Core built-in `notify_leaving_zone.yaml`.  
Copyright Home Assistant contributors; Apache License 2.0.
