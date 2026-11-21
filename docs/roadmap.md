# First Mate — Roadmap

Status: DRAFT 0.1 (21 Nov 2026). The skipper must ratify this roadmap.

This roadmap has two parts:

1. The pre-boarding plan: four weeks, from 22 Nov 2026 to the move aboard in mid-December 2026.
2. The phases after the move aboard.

The requirements are in [requirements/requirements.md](requirements/requirements.md). Decisions are in [decisions/](decisions/).

---

## 1. Principles for the plan

- Build and test CORE before AW and HL (requirements, section 1).
- Sea time and verification are the bottleneck, not code. Every hour aboard without a bus recording is lost test data.
- Do not write safety code before the boarding date. Four weeks is too short to write and verify it. Use the time for decisions, process, and the recorder.
- Each big decision is an ADR. An ADR stays "Proposed" until the skipper accepts it.
- Hard rules go in CI. CI applies to every agent and every person. A prompt line does not.

---

## 2. Pre-boarding plan (4 weeks)

### Goal

On the first day aboard, these items are true:

1. The repository is the single source of truth for requirements, decisions, and process.
2. Any agent (Claude, ChatGPT, Grok, Fable) can start work from `AGENTS.md`.
3. CI runs on every pull request and blocks a merge on failure.
4. The decisions that block Phase 1 are accepted: host hardware, CAN interface, recording format, licence, implementation languages.
5. The bus recorder hardware is on the boat, tested on the bench, with a runbook.
6. A day-one checklist answers the questions in requirements section 6.

### Week 1 (22 to 28 Nov): Foundation

| Item | Owner | Output |
|---|---|---|
| Review and commit the repository skeleton | Skipper | First commit on `main` |
| Turn on branch protection and required checks | Skipper | `main` protected |
| Move the Zora teardown and the guidance summary into `docs/research/` | Skipper or Librarian | Two files |
| Ratify ADR-0001 (ADRs), ADR-0003 (repo is the source of truth), ADR-0004 (agent-agnostic workflow) | Skipper | Status "Accepted" |
| Draft ADR-0008: host and CAN interface options | Architect | ADR with options |
| **Order the recorder hardware** | Skipper | Order placed. Shipping to France takes time. This is the item with the longest lead time. |

### Week 2 (29 Nov to 5 Dec): Big decisions

| Item | Owner | Output |
|---|---|---|
| Language spike (see ADR-0005) | Implementer x2, Verifier | Two small builds of the same slice. A comparison note. |
| Data plane study: Signal K as input adapter, or own decoder (ADR-0006) | Architect, Domain Reviewer | Options with risks |
| Independent review of ADR-0005 and ADR-0006 by a second model family | Skipper | Review notes in the PR |
| Decide ADR-0007 (recording format) and ADR-0009 (licence) | Skipper | Status "Accepted" |

The language spike: build the same thin slice two times, in two candidate languages. The slice:

1. Read a recorded NMEA 2000 file (a public sample file is sufficient).
2. Decode one PGN (for example, water depth).
3. Apply a staleness timeout (CORE-DP-10).
4. Raise and latch an alarm (CORE-AB-02).
5. Pass a seeded-defect test (an input goes stale and the alarm must fire).

Measure: time to build, defects that the reviewer finds, how easily the skipper reads the code, and test quality.

### Week 3 (6 to 12 Dec): Build infrastructure

| Item | Owner | Output |
|---|---|---|
| Accept ADR-0005 and ADR-0006 | Skipper | Status "Accepted" |
| Add the language toolchain to CI: build, lint, type check, unit tests, coverage | Implementer | CI jobs |
| Add the advisory-phase guard for the chosen language (no command PGNs in code) | Implementer, Verifier | CI job |
| Write the first Agent Specification: CORE (from requirements section 3) | Architect | `docs/specs/core.md` |
| Bench-test the recorder: power cycle, disk full, clock, file rotation | Skipper | Test notes |
| Write the recorder runbook | Librarian | `tools/bus-recorder/README.md` |

### Week 4 (13 Dec to boarding): Ready to go aboard

| Item | Owner | Output |
|---|---|---|
| Replay-harness design (CORE-REC-03, CORE-REC-04) | Architect | Design note, no code |
| Seeded-defect catalogue as test stubs (SD-01 to SD-10) | Verifier | Stubs in `eval/seeded-defects/` |
| Day-one checklist final | Skipper | `docs/aboard/day-one-checklist.md` |
| Pack: recorder, cables, spare SD card or SSD, backup of the repo | Skipper | Packed |
| Retrospective on the four weeks | Skipper | Update this roadmap |

### Not in the pre-boarding plan

- No alarm code, anchor watch code, or hazard code.
- No agent runtime code.
- No user interface.
- No cloud tier.

---

## 3. Phases after the move aboard

Durations are estimates. The Fable estimate (requirements section 7) is 26 to 40 weeks to code-complete, at 10 to 15 hours a week. Trust at sea takes one to two seasons.

| Phase | Scope | Exit criteria |
|---|---|---|
| 0. Pre-boarding | This document, section 2 | Section 2 goal is true |
| 1. Capture and learn | Recorder runs all the time. Answer Q-01 to Q-14. Bus captures Q-08. | 30 days of recordings. Equipment ADRs accepted. |
| 2. CORE data plane | Ingest, provenance, source priority, plausibility, staleness, replay with interlock | AC-CORE-4. Fault injection on replayed data. |
| 3. CORE alarm bus | Latch, escalation, two sounders, watchdog, "Can the boat wake me?" status, NMEA 2000 alerts (ADR-0002) | AC-CORE-1 to AC-CORE-6 |
| 4. CORE logbook and paper record | Event log, trips, CORE-PRN | AC-CORE-8 to AC-CORE-13 |
| 5. Anchor watch (AW) | Agent Specification, then build, then shadow mode | AW trust criteria (requirements 5.1) |
| 6. Hazard lookout (HL), part 1 | AIS, depth, geofence. No radar, no chart look-ahead. | Compare with Axiom alarms |
| 7. Maintenance tracker (MT) and FR-CHART | Assets, tasks, chart portfolio | One season |
| 8. Agent layer | Explain and triage over CORE output. Eval harness. | Eval floors pass. Shadow mode for one season. |
| 9. Route planner (RN), sail trim (ST) | Advisory | Per Agent Specification |
| Later | HL chart look-ahead, radar, cloud tier, docking assistant (DK) | Each needs its own decision |

AC-CORE-7 (30 nights with the alarm bus armed) runs in parallel with phases 4 and 5.

---

## 4. Risks to this plan

- **Hardware lead time.** If the recorder hardware does not arrive, phase 1 starts without data. Fallback: a USB gateway on a laptop, recording by hand.
- **Decision fatigue.** Five ADRs in two weeks is a lot for one person. Accept the two-way-door decisions fast. Spend time only on the one-way doors (ADR-0005, ADR-0006).
- **Internet aboard.** All the agents need internet. Plan work that needs agents for times with a good connection.
- **Scope creep.** Each new idea goes in an issue, not in the current phase.
- **Solo review.** The skipper is the only human gate. Use a second model family as the independent reviewer for every safety-critical change. This reduces the risk. It does not remove it.
