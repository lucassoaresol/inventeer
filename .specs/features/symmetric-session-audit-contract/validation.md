# Symmetric Session Audit Contract Validation

**Verdict:** PASS
**Evidence range:** `6044338..HEAD`
**Gate:** `python3 scripts/workspace-gate-evidence.py run --profile workspace` - passed, 29 suites
**Discrimination sensor:** 10 of 10 mutants killed (2 survivors found and closed)
**Coverage:** 20 of 20 acceptance criteria, 5 of 5 edge cases

Verification ran as the standalone fresh-eyes pass from the skill's Sub-Agent Delegation section:
the session's operating instructions forbid dispatching an unrequested sub-agent, so the Verifier
role was executed inline against the committed diff surface.

---

## P1: Compare the same metrics across engines

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 `contract_version` is 4 | Integer 4 | `scripts/test-session-history-audit.py:408` - `assert report["contract_version"] == 4` | PASS |
| AC2 Identical metric key set | Both blocks sort equal | `:490` - `assert sorted(report["codex"]) == sorted(report["claude"])` | PASS |
| AC3 Unobservable metric is `null` | `None`, not `0` | `:496` - `assert block[key] is None, f"{engine}: {key} has a reason but reports {block[key]!r}"` | PASS |
| AC4 Every `null` carries a reason | Non-empty reason for that exact key | `:500` - `assert key in reasons, f"{engine}: {key} is null with no stated reason"` | PASS |
| AC5 No measured metric is listed unsupported | Reason keys are all `None` | `:496` (same assertion, evaluated over the reason map) | PASS |
| AC6 Fully measured engine emits an empty map | `{}` when nothing unsupported | `scripts/audit-session-history.py` `engine_block` always sets the key; `:617` asserts the exact expected sets per engine | PASS |

**Independent test:** the real corpus reports identical sorted keys, with Codex marking `sidechains`
unsupported and Claude marking `continuations` plus the four compaction metrics.

## P1: Measure Claude aborts and subagents

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 Sentinel text block counts one abort | Exact-string match only | `:503` - `assert report["claude"]["aborted_turns"] == 4` over a fixture with both sentinel spellings | PASS |
| AC2 Substring occurrence does not count | Decoy records ignored | `:503` - the fixture adds 2 decoy records quoting the sentinel plus a tool result echoing it; the total stays 4 | PASS |
| AC3 Derived abort statistics reported | Count, max, percentage | `:459-462` - `sessions_with_aborts: 2`, `max_aborts_per_session: 3`, `sessions_with_aborts_percent: 28.57` | PASS |
| AC4 `subagents/*.meta.json` counted | One per meta file | `:504` - `assert report["claude"]["subagents"] == 4`; the fixture also writes `notes.txt`, which is not counted | PASS |
| AC5 Missing `subagents` directory counts zero | No failure | `:598-607` - the empty-root block reports `subagents: 0` | PASS |
| AC6 Empty population yields 0.0, no division by zero | `0.0` | `:608` - `assert missing_report["claude"]["sessions_with_aborts_percent"] == 0.0` | PASS |
| AC7 Only accepted sessions counted | Sidechain excluded from the population | `:503` - the sidechain fixture carries 5 sentinel records that do not reach the total | PASS |

**Independent test:** against the real project directory the auditor reports 15 aborted turns across
11 sessions, a maximum of 3, and 23 subagents - the subagent total independently matching the 23
`Agent` tool calls counted in the same corpus.

## P2: Keep the rendered and receipt surfaces honest

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 `null` renders as `n/a` | Literal `n/a` | `:516-517` - `assert "compactions: n/a"`, `assert "continuations: n/a"` | PASS |
| AC2 Unsupported keys print with reasons | Key and reason both visible | `:518-519` - `assert "unsupported_metrics:"`, `assert "no compaction marker appears"` | PASS |
| AC3 Receipt carries the same keys and map | Receipt embeds the report | `:577` - `assert sorted(both[0]) == sorted(both[1])`; receipt suites 17-20 still pass | PASS |
| AC4 Receipt excludes paths and identifiers | No leak | `:326` and `:395` - `for sensitive in (SECRET, CWD, PRIMARY, ...): assert sensitive not in ...` | PASS |

---

## Edge Cases

| Edge case | `file:line` + assertion | Result |
| --- | --- | --- |
| Sentinel inside a tool result does not count | `:503` - decoy fixture includes a `tool_result` whose content is exactly a sentinel | PASS |
| `subagents` directory with no `.meta.json` | `:504` - `notes.txt` present, count stays 4 | PASS |
| Subagent files of a non-accepted session | `:682` - `subagent_only["sessions_with_aborts_percent"] == 0.0` over a subagent-only cohort | PASS |
| Absent history root still carries the full schema | `:598` - `assert sorted(missing_report["claude"]) == sorted(missing_report["codex"])` | PASS |
| A reason naming an absent key violates the contract | `:495` - `assert key in block, f"{engine}: {key} has a reason but is not a field"` | PASS |

---

## Discrimination Sensor

Mutants were injected into a disposable `git worktree`; the real tree was never modified and the
worktree was removed with `--force` afterwards.

| Mutant | Injected defect | Result |
| --- | --- | --- |
| P1 | Sentinel matched as substring instead of exact | KILLED |
| P2 | Aborts counted over sidechains too | KILLED |
| P3 | Claude `compactions` reported as `0` instead of `null` | KILLED |
| P4 | `unsupported_metrics` dropped from the block | KILLED |
| P5 | Subagents counted from any file, not `*.meta.json` | KILLED |
| P6 | Null metric rendered as `None` instead of `n/a` | KILLED |
| P7 | `engine_block` accepts a metric both unsupported and measured | **SURVIVED**, then killed |
| P7b | `engine_block` accepts a metric outside the canonical key set | **SURVIVED**, then killed |
| P8 | Percentage divides by zero with no guard | KILLED (see Findings 2) |
| P9 | `contract_version` reverted to 3 | KILLED |

**10 of 10 killed after the fix.** P7 and P7b survived the first pass: `engine_block`'s guards are
the single point where the two engines could silently diverge, and no data path exercised them. A
test that drives the builder directly was added at `:557-577`; both mutants now die.

---

## Test Integrity

| Suite | Before | After | Delta |
| --- | --- | --- | --- |
| `scripts/test-session-history-audit.py` | 20 | 20 named cases plus one builder-guard case | assertions added, none removed |
| Aggregate `scripts/test-workspace.sh` | 29 suites | 29 suites | unchanged, all passing |

No assertion was weakened and no test was deleted or skipped.

---

## Findings

1. **The engines were also asymmetric in naming, not only in coverage.** Codex emitted
   `logical_work_streams` while Claude emitted `logical_sessions` for the same concept, so a
   field-by-field comparison was impossible even where both measured. The canonical key set
   collapses them to `logical_work_streams`; `logical_sessions` no longer exists, which breaks any
   consumer reading it by name.

2. **One mutant in the first pass was equivalent, not a survivor.** Replacing the empty-population
   guard with `count / max(len(primary), 1)` yields the same `0.0`, so the suite was right to pass.
   Re-injected as an unguarded `count / len(primary)`, it raises `ZeroDivisionError` and dies. The
   distinction is recorded so a future reader does not mistake the first result for weak coverage.

3. **Claude is interrupted more often than Codex, and this is newly measurable.** Over the same
   window the corpus shows 40.74% of Claude sessions with at least one aborted turn against 27.66%
   for Codex. The figure is now comparable because both engines derive it over primary sessions.
   Compaction remains uncomparable by construction and is reported as such rather than as zero.
