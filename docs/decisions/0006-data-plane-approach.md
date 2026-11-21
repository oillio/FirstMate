# ADR-0006: Data plane: Signal K or own decoder

Status: Proposed
Date: 2026-11-21
Door: One-way
Requirements: CORE-DP-01 to CORE-DP-14, CORE-REC-01 to CORE-REC-06
Depends on: ADR-0005, ADR-0007

The decision is OPEN.

## Context

CORE needs NMEA 2000 decode, source tracking by announced identity, per-value provenance, source priority, staleness, and plausibility checks.

Signal K is an open-source marine data server. iNav4U Zora ships on Signal K (Zora teardown, source 233). Signal K has a large plugin ecosystem and Victron integration. [VERIFY] Confirm how Signal K keeps sensor time, source identity, and quality per value. The teardown found that Zora discards sender timestamps. It does not say if that is a Signal K limit or a Zora limit.

canboat is an open-source NMEA 2000 decoder with a PGN database. Signal K uses a JavaScript port of it. [VERIFY] Confirm the current state of each project.

## Options

### Option A: Signal K is the data plane, and CORE runs as Signal K plugins

- Advantages: least code. Proven in a shipping product.
- Disadvantages: the alarm path depends on a large server that this project does not control. Updates to Signal K can change behaviour. Provenance may not meet CORE-DP-02.

### Option B: Signal K is an input adapter only. CORE is a separate process.

- Signal K decodes and serves data. CORE reads from it, adds its own provenance, staleness, and priority rules, and owns the alarm bus.
- Advantages: reuse of decode and integrations. CORE stays small and under project control.
- Disadvantages: two processes. CORE depends on Signal K for data, so a Signal K fault is a data-loss fault that CORE must detect (CORE-AB-10).

### Option C: own decoder from raw CAN, with the canboat PGN database

- Advantages: full control of provenance from the first byte. No large dependency in the safety path.
- Disadvantages: more code. Integrations (Victron and others) are separate work.

### Option D: Option C for CORE, and Signal K in parallel for non-safety uses

- Signal K runs beside CORE for dashboards, plugins, and experiments. It is not in the CORE path.
- Advantages: control in the safety path, ecosystem outside it.
- Disadvantages: two decoders that can disagree. Needs a comparison check.

## Recommendation (not a decision)

Start Signal K on the first day aboard as a tool to learn the bus. It costs little and needs no decision. Decide this ADR after the first bus captures (Q-08, Q-09) show which data is on the bus and which messages are proprietary.

## Decision

Open.

## Consequences

To be written after the decision.

## Review

- Independent reviewer (model and date):
- Findings and responses:
