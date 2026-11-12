# Dashboard Reference Library — Pilot Test

Date: 2026-11-12

This pilot is the quality gate for the 100-pattern Home Assistant dashboard reference library. The library must be useful for building real dashboards, not merely a gallery of screenshots.

## Why a Pilot Exists

A dashboard source can look excellent and still be a poor engineering reference because it may be abandoned, tied to one screen size, depend on a large stack of fragile custom cards, expose private entity IDs, or use layout techniques that Home Assistant has since replaced with native features.

The pilot therefore tests the curation method before the catalog expands to 100 patterns.

## Current Home Assistant Baseline

For new dashboard work, the default baseline is:

1. Prefer native **Sections** view for responsive grid layout.
2. Prefer native **Tile** and **Area** cards for ordinary controls and room summaries.
3. Prefer per-card/per-section **Visibility** conditions instead of wrapping everything in Conditional cards.
4. Use **Panel** for full-screen maps, cameras, floorplans, or custom applications.
5. Use community cards only when they materially improve the interaction or visualization.
6. Treat custom CSS as an enhancement, not as the structural foundation of a dashboard.
7. Keep phone, tablet, wall-panel, guest, and admin needs separate when one responsive surface cannot serve all of them cleanly.

Official references:
- https://www.home-assistant.io/dashboards/
- https://www.home-assistant.io/dashboards/views/
- https://www.home-assistant.io/dashboards/sections/
- https://www.home-assistant.io/dashboards/cards
- https://www.home-assistant.io/dashboards/tile/
- https://www.home-assistant.io/dashboards/area/
- https://www.home-assistant.io/dashboards/conditional/
- https://www.home-assistant.io/dashboards/picture-elements/

## Scoring Model

Each candidate is scored from 0 to 5 in six dimensions, for a maximum of 30.

| Dimension | What is tested |
|---|---|
| Currency | Recent development or clearly current Home Assistant compatibility |
| Native fit | Works well with current Home Assistant dashboard concepts |
| Portability | Can be adapted to a different home without a rewrite |
| Dependency clarity | Required custom cards/integrations are explicit and bounded |
| Reproducibility | Source/configuration is inspectable and practical to reproduce |
| Reference value | Teaches a pattern worth reusing in other dashboards |

Decision bands:

- **26–30 — Foundation:** safe to use as a primary design reference.
- **22–25 — Reference:** useful pattern source; adapt rather than copy blindly.
- **18–21 — Idea only:** visual/interaction inspiration only.
- **0–17 — Reject:** do not include as an endorsed pattern source.

## Pilot Candidates

| # | Source | Focus | Score | Decision | Key reason |
|---:|---|---|---:|---|---|
| 1 | Home Assistant native dashboards | Native Sections, Tile, Area, Visibility | 30 | Foundation | Official current platform baseline |
| 2 | [Hemma](https://github.com/willsanderson/Hemma) | Responsive rooms, phone/tablet/desktop | 29 | Foundation | Current, UI-configured, HA 2026.9+ |
| 3 | [Bubble Card](https://github.com/Clooos/Bubble-Card) | Pop-ups, touch-first controls | 28 | Foundation | Active, flexible, broad card set |
| 4 | [Mushroom](https://github.com/piitaya/lovelace-mushroom) | Simple clean card system | 28 | Foundation | Mature, visual editors, low setup friction |
| 5 | [UI Lovelace Minimalist](https://github.com/UI-Lovelace-Minimalist/UI) | Design system and reusable templates | 27 | Foundation | Active template ecosystem and consistent UI |
| 6 | [button-card](https://github.com/custom-cards/button-card) | Advanced reusable controls | 26 | Foundation | Excellent for templated controls; higher complexity |
| 7 | [ha-fusion](https://github.com/knowald/ha-fusion) | Drag-and-drop custom dashboard | 26 | Foundation | Current maintained continuation; strong interaction model |
| 8 | [Dwains Dashboard Next](https://github.com/dwainscheeren/dwains-dashboard-next) | Auto-generated whole-home UI | 25 | Reference | Current but next-generation project still evolving |
| 9 | [Homio](https://github.com/iamtherufus/Homio) | Minimal YAML room dashboard | 24 | Reference | Strong visual hierarchy; more manual YAML |
| 10 | [HA Family Hub](https://github.com/JVarhol/HA-Family-Hub) | Family calendar, chores, meals | 25 | Reference | Excellent specialized wall-panel patterns |
| 11 | [Kitchen Dashboard](https://github.com/bdunn44/kitchen-dashboard) | Portrait wall tablet command center | 23 | Reference | Rich real-world layout but many custom dependencies |
| 12 | [HA Floorplanner GUI](https://github.com/sleien/HA-floorplanner-gui) | Interactive floorplan | 23 | Reference | Strong specialized floorplan workflow |

## Pilot Freshness Check

Repository metadata checked during the pilot showed active 2026 development for the primary foundation sources, including Hemma, Bubble Card, Mushroom, UI Lovelace Minimalist, button-card, ha-fusion, and Dwains Dashboard Next.

Older but still useful design references are not automatically rejected. Their role is downgraded when a current native Home Assistant feature provides a simpler equivalent.

## Pilot Result

**PASS**

- 12/12 candidates scored at least 22.
- 7/12 qualify as Foundation sources.
- The sample covers native dashboards, responsive/mobile design, custom-card systems, auto-generated dashboards, family wall panels, portrait tablet layouts, and floorplans.
- No candidate in the pilot is archived.
- The scoring method distinguishes maintainable implementation references from inspiration-only material.

The 100-pattern catalog may therefore proceed using the same scoring and classification rules.

## Rules for the Full 100-Pattern Library

Every pattern must record:

- Pattern ID and name.
- Primary use case.
- Best target device: phone, tablet, wall display, desktop, or universal.
- Recommended Home Assistant view type.
- Native-first implementation path.
- Optional custom-card path.
- Information hierarchy.
- Interaction model.
- Dependencies.
- Complexity: Low / Medium / High.
- Maintenance risk: Low / Medium / High.
- Source inspiration.
- What to copy.
- What **not** to copy.
- Suitability for a future ThamerLab home dashboard.

The 100 entries are **patterns**, not 100 blindly cloned third-party dashboards. A single excellent source may inspire several distinct reusable patterns, and every pattern must be mapped back to current Home Assistant capabilities.
