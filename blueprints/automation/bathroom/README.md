# 🚿 Bathroom Occupancy — Lights & Exhaust Fan

<p align="center">
  <img src="../../../assets/bathroom-occupancy.svg" alt="Bathroom Occupancy Lights and Exhaust Fan" width="100%">
</p>

File: `bathroom_occupancy_lights_fan.yaml`

This Blueprint controls bathroom lighting and an exhaust fan from one or more occupancy/motion sensors while protecting **pre-existing manual states**.

The core design uses two dedicated `input_boolean` helpers as ownership flags:

- One helper records whether this automation started the bathroom lights.
- One helper records whether this automation started the exhaust fan.

That ownership survives a restarted automation run and a Home Assistant restart because the helpers are real Home Assistant entities, not temporary variables.

## Why Ownership Helpers Are Required

A simple motion automation usually does this:

1. Motion turns a light/fan ON.
2. Motion ends.
3. A delay runs.
4. The automation turns everything OFF.

The problem is that step 4 cannot tell whether the automation originally turned the device ON or whether the user had already turned it ON manually.

This Blueprint avoids that problem.

If the light or fan is already ON before the occupancy event, the corresponding ownership helper stays OFF. That means the vacancy branch is not allowed to turn that device class OFF.

## Recommended Helpers

Create two Toggle helpers before creating the automation:

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

Use dedicated helpers for each Blueprint instance. Do not share the same ownership helper between different bathrooms.

## Inputs

| Input | Default | Purpose |
|---|---:|---|
| Occupancy / Motion Sensors | — | One or more binary sensors; any ON means occupied |
| Bathroom Lights | — | One or more light entities |
| Exhaust Fan | — | One or more fan/switch entities |
| Light Ownership Helper | — | Dedicated input_boolean for light ownership |
| Fan Ownership Helper | — | Dedicated input_boolean for fan ownership |
| Light Off Delay | 90 sec | Continuous vacancy time before automation-owned lights are turned OFF |
| Fan Off Delay | 420 sec | Continuous vacancy time before an automation-owned fan is turned OFF |
| Startup Verification | 10 sec | Time allowed for automation-started devices to report ON |
| Shutdown Verification | 15 sec | Time allowed for automation-owned devices to report OFF |

## Step-by-Step Execution

### Step 1 — Occupancy Starts

Any selected occupancy/motion sensor changing from OFF to ON triggers the `occupied` branch.

Because the Blueprint uses `mode: restart`, new occupancy immediately cancels any pending vacancy-off delays.

The ownership helpers are not lost when the automation restarts.

### Step 2 — Reconcile a Stale Light Ownership Helper

If the light ownership helper says ON but every selected bathroom light is actually OFF, the helper is stale.

The Blueprint turns the helper OFF before deciding whether it should start the lights.

This can happen after a manual OFF action or after an interrupted previous cycle.

### Step 3 — Decide Whether the Automation May Own the Lights

The automation starts the selected lights only when:

- Light ownership is currently OFF.
- Every selected light is currently OFF.

If any selected light is already ON, the automation assumes that state is pre-existing/manual and does not claim ownership.

### Step 4 — Start and Verify the Lights

When the automation is allowed to start the lights:

1. It sends `light.turn_on`.
2. It waits up to the Startup Verification timeout.
3. Every selected light must report ON.
4. Only after successful verification does the Light Ownership Helper turn ON.

If startup cannot be confirmed:

- OFF is sent to the selected lights as a precaution.
- Light ownership is cleared.
- A persistent notification explains the startup failure.

### Step 5 — Reconcile Fan Ownership

The same ownership logic is applied independently to the exhaust fan.

If the fan ownership helper is ON while every selected fan target is OFF, the helper is cleared as stale.

### Step 6 — Decide Whether the Automation May Own the Fan

The fan is started only when:

- Fan ownership is OFF.
- Every selected fan/switch target is OFF.

If the exhaust fan was already running manually, the automation does not claim ownership and therefore will not later turn that manually running fan OFF.

### Step 7 — Start and Verify the Fan

The Blueprint uses `homeassistant.turn_on` so both `fan` and `switch` entities can be controlled.

It waits for every selected target to report ON before setting the Fan Ownership Helper to ON.

A failed startup causes a precautionary OFF command, ownership clear, and persistent failure notification.

### Step 8 — A Sensor Changes to OFF

Any selected sensor changing from ON to OFF starts the vacancy branch.

This does not immediately mean the bathroom is empty because other selected sensors may still be ON.

The two shutdown timers run in parallel:

- Light delay branch.
- Fan delay branch.

### Step 9 — Light Vacancy Delay

After the configured Light Off Delay:

1. The Blueprint confirms that **all** occupancy sensors are OFF.
2. It confirms that Light Ownership is ON.
3. Only then does it send OFF to the selected lights.

If another occupancy sensor becomes ON during the delay, `mode: restart` cancels the pending shutdown immediately.

### Step 10 — Verify Light Shutdown

After sending OFF, the Blueprint waits up to the Shutdown Verification timeout.

If every light reports OFF:

- The Light Ownership Helper is cleared.

If shutdown is not confirmed:

- A persistent notification is created.
- Light ownership deliberately remains ON so a later vacancy cycle can attempt shutdown again.

### Step 11 — Fan Vacancy Delay

The fan branch runs independently using the longer Fan Off Delay.

After the delay:

1. All occupancy sensors must still be OFF.
2. Fan Ownership must still be ON.
3. OFF is sent only to the fan entities owned by the automation.

### Step 12 — Verify Fan Shutdown

The Blueprint waits for every selected fan/switch target to report OFF.

On success:

- Fan Ownership is cleared.

On failure:

- A persistent notification is created.
- Fan Ownership remains ON for a later retry opportunity.

## What Happens If Motion Returns During an Off Delay?

This is the reason the Blueprint uses `mode: restart`.

When any sensor turns ON:

- The vacancy run is cancelled immediately.
- Pending light/fan OFF delays are cancelled.
- Ownership helpers remain ON.
- The new occupancy run sees that the automation already owns those devices and does not reset ownership.

The devices therefore stay ON while occupancy has returned.

## Manual Override Behavior

### Manual ON Before Occupancy

If a selected light or fan is already ON before the occupancy event:

- The automation does not turn that class ON.
- The ownership helper remains OFF.
- The vacancy branch is not allowed to turn that class OFF.

This is the primary manual-override protection.

### Manual OFF During an Automation-owned Cycle

If the user manually turns an automation-owned device OFF, the helper may temporarily remain ON until the next occupancy event reconciles a fully-OFF target set or a successful vacancy shutdown clears the helper.

The Blueprint intentionally does not use state-change triggers on the controlled devices themselves because doing so can create feedback loops with its own ON/OFF commands.

### Multiple Targets in One Class

Ownership is tracked per class, not per individual entity.

For the clearest behavior:

- Use one logical light/group for the bathroom when practical.
- Use one logical fan/switch group when multiple fan targets should behave as one unit.

If one entity in a multi-entity class is manually ON before occupancy, the Blueprint does not claim that class.

## Why the Fan Delay Is Longer

Bathroom exhaust fans often need to continue running after a person leaves.

The default timing is:

- Light: 90 seconds after full vacancy.
- Fan: 420 seconds (7 minutes) after full vacancy.

Both are configurable.

## Why Humidity Is Not Included in This Version

Humidity control is intentionally kept separate from the first production version.

Mixing occupancy ownership, manual override, humidity hysteresis, and post-run timing in one initial Blueprint would make failure behavior harder to reason about.

A dedicated humidity-aware extension can be added later and tested independently.

## Restart Behavior

The ownership helpers persist through Home Assistant restart.

However, an in-progress delay does not continue across restart. After restart:

- Ownership information is preserved.
- A new sensor state transition is still required to start a new run.

For critical ventilation requirements, do not rely on Home Assistant alone.

## Failure Cases Covered

| Situation | Result |
|---|---|
| Light already ON before occupancy | Light is treated as manual; automation does not own or turn it OFF |
| Fan already ON before occupancy | Fan is treated as manual; automation does not own or turn it OFF |
| Light startup not confirmed | Precautionary OFF, ownership cleared, persistent failure notification |
| Fan startup not confirmed | Precautionary OFF, ownership cleared, persistent failure notification |
| Occupancy returns during off delay | Pending OFF sequence is cancelled |
| Light shutdown not confirmed | Failure notification; ownership retained for retry |
| Fan shutdown not confirmed | Failure notification; ownership retained for retry |
| Multiple occupancy sensors disagree | Bathroom is considered occupied until all selected sensors are OFF |

## 100-case Logic Test

The repository includes:

`tests/test_bathroom_logic.py`

It runs 100 deterministic ownership/vacancy scenarios and checks the core invariants:

- Pre-existing manual light state is never turned OFF by the automation.
- Pre-existing manual fan state is never turned OFF by the automation.
- Automation-owned devices remain ON if occupancy returns before the off delay.
- Automation-owned devices turn OFF after a complete vacancy cycle.
- Light and fan ownership remain independent.

This test is run in CI in addition to the normal repository validator and Home Assistant `check_config`.

## Safe Live-Test Checklist

1. Create two dedicated Toggle helpers.
2. Create the automation from this Blueprint.
3. Set Light Off Delay to 10 seconds and Fan Off Delay to 20 seconds for the first test.
4. Enter the bathroom and confirm both devices start.
5. Leave and confirm light OFF at 10 seconds and fan OFF at 20 seconds.
6. Repeat, but re-enter before the light delay expires; confirm neither device turns OFF.
7. Repeat, re-enter after the light turns OFF but before the fan delay expires; confirm the light turns back ON and the fan remains ON.
8. Manually turn the light ON before entering; confirm the automation does not turn it OFF after vacancy.
9. Manually turn the fan ON before entering; confirm the automation does not turn it OFF after vacancy.
10. Review the Home Assistant automation trace for each test.
11. Restore production delays only after all supervised tests pass.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/bathroom/bathroom_occupancy_lights_fan.yaml
```

[![Import Bathroom Occupancy](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fbathroom%2Fbathroom_occupancy_lights_fan.yaml)
