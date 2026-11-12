# Home Assistant Dashboard Reference Library

This folder is the design reference for future Home Assistant dashboard work in ThamerLab.

The research baseline was refreshed against Home Assistant **2026.11** on 2026-11-12. Deployment must still check the actual target Home Assistant version before using version-specific features such as automatic Sections or Marketplace-managed community content.

It is not a collection of 100 screenshots or copied private configurations. It is a curated library of **100 reusable dashboard patterns**, grounded in current Home Assistant native capabilities and cross-checked against active community projects.

## Files

- [PILOT_TEST.md](./PILOT_TEST.md) — quality gate performed before the 100-pattern catalog was accepted.
- [SOURCES.md](./SOURCES.md) — official documentation and community source registry.
- [CATALOG.md](./CATALOG.md) — exactly 100 reusable dashboard patterns.

## Design Principles

1. **Native-first** — use Sections, Tile, Area, built-in dashboards and Visibility before adding frontend dependencies.
2. **Registry-driven** — model the real home with Floors, Areas, Devices, Entities, Labels and Users before styling.
3. **Calm by default** — normal healthy states should not compete for attention.
4. **Exceptions first** — open doors, active media, alarms, low batteries and unavailable devices should surface when relevant.
5. **Progressive disclosure** — overview first, detail on tap.
6. **Responsive by design** — phone, wall tablet and desktop have different density and interaction needs.
7. **Touch safety** — risky or remote actions need deliberate interaction and, when appropriate, confirmation.
8. **Stable structure** — use a repeatable room skeleton so controls do not move unpredictably.
9. **Dependency discipline** — every custom card must solve a requirement that native Home Assistant does not solve cleanly.
10. **Maintainability over novelty** — a dashboard that remains usable after upgrades is better than a fragile visual showcase.

## How This Library Should Be Used

For a new dashboard request:

1. Inventory the user's current Floors, Areas, Devices and Entities.
2. Identify target screens and users.
3. Pick the closest catalog pattern or combination of patterns.
4. Start from native Home Assistant controls.
5. Add only the custom layers justified by the selected pattern.
6. Build a small prototype before implementing the full home.
7. Test phone/tablet/desktop behavior as applicable.
8. Verify all high-risk controls and visibility conditions.
9. Record new reusable design findings back into this library.

## Default Architecture

Unless a requirement strongly suggests another direction, start from:

- **D100 Universal Adaptive Reference Dashboard** for overall architecture.
- **D001 Native Whole-Home Overview** for the landing page.
- **D011 Standard Room Control** for each room.
- **D028 / D082** for maintenance exceptions.
- A dedicated Mobile, Wall, Security, Energy or Specialized pattern only when it adds real value.

## What the Library Does Not Do

- It does not copy private entity IDs from third-party repositories.
- It does not assume that high GitHub star count equals technical quality.
- It does not make every dashboard depend on HACS.
- It does not treat custom CSS as a substitute for information architecture.
- It does not force one visual style onto every screen.
