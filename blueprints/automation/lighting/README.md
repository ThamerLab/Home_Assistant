# 🌙 Outdoor Lighting Blueprints

<p align="center">
  <img src="../../../assets/outdoor-dusk-dawn.svg" alt="Dusk to Dawn" width="49%">
  <img src="../../../assets/outdoor-alert.svg" alt="Abnormal State Alert" width="49%">
</p>

This section deliberately separates **scheduled control** from **exception monitoring**.

## 1. 🌙 Outdoor Lights — Dusk to Dawn

File: `outside_lights_dusk_dawn.yaml`

- Turns the light ON when sun elevation crosses below the selected threshold.
- Turns the light OFF when sun elevation crosses above the threshold.
- Verifies the requested state.
- Retries once if verification fails.
- Sends a failure notification if the second attempt still cannot be confirmed.
- Does not force a state during Home Assistant startup, preserving manual control.

[📖 Detailed guide](./DUSK_TO_DAWN.md)

## 2. 💡 Outdoor Light — Abnormal State Alert

File: `outside_light_attention.yaml`

- Detects night + OFF or day + ON mismatches.
- Requires the mismatch to persist for a configured duration.
- Sends Fix / Keep actions.
- Uses unique action IDs for every run.
- Re-checks the current state and sun elevation before applying Fix.

[📖 Detailed guide](./ABNORMAL_STATE_ALERT.md)

The two Blueprints are designed to work together without creating a loop that constantly reverses the user's manual lighting decisions.
