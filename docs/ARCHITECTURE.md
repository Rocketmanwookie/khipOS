# Architecture

## Product boundary

KHIP OS is an agent-centered Linux distribution layer. It does not replace the
Linux kernel. The same runtime must operate in three forms: development app on
Ubuntu, full-screen desktop session, and installable live image.

## Core flow

1. The shell captures an explicit voice or text intent.
2. The runtime records an `IntentFrame`.
3. The router assigns one specialist agent.
4. The specialist emits an `AgentPlan`.
5. Policy classifies every proposed action.
6. Consequential actions produce a pending `ApprovalFrame`.
7. An adapter may emit an `ActuationFrame` only after authorization.
8. Results become `FeedbackFrame` records and update project context.

Subsystems communicate through versioned packets, not direct hidden state.
This keeps routing, approvals, logging, and future remote agents inspectable.

## Layers

- Shell: voice, keyboard, mouse, notifications, movable companion UI
- Orchestrator: task decomposition, routing, scheduling, agent lifecycle
- Specialists: code, writing, spreadsheet, web, CAD, and future plugins
- Tools: application-specific adapters with narrow permissions
- Policy: risk classification, approvals, PSUDO, secrets, audit
- Memory: user, workspace, project, and ephemeral context boundaries
- Platform: Linux session, packaging, updates, recovery, hardware support

Configuration order remains Defaults → System → User → Workspace → Runtime.

## Adapter boundary

Milestone 2 starts adapters as explicit, permission-scoped runtime surfaces. The
first adapter is `workspace_explorer`, an Observe-level adapter that lists files
under the configured workspace root and records a `ContextFrame`. It does not
read file contents, write files, execute commands, or follow paths outside the
workspace.

## Initial technology choices

- Base OS: Ubuntu-family Linux for broad hardware and dual-boot support
- Prototype UI: browser shell for fastest accessible iteration
- Runtime: Python standard library for a zero-dependency bootstrap
- Storage: JSON/JSONL until schemas stabilize; SQLite follows
- Local binding: `127.0.0.1` only by default

These are reversible implementation choices, not permanent product limits.
