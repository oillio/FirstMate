# AGENTS.md

Instructions for every AI agent that works in this repository: Claude, ChatGPT/Codex, Grok, or other agents.

This file is the single source of agent instructions. Tool-specific files (for example `CLAUDE.md`) only point here. Do not copy rules into them.

## 1. What this project is

First Mate is a safety-critical, advisory AI system for a sailing catamaran. A wrong output can put people at sea in danger. Treat reliability, failure modes, and human oversight as first-order concerns.

Current phase: planning. There is no runtime code. The implementation language is not chosen ([ADR-0005](docs/decisions/0005-implementation-languages.md)).

## 2. Hard rules

CI enforces these rules. Do not try to work around a check. If a check is wrong, say so in the pull request.

1. Deterministic code owns all detection and all alarms. A language model must never be in the alarm path.
2. No code may send a command to the engines, the autopilot, or other equipment. The only permitted transmission is NMEA 2000 alert messages ([ADR-0002](docs/decisions/0002-nmea2000-alarm-transmit.md)).
3. Every value carries provenance: source, sensor time, receive time, replay flag, quality flags (CORE-DP-02).
4. Records are append-only. A correction adds a new record.
5. Do not change an ADR with status "Accepted". Write a new ADR that supersedes it.
6. Do not merge to `main`. Open a pull request. The skipper approves every merge.
7. Do not invent sensor readings, test results, or sources. If you did not run a command, do not report its output.
8. Keep code and requirements boat-agnostic. Vessel facts go in the private vessel profile, never in this repository ([ADR-0011](docs/decisions/0011-vessel-profile-separation.md)). No personal data (MMSI, call sign, crew, contacts, prices) in this repository.

Read [docs/principles.md](docs/principles.md) before you propose a design change.

## 3. Decision status

- `[STACK]`: depends on the stack decision. The stack is not chosen.
- `[VERIFY]`: depends on a fact that nobody has confirmed.
- `[ABOARD]`: only the skipper can answer it, on the boat.

When a recommendation depends on an open decision, say so. State your assumptions.

## 4. Writing style

All prose follows ASD-STE100 Simplified Technical English. See [docs/process/writing-style.md](docs/process/writing-style.md). Short sentences, active voice, one word for one idea.

## 5. How to work

1. Find your role in [.agents/roles/](.agents/roles/). Follow it.
2. Read the requirements that your task touches. Cite requirement IDs (for example CORE-AB-02) in commits and pull requests.
3. Work on a branch. One task per pull request.
4. Run `make check` before you open a pull request. Paste the command and its output in the pull request.
5. Fill in the pull request template. Give the stakes tier of the change.
6. Each agent commit gets a `Model: <model ID>` trailer from the git hook `tools/git-hooks/prepare-commit-msg`. Claude Code sets it by itself. Other agents must set the environment variable `FIRSTMATE_MODEL` to their exact model ID before they commit. Do not write the trailer by hand.

## 6. Tasks, approvals, and the board

The task board is the GitHub Project "First Mate" ([ADR-0010](docs/decisions/0010-review-queue-on-github.md)). Use the `gh` command.

1. When you find work that is outside your task, open an issue. Do not do the work. Add the label `source:agent` and a `type:` label. Put it in the column "Inbox".
2. When you need a decision or an approval from the skipper, open an issue with the label `needs:skipper`. Put it in the column "Needs skipper". Give the question, the options, and your recommendation.
3. Never close an issue with the label `needs:skipper`. Never remove that label. Only the skipper does this. A GitHub Action reverses it.
4. A new ADR goes in a pull request with the label `type:adr`. It also gets an issue with `needs:skipper`. Put `Issue: #N` in the ADR. Run `make adr-index`.
5. Link each pull request to its issue with "Closes #N" in the description.

## 7. Commands

| Command | What it does |
|---|---|
| `make check` | Runs all checks (docs, requirement IDs, ADRs, guard, unit tests) |
| `make docs` | Runs the docs checks only |
| `make test` | Runs the unit tests for the repository tools |
| `make adr-index` | Rebuilds the ADR index in `docs/decisions/README.md` |
| `make hooks` | Installs the git hooks. Run once per clone. Needs `jq`. |

Language-specific commands come with ADR-0005.

## 8. Repository map

| Path | Content |
|---|---|
| `docs/requirements/` | Requirements. The IDs are stable. |
| `docs/decisions/` | ADRs |
| `docs/specs/` | Agent Specifications, one for each subsystem |
| `docs/process/` | Development process, AI team, writing style |
| `docs/research/` | Research inputs. Not requirements. |
| `docs/aboard/` | Checklists for work on the boat |
| `eval/` | Eval suites and the seeded-defect catalogue |
| `tools/` | Repository tools and the bus recorder |
| `src/` | Runtime code (empty until ADR-0005 is accepted) |
| `.agents/` | Role and prompt files for any agent |
