# ADR-0001: Record decisions as ADRs

Status: Proposed
Date: 2026-11-21
Door: Two-way
Requirements: none
Depends on: none
Issue: #24

## Context

The project has one human and several AI agents. The agents do not keep memory between sessions. A decision that exists only in a chat is lost, or an agent decides it again in a different way.

## Options

### Option A: ADR files in the repository

- Advantages: every agent can read them. Git keeps the history. CI can check the format.
- Disadvantages: some overhead for small decisions.

### Option B: decisions in chat history and the claude.ai Project

- Advantages: no extra work.
- Disadvantages: ChatGPT and Grok cannot read them. No history. No review.

## Decision

Option A. Record each decision that is hard to reverse, or that an agent could otherwise decide again, as an ADR in `docs/decisions/`.

## Consequences

- An accepted ADR does not change. A new ADR supersedes it.
- The skipper is the only person who sets the status to Accepted.
- CI checks the format (`tools/check_docs.py`).

## Review

- Independent reviewer (model and date):
- Findings and responses:
