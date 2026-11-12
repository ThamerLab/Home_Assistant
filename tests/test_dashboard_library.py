from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "docs" / "dashboard-library"
CATALOG = LIBRARY / "CATALOG.md"
SOURCES = LIBRARY / "SOURCES.md"
PILOT = LIBRARY / "PILOT_TEST.md"
README = LIBRARY / "README.md"

ROW_RE = re.compile(r"^\| (D\d{3}) \| ([^|]+?) \| ([^|]+?) \|", re.MULTILINE)
SOURCE_REF_RE = re.compile(r"\bS\d{2}\b")
SOURCE_DEF_RE = re.compile(r"^\| (S\d{2}) \|", re.MULTILINE)


def main() -> int:
    errors: list[str] = []

    for path in (CATALOG, SOURCES, PILOT, README):
        if not path.exists():
            errors.append(f"Missing dashboard library file: {path.relative_to(ROOT)}")

    if errors:
        print("DASHBOARD LIBRARY TEST FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    catalog = CATALOG.read_text(encoding="utf-8")
    sources = SOURCES.read_text(encoding="utf-8")
    pilot = PILOT.read_text(encoding="utf-8")

    rows = ROW_RE.findall(catalog)
    ids = [row[0] for row in rows]
    names = [row[2].strip() for row in rows]

    expected_ids = [f"D{i:03d}" for i in range(1, 101)]

    if len(rows) != 100:
        errors.append(f"Catalog must contain exactly 100 pattern rows; found {len(rows)}")

    if ids != expected_ids:
        missing = sorted(set(expected_ids) - set(ids))
        unexpected = sorted(set(ids) - set(expected_ids))
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        errors.append(
            "Pattern IDs must be exactly D001..D100 in order "
            f"(missing={missing}, unexpected={unexpected}, duplicates={duplicates})"
        )

    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    if duplicate_names:
        errors.append(f"Pattern names must be unique: {duplicate_names}")

    defined_sources = set(SOURCE_DEF_RE.findall(sources))
    used_sources = set(SOURCE_REF_RE.findall(catalog))
    undefined_sources = sorted(used_sources - defined_sources)
    if undefined_sources:
        errors.append(f"Catalog references undefined source IDs: {undefined_sources}")

    if len(defined_sources) < 50:
        errors.append(
            f"Source registry must contain at least 50 defined sources; found {len(defined_sources)}"
        )

    if "**PASS**" not in pilot:
        errors.append("Pilot test must contain an explicit PASS result")

    if "Total: 100 patterns" not in catalog:
        errors.append("Catalog must explicitly state the 100-pattern total")

    allowed_complexity = {"Low", "Medium", "High"}
    allowed_risk = {"Low", "Medium", "High"}

    table_rows = [
        line for line in catalog.splitlines()
        if re.match(r"^\| D\d{3} \|", line)
    ]

    for line in table_rows:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 11:
            errors.append(
                f"{cells[0] if cells else 'unknown'} must have 11 catalog columns; found {len(cells)}"
            )
            continue

        pattern_id, category, pattern, best_for, view, native_first, optional_layer, complexity, risk, source_refs, design_rule = cells

        required = {
            "category": category,
            "pattern": pattern,
            "best_for": best_for,
            "view": view,
            "native_first": native_first,
            "optional_layer": optional_layer,
            "complexity": complexity,
            "risk": risk,
            "source_refs": source_refs,
            "design_rule": design_rule,
        }
        for field, value in required.items():
            if not value:
                errors.append(f"{pattern_id}: empty required field {field}")

        if complexity not in allowed_complexity:
            errors.append(f"{pattern_id}: invalid complexity {complexity!r}")
        if risk not in allowed_risk:
            errors.append(f"{pattern_id}: invalid risk {risk!r}")

        refs = [ref.strip() for ref in source_refs.split(",")]
        if not refs or any(not re.fullmatch(r"S\d{2}", ref) for ref in refs):
            errors.append(f"{pattern_id}: malformed source references {source_refs!r}")

    category_counts: dict[str, int] = {}
    for _, category, _ in rows:
        category = category.strip()
        category_counts[category] = category_counts.get(category, 0) + 1

    if sum(category_counts.values()) != 100:
        errors.append("Category counts do not sum to 100")

    if errors:
        print("DASHBOARD LIBRARY TEST FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("DASHBOARD LIBRARY TEST PASSED")
    print("- 100/100 unique dashboard patterns")
    print(f"- {len(defined_sources)} source references registered")
    print("- Pilot result: PASS")
    print("- All pattern rows have required metadata")
    print("- All catalog source references resolve to the source registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
