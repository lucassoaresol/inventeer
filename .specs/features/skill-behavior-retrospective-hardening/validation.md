# Skill Behavior Retrospective Hardening Validation

**Date:** 2026-08-27
**Spec:** `.specs/features/skill-behavior-retrospective-hardening/spec.md`
**Diff range:** `2b6d00f..30cc7fa`
**Work SHA:** `30cc7fa8c7014bcfe9136174ce7b30ad0541ab14`
**Verifier:** fresh independent sub-agent (author != verifier)
**Verifier mode:** independent-agent
**Verifier evidence:** Fresh verifier `/root/verify_skill_hardening` independently inspected all twelve requirements, ran the terminal workspace gate and 93 focal checks, and killed three behavioral mutants in an isolated clone.

## Overall Status

**Overall:** PASS

All twelve requirements match the committed implementation and their spec-defined outcomes. No
spec-precision gap, failed criterion, surviving mutant, or unrelated diff was found.

## Delivery Evidence

- **Validation state:** `pending-delivery`
- **Evidence binding:** implementation range `2b6d00f..30cc7fa`; work SHA `30cc7fa8c7014bcfe9136174ce7b30ad0541ab14`
- **Requirement contract:** validated specification at `.specs/features/skill-behavior-retrospective-hardening/spec.md:1`
- **Gate state:** green; `python3 scripts/workspace-gate-evidence.py run --profile workspace` returned `{"profile":"workspace","result":"passed","schema":1}`
- **Pending delivery conditions:** commit this validation report and the verification-only status updates; publication remains separately unauthorized
- **High-risk paths:** TLC provenance gate, exact-head materializer, review ledger v2, and session-history metric classifier

## Task Completion

| Task | Status | Notes |
| --- | --- | --- |
| T1 | Done | Provenance modes and historical compatibility verified. |
| T2 | Done | Pattern identity, safety, recurrence, and legacy behavior verified. |
| T3 | Done | Detached exact-head materialization and source preservation verified. |
| T4 | Done | Ledger v2, v1 compatibility, and pilot promotion verified. |
| T5 | Done | Contract-v5 skill evidence and privacy behavior verified. |
| T6 | Done | Focused read-only skill and both engine surfaces verified. |
| T7 | Done | AD-053, workspace routing, traceability, and aggregate inclusion verified. |

## Requirement Verification

| Requirement | Spec-defined outcome | `file:line` + assertion evidence | Result |
| --- | --- | --- | --- |
| SBRH-01 | A new PASS must declare a supported Verifier mode and real mode-specific evidence. | `.agents/skills/tlc-spec-driven/scripts/validate_state.py:136` validates provenance; `scripts/test-tlc-deterministic-gates.py:196` asserts placeholder evidence exits 1 and `scripts/test-tlc-deterministic-gates.py:208` asserts fallback needs a reason. | PASS |
| SBRH-02 | Aggregate checking preserves historical PASS reports without provenance migration. | `.agents/skills/tlc-spec-driven/scripts/validate_state.py:215` requires provenance only for an explicit feature; `scripts/test-tlc-deterministic-gates.py:236` asserts the historical aggregate fixture exits 0. | PASS |
| SBRH-03 | Same signal and pattern key merge different wording; different signals remain separate. | `.agents/skills/tlc-spec-driven/scripts/lessons.py:214` matches signal plus pattern; `.agents/skills/tlc-spec-driven/scripts/test-lessons.py:113` asserts one merged lesson and `.agents/skills/tlc-spec-driven/scripts/test-lessons.py:157` asserts cross-signal separation. | PASS |
| SBRH-04 | New keys are bounded and sensitive-looking keys fail before write while legacy matching remains usable. | `.agents/skills/tlc-spec-driven/scripts/lessons.py:325` validates shape before loading the store and `.agents/skills/tlc-spec-driven/scripts/lessons.py:220` retains legacy exact matching; `.agents/skills/tlc-spec-driven/scripts/test-lessons.py:79` asserts rejected inputs leave bytes unchanged. | PASS |
| SBRH-05 | The helper verifies full base/head commits, detaches at exact head, and preserves the source checkout. | `.agents/skills/review-pull-request/scripts/materialize-review-head.sh:25` rejects invalid inputs and `.agents/skills/review-pull-request/scripts/materialize-review-head.sh:35` verifies both commits; `.agents/skills/review-pull-request/scripts/test-materialize-review-head.sh:33` asserts head/base/detached state and line 40 asserts source identity. | PASS |
| SBRH-06 | Schema v2 binds passed/failed checks to final head or requires a bounded state-compatible reason; v1 remains valid. | `scripts/pr-review-pilot.py:162` selects the versioned field contract and `scripts/pr-review-pilot.py:171` enforces head/reason invariants; `scripts/test-pr-review-pilot.py:106`, `scripts/test-pr-review-pilot.py:119`, and `scripts/test-pr-review-pilot.py:136` assert the exact outcomes. | PASS |
| SBRH-07 | The nine-record pilot is promoted with its measured limits recorded. | `.specs/STATE.md:866` records AD-053; `scripts/test-pr-review-workflow.py:115` asserts the nine-PR counts, promotion, schema v2, and materialization decision. | PASS |
| SBRH-08 | Structured Claude `Skill` calls aggregate validated names and distinct session counts without content. | `scripts/audit-session-history.py:470` restricts invocation parsing to assistant tool-use items and line 476 to `Skill`; `scripts/test-session-history-audit.py:562` asserts exact invocation totals and line 566 distinct-session totals. | PASS |
| SBRH-09 | Codex invocation metrics are unsupported `null`, never measured zero. | `scripts/audit-session-history.py:76` declares both Codex invocation metrics unsupported; `scripts/test-session-history-audit.py:515` asserts both are null with explicit reasons. | PASS |
| SBRH-10 | Exact `SKILL.md` paths in tool inputs count only as proxies; prose/output decoys do not count. | `scripts/audit-session-history.py:196` walks tool-input strings only and line 208 extracts exact proxies; `scripts/test-session-history-audit.py:289` plants prose and tool-input cases and line 517 asserts only valid proxies. | PASS |
| SBRH-11 | One bounded retrospective skill is exposed from the same source to Codex and Claude. | `.agents/skills/retrospect-skill-usage/SKILL.md:2` declares discriminating metadata; `.agents/skills/retrospect-skill-usage/agents/openai.yaml:1` exposes Codex; `scripts/test-skill-engine-parity.py:58` asserts manifests and exact relative Claude symlinks. | PASS |
| SBRH-12 | Retrospectives stay read-only and sanitized, and recommendations do not self-authorize implementation. | `.agents/skills/retrospect-skill-usage/SKILL.md:8` declares read-only behavior, line 37 prohibits transcript/session content, and line 70 forbids implementation; `scripts/test-session-history-audit.py:632` asserts sensitive content and physical paths are absent. | PASS |

**Status:** All 12 requirements are covered and matched to precise outcomes.

## Test Results

- **Terminal gate:** 1 aggregate workspace profile passed, 0 failed.
- **Focal verification:** 93 checks/scenarios passed, 0 failed, 0 skipped.
- **Focal baseline at `2b6d00f`:** 79 checks/scenarios across the same existing suites; current delta is +14. The five materializer scenarios are new and the remaining increase comes from provenance, lesson safety, ledger-v2, and governance assertions.
- **Suites:** 20 TLC deterministic gates; 11 lesson scenarios; 5 materializer scenarios; 14 ledger tests; 12 review workflow contracts; 20 session-auditor scenarios; 6 engine-parity contracts; 5 workspace-structure contracts.
- **Spec/tasks artifact gates:** their committed validators are included in the aggregate workspace profile.

No test was deleted, weakened, skipped, or disabled in the feature range.

## Diff Integrity

- `git diff --check 2b6d00f..30cc7fa`: clean.
- The range contains 28 expected workspace files and no file under `repos/`.
- The implementation was split into four value increments: `b06bca3`, `b70cfe4`, `3ec9d92`, and `30cc7fa`.
- Real-tree porcelain was empty before the sensor and remained byte-identical after scratch cleanup.
- The only post-verification changes are this report and status-only edits in the feature spec.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum code and no speculative flexibility | PASS |
| Surgical changes and no product-repository mutation | PASS |
| Existing standard-library, shell, Git, and skill conventions retained | PASS |
| Assertions match the spec-defined values, enums, identities, nulls, and failure exits | PASS |
| Every new test maps to SBRH-01..12 or a listed edge case | PASS |
| Privacy and read-only workspace guidelines followed (`AGENTS.md`) | PASS |

## Discrimination Sensor

The preferred temporary worktree could not be created because sandboxed `.git/worktrees` metadata
is read-only. The permitted fallback used a local `--no-hardlinks` clone detached at the exact work
SHA. The clone was deleted after restoring and confirming its clean state.

| Mutation | File:line | Fault | Result |
| --- | --- | --- | --- |
| M1 | `.agents/skills/tlc-spec-driven/scripts/validate_state.py:132` | Replaced real-value validation with unconditional acceptance. | Killed: TLC suite failed six placeholder/fallback cases. |
| M2 | `.agents/skills/review-pull-request/scripts/materialize-review-head.sh:46` | Inverted exact resolved-head equality. | Killed: materializer suite exited 1 on the valid exact-head fixture. |
| M3 | `scripts/audit-session-history.py:476` | Inverted structured `Skill` tool-name detection. | Killed: auditor expected engine block assertion failed. |

**Sensor depth:** lightweight, three high-risk behavioral mutations.
**Result:** 3/3 killed, 0 survived, PASS.

## Edge Cases

- Placeholder Verifier evidence and unsupported mode fail closed.
- Historical reports remain valid only through aggregate compatibility mode.
- Malformed or sensitive-looking pattern keys write nothing.
- Same pattern across different signals does not merge.
- Invalid Git identities and destinations do not claim a review surface or alter source state.
- Excluded-only skill evidence, unsupported roots, decoy prose/results, and receipt privacy are tested.

## Requirement Traceability Update

SBRH-01 through SBRH-12 moved from `Implemented` to `Verified`; the feature status moved from
`Implemented` to `Validated`.

## Summary

**Overall:** PASS

The feature is behaviorally complete at `30cc7fa`. The terminal gate is green, all 93 focal checks
pass, and all three mutants were killed. No validation signal exists to distill into a lesson. The
remaining delivery-only condition is committing this report and its status-only spec update.
