# Installation & Import

This repository is a **Home Assistant Blueprint collection**, not a HACS Integration.

## Supported and Tested Home Assistant Version

All current Blueprints set `homeassistant.min_version` to **2026.9.4**, which is the same Home Assistant Core version used by the repository's automated `check_config` test.

The repository does not claim compatibility with versions older than the version that is actually tested.

## Recommended Installation Method

Each detailed Blueprint guide contains a direct Import button.

You can also import manually:

1. Open Home Assistant.
2. Go to **Settings → Automations & Scenes → Blueprints**.
3. Select **Import Blueprint**.
4. Paste the raw Blueprint URL.
5. Create an Automation or Script from the imported Blueprint.
6. Select the entities, devices, durations, thresholds, URIs, and notification settings appropriate for your Home Assistant instance.
7. Save the automation/script.
8. Run the documented live-test checklist before relying on it.

## Why There Is No `hacs.json`

HACS is intended for supported repository categories such as integrations, dashboard plugins, themes, and similar package types.

This project is a multi-Blueprint collection. Publishing `hacs.json` here would give users the wrong installation path, so Blueprint import is the documented method.

## Updating an Imported Blueprint

Home Assistant stores a local copy of an imported Blueprint.

When the upstream Blueprint changes:

1. Review the upstream release or commit.
2. Update/re-import the Blueprint in Home Assistant as appropriate.
3. Reload automations/scripts if required.
4. Re-test any hardware-facing changes before relying on them.

## Safety Principle

Do not copy another person's private Home Assistant configuration literally.

The Blueprints are designed so each user selects their own:

- Entities.
- Devices.
- Runtime.
- Sun/flow thresholds.
- Media URIs.
- Notification targets.

Private home configuration should remain in the private Home Assistant instance rather than being committed to the public repository.
