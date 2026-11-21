# Bus recorder

Status: DRAFT, NOT TESTED. Test on the bench before you take it aboard (roadmap week 3).

The recorder writes the raw NMEA 2000 bus to disk from the first day aboard (CORE-REC-01, ADR-0007). It uses standard Linux tools only. It has no project code, so it does not wait for ADR-0005.

## What you need

- A Linux host with a SocketCAN interface named `can0` (ADR-0008).
- The `can-utils` package (`candump`, `canplayer`).
- A disk with at least 32 GB free. [VERIFY] Measure the real data rate on the boat bus, then size the disk.

## Install

1. Install can-utils: `sudo apt install can-utils`.
2. Bring up the interface at the NMEA 2000 bit rate (250 kbit/s): `sudo ip link set can0 up type can bitrate 250000`.
3. Check that frames arrive: `candump can0`. Stop it with Ctrl-C.
4. Copy `n2k-recorder.service` to `/etc/systemd/system/`.
5. Make the capture folder: `sudo mkdir -p /var/lib/firstmate/captures`.
6. Start the service: `sudo systemctl enable --now n2k-recorder`.

## Check

- `systemctl status n2k-recorder` shows "active (running)".
- A new file grows in `/var/lib/firstmate/captures/`.

## Bench tests (before boarding)

| Test | Pass when |
|---|---|
| Power cut during a recording | After power returns, recording starts with no action. Old files are readable. |
| Disk full | The service does not crash the host. [VERIFY] Add a disk-space check. |
| No internet | The file times are correct. Needs a GPS time source or a real-time clock. |
| Bus disconnect | Recording continues after the bus returns. |
| Replay | `canplayer -I <file>` replays a capture to a virtual CAN interface (`vcan0`). |

## Known gaps

- `candump -l` writes one file per start. It does not rotate files each hour. Add rotation before long use.
- No disk-space warning yet (CORE-REC-06).
- No health status. Nothing tells you that recording stopped. Check it every day until a health check exists.
