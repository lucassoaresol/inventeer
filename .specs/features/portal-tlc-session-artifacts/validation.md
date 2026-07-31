# Portal TLC Session Artifacts Validation

**Date**: 2026-07-31
**Spec**: `.specs/features/portal-tlc-session-artifacts/spec.md`
**Diff range**: `22d95a3..65c4278`
**Verifier**: standalone fresh-eyes fallback, without sub-agents per user request

## Delivery Evidence

- **Validation state**: `pass`
- **Evidence binding**: implementation and tests at `65c4278`, range `22d95a3..65c4278`
- **Requirement contract**: approved Portal-only transitional policy and AD-031
- **Gate state**: green; 18/18 contract scenarios, ShellCheck, skill validation, and diff integrity
- **Pending delivery conditions**: none; this report is a non-behavioral evidence closure
- **High-risk paths**: none; no product repository or vendored TLC file changed

## Task Completion

| Task | Status | Notes |
| --- | --- | --- |
| Transitional policy and Portal handoff | Done | Commit `0f7af35` |
| Coverage correction from fresh-eyes review | Done | Commit `65c4278` |

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| PTSA-01 | All Portal Codex/TLC handoffs use `session-context/portal/<INV-ID>/tlc/` | `scripts/test-portal-tlc-session-artifacts.sh:27` — `grep -Fq "$contract_path" "$file"` | PASS |
| PTSA-02 | No TLC `.specs/` in any Portal repo | `scripts/test-portal-tlc-session-artifacts.sh:49` — `grep -q 'Do not create or promote ...'` | PASS |
| PTSA-03 | Session artifacts are local, ephemeral, non-canonical, and non-durable | `scripts/test-portal-tlc-session-artifacts.sh:33` — `grep -q 'Esse material é local' AGENTS.md`; lines 35-40 assert the remaining classifications | PASS |
| PTSA-04 | Product code/tests/docs, Linear, and PR remain official; local files are not APEX evidence | `scripts/test-portal-tlc-session-artifacts.sh:39` — `grep -q 'must not be presented as canonical, durable, or official APEX evidence'`; line 44 asserts Linear and PR | PASS |
| PTSA-05 | Review bundles use the task-local `review/` path | `scripts/test-portal-tlc-session-artifacts.sh:62` — `grep -Fq 'session-context/portal/<INV-ID>/review/' README.md` | PASS |
| PTSA-06 | Task directory is eligible for cleanup after merge and closure | `scripts/test-portal-tlc-session-artifacts.sh:64` — `grep -q 'merge.*encerr' README.md` | PASS |
| PTSA-07 | Route retires after end-to-end APEX support | `scripts/test-portal-tlc-session-artifacts.sh:70` — `grep -q 'deve ser retirada quando o Codex executar APEX' AGENTS.md`; line 72 binds end-to-end | PASS |
| PTSA-08 | Claude/APEX, other products, and generic TLC remain unchanged | `scripts/test-portal-tlc-session-artifacts.sh:74` — `grep -q 'Claude/APEX e outros produtos permanecem' README.md`; line 80 rejects the Portal path in TLC | PASS |

**Status**: all 8 acceptance criteria match precise spec outcomes; no precision gaps.

## Edge Cases

| Edge case | Evidence | Result |
| --- | --- | --- |
| Inline TLC creates no file-backed artifact | `scripts/test-portal-tlc-session-artifacts.sh:58` — `grep -q 'Create files there only' .../SKILL.md` | PASS |
| Durable official spec becomes a delivery constraint | `scripts/test-portal-tlc-session-artifacts.sh:55` — `grep -q 'surface the durable' .../specification-policy.md` | PASS |
| Cross-machine portability remains unsupported | `scripts/test-portal-tlc-session-artifacts.sh:66` — `grep -q 'não oferece portabilidade cross-machine' .specs/STATE.md` | PASS |

## Test Adequacy

The first fresh-eyes pass found that the contract test did not explicitly assert PTSA-04's named
official surfaces or two declared edge-case boundaries. Commit `65c4278` added those assertions and
the complete gate was rerun. No assertion was weakened, deleted, or skipped.

The grounded AC gap produced candidate lesson `L-008` for future workspace contract tests.

| Assertion group | Maps to | Keep? |
| --- | --- | --- |
| Lines 22-31 | Active decision and PTSA-01 | Keep |
| Lines 33-46 | PTSA-03 and PTSA-04 | Keep |
| Lines 49-60 | PTSA-02 and inline/durable-spec edge cases | Keep |
| Lines 62-68 | PTSA-05, PTSA-06, portability edge case | Keep |
| Lines 70-83 | PTSA-07 and PTSA-08 | Keep |
| Lines 85-92 | Ignored ephemeral state and structural skill validity | Keep |

**Verdict**: sufficient, non-shallow, requirement-bounded, and aligned with workspace shell-test patterns.

## Discrimination Sensor

| Mutation | File:line | Description | Killed? |
| --- | --- | --- | --- |
| 1 | `README.md:45` in disposable archive | Removed PR from the named official delivery surfaces | Yes; the assertion at test line 44 exited 1 |

**Sensor depth**: lightweight, one targeted contract mutation
**Result**: 1/1 killed — PASS. The archive was removed from `/tmp`; the real worktree was untouched.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum, surgical implementation | PASS |
| No product repo or generic TLC change | PASS |
| No scope creep or unsupported canonical claim | PASS |
| Existing skill and documentation patterns preserved | PASS |
| Every test maps to an AC, edge case, or structural boundary | PASS |
| Guidelines followed | `AGENTS.md`, TLC `coding-principles.md`, and `validate.md` |

## Gate Check

- `./scripts/test-engine-routing.sh`: 9 passed, 0 failed, 0 skipped
- `./scripts/test-portal-tlc-session-artifacts.sh`: 9 passed, 0 failed, 0 skipped
- `shellcheck scripts/test-engine-routing.sh scripts/test-portal-tlc-session-artifacts.sh`: exit 0
- `python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/portal-task-context`: valid
- `git diff --check 22d95a3..65c4278`: exit 0
- Scenario count before feature: 9; after feature: 18; delta: +9

## Requirement Traceability Update

| Requirement | Previous | New |
| --- | --- | --- |
| PTSA-01 through PTSA-08 | Implementing | Verified |

## Summary

**Overall**: Ready

The workspace now has a tested Portal-only handoff for local TLC artifacts, an explicit authority
boundary, a cleanup and retirement lifecycle, and no changes to product repositories or generic TLC.
The next Portal delivery must pilot the mechanics before AD-031 is considered consolidated.
