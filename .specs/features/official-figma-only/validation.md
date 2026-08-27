# Official Figma MCP Only Validation

**Verdict:** PASS
**Date:** 2026-08-27
**Spec:** `.specs/features/official-figma-only/spec.md`
**Diff range:** `66a83bf475334f125fa8b939aa8f7767d9bbf33f..5435bb9951b038df28eb8d9b646a883b9ef4ee70`
**Verifier:** standalone TLC fresh-eyes fallback; multi-agent delegation was not authorized

## Delivery Evidence

- **Validation state:** `pass`
- **Evidence binding:** behavioral commit `5435bb9951b038df28eb8d9b646a883b9ef4ee70`
- **Requirement contract:** `.specs/features/official-figma-only/spec.md` at the behavioral commit
- **Gate state:** focal MCP suite, complete-range diff check and post-commit aggregate gate passed
- **Pending delivery conditions:** restart the engines before relying on the changed MCP inventory
- **High-risk paths:** `.codex/config.toml`, `.mcp.json`, `scripts/test-mcp-config.py`
- **Excluded state:** `.specs/LESSONS.md` and `.specs/lessons.json` remain user-owned staged and unstaged changes outside the behavioral commit

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| Both engines load only the official MCP | Official endpoint exists in both engines and `figma-local` is absent | `scripts/test-mcp-config.py:76`-`:82` asserts `figma["url"] == EXPECTED_FIGMA_URL`; `:89`-`:92` asserts `"figma-local" not in servers` and not auto-enabled | PASS |
| Official server stays enabled with write approval | Codex `figma.enabled` is true and approval remains `writes` | `scripts/test-mcp-config.py:85`-`:86` asserts `default_tools_approval_mode == "writes"` and `enabled is True` | PASS |
| Active guidance routes only to official OAuth MCP | README and AGENTS contain official-only guidance and no local plugin activation text | `scripts/test-mcp-config.py:106`-`:148` asserts required OAuth/official-only phrases and rejects three plugin activation markers | PASS |
| Decision history preserves and narrows AD-051 | AD-051 retains pilot history; active AD-052 supersedes only that portion | `scripts/test-mcp-config.py:151`-`:168` asserts both decisions, historical pilot fields and the exact partial-supersession boundaries | PASS |

**Status:** 4/4 criteria match the exact spec-defined state.

## Edge Cases

- Reintroducing `figma-local` in either engine is rejected at `scripts/test-mcp-config.py:89`-`:92`.
- Changing the official endpoint, enabled state or approval mode is rejected at `scripts/test-mcp-config.py:76`-`:86`.
- Reintroducing active plugin installation guidance is rejected at `scripts/test-mcp-config.py:142`-`:148`.

## Gate Check

- `python3 scripts/test-mcp-config.py`: PASS, 16 checks.
- `python3 scripts/workspace-gate-evidence.py run --profile workspace`: PASS with schema 1 receipt after the corrected behavioral commit.
- `git diff --check 66a83bf475334f125fa8b939aa8f7767d9bbf33f..5435bb9951b038df28eb8d9b646a883b9ef4ee70`: PASS.
- Spec validator: 0 errors and 0 warnings.
- Resource preflight: 12 CPUs, load 0.04, 2,747,412,480 bytes available memory and 1,073,647,616 bytes free swap; execution remained sequential.
- Tests removed or skipped: none. Existing MCP suite remains at 16 grouped checks.

## Discrimination Sensor

Mutations ran only in `/tmp/official-figma-only.4dyA5A/repo`. The real worktree was read-only during sensor execution.

| Mutation | Behavior-level fault | Result |
| --- | --- | --- |
| M1 | Reintroduced `figma-local` in Claude configuration | KILLED by the exact absence assertion |
| M2 | Changed official Codex Figma from `enabled = true` to `false` | Initially survived; direct enabled-state assertion was added, then the mutant was KILLED |
| M3 | Reintroduced `Import plugin from manifest` in active README guidance | KILLED by the forbidden-guidance assertion |

**Sensor depth:** lightweight, three mutations over configuration and guidance boundaries.

**Final result:** 3/3 killed, 0 survived.

**Isolation:** real porcelain before and after remained exactly `MM .specs/LESSONS.md` and
`MM .specs/lessons.json`.

## Corrective Iteration

The first verifier pass exposed that the official enabled state was documented but not asserted.
The unpublished behavioral commit was amended with `assert codex_servers["figma"]["enabled"] is True`,
then the focal suite, mutation and aggregate gate were rerun. Confirmed lesson L-008 already covers
this failure class, so no duplicate lesson was recorded.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum implementation and no scope creep | PASS |
| Only official/local Figma configuration and its contracts changed | PASS |
| Existing endpoint and approval patterns preserved | PASS |
| Every test maps to an acceptance criterion or listed edge case | PASS |
| No test weakened, removed or skipped | PASS |
| Workspace instructions and confirmed lesson L-008 followed | PASS |

## Ranked Gaps

None. The external plugin files intentionally remain on Windows but are not configured or referenced
by either engine.

## Summary

**Overall:** PASS. Both engines now expose only the official Figma OAuth MCP, active plugin guidance
is absent, AD-051 history is preserved through AD-052, and all three behavior-level mutants are killed.
