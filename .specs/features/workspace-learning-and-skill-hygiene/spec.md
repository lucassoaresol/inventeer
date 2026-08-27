# Workspace Learning and Skill Hygiene Specification

**Status:** Draft
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

A sanitized retrospective over 27 Claude sessions and 119 Codex session files exposed two structural
defects in the workspace's own machinery. First, retiring the per-workflow APEX wrappers under
AD-051 left 27 empty `apex-*` directories on disk; Git does not track empty directories, so the
working tree reads clean while the Codex skill discoverer still enumerates them in every session.
Second, the lessons layer cannot promote: `lessons.py` merges a recurrence only when the fully
normalized lesson text is identical, so 30 lessons produced exactly 1 confirmed entry in seven weeks
and the layer behaves as a write-only log instead of a memory.

## Goals

- [ ] Let `sync-apex-commands.sh` reconcile orphaned `apex-*` directories without requiring an MCP
      catalog, and remove the 27 that exist today.
- [ ] Give `lessons.py` a second merge axis so reformulations of the same lesson recur and promote,
      without merging genuinely distinct lessons.
- [ ] Commit the 22 accumulated lessons (L-009..L-030) and close the Handoff at the current SHA.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Semantic or embedding-based lesson matching | `lessons.py` is stdlib-only by contract; an external model would break vendored portability. |
| Changing `promote_threshold`, `window_days` or `quarantine_threshold` | The thresholds are not the defect; the merge axis is. |
| Retroactively merging the existing 30 lessons | Recurrence must reflect observed features, not a batch rewrite of recorded history. |
| Restoring per-workflow APEX wrappers | AD-051 retired them; this feature only removes the residue. |
| Changes under `repos/` | Workspace-only maintenance. |
| Promoting the retrospective findings into new AD entries | Recording a transversal decision is a separate, user-owned act. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Merge axis for lessons | Same signal + token-set Jaccard >= threshold | User selected text similarity over scope-based merging so distinct lessons stay distinct. | y |
| Similarity threshold | 0.60 | Empirical: the maximum similarity between any two distinct same-signal lessons in the real 30-lesson store is 0.158, leaving 3.8x margin. | y |
| Orphan pruning needs no catalog | A dedicated mode that never consults the catalog | No valid catalog can ever produce an `apex-*` directory without `SKILL.md`, so an empty one is unwanted regardless of catalog content. | y |
| Canonical text on merge | The existing lesson's text is kept | The first grounded phrasing stays authoritative; the recurrence records the second feature, not a rewrite. | y |
| Stopword handling | Short tokens (<3 chars) and a fixed English stopword list are dropped before comparison | Function words inflate similarity between unrelated lessons and would erode the safety margin. | y |
| Vendored-skill commit | `lessons.py` and its test ship in a commit isolated from workspace scripts | AGENTS.md requires vendored TLC content to be updated in an isolated commit. | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: Prune orphaned APEX skill directories ⭐ MVP

**User Story**: As the workspace maintainer, I want orphaned `apex-*` directories removed without an
MCP catalog, so that retired wrappers stop costing context in every Codex session.

**Why P1**: The residue is paid on every Codex session and is invisible to Git, so no existing gate
can catch it.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHEN `sync-apex-commands.sh --prune-orphans --apply` runs THEN the system SHALL remove every
   directory under the skills directory whose name starts with `apex-` and that contains no
   `SKILL.md`.  <!-- event-driven -->
2. WHERE the `--prune-orphans` mode is used the system SHALL NOT require the `--catalog`
   argument.  <!-- optional-feature -->
3. The system SHALL preserve every `apex-*` directory that contains a `SKILL.md`.  <!-- ubiquitous -->
4. The system SHALL preserve every directory whose name does not start with `apex-`, whether or not
   it contains a `SKILL.md`.  <!-- ubiquitous -->
5. WHEN `sync-apex-commands.sh --prune-orphans --check` runs and at least one orphan exists THEN the
   system SHALL list each orphan, write no file, and exit 1.  <!-- event-driven -->
6. WHEN `sync-apex-commands.sh --prune-orphans --check` runs and no orphan exists THEN the system
   SHALL report a clean state and exit 0.  <!-- event-driven -->
7. IF `--prune-orphans` is combined with `--catalog` THEN the system SHALL exit 2 with a usage
   error.  <!-- unwanted-behavior -->
8. IF the skills directory does not exist THEN the system SHALL exit 2 with an explicit
   error.  <!-- unwanted-behavior -->

**Independent Test**: Run the mode against a fixture directory holding one empty `apex-x`, one
`apex-y` with `SKILL.md`, and one `nao-apex` directory; only `apex-x` disappears.

---

### P1: Merge lesson recurrences by similarity ⭐ MVP

**User Story**: As the workspace maintainer, I want a reformulated lesson to merge with the one it
restates, so that recurrence reflects reality and confirmed lessons actually accumulate.

**Why P1**: Without it the lessons layer records but never promotes, and Specify/Design load only
one confirmed lesson out of thirty.

**Acceptance Criteria**:

1. The system SHALL attempt an exact normalized-key match before any similarity comparison.  <!-- ubiquitous -->
2. WHEN no exact match exists and a stored lesson shares the incoming signal with a token-set
   Jaccard similarity greater than or equal to `merge_similarity` THEN the system SHALL merge the
   incoming lesson into that stored lesson.  <!-- event-driven -->
3. WHEN a merge occurs THEN the system SHALL keep the stored lesson's text unchanged and append the
   incoming feature and evidence.  <!-- event-driven -->
4. The system SHALL never merge two lessons that carry different signals, at any similarity.  <!-- ubiquitous -->
5. WHEN more than one stored lesson qualifies THEN the system SHALL merge into the one with the
   highest similarity, breaking ties by lowest lesson id.  <!-- event-driven -->
6. WHERE `merge_similarity` is absent from the store the system SHALL default it to 0.60.  <!-- optional-feature -->
7. IF `merge_similarity` is not a number in the closed interval 0.0 to 1.0 THEN the system SHALL
   exit non-zero with an explicit error and write no file.  <!-- unwanted-behavior -->
8. IF either lesson's content-token set is empty after stopword removal THEN the system SHALL NOT
   merge them by similarity.  <!-- unwanted-behavior -->
9. WHEN a similarity merge raises recurrence to `promote_threshold` THEN the system SHALL set the
   lesson status to `confirmed`.  <!-- event-driven -->

**Independent Test**: Add a lesson, then add a reworded restatement of it under a different feature;
recurrence becomes 2 and status becomes `confirmed`, while an unrelated same-signal lesson stays
separate.

---

### P2: Close accumulated learning state

**User Story**: As the workspace maintainer, I want the accumulated lessons committed and the
Handoff closed at the current SHA, so that resuming starts from authoritative state.

**Why P2**: It depends on P1 landing first, but the durable memory is currently outside Git and the
Handoff reads `stale`.

**Acceptance Criteria**:

1. WHEN the feature closes THEN the repository SHALL contain lessons L-009 through L-030 as tracked
   content.  <!-- event-driven -->
2. WHEN the Handoff is rewritten THEN `workspace-handoff.py status` SHALL report a state other than
   `stale`.  <!-- event-driven -->
3. The Handoff SHALL record the behavioral SHA, publication state, contract status, and operational
   status.  <!-- ubiquitous -->

**Independent Test**: `git ls-files` shows the lessons content and `workspace-handoff.py status`
no longer returns `stale`.

---

## Edge Cases

- IF an `apex-*` path is a file rather than a directory THEN the system SHALL leave it untouched.
- IF an `apex-*` directory holds files but no `SKILL.md` THEN the system SHALL treat it as an orphan
  and remove it, because a wrapper without its manifest is not discoverable as a skill.
- WHEN two stored lessons tie at the identical highest similarity THEN the system SHALL choose the
  lowest lesson id so the outcome does not depend on store order.
- IF `merge_similarity` equals 1.0 THEN the system SHALL behave equivalently to exact-match-only
  merging.
- WHEN the incoming lesson matches a `quarantined` lesson by similarity THEN the system SHALL merge
  into it without resurrecting it to `candidate` or `confirmed`.

---

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| APX-01 | P1: Prune orphans | ISSUE | Retrospective: 27 empty dirs, 119/119 Codex files enumerate them | Tasks | Pending |
| APX-02 | P1: Prune orphans | DECISION | User approved item A | Tasks | Pending |
| APX-03 | P1: Prune orphans | SAFETY | Deletion must not reach wrappers holding content | Tasks | Pending |
| APX-04 | P1: Prune orphans | SAFETY | Deletion must not reach non-apex skills | Tasks | Pending |
| APX-05 | P1: Prune orphans | INHERITED | `--check` writes nothing and exits 1 on divergence, per existing script contract | Tasks | Pending |
| APX-06 | P1: Prune orphans | INHERITED | L-008: assert declared lifecycle edge cases, not only the primary path | Tasks | Pending |
| LSN-01 | P1: Merge by similarity | INHERITED | Existing exact-key behavior must not regress | Tasks | Pending |
| LSN-02 | P1: Merge by similarity | DECISION | User selected text-similarity axis | Tasks | Pending |
| LSN-03 | P1: Merge by similarity | DECISION | Threshold 0.60, calibrated at max observed 0.158 | Tasks | Pending |
| LSN-04 | P1: Merge by similarity | SAFETY | Cross-signal merging would corrupt the signal taxonomy | Tasks | Pending |
| LSN-05 | P1: Merge by similarity | SAFETY | Determinism under ties keeps the store reproducible | Tasks | Pending |
| LSN-06 | P1: Merge by similarity | SAFETY | Invalid threshold must fail closed without writing | Tasks | Pending |
| STA-01 | P2: Close state | ISSUE | 22 lessons untracked for nine days | Tasks | Pending |
| STA-02 | P2: Close state | INHERITED | AD-046 Handoff contract | Tasks | Pending |

**Coverage:** 14 total, 14 mapped to tasks, 0 unmapped

---

## Success Criteria

- [ ] `ls -d .agents/skills/apex-*/ | wc -l` returns 1, and that entry is `apex-all-tools`.
- [ ] `sync-apex-commands.sh --prune-orphans --check` exits 0 on the cleaned tree.
- [ ] A reworded restatement of an existing lesson raises its recurrence instead of creating a new id.
- [ ] The 30-lesson real store produces zero similarity merges when replayed, confirming no false positive.
- [ ] `workspace-gate-evidence.py run --profile workspace` passes.
- [ ] `workspace-handoff.py status` does not report `stale`.
