---
name: Task
about: One unit of work for an agent or the skipper
labels: ["type:task"]
---

## What

<!-- One or two sentences. -->

## Tier and requirements

- Tier: <!-- L, M, R, or R+ -->
- Requirement IDs and ADRs: <!-- Example: CORE-AB-02, ADR-0002 -->
- Role: <!-- Architect, Implementer, Verifier, Domain Reviewer, Librarian -->

## Done when

<!-- A condition that a command can check. Examples:
     - `make check` passes and the AC-CORE-3 test passes.
     - docs/specs/core.md exists, and `make docs` passes.
     Do not write "looks good" or "works". The agent must not start without this. -->

-

## Stop and ask when

<!-- Task-specific stop conditions, in addition to AGENTS.md section 5. Write "None" if there are none. -->

-

## Unattended run (fill in only if nobody watches the run)

- What can it touch? <!-- files, folders, commands -->
- What stops it? <!-- time limit, number of attempts -->
- Who approves the result? <!-- the skipper, at merge -->
