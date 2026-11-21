# First Mate — Requirements (Draft)

Status: DRAFT, version 0.4. This is the initial requirements document. It is not complete.

Change history:
- 0.1 (18 Nov 2026): FR-CHART added.
- 0.2 (18 Nov 2026): CORE subsystem added. DEC-001 recorded. Zora teardown findings added as design inputs. Questions to answer aboard added.
- 0.3 (19 Nov 2026): CORE-PRN (degraded-mode paper record) added as section 3.10. AC-CORE-8 to AC-CORE-13 and Silent Drift risks added. Print items in 5.4 and 5.6 moved to CORE-PRN. Questions Q-13 and Q-14 added. AC-CORE-6 reference corrected from section 6.6 to section 5.7.
- 0.4 (21 Nov 2026): Moved from the claude.ai Project into the repository (ADR-0003). DEC-001 recorded as ADR-0002. No change to requirement text.

Conventions:
- Each requirement has an ID, a subsystem owner, and a stakes tier.
- "Must" marks a mandatory requirement. "Should" marks a recommended requirement.
- [STACK] marks an item that depends on the tech stack decision. The stack is not chosen.
- [VERIFY] marks an item that depends on a fact that we have not confirmed.
- [ABOARD] marks an item that we can answer only on the boat (from mid-December 2026).
- Default values are starting values. Tests at sea will set the final values.

---

## 1. Scope and subsystems

Current scope: read-only advisory, with one exception (DEC-001). First Mate does not control engines, autopilot, or other equipment.

| ID | Subsystem | Stakes | Status of spec |
|---|---|---|---|
| CORE | Data plane, alarm bus, recorder, logbook, paper record | Highest in current scope | Draft (this doc) |
| AW | Anchor watch | High | Design inputs only |
| HL | Hazard lookout | High | Design inputs only |
| MT | Maintenance/inspection tracker | Moderate | FR-CHART only |
| RN | Route/navigation planner | Moderate | Design inputs only |
| ST | Sail-trim advisor | Low (suggestion only) | Design inputs only |
| DK | Anchor and docking assistant | Highest (future) | Out of scope |

Why CORE is a subsystem: AW and HL both fail if the data plane or the alarm bus fails. The project principle is "deterministic code owns detection and alerting". The alarm bus is that deterministic code. Thus CORE has the highest stakes in the current scope.

Roadmap rule: build and test CORE before AW and HL.

---

## 2. Decisions

### DEC-001: Alarm messages on the NMEA 2000 bus (scope exception)

Status: ACCEPTED by the skipper, 18 Nov 2026. Recorded as ADR-0002.

Decision: First Mate can transmit alarm messages on the NMEA 2000 bus. This is the only exception to read-only advisory.

Reason: The Raymarine Axiom and its buzzer become a second sounder that the First Mate host does not control. This gives an alarm path that continues if the First Mate display or speaker fails.

Limits:
- First Mate must transmit only standard alert messages. [VERIFY] Confirm the PGNs that the Axiom shows (candidate: NMEA 2000 alert PGNs 126983 to 126988).
- First Mate must not transmit any other message type. This includes autopilot commands, routes, switching commands, and radar settings.
- First Mate must use its own device identity on the bus. It must not use the identity of another device.
- First Mate must limit the transmit rate. [VERIFY] Set the limit after a bus load test.
- One configuration switch must turn off all bus transmission. The change must go in the log.
- A failure to transmit on the bus must not stop or delay the local alarm.
- [ABOARD] Test that the Axiom shows and sounds each alarm level.

Door type: one-way door. First Mate writes to a shared safety bus. Any extension of this exception needs a new decision.

---

## 3. CORE: Data plane, alarm bus, recorder, logbook

Owner: CORE. Stakes: highest in current scope.

Logic type: all CORE functions are deterministic code. The agent layer reads CORE output. The agent layer is not in the detection or alarm path.

### 3.1 Data plane

- CORE-DP-01. First Mate must have its own connection to the NMEA 2000 bus. It must not depend on Zora or any other system to stay up. [STACK]
- CORE-DP-02. Each value must carry provenance through every layer, including agent output. Provenance is: source device identity, sensor time (when the sensor sends it), receive time, replay flag, and quality flags.
- CORE-DP-03. First Mate must identify devices by their announced identity, not by bus address. The skipper must be able to block a source.
- CORE-DP-04. Each value must have a source priority list and a timeout. When the preferred source stops, First Mate must use the next source.
- CORE-DP-05. Coupled values must switch source together. Example: position, course over ground, speed over ground, and GPS time come from one receiver at a time.
- CORE-DP-06. First Mate must return to the preferred source only after a stable period. Default: 3 minutes of good data.
- CORE-DP-07. A source failover must raise an audible warning. A silent failover is not permitted.
- CORE-DP-08. First Mate must not change a priority order that the skipper set, unless the skipper approves.
- CORE-DP-09. Each value must have a plausibility range. A value outside the range is invalid. First Mate must flag it, raise a warning, and not show it as valid. Example: a fixed depth of 504 m from a plotter with no transducer.
- CORE-DP-10. Each value must have a maximum age. First Mate must flag a value that is older than this age as stale. No consumer may use a stale value as valid.
- CORE-DP-11. Each value can have a calibration offset. First Mate must log each calibration change.
- CORE-DP-12. First Mate must keep vessel geometry: draft, air draft, sounder-to-keel offset, GPS antenna position relative to the bow and centreline, bow roller height, chain length, and bridle length.
- CORE-DP-13. A rule that needs a geometry value must not arm while that value is missing. First Mate must not use a hidden default. (Zora uses a 2.5 m draft when none is set.)
- CORE-DP-14. First Mate must detect a flood of messages from one source and protect itself from it. Example: a gateway that puts internet AIS targets on the bus.

### 3.2 Recorder and replay

- CORE-REC-01. First Mate must record raw bus data continuously from the first day aboard. The format must be one that First Mate can replay. [STACK]
- CORE-REC-02. Recorded data is the main test input. Every hour at sea becomes test data.
- CORE-REC-03. Replay must set the replay flag on every value. The flag must reach every display, every log entry, and every agent output.
- CORE-REC-04. Replay data and live data must not feed the alarm bus at the same time. This is a hard interlock.
- CORE-REC-05. Every screen must show a persistent banner while replay runs.
- CORE-REC-06. First Mate must warn at three levels as storage fills, and raise an alarm on a storage fault.

### 3.3 Vessel state

- CORE-VS-01. First Mate must keep a deterministic vessel state. Candidate states (from Zora): drifting, sailing, motoring, motor-sailing, anchoring, anchored, mooring, moored, docking, docked.
- CORE-VS-02. Vessel state is an input to every rule. Each state selects its own alarm profile (depth, AIS, cross-track, drag, arrival).
- CORE-VS-03. First Mate can detect a probable change of state and ask the skipper to confirm it. The agent must not change state by itself.
- CORE-VS-04. A wrong or missing state declaration must not silently turn off a safety rule. Example: in Zora, "docked" turns off all collision warnings. First Mate must show which rules each state turns off.

### 3.4 Alarm bus

- CORE-AB-01. Alarm levels: information, warning, alarm, emergency.
- CORE-AB-02. A safety alarm must latch until a person acknowledges it. When the condition clears, the alarm changes to "cleared, not acknowledged". It does not go away by itself. (The Zora drag alarm clears itself.)
- CORE-AB-03. A safety alarm with no acknowledgement must escalate on a timer: louder sound, then the second sounder, then a second person or device. [VERIFY] Set timer values by test. Starting value: 30 seconds per step.
- CORE-AB-04. First Mate must have two independent sounders. Sounder 1: driven by the First Mate host. Sounder 2: an independent device that sounds when the host heartbeat stops. The Axiom (DEC-001) is an additional path, not one of the two.
- CORE-AB-05. An independent hardware watchdog must monitor the host heartbeat. Test each failure mode with a pulled-plug test.
- CORE-AB-06. First Mate must show one status: "Can the boat wake me?" It lists each alarm path, its state, and the time of its last self-test.
- CORE-AB-07. First Mate must test each sounder at start-up, and at a fixed interval. A failed test is an alarm on the remaining paths.
- CORE-AB-08. A safety alarm must have a maximum silence time. "Silence until cleared" is not permitted for safety alarms.
- CORE-AB-09. Sound policy is central, not per screen. A screen reload must not change it.
- CORE-AB-10. Each armed rule must declare its inputs. Loss, staleness, or invalidity of an input must raise its own alarm. First Mate must not lower the level of a sensor-loss alarm while underway.
- CORE-AB-11. First Mate must group many alarms from one source. The agent can suggest a probable root cause. The grouping must not hide a safety alarm.
- CORE-AB-12. A change to an alarm setting must take effect at once, and First Mate must confirm it on screen. A restart must not be necessary.
- CORE-AB-13. All alarms must work when the agent layer or the language model is not available.
- CORE-AB-14. Each alarm event must go in the log with a correlation ID. The record includes the input values and their provenance.
- CORE-AB-15. First Mate transmits alarms on the NMEA 2000 bus as DEC-001 permits.
- CORE-AB-16. Remote alerts (email, SMS, push) are a later addition. They need internet. They must not be the only path for a crew that sleeps aboard.

### 3.5 Output safety

- CORE-OUT-01. Every First Mate output must stop when its input becomes stale. (Zora stops sending navigation data to the pilot after 5 seconds without a new calculation.)
- CORE-OUT-02. Every future actuation must need a deliberate action, for example a long press. A short tap must do nothing. (Input for DK.)

### 3.6 Logbook and trips

- CORE-LOG-01. The log is a stream of typed, deterministic events. One stream feeds the display, the print, the audit, and the agent.
- CORE-LOG-02. The log is append-only. A correction adds a new entry. The first entry stays.
- CORE-LOG-03. An edit must not change the time, position, or sensor readings of an entry.
- CORE-LOG-04. A back-dated entry must store no sensor readings. Agent text must follow the same rule. The agent must not write a reading that the system did not record.
- CORE-LOG-05. Agent-written text, for example a day summary, must have a "generated" label.
- CORE-LOG-06. Each moment belongs to exactly one trip or stop record. A new record starts only on a change between underway and stopped.
- CORE-LOG-07. An anchoring record must hold: anchor position, depth, chain out, scope at low and high water, swing radius, alarm radius, and tide source with its trust level.
- CORE-LOG-08. First Mate must export the log as PDF and CSV, and tracks as GPX.

### 3.7 Platform

- CORE-PL-01. Updates: First Mate must verify an update before it installs it. It must not install an update underway without consent. The skipper must be able to pin a version and roll back.
- CORE-PL-02. Roles: First Mate must record who acknowledged each alarm. Role locks prevent accidents. They are not security. The documentation must say this.
- CORE-PL-03. The onboard system must work fully without internet and without a vendor cloud.

### 3.8 Acceptance criteria (CORE)

- AC-CORE-1. Fault injection: for each input of each armed rule, stop the input, make it stale, and make it implausible. Each case raises the correct alarm. Pass rate: 100%.
- AC-CORE-2. Pulled-plug test: remove host power. Sounder 2 sounds within the watchdog time.
- AC-CORE-3. A latched alarm stays after its condition clears, until a person acknowledges it.
- AC-CORE-4. With replay running, no replayed value reaches the live alarm bus.
- AC-CORE-5. With the language model off, every alarm test still passes.
- AC-CORE-6. Seeded-defect suite (section 5.7) passes.
- AC-CORE-7. 30 nights of use aboard with the alarm bus armed, with every false alarm and every missed event reviewed.
- AC-CORE-8. Paper-out test: remove the paper. The alarm bus raises a print-fault warning within 60 seconds. Repeat for a printer cable disconnect and a printer power loss.
- AC-CORE-9. Print isolation test: block the print queue and disconnect the printer. Run AC-CORE-1 again. Every alarm test still passes, with no added delay.
- AC-CORE-10. Pulled-plug test (paper): run underway or in replay-to-print test mode, then remove host power. The last fix record on paper is not older than the configured fix interval.
- AC-CORE-11. Print quality test: inject a stale value, an invalid value, and a replayed value. Each prints with its flag, or does not print. None prints as valid. Replay produces no fix record.
- AC-CORE-12. Print accuracy test: print the passage pack for a seeded plan with waypoints in all four hemisphere combinations. Each printed value matches the plan exactly. A western longitude prints with "W" (SD-04).
- AC-CORE-13. Blackout drill [ABOARD]: turn off all First Mate screens. Using only paper, the crew finds the last fix, calculates a dead-reckoning (DR) position and the course to the next waypoint, and finds the distress call script. Time limit: 5 minutes. [VERIFY] Set the limit after the first drill. Repeat the drill at the start of each season.

### 3.9 Silent Drift risks (CORE)

- A sounder fails and nothing notices. Mitigation: CORE-AB-06, CORE-AB-07.
- A source goes stale but the last value stays on screen. Mitigation: CORE-DP-10, CORE-AB-10.
- A configured alarm never fires (inert configuration). Mitigation: AC-CORE-1 and the seeded-defect suite.
- The printer stops (no paper, jam, fault) and nobody notices. The crew trusts a paper record that is out of date. Mitigation: CORE-PRN-17 to CORE-PRN-21, AC-CORE-8.
- Printed paper fades and becomes unreadable. Mitigation: CORE-PRN-24, CORE-PRN-27.
- The static packs go out of date after a replan or a crew change. Mitigation: CORE-PRN-10, CORE-PRN-04 (plan version on each fix record).
- Prints pile up and the crew stops reading them. The paper becomes an archive, not a fallback. Mitigation: CORE-PRN-27, CORE-PRN-28, AC-CORE-13.

### 3.10 Degraded-mode paper record (CORE-PRN)

**Purpose**

A critical fault can stop all electronics on board. Examples: a lightning strike, a fire, water in the electrical system, or a total loss of house power. The crew then needs the last known data to recover and to make decisions. The paper record gives the crew that data.

The paper record is one part of a layered fallback. It does not replace the independent backup kit (CORE-PRN-29).

**Owner and stakes**

- Owner: CORE.
- Stakes: High. A print failure causes no harm while the electronics work. It removes the crew's data at the worst time. A silent print failure also gives false confidence.
- Logic type: deterministic code owns all print content, print triggers, and printer health checks. The print content comes from the log event stream (CORE-LOG-01). The agent layer is not in the print path.

**Print packs and content**

- CORE-PRN-01. First Mate must print three packs: the passage pack, the vessel pack, and the fix record.
- CORE-PRN-02. The passage pack must hold: route legs with true and magnetic bearing and distance; waypoint coordinates; hazards inside the route corridor; tide and current times for the passage; a forecast summary with its source and issue time; ports of refuge; comfort limits; and the official chart numbers for each leg (FR-CHART). The passage pack includes the navigation table for use with a compass and a handheld GPS.
- CORE-PRN-03. The vessel pack must hold: vessel name, flag, call sign, MMSI, length, beam, draft, and air draft; crew list; float plan; emergency contacts; distress call scripts (section 5.6) with a blank line for the position; locations of the liferaft, EPIRB, grab bag, and backup kit; and a summary of the engines and the electrical system.
- CORE-PRN-04. The fix record must hold: time (UTC), position and its source, COG, SOG, heading, log distance, depth, barometer and 3-hour trend, true wind, fuel, water, battery state of charge, vessel state, next waypoint with bearing and distance, active alarms, and the active passage plan version. At anchor, the fix record must also hold the anchoring record (CORE-LOG-07).
- CORE-PRN-05. A stale, invalid, or missing value must print with its flag, or as a blank with the reason. First Mate must not print it as valid (CORE-DP-09, CORE-DP-10).
- CORE-PRN-06. First Mate must not print a fix record from replay data (CORE-REC-03).
- CORE-PRN-07. Each print must have a header with: pack type, sequence number, print time (UTC), and software version. The sequence number lets the crew see a missing print.
- CORE-PRN-08. Positions must print in degrees and decimal minutes, with a hemisphere letter (N, S, E, W) on each value. Times must print in UTC. Each pack must show the offset to local time.
- CORE-PRN-09. The fix record must not hold agent-written text. The passage pack can hold agent-written text only with the "generated" label (CORE-LOG-05).

**Print triggers**

- CORE-PRN-10. First Mate must print the passage pack when the skipper activates a passage plan, and after each replan. First Mate must print the vessel pack when its data changes, and at the start of each passage.
- CORE-PRN-11. First Mate must print the fix record at a fixed interval. The vessel state selects the interval (CORE-VS-02). Defaults: offshore underway, 60 minutes; coastal underway, 30 minutes; at anchor, when the anchor watch arms and then every 4 hours; docked, no fix record. [VERIFY] Set the final values by tests at sea.
- CORE-PRN-12. First Mate must print a fix record at once on these events: an alarm or emergency level alarm; a low house battery warning; a bilge alarm; a host health warning (storage, watchdog, temperature); a fast barometer fall; a position source failover.
- CORE-PRN-13. First Mate must limit event prints to one print per cause in 10 minutes. [VERIFY] Set the limit by test. The limit prevents an alarm storm from using all the paper.
- CORE-PRN-14. The skipper must be able to print any pack at any time with one action.
- CORE-PRN-15. The skipper can turn off scheduled printing, for example in harbour. First Mate must log the change. While scheduled printing is off underway, First Mate must show this on the "Can the boat wake me?" status (CORE-AB-06).

**Isolation**

- CORE-PRN-16. A print fault, a full print queue, or a missing printer must not stop or delay any alarm, any log entry, or any other CORE function. Printing is a consumer of the log. It is not in the alarm path.

**Printer health**

- CORE-PRN-17. The printer must report these states to First Mate: paper out, cover open, and fault. The printer should also report low paper. [STACK]
- CORE-PRN-18. A failed print, or a scheduled print that did not occur, must raise a warning on the alarm bus. The warning must latch (CORE-AB-02).
- CORE-PRN-19. First Mate must log each print and each print failure, with its sequence number.
- CORE-PRN-20. The "Can the boat wake me?" status (CORE-AB-06) must show the printer state and the age of the last successful print of each pack.
- CORE-PRN-21. First Mate should count the prints after each paper load. It should warn before the paper is expected to run out. The crew records each paper load in the log.

**Printer and media [STACK]**

- CORE-PRN-22. The printer must operate from the DC house supply on its own fused circuit. It must not depend on the inverter. [ABOARD] Confirm the house voltage (Q-13).
- CORE-PRN-23. The printer must not use liquid ink.
- CORE-PRN-24. The print media must stay readable for at least 5 years in a dry cabin, out of direct sun. Standard thermal paper does not meet this requirement. [VERIFY] Confirm the rating of the chosen paper.
- CORE-PRN-25. The printer must be at the navigation station, out of direct sun and spray. [ABOARD] Choose the location (Q-14).

**Crew procedure**

- CORE-PRN-26. The crew keeps the prints in one binder at the navigation station. The binder holds the current passage pack, the current vessel pack, and the fix records of the current passage.
- CORE-PRN-27. The watch-change checklist must include this item: "Is the last fix record less than one interval old? Is it in the binder?" The crew also checks the binder for faded prints at the start of each passage.
- CORE-PRN-28. The watch timer should tell the watchkeeper to check the hourly fix and plot it on the paper chart. The skipper selects the mode: (a) First Mate prints and the watchkeeper initials the print; (b) the watchkeeper writes the fix by hand in the paper log; (c) both. See OQ-PRN-1.
- CORE-PRN-29. The documentation must state that the paper record does not replace the independent backup kit. The kit holds a handheld GPS, a handheld VHF, spare batteries, and a hand-bearing compass, in a metal box. The maintenance tracker (MT) should track the battery and expiry dates of the kit.

**Passive display (recommended)**

- CORE-PRN-30. First Mate should drive an e-paper display at the navigation station. The display shows the latest fix record and the next waypoint. An e-paper display keeps its image with no power. The display must show the time of the image in large text, so the crew can see its age. [STACK]

**Open questions**

- OQ-PRN-1. Which hourly log mode does the skipper want (CORE-PRN-28)? Decision: skipper. Recommendation: mode (c) for the first season. Hand-written fixes keep crew skill and attention. Prints give accuracy and a record at a sudden failure.
- OQ-PRN-2. Does RMI accept a printed log as the official log, or must the official log be a bound book? [VERIFY] Ask with OQ-CHART-1.
- OQ-PRN-3. Which printer and paper meet CORE-PRN-17, CORE-PRN-22, CORE-PRN-23, and CORE-PRN-24? [STACK] Candidate: a 12 V or 24 V thermal printer with status reports (for example ESC/POS) and long-life thermal paper.
- OQ-PRN-4. What are the final fix intervals and the event print limit? Set them after tests at sea.

---

## 4. FR-CHART: Chart Portfolio Tracking

### Purpose

The boat flies the Marshall Islands (RMI) flag. RMI requires adequate, up-to-date charts and nautical publications for the intended voyage (SOLAS V/19, RMI MI-108 §7.41.15).

RMI does not accept a chartplotter (ECS) in place of approved charts (RMI Yacht Safety Advisory YSA-01-23). The Raymarine plotter does not satisfy the requirement. First Mate does not satisfy it either.

Thus the boat must carry official charts, in practice paper. These charts must stay corrected. A chart folder that goes out of date is a silent compliance failure and a safety risk.

This feature makes First Mate track the chart and publication portfolio. It does not replace the portfolio.

### Owner and stakes

- Owner: Maintenance/inspection tracker.
- Consumers: Route/navigation planner (coverage checks). Hazard lookout (uncharted-water labels, see HL design inputs).
- Stakes: Moderate. A failure causes a compliance gap or a planning gap. It does not cause direct physical harm.
- Logic type: Deterministic code owns all checks and alerts. The agent layer explains, summarizes, and helps with data entry. The agent layer does not decide compliance status.

### Requirements

**Inventory**

- FR-CHART-01. First Mate must keep a record of each chart on board. Each record must hold: chart number, title, issuing authority (for example SHOM, UKHO, IHM, IH, IIM), format (paper, ENC/S-57, raster, vendor electronic), edition number, edition date, and physical location on board.
- FR-CHART-02. First Mate must keep a coverage area (polygon or bounding box) for each chart. [VERIFY] Some authorities publish chart limits in a machine-readable form. Manual entry must be possible when they do not.
- FR-CHART-03. First Mate must keep a record of each required publication. Examples: tide tables, list of lights, sailing directions, COLREGS, IAMSAR Vol. III, code of signals. Each record must hold title, edition, year, and format. [VERIFY] Confirm the exact RMI list for a private yacht under 24 m.
- FR-CHART-04. First Mate must keep a record of each electronic chart subscription. Examples: S-57 data purchases, Raymarine LightHouse or Navionics cards. Each record must hold provider, coverage, purchase date, and expiry date. These records are for planning only. They do not count toward legal carriage.

**Corrections**

- FR-CHART-05. First Mate must keep a correction log for each chart. Each entry must hold the Notice to Mariners (NtM) number, its date, the date the crew applied it, and the person who applied it.
- FR-CHART-06. First Mate must show, for each chart, the most recent NtM applied and the age of that correction.
- FR-CHART-07. First Mate should identify new NtMs that apply to charts on board, when the boat has internet access. [STACK] [VERIFY] NtM feed formats differ by authority. Confirm a source for each authority in the portfolio.
- FR-CHART-08. First Mate must mark a chart as "correction status unknown" when it cannot check for new NtMs. First Mate must not mark such a chart as current.

**Voyage coverage check**

- FR-CHART-09. First Mate must compare a planned route against the coverage of the official charts on board. The check must use a corridor around the route, not only the route line. [STACK]
- FR-CHART-10. First Mate must report each part of the route that has no official chart coverage. It must also report coverage that is only at a scale too small for coastal or harbour approach.
- FR-CHART-11. First Mate must report each chart on the route that has a superseded edition or an out-of-date correction status.
- FR-CHART-12. The route/navigation planner must show the coverage check result before the skipper activates a passage plan. The skipper can continue. First Mate must record that decision and the open gaps in the log.

**Alerts**

- FR-CHART-13. First Mate must raise a warning when a new edition replaces a chart on board. [VERIFY] This depends on an authority edition feed.
- FR-CHART-14. First Mate must raise a warning before an electronic chart subscription or a publication (for example annual tide tables) expires. The default lead time is 30 days. The skipper can change it.
- FR-CHART-15. First Mate must not raise a chart warning as an alarm. Chart issues are planning issues, not immediate hazards.

**Evidence and export**

- FR-CHART-16. First Mate must export the chart and publication portfolio as a printable list. The list must include editions and correction status. This supports a port state or flag state inspection.
- FR-CHART-17. First Mate must keep all inventory and correction records in the CORE append-only store (CORE-LOG-02).

**Agent assistance**

- FR-CHART-18. The agent layer should help enter charts from a photo of the chart title block or from an authority catalogue page. A human must confirm each entry before it goes into the inventory.
- FR-CHART-19. The agent layer should explain coverage gaps in plain words, and suggest which charts to buy. Deterministic code must produce the gap list. The agent must not produce it.

### Acceptance criteria

- AC-CHART-1. A route through an area with no official chart in the inventory produces a coverage gap report. Test with a seeded route that crosses a known gap.
- AC-CHART-2. A chart with no correction check in more than the threshold period shows "correction status unknown" or "out of date". It never shows "current".
- AC-CHART-3. A change to a chart record keeps the earlier record in the store.
- AC-CHART-4. The printed portfolio list matches the inventory exactly. Test with a seeded inventory.
- AC-CHART-5. An agent-proposed chart entry does not go into the inventory without human confirmation.

### Silent Drift risks

- The NtM feed stops or changes format. First Mate then reports "no new corrections" when corrections exist. Mitigation: FR-CHART-08, and a feed-health check that warns when a feed returns no data for longer than its normal interval.
- Coverage polygons are wrong or too large. The coverage check then passes routes with real gaps. Mitigation: frozen test routes with known gaps in the eval suite.

### Open questions

- OQ-CHART-1. Which charts and publications does RMI accept for a private yacht under 24 m? Do private publishers (for example Imray) count? Action: get a written answer from yachttec@register-iri.com.
- OQ-CHART-2. Which authorities publish machine-readable chart limits, edition data, and NtM feeds for France, Spain, Portugal, Italy, and Albania? Action: research for each authority.
- OQ-CHART-3. Does the coverage check also use the S-57 data that First Mate uses for hazard checks? Assumption: yes, for planning. The legal portfolio stays the paper inventory.

---

## 5. Design inputs for subsystems not yet specified

Source: Fable teardown of iNav4U Zora (`docs/research/zora-teardown.md`). These are candidate requirements. Each subsystem entry will accept, change, or reject them.

### 5.1 Anchor watch (AW)

- Arming is the last step of a guided anchoring workflow: scope and chain calculation, holding test, then watch. Nobody forgets to arm.
- Place the anchor ahead of the bow from heading and chain reach. Correct for the GPS antenna position (CORE-DP-12).
- Two circles: swing circle and alarm circle (swing plus margin). Adjust the swing circle with tide.
- "Recenter from track" estimates the anchor position from the swing, with a ± error.
- Record a denser track at anchor, so swing and drag are visible after the event.
- The watch continues after a restart.
- Tide data must carry a trust level. A global tide model is only an estimate near the coast, which is where the boat anchors. Show the trust level in the scope calculation.
- GPS glitch handling: gate on reported accuracy, require persistence across several samples, compare two receivers when present.
- Loss of position or heading while the watch is armed is an alarm, not a fallback. (Zora places the anchor at the boat position when there is no heading.)
- The drag alarm uses the CORE alarm bus: latch, escalation, two sounders.
- Your spec also requires watching other vessels that drag or swing toward you. Zora does not do this.
- Candidate trust criteria (estimate, not sourced): 30 or more anchored nights in 3 or more conditions; staged drags; zero missed drags in replay; 1 false alarm in 10 nights or fewer.

### 5.2 Hazard lookout (HL)

- Chart look-ahead: check the water ahead against draft, and bridges, cables, and pipes against air draft. This is Zora's largest lead over the current spec. Needs vector charts on board (S-57). [STACK]
- Fixed margins, as candidate values: draft plus 0.5 m; air draft plus 2 m.
- Unknown counts as a hazard: show obstructions with no charted depth, show a bridge with no clearance, label uncharted water. FR-CHART coverage areas can supply the uncharted-water label.
- Show what is missing (position, charts, heading) instead of an empty view.
- AIS collision levels need distance AND time together. Use separate thresholds per vessel state.
- Project AIS targets between reports and show target age. (Zora does not project.)
- Crossing-ahead markers.
- Depth alarm with three levels and two profiles. Loss of depth is an alarm. It must not look like deep water.
- Geofences: keep-out, approach, enter, leave.
- Barometer trend warning.
- Radar: defer. Use the Axiom radar alarms until AIS, depth, and anchor functions are trusted.

### 5.3 Maintenance tracker (MT)

- A task belongs to one asset and has up to three triggers: engine hours, calendar, one-time date. The earliest wins.
- Early notice when a quarter of the interval remains, within bounds (2 to 30 days, 2 to 50 hours), to give time to order parts.
- A service event resets the counter and writes a log entry with date and engine hours.
- One open work card per task. Work in progress silences the reminder.
- Tools, parts, and consumables per task. Agent opportunity: a parts list for the next three months, approved by a human.
- Copy tasks between assets (two identical engines).
- Decommission, never delete. Corrections append.
- Documents attach to a folder and apply to every asset below it. Agent opportunity: the agent reads a manual and drafts the task list. A human approves it.
- Tank and battery level alarms go through the CORE alarm bus.
- Track the battery and expiry dates of the independent backup kit (CORE-PRN-29).

### 5.4 Route/navigation planner (RN)

- Do not build a weather routing solver first. Use an existing router. First Mate checks and explains. [STACK]
- Score each forecast model against the boat's measured wind. Never switch models automatically.
- Label every degraded stretch: no charts, no wave data, beyond the forecast.
- Show ETA with less precision as uncertainty increases.
- Comfort limits for true wind and wave height. A breach message gives value, position, and time.
- Keep the old plan until the new plan is ready. No reroute without a GPS fix.
- Voyage plan with a checklist in three classes: blocks activation, optional, once underway. A captain can waive an item with a logged reason. Some items cannot be waived. The gate is deterministic. The agent only drafts items.
- The system never ends a voyage plan by itself.
- The navigation table for use with a compass and a handheld GPS is now part of the passage pack (CORE-PRN-02).
- The float plan and the crew list are now part of the vessel pack (CORE-PRN-03).
- Routes and waypoints: the Axiom does this. Exchange routes as GPX.

### 5.5 Sail-trim advisor (ST)

- Baseline reef rules before any agent advice: declared sail and reef, apparent wind limit per reef, night rule (one more reef from sunset).
- Polar import, then learning with guard rails: adapt only within 60 to 125 percent of the imported polar, reduce the weight of outliers, keep a dated copy before any reset.

### 5.6 Person overboard and distress (owner to assign)

- One-tap person overboard: position mark, alarm, route back, log entry. Advisory only.
- Step-by-step distress call scripts with live position. Low cost, high value. A printed copy is part of the vessel pack (CORE-PRN-03).
- No subsystem owns these today. Assign an owner in the roadmap.

### 5.7 Seeded-defect catalogue from Zora field defects

These defects reached boats in a commercial product. Each becomes a test that First Mate must pass.

- SD-01. Alarm levels are saved but never checked (tank and battery levels).
- SD-02. Scheduled notices are created but never shown (maintenance).
- SD-03. A new display starts with all sounds off.
- SD-04. A western longitude is read as south (distress position).
- SD-05. One bad GPS fix triggers the drag alarm.
- SD-06. Drag alarm delivery to the chosen channels stops after an update.
- SD-07. A command is accepted but not executed, with no error (for future DK).
- SD-08. A command executes in the wrong direction (for future DK).
- SD-09. An integration fails with no values and no error (Victron).
- SD-10. A radar in standby guards nothing and raises nothing.

---

## 6. Questions to answer aboard (from mid-December 2026)

Equipment facts:

- Q-01. Radar model.
- Q-02. Axiom model and LightHouse version.
- Q-03. Engine panel and engine gateway. Is engine data on the bus today? Which PGNs? Are engine hours present?
- Q-04. Victron GX device model. Does it run Venus OS Large?
- Q-05. AIS model.
- Q-06. GPS sources, and GPS antenna position relative to the bow and centreline.
- Q-07. Any existing NMEA 2000 gateway to USB or Wi-Fi.

Bus tests (first week aboard):

- Q-08. Record a full bus capture in three states: shore power, engines running, instruments and autopilot in standby. Keep the raw files as test data.
- Q-09. List which messages decode with standard tools and which are proprietary Raymarine messages.
- Q-10. Does the Axiom send radar target data on the bus?
- Q-11. Which alert PGNs does the Axiom show and sound (DEC-001)?

Compliance:

- Q-12. Written answer from RMI on the accepted chart and publication portfolio (OQ-CHART-1).

Paper record:

- Q-13. House DC voltage, and a free fused circuit at the navigation station for the printer (CORE-PRN-22).
- Q-14. A printer and binder location at the navigation station, out of direct sun and spray (CORE-PRN-25).

---

## 7. Open items

- Zora purchase: OPEN. Current recommendation: do not buy unless iNav4U gives good answers on API access, licence terms, V2 support, and data export. Reasons: no independent owner evidence, subscription plan terms not clear, strong vendor-cloud dependence, and the teardown already gives most of the design value. Zora is not a safe primary drag alarm (no escalation, server sounder off by default). If bought: enable the server speaker, keep an independent anchor alarm, and give First Mate its own bus connection.
- Effort estimate (Fable, not sourced): code complete for CORE plus AW, HL (no radar, no look-ahead), MT, RN, ST, and the agent layer is about 26 to 40 calendar weeks at 10 to 15 hours a week. Trusted at sea: one to two seasons. The bottleneck is verification and sea time, not code.
- Paper record hourly log mode: OPEN (OQ-PRN-1). Skipper decision.

---

## Sources

- RMI YSA-01-23, Sunsetting of Traditional Paper Nautical Charts: https://www.register-iri.com/wp-content/uploads/YSA-2023-01.pdf
- RMI Marine Guideline 7-41-1: https://www.register-iri.com/wp-content/uploads/MG-7-41-1.pdf
- RMI Yacht Code index and notices: https://www.register-iri.com/yacht/yacht-technical-support/
- Zora teardown (`docs/research/zora-teardown.md`), with its source list.
- Zora guides: https://guides.inav4u.com/
