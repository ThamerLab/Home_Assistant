# Automation Catalog

هذا الملف يشرح **كل نمط Automation/Script منزلي ممثل حاليًا في هذا المستودع**، ويجمعه مع الـBlueprint العام المقابل.

> آخر Snapshot منزلي تم استخدامه كمصدر للمراجعة كان بتاريخ 2026-10-06. المستودع العام لا يحتوي Entity IDs أو أسماء أجهزة خاصة بالمنزل.

## خريطة الأنظمة

| # | النظام | النوع | Blueprint |
|---:|---|---|---|
| 1 | تشغيل القرآن عند الشروق والغروب | Automation | [Quran Sunrise & Sunset](../blueprints/automation/quran/SUNRISE_SUNSET.md) |
| 2 | السقاية المجدولة | Automation | [Smart Irrigation](../blueprints/automation/irrigation/SMART_IRRIGATION.md) |
| 3 | إشعار التحديثات | Automation | [Available Updates](../blueprints/automation/system/README.md) |
| 4 | الإنارة الخارجية من الغروب للفجر | Automation | [Dusk to Dawn](../blueprints/automation/lighting/DUSK_TO_DAWN.md) |
| 5 | تنبيه حالة الإنارة الخارجية غير المعتادة | Automation | [Abnormal State Alert](../blueprints/automation/lighting/ABNORMAL_STATE_ALERT.md) |
| 6 | تنبيه الماء/السقاية التي بقيت شغالة | Automation | [Water Safety Watchdog](../blueprints/automation/irrigation/WATER_SAFETY.md) |
| 7 | السقاية اليدوية المؤقتة | Script | [Manual Irrigation](../blueprints/script/irrigation/README.md) |
| 8 | زر القرآن الذكي | Script | [Quran Safe Toggle](../blueprints/script/quran/README.md) |
| 9 | تنبيه خروج شخص من Zone | Automation | [Zone Exit Notification](../blueprints/automation/presence/README.md) |

---

## 1. 📖 تشغيل القرآن عند الشروق والغروب

**Trigger:** شروق + غروب.

**التسلسل:**

1. Home Assistant يستقبل حدث الشمس.
2. يفحص MA Player.
3. إذا غير متاح يوقف ويبلغ.
4. إذا متاح يطلب من Music Assistant تشغيل URI صريح.
5. يستخدم Replace Queue لمنع استمرار محتوى قديم.
6. ينتظر بحد أقصى 30 ثانية.
7. النجاح يحتاج Player=Playing ونفس URI.
8. عند النجاح ينتهي فورًا.
9. عند الفشل يبلغ ولا ينتظر ساعات.

**سبب التصميم:** الأوتوميشن مسؤول عن بدء التلاوة فقط، وليس تفسير كل Pause/End لاحق.

---

## 2. 🌱 السقاية المجدولة

**Trigger:** شروق/غروب أو وقت مخصص أو Interval.

**التسلسل:**

1. يحدد هل الـTrigger مطابق للSchedule Mode.
2. يفحص هل أي صمام شغال مسبقًا.
3. يشغل جميع الصمامات.
4. يتحقق أن الجميع ON.
5. ينتظر دقيقة.
6. يتأكد أن الصمامات لم تنطفئ.
7. يفحص كل Flow Sensor مختار.
8. عند No-Flow يوقف الجميع فورًا.
9. يراقب أي إطفاء مبكر لبقية المدة.
10. عند نهاية المدة يرسل OFF للجميع.
11. يتحقق أن الجميع OFF.
12. يحسب Estimate إذا توجد حساسات.
13. يرسل Completion فقط بعد نجاح الإيقاف.

---

## 3. 🔔 إشعار التحديثات

**Trigger:** وقت يومي.

**التسلسل:**

1. يجمع كل `update.*` التي حالتها ON.
2. إذا القائمة فارغة لا يرسل شيئًا.
3. يقسم المتاح إلى Priority وOther حسب اختيار المستخدم.
4. يبني ملخصًا.
5. يرسله للأجهزة المختارة.
6. Notification يفتح صفحة Updates.
7. لا يثبت أي تحديث تلقائيًا.

---

## 4. 🌙 الإنارة الخارجية Dusk to Dawn

**Trigger:** Sun elevation يعبر Threshold.

**المساء:**

1. Turn ON.
2. انتظر State=ON.
3. إذا فشل، انتظر 5 ثوان.
4. أعد المحاولة مرة.
5. تحقق مرة ثانية.
6. إذا فشل، أرسل خطأ.

**الصباح:** نفس التسلسل مع OFF.

**قرار مهم:** لا يوجد Startup sync حتى لا يمسح قرارًا يدويًا بمجرد Restart.

---

## 5. 💡 تنبيه حالة الإنارة غير المعتادة

**Trigger:** استمرار Night+OFF أو Day+ON مدة محددة.

**التسلسل:**

1. Template يكتشف التناقض.
2. ينتظر مدة Mismatch.
3. يحدد Night Off أو Day On.
4. ينشئ Fix/Keep IDs فريدة.
5. يرسل Actionable Notification.
6. ينتظر Fix أو Keep أو أن تنحل المشكلة.
7. Fix يعيد التحقق من الحالة الحالية قبل التغيير.
8. Keep لا يغير شيئًا.
9. Notification يُمسح عند نهاية السيناريو.

---

## 6. 🚨 Water Safety Watchdog

**Trigger:** صمام ON لمدة طويلة + Watchdog 5 دقائق + Startup fallback.

**التسلسل:**

1. يتحقق أن التشغيل الطويل ما زال حقيقيًا.
2. ينشئ Stop/Keep IDs فريدة.
3. يرسل Critical Notification.
4. Stop → OFF للجميع → Verify OFF.
5. إذا Verify فشل → Critical failure.
6. Keep → Snooze.
7. All Off يدويًا → Clear notification.
8. No response → التنبيه يبقى ظاهرًا؛ الـWatchdog يستطيع التجديد لاحقًا.

---

## 7. 💧 Manual Irrigation Script

**التسلسل:**

1. يطلب مدة تشغيل عند استدعاء السكربت.
2. يمنع التشغيل إذا وجد صمامًا ON مسبقًا.
3. يشغل الجميع.
4. يتحقق من ON.
5. ينتظر دقيقة.
6. يتحقق من الصمامات وFlow.
7. يراقب الإطفاء المبكر.
8. عند انتهاء المدة يطفئ الجميع.
9. يتحقق من OFF.
10. يعرض تقدير الاستهلاك إذا توجد حساسات.

**مهم:** Restart أثناء تشغيل Script يوقف Sequence؛ لذلك Water Safety Blueprint موصى به كطبقة مستقلة.

---

## 8. 📖 Quran Safe Toggle Script

**التسلسل:**

1. Player unavailable → Failure.
2. نفس URI Playing → Stop + Verify.
3. نفس URI Paused → Resume + Verify.
4. أي حالة أخرى → Replace Queue + Play.
5. نجاح Play يحتاج Playing + نفس URI.
6. فشل التحقق ينتج Notification واضح.

---

## 9. 📍 Zone Exit Notification

**Trigger:** تغير Person state.

**التسلسل:**

1. يقرأ Person وZone.
2. يتحقق أن الحالة السابقة كانت داخل Zone.
3. يتحقق أن الحالة الجديدة خرجت منها.
4. يرسل اسم الشخص والمنطقة إلى Companion App.

**مهم:** دقة وتوقيت الخروج يعتمدان على Device Tracker وليس الـBlueprint نفسه.
