# Principles

Status: DRAFT. Moved from the claude.ai Project memory on 21 Nov 2026. The skipper must ratify each principle. Read this file before you propose a design change.

## Safety

1. **Deterministic code owns detection and alarms.** Agents explain and triage. They never replace safety-critical logic.
2. **The safety bar is asymmetric.** Engine control (DK) gets the most conservative engineering practice. Sail-trim advice can use a softer, curated knowledge layer.
3. **Silent Drift applies to every subsystem**, not only hazard lookout. A rising override rate is the most informative drift signal.
4. **Unknown is not safe.** A missing, stale, or invalid input raises its own alarm. No hidden defaults.

## Architecture

5. **Append-only records from the start.** The onboard store is append-only, so a cloud tier can read it later with no refactor.
6. **Onboard first.** Build the onboard tier before any cloud integration.
7. **The cloud tier is push-only: boat to cloud.** The cloud never sends commands to the boat. An inbound command channel is an attack surface that the project does not accept.
8. **Cloud scope is small:** a dead-man switch, non-real-time compute (passage planning, log analysis), and a status view for family.
9. **The family status view shows data age** and uses templated text over verified telemetry. A confident message built on stale data could delay a search and rescue response.

## Agents and process

10. **Short tasks, not long-lived agents.** Agents do not hold state in context for weeks. They read state from the repository.
11. **Keys, not prompts.** Enforce capability limits by structure (CI, permissions, separate identities), not only by instructions.
12. **One-way doors need a human gate.** Agents can act alone only on two-way doors.
13. **Human attention goes to specifications and verification gates**, not to every line of generated code.
14. **Review gates must be real.** Automation bias, deskilling, and "authority laundering" (an agent output that looks approved but is not) are real risks for a solo developer.
15. **Minimal viable intelligence stack.** Do not build orchestration or parallel infrastructure before a measured need exists.
16. **Candidate frameworks are not commitments.** Four Pillars, Agent Specifications, and similar methods stay candidates until an ADR accepts them.
17. **Files are storage; folders are organisation.** Files are durable and carry the content. Folder structure is a convenience.
