# Installation & Import

هذا المستودع عبارة عن **Home Assistant Blueprint collection** وليس HACS Integration.

## الطريقة الصحيحة

لكل Blueprint يوجد زر Import في صفحة الشرح الخاصة به، أو:

1. افتح Home Assistant.
2. اذهب إلى **Settings → Automations & Scenes → Blueprints**.
3. اختر **Import Blueprint**.
4. الصق Raw URL.
5. أنشئ Automation/Script من الـBlueprint.
6. اختر Inputs المناسبة لمنزلك.
7. احفظ واختبر قبل الاعتماد.

## لماذا لا يوجد hacs.json؟

HACS مخصص لأنواع مستودعات معينة مثل Integrations وDashboard plugins وThemes وغيرها. هذا المستودع يجمع Blueprints متعددة، ولذلك الاعتماد على `hacs.json` هنا يعطي انطباعًا خاطئًا عن طريقة التثبيت.

## تحديث Blueprint مستورد

Home Assistant يحتفظ بنسخة من ملف الـBlueprint لديك. إذا حدّث المصدر، راجع النسخة المستوردة ثم Reload automations/scripts حسب الحاجة.

## مبدأ الأمان

لا تنسخ إعدادات منزل شخص آخر حرفيًا. الـBlueprint مصمم لكي تختار:

- Entities.
- Devices.
- مدة التشغيل.
- حدود الشمس/التدفق.
- URIs.
- إعدادات الإشعار.

بدون رفع بيانات منزلك الخاصة إلى GitHub.
