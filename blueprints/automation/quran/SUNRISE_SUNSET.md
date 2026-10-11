# 📖 Quran — Sunrise & Sunset via Music Assistant

<p align="center">
  <img src="../../../assets/quran-schedule.svg" alt="Quran Sunrise and Sunset via Music Assistant" width="100%">
</p>

هذا الـBlueprint يشغّل عنصر قرآن محدد من **Music Assistant** عند الشروق وعند الغروب، ثم يتحقق أن **نفس URI المطلوب** أصبح العنصر الحالي وأن الـPlayer دخل حالة `playing`.

## لماذا Music Assistant؟

الهدف أن يكون Home Assistant مسؤولًا عن **متى** يبدأ التشغيل، بينما Music Assistant مسؤول عن **المكتبة والـQueue والـPlayer**.

هذا يتجنب الاعتماد المباشر على:

- Native Apple TV entity.
- Native Google Cast entity.
- YouTube.
- `media_extractor`.
- رابط ملف محلي خاص بجهاز واحد.

## المتطلبات

1. Music Assistant مثبت ومربوط بـHome Assistant.
2. الـPlayer ظاهر داخل Home Assistant من Integration اسمها `music_assistant`.
3. العنصر المطلوب موجود في مكتبة Music Assistant.
4. لديك URI دقيق للعنصر، مثل:
   `library://track/151`

> [!IMPORTANT]
> لا تختَر Native HomePod / Apple TV / Cast entity. الـSelector في الـBlueprint مقيد بكيانات `media_player` التابعة لـMusic Assistant.

## المدخلات

| Input | الوظيفة |
|---|---|
| Music Assistant Player | الـMA media_player المستهدف |
| Exact Music Assistant URI | URI العنصر المطلوب بالضبط |
| Media Type | track / album / playlist / radio |
| Notification Devices | أجهزة Companion App الاختيارية |

## التنفيذ خطوة بخطوة

### 1. Trigger الشروق أو الغروب

هناك Triggerان:

- `sunrise`
- `sunset`

ولا توجد مدة انتظار طويلة بعد ذلك.

### 2. فحص توفر الـPlayer

إذا كانت حالته:

- `unavailable`
- أو `unknown`

فلن يحاول التشغيل.

بدل ذلك:

- يرسل Push Notification إلى الأجهزة المختارة.
- ينشئ Persistent Notification.
- ينهي الأوتوميشن.

### 3. تشغيل العنصر عبر Music Assistant

يستدعي:

`music_assistant.play_media`

مع:

- `media_id` = URI الذي أدخلته.
- `media_type` = النوع الذي اخترته.
- `enqueue: replace`.

معنى `replace`: استبدال الـQueue الحالي بالمحتوى المطلوب بدل إضافة السورة خلف محتوى قديم.

### 4. عدم اعتبار Service Call نجاحًا

حتى لو Home Assistant قبل أمر الخدمة، الـBlueprint لا يقول إن التشغيل نجح مباشرة.

ينتظر حتى 30 ثانية حتى يتحقق الشرطان معًا:

1. حالة الـPlayer = `playing`.
2. `media_content_id` = URI المطلوب بالضبط.

### 5. عند النجاح

يرسل إشعار نجاح اختياري يوضح هل التشغيل بدأ عند الشروق أو الغروب.

ثم ينتهي الأوتوميشن فورًا.

**لا يبقى منتظرًا حتى نهاية السورة.**

### 6. عند الفشل

إذا لم يتحقق التشغيل خلال 30 ثانية:

- يرسل Push Notification اختياريًا.
- ينشئ Persistent Notification.
- يعرض:
  - الـPlayer.
  - URI المطلوب.
  - الحالة الحالية.
  - العنصر الحالي إن وجد.

## لماذا لا ننتظر نهاية السورة؟

الانتظار ساعة أو ساعتين يجعل Automation instance مشغولًا بدون حاجة، ويعقّد Reload/Restart ويخلط بين:

- انتهاء طبيعي.
- Pause.
- تغيير المصدر.
- فقدان الاتصال.

هذا الـBlueprint مسؤول فقط عن **بدء التشغيل الموثق**.

## سلوك التزامن

`mode: single`.

إذا كان تشغيل الأوتوميشن ما زال داخل نافذة التحقق القصيرة ووصل Trigger آخر، لن يبدأ Run متداخل.

عمليًا الشروق والغروب متباعدان جدًا، لذلك لا يوجد سبب لاستخدام `restart`.

## حدود التحقق

التحقق يعتمد على ما يبلغه Music Assistant في كيان Home Assistant:

- `state`
- `media_content_id`

هذا يثبت أن MA Queue يرى العنصر المطلوب نشطًا، لكنه لا يقيس الصوت المادي الخارج من السماعة.

## اختبار قبل الاعتماد

1. تأكد أن الـMA Player الصحيح هو الذي ستختاره.
2. احصل على URI من Music Assistant بدل كتابة اسم السورة فقط.
3. أنشئ Automation من الـBlueprint.
4. من واجهة الأوتوميشن استخدم **Run actions** في وقت تستطيع فيه سماع الجهاز، أو أنشئ نسخة اختبارية بTrigger مؤقت.
5. تأكد أن العنصر الحالي في Music Assistant هو نفس URI.
6. اختبر حالة Player unavailable للتأكد من Failure path.
7. بعد نجاح الاختبار اعتمد الشروق والغروب.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/quran/music_assistant_sunrise_sunset.yaml
```

[![Import Quran Sunrise & Sunset](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fquran%2Fmusic_assistant_sunrise_sunset.yaml)
