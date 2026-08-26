# Bounded Workspace Context Validation

**Verdict:** PASS
**Date:** 2026-08-26
**Spec:** `.specs/features/bounded-workspace-context/spec.md`
**Diff range:** `747499280ed4588a8b28f9fbd4d588016fbf2da0..6c58e73fa55a743b46f30ef761ec88212d2d027f`
**Verifier:** independent sub-agent (author != verifier)

## Delivery Evidence

- **Validation state:** `pass`
- **Evidence binding:** base `747499280ed4588a8b28f9fbd4d588016fbf2da0`, work SHA `6c58e73fa55a743b46f30ef761ec88212d2d027f`
- **Requirement contract:** approved acceptance criteria in `spec.md` at work SHA `6c58e73fa55a743b46f30ef761ec88212d2d027f`; lifecycle closure is evidence-only
- **Gate state:** green; focal, structure, diff-integrity, root workspace, and discrimination gates passed
- **Pending delivery conditions:** none; the unpublished closure commit contains only lifecycle and validation evidence
- **High-risk paths:** none after direct selected-route and adjacent-heading verification

## Task Completion

| Task | Status | Notes |
| --- | --- | --- |
| T1 | Done | Manifest schema and hostile-schema coverage pass. |
| T2 | Done | Selection, measurement, privacy, and exit contracts pass. |
| T3 | Done | Adoption files, indexes, documentation, and root gate pass. |
| T4 | Done | The two initial verifier gaps now have direct behavior assertions and discriminating tests. |

## Spec-Anchored Acceptance Criteria

| Requirement | Spec-defined outcome | Evidence and assertion | Result |
| --- | --- | --- | --- |
| BWC-01 | A plan emits ordered metadata, budget, and estimator without source content. | `scripts/test-workspace-context.py:87` iterates the exact route order; `scripts/test-workspace-context.py:90` asserts exit 0; `scripts/test-workspace-context.py:93` asserts the exact output keys; `scripts/test-workspace-context.py:98` asserts selected content is absent. | PASS |
| BWC-02 | A measurement emits exact per-source and total code-point counts, rounded-up estimates, and pass status. | `scripts/test-workspace-context.py:150` invokes `measure`; `scripts/test-workspace-context.py:153` asserts exact characters; `scripts/test-workspace-context.py:154` asserts rounded totals; `scripts/test-workspace-context.py:155` asserts exact source contributions; `scripts/test-workspace-context.py:169` asserts pass status. | PASS |
| BWC-03 | Checking all supported routes reports five passes and exits 0. | `scripts/test-workspace-context.py:102` invokes `check`; `scripts/test-workspace-context.py:103` asserts exit 0; `scripts/test-workspace-context.py:106` asserts all five routes in order; `scripts/test-workspace-context.py:107` asserts every status is pass. | PASS |
| BWC-04 | An oversized selected route emits bounded contributions, fail status, and exits 1. | `scripts/test-workspace-context.py:196` invokes oversized selected `measure`; `scripts/test-workspace-context.py:199` asserts exit 1; `scripts/test-workspace-context.py:201` asserts fail status; `scripts/test-workspace-context.py:202` and `scripts/test-workspace-context.py:203` assert exact estimate and adjacent budget; `scripts/test-workspace-context.py:204` through `scripts/test-workspace-context.py:206` assert no disclosure, no physical path, and no mutation. | PASS |
| BWC-05 | Invalid heading selection exits 2 without source disclosure. | `scripts/test-workspace-context.py:285` through `scripts/test-workspace-context.py:297` build malformed, repeated, and non-Markdown cases; `scripts/test-workspace-context.py:306` asserts exit 2; `scripts/test-workspace-context.py:313` through `scripts/test-workspace-context.py:331` assert absent and duplicated document headings fail without fixture content. | PASS |
| BWC-06 | Invalid schema/path/source/order exits 2 without mutation. | `scripts/test-workspace-context.py:240` through `scripts/test-workspace-context.py:283` enumerate unknown fields, estimator, budget, order, duplicate, unsafe, and missing-source cases; `scripts/test-workspace-context.py:307` asserts exit 2; `scripts/test-workspace-context.py:310` asserts the fixture fingerprint is unchanged. | PASS |
| BWC-07 | Plan, measure, and check disclose no selected content, credentials, transcripts, session IDs, or physical root path. | `scripts/test-workspace-context.py:98` and `scripts/test-workspace-context.py:99` assert plan privacy; `scripts/test-workspace-context.py:108` and `scripts/test-workspace-context.py:109` assert check privacy; `scripts/test-workspace-context.py:170` asserts measure content privacy; `scripts/test-workspace-context.py:204` and `scripts/test-workspace-context.py:205` assert oversized selected-route privacy. The arbitrary forbidden marker covers any selected-source payload category. | PASS |
| BWC-08 | The canonical manifest defines exactly five ordered routes, positive budgets, and explicit heading lists. | `scripts/test-workspace-context.py:66` loads the canonical manifest; `scripts/test-workspace-context.py:73` asserts the exact route tuple; `scripts/test-workspace-context.py:74` asserts positive 20,000-token budgets; `scripts/test-workspace-context.py:75` asserts every reference has a heading list. | PASS |
| BWC-09 | A selected section ending at EOF includes all code points through EOF. | `scripts/test-workspace-context.py:139` places selected `## Last` at EOF; `scripts/test-workspace-context.py:146` includes its complete text in the expected value; `scripts/test-workspace-context.py:153` and `scripts/test-workspace-context.py:155` assert exact counts. | PASS |
| BWC-10 | Two adjacent selected headings are each measured without content or synthetic separators. | `scripts/test-workspace-context.py:209` creates the dedicated fixture; `scripts/test-workspace-context.py:215` selects adjacent headings; `scripts/test-workspace-context.py:221` places them adjacently; `scripts/test-workspace-context.py:226` defines the exact unseparated selection; `scripts/test-workspace-context.py:227` through `scripts/test-workspace-context.py:230` assert exact total/source characters, rounded tokens, and content exclusion. | PASS |
| BWC-11 | A mixed all-route check reports every route deterministically and exits 1. | `scripts/test-workspace-context.py:185` invokes mixed `check`; `scripts/test-workspace-context.py:186` asserts exit 1; `scripts/test-workspace-context.py:189` asserts all route names in order; `scripts/test-workspace-context.py:190` and `scripts/test-workspace-context.py:191` assert the mixed statuses. | PASS |

**Spec-anchored status:** 11/11 pass. Every assertion targets the exact outcome defined by the spec; no spec-precision gap remains.

## Discrimination Sensor

The sensor ran in a disposable copied scratch under `/tmp` because the repository's `.git/worktrees` administration is read-only. The real implementation was never mutated. Its porcelain and the expected staged and unstaged SHA-256 fingerprints for `.specs/LESSONS.md` and `.specs/lessons.json` matched before and after cleanup.

| Mutation | Target | Behavior fault | Result |
| --- | --- | --- | --- |
| 1 | `scripts/workspace-context.py:252` | Forced selected `measure` to return 0 even when its report status is fail. | KILLED by `scripts/test-workspace-context.py:199`. |
| 2 | `scripts/workspace-context.py:95` | Inserted synthetic newlines between selected Markdown sections. | KILLED by exact character assertions beginning at `scripts/test-workspace-context.py:153`; the adjacent-heading assertions at `scripts/test-workspace-context.py:227` cover the corrected edge explicitly. |

**Sensor depth:** lightweight, 2 targeted mutations proportional to T4.
**Sensor result:** 2/2 killed. No mutant survived.

## Edge Cases

- BWC-09 EOF selection: PASS with exact character assertions.
- BWC-10 adjacent selected headings: PASS with a dedicated exact-count and no-separator fixture.
- BWC-11 mixed pass/fail all-route check: PASS with ordered complete output and exit 1.

## Gate Check

- `python3 scripts/test-workspace-context.py`: PASS, 11 logical checks.
- `python3 scripts/test-workspace-structure.py`: PASS, 5 logical checks.
- `python3 scripts/workspace-gate-evidence.py run --profile workspace`: PASS; immediate status is reusable for the same state.
- `git diff --check 747499280ed4588a8b28f9fbd4d588016fbf2da0..6c58e73fa55a743b46f30ef761ec88212d2d027f`: PASS.
- `git diff --check -- .specs/LESSONS.md .specs/lessons.json`: PASS.
- Test count in `scripts/test-workspace-context.py`: 5 logical checks before, 11 after, delta +6; no skips or deletions.
- Structural validators: spec has 0 errors and 0 warnings; tasks have 0 errors and 4 non-blocking granularity warnings.
- Machine preflight: 12 online CPUs, load average 1.55, 2,087,645,184 bytes available memory; the root gate ran sequentially without reducing coverage.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum code and no scope creep | PASS |
| Surgical changes and existing patterns | PASS |
| No weakened, skipped, or deleted tests | PASS |
| Spec-anchored outcomes | PASS: 11/11 exact outcomes asserted. |
| Per-layer coverage | PASS: planner, CLI, manifest, privacy, and workspace contracts covered. |
| Every new test has a claimed requirement or done-when | PASS |
| Documented guidelines | PASS: `AGENTS.md` and TLC `coding-principles.md`. |

## Ranked Gaps

None.

## Summary

The corrected implementation satisfies BWC-01 through BWC-11. Both previous gaps are closed by direct, discriminating tests. Behavioral and delivery validation are complete, and the evidence-only closure preserves the independently verified work SHA.
