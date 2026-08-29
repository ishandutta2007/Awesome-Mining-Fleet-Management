# Awesome-Mining-Fleet-Management

## Top Fleet Management (Mining) Platforms Ecosystem
**Curated List of SaaS Products & Open-Source GitHub Projects**
*Focused on Mine Dispatch, Haul Truck Optimization, Equipment Telemetry, Production Tracking & Autonomous Fleet Coordination*
**Last updated: August 2026**

This repository tracks notable **SaaS / industrial platforms** and **open-source projects** for **Mining Fleet Management**. These systems optimize truck–shovel assignment, track mobile equipment, reduce queue time, and integrate with production and safety systems in surface and underground mines.

**Examples** include Hexagon Mining, Modular Mining, Wenco, Micromine Pitram, Epiroc Mobilaris, Sandvik OptiMine, RPMGlobal, Aitik Fleet, ASI Mining, and GroundHog (the category leaders).

**Open-source emphasis**: Industrial mining fleet management and dispatch is almost entirely commercial. There is no widely adopted open-source equivalent to DISPATCH, MineOperate, or Pitram. Related open building blocks exist for telemetry, GIS, and general fleet tracking; crypto-ASIC “fleet” tools are unrelated to mine haulage. This section is honest about that gap.

Contributions welcome! Open a PR to add/update entries. Keep descriptions factual and link to official sites.

## Table of Contents
- [SaaS/Hosted Platforms](#saas-products)
- [Open-Source GitHub Projects](#open-source-github-projects)
- [How to Contribute](#how-to-contribute)
- [Disclaimer](#disclaimer)

## SaaS/Hosted Platforms
- **[Hexagon Mining (MineOperate / OP Pro)](https://hexagon.com/)**  
  Enterprise mine fleet management and operations platform — dispatch, equipment tracking, and production integration for surface mining.

- **[Modular Mining (DISPATCH)](https://www.modularmining.com/)**  
  Industry-standard fleet management and dynamic truck assignment system (Komatsu) used at major surface mines worldwide.

- **[Wenco](https://www.wencomine.com/)**  
  OEM-agnostic fleet management system focused on surface mining — telemetry, optimization, and production intelligence (Hitachi Construction Machinery).

- **[Micromine Pitram](https://www.micromine.com/)**  
  Mine control and fleet/production management solution for real-time operational visibility and short-interval control.

- **[Epiroc Mobilaris](https://www.epiroc.com/)**  
  Underground and surface positioning, traffic, and fleet-related solutions for mining operations.

- **[Sandvik OptiMine](https://www.rocktechnology.sandvik/)**  
  Underground mining information and process optimization suite integrating equipment and people data.

- **[RPMGlobal](https://rpmglobal.com/)**  
  Mining software suite including fleet and mine management capabilities alongside planning and simulation tools.

- **[Aitik Fleet / site-specific fleet systems](https://www.boliden.com/)**  
  Examples of large-site or OEM-integrated fleet management deployments at major operations.

- **[ASI Mining](https://www.asirobots.com/)**  
  Autonomous and semi-autonomous mining vehicle and fleet coordination technology (associated with Epiroc).

- **[GroundHog](https://www.groundhogapps.com/)**  
  Open-pit and underground fleet and operations applications for monitoring, dispatch support, and production tracking.

## Open-Source GitHub Projects
- **[General open telematics and GPS tracking stacks](https://github.com/)**  
  Self-hosted GPS/AVL platforms (e.g. Traccar-style) that can track vehicles but lack mine-specific dispatch optimization.

- **[Open GIS and mine mapping tools](https://github.com/)**  
  QGIS, PostGIS, and open spatial stacks used for pit maps, roads, and geofences that feed commercial FMS.

- **[MQTT / industrial IoT open brokers](https://github.com/)**  
  Message brokers and collectors used to ingest equipment telemetry into site historians or custom dashboards.

- **[Open time-series databases for equipment data](https://github.com/)**  
  InfluxDB, TimescaleDB, and similar stores for high-frequency machine metrics outside the FMS.

- **[Grafana and open operational dashboards](https://github.com/)**  
  Visualization of production and equipment KPIs when data is exported from commercial fleet systems.

- **[Open simulation and optimization libraries](https://github.com/)**  
  OR-Tools and similar solvers sometimes used in research or custom short-interval control experiments (not production FMS).

- **[Mine planning open research tools](https://github.com/)**  
  Academic and research code for scheduling and haulage modeling — not certified for operational dispatch.

- **[Safety and proximity open prototypes](https://github.com/)**  
  Experimental proximity and collision-awareness projects (must never replace certified CAS).

- **[Data export and historian open connectors](https://github.com/)**  
  Scripts that pull cycle times and tonnage from commercial FMS APIs into open analytics environments.

- **[Note on crypto-miner “fleet” software](https://github.com/)**  
  Open tools for managing Bitcoin/ASIC miner farms exist but are **not** applicable to mining haul trucks, shovels, or underground fleets.

### Additional Strong Open-Source Options
- Using open telematics only for non-critical visibility or contractor light vehicles.
- Exporting FMS cycle and delay data into open analytics for continuous improvement studies.
- Maintaining pit geometry and road networks in open GIS for planning and emergency response.
- Never relying on open or experimental code for primary dispatch, collision avoidance, or autonomous control.
- Participating in industry standards work (data interfaces, OEM telemetry) rather than expecting a full open FMS.

**Frameworks for building custom systems**: There is no practical open-source replacement for production mining fleet management. Sites run **Hexagon, Modular DISPATCH, Wenco, Pitram, OptiMine, GroundHog**, or OEM suites (e.g. Cat MineStar) as the system of record for assignment and safety-critical tracking. Open tools can support secondary analytics, mapping, and research. Autonomy and collision avoidance require certified commercial systems.

## How to Contribute
1. Fork the repo.
2. Add/edit entries in `README.md` (follow existing format).
3. Include: name, link, 1–2 sentence description, and whether it's SaaS or open-source.
4. Submit PR with a short explanation.

Star the repo if you find it useful!

## Disclaimer
- This is a **community-curated** list — not exhaustive and not an endorsement.
- Mining fleet management is safety- and production-critical. Incorrect dispatch or disabled safety systems can cause serious incidents. Open-source or experimental software must not be used for primary truck assignment, collision avoidance, or autonomous operation. Always follow OEM and site procedures, and involve qualified mining engineers and OT security teams.
- This list is not operational or safety advice.

---
**Made for mine operations, fleet engineers, and technology teams optimizing haulage under real constraints.**
Let's keep production data useful while recognizing that certified commercial FMS remains essential underground and on the pit floor.
