# 🌱 Smart Irrigation — Detailed Guide

<p align="center">
  <img src="../../../assets/irrigation.svg" alt="Smart Irrigation Blueprint" width="100%">
</p>

This Blueprint controls one or more irrigation valves that appear in Home Assistant as `switch` entities. Its purpose is not merely to run a timer. It adds verification before, during, and after the irrigation cycle.

## What It Does

It supports three schedule modes:

1. **Sunrise & Sunset** — runs at both sunrise and sunset.
2. **Custom Time** — runs once per day at a user-selected time.
3. **Fixed Clock Interval** — runs at evenly spaced clock hours anchored to local midnight.

It also provides:

- Startup verification for every selected valve.
- Optional blocking when a selected valve is already ON before the scheduled run.
- Flow validation after the first minute.
- Immediate shutdown when any selected flow sensor fails the configured no-flow check.
- Detection of an early/manual valve shutdown.
- A final OFF command for every selected valve.
- Verification that every valve reports OFF.
- Optional Companion App notifications.
- An estimated water-usage calculation from the sampled flow rate.

## Inputs

| Input | Required | Default | Purpose |
|---|---:|---:|---|
| Irrigation Valves | Yes | — | One or more `switch` entities controlled by the automation. |
| Irrigation Duration | Yes | 5 min | Total scheduled runtime. |
| Schedule Mode | Yes | Sunrise & Sunset | Selects the scheduling model. |
| Custom Time | Conditional | 06:00 | Used only in Custom Time mode. |
| Fixed Clock Interval | Conditional | 6 hours | Used only in Repeat mode. |
| Flow Sensors | No | None | Optional flow sensors, expected in m³/h. |
| Stop If No Flow | No | Enabled | Requires every selected flow sensor to report a positive numeric value after one minute. |
| Do Not Start If Already ON | No | Enabled | Prevents the automation from taking control of a pre-existing manual/other run. |
| Valve Startup Verification | No | 10 sec | Maximum time allowed for all selected valves to report ON. |
| Notification Devices | No | None | Companion App devices for notifications. |
| Enable Notifications | No | Enabled | Enables or disables mobile notifications. |

## Step-by-Step Execution

### Step 1 — Select the Valid Trigger

The Blueprint contains triggers for sunrise, sunset, the custom time, and an hourly repeat check. A template condition allows only the trigger that belongs to the selected schedule mode.

For **Fixed Clock Interval**, available values are limited to:

`1, 2, 3, 4, 6, 8, 12, 24`

These values divide 24 hours evenly. For example, every six hours runs at 00:00, 06:00, 12:00, and 18:00.

### Step 2 — Check for a Pre-Existing ON Valve

When **Do Not Start If Any Valve Is Already ON** is enabled, the automation expands every selected switch and checks its current state.

If any selected valve is already ON:

- No new valve is turned on.
- A persistent notification is created.
- A mobile notification is sent if notification devices are configured.
- The automation stops.

This prevents a scheduled run from taking ownership of a valve that was already running manually or from another automation.

### Step 3 — Send the ON Command

The automation calls:

`switch.turn_on`

for all selected irrigation valves.

### Step 4 — Verify Startup

The automation waits until every selected valve reports `on`, up to the configured startup verification timeout.

If startup cannot be confirmed:

- It sends `switch.turn_off` to all selected valves as a precaution.
- It creates a persistent notification.
- It sends an optional mobile failure notification.
- It stops the run.

The automation therefore does not treat a successful service call as proof that the hardware actually entered the expected state.

### Step 5 — Send the Start Notification

A start notification is sent only after startup verification succeeds.

### Step 6 — Wait for the First Minute

The automation waits one minute before sampling flow.

This minute is part of the requested irrigation duration; it is not added on top of it.

### Step 7 — Confirm That All Valves Are Still ON

After the first minute, the automation checks every selected valve again.

If any valve is no longer ON:

- It sends OFF to every selected valve.
- It optionally sends an early-stop notification.
- It stops the run.

### Step 8 — Validate Flow

When flow sensors are selected and no-flow protection is enabled:

- Every selected flow sensor is read.
- An unavailable or non-numeric value is treated as a failure.
- A value of zero or below is treated as a failure.
- If any selected sensor fails, all selected valves are turned OFF and the run stops.

This design is intentionally stricter than checking only the combined flow. One healthy branch cannot hide a failed branch.

### Step 9 — Monitor the Remaining Runtime

If time remains after the first minute, the automation waits for either:

- The remaining duration to expire.
- Any selected valve to transition from `on` to `off`.

If any selected valve turns OFF early, all remaining valves are turned OFF and the run ends as an early/manual shutdown.

### Step 10 — End the Scheduled Cycle

When the requested duration expires, the automation sends:

`switch.turn_off`

to every selected valve.

### Step 11 — Verify Final OFF State

The automation waits up to 15 seconds for every selected valve to report `off`.

If any valve does not confirm OFF:

- The run is not reported as successful.
- A persistent notification is created.
- An optional mobile failure notification is sent.
- The user is instructed to check the irrigation system.

### Step 12 — Estimate Water Usage

If flow sensors were selected, the automation uses the combined one-minute flow sample:

```text
Estimated m³ = sampled total flow (m³/h) × duration (hours)
Estimated liters = Estimated m³ × 1000
```

This is an **estimate**, not a true integrated water meter.

## Restart Behavior

If Home Assistant restarts while an automation is actively waiting or delaying, the active run is interrupted.

For real water hardware, this Blueprint should therefore not be treated as the only safety layer. Use it with:

- [Long-running Water Safety Watchdog](./WATER_SAFETY.md)
- A device-side auto-close feature when available.
- Independent flow monitoring when appropriate.

## Failure Cases Covered

| Situation | Result |
|---|---|
| A selected valve is already ON before start | Scheduled run is skipped |
| A selected valve never confirms ON | All selected valves receive OFF and the run fails |
| A selected valve turns OFF during the first minute | Remaining valves are turned OFF |
| A selected flow sensor is unavailable or not positive | All selected valves are turned OFF |
| A selected valve turns OFF before the scheduled end | Remaining valves are turned OFF |
| Final OFF state is not confirmed | Failure notification; no success claim |

## What This Blueprint Cannot Prove

- A Home Assistant `off` state does not physically prove that water flow stopped.
- The estimated liters value is not a billing-grade measurement.
- A Home Assistant restart can interrupt an active sequence.
- Flow-sensor accuracy depends on the device, firmware, and integration.

## Safe Live-Test Checklist

1. Create a test instance with a one-minute duration.
2. Use a valve you can physically observe.
3. Confirm that it turns ON and then OFF.
4. Manually turn the valve OFF during the run and verify early-stop handling.
5. If flow sensors are configured, verify that each selected sensor reports a positive value during real flow.
6. Test the no-flow path under supervision.
7. Only after those checks pass should you enable the production runtime and schedule.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/irrigation/smart_irrigation.yaml
```

[![Import Smart Irrigation](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Firrigation%2Fsmart_irrigation.yaml)
