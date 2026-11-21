# ADR-0011: Boat-agnostic core, separate vessel profile

Status: Proposed
Date: 2026-11-21
Door: One-way (it sets the shape of all code and data)
Requirements: CORE-DP-03, CORE-DP-12, CORE-DP-13, CORE-PRN-03
Depends on: ADR-0003
Issue: #33

## Context

First Mate must work on boats other than the first one. The first boat is a Lagoon 46 with Raymarine electronics, two Yanmar engines, and a Marshall Islands flag. If these facts get into generic code, a second boat needs a code change, and a wrong value can hide in code where nobody reviews it.

Some vessel data is personal or commercial: MMSI, call sign, crew list, emergency contacts, purchase prices, supplier quotes. This repository is open-source and public. That data must not go in it.

Some vessel data is safety input: draft, air draft, sounder offset, GPS antenna position, chain length. A wrong value can cause a grounding or a missed drag alarm.

## Options

### Option A: vessel data in this repository, in a `vessels/` folder

- Advantages: one repository.
- Disadvantages: personal and commercial data becomes public. Easy for code to reach into one boat's folder.

### Option B: generic code here, vessel profile in a separate private repository

- Advantages: clean split. Private data stays private. Install on a new boat = a new profile repository.
- Disadvantages: two repositories. Agents need access to both. CI for this repository cannot see the real profile.

## Decision

Option B, with these rules.

1. **Generic code and generic requirements live in this repository.** They must not name a boat, a brand, or a model as a fact. They can name a brand in an adapter (for example a Raymarine message decoder) that is selected by the profile.
2. **One private repository per boat holds the vessel profile.** Working name: `firstmate-vessel-<boat>`. First Mate loads the profile at start-up from a configured path.
3. **This repository holds a schema and an example profile.** The example is a fictional boat. Tests use it. The example contains no real personal data.
4. **Every profile value carries its source and status.** Status values: `as-ordered`, `as-quoted`, `manufacturer-spec`, `measured`, `verified-aboard`. A safety value (CORE-DP-12) must be `measured` or `verified-aboard` before a rule that uses it can arm (CORE-DP-13).
5. **Source documents stay in the profile repository**, unchanged: purchase order, options list, customisation quotes, manuals, survey. The structured profile cites them.
6. The profile format comes after ADR-0005. Until then, the profile repository holds the source documents and a plain Markdown summary only.

## Consequences

- Create the private profile repository now and put the source documents in it.
- The requirements document mixes generic and vessel-specific text (for example "Raymarine Axiom" in DEC-001, "RMI" in FR-CHART). The Librarian must split it: generic requirements here, vessel facts and flag-state rules in the profile. Flag-state rules can become a generic "flag-state rule set" with one set per flag.
- `docs/aboard/` is vessel-specific. Move it to the profile repository after the first boarding.
- A later CI check must block known vessel identifiers (boat name, MMSI) in generic code. [STACK]
- A purchase order is "as-ordered", not "as-built". Dealers change items. Each safety value needs a check aboard.

## Review

- Independent reviewer (model and date):
- Findings and responses:
