# Dashboard Reference Library — Source Registry

Last reviewed: 2026-11-12

This registry is the evidence base for the 100 dashboard patterns in [CATALOG.md](./CATALOG.md). It intentionally mixes official Home Assistant documentation with active community projects. Community sources are references, not automatic endorsements of every implementation choice.

## Source Classes

- **Official baseline** — current Home Assistant behavior and native capabilities.
- **Foundation** — strong current implementation reference.
- **Reference** — useful specialized pattern source; adapt to current native features.
- **Idea source** — valuable concept, but not a default architecture.

## Official Home Assistant

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S01 | [Dashboards](https://www.home-assistant.io/dashboards/) | Official baseline | Overall dashboard model and supported customization |
| S02 | [Dashboard Views](https://www.home-assistant.io/dashboards/views/) | Official baseline | Sections, Masonry, Panel, Sidebar |
| S03 | [Sections](https://www.home-assistant.io/dashboards/sections/) | Official baseline | Default responsive grid, section visibility, headers, footers |
| S04 | [Dashboard Cards](https://www.home-assistant.io/dashboards/cards) | Official baseline | Native card inventory and sizing |
| S05 | [Tile Card](https://www.home-assistant.io/dashboards/tile/) | Official baseline | Default entity control surface |
| S06 | [Area Card](https://www.home-assistant.io/dashboards/area/) | Official baseline | Area-aware summaries that follow the registry |
| S07 | [Conditional / Visibility](https://www.home-assistant.io/dashboards/conditional/) | Official baseline | State, user, screen, location, time and other visibility conditions |
| S08 | [Picture Elements](https://www.home-assistant.io/dashboards/picture-elements/) | Official baseline | Native floorplans and image overlays |
| S09 | [Built-in Dashboard Model](https://www.home-assistant.io/dashboards/) | Official baseline | Home, Lights, Climate, Security, Energy and Maintenance design direction |

## General Dashboard Frameworks and Design Systems

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S10 | [Hemma](https://github.com/willsanderson/Hemma) | Foundation | Current HA 2026.9+ responsive room-first UI generated from configuration |
| S11 | [Bubble Card](https://github.com/Clooos/Bubble-Card) | Foundation | Touch-first controls, pop-ups, modules, reusable interaction patterns |
| S12 | [Mushroom](https://github.com/piitaya/lovelace-mushroom) | Foundation | Mature clean card system with visual editors |
| S13 | [UI Lovelace Minimalist](https://github.com/UI-Lovelace-Minimalist/UI) | Foundation | Consistent reusable design system and templated cards |
| S14 | [button-card](https://github.com/custom-cards/button-card) | Foundation | Advanced templated interaction and state-aware controls |
| S15 | [card-mod](https://github.com/thomasloven/lovelace-card-mod) | Reference | CSS styling when native theming is insufficient |
| S16 | [auto-entities](https://github.com/thomasloven/lovelace-auto-entities) | Reference | Dynamic entity lists and maintenance surfaces |
| S17 | [ha-fusion](https://github.com/knowald/ha-fusion) | Foundation | Current drag-and-drop alternative dashboard with real-time HA control |
| S18 | [Dwains Dashboard Next](https://github.com/dwainscheeren/dwains-dashboard-next) | Reference | Next-generation auto-generated whole-home patterns |
| S19 | [Homio](https://github.com/iamtherufus/Homio) | Reference | Minimal room hierarchy and wall-tablet visual language |
| S20 | [Adaptive Mushroom](https://github.com/sga-noud/adaptive-mushroom) | Reference | One dashboard adapting across mobile/tablet and light/dark |
| S21 | [Home Assistant Mobile First](https://github.com/Clooos/Home-Assistant-Mobile-First) | Reference | Mobile-first navigation and information hierarchy |
| S22 | [Atrium Dashboard](https://github.com/ericmatte/ha-atrium-dashboard) | Reference | Dynamic area discovery and room detail panels |
| S23 | [Live Dashboard](https://github.com/mbonny95/live_dashboard) | Reference | Area-driven lightweight tablet dashboard with optional modules |
| S24 | [HAven](https://github.com/TommySharpNZ/haven) | Reference | Lightweight fixed-canvas dashboard for older displays |
| S25 | [Koti](https://github.com/clutchthrower/koti) | Reference | Native Android room dashboard for older wall tablets |
| S26 | [Dashboard Home Assistant Builder](https://github.com/hiddevanbrussel/Dashboard-Home-Assistant) | Reference | Touch-first drag/resize wall tablet patterns |
| S27 | [Panalume](https://github.com/leacho73/panalume) | Reference | Drag-and-drop dashboard with broad device card coverage |
| S28 | [Fast Search Card](https://github.com/fastender/Fast-Search-Card) | Reference | Search-first dashboard, status center and adaptive navigation |
| S29 | [simUI](https://github.com/watari-dev/ha-simui) | Reference | Information-dense preset surfaces driven by HA registries |
| S30 | [Black Minimalist](https://github.com/jlnbln/Black-Minimalist) | Reference | Sections-aware modern dark dashboard and dependency discipline |
| S31 | [Prism Dashboard](https://github.com/BangerTech/Prism-Dashboard) | Reference | Glass-style reusable cards spanning media, energy, cleaning and printing |

## Family, Kitchen and Shared-Screen Sources

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S32 | [HA Family Hub](https://github.com/JVarhol/HA-Family-Hub) | Reference | Family calendar, meals, chores, routines and shared kiosk patterns |
| S33 | [Hearthglance](https://github.com/alexkibler/hearthglance) | Reference | Native HA family views for calendars, lists, meals and chores |
| S34 | [Kitchen Dashboard](https://github.com/bdunn44/kitchen-dashboard) | Reference | Portrait wall-tablet command center with rich pop-ups and household modules |
| S35 | [Home Assistant Family Panel](https://github.com/calebgab/Home-Assistant-Family-Panel) | Reference | Shared calendar, chores, reminders, presence and guest Wi-Fi patterns |
| S36 | [TaskMate](https://github.com/tempus2016/taskmate) | Reference | Kids, parents and wall-tablet chore/reward dashboards |

## Energy, Vehicle and Utility Sources

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S37 | [Solar Dashboard](https://github.com/jkir4n/solar-dashboard) | Reference | Solar, battery, grid and forecast visualization |
| S38 | [EVCC Card](https://github.com/mkshb/hass-evcc-card) | Reference | EV charging, site flow, battery and charging plans |
| S39 | [Tesla FrontEnd Card](https://github.com/ds2000/homeassistant-fe-tesla) | Reference | Vehicle state, charging, climate and access UI |
| S40 | [Energy Flow Card Plus](https://github.com/flixlix/energy-flow-card-plus) | Reference | Detailed animated power-flow visualization |
| S41 | [Smart Irrigation](https://github.com/altmenorg/HAsmartirrigation) | Reference | Zone irrigation control, weather/ET logic and dashboard panel |
| S42 | [NeverDry](https://github.com/never-dry/NeverDry) | Reference | Water-balance and per-zone irrigation status/action cards |

## Climate, Weather and Environmental Sources

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S43 | [Air Quality Card](https://github.com/wander00-1/ha-air-quality-card) | Reference | AQI, pollutants, comfort trends and threshold visualization |
| S44 | [Weather Station Core](https://github.com/kmich/ha_ws_core) | Reference | Vanilla, mobile, Bubble and enhanced weather dashboard variants |
| S45 | [Cloudless Multiroom Thermostat](https://github.com/BarBaar44/Cloudless-Multiroom-Thermostat) | Reference | Multi-room heating overview and room status patterns |
| S46 | [Weather Console Card](https://github.com/mycrouch/weather-console-card) | Reference | Dense weather-console presentation for dedicated panels |

## Security, Network and System Sources

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S47 | [Limited Access Dashboard](https://github.com/EndOfTheLine-HA/ha-limited-access-dashboard) | Reference | Restricted guest/child/contractor control surfaces |
| S48 | [UniFi Insights](https://github.com/tinkerologie/ha-unifi-insights) | Reference | Network topology, health, performance and Protect activity |
| S49 | [Homelable](https://github.com/Pouzor/homelable-hacs) | Reference | Interactive homelab/network topology in Home Assistant |
| S50 | [Kiosk Mode](https://github.com/00-10-01-11/ha-kiosk-mode) | Reference | Hiding HA chrome for wall displays |

## Floorplan, Appliance and Specialized Sources

| ID | Source | Class | Why it matters |
|---|---|---|---|
| S51 | [HA Floorplanner GUI](https://github.com/sleien/HA-floorplanner-gui) | Reference | Browser-drawn 2D floorplan exported to SVG/CSS/dashboard YAML |
| S52 | [Vacuum Agent](https://github.com/kingchddg901/Vacuum_Agent) | Reference | Live map, room cleaning, zones and vacuum health |
| S53 | [Roborock Dashboard](https://github.com/Red5Rebel/HA-Roborock-Dashboard) | Reference | Room selection, cleaning modes, consumables and dock status |
| S54 | [Bambu Lab Home Assistant](https://github.com/greghesp/ha-bambulab) | Reference | Built-in 3D-printer cards, camera, AMS and controls |
| S55 | [3D-Printer Control Center](https://github.com/Taracraft/3D-Printer-Control-Center) | Reference | Full 3D-print dashboard, queue and file-management patterns |
| S56 | [Laundry Dashboard Example](https://github.com/Ampersandman/Dreame-Home-Laundry) | Reference | Washer/dryer progress, program and controls |
| S57 | [Vacuum Orchestrator Card](https://github.com/hyperfelixations/vacuum-orchestrator-card) | Reference | Multi-robot queue, jobs, history and touch-first views |

## Curation Notes

1. A high-star repository is not automatically preferred over a smaller current project.
2. Native Home Assistant features win when they satisfy the use case cleanly.
3. A custom card earns a place when it adds interaction, density, visualization, or workflow that native cards do not provide well.
4. Archived or clearly superseded projects may be kept only as idea sources, never as default implementation guidance.
5. Every future dashboard built from this library should begin by mapping real Areas, Floors, Labels, Users and screen sizes before copying any visual pattern.
