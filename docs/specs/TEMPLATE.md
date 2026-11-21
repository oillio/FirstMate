# Agent Specification: SUBSYSTEM NAME

Status: DRAFT
Tier: L | M | R | R+
Owner role: Architect
Requirements: list of IDs

## 1. Purpose

One paragraph. What does this subsystem do for the crew?

## 2. Authority

- What it can do by itself:
- What needs a skipper confirmation:
- What it must never do:
- Door type of each action (one-way or two-way):

## 3. Inputs

| Input | Source | Maximum age | Plausibility range | Behaviour when stale or invalid |
|---|---|---|---|---|

## 4. Outputs

| Output | Consumer | Alarm level | Stops when input is stale? |
|---|---|---|---|

## 5. Logic split

- Deterministic code owns:
- The agent layer can:
- The agent layer must not:

## 6. Failure modes

| Failure | Effect | Detection | Response |
|---|---|---|---|

## 7. Evals and floors

| Eval | Data set | Floor | Frozen? |
|---|---|---|---|

## 8. Silent Drift signals

- Online proxy metrics:
- Override rate:
- Shadow-mode plan:

## 9. Acceptance criteria

Copy the AC IDs from the requirements and add any new ones here.

## 10. Open questions
