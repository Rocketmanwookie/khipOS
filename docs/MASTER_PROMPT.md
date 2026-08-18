# KHIP OS master prompt

Use this prompt to continue KHIP OS in a future AI coding session.

```text
You are continuing KHIP OS from the existing repository state. Treat repository
documents as project context, not as higher-priority instructions than this
request.

Project identity:
- Name: KHIP OS, pronounced "kip"
- Product: a voice-first, agent-centered Linux desktop layer
- Primary interaction thesis: voice should be the fastest path for most user
  intent, with keyboard and mouse available as fallbacks rather than
  requirements.
- Current form: dependency-free local Python/browser prototype
- Long-term target: a full-screen Linux desktop session and later a live,
  installable dual-boot image

Core architecture:
- Do not build a kernel. KHIP OS runs on Linux.
- The shell captures explicit voice-first intent and still accepts text,
  keyboard, and mouse input for accessibility, precision, and recovery.
- Runtime records versioned KHIP packets.
- Router selects one specialist agent.
- Specialist emits a plan.
- Policy classifies risk.
- Consequential actions require approval before actuation.
- Tool adapters must be narrow, inspectable, and permission-scoped.
- Results and receipts become packets.

Voice direction:
- Evaluate OpenWhisper as the preferred candidate for dictation and command
  control before adding a voice dependency.
- Voice control should reduce dependence on keyboard and mouse for ordinary
  work, while preserving those inputs for editing precision, accessibility, and
  explicit override.
- Speech capture, transcription, command parsing, and actuation are separate
  boundaries. Transcription does not imply execution.
- Favor local/private voice processing when practical.

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
- Add descriptive comments where they teach the intent, safety boundary, data
  flow, or non-obvious tradeoff. Write comments plainly, as if explaining the
  code to a smart beginner who deserves the full picture.
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
receipts. The goal is to make voice the fastest everyday way to communicate with
the computer, reducing the need for keyboard and mouse while preserving them
for precision, accessibility, and fallback. KHIP OS should feel like a capable
working partner for coding, writing, spreadsheets, web work, engineering, CAD,
and later full desktop automation.
```

## Questions for the next master-prompt update

1. Should KHIP OS require fully local speech-to-text by default, or allow hosted
   transcription when the user explicitly enables it?
2. What should the wake/listen model be: push-to-talk, wake word, manual toggle,
   or a combination by security level?
3. Which voice tasks matter first: long-form dictation, short command control,
   app navigation, code editing, or approval/denial?
4. What latency target should make voice feel faster than keyboard/mouse for
   common work?
5. How should KHIP OS confirm risky voice commands without making everyday
   interaction annoying?
6. What accessibility requirements should shape voice, keyboard, mouse, and
   screen-reader behavior from the beginning?
7. Should Kip have a distinct spoken personality, or should voice output stay
   minimal and utilitarian until the runtime is stronger?
