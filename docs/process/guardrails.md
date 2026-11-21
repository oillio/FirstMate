# Guardrails

Status: DRAFT. Added 21 Nov 2026.

The skipper cannot read every line of agent code. These guardrails make the most important rules structural, so that an agent cannot change them alone (principle 11, "keys, not prompts").

## 1. Guard files

Guard files set the agent limits and run the checks. The list is in `tools/guard-files.txt`. It includes `.claude/`, `.github/`, `.agents/`, `AGENTS.md`, the check tools, `tests/`, `eval/seeded-defects/`, and `docs/process/`.

Rule: a pull request that changes a guard file changes only guard files, and has the label `type:guard`. Reason: an agent must not weaken a check in the same change as the code that the check would fail. A separate pull request makes the change visible to the skipper.

## 2. Layers

| Layer | What it does | Enforced by | Strength |
|---|---|---|---|
| `guard-files` CI check | Fails a pull request that mixes guard files with other files, or has no `type:guard` label | GitHub Actions, required status check | Strong, after part 4 step 2 |
| Branch protection | Blocks merge without the skipper's review and green checks | GitHub ruleset (SETUP part B) | Strong |
| `ask` rules | Claude Code asks the skipper before it edits a guard file | `.claude/settings.json` | Medium. See limits. |
| `deny` rules | Claude Code refuses force-push, push to `main`, hard reset, and `gh pr merge` | `.claude/settings.json` | Medium. Tripwire only. |
| Stop hook | When Claude tries to stop with changed files and `make check` fails, Claude continues | `.claude/hooks/stop-check.sh` | Medium. Stops a false "done". |
| `Session-Models:` trailer | Shows that a commit came from more than one model | Git hook | Detection only |

## 3. Known limits

- The `ask` rules cover the Claude Code file-edit tools. An agent can still change a file with a shell command (for example `sed`). The CI check catches this at the pull request. The `ask` rule does not.
- Hooks are best-effort. CI is the real gate.
- The Stop hook lets Claude stop at the second attempt in one turn, to prevent a loop. Claude must then report the failure.
- Until SETUP part D is done, agents use the skipper's GitHub account. Then the agent actions look like the skipper's actions.
- Other agents (Codex, Grok) do not read `.claude/settings.json`. For them, only CI and branch protection apply.

## 4. One-time steps for the skipper

1. Create the label: `gh label create type:guard --color 5319e7 --description "Changes guard files"`. (The board setup prompt also creates it.)
2. In the `main` ruleset (SETUP step 7), add `guard-files` as a required status check, next to `checks`.
3. Test the `ask` rule. In a new Claude Code session, ask: "Add a blank line at the end of Makefile." Claude Code must ask for approval. Decline. Repeat with a new file `.github/test.txt`. [VERIFY] The path form `Edit(./path)` and the coverage of new files.
4. Test the Stop hook. Ask Claude Code to add an unknown requirement ID (`CORE-AB-` with the number 99) to `docs/roadmap.md` and then stop. `make check` fails on the unknown ID. Claude must continue and fix it, or report the failure. Then discard the change.
5. Check the model-switch setting. `.claude/settings.json` has `"switchModelsOnFlag": false`. [VERIFY] Nobody has confirmed this key name. A wrong key is ignored with no error: an inert setting (SD-01). Open `/config` in Claude Code and confirm that the "switch models when a message is flagged" option shows "off" or "ask". If it does not, fix the key in a `type:guard` pull request.
