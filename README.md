# First Mate

First Mate is an open-source digital crew member for a Lagoon 46 sailing catamaran.

It monitors the boat sensors, keeps watch at anchor, looks for hazards, keeps the log, and tracks maintenance. It gives advice. It does not control the boat.

> **Status: planning phase.** There is no runtime code yet. Do not use any part of this project for navigation or safety.

## Safety position

- First Mate is advisory only. The one exception is alarm messages on the NMEA 2000 bus ([ADR-0002](docs/decisions/0002-nmea2000-alarm-transmit.md)).
- Deterministic code owns all detection and all alarms. The language model explains and triages. It is never in the alarm path.
- All alarms must work when the language model is not available.

## Where to start

| You want to | Read |
|---|---|
| Finish the one-time setup | [SETUP.md](SETUP.md) |
| Understand the project | [docs/README.md](docs/README.md) |
| See the plan | [docs/roadmap.md](docs/roadmap.md) |
| Read the requirements | [docs/requirements/requirements.md](docs/requirements/requirements.md) |
| See the decisions | [docs/decisions/](docs/decisions/) |
| Work on the code as an AI agent | [AGENTS.md](AGENTS.md) |
| Contribute | [docs/process/development-process.md](docs/process/development-process.md) |

## Checks

Run all checks:

```sh
make check
```

## Licence

Not chosen yet. See [ADR-0009](docs/decisions/0009-license.md).
