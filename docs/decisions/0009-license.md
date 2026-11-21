# ADR-0009: Licence

Status: Proposed
Date: 2026-11-21
Door: One-way (for code that others receive under the licence)
Requirements: none
Depends on: none

The decision is OPEN. This ADR gives facts, not legal advice. The project owner is not a lawyer, and neither is the AI that wrote this ADR.

## Context

The project is open-source. A repository with no licence is not open-source: others have no right to use the code. Choose a licence before the first public code.

Safety-critical software adds two concerns:

1. A strong disclaimer of warranty and liability. All common open-source licences have one.
2. Whether others may build closed products from the code.

## Options

### Option A: Apache-2.0

- Permissive. Includes an explicit patent grant. Common in industry.

### Option B: MIT

- Permissive and very short. No explicit patent grant.

### Option C: GPL-3.0 or AGPL-3.0

- Copyleft. Others who distribute changed versions must publish their source. AGPL also covers use over a network.

## Recommendation (not a decision)

Apache-2.0 if the goal is wide reuse. GPL-3.0 if the goal is that improvements stay open. Add a safety notice in the README: "Not for navigation. No warranty." in any case.

## Decision

Open.

## Consequences

Add a `LICENSE` file and a licence header rule after the decision.

## Review

- Independent reviewer (model and date):
- Findings and responses:
