# ADR-0010: Review queue and task board on GitHub

Status: Proposed
Date: 2026-11-21
Door: Two-way
Requirements: none
Depends on: ADR-0001, ADR-0003, ADR-0004

## Context

The skipper is the only human gate. Agents make tasks, findings, and decisions faster than one person can track them in a Markdown list. The skipper needs one queue that shows what waits for him: decisions, approvals, and reviews.

The queue must work with every agent (ADR-0004). It must not become a second source of truth (ADR-0003). An agent must not be able to make an item look approved when the skipper did not approve it.

## Options

### Option A: ADR folders by status (`proposed/`, `accepted/`)

- Advantages: easy to see at a glance.
- Disadvantages: acceptance moves the file and breaks links. Five statuses need five folders. Status is stored two times and can disagree. Covers ADRs only, not tasks.

### Option B: GitHub Issues, Pull Requests, and a GitHub Projects board

- Advantages: every agent can use the `gh` command. Issues link to PRs and ADRs. A merge moves the card. No new tool to integrate.
- Disadvantages: needs internet. A board column is not a permission: anyone with write access can move a card.

### Option C: an external board (Linear, Trello, Notion)

- Advantages: better board features.
- Disadvantages: each agent needs its own connector. A second source of truth. Another vendor.

## Decision

Option B, with these rules.

**ADRs**

1. ADR files stay in one folder. The `Status:` line is the only record of status.
2. A proposed ADR is a pull request with the label `type:adr`. Merging the PR that sets `Status: Accepted` is the acceptance.
3. Each Proposed ADR has an `Issue: #N` line that links its board card. CI enforces this after the board exists.
4. A tool generates the ADR index in `docs/decisions/README.md` from the ADR files. CI fails if the index is out of date.

**Board**

5. Columns: Inbox, Needs skipper, Ready, In progress, In review, Done.
6. Labels: `type:task`, `type:adr`, `type:approval`, `type:aboard`, `needs:skipper`, `source:agent`, `tier:L`, `tier:M`, `tier:R`.
7. Agents can open issues and put them in Inbox or Needs skipper. Agents never close, or remove the label from, an issue with `needs:skipper`.
8. `docs/plan/skipper-todo.md` is retired when its items move to issues. There is one list.

**Enforcement**

9. The board is a view, not a gate. The gates are branch protection and `CODEOWNERS`: only the skipper merges to `main`.
10. A GitHub Action reopens a `needs:skipper` issue that anybody other than the repository owner closes. It puts the label back if anybody other than the owner removes it.
11. Rule 10 works only if agents use a GitHub identity that is not the skipper's. Agents use a separate machine account with write access. The skipper uses his own account. [VERIFY] Confirm that the GitHub terms allow one machine account per person.

## Consequences

- Agents need `gh` and a token for the machine account.
- The review queue is the "Needs skipper" column plus the open PRs that request the skipper's review.
- Until the machine account exists, agent actions look like skipper actions. Rule 10 then gives no protection. The skipper must know this.
- Work aboard with no internet uses the local clone. Board updates wait for a connection.

## Review

- Independent reviewer (model and date):
- Findings and responses:
