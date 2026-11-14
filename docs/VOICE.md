# Voice interface plan

KHIP OS is voice-first because spoken intent should become the fastest ordinary
way to work with the computer. Keyboard and mouse remain important for
precision, accessibility, fallback, and user choice, but they should not be
required for common command, dictation, navigation, and approval flows.

## Goals

- Make voice input fast enough that it feels natural for everyday work.
- Support both dictation and command/control without mixing their safety rules.
- Keep listening state visible and user-controlled.
- Show live input level and clipping warnings so users can diagnose microphone
  gain before blaming transcription quality.
- Prefer local/private speech processing when practical.
- Keep raw audio out of persistent storage unless the user explicitly enables a
  diagnostic mode.
- Preserve keyboard and mouse as reliable fallback controls.

## Candidate: OpenWhisper

OpenWhisper is the preferred candidate to evaluate for Milestone 2 voice work.
It is not selected as a dependency yet. The project needs a short technical
evaluation before implementation so KHIP OS does not bake in a speech stack
that is slow, hard to package, privacy-hostile, or awkward for command control.

Evaluation questions:

- Can OpenWhisper run locally on the target Ubuntu-family base?
- What CPU, GPU, RAM, and model-size tradeoffs are realistic?
- What is the cold-start and steady-state latency for short commands?
- How well does it handle long-form dictation versus short imperative commands?
- Can it stream partial transcripts, or does it only return completed phrases?
- Does it provide enough confidence/timing data for command confirmation?
- How cleanly can it be packaged for a future desktop session and live image?
- What licenses, model licenses, and redistribution limits apply?

## Voice pipeline

Speech input must stay separated into explicit stages:

1. Capture: microphone state, permission, push-to-talk or active listening.
2. Transcribe: audio becomes text through the selected speech engine.
3. Interpret: text is classified as dictation, command, navigation, or approval.
4. Plan: KHIP packets record intent and proposed specialist work.
5. Approve: sensitive actions require explicit confirmation.
6. Actuate: approved adapters perform work and emit receipts.

Transcription alone never implies execution. A transcript is input evidence, not
permission to act.

## Microphone level diagnostics

The browser shell includes a live microphone meter that uses Web Audio to show
RMS loudness, peak hold, and clipping risk while listening. This is a diagnostic
surface only. The current Web Speech API path does not expose a reliable way for
KHIP OS to lower the microphone gain before recognition, so users should adjust
input gain in operating-system or browser settings when the meter reaches the
red clipping zone.

When KHIP OS owns the speech-to-text pipeline through OpenWhisper or another
adapter, software gain, normalization, and automatic clipping protection can be
evaluated inside that adapter boundary.

## Modes

Dictation mode is for entering text into documents, prompts, comments, notes,
and fields. It should optimize accuracy, punctuation, editing commands, and
correction flow.

Command mode is for operating KHIP OS, selecting agents, navigating projects,
asking for plans, and requesting tool work. It should optimize latency,
confirmation, command grammar, and safety classification.

Approval mode is for granting or denying specific pending actions. It should use
short, unmistakable phrases and show the exact action being approved. Ambiguous
approval speech must fail closed.

## Listen models to evaluate

- Push-to-talk: safest default and easiest to reason about.
- Manual toggle: useful for longer dictation, but must stay visibly active.
- Wake phrase: useful later, but requires careful false-positive handling.
- Security-tiered mode: low-risk navigation can be more fluid; risky commands
  require explicit confirmation.

Milestone 2 should start with push-to-talk and manual toggle. Wake phrase work
belongs behind a later safety review.

## Acceptance criteria for first voice adapter

- Runs on Linux without cloud access for the default path, or clearly documents
  why a hosted path is being evaluated.
- Has deterministic tests around transcript classification and approval gating.
- Records voice-derived intents as normal KHIP packets.
- Does not persist raw audio by default.
- Keeps microphone state visible in the shell.
- Supports text fallback for every voice flow.
- Fails closed for unclear approvals or sensitive commands.

## Open decisions

- Required maximum latency for short commands.
- Minimum acceptable dictation quality before shipping as a default path.
- Whether hosted transcription is allowed as an explicit opt-in.
- How much command grammar should be fixed versus natural language.
- Whether Kip should speak responses, display them, or both.
