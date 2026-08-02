# Native APEX Pilot — `eng-ready`

**Date:** 2026-08-02
**Engine:** Claude Code 2.1.220
**Repository:** `repos/portal-api`
**Mode:** read-only, non-interactive; edit, write, shell, agent, and worktree tools disabled
**Local evidence pointer:** Claude session `33333333-4444-4555-8666-777777777777`

## Verdict

**BLOCKED — the canonical `eng-ready` workflow cannot complete against the APEX MCP contract
currently exposed to Claude Code.** This is not evidence of a successful APEX execution.

## Sanitized Evidence

| Checkpoint | Outcome |
| --- | --- |
| APEX server discovery | Connected; server appeared in the Claude MCP inventory. |
| Canonical workflow acquisition | `apex://framework/workflows/eng-ready` was read successfully. |
| Repository eligibility | `repos/portal-api` contains `ENV.md` and `AGENTS.md`. |
| Step 0 workspace resolution | The required `=== APEX WORKSPACE ===` context block was absent; the explicitly supplied repository path was used. |
| Step 1 gate | Blocked because the workflow requires `preflight(repo_path=...)`, but no `preflight` tool was published by the server. |
| Read-only APEX calls | Two diagnostic calls were denied by Claude's non-interactive permission gate and did not execute. |
| Product/external mutation | None. No product files, Git state, Linear, or GitHub were changed. |

## Contract Gap

The framework resource and tool surface are version-skewed: the served workflow requires
`preflight`, while the connected server publishes neither `preflight` nor an equivalent named tool.
Approval changes cannot repair that mismatch. An interactive session can address the separate
permission denial, but the workflow remains blocked until the MCP server exposes the required gate.

## Revalidation Route

Re-run this pilot only after the APEX server contract changes. A passing revalidation must show all
of the following in one native Claude session:

1. the workspace context resolves `repos/portal-api` without a manually injected fallback;
2. `preflight(repo_path=...)` is present and executes;
3. the returned `{ready, summary, checks[]}` payload is rendered by `eng-ready`;
4. denied, failed, or unresolved calls are not reported as successful execution; and
5. the repository and external systems remain unchanged for the read-only pilot.

This document contains only distilled metadata and outcomes. The transcript and tool payloads stay
in local engine history and are not copied into Git, per AD-027.
