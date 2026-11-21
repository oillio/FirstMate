# Prompt: set up the task board (ADR-0010)

Use this prompt one time, in Claude Code on the skipper's Mac, after the first commit. The skipper must be present: some steps need his browser.

---

Read `AGENTS.md` and `docs/decisions/0010-review-queue-on-github.md`. Your role is Librarian. Set up the board as ADR-0010 describes. Repository: oillio/FirstMate.

Work in this order. Stop and ask me if a step fails. Report each command and its output.

1. Check `gh auth status`. The token needs the scopes `repo` and `project`. If `project` is missing, tell me to run `gh auth refresh -s project`.
2. Make a branch `chore/board-setup`.
3. Create these labels with `gh label create`. Skip a label that exists.
   - `type:task`, `type:adr`, `type:approval`, `type:aboard`
   - `needs:skipper` (red), `source:agent`
   - `tier:L`, `tier:M`, `tier:R`
   - `type:guard` (changes to guard files, see `tools/guard-files.txt`)
   - `review:changes-needed` (a review ended with BLOCK or CHANGES NEEDED)
4. Create a GitHub Project (owner: oillio) named "First Mate" with `gh project create`. Link it to the repository with `gh project link`.
5. The Status field must have these options, in this order: Inbox, Needs skipper, Ready, In progress, In review, Done. The `gh` command cannot always edit field options. If it cannot, give me the exact steps to do it in the browser, and wait.
6. For each unchecked item in `docs/plan/skipper-todo.md`, create one issue. Labels: `type:task` or `type:aboard`, plus `needs:skipper` when only I can do it. Add each issue to the project. Set Status to "Needs skipper" or "Ready". Put the roadmap week in the issue body.
7. For each ADR with `Status: Proposed`, create one issue titled "Decide ADR-NNNN: <title>". Labels: `type:adr`, `needs:skipper`. Add it to the project with Status "Needs skipper". Add the line `Issue: #N` to the ADR, under the `Depends on:` line.
8. In `tools/check_docs.py`, set `REQUIRE_ADR_ISSUE = True`.
9. Replace the content of `docs/plan/skipper-todo.md` with one line: "Retired. The list is now the GitHub Project 'First Mate' (ADR-0010)." Keep the file.
10. Run `make adr-index` and `make check`. Both must pass.
11. Commit, push the branch, and open a pull request. Title: "Set up task board (ADR-0010)". Labels: `type:adr`. Body: link ADR-0010, list the issues you created, and paste the `make check` output.
12. Give me the list of browser steps that remain (project workflows, branch protection). Do not merge.
