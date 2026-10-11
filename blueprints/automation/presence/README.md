# 📍 Zone Exit Notification

<p align="center">
  <img src="../../../assets/zone-notification.svg" alt="Zone Exit Notification Blueprint" width="100%">
</p>

Blueprint بسيط وموثوق يرسل إشعارًا إلى تطبيق Home Assistant عندما يغادر **Person** منطقة **Zone** محددة.

هذا الملف هو نسخة موثقة من الـBlueprint الرسمي المضمّن في Home Assistant:
[Zone Notification](https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/blueprints/notify_leaving_zone.yaml).

## مثال الاستخدام المنزلي

يمكن استخدامه لتنبيه صاحب المنزل عند مغادرة شخص متتبَّع من `zone.home` — مثل سيناريو متابعة خروج العاملة المنزلية **إذا كان الشخص قد وافق على مشاركة موقعه وتم إعداد Person/Device Tracker بشكل مشروع وواضح**.

الـBlueprint لا يضيف أي وسيلة تتبع جديدة؛ هو يعتمد فقط على `person` و`zone` الموجودين أصلًا داخل Home Assistant.

## ماذا تحتاج؟

| Input | ماذا تختار؟ |
|---|---|
| **Person** | كيان `person.*` للشخص المراد مراقبة خروجه |
| **Zone** | المنطقة مثل `zone.home` |
| **Device to notify** | جوال عليه تطبيق Home Assistant الرسمي |

## ماذا يحدث؟

1. يراقب تغير حالة الـPerson.
2. يتحقق أن الحالة السابقة كانت داخل الـZone المحددة.
3. عند الخروج يرسل Push Notification إلى الجهاز المختار.

## Import

يمكنك استيراد النسخة الموجودة في هذا المستودع:

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/presence/notify_leaving_zone.yaml
```

[![Open your Home Assistant instance and import this blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fnotify_leaving_zone.yaml)

## الخصوصية

- لا تضع أسماء أشخاص أو Device IDs خاصة بك داخل النسخة العامة.
- استخدم مشاركة الموقع فقط بموافقة الشخص المعني.
- إعدادات الـPerson والـDevice Tracker تبقى داخل Home Assistant لديك وليست جزءًا من هذا المستودع.

## المصدر

Copyright Home Assistant contributors.  
Source: `home-assistant/core` built-in blueprint, linked above.
