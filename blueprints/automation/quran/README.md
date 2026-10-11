# 📖 Quran / Music Assistant Blueprints

<p align="center">
  <img src="../../../assets/quran-schedule.svg" alt="Quran Schedule" width="49%">
  <img src="../../../assets/quran-toggle.svg" alt="Quran Toggle" width="49%">
</p>

The design goal is to make **Music Assistant the only playback layer** for these Quran workflows while Home Assistant handles scheduling, conditions, and notifications.

## Automation: Sunrise & Sunset

`music_assistant_sunrise_sunset.yaml`

- Plays an exact Music Assistant URI at sunrise and sunset.
- Uses `enqueue: replace`.
- Verifies both `playing` and the exact `media_content_id`.
- Includes an explicit failure path.
- Does not wait for the recitation to finish.

[📖 Detailed step-by-step guide](./SUNRISE_SUNSET.md)

## Script: Safe Toggle

`../../script/quran/music_assistant_quran_toggle.yaml`

- Same URI Playing → Stop and verify.
- Same URI Paused → Resume and verify.
- Any other state or content → Replace queue, play, and verify.
- Player selector is restricted to Music Assistant media players.

[📖 Detailed script guide](../../script/quran/README.md)
