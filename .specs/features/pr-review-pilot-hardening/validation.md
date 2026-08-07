# PR Review Pilot Hardening Validation

**Date:** 2026-08-07
**Spec:** `.specs/features/pr-review-pilot-hardening/spec.md`
**Evidence base:** functional commit `46ebfd9a24bd5ede15b4ff60df4754f49bec66fb`
**Verifier:** standalone fresh-eyes fallback; no sub-agent per user constraint

## Verdict

**Delivered behavioral PASS.** All eight requirements match their specified outcomes, the complete
workspace gate is green, and four disposable-copy mutants were killed. The implementation is bound
to an attributable functional commit. Transversal promotion remains intentionally deferred until
the prospective 5–10-review pilot produces real outcome evidence.

## Delivery Evidence

- **Validation state:** `delivered`
- **Evidence binding:** functional commit `46ebfd9a24bd5ede15b4ff60df4754f49bec66fb`;
  behavior-bearing hashes are listed below
- **Requirement contract:** verified `spec.md`, AD-038, and AD-039 as observed on 2026-08-07
- **Gate state:** green on the clean functional commit — `bash scripts/test-workspace.sh`, 18 suites,
  133 explicit harness checks, 36 skill-folder validations, Shell syntax, and `git diff --check`
- **Delivery boundary:** committed locally; pushing or opening a PR was not requested
- **High-risk paths:** closed-schema/path-boundary enforcement and append-only JSONL in
  `scripts/pr-review-pilot.py`; stale base/head identity and outcome aggregation in the same helper
- **External smoke evidence:** GitHub MCP loaded with `GITHUB_PAT_TOKEN` and read the private root
  repository README successfully; no GitHub mutation was attempted

### Behavior-bearing file hashes

| File | SHA-256 |
| --- | --- |
| `.specs/features/pr-review-pilot-hardening/spec.md` | `d3b8b5aa85d6d58ce9c55d8bb08f8db048706705bc7e5849b5e639c169b11559` |
| `.agents/skills/review-pull-request/SKILL.md` | `ecc3f50a31e65e2fe37bef0d791bd35ee8ab4b431843acea40ba5382bd5b254e` |
| `.agents/skills/review-pull-request/references/review-contract.md` | `00842bfbd418d165de0ec5f2cbf9715db42e16feabd240d3a9bf9bdee6d7f482` |
| `scripts/pr-review-pilot.py` | `0b84b8b6256134280ca8c01384f1dd227256cbf5be1aa51d6acb303b98eaf906` |
| `scripts/test-pr-review-pilot.py` | `c52b4f296129a6c0000736e50326e89465d54c5aadfc5e58becf70294e6c2817` |
| `scripts/test-pr-review-workflow.py` | `e42fd51dffd89a597177e248b935fd959f24667928b79d81a43532732db3ec82` |
| `scripts/test-workspace.sh` | `28eff254d172a9c2348dcfc0deefba2688005a5d92705a5937c225dfc1ad32c9` |
| `scripts/test-workspace-structure.py` | `376da3492b906c22af947f92215da10107dc7b8f006d11bde4153b12ea4bea48` |

## Task Completion

| Task | Status | Evidence |
| --- | --- | --- |
| Contract hardening | PASS | Base/head freshness, deterministic verdicts, Linear snapshot and token contracts |
| Sanitized pilot ledger | PASS | Closed schema, append-only canonical JSONL, comparable aggregates |
| Unified root gate | PASS | All maintained harnesses and structural checks run through one command |
| Standalone validation | PASS | 8/8 requirements, 18 suites, 4/4 killed mutants |

## Spec-Anchored Acceptance Criteria

| Requirement | Spec-defined outcome | Evidence | Result |
| --- | --- | --- | --- |
| PRH-01 | Either final SHA change makes the verdict stale | `scripts/test-pr-review-pilot.py:58-76` — `assertRaisesRegex(..., "verdict must be stale")` and exact `stale` assertions | PASS |
| PRH-02 | Unresolved P0–P2 findings block unless already accepted by contract | `scripts/test-pr-review-pilot.py:78-85` — unresolved P2 rejects non-block and accepts `block`; contract defines the accepted-risk exception | PASS |
| PRH-03 | Valid records append as one canonical JSON line below the pilot root | `scripts/test-pr-review-pilot.py:94-104` — two records, two lines, stable first line and one ledger path | PASS |
| PRH-04 | Unknown/sensitive fields and path escapes fail closed | `scripts/test-pr-review-pilot.py:87-92,158-172` — comment/diff/token and direct/symlink escapes raise | PASS |
| PRH-05 | Metrics use comparable states and null zero denominators | `scripts/test-pr-review-pilot.py:106-156` — exact rates, check states, evidence source, stale cause, expansion reasons, and `None` rates | PASS |
| PRH-06 | Reused Linear snapshots require retrieval time and `updatedAt`; changed inputs refresh | `.agents/skills/advance-delivery-front/SKILL.md:28-35` plus workflow contract checks | PASS |
| PRH-07 | One root command runs every maintained gate without reduced coverage | `scripts/test-workspace.sh:18-56` — 15 harnesses plus skill, Shell and diff-integrity suites | PASS |
| PRH-08 | Dedicated least-privilege token is default; `gh` reuse is scoped fallback | `README.md:235-247`, MCP config tests, and successful read-only GitHub MCP smoke query | PASS |

**Status:** 8/8 requirements match precise outcomes; zero gaps and zero spec-precision gaps.

## Gate Check

- **Final resource preflight:** 2026-08-07T16:20:00Z; 2 CPUs, load 1m `0.62`, 3,397,746,688
  bytes available memory, no swap, 45,390,438,400 bytes free; sequential concurrency 1 selected
- **Command:** `bash scripts/test-workspace.sh`
- **Result:** 18 suites passed; 133 explicit checks passed; 0 failed; 0 skipped
- **Structural results:** 36/36 skill folders valid, 12 Python files parsed, 65 relative Markdown
  links resolved, 8/8 Claude symlinks matched, all Shell files passed `bash -n`
- **Diff integrity:** `git diff --check` passed
- **Test integrity:** no existing test was deleted, skipped, or weakened; this feature adds 11 ledger
  behavior tests, one stronger workflow assertion group, and three workspace-structure checks

## Discrimination Sensor

All mutations ran in four independent `/tmp/pr-review-final-*` copies. The real worktree was never
edited or stashed, and all temporary copies were deleted afterward.

| Mutation | Fault | Covering evidence | Result |
| --- | --- | --- | --- |
| M1 | Ignore base-SHA changes when computing stale identity | Base-change and stale-summary tests | KILLED — suite exit 1 |
| M2 | Accept unknown fields instead of enforcing the closed schema | comment/diff/token rejection test | KILLED — suite exit 1 |
| M3 | Emit numeric zero when no decided finding denominator exists | null-rate test | KILLED — suite exit 1 |
| M4 | Count every GitHub review source as `threads` | `approval-only` aggregation test | KILLED — suite exit 1 |

**Sensor depth:** focused lightweight-plus, four behavior mutations. **Result:** 4/4 killed.

## Code Quality

| Check | Result |
| --- | --- |
| No functionality beyond the approved audit recommendations | PASS |
| Product repositories and external systems remained read-only | PASS |
| Closed schema excludes review prose and sensitive payloads by construction | PASS |
| Tests map to every acceptance criterion and assert exact outcomes | PASS |
| Unified runner reuses maintained harnesses rather than duplicating their logic | PASS |
| Workspace conventions, skill structure, Claude parity and Markdown links | PASS |

## Lessons Handoff

This is a clean behavioral PASS: no failed criterion, surviving mutant, spec-precision gap,
`SPEC_DEVIATION`, or new independently confirmed product finding. No TLC lesson is recorded.

## Summary

**Overall:** delivered behavioral PASS. **Spec check:** 8/8. **Gate:** 18/18 suites, 133 explicit
checks. **Sensor:** 4/4 killed. **Next:** collect the 5–10 real reviews through normal use and then
assess transversal promotion from the sanitized aggregate.
