# 🚨 Long-running Water Safety Watchdog — Detailed Guide

<p align="center">
  <img src="../../../assets/water-safety.svg" alt="Long-running Water Safety Watchdog" width="100%">
</p>

This Blueprint is an independent safety layer for water or irrigation devices exposed as `switch` entities. It does not start irrigation on its own. It watches for unexpectedly long ON periods and asks the user whether to stop or keep the water running.

## Purpose

If any selected switch remains `on` longer than the configured threshold:

- A critical notification is sent.
- The notification offers **Stop all** and **Keep running**.
- Stop all sends OFF to every selected switch and verifies the reported OFF state.
- Keep running creates a temporary snooze period.
- If all switches are turned OFF manually while the notification is visible, the notification is cleared.

## Inputs

| Input | Default | Purpose |
|---|---:|---|
| Water / Irrigation Switches | — | One or more switches to monitor |
| Alert After | 10 min | How long a switch may remain ON before the warning |
| Snooze After Keep Running | 30 min | Suppresses new warnings after the user deliberately keeps water running |
| Notification Tag | long_running_water | Allows multiple watchdog instances to use separate notification threads |
| Device to Notify | — | Companion App device that receives the actionable notification |

## Step-by-Step Execution

### Step 1 — Trigger Paths

The Blueprint can start from three trigger paths:

1. A selected switch stays ON for the configured threshold.
2. A five-minute periodic watchdog runs.
3. Home Assistant starts.

The periodic watchdog and startup path exist because Home Assistant does not preserve a state-trigger `for:` timer through restart or automation reload.

### Step 2 — Confirm Long-running State

For the direct state trigger, the configured ON duration has already been satisfied.

For the watchdog and startup paths, the automation:

- Expands all selected switches.
- Checks which are currently ON.
- Calculates the age of the current ON state from `last_changed`.
- Continues only when at least one selected switch appears to have exceeded the configured threshold.

### Step 3 — Create Unique Action IDs

Each automation run creates action IDs derived from `context.id`:

- `WATER_STOP_<context.id>`
- `WATER_KEEP_<context.id>`

This prevents an old notification button from accidentally controlling a newer automation run.

### Step 4 — Send the Critical Notification

The notification lists each selected switch that is still ON and shows its approximate ON duration.

It provides:

- 🛑 **Stop all**
- 💧 **Keep running**

A configurable notification tag is used so a newer warning can replace the older warning from the same Blueprint instance.

### Step 5 — Wait for the User or for Manual Resolution

The automation waits up to five minutes for one of the following:

- Stop all.
- Keep running.
- All selected switches become OFF on their own or by manual control.

### Step 6 — Stop All Path

If Stop all is selected:

1. OFF is sent to every selected switch.
2. The automation waits up to 15 seconds.
3. Success requires every selected switch to report `off`.
4. The original warning is cleared.
5. A confirmation is sent if shutdown is confirmed.
6. If shutdown cannot be confirmed, a new critical failure notification is sent.

The automation therefore does not equate a completed service call with a confirmed shutdown.

### Step 7 — Keep Running Path

If Keep running is selected:

1. The original warning is cleared.
2. A confirmation message is sent.
3. The automation waits for the configured snooze duration.

Because the Blueprint uses `mode: single`, the snooze period intentionally prevents duplicate warnings during that period.

After the snooze ends, the periodic watchdog can alert again if a selected switch is still ON.

### Step 8 — Manual OFF Path

If all selected switches become OFF while the action notification is waiting, the notification is cleared and no additional control command is sent.

### Step 9 — No Response

If the five-minute action wait expires without a response, the warning is intentionally not cleared. A future watchdog run can replace it using the same notification tag if the condition still exists.

## Restart and Reload Limitations

The direct state-trigger `for:` timer does not survive Home Assistant restart or automation reload.

The startup and periodic watchdog reduce this risk, but they do not provide perfect persistence. If a device or integration restores the entity state with a new `last_changed` timestamp after startup, the automation cannot reconstruct the exact pre-restart ON duration.

For safety-critical water hardware, consider additional independent protection:

- Device-side auto-close.
- Independent flow monitoring.
- A mechanical shutoff strategy appropriate to the installation.

## Critical Notification Notes

The Blueprint sends the critical-notification payload used by the Home Assistant Companion App. Actual critical-alert behavior also depends on the mobile operating system and the permissions granted to the app.

## What Is Verified

The Blueprint verifies that Home Assistant sees all selected switches as `off`.

It **cannot** prove by switch state alone that water has physically stopped. Physical confirmation requires an independent flow or position signal.

## Safe Live-Test Checklist

1. Use a test switch or a supervised valve.
2. Set Alert After to five minutes.
3. Wait for the actionable notification.
4. Test Keep running and confirm the snooze behavior.
5. Test again and select Stop all.
6. Verify both Home Assistant state and the physical water result.
7. If possible, test an unavailable-device scenario to confirm that shutdown failure produces a critical warning.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/irrigation/long_running_water_safety.yaml
```

[![Import Water Safety Watchdog](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Flong_running_water_safety.yaml)
