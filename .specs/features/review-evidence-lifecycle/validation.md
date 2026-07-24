# Review Evidence Lifecycle Validation

**Date:** 2026-07-24
**Spec:** `.specs/features/review-evidence-lifecycle/spec.md`
**Diff range:** `4b18e5a..afb1fe3`
**Evidence head:** `afb1fe322e876b091c398b031c9b9d4ac274ebbd`
**Verifier:** independent TLC sub-agent (author != verifier)

## Verdict

**FAIL.** The deterministic Build gate is green and all three discrimination mutants were killed,
but three requirements are not satisfied: an adjacent checksum can verify a different file while the
parent is recorded as verified (REL-12/REL-14), and `sub-agents.md` still permits stash-based sensor
mutation (REL-19).

## Delivery Evidence

- **Validation state:** `fail`
- **Evidence binding:** committed range `4b18e5a..afb1fe3`; work SHA
  `afb1fe322e876b091c398b031c9b9d4ac274ebbd`; source worktree clean before and after verification
- **Requirement contract:** approved `spec.md`, `design.md`, and `tasks.md` at `afb1fe3`
- **Gate state:** green — 29/29 behavior tests, ShellCheck, three skill validators, and
  `git diff --check 4b18e5a..afb1fe3`
- **Pending delivery conditions:** correct F1 and F2 below, add regressions, commit the correction and
  rerun an independent verifier over the new final range
- **High-risk paths:** adjacent parent-checksum binding and TLC sensor-isolation instructions
- **Promotion readiness:** no

## Task Completion

| Task | Status | Evidence |
| --- | --- | --- |
| T1 | PASS | `f32e75c`; approved spec/design/tasks present |
| T2 | PASS | `2b2f94f`; inspector 14/14, ShellCheck and validator green |
| T3 | FAIL | Ordinary lineage cases pass, but adversarial adjacent-checksum binding violates REL-12/14 |
| T4 | FAIL | New `validate.md` is correct, but linked `sub-agents.md` retains forbidden stash guidance |
| T5 | PASS | AD-023 and workspace handoff are present |
| T6 | FAIL | Independent verification found F1 and F2 |

## Spec-Anchored Acceptance Criteria

For policy-only criteria, the assertion expression below is the independent verifier's exact contract
comparison. Executable criteria cite the assertion that ran.

| Requirement | Spec-defined outcome | `file:line` + assertion expression | Result |
| --- | --- | --- | --- |
| REL-01 | Separate implementation and validation state sets | `continuity-policy.md:43-57` — `implementation == {working-tree, committed, pushed, pr-observed} && validation == {missing, pass, fail, stale, pending-delivery}` | PASS |
| REL-02 | Any bound SHA/diff/contract/gate change makes PASS stale | `continuity-policy.md:53-57` — `changed(bound_input) => validation == stale` | PASS |
| REL-03 | A delivery-only remainder produces pending-delivery and blocks reviewable | `continuity-policy.md:56-57,258-259` — `pass && delivery_guard => pending-delivery && !reviewable` | PASS |
| REL-04 | Review correction recomputes affected boundaries/surfaces/gates/validation | `continuity-policy.md:224-230` — `changed(review_head_or_dirty_surface) => stale(validation) && reassess(review_commits,surface,gates,head,base)` | PASS |
| REL-05 | Scope has all five typed collections | `continuity-policy.md:161-167` — `surface_fields == {exact,families,renames,generated,forbidden}` | PASS |
| REL-06 | Expected mechanical rename is not scope creep by count alone | `continuity-policy.md:169-170` — `expected_rename && many_files => file_count_is_informational` | PASS |
| REL-07 | Schema v2 emits merge-base-relative commits | `test-inspect-git-front.sh:93,100-102` — `grep schema_version\\t2` and `[[ "$review_commits" == "$expected_review_commits" ]]` | PASS |
| REL-08 | Rename/copy entries include status, source and target | `test-inspect-git-front.sh:103-105` — `grep R100 | grep rename-source.txt | grep rename-target.txt` | PASS |
| REL-09 | Dirty paths are split and inspection is read-only | `test-inspect-git-front.sh:113-115,154-156` — exact `grep` per class and `[[ "$fingerprint_before" == "$fingerprint_after" ]]` | PASS |
| REL-10 | Same refs/worktree/timestamp are byte-identical | `test-inspect-git-front.sh:126-133` — `[[ "$output" == "$second_output" ]]` | PASS |
| REL-11 | No-parent bundle records stage and explicit absence | `test-create-review-bundle.sh:51-53` — exact `grep` for `review_stage initial` and `parent_status none` | PASS |
| REL-12 | Child records the supplied parent's computed hash and truthful adjacent-checksum status | `test-create-review-bundle.sh:72-75` passes the ordinary case, but `create-review-bundle.sh:163-168` runs the sidecar's named target; adversarial probe assertion `[[ child_exit -ne 0 ]]` observed `child_exit=0`, child created, `parent_checksum_status=verified` | FAIL |
| REL-13 | Manifest union is classified added/removed/retained | `test-create-review-bundle.sh:76-79` — exact `grep` for retained, added and removed rows | PASS |
| REL-14 | Invalid parent/checksum fails with no child ZIP or source mutation | `test-create-review-bundle.sh:95-118` covers mismatch and duplicate manifest, but the wrong-target sidecar probe at `create-review-bundle.sh:163-168` observed success and a child ZIP; expected `exit != 0 && child_created == no` | FAIL |
| REL-15 | Lineage never claims freshness, validation or approval | `create-review-bundle/SKILL.md:62-64` — `lineage_role == historical_review_evidence_only` | PASS |
| REL-16 | Compatibility rubric names every required representation concern | `specify.md:11-15` — `dimensions` includes wire format, persistence, migration/backfill, rollout compatibility, exact encoding/precision and safe disclosure | PASS |
| REL-17 | Broad mechanical atomicity follows one reversible invariant, not file count | `tasks.md:29-39` — `atomic == one_reversible_semantic_deliverable` | PASS |
| REL-18 | Resource constraints require complete deterministic shards and aggregation | `tasks.md:74-79,117-127` — `resource_recipe => all_shards && aggregate_counts && !weaken_coverage` | PASS |
| REL-19 | Sensors permit only disposable worktrees/copies and forbid stash | `validate.md:84-93` is compliant, but `sub-agents.md:100-106` says scratch state may be `git stash or temp copy`; assertion `rg -n "git stash" TLC sensor guidance` expected no permissive match and found one at line 102 | FAIL |
| REL-20 | Validation closes with exact evidence/range, gates, pending conditions and risks | `validate.md:181-190,202-209` — report and compact-summary contracts require every field | PASS |
| REL-21 | Confirmed grounded review finding is accepted; empty grounding rejected | `test-lessons.py:29-49,51-64` — `lesson["signal"] == "review_finding"`, exact feature/evidence values, then `expect=2` and unchanged count for empty source | PASS |

**Status:** 18/21 requirements fully matched; no spec-precision gaps. REL-12, REL-14 and REL-19 fail
precise outcomes.

## Edge Cases

- PASS — uncommitted validation remains `working-tree`/promotion-blocking in policy.
- PASS — missing adjacent checksum records `missing` and continues (`test-create-review-bundle.sh:83-93`).
- FAIL — an adjacent sidecar that validly checks a different file is accepted as verification of the
  supplied parent (`create-review-bundle.sh:163-168`).
- PASS — diverged rename retains the three-dot surface (`test-inspect-git-front.sh:96-105,157`).
- PASS — resource-aware gating requires complete deterministic shards (`tasks.md:74-79`).

## Gate Check

- **Behavior commands:**
  - `bash .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh` — 14 passed
  - `bash .agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh` — 13 passed
  - `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` — 2 passed
- **ShellCheck:** production scripts and both Bash harnesses — passed, zero findings
- **Skill validators:** `quick_validate.py` for `advance-delivery-front`, `create-review-bundle`, and
  `tlc-spec-driven` — 3/3 valid
- **Diff integrity:** `git diff --check 4b18e5a..afb1fe3` — passed
- **Result:** 29 passed, 0 failed, 0 skipped in the declared behavior suite; all static gates green
- **Test integrity:** baseline `4b18e5a` rerun produced 12 inspector + 8 bundle tests and no focused
  lessons probe; evidence head produced 14 + 13 + 2 = 29, delta +9. No deletion, skip, or weakened
  assertion was found in the feature diff.
- **Unclaimed tests:** none; legacy cases map to retained safety/done-when behavior, and the nine added
  cases map to REL-07..14 and REL-21.

## Discrimination Sensor

All mutations ran in three separate `git archive afb1fe3` exports under `/tmp`; the real worktree was
never edited, stashed, or restored.

| Mutation | File:line | Fault and expected assertion | Result |
| --- | --- | --- | --- |
| M1 | `inspect-git-front.sh:144` | Change three-dot changed-path range to two-dot; exact review-surface equality at `test-inspect-git-front.sh:96-97` must fail | KILLED, harness exit 1 |
| M2 | `create-review-bundle.sh:163-168` | Continue after an actual parent checksum mismatch; fail-closed assertion at `test-create-review-bundle.sh:99-105` must fail | KILLED, harness exit 1 |
| M3 | `lessons.py:38-45` | Remove `review_finding` from accepted signals; grounded-add probe at `test-lessons.py:29-49` must fail | KILLED, probe exit 1 |

**Sensor depth:** lightweight. **Result:** 3/3 killed, 0 survived. This does not erase the separate
wrong-target checksum edge failure discovered by forward testing.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum/surgical scope; no unrelated feature | PASS |
| Existing patterns and read-only product-repo boundaries | PASS |
| Test assertions map to specified values/states | FAIL — no assertion binds an adjacent checksum entry to the supplied parent basename/hash |
| Per-layer coverage and listed edge cases | FAIL — invalid-checksum coverage misses the wrong-target sidecar case |
| Cross-reference consistency | FAIL — `sub-agents.md:102` contradicts REL-19 and `validate.md:88-93` |
| Documented guidance followed | PASS — `AGENTS.md`, TLC validate/coding principles, and feature tasks were applied |
| Senior-engineer approval | FAIL until F1/F2 are corrected |

All 21 paths in `4b18e5a..afb1fe3` were reviewed. No product repository, Linear state, GitHub state,
or implementation/test file was modified by this verifier.

## Fix Plans

### F1 — Bind the adjacent checksum to the supplied parent bundle

- **Severity:** Major
- **Requirements:** REL-12, REL-14
- **Root cause:** `create-review-bundle.sh:163-168` delegates to `sha256sum -c` and accepts success for
  whatever filename the sidecar names; it never proves that the checked entry is the supplied parent.
- **Fix task:** parse/validate the adjacent checksum contract and require its expected hash/target to
  bind exactly to the supplied parent (or directly compare its declared digest with the already
  computed `parent_sha256`); reject malformed, ambiguous, or wrong-target sidecars before creating the
  child. Add the reproduced decoy-target case to the bundle harness and retain source fingerprint/no
  child assertions.
- **Done when:** correct parent sidecar is `verified`; missing remains `missing`; wrong hash, malformed,
  ambiguous, and wrong-target sidecars all exit non-zero without source mutation or child ZIP.

### F2 — Remove stash permission from every TLC verifier entry point

- **Severity:** Major
- **Requirement:** REL-19
- **Root cause:** the feature corrected `validate.md` but did not update the linked verifier summary in
  `sub-agents.md:102`.
- **Fix task:** replace stash guidance with disposable worktree/copy wording consistent with
  `validate.md:88-93`; add a focused static regression that rejects permissive stash-based sensor
  guidance across the TLC verifier references.
- **Done when:** all verifier entry points allow only disposable worktrees/copies, the focused static
  regression and TLC validator pass, and no permissive `git stash` sensor instruction remains.

## Lessons Handoff

This validation contains grounded `ac_gap`/forward-test failure signals for F1 and F2. Per the
orchestrator's explicit scope, the verifier did not modify `.specs/lessons.json`, `.specs/LESSONS.md`,
or TLC lesson files; lesson distillation must be handled by the orchestrator after accepting the
findings.

## Summary

**Overall:** FAIL — not promotion-ready. **Spec check:** 18/21. **Gate:** 29/29 plus all static gates.
**Sensor:** 3/3 killed. **Next step:** route F1 and F2 to an implementer, then independently reverify
the corrective evidence range.
