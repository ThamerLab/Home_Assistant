# 🌙 Outdoor Lighting

<p align="center">
  <img src="../../../assets/outdoor-lighting.svg" alt="Outdoor Lighting Blueprints" width="100%">
</p>

قسم الإنارة الخارجية يحتوي Blueprintين متكاملين.

## 1) Dusk to Dawn

`outside_lights_dusk_dawn.yaml`

- تشغيل الإنارة عندما ينزل ارتفاع الشمس تحت الحد المختار.
- إطفاؤها عندما يرتفع فوق نفس الحد.
- Retry واحد إذا لم تستجب الإنارة.
- لا يوجد Startup sync يجبر الإنارة على وضع معين، لذلك التحكم اليدوي يبقى له أولوية بعد حدث الشروق/الغروب.

### Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/lighting/outside_lights_dusk_dawn.yaml
```

[![Import Dusk to Dawn](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_lights_dusk_dawn.yaml)

## 2) Abnormal State Alert

`outside_light_attention.yaml`

يراقب الحالات غير المعتادة:

- 🌙 الليل + اللمبة مطفأة لمدة محددة.
- ☀️ النهار + اللمبة شغالة لمدة محددة.

ثم يرسل Actionable Notification فيه:

- **Fix**: يرجع اللمبة للوضع المتوقع الآن.
- **Keep**: يحترم اختيارك ولا يغير اللمبة.

كما أن Action IDs فريدة لكل تشغيل باستخدام `context.id` لتجنب ضغط زر قديم على تشغيل جديد.

### Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/lighting/outside_light_attention.yaml
```

[![Import Outdoor Light Alert](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_light_attention.yaml)
