# Day-one checklist aboard

Status: DRAFT. Finish it in roadmap week 4.

Goal: start the raw bus recording on the first day, and answer the questions in requirements section 6.

## Before you connect anything

1. Photograph the NMEA 2000 backbone: terminators, power insertion point, free T-pieces.
2. Find the house DC voltage and a free fused circuit at the navigation station (Q-13).
3. Write down every device on the bus that the Axiom lists (Q-02, Q-05, Q-06).

CAUTION: Connect the recorder only to a free T-piece or drop. Do not remove a terminator. Do not power the recorder from the bus unless you know the bus power budget.

## Day 1: start the recording

1. Connect the recorder (ADR-0008) to a free drop.
2. Start the recorder. Follow `tools/bus-recorder/README.md`.
3. Confirm that a file grows in `data/captures/`.
4. Confirm that the recorder clock is correct (UTC).
5. Pull the recorder power. Restore it. Confirm that recording starts again with no action.

## Week 1: bus captures (Q-08)

Record one labelled capture of at least 30 minutes in each state:

1. Shore power, instruments on, engines off.
2. Engines running, both engines.
3. Instruments and autopilot in standby.

Write the state, the date, and the devices on in the side file of each capture.

## Week 1: equipment facts

Answer Q-01 to Q-07 and Q-09 to Q-11. Put each answer in `docs/aboard/equipment.md` with a photo where possible.

## Back up

Copy the captures to an external drive every week. The captures cannot be made again.
