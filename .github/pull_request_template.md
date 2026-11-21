## What and why

<!-- One or two sentences. -->

## Tier

<!-- L, M, R, or R+. See docs/process/development-process.md. -->

## Requirement IDs and ADRs

<!-- Example: CORE-AB-02, ADR-0002 -->

## Done when

<!-- Copy the "Done when" condition from the issue. Show the evidence below. -->

## Checks run

<!-- Paste the command and its output. Do not report a result that you did not see. -->

```text
$ make check
```

## Review

- [ ] Author is human / model: <!-- name the model -->
- [ ] Independent reviewer (tier M and above): <!-- model and session -->
- [ ] Domain review (tier M and above)
- [ ] Docs updated
- [ ] No language model in the detection or alarm path
- [ ] No transmission on the NMEA 2000 bus except ADR-0002 alert messages
- [ ] Guard files changed? Then this pull request has only guard files and the label `type:guard`
- [ ] A `Session-Models:` trailer on a commit? Then name the models here
