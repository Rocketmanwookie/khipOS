# Safety and privacy model

## Invariants

- Listening state is always visible and user-controlled.
- Raw audio is not stored by the Milestone 1 runtime.
- Planning is not execution.
- External communication, purchases, deletion, privilege elevation, software
  installation, publishing, and command execution require authorization.
- Credentials do not enter agent prompts or event packets.
- Every action adapter declares its permissions and reversible behavior.
- A user can inspect and stop active agents.

## Authorization levels

1. Observe: read-only local state.
2. Prepare: drafts, plans, previews, and proposed diffs.
3. Act with approval: external or system-changing actions.
4. Blocked: actions forbidden by policy or unavailable permissions.

PSUDO is the planned physical authorization layer. It should complement, not
replace, scoped software permissions and an audit trail.
