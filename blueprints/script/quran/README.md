# 📖 Quran — Music Assistant Safe Toggle Script

<p align="center">
  <img src="../../../assets/quran-toggle.svg" alt="Quran Safe Toggle Script" width="100%">
</p>

This Script Blueprint turns one exact Quran item in Music Assistant into a single smart control: **play / resume / stop**, depending on the actual player state and active URI.

## Requirements

- Music Assistant is installed.
- The target is a Music Assistant `media_player`, not the native Cast or Apple TV entity.
- The exact URI of the requested item is known.
- The correct media type is selected.

## Inputs

| Input | Purpose |
|---|---|
| Music Assistant Player | Target MA player |
| Exact Music Assistant URI | URI for the requested Quran item |
| Media Type | track / album / playlist / radio |
| Notification Devices | Optional devices for playback failure notifications |

## Step-by-Step Logic

### Step 1 — Player Unavailable

If the player state is `unavailable` or `unknown`:

- No Play or Stop command is sent.
- Optional mobile failure notifications are sent.
- A persistent notification is created.
- The script stops.

### Step 2 — Same URI Is Currently Playing

Conditions:

- `state == playing`
- `media_content_id == requested URI`

The script then:

1. Sends `media_player.media_stop`.
2. Waits up to 15 seconds.
3. Treats the stop as successful only if the player is no longer playing that exact URI.
4. Sends a failure notification if the stop cannot be confirmed.

### Step 3 — Same URI Is Paused

Conditions:

- `state == paused`
- `media_content_id == requested URI`

The script then:

1. Sends `media_player.media_play`.
2. Waits up to 15 seconds.
3. Requires `playing` plus the same exact URI.
4. Sends a failure notification if resume cannot be confirmed.

### Step 4 — Any Other State or Content

This includes idle, available-but-off, different music, or a different Quran URI.

The script then:

1. Calls `music_assistant.play_media`.
2. Uses `enqueue: replace`.
3. Waits up to 30 seconds.
4. Requires `playing` plus the requested URI.
5. Sends a failure notification and persistent diagnostic message if verification fails.

## Why Exact URI Matching Matters

Checking only for `playing` is not enough. The player could be playing a different source or different media item.

The URI check ties the action to the exact requested content.

## Concurrency

The script uses `mode: single`.

Repeated rapid button presses do not create multiple competing script runs.

## Limits

- Verification depends on Music Assistant state updates reaching Home Assistant.
- Final Stop/Resume behavior depends on the capabilities Music Assistant exposes for the target player.
- The script does not search by title; an exact URI is required.
- No home-specific entity ID is stored in the Blueprint.

## Safe Live-Test Checklist

Test all four state paths independently:

1. Player Idle → requested URI should start.
2. Requested URI Playing → it should stop.
3. Requested URI Paused → it should resume.
4. Different content Playing → the queue should be replaced by the requested URI.

Review the Home Assistant trace after each test.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/script/quran/music_assistant_quran_toggle.yaml
```

[![Import Quran Safe Toggle](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fscript%2Fquran%2Fmusic_assistant_quran_toggle.yaml)
