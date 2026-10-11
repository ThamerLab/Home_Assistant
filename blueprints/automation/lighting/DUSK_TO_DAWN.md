# 🌙 Outdoor Lights — Dusk to Dawn

<p align="center">
  <img src="../../../assets/outdoor-dusk-dawn.svg" alt="Outdoor Lights Dusk to Dawn" width="100%">
</p>

This Blueprint controls an outdoor light when **sun elevation crosses** a user-selected threshold. It does not use a fixed clock time.

## Inputs

| Input | Default | Purpose |
|---|---:|---|
| Outdoor Light | — | The `light` entity to control |
| Sun Elevation Threshold | 5° | The elevation boundary between dusk and dawn actions |
| Notification Devices | None | Optional Companion App devices for command-failure alerts |

## Step-by-Step Execution

### Step 1 — Dusk Trigger

The automation watches the `elevation` attribute of `sun.sun`.

When the value crosses from above the configured threshold to below it, the `dusk` trigger fires.

### Step 2 — Send ON

The automation calls `light.turn_on` for the selected outdoor light.

### Step 3 — Verify ON

It waits up to ten seconds for the selected light to report `on`.

If the state is confirmed, the dusk sequence ends successfully.

### Step 4 — Retry Once

If the first ON verification times out:

1. The automation waits five seconds.
2. It sends `light.turn_on` again.
3. It waits up to another ten seconds for `on`.

### Step 5 — Report Dusk Failure

If the second attempt still cannot be confirmed:

- A persistent notification is created.
- Each configured notification device receives a failure notification.

### Step 6 — Dawn Trigger

When sun elevation crosses from below the threshold to above it, the `dawn` trigger fires.

### Step 7 — Send OFF and Verify

The dawn path mirrors the dusk logic:

1. Send `light.turn_off`.
2. Wait up to ten seconds for `off`.
3. If needed, wait five seconds and retry once.
4. Verify `off` again.
5. Report a persistent/mobile failure if the second attempt is not confirmed.

## Why There Is No Startup Trigger

This is intentional.

If the automation turns the light ON at night and the user later turns it OFF manually, a Home Assistant restart should not immediately reverse that decision.

The same principle applies during the day: if the user manually turns the light ON after the morning OFF action, startup does not force it OFF again.

The automation acts only when sun elevation **crosses** the configured boundary again.

## Manual Priority

This design gives the user practical manual priority between sun-boundary events:

- Scheduled ON at dusk → user turns it OFF → it stays OFF.
- Scheduled OFF at dawn → user turns it ON → it stays ON.

If you want to be notified about those unusual states without forcing a correction, pair this Blueprint with [Outdoor Light — Abnormal State Alert](./ABNORMAL_STATE_ALERT.md).

## Limits

- A numeric-state trigger reacts to crossing the threshold, not merely to Home Assistant starting while the sun is already above or below it.
- Correct behavior depends on Home Assistant location and timezone configuration.
- A reported `on` or `off` state comes from the integration and is not a physical light sensor measurement.

## Safe Live-Test Checklist

1. Use a test light when possible.
2. Choose a threshold near the current sun elevation or use a controlled test configuration.
3. Confirm the first state change.
4. Review the automation trace.
5. Test a non-responsive device in a safe setup to verify retry and failure notifications.
6. Only after testing should you apply the Blueprint to the production outdoor light.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/lighting/outside_lights_dusk_dawn.yaml
```

[![Import Dusk to Dawn](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Flighting%2Foutside_lights_dusk_dawn.yaml)
