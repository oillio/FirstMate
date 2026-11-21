# ADR-0004: Agent-agnostic workflow

Status: Proposed
Date: 2026-11-21
Door: Two-way
Requirements: none
Depends on: ADR-0003

## Context

The skipper has access to Claude (Claude Code), ChatGPT, Grok, and limited access to Fable. Different model families make different errors. A reviewer from a different model family is more independent than a reviewer from the same family. Lock-in to one provider is a risk.

Each tool reads its own instruction file. Each tool has its own hook and permission system.

## Options

### Option A: one shared instruction file, enforcement in git and CI

- `AGENTS.md` holds all agent rules. Tool files (`CLAUDE.md`, others) only point to it.
- Role and prompt files are plain Markdown in `.agents/`. Any agent can load them.
- Hard rules are in CI and git, not in tool-specific hooks. CI applies to every agent.
- Tool-specific settings (for example `.claude/settings.json`) are an extra layer only. They are never the only control.

### Option B: optimise for Claude Code only

- Advantages: use all Claude Code features (subagents, hooks, skills) directly.
- Disadvantages: other agents get no rules. Enforcement depends on one vendor.

## Decision

Option A.

## Consequences

- A rule that must have zero exceptions goes in CI. A tool hook can repeat it for faster feedback.
- The independent reviewer for safety-critical changes comes from a different model family from the author, when one is available.
- Adding a new agent needs only a pointer file to `AGENTS.md`.

## Review

- Independent reviewer (model and date):
- Findings and responses:
