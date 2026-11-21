# ADR-0002: Alarm messages on the NMEA 2000 bus

Status: Accepted
Date: 2026-11-18
Door: One-way
Requirements: DEC-001, CORE-AB-04, CORE-AB-15
Depends on: none

This ADR records DEC-001 from the requirements document. The skipper accepted it on 18 Nov 2026.

## Context

The current scope is read-only advisory. The alarm bus needs more than one path to wake the crew. The Raymarine Axiom on the boat can show and sound alarms that it receives on the NMEA 2000 bus. The First Mate host does not control the Axiom buzzer. Thus the Axiom gives an alarm path that continues if the First Mate display or speaker fails.

## Decision

First Mate can transmit alarm messages on the NMEA 2000 bus. This is the only exception to read-only advisory.

Limits:

- First Mate transmits only standard alert messages. [VERIFY] Confirm the PGNs that the Axiom shows (candidate: NMEA 2000 alert PGNs 126983 to 126988).
- First Mate transmits no other message type. This includes autopilot commands, routes, switching commands, and radar settings.
- First Mate uses its own device identity on the bus. It does not use the identity of another device.
- First Mate limits the transmit rate. [VERIFY] Set the limit after a bus load test.
- One configuration switch turns off all bus transmission. The change goes in the log.
- A failure to transmit on the bus does not stop or delay the local alarm.
- [ABOARD] Test that the Axiom shows and sounds each alarm level.

## Consequences

- First Mate writes to a shared safety bus. Any extension of this exception needs a new ADR.
- CI must include a guard that blocks any transmit code outside the alert PGN allowlist. The first version of the guard is a text tripwire in `tools/check_docs.py`. A stronger guard comes with ADR-0005.
- The Axiom is an additional alarm path. It is not one of the two independent sounders in CORE-AB-04.

## Review

- Independent reviewer (model and date): not recorded.
- Findings and responses: not recorded.
