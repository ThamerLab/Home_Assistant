# Home Assistant Dashboard Reference Library — 100 Patterns

Last reviewed: 2026-11-12

This catalog is the implementation reference used to design future Home Assistant dashboards in ThamerLab. It contains **100 reusable dashboard patterns** across whole-home control, rooms, mobile, wall tablets, climate, security, energy, family/media, infrastructure and specialized use cases.

The catalog is deliberately **native-first**. Community projects are used when they add meaningful interaction, density or visualization. See [SOURCES.md](./SOURCES.md) for the source registry and [PILOT_TEST.md](./PILOT_TEST.md) for the quality gate that was completed before this 100-pattern catalog was adopted.

## Reading the Catalog

- **View** is the preferred Home Assistant view type.
- **Native-first** is the implementation path to try before adding dependencies.
- **Optional layer** is a community card/framework that can improve the pattern.
- **Complexity** estimates build effort.
- **Risk** estimates future maintenance sensitivity to custom frontend changes.
- **Sources** refer to IDs in [SOURCES.md](./SOURCES.md).
- **Design rule** is the part worth carrying into future builds.

## Catalog

| ID | Category | Pattern | Best for | View | Native-first | Optional layer | Complexity | Risk | Sources | Design rule |
|---|---|---|---|---|---|---|---|---|---|---|
| D001 | Whole-home | Native Whole-Home Overview | Universal | Sections | Area cards + Tile cards + badges | None | Low | Low | S01,S03,S05,S06 | Use Areas as the primary information architecture; do not mirror the entity registry. |
| D002 | Whole-home | Active-Only Home | Universal | Sections | Visibility conditions on active lights, covers, media and alerts | Bubble Card or Mushroom | Low | Low | S03,S07,S11,S12 | Keep the default surface calm; show exceptions and active states, not every device. |
| D003 | Whole-home | Floor-by-Floor Home | Tablet/Desktop | Sections | One section per Floor with Area cards | Hemma | Low | Low | S03,S06,S10 | Use floor hierarchy for navigation when the home has many rooms. |
| D004 | Whole-home | Status Bar + Room Grid | Universal | Sections | Header badges for weather/presence/alerts + room Area cards | Mushroom chips | Low | Low | S03,S06,S12 | Put global state in the header and room-specific state in the grid. |
| D005 | Whole-home | Apple-Home Style Summary | Universal | Sections | Compact Area/Tile cards with state color | Hemma or simUI | Medium | Low | S05,S06,S10,S29 | Use color only for state and exceptions; keep inactive surfaces neutral. |
| D006 | Whole-home | Auto-Generated Area Overview | Universal | Sections | Automatic sections and Area registry | Atrium or Dwains Next | Medium | Medium | S03,S18,S22 | Prefer registry-driven generation when device churn is high. |
| D007 | Whole-home | Search-First Home | Phone/Desktop | Panel | Native dashboard links and entity search | Fast Search Card | Medium | Medium | S28,S01 | Use search as a fallback for long-tail devices, not as the only navigation. |
| D008 | Whole-home | One-Screen Command Center | Large tablet | Sections | Dense sections for rooms, weather, security, media and climate | Panalume or Prism | High | Medium | S27,S31,S34 | Reserve one-screen density for large always-on displays; avoid shrinking touch targets. |
| D009 | Whole-home | Day/Night Context Home | Universal | Sections | Time and sun visibility conditions | Bubble Card | Medium | Low | S07,S11 | Swap context by time without moving core controls between unpredictable locations. |
| D010 | Whole-home | Guest-Safe Home | Phone/Tablet | Sections | User visibility + only safe Tiles/Scenes | Limited Access Dashboard | Medium | Medium | S07,S47 | Expose scenes and bounded controls; hide admin, locks, system and destructive actions. |
| D011 | Rooms | Standard Room Control | Universal | Sections | Heading + lights + climate + covers + sensors | Mushroom | Low | Low | S03,S05,S12 | Use the same room skeleton everywhere so navigation becomes muscle memory. |
| D012 | Rooms | Bedroom Night Room | Phone/Bedside | Sections | Low-light scenes, climate, blinds, fan and sleep status | Bubble Card | Medium | Low | S07,S11,S19 | Prioritize one-tap sleep actions and avoid bright graphs at night. |
| D013 | Rooms | Living Room Media Room | Tablet/Phone | Sections | Media player + lights + climate + covers | Bubble Card or Prism | Medium | Low | S11,S31 | Put playback and scene actions above device-level controls. |
| D014 | Rooms | Kitchen Utility Room | Wall tablet | Sections | Lights, appliances, timers, calendar and shopping list | Family Hub | Medium | Medium | S32,S33,S34 | Mix household workflow with controls, but keep safety-critical appliance actions explicit. |
| D015 | Rooms | Bathroom Occupancy Room | Phone/Tablet | Sections | Lights, fan, humidity, occupancy and automation status | Mushroom | Low | Low | S05,S12 | Show automation state and manual override; avoid exposing raw helper entities. |
| D016 | Rooms | Office Productivity Room | Desktop/Tablet | Sections | Lights, climate, desk power, presence, focus scene | Hemma | Medium | Low | S10,S19 | Lead with work modes/scenes; put diagnostics behind secondary actions. |
| D017 | Rooms | Garage / Workshop Room | Tablet | Sections | Door, lights, presence, tools, temperature and cameras | Bubble Card | Medium | Medium | S11,S47 | Put door state and safety alerts above convenience controls. |
| D018 | Rooms | Outdoor / Patio Room | Phone/Tablet | Sections | Lighting, irrigation, weather, gate and outdoor sensors | Smart Irrigation | Medium | Medium | S41,S42,S44 | Pair outdoor actions with weather and safety context. |
| D019 | Rooms | Multi-Zone Master Suite | Tablet | Sections | Bedroom, dressing and bathroom sub-sections | Hemma | Medium | Low | S10,S03 | Use sub-areas visually without creating a separate dashboard for every adjacent space. |
| D020 | Rooms | Room Popup Navigation | Phone/Tablet | Sections | Area summary cards navigate or open detail surfaces | Bubble Card | Medium | Medium | S06,S11 | Keep overview cards shallow; use popups for detail, not for essential emergency actions. |
| D021 | Mobile | Bottom-Navigation Mobile Home | Phone | Sections | Four to five views with native navigation structure | Mobile First or Hemma | Medium | Low | S10,S21 | Keep primary navigation reachable by thumb and limit top-level destinations. |
| D022 | Mobile | One-Hand Quick Actions | Phone | Sections | Large Tiles for lights, lock, garage, scenes and climate | Mushroom | Low | Low | S05,S12 | Prefer big targets and one-tap actions; push detail into more-info. |
| D023 | Mobile | Personal Presence & Commute | Phone | Sections | Person, zones, travel sensors, weather and arrival scenes | Mushroom | Medium | Low | S07,S12 | Make it user-specific with visibility rules rather than duplicating global home status. |
| D024 | Mobile | Security Pocket View | Phone | Sections | Alarm, locks, garage, door sensors and camera snapshots | Bubble Card | Medium | Medium | S07,S11,S47 | Keep arm/disarm and access actions separated from passive camera viewing. |
| D025 | Mobile | Climate Pocket View | Phone | Sections | Thermostat Tiles with HVAC features + comfort sensors | Mushroom | Low | Low | S05,S12,S45 | Use native climate features first; avoid full thermostat cards when a Tile is sufficient. |
| D026 | Mobile | Media Remote | Phone | Panel | Primary media player controls and source/volume actions | Prism or Bubble Card | Medium | Low | S11,S31 | Make transport controls persistent and keep source selection secondary. |
| D027 | Mobile | Car & EV Pocket View | Phone | Sections | Vehicle battery, range, lock, climate and charging | Tesla card or EVCC card | Medium | Medium | S38,S39 | Separate vehicle controls from charging-site controls to avoid accidental actions. |
| D028 | Mobile | Maintenance Alerts | Phone | Sections | Low batteries, unavailable devices, updates and failures | auto-entities | Medium | Low | S09,S16 | Only show items needing attention; an empty maintenance view is success. |
| D029 | Mobile | Night / Sleep Dashboard | Phone | Sections | Low-brightness scenes, doors, climate, media stop and alarm state | Bubble Card | Medium | Low | S07,S11 | Minimize color and motion; require confirmation for disruptive whole-home actions. |
| D030 | Mobile | Adaptive Single Dashboard | Phone/Tablet/Desktop | Sections | Screen visibility conditions and responsive sections | Adaptive Mushroom | High | Medium | S07,S20 | Adapt card density per screen while preserving control locations and labels. |
| D031 | Wall | Landscape Wall Tablet | Wall tablet | Sections | Large room tiles, weather, security, climate and scenes | Hemma | Medium | Low | S10,S19 | Use 3–4 columns, large targets and persistent global status. |
| D032 | Wall | Portrait Kitchen Tablet | Wall tablet | Sections | Calendar, weather, family, timers, rooms and quick actions | Kitchen Dashboard | High | Medium | S32,S33,S34 | Design vertically from the start; do not squeeze a landscape dashboard into portrait. |
| D033 | Wall | Hallway Glance Panel | Wall display | Sections | Time, weather, presence, doors, active lights and scenes | Mushroom | Low | Low | S12,S24 | Optimize for a two-second glance; avoid deep controls. |
| D034 | Wall | Bedside Dashboard | Small tablet | Sections | Clock, sleep scene, climate, blinds and low light | HAven | Low | Low | S24,S07 | Make nighttime controls local and predictable; hide household administration. |
| D035 | Wall | Old Tablet Lightweight | Old tablet | Panel | Static HTML or minimal native cards | HAven or Koti | Medium | Low | S24,S25 | Reduce animations, charts and custom CSS; prioritize render performance. |
| D036 | Wall | Kiosk + Screensaver | Wall tablet | Panel | Dashboard plus idle clock/photo/weather state | Dashboard Builder + Kiosk Mode | Medium | Medium | S26,S50 | Treat kiosk chrome removal and screensaver behavior as display concerns, not dashboard logic. |
| D037 | Wall | Doorbell Wake Panel | Wall tablet | Panel | Camera-focused panel shown on doorbell/motion event | Kiosk tooling | High | Medium | S23,S50 | Return automatically to the home surface after the event; never strand the display on a camera. |
| D038 | Wall | Family Command Center | Wall tablet | Panel | Calendar, chores, meals, lists, weather and safe smart-home actions | Family Hub | High | Medium | S32,S33,S35,S36 | Household workflow should dominate; smart-home controls are supporting tools. |
| D039 | Wall | Security Camera Wall | Large display | Panel | Camera grid + alarm/door summary | Bubble Card | Medium | Medium | S47,S11 | Use live video selectively; too many streams can overwhelm clients and networks. |
| D040 | Wall | Wall Floorplan | Large tablet | Panel | Picture Elements or SVG floorplan | Floorplanner GUI | High | Medium | S08,S51 | Use spatial control where physical location matters; keep a non-floorplan fallback view. |
| D041 | Climate | Whole-Home Climate Overview | Tablet/Desktop | Sections | Climate dashboard patterns grouped by Floor/Area | None | Low | Low | S09,S03 | Show setpoint, actual temperature and HVAC action; hide rarely used modes. |
| D042 | Climate | Per-Room Thermostat Detail | Universal | Sections | Thermostat or Tile with HVAC/fan/swing features | Mushroom | Low | Low | S05,S12 | Use the smallest control that exposes every capability the user actually uses. |
| D043 | Climate | Comfort + Air Quality | Tablet/Desktop | Sections | Temperature, humidity, CO2/AQI and trends | Air Quality Card | Medium | Low | S43,S44 | Separate comfort metrics from health alerts and apply clear thresholds. |
| D044 | Climate | HVAC Diagnostics | Desktop | Sections | Entity/Statistic cards for runtime, action, pressure/fault sensors | auto-entities | Medium | Low | S16,S45 | Keep diagnostics off everyday dashboards; make faults visible globally. |
| D045 | Climate | Humidity / Mold Risk | Phone/Tablet | Sections | Humidity, dew point, ventilation and warning visibility | Air Quality Card | Medium | Low | S43,S07 | Show warnings only when thresholds are crossed; do not make raw history the hero. |
| D046 | Climate | Bedroom Sleep Climate | Phone/Bedside | Sections | Climate, fan, humidity, sleep preset and window state | Mushroom | Low | Low | S12,S45 | Tie controls to sleep outcomes, not to every HVAC attribute. |
| D047 | Climate | Multi-Split AC Overview | Tablet | Sections | One compact Tile per zone + master summary | Hemma | Medium | Low | S05,S10 | Keep per-zone controls consistent and reserve expanded detail for the selected room. |
| D048 | Climate | Ventilation / Exhaust Dashboard | Tablet | Sections | Fans, humidity, AQI, occupancy and runtime | Mushroom | Medium | Low | S12,S43 | Show automatic/manual state clearly so users understand why fans are running. |
| D049 | Climate | Weather-Aware Climate | Tablet/Desktop | Sections | Outdoor weather + indoor comfort + windows/covers | Weather Station Core | Medium | Low | S44,S07 | Place weather next to decisions it affects; avoid decorative forecast duplication. |
| D050 | Climate | Climate Energy Optimization | Desktop | Sections | HVAC consumption, tariff, comfort bands and schedules | Solar Dashboard | High | Medium | S37,S40,S45 | Show comfort and cost together; never optimize energy without exposing comfort impact. |
| D051 | Security | Security Overview | Universal | Sections | Alarm, locks, cameras, doors, motion and alerts grouped by Area | None | Low | Low | S09,S03 | Follow the built-in Security dashboard model before adding custom chrome. |
| D052 | Security | Door & Window Status | Phone/Tablet | Sections | Entity filters/visibility for open contacts | auto-entities | Low | Low | S07,S16 | Show only open or abnormal contacts in the primary alert section. |
| D053 | Security | Camera Matrix | Tablet/Desktop | Panel | Picture Entity / camera cards in a dedicated grid | Bubble Card | Medium | Medium | S09,S11 | Use snapshots in overview; reserve live streams for selected cameras. |
| D054 | Security | Alarm Control Center | Wall/Phone | Sections | Alarm panel + key status + nearby cameras | None | Medium | Medium | S09,S47 | Separate arm/disarm from unrelated controls and require deliberate disarm interaction. |
| D055 | Security | Presence & Occupancy Overview | Universal | Sections | People, zones, area occupancy and motion summaries | Hemma | Medium | Low | S07,S10 | Differentiate person presence from motion/occupancy sensors. |
| D056 | Security | Guest / Contractor Access | Phone | Sections | Time/user restricted controls only | Limited Access Dashboard | Medium | Medium | S47,S07 | Use least privilege and bounded time windows; do not expose general HA navigation. |
| D057 | Security | Lock + Garage Access | Phone/Wall | Sections | Locks, garage doors, gate cameras and confirmations | Bubble Card | Medium | Medium | S11,S47 | Require confirmation for remote open/unlock; show current state adjacent to the action. |
| D058 | Security | Critical Safety Alerts | Universal | Sections | Smoke, CO, water leak and critical device warnings | None | Low | Low | S07,S09 | Critical alerts must override aesthetic minimalism and be visible without navigation. |
| D059 | Security | Night Perimeter | Phone/Bedside | Sections | Doors, windows, garage, locks, motion and alarm state | Mushroom | Low | Low | S07,S12 | Make the bedtime question simple: is the perimeter secure, yes or no? |
| D060 | Security | Security Activity Timeline | Tablet/Desktop | Sections | Activity/history + cameras + recent security entities | UniFi Insights | Medium | Medium | S09,S48 | Use timeline for investigation, not as the first surface for urgent state. |
| D061 | Energy | Native Energy Overview | Desktop/Tablet | Built-in | Home Assistant Energy dashboard | None | Low | Low | S09,S01 | Use the native energy model as the source of truth before duplicating it. |
| D062 | Energy | Solar + Battery Flow | Tablet/Desktop | Sections | Energy cards for solar, grid, battery and home | Energy Flow Card Plus | Medium | Low | S37,S40 | Animate direction only when it helps comprehension; keep numeric power visible. |
| D063 | Energy | Tariff / Cost Dashboard | Desktop | Sections | Statistics and cost sensors by period | None | Medium | Low | S04,S37 | Separate instantaneous power from accumulated cost and energy. |
| D064 | Energy | Circuit / Appliance Power | Desktop/Tablet | Sections | Top consumers + history/statistics | auto-entities | Medium | Low | S16,S40 | Rank actionable loads; do not dump every power sensor at equal weight. |
| D065 | Energy | EV Charging Site | Phone/Tablet | Sections | Charger power, SoC, plan, tariff and site flow | EVCC Card | Medium | Low | S38 | Make start/stop and charge limit obvious; keep advanced planning one level deeper. |
| D066 | Energy | Vehicle Control Dashboard | Phone | Sections | Battery, range, climate, doors and charge port | Tesla Card | Medium | Medium | S39 | Use clear remote-action confirmations and distinguish stale vehicle data. |
| D067 | Energy | Water Consumption | Desktop/Tablet | Sections | Current flow, daily use, leaks and historical usage | None | Medium | Low | S04,S09 | Treat unexpected continuous flow as an alert, not just a chart anomaly. |
| D068 | Energy | Gas / Heating Energy | Desktop | Sections | Gas/heat energy, climate demand, boiler state | None | Medium | Low | S09,S45 | Correlate consumption with heating demand and outside temperature. |
| D069 | Energy | Irrigation Water Dashboard | Tablet | Sections | Zones, flow, runtime, weather and water balance | Smart Irrigation | Medium | Medium | S41,S42 | Always pair manual watering with valve state and safety feedback. |
| D070 | Energy | Sustainability KPI Board | Desktop/Wall | Sections | Solar share, grid import, self-consumption, water and efficiency KPIs | Solar Dashboard | Medium | Low | S37,S40 | Use a few stable KPIs; avoid turning sustainability into a wall of gauges. |
| D071 | Media | Whole-Home Now Playing | Tablet | Sections | Active media players + volume + source | Bubble Card | Medium | Low | S11,S31 | Show active players first and hide idle players unless needed. |
| D072 | Media | TV / AV Remote | Phone/Tablet | Panel | Media player plus scene/script remote controls | Prism | Medium | Low | S31,S14 | Group by activity such as Watch TV, not by individual receiver/input entities. |
| D073 | Media | Multi-Room Music | Tablet | Sections | Room players, groups, volume and favorites | Bubble Card | Medium | Low | S11,S34 | Make grouping and volume safe; avoid simultaneous full-volume actions. |
| D074 | Media | Scheduled Audio / Recitation | Phone/Tablet | Sections | Playback state, target player, schedule and manual safe toggle | Mushroom | Medium | Low | S12,S14 | Expose what is playing and where before exposing schedule controls. |
| D075 | Family | Family Calendar Wall | Wall tablet | Panel | Calendar, weather, next events and person color coding | Hearthglance | Medium | Low | S32,S33,S35 | Calendar readability beats smart-home density on shared family screens. |
| D076 | Family | Chores + Rewards | Wall/Tablet | Panel | Assignments, completion, streaks and rewards | TaskMate | High | Medium | S36,S32 | Keep completion one-tap and make parent/admin actions separate. |
| D077 | Family | Meals + Shopping | Kitchen tablet | Panel | Meal plan, recipes, shopping and expiring items | Family Hub | High | Medium | S32,S33 | Optimize for meal workflow; avoid mixing unrelated device controls into the main grid. |
| D078 | Lifestyle | Morning Routine | Phone/Wall | Sections | Weather, calendar, commute, lights, blinds and scenes | Mushroom | Medium | Low | S07,S12 | Use context visibility so morning content disappears later in the day. |
| D079 | Lifestyle | Evening / Goodnight Routine | Phone/Bedside | Sections | Perimeter, lights, media, climate and goodnight scene | Bubble Card | Medium | Low | S07,S11 | Summarize unresolved issues before the Goodnight action runs. |
| D080 | Lifestyle | Ambient Photo Frame | Wall display | Panel | Photos, clock, weather and subtle status overlay | Dashboard Builder | Medium | Low | S26,S32 | Ambient mode should be visually quiet and return instantly to controls on interaction. |
| D081 | System | Home Assistant Health | Desktop | Sections | Core status, CPU/RAM/storage, database and uptime | None | Medium | Low | S04,S29 | Show health indicators and trends; avoid raw sensor dumps. |
| D082 | System | Updates + Maintenance | Desktop/Phone | Sections | Updates, low batteries, unavailable entities and maintenance items | auto-entities | Medium | Low | S09,S16 | The view should empty itself when everything is healthy. |
| D083 | System | UniFi / Network Operations | Desktop/Tablet | Panel | Topology, WAN, APs, switches, clients and Protect health | UniFi Insights | High | Medium | S48 | Use topology for diagnosis; use a small site-health summary for daily operation. |
| D084 | System | Proxmox / Containers | Desktop | Sections | Hosts, VMs, containers, CPU/RAM and status | Homelable | High | Medium | S49 | Separate host health from service availability and user-facing outages. |
| D085 | System | NAS / Storage / Backup | Desktop | Sections | Capacity, SMART, backup recency and errors | None | Medium | Low | S04,S49 | Make backup age and failure more prominent than raw storage telemetry. |
| D086 | System | Battery Fleet | Phone/Desktop | Sections | Low batteries grouped by Floor/Area | auto-entities | Low | Low | S09,S16 | Sort by urgency and hide healthy batteries by default. |
| D087 | System | Zigbee / Z-Wave Health | Desktop | Sections | Unavailable nodes, battery, link quality and coordinator status | auto-entities | Medium | Medium | S16,S49 | Treat link quality as diagnostic context, not as a daily KPI. |
| D088 | System | Internet + Uptime | Wall/Desktop | Sections | WAN state, latency, critical services and outage history | UniFi Insights | Medium | Low | S48,S49 | Distinguish internet failure from local service failure. |
| D089 | System | Automation Diagnostics | Desktop | Sections | Failed/unavailable helpers, automation traces links and recent errors | None | High | Low | S04,S28 | Keep diagnostics actionable: show what failed, when, and where to investigate. |
| D090 | System | Home NOC Command Center | Large desktop/wall | Panel | Network, servers, HA, storage, backups and security health | Homelable + UniFi Insights | High | Medium | S48,S49 | Use red only for actionable faults; avoid permanently alarming normal high utilization. |
| D091 | Specialized | 2D Interactive Floorplan | Tablet/Desktop | Panel | Picture Elements over a floor image | Floorplanner GUI | High | Medium | S08,S51 | Use spatial state for lights, doors and temperature; keep text controls reachable. |
| D092 | Specialized | 3D / Visual House Plan | Large tablet | Panel | Rendered house image with state overlays | card-mod/button-card as needed | High | High | S08,S14,S15 | Treat 3D as a visualization layer, not as the only control path. |
| D093 | Specialized | Robot Vacuum Map | Phone/Tablet | Panel | Vacuum map, rooms, zones, status and consumables | Vacuum Agent | High | Medium | S52,S53,S57 | Map interaction should lead; maintenance and history should stay secondary. |
| D094 | Specialized | Laundry Center | Wall/Phone | Sections | Washer/dryer state, remaining time, finish time and alerts | Laundry card | Medium | Medium | S56 | Show finished-but-not-unloaded as a household task, not merely an appliance state. |
| D095 | Specialized | 3D Printer Center | Desktop/Tablet | Panel | Camera, progress, temperatures, AMS/material and controls | Bambu Lab cards | High | Medium | S54,S55,S31 | Put Stop behind confirmation; surface print errors and remaining time prominently. |
| D096 | Specialized | Garden + Irrigation | Tablet | Sections | Zones, soil/weather, valves, water balance and manual run | Smart Irrigation | Medium | Medium | S41,S42,S44 | Manual controls must show active valve and water-flow feedback. |
| D097 | Specialized | Pool / Spa Control | Tablet | Sections | Temperature, pumps, heater, cover, chemistry and scenes | Tile cards | Medium | Medium | S05,S14 | Separate dangerous/heavy-load actions from everyday temperature and lighting controls. |
| D098 | Accessibility | Large-Touch Accessible Home | Tablet | Sections | Large Tiles, high contrast, plain labels and limited navigation | Mushroom | Low | Low | S05,S12 | Prefer clarity over density; never encode critical state by color alone. |
| D099 | Accessibility | Child / Guest Restricted Home | Phone/Tablet | Sections | User-specific safe controls and scenes | Limited Access Dashboard | Medium | Medium | S07,S47 | Expose only the minimum set of devices and avoid irreversible actions. |
| D100 | Universal | Universal Adaptive Reference Dashboard | Phone/Tablet/Desktop | Sections | Native Areas + responsive visibility + consistent room skeleton + maintenance exceptions | Hemma/Bubble/Mushroom only where justified | High | Low | S03,S05,S06,S07,S10,S11,S12 | This is the capstone pattern: native-first, registry-driven, responsive, calm by default, detailed on demand. |

## Category Coverage

| Category | IDs | Count |
|---|---|---:|
| Whole-home | D001–D010 | 10 |
| Rooms | D011–D020 | 10 |
| Mobile | D021–D030 | 10 |
| Wall | D031–D040 | 10 |
| Climate | D041–D050 | 10 |
| Security | D051–D060 | 10 |
| Energy | D061–D070 | 10 |
| Media / Family / Lifestyle | D071–D080 | 10 |
| System | D081–D090 | 10 |
| Specialized / Accessibility / Universal | D091–D100 | 10 |

**Total: 100 patterns.**

## Default Selection Logic for Future Builds

When choosing a pattern for a real home:

1. Start with **D001 Native Whole-Home Overview**.
2. Map Floors, Areas, Labels and Users correctly before styling.
3. Use **D011 Standard Room Control** as the repeatable room skeleton.
4. Add device-specific views only when they improve a real workflow.
5. Use **D028 / D082** for exception-driven maintenance instead of exposing system clutter everywhere.
6. Add a dedicated mobile or wall pattern only when screen behavior materially differs.
7. Use custom cards to solve a specific interaction problem, never merely because they are fashionable.
8. Keep safety and access actions visually distinct and require confirmation where appropriate.
9. Prefer progressive disclosure: summary first, detail on tap.
10. Re-test dependencies and responsive behavior before any dashboard is declared complete.

## Capstone Recommendation

For a new multi-device home dashboard, the library's default architecture is **D100**:

- Native Sections layout.
- Area/room registry as the information architecture.
- Native Tile and Area cards for common controls.
- Conditional visibility for context and exceptions.
- A consistent room template.
- Separate maintenance/system surfaces.
- Bubble Card, Mushroom, Hemma, button-card or other custom tools only when a clearly defined requirement justifies them.
