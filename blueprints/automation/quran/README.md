# 📖 Quran via Music Assistant

<p align="center">
  <img src="../../../assets/quran.svg" alt="Quran via Music Assistant" width="100%">
</p>

هذا القسم يحوّل تشغيل القرآن إلى **Music Assistant** بدل الاعتماد مباشرة على Apple TV أو Google Cast أو روابط YouTube.

## الملفات

### 1) Sunrise & Sunset Automation

`music_assistant_sunrise_sunset.yaml`

يشغّل URI محدد من مكتبة Music Assistant عند الشروق والغروب، ثم ينتظر حتى 30 ثانية للتأكد من أن نفس الـURI بدأ فعليًا.

**لا ينتظر انتهاء السورة**؛ الأوتوميشن ينتهي بعد تأكيد بداية التشغيل.

### 2) Safe Toggle Script

`../../script/quran/music_assistant_quran_toggle.yaml`

سكريبت Blueprint يمكن استخدامه كزر:

- إذا نفس السورة تعمل → Stop.
- إذا نفس السورة Paused → Resume.
- إذا يعمل شيء آخر → Replace queue وتشغيل السورة.
- إذا الجهاز غير متاح → تنبيه خطأ.
- يتحقق من `media_content_id` قبل اعتبار التشغيل ناجحًا.

## المتطلبات

- Music Assistant مثبت ومربوط بـHome Assistant.
- الـPlayer المختار يجب أن يكون **كيان Music Assistant نفسه**، وليس الـNative Apple TV / Cast entity.
- يجب معرفة الـURI الحقيقي للعنصر من Music Assistant.

مثال:

```text
library://track/151
```

## Import — Sunrise/Sunset

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/quran/music_assistant_sunrise_sunset.yaml
```

[![Import Quran Sunrise/Sunset](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fquran%2Fmusic_assistant_sunrise_sunset.yaml)

## Import — Safe Toggle Script

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/script/quran/music_assistant_quran_toggle.yaml
```

[![Import Quran Toggle Script](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fscript%2Fquran%2Fmusic_assistant_quran_toggle.yaml)

## ملاحظة

لا يحتوي المستودع على أسماء سماعات منزلك أو Entity IDs أو URIs شخصية مفروضة على الجميع؛ تختارها من Inputs عند إنشاء الأوتوميشن/السكريبت.
