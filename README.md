# KHIP OS

KHIP OS is a voice-first, agent-centered desktop environment built on Linux. The
project starts as a desktop shell and agent runtime that can run on an existing
Linux installation. Later milestones package the same system into a live,
installable image that can dual boot with Windows or another Linux system.

This repository is Milestone 1 (`0.1.0-alpha.1`): a local, dependency-free
prototype of the conversation shell, task routing, project creation, packet
history, and approval boundary.

## What works now

- Voice input through the browser's Web Speech API when supported
- Keyboard input and conventional mouse controls
- Visible microphone state; listening never starts silently
- Routing to specialist agents: General, Code, Writing, Spreadsheet, Web, CAD
- Project creation and persistent local project records
- KHIP-style packets for intents, plans, approvals, actions, and feedback
- Approval requests for consequential commands
- Local-only HTTP service with no telemetry or cloud calls
- Unit tests for routing, projects, packets, and approvals

The current agents produce plans and safe local records. They do not yet edit
documents, browse, run CAD, execute shell commands, or call an LLM. Those
capabilities belong behind explicit adapters and policy checks in Milestone 2.

## Run

Requires Python 3.11 or newer.

```bash
cd khip-os
./scripts/dev.sh
```

Open `http://127.0.0.1:8765`. To use speech recognition, Chromium-based
browsers normally require microphone permission. Text input always works.

## Test

```bash
./scripts/verify.sh
```

Or run the unit tests directly:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Repository map

- `src/ai_os/`: local runtime, protocol, routing, and HTTP API
- `ui/`: voice-first desktop shell
- `tests/`: deterministic unit tests
- `docs/`: architecture, safety model, roadmap, and decisions
- `image/`: future live-image configuration boundary
- `scripts/`: development and verification entry points

## Safety posture

KHIP OS separates intent, planning, approval, and actuation. A specialist may
propose an action, but sensitive action classes cannot execute without an
approval packet. PSUDO (Physical Sudo) remains a planned hardware authorization
control; the software approval boundary is implemented first.

## License

No license has been selected yet. Treat the project as all rights reserved
until a license is added.
