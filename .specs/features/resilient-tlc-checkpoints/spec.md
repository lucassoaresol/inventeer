# Resilient TLC Checkpoints Specification

**Status:** Approved by the user's 2026-08-02 implementation authorization
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

Portal deliveries executed with Codex and TLC can span several continuation sessions after abrupt
engine failures. TLC currently persists its handoff only during a conscious pause or shutdown, so
a crash after a verified transition can force the next session to reconstruct completed gates,
validated surfaces, active processes, and the precise next action from histories.

## Goals

- Persist a deterministic local checkpoint after each declared verifiable transition.
- Keep checkpoints in the ignored Portal TLC artifact route established by AD-031.
- Preserve decisions and unrelated state-file sections exactly when updating the handoff.
- Fail without corrupting the last valid checkpoint.
- Make repeated writes with identical input a filesystem no-op.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Detecting or handling the crash itself | A checkpoint reduces the recovery window; it cannot run after an abrupt process loss. |
| Synchronizing checkpoints across machines | AD-031 defines local, ignored, non-durable artifacts. |
| Changing the vendored TLC skill | The checkpoint obligation is specific to this workspace's Portal execution route. |
| Applying checkpoints to Claude/APEX or other products | AD-031 is restricted to Portal + Codex + TLC. |
| Replacing Linear, pull requests, Git, or product artifacts | The checkpoint is local execution memory, not canonical delivery evidence. |
| Building another session-history auditor | AD-033 and `scripts/audit-session-history.py` already provide that capability. |

## Assumptions and Decisions

| Decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Persistence scope | Local to each machine | The user approved the local checkpoint contract; cross-machine synchronization is separate. | Yes |
| Target | `session-context/portal/<INV-ID>/tlc/STATE.md` | It reuses AD-031 without dirtying a product or workspace worktree. | Yes |
| Target selection | Workspace root plus validated `INV-ID` | The helper must not accept an arbitrary output path. | Yes |
| Update scope | Replace only `## Handoff` | Decisions and unrelated sections have independent lifecycles. | Yes |
| Time source | No implicit timestamp | Identical inputs must produce identical bytes and a true no-op. | Yes |
| Trigger values | `gate`, `commit`, `bundle`, `pr`, or `validation` | These are the approved verifiable transitions. | Yes |
| Integration | Workspace instructions, helper, and contract tests | The vendored TLC remains unchanged. | Yes |
| Cleanup | Existing AD-031 lifecycle | The local issue directory becomes eligible after merge and issue closure. | Yes |

**Open questions:** none.

## P1: Persist a Recoverable Execution Handoff

**User Story:** As the workspace owner, I want each stable delivery transition checkpointed so that
a continuation session can resume from precise local execution state after an abrupt failure.

**Acceptance Criteria:**

1. WHEN the helper receives a workspace root, a valid `INV-[1-9][0-9]*` issue identifier, and all
   required handoff values, THEN it SHALL target exactly
   `<workspace>/session-context/portal/<INV-ID>/tlc/STATE.md`.
2. WHEN the target does not exist, THEN the helper SHALL create a UTF-8 state file containing
   `# TLC State`, an empty `## Decisions` section, and one `## Handoff` section.
3. WHEN a checkpoint is written, THEN `## Handoff` SHALL contain exactly these ordered fields:
   `Feature`, `Phase / Task`, `Completed`, `Checkpoint event`, `Validated SHA / surface`,
   `In-progress process`, `Next step`, `Blockers`, `Uncommitted files`, `Branch`, and
   `Validation state`.
4. WHEN the state file already contains decisions or sections after `## Handoff`, THEN the helper
   SHALL preserve every byte outside the handoff body.
5. WHEN identical checkpoint input is submitted again, THEN the helper SHALL emit `unchanged`,
   preserve the target inode and bytes, and perform no replacement.
6. WHEN checkpoint content changes, THEN the helper SHALL write a temporary file in the target
   directory, flush it, atomically replace the target, and emit `updated`.
7. WHEN atomic replacement fails, THEN the helper SHALL return non-zero, preserve the previous
   target bytes, and leave no temporary checkpoint file behind.

## P1: Enforce the Workspace Boundary

**User Story:** As the workspace owner, I want malformed or unsafe checkpoint requests rejected so
that local recovery state cannot escape its intended route or corrupt Markdown structure.

**Acceptance Criteria:**

1. WHEN the issue identifier does not match `INV-[1-9][0-9]*`, THEN the helper SHALL return non-zero
   before creating any target directory or file.
2. WHEN any field contains a newline, carriage return, or an empty required value, THEN the helper
   SHALL return non-zero without changing the previous checkpoint.
3. WHEN the computed target or an existing symlink resolves outside the supplied workspace root,
   THEN the helper SHALL return non-zero without writing outside the workspace.
4. WHEN `checkpoint event` is not one of `gate`, `commit`, `bundle`, `pr`, or `validation`, or
   `validation state` is not one of `not-started`, `in-progress`, `passed`, `failed`, or `blocked`,
   THEN the helper SHALL return non-zero without changing the previous checkpoint.
5. WHEN the handoff is persisted, THEN uncommitted state SHALL contain path labels only and the
   checkpoint SHALL NOT contain transcript bodies, diffs, credentials, customer data, or production
   output.

## P1: Require Checkpoints at Stable Transitions

**User Story:** As a future Codex continuation, I want predictable checkpoint timing so that the
last file-backed state describes a completed transition rather than an arbitrary tool call.

**Acceptance Criteria:**

1. WHEN Portal + Codex + TLC completes a gate, creates an atomic commit, creates a review bundle,
   creates or updates a pull request, or changes validation state, THEN workspace instructions SHALL
   require invoking the helper after the transition succeeds.
2. WHEN a transition fails before producing its expected outcome, THEN workspace instructions SHALL
   prohibit advancing the checkpoint as though it succeeded.
3. WHEN the contract is documented, THEN it SHALL state that the checkpoint is ignored, local,
   ephemeral, non-canonical, non-portable across machines, and eligible for cleanup only under
   AD-031's post-merge and closed-issue lifecycle.
4. WHEN the decision is recorded, THEN it SHALL use AD-036 and SHALL preserve AD-031, AD-032, and
   the vendored TLC skill unchanged.

## Edge Cases

- A state file with zero or multiple `## Handoff` sections is malformed and must be rejected without
  changing it.
- Comma-separated display values are derived from repeatable single-line CLI values; an empty list
  is rendered as `none`.
- A stale process description is recovery context only; the continuation must re-check liveness
  before treating it as running.
- A crash between declared transitions can still lose work since the last checkpoint; this is an
  explicit residual risk, not a successful-transition checkpoint failure.
- Concurrent writers are not coordinated; Portal delivery remains a single-writer workflow per
  issue on one machine.

## Requirement Traceability

| Requirement | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- |
| RTCP-01 | ISSUE | Eight INV-3145 session files and four post-retrospective continuations | Helper | Pending |
| RTCP-02 | DECISION | User approved local per-machine checkpoints | Helper | Pending |
| RTCP-03 | INHERITED | AD-031 Portal TLC artifact route | Helper | Pending |
| RTCP-04 | INHERITED | TLC section-scoped memory invariant | Helper | Pending |
| RTCP-05 | SAFETY | Abrupt failure must not corrupt the last checkpoint | Helper | Pending |
| RTCP-06 | SAFETY | Target and Markdown input boundaries | Helper | Pending |
| RTCP-07 | ISSUE | Handoff currently persists only on conscious pause/end | Contract | Pending |
| RTCP-08 | INHERITED | AD-027 privacy boundary | Contract | Pending |
| RTCP-09 | INHERITED | AD-031 local lifecycle and cross-machine limitation | Contract | Pending |
| RTCP-10 | DECISION | Use AD-036 and leave vendored TLC unchanged | Contract | Pending |

**Coverage:** 10 requirements; all mapped to helper or contract work.

## Success Criteria

- A continuation can read the last successful transition from the issue-local `STATE.md` without
  inspecting transcript bodies.
- Repeating the same checkpoint changes neither bytes nor inode.
- Invalid input, path escape, malformed state, and replacement failure preserve the previous state.
- Contract tests enforce all five triggers and the local, non-canonical lifecycle.
- Targeted tests, the complete workspace gate, range diff integrity, and focused discrimination
  mutants pass without changing any product repository or the vendored TLC skill.
