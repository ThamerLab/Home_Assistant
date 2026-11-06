# 🚿 Bathroom Occupancy — Lights & Exhaust Fan

<p align="center">
  <img src="../../../assets/bathroom-occupancy.svg" alt="Bathroom Occupancy Lights and Exhaust Fan" width="100%">
</p>

File: `bathroom_occupancy_lights_fan.yaml`

This Blueprint is designed as a long-term bathroom automation rather than a fixed one-off rule. Every important timing value is configurable from the Blueprint UI, and manual ON states can use one of three behaviors.

## Design Goals

- One or more occupancy/motion sensors.
- Independent light and fan logic.
- Optional automatic light ON.
- Optional automatic fan ON.
- Configurable light ON delay.
- Configurable fan ON delay.
- Configurable light OFF delay.
- Configurable fan OFF delay.
- Configurable maximum manual light hold.
- Configurable maximum manual fan hold.
- Configurable startup and shutdown verification timeouts.
- Three manual-ON policies for each device class.
- Persistent ownership helpers so the automation knows what it started itself.

## Required Ownership Helpers

Create two dedicated Toggle helpers before creating the automation:

```text
Settings
→ Devices & services
→ Helpers
→ Create helper
→ Toggle
```

Recommended names:

- Bathroom Light Automation Ownership
- Bathroom Fan Automation Ownership

Use dedicated helpers for each bathroom automation instance.

The helper is ON only when this automation started that device class. If a device was already ON before the automation claimed it, the helper remains OFF and the state is treated as manual.

## Inputs

| Input | Default | Purpose |
|---|---:|---|
| Occupancy / Motion Sensors | — | Any ON = occupied; all OFF = vacant |
| Bathroom Lights | — | Light entities controlled by the Blueprint |
| Exhaust Fan | — | Fan or switch entities used for ventilation |
| Light Ownership Helper | — | Records automation ownership of the lights |
| Fan Ownership Helper | — | Records automation ownership of the fan |
| Automatically Turn On Lights | ON | Allows occupancy to start lights |
| Automatically Turn On Fan | ON | Allows occupancy to start fan |
| Light ON Delay | 0 sec | How long occupancy must remain active before lights start |
| Fan ON Delay | 0 sec | How long occupancy must remain active before fan starts |
| Light OFF Delay | 90 sec | Vacancy delay for automation-owned lights |
| Fan OFF Delay | 420 sec | Vacancy delay for automation-owned fan |
| Manual Light ON Behavior | Timed Hold | Policy for manually pre-started lights |
| Manual Fan ON Behavior | Timed Hold | Policy for manually pre-started fan |
| Maximum Manual Light Hold | 1800 sec | Maximum vacant hold for manual lights |
| Maximum Manual Fan Hold | 3600 sec | Maximum vacant hold for manual fan |
| Startup Verification | 10 sec | Time allowed for automation-started devices to confirm ON |
| Shutdown Verification | 15 sec | Time allowed for controlled devices to confirm OFF |
| Home Assistant Startup Reconcile Delay | 30 sec | Wait after HA startup before restarting vacancy/manual-hold protection |

## Manual ON Behaviors

Each device class has its own independent policy.

### Timed Hold — Recommended

Manual ON is treated as a temporary occupancy hold.

When the bathroom becomes fully vacant:

1. The manual-hold timer starts.
2. The device remains ON during that hold.
3. If occupancy returns, `mode: restart` cancels the pending shutdown.
4. If the bathroom remains vacant until the maximum hold expires, the device is turned OFF.
5. Shutdown is verified.

This is the recommended mode when you want manual control but do not want a forgotten light or fan to remain ON indefinitely.

### Normal Vacancy Delay

A manually pre-started device is allowed to stay ON only for the same normal vacancy delay used by automation-owned devices.

Example:

- Light OFF Delay = 90 sec.
- Manual Light ON Behavior = Normal Vacancy Delay.
- A manually pre-started light will turn OFF after 90 seconds of continuous vacancy.

### Keep On

A manually pre-started device is never turned OFF by this automation.

Use this only when the user's manual ON decision must always remain authoritative until the user turns the device OFF manually.

## Step-by-Step Execution

### Step 1 — Aggregate Occupancy Starts

The Blueprint does not trigger independently on every sensor edge.

It uses an aggregate template:

- **Occupied** becomes true when any selected sensor is ON.
- **Vacant** becomes true only when every selected sensor is OFF.

This is important with multiple sensors. One sensor turning OFF while another remains ON does not restart or cancel the active occupied sequence.

Because the Blueprint uses `mode: restart`, a true transition back to aggregate Occupied cancels any pending vacancy shutdown sequence.

### Step 2 — Optional Light ON Delay

If automatic light ON is enabled, the automation waits the configured Light ON Delay.

After the delay, at least one occupancy sensor must still be ON.

If occupancy ended during the delay, the light is not started.

### Step 3 — Light Ownership Decision

If every selected light is OFF and the automation does not currently own the lights:

1. Light ownership is set ON **before** the ON command.
2. The lights are turned ON.
3. The automation waits for ON-state verification.
4. If startup fails, OFF is sent as a precaution and ownership is released.

If a selected light was already ON before the automation claimed it, the automation does not claim ownership.

### Step 4 — Optional Fan ON Delay

The fan follows the same logic independently using Fan ON Delay.

This allows useful configurations such as:

- Lights immediately, fan immediately.
- Lights immediately, fan after 60 seconds.
- Lights automatic, fan manual only.
- Fan automatic, lights manual only.

### Step 5 — Full Vacancy Detection

A selected sensor changing OFF starts the vacancy branch only after the Blueprint confirms that **all** selected occupancy sensors are OFF.

Unknown or unavailable sensors are not treated as OFF, which prevents an automatic shutdown when occupancy status is uncertain.

### Step 6 — Automation-owned Light Shutdown

If Light Ownership is ON:

1. Wait Light OFF Delay.
2. Confirm the bathroom is still fully vacant.
3. Confirm Light Ownership is still ON.
4. Send Light OFF.
5. Verify every selected light is OFF.
6. Clear ownership only after successful verification.

If shutdown cannot be confirmed, ownership remains ON so a later vacancy cycle can retry.

### Step 7 — Manually Started Light Handling

If Light Ownership is OFF but one or more selected lights are ON, the selected Manual Light ON Behavior is applied:

- **Timed Hold:** wait Maximum Manual Light Hold.
- **Normal Vacancy Delay:** wait Light OFF Delay.
- **Keep On:** take no action.

Before any OFF command, the Blueprint confirms again that:

- All occupancy sensors are still OFF.
- Light Ownership is still OFF.
- At least one selected light is still ON.

### Step 8 — Automation-owned Fan Shutdown

If Fan Ownership is ON, the fan uses Fan OFF Delay, then follows the same re-check, OFF command, and verification pattern.

### Step 9 — Manually Started Fan Handling

If Fan Ownership is OFF while the fan is ON:

- **Timed Hold:** wait Maximum Manual Fan Hold.
- **Normal Vacancy Delay:** wait Fan OFF Delay.
- **Keep On:** take no action.

The fan policy is completely independent of the light policy.

## Useful Configuration Examples

### Fast Bathroom

- Light ON Delay: 0 sec
- Fan ON Delay: 0 sec
- Light OFF Delay: 60 sec
- Fan OFF Delay: 300 sec
- Manual modes: Timed Hold
- Manual Light Hold: 1200 sec
- Manual Fan Hold: 1800 sec

### Guest Bathroom

- Light ON Delay: 0 sec
- Fan ON Delay: 60 sec
- Light OFF Delay: 120 sec
- Fan OFF Delay: 600 sec
- Manual Light Hold: 1800 sec
- Manual Fan Hold: 3600 sec

### Fan Is Manual-only

- Automatically Turn On Lights: ON
- Automatically Turn On Fan: OFF
- Manual Fan ON Behavior: Timed Hold
- Maximum Manual Fan Hold: any preferred maximum

The automation will not start the fan from occupancy, but a manually pre-started fan can still be protected against being forgotten after vacancy.

## Important Manual-control Limit

Ownership is tracked per device class, not per individual light or fan entity.

For the cleanest behavior, group fixtures that should behave as one logical bathroom light or one logical fan target.

If the automation already owns a device and the user sends another ON command while it is already ON, Home Assistant may not provide enough information to reliably interpret that command as a new manual override. The Blueprint therefore bases ownership primarily on whether the class was already ON before automation ownership was established.

## Restart Behavior

Ownership helpers persist through Home Assistant restart, but active Home Assistant delays do not.

To recover safely, the Blueprint also has a Home Assistant startup trigger:

1. Wait the configurable **Home Assistant Startup Reconcile Delay**.
2. Check whether every occupancy sensor is OFF.
3. If the bathroom is fully vacant, re-run the normal vacancy logic.
4. Automation-owned devices resume their normal OFF-delay protection.
5. Manually pre-started devices resume the selected Manual ON policy and maximum hold protection.

If occupancy is active or uncertain after startup, no automatic shutdown occurs.

For ventilation that must be guaranteed independently of Home Assistant, use device-side or electrical controls appropriate to the installation.

## 100-case Logic Test

The repository runs:

`tests/test_bathroom_logic.py`

The test executes exactly 100 deterministic timing configurations covering combinations of:

- Manual light pre-state.
- Manual fan pre-state.
- Automatic light ON enabled/disabled.
- Automatic fan ON enabled/disabled.
- Timed Hold / Normal Vacancy / Keep On.
- Occupancy lasting or ending before ON delays.
- Occupancy returning before shutdown.
- Independent light and fan ownership.

It verifies the safety invariants before merge.

## Safe Live-Test Checklist

1. Create two dedicated ownership Toggle helpers.
2. Import the Blueprint.
3. For the first test, set Light ON Delay and Fan ON Delay to 0.
4. Set Light OFF Delay to 10 seconds and Fan OFF Delay to 20 seconds.
5. Set both Manual ON Behaviors to Timed Hold.
6. Set both manual maximum holds to 30 seconds.
7. Enter the bathroom and confirm the expected automatic starts.
8. Leave and confirm the configured OFF timing.
9. Re-enter during an OFF delay and confirm shutdown is cancelled.
10. Turn a device ON manually before occupancy and confirm the manual policy is used after vacancy.
11. Test Keep On and confirm the manually pre-started device remains ON.
12. Restore production timing values only after the supervised tests pass.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/bathroom/bathroom_occupancy_lights_fan.yaml
```

[![Import Bathroom Occupancy](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fbathroom%2Fbathroom_occupancy_lights_fan.yaml)
