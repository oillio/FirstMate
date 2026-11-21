# One-time setup

Status: current, 21 Nov 2026. Delete this file, or mark it DONE, when all steps are complete.

Do these steps in order. Part A comes before the first commit.

WARNING: The approval guard (ADR-0010, rule 10) works only after part D. Until part E passes, agent actions look like your actions. Treat every closed `needs:skipper` item as unchecked. Even after part E, the guard stops accidents only. Your own GitHub credentials stay on the Mac, so a determined agent could still use them.

---

## A. Protected files and the first commit (Terminal)

1. Go to the repository:

   ```sh
   cd ~/FirstMate
   ```

2. Unpack the protected files (`.github/`, `.claude/settings.json`, `Makefile`). Then delete the zip:

   ```sh
   unzip -o firstmate-protected-files.zip && rm firstmate-protected-files.zip
   ```

   Use the zip in the repository folder. An earlier copy sent in chat is out of date.

   Then install the git hooks. They add a `Model:` trailer to each agent commit. They need `jq` (`brew install jq` if `make` reports it is missing):

   ```sh
   make hooks
   ```

3. Run the checks:

   ```sh
   make check
   ```

   The output must end with `PASS` and `OK`.

4. Stage all files and check the list:

   ```sh
   git add -A && git status
   ```

   The list must include `.github/`, `.claude/settings.json`, and `Makefile`. It must not include a `.zip` file.

5. Commit and push:

   ```sh
   git commit -m "Add planning skeleton, ADRs 0001-0010, CI"
   git push -u origin main
   ```

## B. GitHub settings (browser)

6. Open **Actions**. Confirm that the `checks` run is green.
   - Check the repository visibility (**Settings → General**). On GitHub Free, rulesets work only on **public** repositories. A private repository needs GitHub Pro for step 7 to have any effect. The project is open-source, so public is the expected setting. Do not push secrets.
7. Open **Settings → Rules → Rulesets → New branch ruleset**. Set the target to `main`. Turn on:
   - Require a pull request before merging, with "Require review from Code Owners".
   - Require status checks to pass. Add `checks`.
   - Block force pushes.
   - Restrict deletions.
   - Put yourself on the bypass list. GitHub does not let an author approve his own pull request. The bypass lets you merge your own changes. Only you have it.

## C. Board setup (Claude Code desktop, as yourself)

8. Give `gh` the project scope:

   ```sh
   gh auth refresh -s project
   ```

9. Open Claude Code desktop on `~/FirstMate`. Write: `Run the task in .agents/prompts/setup-board.md`.
   - It makes the labels, the "First Mate" project, and the issues.
   - It adds `Issue: #N` lines to the proposed ADRs and retires `docs/plan/skipper-todo.md`.
   - It opens a pull request. It does not merge.
   - It stops when a step needs the browser (usually the Status column options).
10. In the project, open **⋯ → Workflows**. Turn on:
    - Auto-add to project (filter: `is:issue,pr is:open`).
    - Item closed → Done.
    - Pull request merged → Done.

    [VERIFY] The workflow names can differ in the current GitHub interface.
11. Review the pull request. To accept ADR-0010, set its `Status:` to `Accepted` in that pull request, then run `make adr-index`. Do the same for ADR-0001, ADR-0003, and ADR-0004 if you agree with them. Merge.

## D. Agent identity

12. Make a second GitHub account for the agents, for example `firstmate-crew`. Use a different email address. [VERIFY] Read the GitHub terms for machine accounts.
13. Invite that account to the repository with **Write** access. Accept the invite. Also add it to the project: **Settings → Manage access**.
14. As that account, make a classic personal access token with the scopes `repo` and `project`.
15. Make the file `~/FirstMate/.claude/settings.local.json`. Git ignores this file. Put the token in it:

    ```json
    { "env": { "GH_TOKEN": "<the token>" } }
    ```

16. Run `gh auth setup-git` one time. [VERIFY] Step 17 confirms that `git push` uses `GH_TOKEN`.
17. In a new Claude Code session, ask it to run `gh api user --jq .login`. The answer must be `firstmate-crew`, not `oillio`.

## E. Test the guard

18. Ask Claude Code to open a test issue with the label `needs:skipper` and then close it. Within about one minute, the `guard-approvals` Action must reopen it, with a comment.
19. Close the same issue yourself. It must stay closed.

If step 18 fails, the identity setup in part D is wrong. Fix it before you trust the board.

## F. Move project knowledge into the repository

Claude Code cannot read claude.ai Projects, their chats, or their memory. Move what agents need.

20. **Zora teardown.** Open the claude.ai Project doc "Zora taredown". Copy all the text. Paste it into `docs/research/zora-teardown.md`. Add one line at the top: `Source: claude.ai Project "First Mate", doc "Zora taredown", moved <date>.`
21. **Guidance summary.** Do the same for `claude/anthropic-guidance-summary.md` into `docs/research/anthropic-guidance-summary.md`.
22. **Earlier design files.** Find `dev-wiki-design.md` and `sailing-wiki-boundary.md` (July 2026 chat "Wiki strategy for sailing app and dev team"). Put them in `docs/research/`. They define the L/M/R tiers and the knowledge-source rules.
23. **Vessel profile repository (ADR-0011).** On GitHub, create a **private** repository, for example `firstmate-vessel-<boat>`. Put the source documents in a `sources/` folder, unchanged: the Lagoon purchase order, the options list (the spreadsheet), and the customisation quotes. Do not put these in the public FirstMate repository: they hold prices and personal data.
24. Replace the claude.ai Project "First Mate" docs with one pointer doc: "Source of truth: github.com/oillio/FirstMate (ADR-0003)."
25. Run `make check`. Open a pull request.

## G. Vessel profile summary (optional, after step 23)

In the private profile repository, ask an agent for a one-page `README.md`. Give it this task:

> Read the documents in `sources/`. Write a summary of the boat as ordered: dimensions (LOA, beam, draft, air draft, displacement), engines and saildrives, electrical system (house voltage, batteries, inverter, charging), electronics with models, tanks, ground tackle, and options fitted. For each value, cite the document and page. Mark every value "as-ordered" or "as-quoted". Do not guess. List the values that need a check aboard.

Do not export the research chats from the boat Project. They show how decisions were made, not what was installed.

## After setup

- Your review queue: the **Needs skipper** column, plus the open pull requests that request your review.
- Agents put new work in **Inbox**. You move items to **Ready**.
