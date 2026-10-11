# 🔔 Available Updates — Daily Summary

<p align="center">
  <img src="../../../assets/updates.svg" alt="Available Updates Notification" width="100%">
</p>

This Blueprint sends a daily summary only when one or more Home Assistant `update.*` entities are in the `on` state, meaning an update is available.

## Why Explicit Priority Selection?

Classifying update importance by matching words in `friendly_name` is fragile because names vary by integration, language, and version.

This Blueprint lets the user explicitly choose **Priority Update Entities**. Every other available update is automatically grouped under Other updates.

## Inputs

| Input | Default | Purpose |
|---|---:|---|
| Notification Time | 09:30 | Daily time to check for updates |
| Priority Update Entities | None | Update entities that should appear first |
| Notification Devices | — | One or more Companion App devices |
| Notification Tag | home_assistant_updates | Replaces the previous summary instead of stacking duplicates |

## Step-by-Step Execution

### Step 1 — Daily Trigger

The automation runs once at the configured notification time.

### Step 2 — Check for Available Updates

It evaluates all `update.*` entities.

If none are `on`:

- The automation ends.
- No empty notification is sent.

### Step 3 — Build Priority and Other Groups

Only currently available updates are considered.

Each available update is placed into one of two groups:

- **Priority** — the entity was selected in Priority Update Entities.
- **Other** — every other available update.

### Step 4 — Build the Summary

The automation lists each update by its display name under the appropriate group.

### Step 5 — Send the Notification

The summary is sent to every selected Companion App device.

The notification contains:

- The total number of available updates in the title.
- Priority and Other sections when relevant.
- A notification tag so newer summaries replace older ones.
- A URL that opens the Home Assistant Updates page.

## What It Does Not Do

This Blueprint does not:

- Install updates.
- Restart Home Assistant.
- Automatically classify every update as critical.
- Modify update entities.

It is a notification-only workflow.

## Safe Test Checklist

1. Create an automation from the Blueprint.
2. Select one or more notification devices.
3. Select any update entities you want treated as Priority.
4. Temporarily set the notification time a few minutes ahead.
5. Confirm that at least one `update.*` entity is currently `on`.
6. Verify that the message arrives and the grouping is correct.
7. Restore the desired daily notification time.

## Import

```text
https://raw.githubusercontent.com/ThamerLab/Home_Assistant/main/blueprints/automation/system/available_updates_notification.yaml
```

[![Import Available Updates](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FThamerLab%2FHome_Assistant%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Favailable_updates_notification.yaml)
