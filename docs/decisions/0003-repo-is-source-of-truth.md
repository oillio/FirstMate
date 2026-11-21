# ADR-0003: The repository is the source of truth

Status: Proposed
Date: 2026-11-21
Door: Two-way
Requirements: none
Depends on: ADR-0001

## Context

Project knowledge is in four places today: the claude.ai Project docs, chat histories, Claude memory, and this repository. Different agents can see different places. Two copies of a requirement drift apart.

## Options

### Option A: the repository is the source of truth

- Advantages: every agent and every tool can read it. Git history and pull requests give review and audit. CI can check it.
- Disadvantages: the claude.ai Project needs a manual sync, or it goes out of date.

### Option B: the claude.ai Project is the source of truth

- Advantages: easy to use in chat.
- Disadvantages: only Claude can read it. No history, no review, no CI.

## Decision

Option A. The repository wins when two copies differ.

## Consequences

- Move the requirements, the Zora teardown, and the guidance summary into `docs/`.
- The claude.ai Project keeps a short pointer doc and, optionally, read-only copies. Mark each copy with the commit it came from.
- Results of design chats go into the repository through a pull request. A chat is not a record.

## Review

- Independent reviewer (model and date):
- Findings and responses:
