# 💧 Manual Irrigation — Safe Timed Run

<p align="center">
  <img src="../../../assets/manual-irrigation.svg" alt="Safe Manual Irrigation Script" width="100%">
</p>

This Script Blueprint runs one or more irrigation valves manually for a duration selected **each time the script is started**. It follows the same core safety philosophy as Smart Irrigation: verify startup, optionally validate flow, detect early shutdown, send a final OFF command, and verify OFF state.

## Difference from Smart Irrigation

- Smart Irrigation starts from a schedule.
- Manual Irrigation starts when the user runs the script.
- The **Duration** field is requested for each script run.

## Inputs When Creating the Script

| Input | Purpose |
|---|---|
| Irrigation Valves | Switches controlled by the script |
| Flow Sensors | Optional flow sensors, expected in m³/h |
| Stop If Any Selected Flow Sensor Has No Flow | Enables strict per-sensor no-flow protection |
| Do Not Start If Already ON | Prevents taking over a pre-existing run |
| Valve Startup Verification | Maximum time allowed for all selected valves to confirm ON |
| Notification Devices | Optional Companion App devices |

## Runtime Field

**Duration:** 1 to 120 minutes, default 10.

## Step-by-Step Execution

### Step 1 — Read the Requested Runtime

The script reads the Duration field provided for the current run.

### Step 2 — Check for a Pre-Existing ON Valve

If blocking is enabled and any selected valve is already ON:

- The script does not take control of the valve.
- A persistent notification is created.
- Optional mobile notifications are sent.
- The script stops.

### Step 3 — Turn All Selected Valves ON

The script sends `switch.turn_on` to every selected irrigation valve.

### Step 4 — Verify Startup

The script waits up to the configured startup-verification timeout for all selected valves to report `on`.

If startup cannot be confirmed:

- OFF is sent to every selected valve.
- A failure notification is created.
- The script stops.

### Step 5 — Wait One Minute

The first minute allows the irrigation system and flow sensors to stabilize.

This minute is included in the requested runtime.

### Step 6 — Confirm Valves Are Still ON

If any selected valve has turned OFF during the first minute:

- OFF is sent to the remaining selected valves.
- An early-stop notification is sent.
- The script stops.

### Step 7 — Validate Flow

When flow protection is enabled and sensors are selected:

- Every selected flow sensor must provide a positive numeric reading.
- Unavailable, non-numeric, zero, or negative values fail the check.
- Any failed sensor causes all selected valves to receive OFF.

### Step 8 — Monitor the Remaining Runtime

The script waits for either:

- The requested runtime to expire.
- Any selected valve to transition from `on` to `off`.

An early OFF state is treated as a manual or unexpected stop and causes the remaining valves to be turned OFF.

### Step 9 — Final Shutdown

At the end of the requested runtime, OFF is sent to every selected valve.

### Step 10 — Verify OFF

The script waits up to 15 seconds for every selected valve to report `off`.

If shutdown cannot be confirmed:

- A persistent failure notification is created.
- Optional mobile notifications are sent.
- The script does not claim successful completion.

### Step 11 — Report Completion

If shutdown is confirmed, the script sends an optional completion notification.

When flow sensors are configured, it also reports an estimated water usage based on the sampled flow rate.

## Water Usage Estimate

The estimate is:

```text
Estimated liters =
  sampled total flow (m³/h)
  × runtime in hours
  × 1000
```

This is an estimate, not a true integrated water-meter value.

## Restart Limitation

If Home Assistant restarts while the script is waiting or delaying, the active sequence is interrupted and the final OFF step is not guaranteed to run.

For real irrigation hardware, pair this script with:

- [Long-running Water Safety Watchdog](../../automation/irrigation/WATER_SAFETY.md)
- Device-side auto-close when available.

## Safe Live-Test Checklist

1. Import the script Blueprint.
2. Select a supervised test valve or a valve you can physically observe.
3. Run it for one minute.
4. Confirm ON and final OFF behavior.
5. Manually turn one valve OFF during a test run and confirm that remaining valves are stopped.
6. Test the flow-failure path under supervision.
7. Do not rely on long unattended runs until all checks pass.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/script/irrigation/manual_irrigation_safe_run.yaml
```

[![Import Manual Irrigation](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fscript%2Firrigation%2Fmanual_irrigation_safe_run.yaml)
