# Workspace MCP and Resource Preflight

**Status:** Approved from the user's 2026-07-28 request and scope correction
**Scope:** This workspace only; no product repository, Linear, GitHub, or external account mutation

## Objective

Make complex work adapt to the machine before consuming resources and expose only the documentation
MCP that has durable, cross-project value in both Codex and Claude Code.

## Requirements

1. **WMR-01 — Machine snapshot:** The workspace SHALL provide one read-only command that reports
   online CPUs, load, memory, swap, and workspace filesystem capacity before expensive work.
2. **WMR-02 — Execution routing:** Workspace and TLC instructions SHALL require a fresh resource
   snapshot before full suites, builds, containers, browsers, mutation testing, or parallel agents.
3. **WMR-03 — Coverage integrity:** A constrained execution plan MAY shard or bound concurrency but
   SHALL run the complete required gate and SHALL NOT relabel a partial selection as full coverage.
4. **WMR-04 — Context7 parity:** Codex and Claude Code SHALL receive the same project-scoped Context7
   stdio server definition without checked-in credentials.
5. **WMR-05 — Current-doc chain:** Context7 SHALL remain after codebase and project documentation in
   the TLC knowledge chain; it SHALL not replace canonical repository sources.
6. **WMR-06 — Cwd-sensitive MCP boundary:** The workspace SHALL NOT configure shadcn at this root
   because its tools resolve `components.json` and write targets from the server working directory.
   A future adoption belongs in `repos/portal-web` under a separately authorized product change.
7. **WMR-07 — Provider MCP boundary:** The workspace SHALL NOT configure Cloudflare or AWS MCPs
   without a current canonical need. Cloudflare is being left behind by the Portal migration; the
   current official AWS surface adds authentication and operational authority before that migration
   is represented in the registered project sources.
8. **WMR-08 — Verification:** Automated checks SHALL parse both MCP configs, run the machine snapshot,
   validate the TLC skill, and assert the resource and boundary contracts above.

## Success Criteria

- The preflight command exits zero on this Linux host and exposes all five resource dimensions.
- Context7 is configured in `.codex/config.toml` and `.mcp.json` with matching command and arguments.
- No secret, API key, Cloudflare, AWS, or root-scoped shadcn server is added.
- Static and mutation checks detect removal of Context7 or weakening of the preflight contract.
