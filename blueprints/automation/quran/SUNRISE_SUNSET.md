# 📖 Quran — Sunrise & Sunset via Music Assistant

<p align="center">
  <img src="../../../assets/quran-schedule.svg" alt="Quran Sunrise and Sunset via Music Assistant" width="100%">
</p>

This Blueprint plays one exact Quran item through **Music Assistant** at sunrise and sunset. It verifies that the requested URI becomes the current media item and that the player reaches the `playing` state.

## Why Music Assistant?

The intended architecture is:

- Home Assistant decides **when** playback should begin.
- Music Assistant manages the library, queue, and target player.

This avoids direct dependency on native Apple TV, Google Cast, YouTube, `media_extractor`, or a device-specific local media URL.

## Requirements

1. Music Assistant is installed and connected to Home Assistant.
2. The selected player appears in Home Assistant through the `music_assistant` integration.
3. The requested Quran item exists in Music Assistant.
4. You have the exact URI for the item, for example `library://track/151`.

> [!IMPORTANT]
> Do not select the native HomePod, Apple TV, or Google Cast entity. The Blueprint selector is restricted to `media_player` entities provided by the Music Assistant integration.

## Inputs

| Input | Purpose |
|---|---|
| Music Assistant Player | Target Music Assistant media player |
| Exact Music Assistant URI | Exact URI for the requested item |
| Media Type | track / album / playlist / radio |
| Notification Devices | Optional Companion App devices |

## Step-by-Step Execution

### Step 1 — Sunrise or Sunset Trigger

The Blueprint has two triggers:

- `sunrise`
- `sunset`

There is no long-running timer after the trigger.

### Step 2 — Check Player Availability

If the selected player state is `unavailable` or `unknown`, the Blueprint does not attempt playback.

Instead, it:

- Sends a mobile failure notification to selected devices.
- Creates a persistent notification.
- Stops the automation.

### Step 3 — Start Playback Through Music Assistant

The Blueprint calls `music_assistant.play_media` with:

- `media_id` = the exact URI entered by the user.
- `media_type` = the selected media type.
- `enqueue: replace`.

Using `replace` ensures that the requested Quran item replaces the current queue instead of being appended behind older content.

### Step 4 — Verify the Exact Item

A successful service call is not treated as success by itself.

The Blueprint waits up to 30 seconds until both conditions are true:

1. The player state is `playing`.
2. `media_content_id` exactly matches the requested URI.

### Step 5 — Success Path

When both conditions are confirmed, an optional success notification indicates whether playback started at sunrise or sunset.

The automation then ends immediately.

It does **not** remain active for the full duration of the recitation.

### Step 6 — Failure Path

If the requested item cannot be confirmed within 30 seconds:

- An optional mobile failure notification is sent.
- A persistent notification is created.
- The diagnostic message includes the player, requested URI, current state, and current media content ID when available.

## Why the Automation Does Not Wait for the Recitation to End

Keeping an automation instance active for one or two hours creates unnecessary complexity and can confuse natural completion, pause, manual content changes, connection loss, restart, or reload.

This Blueprint has one responsibility: **start the requested item and verify that the correct item started**.

## Concurrency

The Blueprint uses `mode: single`.

Sunrise and sunset are far apart, so overlapping runs are not expected. A short verification window is sufficient.

## Verification Limits

Verification is based on what Music Assistant reports through Home Assistant:

- `state`
- `media_content_id`

That confirms that Music Assistant considers the requested item active. It does not physically measure audible sound from the speaker.

## Safe Live-Test Checklist

1. Confirm that the selected entity is the correct Music Assistant player.
2. Obtain the exact URI from Music Assistant rather than relying on a title search.
3. Create an automation from the Blueprint.
4. Run the actions while you can observe or hear the target device.
5. Confirm that Music Assistant reports the requested URI as the active item.
6. Test an unavailable-player scenario to verify the failure path.
7. Only after those checks pass should you rely on sunrise and sunset scheduling.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/quran/music_assistant_sunrise_sunset.yaml
```

[![Import Quran Sunrise & Sunset](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fquran%2Fmusic_assistant_sunrise_sunset.yaml)
