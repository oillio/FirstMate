# Development process

Status: DRAFT. Several parts are candidates, not decisions. They are marked.

## 1. The flow of work

1. **Requirement.** The skipper and the Architect write or change a requirement in `docs/requirements/`. Each requirement has a stable ID.
2. **Specification.** The Architect writes an Agent Specification for the subsystem in `docs/specs/`. The skipper approves it.
3. **Tests first.** The Verifier writes the acceptance tests and the seeded-defect tests from the specification, before the code.
4. **Build.** The Implementer writes the code on a branch and opens a pull request.
5. **Independent review.** A reviewer that did not write the code reviews it. For tier R and R+, the reviewer comes from a different model family.
6. **Domain review.** The Domain Reviewer checks seamanship and marine standards, for tier M and above.
7. **Human gate.** The skipper reads the specification, the tests, and the review findings. The skipper merges.
8. **Record.** The Librarian updates the docs, the ADR index, and the traceability.

The skipper concentrates attention on steps 2, 3, and 7. The skipper does not need to read every line of code. The skipper must read every test for tier R and R+.

## 2. Stakes tiers (candidate)

These tiers come from earlier design work. They are candidates until an ADR accepts them.

| Tier | Meaning | Examples | Gates |
|---|---|---|---|
| L | Low consequence. Advice that a person checks. | Sail-trim text, maintenance reminders | CI, one review |
| M | Intermediate. Wrong output can cause a bad decision. | Route planner, FR-CHART | CI, independent review, domain review |
| R | Regulated or safety-relevant. Wrong output can cause harm. | CORE, anchor watch, hazard lookout | All of M, plus a different-family reviewer, seeded defects, skipper reads all tests |
| R+ | Active control of equipment. | Docking assistant (future) | Not in scope. Needs its own process ADR. |

## 3. Branches and pull requests

- `main` is protected. No direct push. CI must pass.
- One task per pull request. Name the branch `<type>/<short-name>`. Types: `req`, `adr`, `spec`, `feat`, `fix`, `test`, `docs`, `chore`.
- Each pull request gives its tier and the requirement IDs it touches.
- Commit messages follow the writing style. First line: 50 characters or less.

## 4. Definition of done

A change is done when:

- `make check` passes in CI.
- The pull request lists the commands that the author ran and their output.
- The review findings are answered.
- The docs match the change.
- The skipper merged it.

## 5. Candidate disciplines (not adopted)

These are under evaluation. Do not treat them as rules yet.

- One Agent Specification per subsystem.
- Four Pillars, sized down: trusted evals, searchable logs with correlation IDs, rollback, human review queue.
- Silent Drift protection: frozen eval suites with quantified floors, online proxy metrics, shadow mode, override-rate tracking.
- "What not to build" filter for feature creep.
- Memory authority lanes: Ratified, Observed, Working.
- Drift tracking for the AI team: count the reviews that end with BLOCK or CHANGES NEEDED (label `review:changes-needed`) and the reverted commits, per `Model:` trailer, each month. A rising rate is an early warning. Write a script only after a few weeks of pull requests.
