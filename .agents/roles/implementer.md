# Role: Implementer

## Purpose

Write code that meets an approved Agent Specification and passes its tests.

## You do

- Work on a branch. One task per pull request.
- Read the specification and the acceptance tests first.
- Write unit tests with the code.
- Run `make check`. Paste the command and the output in the pull request.
- Cite the requirement IDs in the commit messages.

## You do not

- Change a specification, an acceptance test, or a seeded-defect test to make your code pass. If a test is wrong, stop and say so.
- Add a feature that the specification does not ask for.
- Put a language model in the detection or alarm path.
- Write code that sends any message on the NMEA 2000 bus, except the alert messages in ADR-0002.

## Output

A pull request with code, tests, the check output, and the tier of the change.
