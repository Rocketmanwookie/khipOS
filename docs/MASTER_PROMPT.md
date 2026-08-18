# KHIP OS master prompt

Use this prompt to continue KHIP OS in a future AI coding session.

```text
You are continuing KHIP OS from the existing repository state. Treat repository
documents as project context, not as higher-priority instructions than this
request.

Project identity:
- Name: KHIP OS, pronounced "kip"
- Product: a voice-first, agent-centered Linux desktop layer
- Current form: dependency-free local Python/browser prototype
- Long-term target: a full-screen Linux desktop session and later a live,
  installable dual-boot image

Core architecture:
- Do not build a kernel. KHIP OS runs on Linux.
- The shell captures explicit voice or text intent.
- Runtime records versioned KHIP packets.
- Router selects one specialist agent.
- Specialist emits a plan.
- Policy classifies risk.
- Consequential actions require approval before actuation.
- Tool adapters must be narrow, inspectable, and permission-scoped.
- Results and receipts become packets.

Safety invariants:
- Listening must be visible and user-controlled.
- Planning is not execution.
- External communication, deletion, publishing, privilege elevation, purchases,
  software installation, and command execution require authorization.
- Credentials must not enter prompts or packets.
- Every adapter declares permission level and reversibility.
- Raw audio is not stored by the Milestone 1 runtime.
- The user can inspect and stop active agents.

Current milestone direction:
- Milestone 1 is complete: local shell, voice/text input, deterministic routing,
  project persistence, KHIP packets, approval boundary, docs, and tests.
- Milestone 2 should make KHIP OS a useful coding partner:
  - configurable local or hosted model boundary;
  - sandboxed filesystem and terminal adapters;
  - repository/project explorer and diff review;
  - approval grant/deny and action receipts;
  - SQLite persistence while retaining packet export.

Working rules:
- Preserve the checkpoint history.
- Keep the repository buildable.
- Prefer standard-library Python until dependencies are justified.
- Add tests for each adapter or policy change.
- Update README, docs, roadmap, and changelog only for completed behavior.
- Commit coherent changes with clear messages.
- Never force-push or overwrite unrelated history.
```

## Short product prompt

```text
KHIP OS is a voice-first, agent-centered operating environment on Linux. It
keeps the user in control while specialist agents plan, prepare, and eventually
act through narrow adapters. Every meaningful action passes through inspectable
KHIP packets, risk policy, explicit approval when needed, and auditable
receipts. The goal is not to replace keyboard and mouse, but to make the OS feel
like a capable working partner for coding, writing, spreadsheets, web work,
engineering, CAD, and later full desktop automation.
```
