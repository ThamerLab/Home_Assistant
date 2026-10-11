<div align="center">

<img src="./assets/hero.svg" alt="ThamerLab Home Assistant Collection" width="100%">

<br>

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Blueprints-41BDF5?logo=homeassistant&logoColor=white)
![Music Assistant](https://img.shields.io/badge/Music%20Assistant-Quran-13705A)
![Safety](https://img.shields.io/badge/Safety-Water%20%26%20Lighting-EF4444)
![Language](https://img.shields.io/badge/Docs-Arabic%20%2B%20English-8B5CF6)
![Country](https://img.shields.io/badge/Built%20in-Saudi%20Arabia-10B981)
![Maintained](https://img.shields.io/badge/Maintained-Yes-22C55E)

**مجموعة عملية وقابلة للمشاركة لملفات Home Assistant — Blueprints، Dashboards، Packages وأتمتة منزلية مجرّبة.**

[Blueprints](#-blueprints) · [القرآن](#-القرآن--music-assistant) · [الإنارة الخارجية](#-الإنارة-الخارجية) · [أمان المياه](#-أمان-المياه) · [الاستيراد](#-الاستيراد-السريع)

</div>

---

## ✨ وش موجود هنا؟

المستودع مخصص للحلول التي يمكن مشاركتها وإعادة استخدامها بدون ربطها بكيانات أو أسرار منزل محدد:

- 🧩 **Blueprints** جاهزة للاستيراد.
- 📖 تشغيل القرآن عبر **Music Assistant**.
- 🌙 أتمتة ومراقبة **الإنارة الخارجية**.
- 💧 سقاية ذكية + **Watchdog للمياه التي تبقى شغالة**.
- 📍 Presence / Zone notifications.
- 📊 مكان منظم لـDashboards وPackages المستقبلية.

> [!TIP]
> كل Blueprint هنا مصمم ليكون **Generic**: تختار كياناتك وأجهزتك من Inputs بدون رفع Entity IDs أو أسرار منزلك إلى GitHub.

## 🧩 Blueprints

| النظام | Blueprint | ماذا يسوي؟ | التوثيق |
|---|---|---|---|
| 🌱 السقاية | **Smart Irrigation** | شروق/غروب، وقت مخصص، Repeat، Flow، No-Flow، استهلاك تقديري | [شرح](./blueprints/automation/irrigation/README.md) |
| 🚨 المياه | **Long-running Water Safety** | Critical alert إذا بقي صمام/ماء شغال، Stop/Keep، تحقق من الإطفاء | [شرح](./blueprints/automation/irrigation/WATER_SAFETY.md) |
| 📖 القرآن | **Quran Sunrise & Sunset** | تشغيل URI دقيق من Music Assistant عند الشروق والغروب والتحقق من البداية | [شرح](./blueprints/automation/quran/README.md) |
| 📖 القرآن | **Quran Safe Toggle Script** | Stop/Resume/Replace Queue حسب العنصر الحالي | [شرح](./blueprints/automation/quran/README.md) |
| 🌙 الإنارة | **Outdoor Lights — Dusk to Dawn** | تشغيل/إطفاء حسب ارتفاع الشمس مع Retry واحترام التحكم اليدوي | [شرح](./blueprints/automation/lighting/README.md) |
| 💡 الإنارة | **Outdoor Light — Abnormal State Alert** | تنبيه إذا بقيت مطفأة ليلًا أو شغالة نهارًا مع Fix/Keep | [شرح](./blueprints/automation/lighting/README.md) |
| 📍 Presence | **Zone Exit Notification** | إشعار عند خروج Person من Zone، ومناسب لسيناريو تنبيه خروج العاملة بموافقتها | [شرح](./blueprints/automation/presence/README.md) |

## 📖 القرآن — Music Assistant

<p align="center">
  <img src="./assets/quran.svg" alt="Quran via Music Assistant" width="82%">
</p>

بدل التشغيل المباشر على Apple TV / Google Cast، الـBlueprints هنا تستخدم **Music Assistant** وURI دقيق من المكتبة.

الموجود:

- **Sunrise & Sunset Automation:** يشغّل السورة عند الشروق والغروب، ويتأكد أن نفس URI بدأ خلال 30 ثانية، ثم ينهي الأوتوميشن بدون انتظار ساعة أو ساعتين.
- **Safe Toggle Script:** إذا نفس السورة تعمل يوقفها، إذا Paused يكملها، وإذا شيء ثاني يعمل يستبدل الـQueue بالسورة المطلوبة.

[📖 شرح القرآن كامل](./blueprints/automation/quran/README.md)

## 🌙 الإنارة الخارجية

<p align="center">
  <img src="./assets/outdoor-lighting.svg" alt="Outdoor Lighting Blueprints" width="82%">
</p>

يوجد Blueprintان منفصلان حتى يبقى المنطق واضحًا:

1. **Dusk to Dawn** — يتحكم بالإنارة عند عبور الشمس للحد المختار، مع Retry واحد.
2. **Abnormal State Alert** — إذا بقيت اللمبة مطفأة ليلًا أو شغالة نهارًا لمدة طويلة، يرسل تنبيه فيه **Fix / Keep**.

[💡 شرح الإنارة الخارجية](./blueprints/automation/lighting/README.md)

## 🚨 أمان المياه

<p align="center">
  <img src="./assets/water-safety.svg" alt="Long Running Water Safety" width="82%">
</p>

**Long-running Water Safety Watchdog** مستقل عن جدول السقاية:

- تنبيه افتراضي بعد 10 دقائق.
- Critical Notification.
- زر **Stop all** وزر **Keep running**.
- يتحقق أن كل الكيانات أصبحت `off` بعد أمر الإيقاف.
- Watchdog كل 5 دقائق لاستدراك Restart/Reload.
- Snooze بعد اختيار Keep ثم يرجع للمراقبة.

[🚨 شرح Water Safety](./blueprints/automation/irrigation/WATER_SAFETY.md)

## 📍 تنبيه الخروج من المنزل

Blueprint **Zone Exit Notification** هو نسخة موثقة من Blueprint Home Assistant الرسمي.

مثال الاستخدام: إرسال إشعار عند خروج Person من `zone.home` — مثل تنبيه خروج العاملة المنزلية عندما يكون تتبع الشخص مُعدًا **بموافقته**.

[📍 شرح Zone Notification](./blueprints/automation/presence/README.md)

## 🚀 الاستيراد السريع

### Smart Irrigation
[![Import Smart Irrigation](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Fsmart_irrigation.yaml)

### Water Safety Watchdog
[![Import Water Safety](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Flong_running_water_safety.yaml)

### Quran — Sunrise & Sunset
[![Import Quran Schedule](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fquran%2Fmusic_assistant_sunrise_sunset.yaml)

### Quran — Safe Toggle Script
[![Import Quran Toggle](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fscript%2Fquran%2Fmusic_assistant_quran_toggle.yaml)

### Outdoor Lights — Dusk to Dawn
[![Import Outdoor Lights](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_lights_dusk_dawn.yaml)

### Outdoor Light — Abnormal State Alert
[![Import Outdoor Light Alert](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_light_attention.yaml)

### Zone Exit Notification
[![Import Zone Exit Notification](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fnotify_leaving_zone.yaml)

أو يدويًا:

```text
Settings
→ Automations & Scenes
→ Blueprints
→ Import Blueprint
```

## 🗂️ هيكلة المستودع

```text
Home_Assistant/
├── assets/
│   ├── hero.svg
│   ├── irrigation.svg
│   ├── outdoor-lighting.svg
│   ├── quran.svg
│   ├── water-safety.svg
│   └── zone-notification.svg
├── blueprints/
│   ├── README.md
│   ├── automation/
│   │   ├── irrigation/
│   │   │   ├── smart_irrigation.yaml
│   │   │   ├── long_running_water_safety.yaml
│   │   │   ├── README.md
│   │   │   └── WATER_SAFETY.md
│   │   ├── lighting/
│   │   │   ├── outside_lights_dusk_dawn.yaml
│   │   │   ├── outside_light_attention.yaml
│   │   │   └── README.md
│   │   ├── presence/
│   │   │   ├── notify_leaving_zone.yaml
│   │   │   └── README.md
│   │   └── quran/
│   │       ├── music_assistant_sunrise_sunset.yaml
│   │       └── README.md
│   └── script/
│       └── quran/
│           └── music_assistant_quran_toggle.yaml
├── dashboards/
├── packages/
└── README.md
```

## 🎨 الهوية

| اللون | الاستخدام | Hex |
|---|---|---|
| 🔵 Home Assistant Blue | العناصر الأساسية | `#41BDF5` |
| 🟢 Emerald | النجاح / Music Assistant / الأتمتة | `#10B981` |
| 🟡 Gold | القرآن | `#C9A84F` |
| 🟣 Violet | Presence / Notifications | `#8B5CF6` |
| 🔴 Red | Safety / Critical Alerts | `#EF4444` |
| ⚫ Deep Navy | الخلفيات | `#0B1220` |

## 🔐 الأمان والخصوصية

- لا ترفع `secrets.yaml` أو Tokens أو API Keys.
- لا تضع عناوين IP عامة أو Webhook IDs أو بيانات تسجيل الدخول.
- لا تضع أسماء أشخاص أو Device IDs الخاصة بمنزلك داخل Blueprint عام.
- تتبع المواقع يعتمد على بيانات موجودة أصلًا داخل Home Assistant؛ استخدم مشاركة الموقع فقط بموافقة الشخص المعني.
- اختبر أي Automation يتحكم بالمياه أو الأجهزة الفعلية قبل الاعتماد عليه.

## 🗺️ Roadmap

- [ ] Irrigation dashboard جاهز للاستيراد.
- [ ] Notification Center package.
- [ ] Energy monitoring package.
- [ ] Climate control package.
- [ ] Mobile-first Mushroom dashboard examples.
- [ ] المزيد من Blueprints المجرّبة والموثقة.

---

<div align="center">

Made for Home Assistant by **ThamerLab**

</div>
