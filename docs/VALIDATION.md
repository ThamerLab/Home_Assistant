# ✅ Validation

## Status

**MERGE GATE ACTIVE**

A Blueprint change is not considered ready for `main` until the **latest commit in the pull request** passes both validation jobs:

1. **Repository policy & static validation**
2. **Home Assistant 2026.9.4 config check**

Workflow:

`.github/workflows/validate-blueprints.yml`

The workflow runs again when relevant Blueprints, documentation, assets, tests, or workflow files change. A successful run for an older commit does not validate a newer commit.

## 1. Repository Policy & Static Validation

Validator:

`tests/validate_repo.py`

It automatically checks:

- Every Blueprint YAML file can be parsed with `!input` support.
- The actual Blueprint file set matches the validation map.
- `blueprint.name` exists.
- `blueprint.domain` is correct.
- `description` exists.
- `author` exists.
- `source_url` points to the matching file in this repository.
- `homeassistant.min_version` uses `X.Y.Z` format.
- Every referenced `!input` is defined inside `blueprint.input`.
- No `wait_template` or `wait_for_trigger` is left without a timeout.
- Water/irrigation and lighting Blueprints do not use `mode: restart`.
- Template triggers do not accidentally reference action-time variables that should be provided through `trigger_variables`.
- Every Blueprint has a unique dedicated image.
- Every SVG parses as valid XML.
- Every Blueprint has dedicated documentation.
- Each guide identifies its Blueprint file.
- Each guide embeds its dedicated image.
- Each guide contains step-by-step documentation.
- Each Blueprint appears in the root README.
- Each Blueprint appears in the Blueprint Catalog.
- Local Markdown links and local image paths resolve to real repository files.
- Known private-home identifier patterns are not present in public text files.
- Public documentation and Blueprint-facing text remain English-only.
- No misleading `hacs.json` file exists.

## 2. Home Assistant Configuration Validation

CI builds a test configuration under:

`tests/ha_config/`

It copies all Blueprints into the structure expected by Home Assistant and creates test instances for every Blueprint.

Coverage includes:

- Smart Irrigation — Sun mode.
- Smart Irrigation — Custom time.
- Smart Irrigation — Fixed interval.
- Long-running Water Safety.
- Outdoor Dusk to Dawn.
- Outdoor Abnormal State Alert.
- Zone Exit Notification.
- Quran Sunrise & Sunset.
- Available Updates.
- Quran Safe Toggle Script.
- Manual Irrigation Script.

The workflow then runs Home Assistant Core **2026.9.4** itself:

```text
python -m homeassistant --script check_config -c /config
```

inside:

```text
ghcr.io/home-assistant/home-assistant:2026.9.4
```

This verifies that Blueprint files load, inputs expand, and the generated automations/scripts are accepted by a real Home Assistant configuration check.

## 3. Manual Logic Audit

CI cannot understand user intent by itself, so logic is also reviewed manually for:

- Trigger semantics.
- Trigger-time versus action-time variables.
- Conditions.
- Actions.
- Waits and timeouts.
- Failure paths.
- Retry behavior.
- Restart/reload behavior.
- Automation mode.
- Overlapping-run behavior.
- State verification after hardware commands.
- Water-valve safety.
- Manual-lighting priority.
- Exact Quran URI verification.
- Explicit update-priority selection.

## 4. Documentation Gate

Repository policy:

> **No Blueprint without a dedicated image, dedicated guide, step-by-step execution explanation, limits, test procedure, and import URL.**

A new Blueprint that is not added to the validation map, or that lacks its required documentation/artwork, causes the validation job to fail.

## What PASS Means

A green validation run means the tested repository revision:

- Contains valid YAML/XML.
- Meets this project's Blueprint structure and documentation rules.
- Can instantiate all test Blueprint instances in Home Assistant 2026.9.4.
- Passes Home Assistant `check_config`.
- Has valid local documentation links and images.
- Has no known private-home identifiers covered by the repository scanner.
- Meets the English-only public-content rule.

## What PASS Does Not Mean

No GitHub test can guarantee real-world physical-device behavior.

CI cannot prove:

- A water valve mechanically closed even though the entity reports OFF.
- A Zigbee or Wi-Fi command arrived every time.
- A Music Assistant target produced audible sound.
- A location tracker updated at exactly the expected time.
- Every firmware version reports state identically.

For that reason, every hardware-facing guide includes a **Live-Test Checklist**.

## Merge Rule

The required sequence is:

```text
Edit
→ Static validation
→ Home Assistant check_config
→ Review diff
→ Latest commit must be green
→ Merge
```

The rule is not bypassed because an earlier revision of the same pull request passed.
