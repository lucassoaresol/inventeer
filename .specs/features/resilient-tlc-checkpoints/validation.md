# Resilient TLC Checkpoints Validation

**Date:** 2026-08-02
**Spec:** `.specs/features/resilient-tlc-checkpoints/spec.md`
**Behavioral diff range:** `ac22200..a054ffa`
**Verifier:** standalone fresh-eyes fallback, without sub-agents per user request

## Delivery Evidence

- **Validation state:** pass
- **Evidence binding:** specification `1928db9`, helper and functional tests `56b9c21`, AD-036 and
  integration contract `c5681a4`, fresh-eyes edge correction `a054ffa`
- **Requirement contract:** user-approved 2026-08-02 local per-machine checkpoint scope, AD-027,
  AD-031, AD-032, and AD-036
- **Gate state:** green; 106 passed, 0 failed, 0 skipped; 6/6 focused mutants killed; range diff
  integrity clean
- **Pending delivery conditions:** none
- **High-risk paths:** atomic replacement and section-scoped state preservation in
  `scripts/update-tlc-checkpoint.py`

## Task Completion

| Task | Status | Evidence |
| --- | --- | --- |
| Define the approved checkpoint contract | Done | `1928db9` |
| Implement the deterministic writer and functional tests | Done | `56b9c21` |
| Record AD-036, instructions, documentation, and contract tests | Done | `c5681a4` |
| Close fresh-eyes recovery-edge coverage | Done | `a054ffa` |

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| Recover-1 | Exact issue-local Portal TLC target | `scripts/test-tlc-checkpoint.py:75-76,103-106` — target and complete file equality | PASS |
| Recover-2 | New UTF-8 file has title, Decisions, and one Handoff | `scripts/test-tlc-checkpoint.py:105-107` — exact full-text equality | PASS |
| Recover-3 | Eleven ordered handoff fields | `scripts/test-tlc-checkpoint.py:79-92,105-107` — exact schema embedded in full-text equality | PASS |
| Recover-4 | Bytes outside Handoff remain exact | `scripts/test-tlc-checkpoint.py:119-123` — exact expected prefix and following section | PASS |
| Recover-5 | Identical input emits `unchanged` and preserves bytes/inode | `scripts/test-tlc-checkpoint.py:127-131` — stdout, bytes, and inode equality | PASS |
| Recover-6 | Changed input uses same-directory temp, fsync, atomic replace, and emits `updated` | `scripts/test-tlc-checkpoint.py:101-102,141-155` — exact stdout, paths, and `['fsync', 'replace']` order | PASS |
| Recover-7 | Replace failure preserves prior state and leaves no temp | `scripts/test-tlc-checkpoint.py:154-158` — return code, bytes, and empty temp glob | PASS |
| Boundary-1 | Invalid INV identifier creates no state | `scripts/test-tlc-checkpoint.py:160-164` — non-zero and absent `session-context` | PASS |
| Boundary-2 | Empty or multiline input preserves prior state | `scripts/test-tlc-checkpoint.py:166-170` — non-zero and byte equality for both inputs | PASS |
| Boundary-3 | Resolved path cannot escape workspace | `scripts/test-tlc-checkpoint.py:177-184` — non-zero and no outside `portal` directory | PASS |
| Boundary-4 | Event and validation enums reject unknown values | `scripts/test-tlc-checkpoint.py:172-175` — non-zero and unchanged bytes | PASS |
| Boundary-5 | Uncommitted values are relative paths and persisted metadata is sanitized | `scripts/test-tlc-checkpoint.py:198-201`; `scripts/test-tlc-checkpoint-contract.sh:59-63` | PASS |
| Trigger-1 | All five successful transitions require a checkpoint | `scripts/test-tlc-checkpoint-contract.sh:24-42` — exact trigger loops and success phrase | PASS |
| Trigger-2 | Failed transitions cannot advance state | `scripts/test-tlc-checkpoint-contract.sh:28-31` — explicit failure prohibition | PASS |
| Trigger-3 | Ignored local lifecycle and AD-031 cleanup timing | `scripts/test-tlc-checkpoint-contract.sh:44-57,74-78` — exact lifecycle, cleanup, and Git assertions | PASS |
| Trigger-4 | AD-036 is active; AD-031, AD-032, and vendored TLC remain intact | `scripts/test-tlc-checkpoint-contract.sh:18-22,65-72` | PASS |

**Status:** all 16 acceptance criteria match precise spec-defined outcomes.

## Edge Cases

| Edge case | Evidence | Result |
| --- | --- | --- |
| Zero or multiple Handoff sections | `scripts/test-tlc-checkpoint.py:186-196` preserves each malformed input | PASS |
| Empty repeatable values render `none` | `scripts/test-tlc-checkpoint.py:203-215` asserts all three fields | PASS |
| Stale process requires liveness check | `scripts/test-tlc-checkpoint-contract.sh:53-54` | PASS |
| Work after the last event remains a residual loss window | `scripts/test-tlc-checkpoint-contract.sh:51-52` | PASS |
| Execution remains single-writer per issue and machine | `scripts/test-tlc-checkpoint-contract.sh:55-56` | PASS |

## Test Adequacy

The functional suite compares complete output where representation matters and asserts negative
effects for every failure boundary. It distinguishes write, no-op, and failed-write states using
stdout, bytes, inode, call ordering, target paths, and temporary residue. The integration suite
asserts every authority surface, trigger, lifecycle property, privacy boundary, and Git exclusion.
Every test maps to an AC or named edge case; none tests a framework behavior or unclaimed feature.

The first fresh-eyes pass found that liveness revalidation, the residual loss window, and the
single-writer boundary were documented but not asserted. Commit `a054ffa` added exact contract
assertions, after which the complete gate and three focused documentation mutations passed. This
recurrence is already described by confirmed lesson L-008, so no duplicate lesson was added; L-008
was penalized once because its loaded guidance did not prevent the initial gap.

## Discrimination Sensor

| Mutation | Scratch behavior fault | Result |
| --- | --- | --- |
| 1 | Removed `fsync` before replacement | KILLED by exact atomic event order |
| 2 | Disabled identical-content no-op | KILLED by stdout and inode assertions |
| 3 | Allowed `INV-0` | KILLED by invalid-issue effect assertions |
| 4 | Removed liveness requirement | KILLED by recovery lifecycle contract |
| 5 | Removed residual-window disclosure | KILLED by recovery lifecycle contract |
| 6 | Changed `single-writer` to `multi-writer` | KILLED by AD-036 boundary contract |

**Sensor depth:** two lightweight passes: three helper mutations and three correction-specific
contract mutations
**Result:** 6/6 killed — PASS. Both scratch roots were removed; the real worktree was never mutated.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum, requirement-bounded implementation | PASS |
| Atomic and section-scoped state changes | PASS |
| No arbitrary output path or cross-machine claim | PASS |
| No product repository or vendored TLC change | PASS |
| Exact, non-shallow, spec-anchored tests | PASS |
| Workspace guidelines and TLC coding principles followed | PASS |

## Gate Check

- Complete serial workspace suite: 106 passed, 0 failed, 0 skipped
- Previous suite: 88; delta: +18 checkpoint tests, no deletion or weakening
- Checkpoint functional suite: 11 passed
- Checkpoint integration contract: 7 passed
- Discrimination sensor: 6 killed, 0 survived across two passes
- `git diff --check ac22200..a054ffa`: exit 0
- Changed surface contains seven workspace files; no `repos/`, `session-context/`, or
  `.agents/skills/tlc-spec-driven/` file changed
- Resource snapshot: 2 CPUs, about 2.8 GB memory available, no swap, about 44 GB disk available;
  gate executed serially
- Interactive UAT: not applicable to this infrastructure-only feature

## Requirement Traceability Update

| Requirement | Previous | New |
| --- | --- | --- |
| RTCP-01 through RTCP-10 | Pending | Verified |

## Summary

**Overall:** ready

Portal + Codex + TLC now has a deterministic, issue-local checkpoint writer that persists the last
successful transition without dirtying Git or product repositories. It preserves state outside the
handoff, fails without losing the previous checkpoint, rejects unsafe requests, and is required at
the five approved stable transitions. The remaining limitation is explicit: checkpoints are local
per machine and can only bound, not eliminate, work lost after their last successful event.
