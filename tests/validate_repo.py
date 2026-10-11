from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

BLUEPRINTS = {
    "blueprints/automation/irrigation/smart_irrigation.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/irrigation/SMART_IRRIGATION.md",
        "image": "assets/irrigation.svg",
    },
    "blueprints/automation/irrigation/long_running_water_safety.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/irrigation/WATER_SAFETY.md",
        "image": "assets/water-safety.svg",
    },
    "blueprints/automation/lighting/outside_lights_dusk_dawn.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/lighting/DUSK_TO_DAWN.md",
        "image": "assets/outdoor-dusk-dawn.svg",
    },
    "blueprints/automation/lighting/outside_light_attention.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/lighting/ABNORMAL_STATE_ALERT.md",
        "image": "assets/outdoor-alert.svg",
    },
    "blueprints/automation/presence/notify_leaving_zone.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/presence/README.md",
        "image": "assets/zone-notification.svg",
    },
    "blueprints/automation/quran/music_assistant_sunrise_sunset.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/quran/SUNRISE_SUNSET.md",
        "image": "assets/quran-schedule.svg",
    },
    "blueprints/automation/system/available_updates_notification.yaml": {
        "domain": "automation",
        "doc": "blueprints/automation/system/README.md",
        "image": "assets/updates.svg",
    },
    "blueprints/script/quran/music_assistant_quran_toggle.yaml": {
        "domain": "script",
        "doc": "blueprints/script/quran/README.md",
        "image": "assets/quran-toggle.svg",
    },
    "blueprints/script/irrigation/manual_irrigation_safe_run.yaml": {
        "domain": "script",
        "doc": "blueprints/script/irrigation/README.md",
        "image": "assets/manual-irrigation.svg",
    },
}

PRIVATE_PATTERNS = {
    "private LAN address": re.compile(r"192\.168\.\d+\.\d+"),
    "private mobile notify service": re.compile(r"mobile_app_t4mer", re.I),
    "private homepod name": re.compile(r"almjles|nesthub58bb", re.I),
    "private Zigbee IEEE": re.compile(r"0x28dba7fffe6d(?:d28e|9c8b)", re.I),
    "private work email/domain": re.compile(r"gca\.gov\.sa", re.I),
    "private external host": re.compile(r"haroshn\.t4mer\.com", re.I),
}


class InputRef(str):
    pass


class BlueprintLoader(yaml.SafeLoader):
    pass


def input_constructor(loader: BlueprintLoader, node: yaml.Node) -> InputRef:
    return InputRef(loader.construct_scalar(node))


BlueprintLoader.add_constructor("!input", input_constructor)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=BlueprintLoader)


def walk(value):
    yield value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(key)
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def find_waits(value, path="$"):
    waits = []
    if isinstance(value, dict):
        if "wait_template" in value or "wait_for_trigger" in value:
            waits.append((path, "timeout" in value))
        for key, item in value.items():
            waits.extend(find_waits(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            waits.extend(find_waits(item, f"{path}[{index}]"))
    return waits


def main() -> int:
    errors: list[str] = []

    actual_yaml = {
        str(path.relative_to(ROOT))
        for path in (ROOT / "blueprints").rglob("*.yaml")
    }
    expected_yaml = set(BLUEPRINTS)

    unexpected = sorted(actual_yaml - expected_yaml)
    missing = sorted(expected_yaml - actual_yaml)
    if unexpected:
        errors.append(f"Blueprint YAML missing from validation map: {unexpected}")
    if missing:
        errors.append(f"Expected blueprint YAML files missing: {missing}")

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index_readme = (ROOT / "blueprints/README.md").read_text(encoding="utf-8")

    for rel_path, meta in BLUEPRINTS.items():
        path = ROOT / rel_path
        doc = ROOT / meta["doc"]
        image = ROOT / meta["image"]

        if not path.exists():
            continue

        try:
            data = load_yaml(path)
        except Exception as exc:
            errors.append(f"{rel_path}: YAML parse failed: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel_path}: top-level YAML must be a mapping")
            continue

        bp = data.get("blueprint")
        if not isinstance(bp, dict):
            errors.append(f"{rel_path}: missing blueprint metadata")
            continue

        if not bp.get("name"):
            errors.append(f"{rel_path}: blueprint.name is required")
        if bp.get("domain") != meta["domain"]:
            errors.append(
                f"{rel_path}: domain={bp.get('domain')!r}, expected {meta['domain']!r}"
            )
        if not bp.get("description"):
            errors.append(f"{rel_path}: blueprint.description is required by repository policy")
        if not bp.get("author"):
            errors.append(f"{rel_path}: blueprint.author is required by repository policy")

        expected_source = f"https://github.com/ThamerLab/Home_Assistant/blob/main/{rel_path}"
        if bp.get("source_url") != expected_source:
            errors.append(
                f"{rel_path}: source_url must be {expected_source!r}; got {bp.get('source_url')!r}"
            )

        ha_meta = bp.get("homeassistant")
        if not isinstance(ha_meta, dict) or not re.fullmatch(
            r"\d+\.\d+\.\d+", str(ha_meta.get("min_version", ""))
        ):
            errors.append(f"{rel_path}: homeassistant.min_version must use X.Y.Z")

        inputs = bp.get("input", {})
        if not isinstance(inputs, dict):
            errors.append(f"{rel_path}: blueprint.input must be a mapping")
            inputs = {}

        referenced_inputs = {str(item) for item in walk(data) if isinstance(item, InputRef)}
        undefined_inputs = sorted(referenced_inputs - set(inputs))
        if undefined_inputs:
            errors.append(f"{rel_path}: undefined !input references: {undefined_inputs}")

        for wait_path, has_timeout in find_waits(data):
            if not has_timeout:
                errors.append(f"{rel_path}: {wait_path} has wait action without timeout")

        if "irrigation" in rel_path or "lighting" in rel_path:
            if data.get("mode") == "restart":
                errors.append(f"{rel_path}: high-risk hardware blueprint must not use mode: restart")

        text = path.read_text(encoding="utf-8")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{rel_path}: contains {label}")

        if not doc.exists():
            errors.append(f"{rel_path}: dedicated documentation missing: {meta['doc']}")
        else:
            doc_text = doc.read_text(encoding="utf-8")
            if path.name not in doc_text and rel_path not in doc_text:
                errors.append(
                    f"{meta['doc']}: must identify its blueprint filename/path ({path.name})"
                )
            if meta["image"].split("/")[-1] not in doc_text:
                errors.append(
                    f"{meta['doc']}: must embed dedicated image {meta['image']}"
                )

        if not image.exists():
            errors.append(f"{rel_path}: dedicated image missing: {meta['image']}")
        else:
            try:
                ET.parse(image)
            except Exception as exc:
                errors.append(f"{meta['image']}: invalid SVG/XML: {exc}")

        if path.name not in root_readme and rel_path not in root_readme:
            errors.append(f"README.md: blueprint not listed: {rel_path}")
        if path.name not in index_readme and rel_path not in index_readme:
            errors.append(f"blueprints/README.md: blueprint not listed: {rel_path}")

    if (ROOT / "hacs.json").exists():
        errors.append(
            "hacs.json must not exist: this multi-blueprint collection is imported through "
            "Home Assistant Blueprints, not published as a HACS repository type."
        )

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALIDATION PASSED: {len(BLUEPRINTS)} blueprints")
    for rel_path, meta in BLUEPRINTS.items():
        print(f"- {rel_path} | doc={meta['doc']} | image={meta['image']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
