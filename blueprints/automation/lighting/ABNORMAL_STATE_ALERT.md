# 💡 Outdoor Light — Abnormal State Alert

<p align="center">
  <img src="../../../assets/outdoor-alert.svg" alt="Outdoor Light Abnormal State Alert" width="100%">
</p>

This Blueprint does not continuously force the outdoor light into a preferred state. Its job is to detect a mismatch between **light state** and **sun elevation**, then ask the user whether to Fix it or Keep the current state.

## What Counts as an Abnormal State?

With the default threshold of 5°:

- Sun elevation below 5° while the light is `off`.
- Sun elevation above 5° while the light is `on`.

The mismatch must remain true for the full configured **Mismatch Duration** before a notification is sent.

## Inputs

| Input | Default | Purpose |
|---|---:|---|
| Outdoor Light | — | The light to monitor |
| Sun Elevation Threshold | 5° | Boundary used to classify the expected day/night state |
| Mismatch Duration | 30 min | How long the mismatch must persist before alerting |
| Notification Tag | outside_light_attention | Prevents multiple instances from sharing the same notification thread |
| Device to Notify | — | Companion App device that receives the actionable notification |

## Step-by-Step Execution

### Step 1 — Template Trigger

The trigger template becomes true when either mismatch appears.

The condition must stay true continuously for the configured mismatch duration before the automation starts.

### Step 2 — Identify the Current Situation

The automation classifies the mismatch as:

- `night_off`
- `day_on`
- `resolved` if the mismatch disappeared before actions started

### Step 3 — Create Unique Action IDs

The automation creates unique Fix and Keep action IDs from `context.id`.

This prevents an old mobile notification from applying an action to a newer run.

### Step 4 — Send the Actionable Notification

For Night + OFF, the buttons are:

- **Turn it on**
- **Keep it off**

For Day + ON, the buttons are:

- **Turn it off**
- **Keep it on**

### Step 5 — Wait for a Decision or Resolution

The automation waits up to six hours for:

- Fix.
- Keep.
- The abnormal state to resolve by itself or by manual control.

### Step 6 — Re-check Before Fix

If the user selects Fix, the automation does **not** blindly replay the original decision.

It checks the current light state and current sun elevation again.

For example, if the user responds to a Night + OFF notification much later, the automation only turns the light ON if it is still below the configured sun-elevation threshold and the light is still OFF.

### Step 7 — Keep

If Keep is selected, the automation does not change the light. It only clears the notification.

Because the template trigger needs a new false-to-true transition, the same continuously true mismatch does not repeatedly trigger immediately.

### Step 8 — Automatic Resolution

If the light or sun condition resolves the mismatch while the notification is waiting, the notification is cleared and no control command is sent.

## Restart and Reload Behavior

Like other Home Assistant triggers using `for:`, the elapsed mismatch timer does not survive a Home Assistant restart or automation reload. If the mismatch still exists after restart, the duration is counted again from the restored tracking state.

## Why This Is Separate from Dusk to Dawn

The separation is intentional:

- Dusk to Dawn performs scheduled control.
- Abnormal State Alert supervises exceptions while respecting a manual decision.

Keeping those responsibilities separate prevents the watchdog from automatically undoing a user choice.

## Safe Live-Test Checklist

1. Create a test instance with a test light.
2. Set Mismatch Duration to five minutes.
3. Create a mismatch appropriate to the current sun elevation.
4. Confirm the notification arrives.
5. Test Keep and verify that the light does not change.
6. Test Fix and verify that it acts only while the current conditions still justify the correction.
7. Manually resolve the mismatch while the notification is visible and verify that the notification clears without another change.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/lighting/outside_light_attention.yaml
```

[![Import Outdoor Light Alert](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_light_attention.yaml)
