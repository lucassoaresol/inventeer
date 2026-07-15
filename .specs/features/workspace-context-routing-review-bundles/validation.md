# Workspace Context Routing and Review Bundles — Validation

**Date:** 2026-07-15
**Spec:** `.specs/features/workspace-context-routing-review-bundles/spec.md`
**Diff range:** `af2cd19..d55ca6d`
**Verifier:** fresh independent sub-agent (author != verifier)
**Verdict:** PASS

## Scope and task completion

No `tasks.md` exists for this feature. The four commits in the requested range were independently
reviewed: `177340c`, `33afa9a`, `14e3551`, and `d55ca6d`. The diff contains 13 files, remains inside
the workspace, and does not modify `repos/` or `inv-cortex`.

## Spec-anchored acceptance criteria

| AC | Spec-defined outcome | Evidence (`file:line` + assertion/contract expression) | Result |
|---|---|---|---|
| WCR-01 | A multi-issue/cycle/backlog route compares readiness, formal dependencies, code collisions, and execution order without fully preparing every issue. | `.agents/skills/triage-project-cycle/SKILL.md:28-31` — “do not expand every issue into a full context package”; `:43-47` — evaluate readiness and build waves from formal blockers and code collisions; `:53-60` — package requires comparison, dependency graph, collisions, and execution waves. | PASS |
| WCR-02 | Issue-less discovery starts from the registry/canonical sources, separates facts from hypotheses, and does not invent Linear hierarchy. | `.agents/skills/discover-project-context/SKILL.md:18-19` — read registry and reject an unregistered route; `:25-38` — establish source authority and separate observed behavior, inference, hypothesis, and unknowns; `:67-70` — do not require/invent an issue or present hypothesis as fact. | PASS |
| WCR-03 | Selecting or finding an issue hands off to the matching single-issue product context skill. | `.agents/skills/triage-project-cycle/SKILL.md:62-66` — invoke the matching product task-context skill after selection and pass only relevant evidence; `.agents/skills/discover-project-context/SKILL.md:58-63` — switch to product task-context when an `INV-*` exists and defer TLC until ownership/work item are clear. | PASS |
| RB-01 | Changes relative to the base produce a ZIP containing manifest, status, commits, index, one diff per file, and SHA-256 checksum. | `.agents/skills/create-review-bundle/scripts/create-review-bundle.sh:142-145,147-173,187-208` — creates `status.txt`, `commits.txt`, `files.tsv`, per-file diffs, manifest, ZIP, and checksum; `.agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh:32-50` — asserts ZIP/checksum, manifest/index, three diffs, and `sha256sum -c`. Independent archive listing contained every required entry. | PASS |
| RB-02 | Tracked, removed, and untracked paths appear individually. | `.agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh:44-47` — asserts exactly three diff files and exact TSV rows for `changed.txt`, `removed.txt`, and `untracked file.txt`; implementation classification is at `.agents/skills/create-review-bundle/scripts/create-review-bundle.sh:114-120,147-166`. | PASS |
| RB-03 | Bundle generation does not alter the source repository status. | `.agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh:50-68` — exact before/after status comparisons for external, rejected internal, and ignored internal output; `.agents/skills/create-review-bundle/scripts/create-review-bundle.sh:94-105` — rejects a non-ignored internal destination before `mkdir`. Independent three-destination reproduction is recorded below. | PASS |
| RB-04 | Invalid bases, empty changes, and likely credential/key/dump paths are refused. | `.agents/skills/create-review-bundle/scripts/create-review-bundle.sh:18-33,81-84,122-133` — explicit sensitive-name, invalid-base, empty-set rejection; `.agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh:70-91` — asserts empty/base/credential refusal. Independent matrix returned `3` (empty), `2` (invalid base), and `4` for `credentials.json`, `private.pem`, and `archive.dump`. | PASS |
| DOC-01 | README, registry, AGENTS, and workspace decisions expose the routes, limits, and handoffs. | `README.md:34-43,75-99` — skill catalog, intent routing, handoffs, and bundle limits; `projects/README.md:17-28` — registry routing and canonical-source boundary; `AGENTS.md:35-49` — mandatory skill routing; `.specs/STATE.md:161-188` — AD-018/AD-019 decisions and trade-offs. | PASS |

**Spec-anchored status:** 8/8 ACs match the specified outcome; zero uncovered criteria and zero
spec-precision gaps.

## Independent RB-03 reproduction

The source fixture status before every case was exactly:

```text
 M tracked.txt
?? untracked.txt
```

| Destination | Exit/result | Exact source status | Residue |
|---|---|---|---|
| External output | Success | Identical before/after | Exactly one `.zip` and its `.zip.sha256` |
| Non-ignored internal output | Exit `4` | Identical before/after | Requested directory absent |
| Ignored internal output (`session-context/`) | Success | Identical before/after | Exactly one `.zip` and its `.zip.sha256`; no visible Git residue |

## Gate checks

| Check | Result |
|---|---|
| `quick_validate.py` — `triage-project-cycle` | PASS — `Skill is valid!` |
| `quick_validate.py` — `discover-project-context` | PASS — `Skill is valid!` |
| `quick_validate.py` — `create-review-bundle` | PASS — `Skill is valid!` |
| `bash -n` on both shell scripts | PASS |
| `shellcheck` on both shell scripts | PASS — zero findings |
| `test-create-review-bundle.sh` | PASS — 8/8 behavioral checks, 0 failed, 0 skipped |
| Markdown local links in changed files | PASS — 7/7 targets exist |
| `git diff --check af2cd19..d55ca6d` | PASS — no output |

The functional test script is new in this range: baseline count 0, current count 8, delta +8. No
test was deleted, skipped, or weakened in the requested range.

## Discrimination sensor

All mutations were applied only to independent copies beneath `/tmp`; the real worktree was never
mutated.

| Mutation | Behavior fault | Test that killed it | Result |
|---|---|---|---|
| M1 | Inverted the `check-ignore` guard, allowing non-ignored internal output. | Test 4 failed: “non-ignored output inside source repository should be rejected”. | KILLED |
| M2 | Removed `.env` from sensitive-path classification. | Test 8 failed: “sensitive path should be rejected”. | KILLED |
| M3 | Suppressed collection of untracked paths. | Test 2 failed: “expected three per-file diffs”. | KILLED |

**Sensor result:** 3/3 killed; 0 survived.

## Code quality

| Principle | Result |
|---|---|
| Minimum code / no speculative abstraction | PASS |
| Surgical scope / no unrelated repository changes | PASS |
| Read-only source-repository behavior | PASS |
| Existing Bash/skill patterns and documented workspace conventions | PASS |
| Tests trace to RB acceptance criteria and assert observable outcomes | PASS |
| No unclaimed tests | PASS — all eight checks map to RB-01 through RB-04 |
| Guidelines followed | PASS — `AGENTS.md` and `.agents/skills/tlc-spec-driven/references/coding-principles.md` |

## Summary

**Overall:** PASS — ready. All 8 ACs have file-and-line evidence, every requested gate passed, the
three RB-03 destination modes preserved exact source status with the expected residue, and all 3
behavior-level mutants were killed.

**Ranked gaps:** none.
