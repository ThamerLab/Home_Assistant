# 💧 Irrigation Blueprints

<p align="center">
  <img src="../../../assets/irrigation.svg" alt="Smart Irrigation" width="49%">
  <img src="../../../assets/water-safety.svg" alt="Water Safety Watchdog" width="49%">
</p>

This section contains two separate Blueprints because **normal irrigation control** and **long-running safety monitoring** are different responsibilities.

## 1. 🌱 Smart Irrigation

File: `smart_irrigation.yaml`

Main responsibilities:

- Sunrise / Sunset scheduling.
- Custom daily time.
- Fixed clock intervals.
- Blocks a scheduled start when a selected valve is already ON.
- Verifies that all selected valves report ON.
- Samples every selected flow sensor after one minute.
- Stops on failed no-flow validation.
- Detects early/manual valve shutdown.
- Sends a final OFF command and verifies OFF state.
- Optionally estimates water usage.

[📖 Detailed step-by-step guide](./SMART_IRRIGATION.md)

## 2. 🚨 Long-running Water Safety Watchdog

File: `long_running_water_safety.yaml`

Main responsibilities:

- Monitors how long selected water switches remain ON.
- Sends a critical notification.
- Offers Stop all / Keep running actions.
- Verifies OFF state after a stop command.
- Uses a five-minute watchdog plus a startup fallback.
- Supports a snooze period after Keep running.

[📖 Detailed step-by-step guide](./WATER_SAFETY.md)

> [!IMPORTANT]
> For real irrigation hardware, use both when practical: Smart Irrigation for normal operation and Water Safety as an independent supervisory layer.
