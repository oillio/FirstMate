# AI team

Status: DRAFT.

## 1. Roles

Each role is a file in `.agents/roles/`. Any agent can take any role. A role is a set of instructions and limits, not a model.

| Role | Does | Does not |
|---|---|---|
| Architect | Requirements, specifications, ADR drafts, design notes | Write production code. Accept ADRs. |
| Implementer | Code and unit tests on a branch, to a specification | Change specifications or acceptance tests |
| Verifier | Acceptance tests, seeded-defect tests, independent code review | Review code that it wrote |
| Domain Reviewer | Seamanship, COLREGs, NMEA 2000, marine standards review | Approve code changes alone |
| Librarian | Docs, ADR index, traceability, sync of copies | Change requirements content |

The skipper is the only human. The skipper accepts ADRs, approves specifications, and merges.

## 2. Which tool for which work (candidate)

| Work | First choice | Second choice | Why |
|---|---|---|---|
| Daily build work in the repository | Claude Code (desktop app or CLI) | Codex CLI (ChatGPT) | Runs commands, tests, and git on the local clone |
| Independent review of tier R changes | A model family different from the author | A new Claude session with no history | Different families make different errors |
| Hard design questions and one-way-door ADRs | Fable (limited access) | Claude Opus | Use limited access where the stakes are highest. Fable 5.2 has extra cybersecurity safeguards. Use it for design text, not for bus-protocol code or bus-flood tests. |
| Research with current web sources | Claude, Grok | ChatGPT | Compare two sources for important facts |
| Exploratory design chat | claude.ai Project "First Mate" | Any | Results go into the repository by pull request |

## 3. Rules for all agents

- Start every session from `AGENTS.md`.
- Short tasks. Do not keep state in a long chat. Read state from the repository.
- Report the commands you ran and their output. Do not report a result that you did not see.
- A finding from a reviewer goes in the pull request, not only in a chat.
- The task has a "Done when" condition that a command can check. An agent's statement that it is done is not evidence.
- See [guardrails.md](guardrails.md) for the checks that agents cannot change alone.
