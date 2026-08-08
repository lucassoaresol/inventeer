# TLC Spec-Driven 3.3.0 Upgrade Validation

**Date:** 2026-08-08

**Functional range:** `afe790f..2036882`

**Validation status:** PASS

**Overall:** PASS

## Verification Contract

This is a standalone fresh-eyes verification of the complete functional range. The TLC normally
requires author and verifier to be different agents, but the user explicitly prohibited subagents;
the same agent therefore performed a separate spec-anchored pass after implementation, without
relying on task completion claims. The later evidence-only commit does not alter the functional head
under test.

## Requirement Outcomes

| Requirement | Outcome | Evidence |
| --- | --- | --- |
| TLC330-01 | PASS — the manifest pins upstream 3.3.0 and the exact release commit. | `.agents/vendor.json:7` |
| TLC330-02 | PASS — the manifest enumerates six retained customizations and the focused suite asserts their content anchors. | `scripts/test-tlc-deterministic-gates.py:208` |
| TLC330-03 | PASS — manifest, skill metadata, and README version are asserted together. | `scripts/test-tlc-deterministic-gates.py:238` |
| TLC330-04 | PASS — both Markdown colon forms and wrapped criteria have positive fixtures; missing SHALL remains negative. | `scripts/test-tlc-deterministic-gates.py:123` |
| TLC330-05 | PASS — explicit overall PASS and FAIL outrank conflicting subordinate sensor results. | `scripts/test-tlc-deterministic-gates.py:163` |
| TLC330-06 | PASS — PASS without `file:line` evidence fails closed. | `scripts/test-tlc-deterministic-gates.py:173` |
| TLC330-07 | PASS — matching task dependencies pass and Mermaid/field disagreement fails. | `scripts/test-tlc-deterministic-gates.py:186` |
| TLC330-08 | PASS — a supported Conventional Commit passes and malformed input fails. | `scripts/test-tlc-deterministic-gates.py:197` |
| TLC330-09 | PASS — the root gate executes the behavioral harness covering all four validators. | `scripts/test-workspace.sh:32` |
| TLC330-10 | PASS — AD-040 makes adoption prospective and the root test rejects a historical sweep. | `scripts/test-tlc-deterministic-gates.py:248` |
| TLC330-11 | PASS — spec, tasks, commit, and state transitions are all named and asserted. | `scripts/test-tlc-deterministic-gates.py:259` |
| TLC330-12 | PASS — five representative mutations were killed in disposable copies and the real worktree fingerprint was unchanged. | `.specs/features/tlc-spec-driven-3-3-upgrade/validation.md:53` |

## Gate Evidence

| Gate | Result |
| --- | --- |
| Focused deterministic harness | PASS — 16 tests, no failures or skips. |
| Root workspace gate | PASS — 19 suites, no failures; baseline was 16 suites, for a net addition of 3 suites. |
| Spec closure gate | PASS — 0 errors and 0 warnings. |
| Task plan gate | PASS — 0 errors and 0 warnings. |
| Skill structural validation | PASS. |
| Range integrity | PASS — `git diff --check afe790f..2036882`. |
| Repository state after functional validation | PASS — clean worktree. |

## Discrimination Sensor

The sensor copied only the relevant validators, focused harness, and contract files into a temporary
directory for each mutation. Each copy ran the same focused suite and was removed afterward.

| Mutation | Expected discrimination | Result |
| --- | --- | --- |
| M1: regress acceptance-heading colon recognition | Spec fixtures fail | KILLED |
| M2: let subordinate state results control the verdict | State fixtures fail | KILLED |
| M3: regress dependency-field parsing | Task fixtures fail | KILLED |
| M4: remove a retained local-extension contract | Workspace adoption fixture fails | KILLED |
| M5: remove a required transition-gate policy | Transition policy fixture fails | KILLED |

**Sensor result:** PASS — 5/5 mutants killed.

**Real-tree result:** PASS — fingerprint unchanged after disposable-copy execution.

## Fresh-Eyes Findings

The first standalone review found that TLC330-02 lacked a persistent retained-extension assertion and
that TLC330-11 did not assert all four transition gates. VF1 added both contracts in functional commit
`2036882`; the complete focused and root gates then passed. No unresolved requirement, surviving
mutant, regression, or evidence gap remains.

## Delivery Verdict

The functional range satisfies all 12 acceptance criteria and is ready for local use. The final
documentation commit records this report, closes T5, and updates handoff state; it contains no
functional change. No push, pull request, deployment, or product-repository mutation is part of this
delivery.

**Overall:** PASS
