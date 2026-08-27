# Workspace Learning and Skill Hygiene Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: none - no architectural decision; both changes extend an existing script contract.
**Status**: Draft

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: `AGENTS.md`, `scripts/test-workspace.sh` (aggregate suite listing every contract test).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Shell tooling (`scripts/*.sh`) | integration | Every declared mode plus each lifecycle edge case, not only the primary path (L-008) | `scripts/test-<name>.sh` | `bash scripts/test-<name>.sh` |
| Python tooling (`scripts/*.py`, skill `scripts/*.py`) | unit + integration | All branches; 1:1 to spec ACs; every listed edge case has a test | `scripts/test-<name>.py`, `<skill>/scripts/test-<name>.py` | `python3 <path>` |
| Versioned state (`.specs/**`, Handoff) | none | Build gate only - asserted by existing contract suites | - | build gate only |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After a task touching one tool | `bash scripts/test-sync-apex-commands.sh` or `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` | N/A |
| Full | After a phase completes | `bash scripts/test-workspace.sh` | N/A - suite is pure Python/bash, no browser or container |
| Build | Before declaring the feature done | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | N/A |
| Diff integrity | At feature validation, against the evidence range | `git diff --check <evidence-base>..<evidence-head>` | N/A |

Machine snapshot at planning time: 12 CPUs, 2.4 GB of 3.9 GB memory available, load 1.10. The
aggregate suite completed well inside these limits, so no shard recipe is required.

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | Skill discovery in both engines exposes exactly one APEX entry, and orphan directories can never silently return | APX-01..APX-06 | T1, T2 | Full | `scripts/sync-apex-commands.sh` and its suite revert together; no other tool depends on the new mode | `fix(workspace): prune orphaned apex skill directories` |
| VI-002 | A reformulated lesson merges into the lesson it restates, so recurrence and promotion reflect reality | LSN-01..LSN-06 | T3 | Full | Vendored skill file and its suite revert as one unit, isolated from workspace scripts | `feat(tlc): merge lesson recurrences by similarity` |
| VI-003 | Accumulated learning is tracked and the Handoff is authoritative at the current SHA | STA-01, STA-02 | T4, T5 | Build | State-only commit; reverting restores the prior Handoff and lesson store without touching tooling | `chore(workspace): record accumulated lessons and close handoff` |

---

## Execution Plan

Phases are ordered and run sequentially - each phase completes before the next begins, and tasks within a phase execute in order.

### Phase 1: Skill hygiene

```
T1 → T2
```

### Phase 2: Lessons merge axis

```
T3
```

### Phase 3: State closure

```
T4 → T5
```

---

## Task Breakdown

### T1: Add orphan pruning to APEX synchronization

**What:** Add a `--prune-orphans` mode that removes `apex-*` directories lacking `SKILL.md` without consulting the MCP catalog.
**Where:** `scripts/sync-apex-commands.sh`
**Depends on:** None
**Reuses:** Existing `--check`/`--apply` mode parsing, `to_remove` reporting, and the fixture harness in `scripts/test-sync-apex-commands.sh`
**Requirement:** APX-01, APX-02, APX-03, APX-04, APX-05, APX-06
**Value Increment:** VI-001
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] `--prune-orphans` runs without `--catalog` and rejects being combined with it
- [ ] Empty `apex-*` and `apex-*` holding files but no `SKILL.md` are both removed
- [ ] `apex-*` with `SKILL.md`, non-`apex` directories, and `apex-*` regular files survive
- [ ] `--check` writes nothing, lists each orphan, exits 1 when orphans exist and 0 when clean
- [ ] Missing skills directory exits 2
- [ ] Gate check passes: `bash scripts/test-sync-apex-commands.sh`
- [ ] Test count: existing assertions plus the new orphan cases all pass, none removed

**Tests:** integration
**Gate:** quick

---

### T2: Remove the orphaned APEX directories

**What:** Apply the new mode to the real skills tree so only `apex-all-tools` remains.
**Where:** `.agents/skills/`
**Depends on:** T1
**Reuses:** The `--prune-orphans --apply` mode delivered by T1
**Requirement:** APX-01
**Value Increment:** VI-001
**Tools:** shell
**Done when:**

- [ ] `ls -d .agents/skills/apex-*/ | wc -l` returns 1 and it is `apex-all-tools`
- [ ] `bash scripts/sync-apex-commands.sh --prune-orphans --check` exits 0
- [ ] `.claude/skills/` symlinks are unchanged
- [ ] Gate check passes: `bash scripts/test-workspace.sh`

**Tests:** none
**Gate:** full

---

### T3: Merge lesson recurrences by token-set similarity

**What:** Add a similarity fallback to lesson lookup so a reformulated lesson merges into the stored lesson it restates.
**Where:** `.agents/skills/tlc-spec-driven/scripts/lessons.py`
**Depends on:** None
**Reuses:** Existing `_norm`, `_key`, `_find`, and `DEFAULTS` handling, plus the harness in `test-lessons.py`
**Requirement:** LSN-01, LSN-02, LSN-03, LSN-04, LSN-05, LSN-06
**Value Increment:** VI-002
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] Exact-key match is attempted before any similarity comparison
- [ ] Same-signal similarity at or above `merge_similarity` merges and keeps the stored text
- [ ] Different signals never merge, at any similarity
- [ ] Highest similarity wins, ties broken by lowest lesson id
- [ ] `merge_similarity` defaults to 0.60 and an out-of-range or non-numeric value exits non-zero writing nothing
- [ ] Empty content-token sets do not merge; threshold 1.0 reduces to exact-match behavior
- [ ] A merge reaching `promote_threshold` sets status to `confirmed`; a quarantined target stays quarantined
- [ ] Replaying the real 30-lesson store produces zero similarity merges
- [ ] Gate check passes: `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py`
- [ ] Test count: existing assertions plus the new similarity cases all pass, none removed

**Tests:** unit
**Gate:** quick

---

### T4: Record the accumulated lessons

**What:** Commit lessons L-009 through L-030 so the durable learning layer is tracked.
**Where:** `.specs/lessons.json`
**Depends on:** None
**Reuses:** Existing store schema and the renderer in `lessons.py`
**Requirement:** STA-01
**Value Increment:** VI-003
**Tools:** shell
**Done when:**

- [ ] `git ls-files` shows the store containing L-009..L-030
- [ ] `.specs/LESSONS.md` matches what `lessons.py` renders from the store
- [ ] Gate check passes: `python3 scripts/workspace-gate-evidence.py run --profile workspace`

**Tests:** none
**Gate:** build

---

### T5: Close the Handoff at the current SHA

**What:** Rewrite the Handoff section so resuming starts from authoritative state.
**Where:** `.specs/STATE.md`
**Depends on:** T4
**Reuses:** `scripts/workspace-handoff.py write` and the AD-046 contract
**Requirement:** STA-02
**Value Increment:** VI-003
**Tools:** shell
**Done when:**

- [ ] Handoff records behavioral SHA, publication state, contract status, and operational status
- [ ] `python3 scripts/workspace-handoff.py status` does not report `stale`
- [ ] Only `## Handoff` changed; the Decisions section is untouched
- [ ] Gate check passes: `python3 scripts/workspace-gate-evidence.py run --profile workspace`

**Tests:** none
**Gate:** build

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3

Phase 1:  T1 ------→ T2
Phase 2:  T3
Phase 3:  T4 ------→ T5
```

Execution is strictly sequential - there is no intra-phase parallelism. Five tasks pack into a single batch, so execution happens inline with no sub-agents.

---

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1: Orphan pruning mode | One script mode | Its suite + one revert | Granular |
| T2: Apply the pruning | Untracked disk state | Re-runnable check, no revert surface | Granular |
| T3: Similarity merge axis | One lookup function | Its suite + one revert | Granular |
| T4: Record lessons | One store file | One revert | Granular |
| T5: Close Handoff | One document section | One revert | Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | no inbound arrow | Match |
| T2 | T1 | T1 → T2 | Match |
| T3 | None | no inbound arrow (own phase) | Match |
| T4 | None | no inbound arrow (phase order already sequences it after T3) | Match |
| T5 | T4 | T4 → T5 | Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Shell tooling | integration | integration | OK |
| T2 | Untracked skill directories - no code layer | none | none | OK |
| T3 | Python tooling | unit + integration | unit | OK |
| T4 | Versioned state | none | none | OK |
| T5 | Versioned state | none | none | OK |

T3 declares `unit` because `test-lessons.py` drives the module directly against a temporary store,
which is the integration level available for this layer; no separate integration surface exists.
