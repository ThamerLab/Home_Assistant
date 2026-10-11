<div align="center">

<img src="./assets/hero.svg" alt="ThamerLab Home Assistant Collection" width="100%">

<br>

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Blueprints-41BDF5?logo=homeassistant&logoColor=white)
![Target](https://img.shields.io/badge/Validated%20against-HA%202026.9.4-18BCF2)
![Music Assistant](https://img.shields.io/badge/Music%20Assistant-Quran-13705A)
![Safety](https://img.shields.io/badge/Safety-Water%20%26%20Lighting-EF4444)
![Docs](https://img.shields.io/badge/Docs-Step--by--step-8B5CF6)
![Country](https://img.shields.io/badge/Built%20in-Saudi%20Arabia-10B981)

**Reusable Home Assistant Blueprints with detailed Arabic documentation, dedicated visuals, failure handling, and automated validation.**

[Blueprints](#-blueprints) · [Automation Catalog](./docs/AUTOMATION_CATALOG.md) · [Installation](./docs/INSTALLATION.md) · [Validation](./docs/VALIDATION.md)

</div>

---

## 🎯 فلسفة المستودع

هذا المستودع لا يحفظ نسخة خاصة من منزل واحد. بدل ذلك، يحوّل الأتمتة العملية إلى **Blueprints عامة**:

- بدون Entity IDs خاصة.
- بدون IPs أو Tokens أو Device IDs خاصة.
- كل Blueprint له شرح مستقل خطوة بخطوة.
- كل Blueprint له صورة مستقلة.
- كل Wait له Timeout واضح.
- أتمتة الماء والأجهزة الفعلية تتضمن Failure paths بدل افتراض النجاح.
- التغييرات تمر عبر Static Validation + Home Assistant Config Check قبل دمجها.

> [!IMPORTANT]
> نجاح CI يثبت صحة YAML/Blueprint schema وقابلية تحميل Config الاختبار. لا يوجد اختبار Repository يستطيع ضمان استجابة جهاز مادي أو شبكة Zigbee/Wi-Fi بنسبة 100%؛ لذلك يوجد **Live Test Checklist** في شرح كل Blueprint حساس.

## 🧩 Blueprints

### 💧 Water & Irrigation

<table>
<tr>
<td width="50%" valign="top">

<img src="./assets/irrigation.svg" alt="Smart Irrigation" width="100%">

#### 🌱 Smart Irrigation

`smart_irrigation.yaml`

- Sunrise / Sunset / Custom / Fixed interval.
- يمنع بدء دورة فوق صمام شغال مسبقًا.
- Verify ON.
- يفحص **كل** Flow Sensor مختار.
- No-flow shutdown.
- Manual/early-stop detection.
- Verify OFF.
- Estimated water usage.

[📖 شرح تفصيلي](./blueprints/automation/irrigation/SMART_IRRIGATION.md)

</td>
<td width="50%" valign="top">

<img src="./assets/water-safety.svg" alt="Long Running Water Safety" width="100%">

#### 🚨 Long-running Water Safety

`long_running_water_safety.yaml`

- Alert بعد مدة ON طويلة.
- Critical notification.
- Stop all / Keep running.
- Verify OFF.
- 5-minute watchdog.
- Startup fallback.
- Unique notification action IDs.

[📖 شرح تفصيلي](./blueprints/automation/irrigation/WATER_SAFETY.md)

</td>
</tr>
</table>

### 📖 Quran / Music Assistant

<table>
<tr>
<td width="50%" valign="top">

<img src="./assets/quran-schedule.svg" alt="Quran Sunrise and Sunset" width="100%">

#### 📖 Quran Sunrise & Sunset

`music_assistant_sunrise_sunset.yaml`

- Music Assistant player only.
- Exact library URI.
- `enqueue: replace`.
- Verify `playing` + exact URI.
- No 1–2 hour wait.

[📖 شرح تفصيلي](./blueprints/automation/quran/SUNRISE_SUNSET.md)

</td>
<td width="50%" valign="top">

<img src="./assets/quran-toggle.svg" alt="Quran Safe Toggle" width="100%">

#### ▶️ Quran Safe Toggle Script

`music_assistant_quran_toggle.yaml`

- Same URI Playing → Stop + Verify.
- Same URI Paused → Resume + Verify.
- Other content → Replace Queue + Play + Verify.

[📖 شرح تفصيلي](./blueprints/script/quran/README.md)

</td>
</tr>
</table>

### 🌙 Outdoor Lighting

<table>
<tr>
<td width="50%" valign="top">

<img src="./assets/outdoor-dusk-dawn.svg" alt="Outdoor Dusk to Dawn" width="100%">

#### 🌙 Dusk to Dawn

`outside_lights_dusk_dawn.yaml`

- Sun elevation crossing.
- ON at dusk / OFF at dawn.
- Verify first attempt.
- Retry once.
- Failure notification.
- No startup force-sync.

[📖 شرح تفصيلي](./blueprints/automation/lighting/DUSK_TO_DAWN.md)

</td>
<td width="50%" valign="top">

<img src="./assets/outdoor-alert.svg" alt="Outdoor Light Alert" width="100%">

#### 💡 Abnormal State Alert

`outside_light_attention.yaml`

- Night + OFF / Day + ON.
- Configurable mismatch duration.
- Fix / Keep.
- Unique Action IDs.
- Re-check before applying Fix.

[📖 شرح تفصيلي](./blueprints/automation/lighting/ABNORMAL_STATE_ALERT.md)

</td>
</tr>
</table>

### 🔔 System & Presence

<table>
<tr>
<td width="50%" valign="top">

<img src="./assets/updates.svg" alt="Available Updates Notification" width="100%">

#### 🔔 Available Updates

`available_updates_notification.yaml`

- Daily check.
- Sends only when updates exist.
- User-selected Priority updates.
- Other updates grouped automatically.
- Opens Home Assistant Updates page.

[📖 شرح تفصيلي](./blueprints/automation/system/README.md)

</td>
<td width="50%" valign="top">

<img src="./assets/zone-notification.svg" alt="Zone Exit Notification" width="100%">

#### 📍 Zone Exit Notification

`notify_leaving_zone.yaml`

- Official Home Assistant logic mirrored with attribution.
- Person leaves selected Zone.
- Companion App notification.
- Suitable for consent-based household presence alerts.

[📖 شرح تفصيلي](./blueprints/automation/presence/README.md)

</td>
</tr>
</table>

### 💧 Manual Irrigation Script

<p align="center">
  <img src="./assets/manual-irrigation.svg" alt="Manual Irrigation Safe Run" width="72%">
</p>

#### 💧 Manual Irrigation — Safe Timed Run

`manual_irrigation_safe_run.yaml`

مدة التشغيل تُطلب عند كل تشغيل للسكريبت، مع Verify ON، Flow protection، Early-stop detection، Final OFF verification، وNotifications اختيارية.

[📖 شرح تفصيلي](./blueprints/script/irrigation/README.md)

## 📚 Automation Catalog

لشرح جميع الأنظمة نقطة بنقطة في مكان واحد:

**[docs/AUTOMATION_CATALOG.md](./docs/AUTOMATION_CATALOG.md)**

يشمل:

1. Quran sunrise/sunset.
2. Scheduled irrigation.
3. Available updates.
4. Outdoor dusk/dawn.
5. Outdoor abnormal-state alert.
6. Long-running water safety.
7. Manual irrigation.
8. Quran safe toggle.
9. Zone exit notification.

## 🚀 Import

كل صفحة شرح تحتوي زر Import مباشر.

الطريقة اليدوية:

```text
Home Assistant
→ Settings
→ Automations & Scenes
→ Blueprints
→ Import Blueprint
```

راجع [Installation Guide](./docs/INSTALLATION.md).

## ✅ Validation

التغييرات تخضع إلى Workflow:

`.github/workflows/validate-blueprints.yml`

ويشمل:

- YAML parse.
- Blueprint metadata.
- `!input` integrity.
- Wait timeouts.
- Dedicated docs/images coverage.
- SVG/XML validation.
- Private-home-data scan داخل Blueprints.
- Home Assistant `check_config` مع Instantiation تجريبية لكل Blueprint.

التفاصيل والحالة الحالية:
[docs/VALIDATION.md](./docs/VALIDATION.md)

## 🗂️ Structure

```text
Home_Assistant/
├── assets/
├── blueprints/
│   ├── automation/
│   │   ├── irrigation/
│   │   │   ├── smart_irrigation.yaml
│   │   │   └── long_running_water_safety.yaml
│   │   ├── lighting/
│   │   │   ├── outside_lights_dusk_dawn.yaml
│   │   │   └── outside_light_attention.yaml
│   │   ├── presence/
│   │   │   └── notify_leaving_zone.yaml
│   │   ├── quran/
│   │   │   └── music_assistant_sunrise_sunset.yaml
│   │   └── system/
│   │       └── available_updates_notification.yaml
│   └── script/
│       ├── irrigation/
│       │   └── manual_irrigation_safe_run.yaml
│       └── quran/
│           └── music_assistant_quran_toggle.yaml
├── docs/
│   ├── AUTOMATION_CATALOG.md
│   ├── INSTALLATION.md
│   └── VALIDATION.md
├── tests/
└── .github/workflows/
```

## 🔐 Security & Privacy

- لا ترفع `secrets.yaml`.
- لا تضع Tokens أو Passwords أو Webhook secrets.
- لا تضع Entity IDs أو Device IDs أو IPs الخاصة بمنزلك داخل Blueprint عام.
- Location/presence automations تستخدم فقط بيانات تم إعدادها مسبقًا داخل Home Assistant وبموافقة الشخص المعني.
- اختبر الماء والأجهزة الفعلية تحت المراقبة قبل الاعتماد.

## 🧱 Other folders

`dashboards/` و`packages/` ما زالا مساحات تجهيز؛ لا يتم ادعاء وجود Dashboard/Package جاهز قبل إضافته واختباره.

`forms/` يحتوي أداة مستقلة وليست جزءًا من Blueprint validation.

---

<div align="center">

Built and maintained by **ThamerLab**

</div>
