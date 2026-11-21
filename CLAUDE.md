@AGENTS.md

## Claude-specific notes

- `AGENTS.md` holds all project rules. Do not add project rules here.
- Hard limits for Claude Code are in `.claude/settings.json`. CI enforces the rest.
- For an independent review, use a new session or a subagent that did not write the code. Use `.agents/prompts/independent-review.md`.
