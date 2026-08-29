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
- [SaaS/Hosted Platforms](#saashosted-platforms)
- [Open-Source GitHub Projects](#open-source-github-projects)
- [How to Contribute](#how-to-contribute)
- [Disclaimer](#disclaimer)

## SaaS/Hosted Platforms

| Platform | Primary Focus & Capabilities | Starting Pricing | Free Tier / Trial Limits |
| :--- | :--- | :--- | :--- |
| **[GroundHog](https://groundhogapps.com/)** | Cloud FMS, short-interval control, and production tracking for open-pit and underground mines. | Starts at **$20,000/year** (or ~$1,666/month pay-per-project contractor baseline). | **6-week free on-site pilot program** (no credit card required; full modular access). |
| **[Caterpillar MineStar](https://www.cat.com/en_US/products/new/technology/minestar.html)** | Cloud-connected equipment tracking, production recording, terrain guidance, and dispatch (MineStar Edge & Fleet). | Starts at **$3,000/year site base fee + ~$250/asset/month** (MineStar Edge cloud tier). | **180-day free trial** of Health Equipment Insights on new Cat machines; **30–90 day** dealer demo kit pilots. |
| **[Fleetio](https://www.fleetio.com/)** | Cloud fleet operations, preventative maintenance schedules, inspections, fuel, and equipment telematics aggregation. | Starts at **$4/vehicle/month** (billed annually, 5-vehicle minimum = **$20/month** starting cost). | **14-day free trial** (no credit card required; full platform access for all registered vehicles). |
| **[Micromine Pitram](https://www.micromine.com/pitram/)** | Real-time mine control, automated haulage dispatch, short-interval control, and equipment telemetry. | Starts at **$250 AUD/day** (~$5,000 AUD/month modular subscription tier). | **30-day free trial** on select modules (e.g. Alastri with consulting setup); **100% free academic access** via Micromine University Program. |
| **[Samsara](https://www.samsara.com/)** | Heavy machinery & mining support fleet telematics, real-time GPS tracking, AI safety cameras, and CAN diagnostics. | Starts at **$27/vehicle/month** (software subscription + ~$99 hardware gateway; 3-year term). | **30-day hardware & software trial** (30-day money-back guarantee / full refund return window). |
| **[Trackunit](https://www.trackunit.com/)** | Off-highway machine telematics, heavy equipment health, CAN-bus integration, and utilization monitoring. | Starts at **$15/asset/month** (base Raw/Spot telematics software tier; 36-month agreement). | **30-day free pilot evaluation** on up to 5 machines upon technical consultation. |
| **[Geotab](https://www.geotab.com/)** | Ruggedized heavy-duty vehicle telematics, engine diagnostics, fuel monitoring, and site safety analytics. | Starts at **$30/vehicle/month** (bundled GO hardware + Pro telematics tier). | **30-day free pilot** for up to 20 vehicles (free demo units shipped); **30-day free trial** for Altitude analytics. |
| **[Hexagon Mining (HxGN MineOperate)](https://hexagon.com/products/product-groups/mineoperate)** | Surface/underground dispatch optimization, machine guidance, payload monitoring, and autonomous coordination. | Starts at **$25,000/site/year** (OP Foundation / entry telematics tier). | **30 to 60-day enterprise Proof-of-Concept (POC)** on selected production equipment with engineer support. |
| **[Modular Mining (Komatsu DISPATCH)](https://www.modularmining.com/)** | Real-time dynamic truck-shovel assignment, LP haulage optimization, and open-pit fleet management. | Starts at **$30,000/year** (base modular site license subscription for mid-sized operations). | **30-day guided operational simulation & site POC demo** on active haul profiles. |
| **[Wenco Mine Systems](https://www.wencomine.com/)** | OEM-agnostic open-pit fleet management, high-precision GPS machine guidance, and production dispatch (Hitachi). | Starts at **$22,000/site/year** (Wenco Lite / production tracking entry baseline). | **30-day on-site pilot demonstration program** with pre-configured mobile tablet hardware. |
| **[Sandvik OptiMine](https://www.rocktechnology.sandvik/en/products/digital-mining-solutions/optimine/)** | Underground digital operations suite, 3D spatial machine tracking, schedule compliance, and production analytics. | Starts at **$24,000/year** (modular starter package for underground mobile asset tracking). | **30-day site digital twin simulation pilot** with dedicated application specialist support. |
| **[Epiroc Mobilaris](https://www.epiroc.com/)** | Underground 3D positioning, situational awareness, traffic control, and mobile machine monitoring. | Starts at **$20,000/year** (Mobilaris Mining Intelligence entry monitoring package). | **30-day virtual site model pilot / proof of concept** with custom mine layout. |
| **[RPMGlobal](https://rpmglobal.com/)** | Mining asset management, maintenance lifecycle tracking, fleet scheduling, and simulation (AMT/MinePlanner). | Starts at **$18,000/year** (entry AMT asset management subscription). | **30-day guided software trial & personalized sandbox demo** with sample fleet data. |
| **[ASI Mining](https://www.asirobots.com/)** | OEM-agnostic autonomous haulage systems (AHS), semi-autonomous command, and multi-vehicle dispatch (Mobius). | Starts at **$35,000/year** (Mobius Core baseline coordination software license). | **30-day virtual simulation testbed trial** with digital autonomous haulage scenario evaluation. |

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
