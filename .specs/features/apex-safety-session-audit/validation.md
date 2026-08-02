# APEX Safety and Session Audit Validation

**Date**: 2026-08-02
**Spec**: `.specs/features/apex-safety-session-audit/spec.md`
**Diff ranges**: original delivery `c4e1d0e..b8f40fc`; native-pilot amendment
`c1e3cef..2223fc9`
**Verifier**: standalone fresh-eyes fallback, without sub-agents per user request

## Delivery Evidence

- **Validation state**: workspace tooling `pass`; native APEX `blocked` on an external contract gap
- **Evidence binding**: original implementation at `b8f40fc`; outcome-aware amendment and sanitized
  native pilot at `2223fc9`
- **Requirement contract**: approved 2026-08-02 workspace tooling request, AD-026, AD-027,
  AD-032, and AD-033
- **Gate state**: green; 85/85 workspace checks, 5/5 targeted mutants across both validation
  passes, real-history outcome check, and range-scoped diff integrity
- **Pending delivery conditions**: native `eng-ready` requires the APEX server to publish
  `preflight` and inject the `=== APEX WORKSPACE ===` context block
- **High-risk paths**: `.codex/config.toml` approval semantics and local history parsing

## Task Completion

| Task | Status | Notes |
| --- | --- | --- |
| Define the requirement contract | Done | Commit `99293cc` |
| Approval-gate Codex APEX writes | Done | Commit `6f0fb6d` |
| Add sanitized session audit | Done | Commit `404b8af` |
| Close the pre-cutoff continuation edge | Done | Commit `b8f40fc` |
| Run native Claude/APEX `eng-ready` pilot | Blocked as designed | Canonical resource loaded; required `preflight` absent |
| Separate successful, failed, denied, and unresolved APEX attempts | Done | Commit `2223fc9` |

## Native APEX Pilot Amendment

Claude Code 2.1.220 ran a real, read-only pilot against `repos/portal-api` in local session
`33333333-4444-4555-8666-777777777777`. Edit, write, shell, agent, and worktree tools were disabled;
no product file, Git state, Linear item, or GitHub object changed.

The server connected and the canonical `apex://framework/workflows/eng-ready` resource loaded. The
workflow then failed closed before its gate result because:

1. the session did not receive the `=== APEX WORKSPACE ===` context block required by Step 0;
2. the connected server did not publish `preflight`, which Step 1 requires; and
3. two optional diagnostic APEX calls were denied in non-interactive mode.

The exact sanitized evidence and revalidation contract are recorded in `apex-native-pilot.md`.
Reading a workflow resource, attempting a tool, or reproducing part of the check with filesystem
tools is not classified as APEX execution (AD-034).

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + assertion/evidence | Result |
| --- | --- | --- | --- |
| APEX-1 | Codex APEX uses exact approval mode `writes` | `scripts/test-mcp-config.py:30` — `assert codex_servers["apex"]["default_tools_approval_mode"] == "writes"` | PASS |
| APEX-2 | Guardrails require approval and preserve ownership/executor boundaries | `scripts/test-mcp-config.py:76` and `:87` — required README and AGENTS phrases; source at `AGENTS.md:64-65` | PASS |
| APEX-3 | Configuration test fails when approval is weakened | Scratch mutation `writes` to `prompt` was killed by `scripts/test-mcp-config.py:30` | PASS |
| APEX-4 | Claude APEX configuration remains unchanged | `git diff --name-only c4e1d0e..b8f40fc` excludes `.mcp.json`; `scripts/test-mcp-config.py:24-25` still parses the original Claude definition | PASS |
| AUDIT-1 | Codex summary reports main, continuation, subagent, logical, and APEX counts | `scripts/test-session-history-audit.py:200` — exact full-dictionary equality through line 212 | PASS |
| AUDIT-2 | Claude summary reports session, sidechain, logical, and APEX counts | `scripts/test-session-history-audit.py:213` — exact full-dictionary equality through line 223 | PASS |
| AUDIT-3 | Drop/continue reference is one continuation, including an old parent | Fixture at `scripts/test-session-history-audit.py:142` references `OLD_PARENT`; line 159 places the parent before the cutoff; lines 203 and 205 assert continuation and logical counts | PASS |
| AUDIT-4 | Explicitly excluded session contributes to no count | Fixture at `scripts/test-session-history-audit.py:149`; lines 199-212 assert one exclusion and the complete accepted summary without its `apex_git_push` | PASS |
| AUDIT-5 | JSON and text contain no transcript content or history path | `scripts/test-session-history-audit.py:196`, `:230`, and `:231` — sentinel and fixture-path absence | PASS |
| AUDIT-6 | Only structured APEX calls count | Fake prompt name at `scripts/test-session-history-audit.py:136`; structured event at line 137; exact result at line 208 contains only `apex_framework_index` | PASS |
| AUDIT-7 | Fixtures detect all required classification, exclusion, counting, and leakage behavior | `scripts/test-session-history-audit.py:133` through line 251 — exact aggregate and empty-directory assertions; script exits non-zero on any mismatch | PASS |
| AUDIT-8 | Attempt outcomes remain distinct | Fixtures assert Codex `Err`, Claude success, failure, `toolDenialKind`, and missing result as separate aggregates | PASS |
| PILOT-1 | Fetch and attempt the canonical read-only workflow | Native Claude session loaded `apex://framework/workflows/eng-ready` and attempted Step 1 without mutations | PASS |
| PILOT-2 | Fail closed when a required tool is absent | Direct deferred-tool lookup found no `preflight`; no manual proxy was presented as APEX | PASS |
| PILOT-3 | Persist only sanitized pilot evidence | `apex-native-pilot.md` contains metadata, outcomes, and routes; no transcript or tool payload | PASS |

**Status**: all 15 acceptance criteria match precise spec outcomes; native APEX remains honestly
blocked rather than falsely reported as executed.

## Edge Cases

| Edge case | Evidence | Result |
| --- | --- | --- |
| Wrong cwd and pre-cutoff sessions are ignored | Fixtures at `scripts/test-session-history-audit.py:150-161`; accepted count fixed at line 201 | PASS |
| Continuation parent predates cutoff | `OLD_PARENT` at lines 142 and 158-160; continuation remains `1` at line 203 | PASS |
| Claude resumes are not invented | Only explicit `isSidechain` at line 170 affects expected sidechain/logical counts at lines 215-216 | PASS |
| Missing history directories are safe and empty | `scripts/test-session-history-audit.py:233-251` | PASS |

## Test Adequacy

The initial fresh-eyes pass found one uncovered declared edge: the continuation fixture referenced a
parent inside the cutoff even though the spec also promises classification when the parent predates
the cutoff. Commit `b8f40fc` reused the already excluded old fixture as the referenced parent. The
full 85-check gate and the continuation mutation were rerun after the correction.

The independently confirmed recurrence promoted lesson `L-008` to confirmed: workspace contract
tests must assert every declared lifecycle edge case, not only the primary path.

The native pilot exposed a second semantic edge: a structured tool request may be denied, fail, or
never receive a result. Commit `2223fc9` now counts `apex_sessions` and `apex_calls` from successes
only, while preserving attempts and non-success outcomes in separate aggregates. Against the real
histories after 2026-07-29, the Claude pilot is one attempt session with zero successful APEX
sessions and two denials, exactly matching the observed execution.

| Assertion group | Maps to | Keep? |
| --- | --- | --- |
| `test-mcp-config.py:24-31` | APEX-1, APEX-3, APEX-4 | Keep |
| `test-mcp-config.py:69-98` | APEX-2 and active decision integrity | Keep |
| `test-session-history-audit.py:133-178` | Codex/Claude fixtures, outcome classes, and edge conditions | Keep |
| `test-session-history-audit.py:180-223` | AUDIT-1 through AUDIT-4, AUDIT-6, and AUDIT-8 | Keep |
| `test-session-history-audit.py:225-251` | AUDIT-5 and missing-directory edge | Keep |

**Verdict**: sufficient, non-shallow, requirement-bounded, and aligned with existing workspace
contract-test patterns. No tests or assertions were deleted, skipped, or weakened.

## Discrimination Sensor

| Mutation | Scratch target | Description | Killed? |
| --- | --- | --- | --- |
| 1 | `.codex/config.toml` in disposable archive | Changed APEX approval from `writes` to `prompt` | Yes; exact config assertion failed |
| 2 | `scripts/audit-session-history.py` in disposable archive | Changed structured server filter from `apex` to `linear` | Yes; exact APEX aggregate failed |
| 3 | `scripts/audit-session-history.py` in disposable archive | Disabled the `caiu` continuation marker | Yes; continuation and logical counts failed after the edge fix |
| 4 | `scripts/audit-session-history.py` in disposable archive | Replaced Claude `toolDenialKind` detection with a missing field | Yes; exact Claude outcome aggregate failed |
| 5 | `scripts/audit-session-history.py` in disposable archive | Inverted Codex `Ok`/`Err` success recognition | Yes; exact Codex outcome aggregate failed |

**Sensor depth**: lightweight, five targeted behavior-level mutations across the two validation
passes
**Result**: 5/5 killed — PASS. The real worktree remained untouched by every mutant.

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
- Discrimination sensor: 5 killed, 0 survived across original and amendment passes
- Real-history check: Claude `apex_attempt_sessions=1`, `apex_sessions=0`,
  `apex_denials={apex_framework_index:1, apex_rag_status:1}`
- `git diff --check`: exit 0 for the amendment worktree
- First aggregate attempt invoked non-executable vendored Python tests directly and stopped after 28
  passing Bash checks; the command was corrected to use `python3`, then the complete suite passed.
  This runner mistake changed no code and is not a project-local execution lesson.

## Requirement Traceability Update

| Requirement | Previous | New |
| --- | --- | --- |
| ASSA-01 through ASSA-08 | Implementing | Verified |
| ASSA-09 through ASSA-10 | Implementing | Verified |

## Summary

**Overall**: Workspace tooling ready; native APEX `eng-ready` blocked

Codex APEX writes are approval-gated without changing Claude, the session audit safely reduces 27
recent Codex files to 14 logical work streams, and APEX usage is derived from structured call/result
outcomes. The real Claude pilot proved that the current server contract cannot execute `eng-ready`
because `preflight` and workspace context are absent. The workspace now records that limitation,
fails closed, and has an exact revalidation route instead of overstating APEX confidence.
