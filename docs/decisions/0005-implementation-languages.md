# ADR-0005: Implementation languages

Status: Proposed
Date: 2026-11-21
Door: One-way
Requirements: CORE-AB-13, CORE-PL-01, CORE-DP-02
Depends on: ADR-0006 (they affect each other; decide them together)

The decision is OPEN. This ADR gives the options, the criteria, and a test to decide.

## Context

First Mate has three kinds of code with different needs:

1. **CORE** (data plane, alarm bus, recorder control, logbook). Highest stakes. Deterministic. Runs for months without a restart. The data rate is low for a modern computer (an NMEA 2000 bus carries at most about 250 kbit/s), so raw speed is not a criterion.
2. **Agent layer and evals.** Calls model APIs. Must support Anthropic, OpenAI, and xAI. Changes often.
3. **User interface.** Screens on tablets and phones at the navigation station. [STACK]

Process separation between CORE and the agent layer helps CORE-AB-13 (alarms work without the model). It is possible in any language.

Criteria, in order:

1. Defects that the compiler or type checker finds before run time. The worst field defects in Zora were inert configuration and unhandled states (requirements 5.7).
2. The skipper can read and review the code. He is the only human gate.
3. Ecosystem for NMEA 2000 decoding and for the model SDKs.
4. Deployment on the onboard host: one artefact, verified update, rollback (CORE-PL-01).
5. How well the AI agents write and test the language.
6. Number of languages. Each language adds toolchains, CI jobs, and review load for one person.

## Options

### Option A: Python everywhere

- Advantages: one language. Best model SDK support. python-can reads SocketCAN. Fast iteration. Easy for the skipper to read.
- Disadvantages: type errors appear at run time unless strict type checking is in CI. A rarely used alarm branch can fail only when it runs. Packaging and verified updates need more work.
- Mitigation: strict type checks, 100% branch coverage on the alarm path, property-based tests, CORE in its own process.

### Option B: Rust for CORE, Python for the agent layer, evals, and tools

- Advantages: the compiler forces every enum case and every error to be handled. One static binary per release makes verified update and rollback simple. CORE runs in a separate process from the agent layer by design.
- Disadvantages: two languages. Slower iteration. Harder for the skipper to read if he does not know Rust. Fewer marine libraries.

### Option C: TypeScript on Signal K for everything

- Advantages: Signal K server is Node. Zora ships on Signal K. Large plugin ecosystem.
- Disadvantages: the alarm path runs inside a server that this project does not control. Type safety depends on discipline. Couples ADR-0005 and ADR-0006 to one answer.

### Option D: Go for CORE, Python for the agent layer

- Advantages: simple language, static binary, good concurrency.
- Disadvantages: weaker exhaustiveness checks than Rust. Two languages.

## Recommendation (not a decision)

Run the language spike in the roadmap (week 2) for Option A and Option B. Decide on the evidence.

Current leaning: Option B if the skipper can read the Rust spike code with comfort. Option A with strict checks if he cannot. A reviewer cannot gate code that he cannot read.

Question for the skipper: which languages do you read with comfort today?

## Decision

Open.

## Consequences

To be written after the decision.

## Review

- Independent reviewer (model and date):
- Findings and responses:
