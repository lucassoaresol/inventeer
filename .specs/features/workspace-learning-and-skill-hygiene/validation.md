# Workspace Learning and Skill Hygiene Validation

**Verdict:** PASS
**Evidence range:** `6a465f3..632a492`
**Gate:** `python3 scripts/workspace-gate-evidence.py run --profile workspace` - passed, 28 suites
**Discrimination sensor:** 8 of 8 mutants killed
**Coverage:** 20 of 20 acceptance criteria, 5 of 5 edge cases

Verification ran as the standalone fresh-eyes pass described in the skill's Sub-Agent Delegation
section: the session's operating instructions forbid dispatching a sub-agent that the user did not
request, so the Verifier role was executed inline against the committed diff surface rather than by
a separate agent. Every criterion below is re-derived from `spec.md` and cited to `file:line`.

---

## P1: Prune orphaned APEX skill directories

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 WHEN `--prune-orphans --apply` THEN remove every `apex-*` without `SKILL.md` | Directory gone from disk | `scripts/test-sync-apex-commands.sh:209-211` - `[[ ! -e "$orphans/apex-vazio" ]]`, `apex-sem-manifesto`, `apex-com-subdir` | PASS |
| AC2 WHERE `--prune-orphans` is used, `--catalog` is not required | Runs to completion with no catalog argument | `scripts/test-sync-apex-commands.sh:198` - `run --check --prune-orphans --skills-dir "$orphans"` | PASS |
| AC3 SHALL preserve `apex-*` holding `SKILL.md` | File still present | `scripts/test-sync-apex-commands.sh:214` - `[[ -f "$orphans/apex-valido/SKILL.md" ]]` | PASS |
| AC4 SHALL preserve non-`apex-` directories | File still present | `scripts/test-sync-apex-commands.sh:215` - `[[ -f "$orphans/nao-apex/SKILL.md" ]]` | PASS |
| AC5 WHEN `--check` and orphans exist THEN list each, write nothing, exit 1 | Exit 1, each name listed, tree untouched | `scripts/test-sync-apex-commands.sh:198-206` - `if run ...; then fail`, `grep -q '\[ORFAO\] (3)'`, `[[ -d "$orphans/$name" ]]` | PASS |
| AC6 WHEN `--check` and no orphan THEN report clean, exit 0 | Exit 0 with the clean message | `scripts/test-sync-apex-commands.sh:219-222` - `grep -q 'Nenhum diretório órfão'` | PASS |
| AC7 IF combined with `--catalog` THEN exit 2 | Usage error, exit 2 | `scripts/test-sync-apex-commands.sh:226-227` - `assert_exit_2 "--prune-orphans com --catalog"` | PASS |
| AC8 IF skills directory missing THEN exit 2 | Exit 2, directory not created | `scripts/test-sync-apex-commands.sh:230-232` - `assert_exit_2` + `[[ ! -e "$orphans/nao-existe" ]]` | PASS |

**Independent test:** executed against the real tree - `--check` listed exactly the 27 predicted
orphans and exited 1; `--apply` left `.agents/skills/apex-all-tools` as the only `apex-*` entry; the
re-run exited 0; all 8 `.claude/skills` symlinks still resolve (`find -xtype l` returned 0).

## P1: Merge lesson recurrences by similarity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 SHALL attempt exact key match before similarity | Exact lookup runs first | `.agents/skills/tlc-spec-driven/scripts/lessons.py:211-214` - `k = _key(...)` loop returns before `threshold = data["merge_similarity"]` at :216 | PASS (structural - see Findings 1) |
| AC2 WHEN same signal and Jaccard >= threshold THEN merge | Recurrence rises, no new id | `test-lessons.py:83,85` - `assert len(data["lessons"]) == 1`, `assert merged["recurrence"] == 2` | PASS |
| AC3 WHEN merging THEN keep stored text, append feature and evidence | Stored phrasing unchanged | `test-lessons.py:87-91` - `assert merged["text"] == "Bind validation evidence..."`, `assert "validation.md:R7" in merged["evidence"]` | PASS |
| AC4 SHALL never merge across signals | Separate lesson created | `test-lessons.py:123` - `assert len(data["lessons"]) == 3, "identical text under a different signal must not merge"` | PASS |
| AC5 WHEN several qualify THEN highest similarity, ties by lowest id | `L-800` wins over `L-900` | `test-lessons.py:217-219` - `assert len(winner) == 1 and winner[0]["id"] == "L-800"` | PASS |
| AC6 WHERE absent THEN default 0.60 | Key materializes at 0.6 | `lessons.py:55` - `"merge_similarity": 0.60`; store after write carries `0.6` | PASS |
| AC7 IF threshold invalid THEN exit non-zero, write nothing | Exit 2, lesson count unchanged | `test-lessons.py:147-166` - loop over `(-0.1, 1.5, "0.6", True, None)`, `expect=2`, `assert len(after["lessons"]) == 4` | PASS |
| AC8 IF content-token set empty THEN no similarity merge | Two separate lessons | `test-lessons.py:269` - `assert len(stop) == 2, "empty content-token sets must not merge"` | PASS |
| AC9 WHEN merge reaches `promote_threshold` THEN confirmed | Status flips to confirmed | `test-lessons.py:86` - `assert merged["status"] == "confirmed"` | PASS |

**Independent test:** replaying the real 30-lesson store produced 30 of 30 correct self-identifications
and 0 false merges; the highest similarity between any two distinct same-signal lessons is 0.158
(`L-003`~`L-006`), a 3.8x margin below the 0.60 threshold.

## P2: Close accumulated learning state

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 WHEN feature closes THEN L-009..L-030 tracked | Present in `git ls-files` | `git show 632a492:.specs/lessons.json` contains all 22 ids; `git ls-files .specs/lessons.json .specs/LESSONS.md` lists both | PASS |
| AC2 WHEN Handoff rewritten THEN status is not `stale` | `state` field reports `fresh` | `python3 scripts/workspace-handoff.py status` -> `{"reason": "match", "state": "fresh"}` | PASS |
| AC3 Handoff SHALL record SHA, publication, contract, operational status | All four fields present | `.specs/STATE.md:874-879` - `Valid at SHA`, `Publication state`, `Contract status`, `Operational status` | PASS |

---

## Edge Cases

| Edge case | `file:line` + assertion | Result |
| --- | --- | --- |
| `apex-*` path is a regular file - untouched | `scripts/test-sync-apex-commands.sh:216` - `[[ -f "$orphans/apex-arquivo-regular" ]]` | PASS |
| `apex-*` holds files but no `SKILL.md` - removed | `scripts/test-sync-apex-commands.sh:210` - `[[ ! -e "$orphans/apex-sem-manifesto" ]]` | PASS |
| Identical similarity tie - lowest id wins | `test-lessons.py:217` - `winner[0]["id"] == "L-800"` with `L-900` listed first in the store | PASS |
| Threshold 1.0 reduces to exact-match-only | `test-lessons.py:143` - `assert len(data["lessons"]) == 4` | PASS |
| Merge into a quarantined lesson does not resurrect it | `test-lessons.py:241` - `assert touched[0]["status"] == "quarantined"` | PASS |

---

## Discrimination Sensor

Mutants were injected into a disposable `git worktree` at `HEAD`, never the real tree. After the
run, the scratch reported 0 porcelain lines, the worktree was removed with `--force`, and the real
tree matched its pre-sensor baseline.

| Mutant | Injected defect | Suite | Result |
| --- | --- | --- | --- |
| M1 | `[[ -f "$dir/SKILL.md" ]] && continue` inverted to `\|\|` | sync | KILLED - `expected 3 orphans listed` |
| M2 | `[[ -z "$CATALOG" ]] \|\| usage` removed | sync | KILLED - `exited with 0 instead of 2` |
| M3 | `--check` exits 0 instead of 1 on divergence | sync | KILLED - `should exit 1 while orphans exist` |
| M4 | Missing skills directory created instead of failing | sync | KILLED - `exited with 0 instead of 2` |
| M5 | Cross-signal guard removed from `_find` | lessons | KILLED - `identical text under a different signal must not merge` |
| M6 | Tie-break flipped to highest id | lessons | KILLED - `tie must break on lowest id, got ['L-900']` |
| M7 | Threshold comparison replaced by `score < 0.0` | lessons | KILLED - `an unrelated same-signal lesson must stay separate` |
| M8 | Range validation of `merge_similarity` removed | lessons | KILLED - invalid threshold accepted a write |

**8 of 8 killed.** No surviving mutant, so no fix task was raised.

---

## Test Integrity

| Suite | Before | After | Delta |
| --- | --- | --- | --- |
| `scripts/test-sync-apex-commands.sh` | 16 | 21 | +5, none removed |
| `.agents/skills/tlc-spec-driven/scripts/test-lessons.py` | 2 | 10 | +8, none removed |
| Aggregate `scripts/test-workspace.sh` | 28 suites | 28 suites | unchanged, all passing |

No assertion was weakened and no test was deleted or skipped.

---

## Findings

1. **Spec-precision gap on APX/LSN AC1 (ordering).** "SHALL attempt an exact normalized-key match
   before any similarity comparison" describes an internal ordering that no black-box test can
   discriminate: identical text scores a Jaccard of 1.0, so it merges under either order at any
   threshold. The criterion is verified structurally at `lessons.py:211-216`, and the exact path is
   exercised indirectly by `test-lessons.py:143`. Stated as an observable outcome, the criterion
   should have constrained cost or the tie-break, not the sequence.

2. **A deviation from the planned Value Increment boundary.** `tasks.md` planned VI-003 as a single
   commit holding T4 and T5. T5 was moved to the closure commit because `workspace-handoff.py status`
   can only be observed after the Handoff is written, and writing a Handoff that asserts an unproven
   `fresh` state would have inverted the evidence order. The rollback boundary is unchanged: both
   commits are state-only.

3. **The Handoff contract cannot declare the lessons store as closure evidence.**
   `validate_relative_path` at `scripts/workspace-handoff.py:137` accepts only `.specs/STATE.md` and
   paths under `.specs/features/`. Any commit touching `.specs/lessons.json` after the recorded SHA
   is therefore a non-evidence descendant and forces `stale` (`scripts/workspace-handoff.py:337`).
   This is the structural reason L-009..L-030 stayed untracked for nine days: committing them and
   keeping a fresh Handoff were mutually exclusive under AD-046 unless the Handoff is re-anchored
   afterwards, which is what this feature did. Worth an AD-level decision, not a silent workaround.
