# ADR-0008: Onboard host and CAN interface

Status: Proposed
Date: 2026-11-21
Door: Two-way for the recorder. One-way for the final CORE host.
Requirements: CORE-DP-01, CORE-REC-01, CORE-AB-04, CORE-AB-05, CORE-PRN-22, Q-07, Q-13
Depends on: none
Issue: #30

The decision is OPEN. It is the most time-critical decision before boarding, because hardware must ship to France.

## Context

This ADR has two parts:

1. **Recorder host (now).** A small computer and a CAN interface that record the raw bus from the first day (ADR-0007). It must run from the house DC supply, survive power loss, and need no attention.
2. **CORE host (later).** The final host must meet the alarm bus requirements (watchdog, two sounders, verified updates). Do not decide it now. The recorder host can become a development host later.

House DC voltage is not confirmed (Q-13). [ABOARD]

## Options for the recorder

All product details are [VERIFY]. Confirm specifications, power input, and stock before you order.

### Option A: Raspberry Pi with an NMEA 2000 CAN HAT

- Example: a CAN HAT with an NMEA 2000 connector and a wide-range DC power input.
- Advantages: SocketCAN works natively. Low power. Large community. Powered from the bus or the house supply.
- Disadvantages: SD cards fail after power loss. Use an SSD or an industrial SD card and a read-only root file system.

### Option B: Small x86 or ARM computer with a USB CAN adapter

- Example: a USB-to-CAN adapter with SocketCAN support, and an NMEA 2000 drop cable.
- Advantages: more storage and power for later development.
- Disadvantages: more power draw. You must make your own cable and termination check.

### Option C: Existing USB NMEA 2000 gateway on a laptop

- Advantages: no new hardware if the boat has a gateway (Q-07).
- Disadvantages: the laptop must stay on. Vendor format (ADR-0007, Option B). Use only as a fallback.

## Recommendation (not a decision)

Option A for the recorder, with an SSD, plus Option C as the fallback. Buy two CAN interfaces if the cost is low, so one failure does not stop recording.

Other items to order with it:

- An NMEA 2000 T-piece and drop cable.
- A fused DC supply lead. [ABOARD] Confirm voltage.
- A USB GPS receiver or a real-time clock module, so recordings have a correct time when there is no internet.

## Decision

Open.

## Consequences

To be written after the decision.

## Review

- Independent reviewer (model and date):
- Findings and responses:
