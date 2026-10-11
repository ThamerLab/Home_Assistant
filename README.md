<div align="center">

<img src="./assets/hero.svg" alt="ThamerLab Home Assistant Collection" width="100%">

<br>

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Blueprints-41BDF5?logo=homeassistant&logoColor=white)
![Language](https://img.shields.io/badge/Docs-Arabic%20%2B%20English-8B5CF6)
![Country](https://img.shields.io/badge/Built%20in-Saudi%20Arabia-10B981)
![Maintained](https://img.shields.io/badge/Maintained-Yes-22C55E)
![Repository](https://img.shields.io/badge/ThamerLab-Smart%20Home-0B1220)

**مجموعة عملية وقابلة للمشاركة لملفات Home Assistant — Blueprints، Dashboards، Packages وأتمتة منزلية مجرّبة.**

[Blueprints](#-blueprints) · [الاستيراد](#-الاستيراد-السريع) · [هيكلة المستودع](#-هيكلة-المستودع) · [الأمان والخصوصية](#-الأمان-والخصوصية)

</div>

---

## ✨ وش موجود هنا؟

المستودع مخصص للحلول التي يمكن مشاركتها وإعادة استخدامها بدون ربطها بكيانات أو أسرار منزل محدد:

- 🧩 **Blueprints** جاهزة للاستيراد.
- 📊 **Dashboards** وواجهات Lovelace.
- 📦 **Packages** لتنظيم الأنظمة حسب الوظيفة.
- 🔔 أنماط Notifications قابلة لإعادة الاستخدام.
- 🏠 Automations منزلية عامة يمكن تحويلها إلى Blueprints.

> [!TIP]
> الهدف أن يكون كل ملف هنا **Generic** وقابلًا للاستخدام في أي Home Assistant، مع إبقاء Entity IDs والبيانات الشخصية والأسرار خارج المستودع.

## 🧩 Blueprints

<table>
<tr>
<td width="50%" valign="top">

<img src="./assets/irrigation.svg" alt="Smart Irrigation" width="100%">

### 🌱 Smart Irrigation

نظام سقاية عام يدعم الشروق والغروب، الوقت المخصص، التكرار، أكثر من صمام، مراقبة التدفق، حماية No-Flow، اكتشاف الإيقاف اليدوي والتنبيهات.

**مناسب لـ:** صمامات Zigbee / Wi‑Fi التي تظهر كـ `switch`، وFlow Sensors.

[📖 الشرح الكامل](./blueprints/automation/irrigation/README.md)

</td>
<td width="50%" valign="top">

<img src="./assets/zone-notification.svg" alt="Zone Exit Notification" width="100%">

### 📍 Zone Exit Notification

يرسل Push Notification عندما يغادر Person منطقة Zone محددة. النسخة موثقة من Blueprint Home Assistant الرسمي.

**مثال منزلي:** تنبيه خروج العاملة من `zone.home` عندما يكون تتبع الشخص مُعدًا بموافقته.

[📖 الشرح الكامل](./blueprints/automation/presence/README.md)

</td>
</tr>
</table>

### مقارنة سريعة

| Blueprint | Trigger | أهم الحماية/المنطق | Notification |
|---|---|---|---|
| 🌱 Smart Irrigation | Sun / Time / Repeat | No-flow + manual-stop detection | اختياري، عدة أجهزة |
| 📍 Zone Exit Notification | تغير حالة Person وخروجه من Zone | يتحقق من الـZone السابقة والجديدة | جهاز mobile_app واحد |

## 🚀 الاستيراد السريع

### Smart Irrigation

[![Import Smart Irrigation](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Fsmart_irrigation.yaml)

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/irrigation/smart_irrigation.yaml
```

### Zone Exit Notification

[![Import Zone Exit Notification](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fnotify_leaving_zone.yaml)

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/presence/notify_leaving_zone.yaml
```

أو من Home Assistant:

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
│   └── zone-notification.svg
├── blueprints/
│   ├── README.md
│   └── automation/
│       ├── irrigation/
│       │   ├── README.md
│       │   └── smart_irrigation.yaml
│       └── presence/
│           ├── README.md
│           └── notify_leaving_zone.yaml
├── dashboards/
│   └── README.md
├── packages/
│   └── README.md
└── README.md
```

## 🎨 هوية المستودع

| اللون | الاستخدام | Hex |
|---|---|---|
| 🔵 Home Assistant Blue | العناصر الأساسية | `#41BDF5` |
| 🟢 Emerald | النجاح والأتمتة الآمنة | `#10B981` |
| 🟣 Violet | Presence / Notifications | `#8B5CF6` |
| ⚫ Deep Navy | الخلفيات | `#0B1220` |

## 🔐 الأمان والخصوصية

- لا ترفع `secrets.yaml` أو Tokens أو API Keys.
- لا تضع عناوين IP عامة أو Webhook IDs أو بيانات تسجيل الدخول.
- لا تضع أسماء أشخاص أو Device IDs الخاصة بمنزلك داخل Blueprint عام.
- Blueprints الخاصة بالموقع تعتمد على بيانات موجودة أصلًا داخل Home Assistant؛ استخدم مشاركة الموقع فقط بموافقة الشخص المعني.
- راجع أي Automation يتحكم بماء، أقفال، أبواب أو أجهزة قدرة عالية قبل تشغيله.

## 🧱 Dashboards & Packages

المجلدان `dashboards/` و`packages/` مهيآن لإضافة واجهات وأنظمة قابلة لإعادة الاستخدام لاحقًا:

- Irrigation
- Climate
- Security
- Energy
- Presence
- Notifications
- Mobile-first views

## 🗺️ Roadmap

- [ ] Irrigation dashboard جاهز للاستيراد
- [ ] Notification Center package
- [ ] Energy monitoring package
- [ ] Climate control package
- [ ] Mobile-first Mushroom dashboard examples
- [ ] المزيد من Blueprints المجرّبة والموثقة

## 🤝 المساهمة

أي إضافة يفضل أن تكون:

1. بدون أسرار أو Entity IDs شخصية.
2. موثقة بوضوح.
3. قابلة لإعادة الاستخدام.
4. فيها متطلبات وطريقة استيراد واختبار واضحة.

---

<div align="center">

Made for Home Assistant by **ThamerLab**

</div>
