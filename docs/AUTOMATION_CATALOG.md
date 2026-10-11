# Automation Catalog

This document explains every reusable automation and script pattern currently represented in this repository and links each one to its corresponding public Blueprint.

> The public repository intentionally excludes private entity IDs, device names, IP addresses, and other home-specific configuration.

## System Map

| # | System | Type | Blueprint |
|---:|---|---|---|
| 1 | Quran playback at sunrise and sunset | Automation | [Quran Sunrise & Sunset](../blueprints/automation/quran/SUNRISE_SUNSET.md) |
| 2 | Scheduled irrigation | Automation | [Smart Irrigation](../blueprints/automation/irrigation/SMART_IRRIGATION.md) |
| 3 | Available update notifications | Automation | [Available Updates](../blueprints/automation/system/README.md) |
| 4 | Outdoor lighting from dusk to dawn | Automation | [Dusk to Dawn](../blueprints/automation/lighting/DUSK_TO_DAWN.md) |
| 5 | Outdoor-light abnormal-state alert | Automation | [Abnormal State Alert](../blueprints/automation/lighting/ABNORMAL_STATE_ALERT.md) |
| 6 | Long-running water safety | Automation | [Water Safety Watchdog](../blueprints/automation/irrigation/WATER_SAFETY.md) |
| 7 | Timed manual irrigation | Script | [Manual Irrigation](../blueprints/script/irrigation/README.md) |
| 8 | Quran smart toggle | Script | [Quran Safe Toggle](../blueprints/script/quran/README.md) |
| 9 | Zone exit notification | Automation | [Zone Exit Notification](../blueprints/automation/presence/README.md) |

---

## 1. 📖 Quran Playback at Sunrise and Sunset

**Triggers:** Sunrise and sunset.

### Step-by-Step Flow

1. Home Assistant receives the sun event.
2. The automation checks the selected Music Assistant player.
3. If the player is unavailable or unknown, the run stops and reports the failure.
4. If the player is available, Music Assistant is asked to play one exact URI.
5. The queue is replaced so older content does not remain ahead of the requested item.
6. The automation waits up to 30 seconds.
7. Success requires both `playing` state and the exact requested `media_content_id`.
8. On success, the automation ends immediately.
9. On failure, a diagnostic notification is created.

**Design reason:** the automation owns the start event only. It does not attempt to interpret every pause, stop, or natural completion during a long recitation.

---

## 2. 🌱 Scheduled Irrigation

**Triggers:** Sunrise/sunset, one custom time, or a fixed clock interval.

### Step-by-Step Flow

1. Confirm that the current trigger belongs to the selected schedule mode.
2. Check whether any selected valve is already ON.
3. If a valve is already ON and blocking is enabled, skip the scheduled run.
4. Send ON to all selected valves.
5. Verify that every selected valve reports ON.
6. Wait one minute.
7. Confirm that all selected valves are still ON.
8. Read every selected flow sensor.
9. If no-flow protection is enabled, require every selected sensor to report a positive numeric value.
10. If any sensor fails, send OFF to all valves and stop.
11. Monitor the remaining runtime for any selected valve turning OFF early.
12. At the end of the runtime, send OFF to all selected valves.
13. Verify that every selected valve reports OFF.
14. Calculate an estimated water-usage value when flow sensors are configured.
15. Send the completion notification only after shutdown is confirmed.

---

## 3. 🔔 Available Updates

**Trigger:** One configured time every day.

### Step-by-Step Flow

1. Read all `update.*` entities.
2. If none are `on`, send nothing.
3. Split available updates into Priority and Other groups.
4. Priority membership is chosen explicitly by the user, not guessed from names.
5. Build a single summary.
6. Send it to the selected Companion App devices.
7. Include a link to the Home Assistant Updates page.
8. Do not install or apply any update automatically.

---

## 4. 🌙 Outdoor Lighting — Dusk to Dawn

**Trigger:** Sun elevation crossing the configured threshold.

### Evening Flow

1. Send `light.turn_on`.
2. Wait for the selected light to report ON.
3. If verification fails, wait five seconds.
4. Retry ON once.
5. Verify again.
6. If the second attempt fails, create failure notifications.

### Morning Flow

The same sequence runs with `light.turn_off` and OFF-state verification.

**Important design choice:** there is no startup force-sync. A Home Assistant restart does not automatically reverse a manual lighting decision made after the scheduled event.

---

## 5. 💡 Outdoor Light — Abnormal State Alert

**Trigger:** Night + OFF or Day + ON remains true for the configured mismatch duration.

### Step-by-Step Flow

1. A template trigger detects the mismatch.
2. The mismatch must remain true for the configured duration.
3. The automation identifies whether the situation is Night + OFF or Day + ON.
4. Unique Fix and Keep action IDs are generated from the current automation context.
5. An actionable notification is sent.
6. The automation waits for Fix, Keep, or automatic resolution.
7. If Fix is selected, current sun elevation and current light state are checked again before changing the light.
8. If Keep is selected, the light is not changed.
9. If the mismatch resolves by itself, the notification is cleared.

---

## 6. 🚨 Long-running Water Safety Watchdog

**Triggers:** A selected switch remaining ON too long, a five-minute periodic watchdog, and Home Assistant startup.

### Step-by-Step Flow

1. Confirm that a selected switch has exceeded the configured ON duration.
2. Generate unique Stop and Keep action IDs.
3. Send a critical actionable notification.
4. If Stop is selected, send OFF to all selected switches.
5. Wait up to 15 seconds for every selected switch to report OFF.
6. If shutdown verification fails, send a new critical failure notification.
7. If Keep is selected, clear the original warning and enter the configured snooze period.
8. If all selected switches are turned OFF manually, clear the warning.
9. If no response is received, the warning remains visible and a later watchdog run can replace it.

---

## 7. 💧 Manual Irrigation Script

### Step-by-Step Flow

1. Ask for a runtime when the script is called.
2. Check whether a selected valve is already ON.
3. If blocking is enabled and a valve is already ON, do not take control.
4. Send ON to all selected valves.
5. Verify that every selected valve reports ON.
6. Wait one minute.
7. Confirm that all selected valves are still ON.
8. Validate every selected flow sensor when no-flow protection is enabled.
9. Monitor for early valve shutdown during the remaining runtime.
10. At the end, send OFF to every selected valve.
11. Verify that all selected valves report OFF.
12. Send a completion notification only after successful shutdown verification.
13. Report an estimated water-usage value when flow sensors are configured.

**Important:** a Home Assistant restart interrupts an active script sequence, so this script should be paired with the independent Water Safety Watchdog for real irrigation hardware.

---

## 8. 📖 Quran Safe Toggle Script

### Step-by-Step Flow

1. If the Music Assistant player is unavailable, stop and report the failure.
2. If the requested URI is currently playing, send Stop and verify the result.
3. If the requested URI is currently paused, send Resume and verify the result.
4. For any other content or player state, replace the Music Assistant queue with the requested URI.
5. Wait for `playing` plus the exact URI.
6. If verification fails, send a diagnostic notification.

The exact URI check prevents unrelated content from being mistaken for the requested Quran item.

---

## 9. 📍 Zone Exit Notification

**Trigger:** Any state change of the selected Person entity.

### Step-by-Step Flow

1. Read the selected Person and Zone.
2. Determine the state that represents being inside the selected zone.
3. Confirm that the previous state represented the selected zone.
4. Confirm that the new state is outside that zone.
5. Send a Companion App notification.

**Important:** location accuracy and notification timing depend on the underlying Device Tracker, not on this Blueprint itself.
