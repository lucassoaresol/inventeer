# APEX Safety and Session Audit Validation

**Date**: 2026-08-02
**Spec**: `.specs/features/apex-safety-session-audit/spec.md`
**Diff range**: `c4e1d0e..b8f40fc`
**Verifier**: standalone fresh-eyes fallback, without sub-agents per user request

## Delivery Evidence

- **Validation state**: `pass`
- **Evidence binding**: implementation and tests at `b8f40fc`, range `c4e1d0e..b8f40fc`
- **Requirement contract**: approved 2026-08-02 workspace tooling request, AD-026, AD-027,
  AD-032, and AD-033
- **Gate state**: green; 85/85 workspace checks, 3/3 targeted mutants, and range-scoped diff
  integrity
- **Pending delivery conditions**: none; this report is a non-behavioral evidence closure
- **High-risk paths**: `.codex/config.toml` approval semantics and local history parsing

## Task Completion

| Task | Status | Notes |
| --- | --- | --- |
| Define the requirement contract | Done | Commit `99293cc` |
| Approval-gate Codex APEX writes | Done | Commit `6f0fb6d` |
| Add sanitized session audit | Done | Commit `404b8af` |
| Close the pre-cutoff continuation edge | Done | Commit `b8f40fc` |

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + assertion/evidence | Result |
| --- | --- | --- | --- |
| APEX-1 | Codex APEX uses exact approval mode `writes` | `scripts/test-mcp-config.py:30` — `assert codex_servers["apex"]["default_tools_approval_mode"] == "writes"` | PASS |
| APEX-2 | Guardrails require approval and preserve ownership/executor boundaries | `scripts/test-mcp-config.py:76` and `:87` — required README and AGENTS phrases; source at `AGENTS.md:64-65` | PASS |
| APEX-3 | Configuration test fails when approval is weakened | Scratch mutation `writes` to `prompt` was killed by `scripts/test-mcp-config.py:30` | PASS |
| APEX-4 | Claude APEX configuration remains unchanged | `git diff --name-only c4e1d0e..b8f40fc` excludes `.mcp.json`; `scripts/test-mcp-config.py:24-25` still parses the original Claude definition | PASS |
| AUDIT-1 | Codex summary reports main, continuation, subagent, logical, and APEX counts | `scripts/test-session-history-audit.py:153-161` — exact full-dictionary equality | PASS |
| AUDIT-2 | Claude summary reports session, sidechain, logical, and APEX counts | `scripts/test-session-history-audit.py:162-168` — exact full-dictionary equality | PASS |
| AUDIT-3 | Drop/continue reference is one continuation, including an old parent | Fixture at `scripts/test-session-history-audit.py:109` references `OLD_PARENT`; line `126` places the parent before the cutoff; lines `156` and `158` assert continuation and logical counts | PASS |
| AUDIT-4 | Explicitly excluded session contributes to no count | Fixture at `scripts/test-session-history-audit.py:116`; lines `152-161` assert one exclusion and the complete accepted summary without its `apex_git_push` | PASS |
| AUDIT-5 | JSON and text contain no transcript content or history path | `scripts/test-session-history-audit.py:149`, `:173`, and `:174` — sentinel and fixture-path absence | PASS |
| AUDIT-6 | Only structured APEX calls count | Fake prompt name at `scripts/test-session-history-audit.py:103`; structured event at `:104`; exact result at `:160` contains only `apex_framework_index` | PASS |
| AUDIT-7 | Fixtures detect all required classification, exclusion, counting, and leakage behavior | `scripts/test-session-history-audit.py:152-194` — exact aggregate and empty-directory assertions; script exits non-zero on any mismatch | PASS |

**Status**: all 11 acceptance criteria match precise spec outcomes; no precision gaps.

## Edge Cases

| Edge case | Evidence | Result |
| --- | --- | --- |
| Wrong cwd and pre-cutoff sessions are ignored | Fixtures at `scripts/test-session-history-audit.py:117-128`; accepted count fixed at line `154` | PASS |
| Continuation parent predates cutoff | `OLD_PARENT` at lines `109`, `125-126`; continuation remains `1` at line `156` | PASS |
| Claude resumes are not invented | Only explicit `isSidechain` at line `88` affects expected sidechain/logical counts at lines `164-165` | PASS |
| Missing history directories are safe and empty | `scripts/test-session-history-audit.py:176-194` | PASS |

## Test Adequacy

The initial fresh-eyes pass found one uncovered declared edge: the continuation fixture referenced a
parent inside the cutoff even though the spec also promises classification when the parent predates
the cutoff. Commit `b8f40fc` reused the already excluded old fixture as the referenced parent. The
full 85-check gate and the continuation mutation were rerun after the correction.

The independently confirmed recurrence promoted lesson `L-008` to confirmed: workspace contract
tests must assert every declared lifecycle edge case, not only the primary path.

| Assertion group | Maps to | Keep? |
| --- | --- | --- |
| `test-mcp-config.py:24-31` | APEX-1, APEX-3, APEX-4 | Keep |
| `test-mcp-config.py:69-98` | APEX-2 and active decision integrity | Keep |
| `test-session-history-audit.py:100-131` | Codex/Claude fixtures and edge conditions | Keep |
| `test-session-history-audit.py:133-168` | AUDIT-1 through AUDIT-4 and AUDIT-6 | Keep |
| `test-session-history-audit.py:170-194` | AUDIT-5 and missing-directory edge | Keep |

**Verdict**: sufficient, non-shallow, requirement-bounded, and aligned with existing workspace
contract-test patterns. No tests or assertions were deleted, skipped, or weakened.

## Discrimination Sensor

| Mutation | Scratch target | Description | Killed? |
| --- | --- | --- | --- |
| 1 | `.codex/config.toml` in disposable archive | Changed APEX approval from `writes` to `prompt` | Yes; exact config assertion failed |
| 2 | `scripts/audit-session-history.py` in disposable archive | Changed structured server filter from `apex` to `linear` | Yes; exact APEX aggregate failed |
| 3 | `scripts/audit-session-history.py` in disposable archive | Disabled the `caiu` continuation marker | Yes; continuation and logical counts failed after the edge fix |

**Sensor depth**: lightweight, three targeted behavior-level mutations
**Result**: 3/3 killed — PASS. Every scratch directory was removed; the real worktree remained
untouched.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum, surgical implementation | PASS |
| No product repository or Claude configuration mutation | PASS |
| No transcript content persisted or emitted | PASS |
| Existing Python and workspace contract patterns preserved | PASS |
| Every test maps to an AC, edge case, or active workspace boundary | PASS |
| Guidelines followed | `AGENTS.md`, TLC `coding-principles.md`, and `validate.md` |

## Gate Check

- Complete serial workspace suite: 85 passed, 0 failed, 0 skipped
- Feature audit fixtures: 6 passed, 0 failed, 0 skipped
- MCP configuration contract: 11 passed, 0 failed, 0 skipped
- Discrimination sensor: 3 killed, 0 survived
- `git diff --check c4e1d0e..b8f40fc`: exit 0
- First aggregate attempt invoked non-executable vendored Python tests directly and stopped after 28
  passing Bash checks; the command was corrected to use `python3`, then the complete suite passed.
  This runner mistake changed no code and is not a project-local execution lesson.

## Requirement Traceability Update

| Requirement | Previous | New |
| --- | --- | --- |
| ASSA-01 through ASSA-08 | Implementing | Verified |

## Summary

**Overall**: Ready

Codex APEX writes are approval-gated without changing Claude, the session audit safely reduces 27
recent Codex files to 14 logical work streams, and APEX usage is derived only from structured calls.
The validation found and closed one declared edge-case coverage gap before PASS.
