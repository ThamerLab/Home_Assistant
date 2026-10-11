# 📖 Quran — Music Assistant Safe Toggle Script

<p align="center">
  <img src="../../../assets/quran-toggle.svg" alt="Quran Safe Toggle Script" width="100%">
</p>

Script Blueprint لتحويل أي عنصر قرآن داخل Music Assistant إلى زر ذكي واحد: **تشغيل / استكمال / إيقاف** حسب العنصر الحالي الحقيقي.

## المتطلبات

- Music Assistant.
- MA `media_player` وليس Native Cast/Apple TV.
- URI دقيق للعنصر.
- Media Type الصحيح.

## المدخلات

| Input | الوظيفة |
|---|---|
| Music Assistant Player | الـMA Player المستهدف |
| Exact Music Assistant URI | URI السورة/العنصر |
| Media Type | track / album / playlist / radio |
| Notification Devices | أجهزة اختيارية لتنبيهات الفشل |

## المنطق خطوة بخطوة

### الحالة A — الـPlayer غير متاح

إذا الحالة `unavailable` أو `unknown`:

- لا يرسل Play/Stop.
- يرسل Failure Notification.
- ينشئ Persistent Notification.
- ينهي السكربت.

### الحالة B — نفس URI يعمل الآن

الشروط:

- `state == playing`
- `media_content_id == URI`

التصرف:

1. يرسل `media_player.media_stop`.
2. ينتظر حتى 15 ثانية.
3. النجاح يتطلب أن العنصر لم يعد في حالة Playing بنفس URI.
4. إذا لم يتأكد، يرسل Failure Notification ولا يدعي أن الإيقاف نجح.

### الحالة C — نفس URI متوقف مؤقتًا

الشروط:

- `state == paused`
- `media_content_id == URI`

التصرف:

1. يرسل `media_player.media_play`.
2. ينتظر حتى 15 ثانية.
3. يتأكد أن الحالة `playing` ونفس URI ما زال العنصر الحالي.
4. إذا لم يتأكد، يبلغ بالفشل.

### الحالة D — أي شيء آخر

يشمل:

- Player idle.
- Player off لكنه متاح.
- Music آخر يعمل.
- Quran URI آخر يعمل.

التصرف:

1. `music_assistant.play_media`.
2. `enqueue: replace`.
3. ينتظر حتى 30 ثانية.
4. النجاح يتطلب `playing` + نفس URI.
5. خلاف ذلك يرسل Failure Notification + Persistent Notification.

## لماذا المقارنة بالـURI مهمة؟

لو اكتفينا بفحص `playing`، ممكن يكون Spotify أو راديو أو سورة أخرى هي التي تعمل.

الـURI يجعل القرار مرتبطًا **بنفس العنصر المطلوب**.

## mode

`single`

إذا ضغطت الزر عدة مرات بسرعة، لا تبدأ عدة Runs متنافسة في نفس الوقت.

## حدود التصميم

- يعتمد على تحديث حالة Music Assistant في Home Assistant.
- Stop/Resume النهائي يعتمد على قدرات الـPlayer التي يوفرها Music Assistant.
- لا يختار السورة بالاسم أو Search؛ يجب إدخال URI صريح.
- لا يحتوي أي Entity ID خاص بمنزل معين.

## اختبار آمن

اختبر الحالات الأربع بشكل منفصل:

1. Player Idle → يجب أن يبدأ URI المطلوب.
2. نفس URI Playing → يجب أن يتوقف.
3. نفس URI Paused → يجب أن يستكمل.
4. شيء آخر Playing → يجب أن يستبدل الـQueue بالعنصر المطلوب.

راجع Trace في كل حالة.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/script/quran/music_assistant_quran_toggle.yaml
```

[![Import Quran Safe Toggle](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fscript%2Fquran%2Fmusic_assistant_quran_toggle.yaml)
