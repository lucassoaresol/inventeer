# Symmetric Session Audit Contract Specification

**Status:** Validated
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

Contract v3 reports `continuations`, `compactions`, `aborted_turns`, `subagents` and their derived
per-session statistics for Codex, and none of them for Claude. AD-048 was grounded on "49.02% of
Codex sessions compacted" - a figure that has no Claude counterpart, so the same question cannot be
asked of both engines. Worse, the asymmetry is silent: a consumer reading the Claude block cannot
tell an unmeasured metric from a measured zero.

## Goals

- [x] Emit the same metric keys for both engines so a cohort can be compared field by field.
- [x] Measure, for Claude, every signal its transcript format actually carries.
- [x] Report an unmeasurable signal as `null` with a stated reason, never as `0`.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Inferring Claude compactions from heuristics such as token gaps | No marker was observed in 28 transcripts; a guess would recreate the false-confidence this feature removes. |
| Backfilling historical cohorts under the new contract | Receipts record the contract version that produced them; re-deriving old ones is a separate act. |
| Changing what Codex measures | Codex coverage is already complete; only its schema gains the support map. |
| Emitting cost or duration figures | `cost-state` exists only in recent Claude transcripts and has no Codex counterpart; adding it would create a new asymmetry while fixing another. |
| Reading or emitting transcript content | The auditor is metadata-only by contract. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Unmeasurable metrics representation | `null` plus an `unsupported_metrics` reason map | A `0` asserts "did not happen"; `null` asserts "not observable here", which is the true state. | y |
| Claude abort detection | Exact match on the two sentinel strings | Substring matching hits transcript content that merely discusses interruption; the 28-file corpus yields 15 either way, but only exact matching is sound. | y |
| Claude continuations | Unsupported, not zero | A resumed Claude session appends to the same transcript; 28 files carry 28 distinct session ids with no duplication, so no second instance exists to count. | y |
| Claude compactions | Unsupported, not zero | No `compact_boundary` subtype and no `isCompactSummary` record appears in any of the 28 transcripts; the observed subtypes are unrelated. | y |
| Claude subagents | Counted from `<session>/subagents/*.meta.json` | The sidecar directory is authoritative and its total of 23 independently matches the 23 `Agent` tool calls in the same corpus. | y |
| Version bump | `contract_version` 4 | AD-046 established that a contract change bumps the version and may break consumers; the key set changes for both engines. | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: Compare the same metrics across engines ⭐ MVP

**User Story**: As the workspace maintainer, I want both engine blocks to carry the same metric
keys, so that a retrospective can compare them without knowing which fields each engine happens to
support.

**Why P1**: A decision like AD-048 is currently derivable for one engine only.

**Acceptance Criteria**:

1. The report SHALL emit `contract_version` 4.  <!-- ubiquitous -->
2. The Codex and Claude blocks SHALL expose an identical set of metric keys.  <!-- ubiquitous -->
3. WHEN a metric is not observable for an engine THEN that engine's block SHALL set it to `null`.  <!-- event-driven -->
4. WHEN a metric is set to `null` THEN the engine's `unsupported_metrics` map SHALL carry a non-empty reason for that exact key.  <!-- event-driven -->
5. The system SHALL NOT list a measured metric in `unsupported_metrics`.  <!-- ubiquitous -->
6. WHERE an engine measures every metric the system SHALL emit an empty `unsupported_metrics` map.  <!-- optional-feature -->

**Independent Test**: Both blocks return the same `sorted(keys)`, and every `null` value has a
reason entry.

---

### P1: Measure Claude aborts and subagents ⭐ MVP

**User Story**: As the workspace maintainer, I want Claude interruptions and subagents counted, so
that engine comparison rests on measurement rather than absence.

**Why P1**: These are the signals the Claude format genuinely carries.

**Acceptance Criteria**:

1. WHEN a user record's text block equals `[Request interrupted by user]` or
   `[Request interrupted by user for tool use]` THEN the system SHALL count one aborted turn.  <!-- event-driven -->
2. The system SHALL NOT count a record whose text merely contains a sentinel as a substring.  <!-- ubiquitous -->
3. The system SHALL report `sessions_with_aborts`, `max_aborts_per_session`, and
   `sessions_with_aborts_percent` derived from the accepted sessions.  <!-- ubiquitous -->
4. WHEN a session directory contains `subagents/*.meta.json` THEN the system SHALL count those files
   as that session's subagents.  <!-- event-driven -->
5. IF a session has no `subagents` directory THEN the system SHALL count zero subagents for it
   without failing.  <!-- unwanted-behavior -->
6. WHILE no session is accepted the system SHALL report 0.0 for every derived percentage rather than
   dividing by zero.  <!-- state-driven -->
7. The system SHALL count aborts and subagents only for sessions accepted by the cwd, window, and
   exclusion filters.  <!-- ubiquitous -->

**Independent Test**: Against the real project directory the auditor reports 15 aborted turns across
11 sessions, a maximum of 3, and 23 subagents.

---

### P2: Keep the rendered and receipt surfaces honest

**User Story**: As the workspace maintainer, I want the text and receipt outputs to distinguish an
unmeasured metric from a zero, so a reader cannot misread the table.

**Why P2**: The JSON is correct without it, but the text output is what a retrospective reads.

**Acceptance Criteria**:

1. WHEN rendering a `null` metric THEN the text output SHALL print `n/a` rather than a number.  <!-- event-driven -->
2. WHEN an engine has unsupported metrics THEN the text output SHALL print each key with its
   reason.  <!-- event-driven -->
3. The receipt output SHALL carry the same metric keys and reason map as the JSON report.  <!-- ubiquitous -->
4. The receipt SHALL continue to exclude physical paths and session identifiers.  <!-- ubiquitous -->

**Independent Test**: `--format text` shows `n/a` for Claude compactions with its reason; the
receipt round-trips the same keys.

---

## Edge Cases

- IF a sentinel string appears inside a tool result rather than a text block THEN the system SHALL
  NOT count it, because tool output can echo a transcript.
- WHEN the `subagents` directory exists but holds no `.meta.json` file THEN the system SHALL count
  zero for that session.
- IF a session directory name does not correspond to an accepted session THEN its subagent files
  SHALL NOT be counted.
- WHEN no Claude history root exists THEN the empty block SHALL still carry every metric key and the
  reason map, so the schema does not depend on the data.
- IF `unsupported_metrics` names a key absent from the block THEN the contract is violated and the
  test SHALL fail.

---

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| SSA-01 | P1: Compare | ISSUE | Retrospective finding 5: v3 is asymmetric | Tasks | Pending |
| SSA-02 | P1: Compare | INHERITED | AD-046 bumps the contract version on a schema change | Tasks | Pending |
| SSA-03 | P1: Compare | SAFETY | A measured `0` and an unmeasurable metric must not be conflated | Tasks | Pending |
| SSA-04 | P1: Measure | DECISION | Exact sentinel matching chosen over substring | Tasks | Pending |
| SSA-05 | P1: Measure | ISSUE | Aborts and subagents are carried by the Claude format | Tasks | Pending |
| SSA-06 | P1: Measure | SAFETY | Derived percentages must not divide by zero | Tasks | Pending |
| SSA-07 | P2: Surfaces | ISSUE | The text output is what a retrospective reads | Tasks | Pending |
| SSA-08 | P2: Surfaces | INHERITED | AD-046 receipt sanitization must survive the change | Tasks | Pending |
| SSA-09 | P2: Surfaces | INHERITED | AGENTS.md names the contract version and must not drift | Tasks | Pending |

**Coverage:** 9 total, 9 mapped to tasks, 0 unmapped

---

## Success Criteria

- [ ] `sorted(report["codex"])` equals `sorted(report["claude"])`.
- [ ] Every `null` metric has a reason; no measured metric has one.
- [ ] The real corpus reports 15 aborted turns, 11 sessions with aborts, max 3, and 23 subagents.
- [ ] `--format text` prints `n/a` plus a reason for Claude compactions and continuations.
- [ ] AGENTS.md names contract v4.
- [ ] `scripts/workspace-gate-evidence.py run --profile workspace` passes.
