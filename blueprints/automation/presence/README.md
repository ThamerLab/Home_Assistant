# 📍 Zone Exit Notification — Detailed Guide

<p align="center">
  <img src="../../../assets/zone-notification.svg" alt="Zone Exit Notification Blueprint" width="100%">
</p>

This Blueprint sends a notification when a selected `person` entity leaves a selected `zone`.

Its core logic is based on Home Assistant's official built-in **Zone Notification** Blueprint. The YAML file preserves attribution to the upstream Home Assistant project.

## Purpose

Use this Blueprint when you already have a Person entity and a Zone configured in Home Assistant and want a notification when that Person leaves the Zone.

The Blueprint does **not** create location tracking by itself. It only reacts to state changes from an existing Home Assistant Person entity.

## Inputs

| Input | Purpose |
|---|---|
| Person | Existing `person.*` entity |
| Zone | Existing `zone.*` entity |
| Device to notify | Companion App device that receives the notification |

## Step-by-Step Execution

### Step 1 — Watch the Person State

Any state change of the selected Person triggers the automation.

### Step 2 — Resolve the Zone State

The automation reads the selected zone and stores its display name in `zone_state`.

### Step 3 — Confirm That the Person Actually Left

The automation does not notify on every Person state change.

For the Home zone:

- The previous state must be `home`.
- The new state must not be `home`.

For any other zone:

- The previous state must match the selected zone name.
- The new state must differ from that zone name.

### Step 4 — Send the Notification

The selected Companion App device receives a message containing the person's display name and the zone that was left.

## Example Setup

1. Configure an appropriate Device Tracker.
2. Link it to a Home Assistant Person entity.
3. Import this Blueprint.
4. Select the Person.
5. Select the Zone.
6. Select the phone that should receive notifications.
7. Save the automation.
8. Test a real or controlled zone exit and review the automation trace.

## Accuracy and Timing

This Blueprint does not determine location accuracy. Notification timing depends on:

- The tracked device.
- Location permissions.
- Background location behavior.
- GPS, Wi-Fi, and cellular positioning.
- Zone radius.
- Device Tracker update frequency.
- How quickly the integration reports changes to Home Assistant.

A delayed tracker update can therefore produce a delayed zone-exit notification.

## Privacy

- Use location tracking only with appropriate consent.
- Do not publish person names, device IDs, or private location data in a public repository.
- Keep Person and Device Tracker configuration inside the private Home Assistant instance.

## Safe Live-Test Checklist

1. Create a test zone or use an existing zone.
2. Confirm that the selected Person currently appears inside that zone.
3. Perform a controlled exit.
4. Review the automation trace.
5. Confirm that `from_state` represented the selected zone and `to_state` represented a different state.
6. Confirm that the notification arrives on the selected device.
7. Adjust tracker or zone settings if the location update is too slow or inaccurate.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/presence/notify_leaving_zone.yaml
```

[![Import Zone Exit Notification](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fnotify_leaving_zone.yaml)

## Upstream Source

Home Assistant Core built-in `notify_leaving_zone.yaml`.  
Copyright Home Assistant contributors; Apache License 2.0.
