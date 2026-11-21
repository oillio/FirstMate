# ADR-0007: Raw bus recording format

Status: Proposed
Date: 2026-11-21
Door: Two-way
Requirements: CORE-REC-01, CORE-REC-02, Q-08
Depends on: ADR-0008

## Context

CORE-REC-01 requires a raw recording of the bus from the first day aboard, in a format that First Mate can replay. The language and the data plane are not chosen. The recording must not depend on them. Recorded data cannot be made again later.

## Options

### Option A: raw CAN frames in the SocketCAN `candump` log format

- Each line holds a timestamp, the interface, the CAN ID, and the data bytes.
- Advantages: lowest level. No decode, so no decode errors are recorded. Standard Linux tools write it (`candump -l`) and replay it (`canplayer`). Decoders such as canboat read it. [VERIFY] Confirm that the chosen decoder reads it. Plain text, easy to compress.
- Disadvantages: needs a SocketCAN interface. Fast-packet messages must be put together by the decoder. Files are larger than decoded data (compression helps).

### Option B: a gateway vendor format (for example Actisense)

- Advantages: works with a USB gateway that many boats have.
- Disadvantages: vendor format. Some gateways filter or change messages.

### Option C: decoded data (Signal K deltas or JSON)

- Advantages: easy to read.
- Disadvantages: the decoder decides what is kept. A decode defect corrupts the record for ever. Fails CORE-REC-01 intent.

## Recommendation

Option A. Keep the raw files read-only. Decode copies, never the originals.

File rules:

- One file per hour, compressed after it closes.
- File name holds the UTC start time and the host name.
- Each file has a side file with the host clock source and its state at the start (GPS time, NTP, or none).
- The raw recordings do not go in git. They go in `data/captures/` (git ignores it) and on an external backup.

## Decision

Open until the skipper accepts it.

## Consequences

- The recorder needs a SocketCAN interface (ADR-0008).
- Test data for every later phase comes from these files.

## Review

- Independent reviewer (model and date):
- Findings and responses:
