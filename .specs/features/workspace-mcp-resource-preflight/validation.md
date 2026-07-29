# Workspace MCP and Resource Preflight Validation

**Date:** 2026-07-28
**Spec:** `.specs/features/workspace-mcp-resource-preflight/spec.md`
**Implementation range:** `c3e3df4..7d8eb2c`
**Implementation head:** `7d8eb2c`
**Verifier:** standalone fresh-eyes fallback, without sub-agent by user request

## Verdict

**PASS.** All eight requirements match their specified outcomes. The complete workspace gate has 37
behavioral checks passing, ShellCheck and skill validation are green, the Context7 process starts and
waits for an MCP client, and all three disposable-copy mutants were killed.

## Delivery Evidence

- **Validation state:** `pass`
- **Evidence binding:** implementation range `c3e3df4..7d8eb2c`; the closure commit contains only
  this report, its grounded lesson, and workspace handoff reconciliation
- **Requirement contract:** approved `spec.md` at `869306a`, including the user's exclusion of
  Cloudflare Docs
- **Gate state:** green after corrective commit `7d8eb2c`; 37/37 behavioral checks, ShellCheck,
  skill validation, and `git diff --check c3e3df4..7d8eb2c`
- **Pending delivery conditions:** none after the evidence-only closure commit
- **High-risk paths:** MCP startup depends on network/package availability; no credentials or
  provider-account tools were configured

## Requirement Evidence

| Requirement | Spec-defined outcome | Evidence | Result |
| --- | --- | --- | --- |
| WMR-01 | One read-only snapshot reports CPU, load, memory, swap, and filesystem | `scripts/check-machine-resources.sh:14-32`; numeric assertions at `scripts/test-machine-resource-preflight.sh:20-25` | PASS |
| WMR-02 | Workspace and TLC require a snapshot before heavy work | `AGENTS.md:79-88`; `.agents/skills/tlc-spec-driven/references/implement.md:37-47`; contract assertions at `scripts/test-machine-resource-preflight.sh:27-40` | PASS |
| WMR-03 | Resource routing may schedule differently but cannot reduce gate coverage | `implement.md:44-47` requires every shard and aggregation; mutation M3 proves the assertion discriminates representative-only coverage | PASS |
| WMR-04 | Codex and Claude receive identical credential-free Context7 stdio definitions | `.codex/config.toml:10-13`; `.mcp.json:7-10`; exact parity assertion at `scripts/test-mcp-config.py:26-31` | PASS |
| WMR-05 | Context7 follows codebase and project docs | `.agents/skills/tlc-spec-driven/SKILL.md` Knowledge Verification Chain; order assertions at `scripts/test-mcp-config.py:59-63`; `README.md:132-136` | PASS |
| WMR-06 | No root-scoped shadcn; product ownership is documented | forbidden-server assertion at `scripts/test-mcp-config.py:13,33-36`; boundary at `README.md:140-141` | PASS |
| WMR-07 | No Cloudflare/AWS MCP without canonical need and authority | forbidden-server assertion at `scripts/test-mcp-config.py:13,33-36`; rationale at `README.md:142-145` and AD-029 | PASS |
| WMR-08 | Automated parsing, snapshot, skill, integrity, and mutation checks | gate and sensor evidence below | PASS |

**Status:** 8/8 requirements match precise outcomes; zero spec-precision gaps.

## Gate Check

- `./scripts/test-machine-resource-preflight.sh` — 4 passed
- `python3 scripts/test-mcp-config.py` — 6 passed
- `./scripts/test-engine-routing.sh` — 9 passed
- `./scripts/test-sync-apex-commands.sh` — 15 passed
- `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` — 2 passed
- `python3 .agents/skills/tlc-spec-driven/scripts/test-validation-guidance.py` — 1 passed
- ShellCheck over the five workspace Bash scripts in scope — passed
- skill-creator `quick_validate.py` for `tlc-spec-driven` — passed
- `git diff --check c3e3df4..7d8eb2c` — passed
- Context7 stdio smoke: `timeout 15s npx -y @upstash/context7-mcp` — exited 124 after remaining
  active for 15 seconds with no startup error, the expected behavior while awaiting an MCP client
- **Result:** 37 passed, 0 failed, 0 skipped; all static gates green

The initial range-scoped diff gate found trailing blank lines in four newly added files. The earlier
worktree-only check had not included those files while they were untracked. Corrective commit
`7d8eb2c` removed them; a staged check and the final complete-range check then passed. This grounded
gate failure is distilled as a project-local lesson.

## Discrimination Sensor

All mutations ran in separate `git archive 7d8eb2c` exports under a disposable `/tmp` directory. The
real worktree was never edited or stashed, and the directory was removed after the run.

| Mutation | Fault | Covering assertion | Result |
| --- | --- | --- | --- |
| M1 | Rename Claude's `context7` server to `context7-disabled` | `scripts/test-mcp-config.py:26-31` requires the named server in both engines | KILLED — exit 1, `Claude omits Context7` |
| M2 | Replace the canonical preflight command with informal inspection | `scripts/test-machine-resource-preflight.sh:27-31` requires the versioned command | KILLED — exit 1, canonical command missing |
| M3 | Permit one representative shard instead of every required shard | `scripts/test-machine-resource-preflight.sh:33-40` requires complete coverage language | KILLED — exit 1, complete gate coverage missing |

**Sensor depth:** lightweight, three targeted policy/configuration mutations. **Result:** 3/3 killed.

## Code Quality and Boundaries

| Check | Result |
| --- | --- |
| Minimum scope; no product-repo changes | PASS |
| No credentials or provider-account authority | PASS |
| Context7 is secondary to canonical local sources | PASS |
| Cwd-sensitive shadcn remains with its product owner | PASS |
| Cloudflare exclusion follows the user's migration correction | PASS |
| AWS MCP is deferred until canonical migration/auth scope exists | PASS |
| Preflight changes scheduling, never gate coverage | PASS |
| Existing APEX and retrospective routing remains green | PASS |

## Lessons Handoff

The initial `gate_fail` is grounded above. Record one candidate lesson: staged or equivalent checks
must cover new files before commit, because a plain worktree diff check omits untracked paths. No
other failed AC, surviving mutant, spec-precision gap, or deviation remains.

## Summary

**Overall:** PASS. **Spec check:** 8/8. **Gate:** 37/37 plus static checks. **Sensor:** 3/3 killed.
The workspace now has portable Context7 access and an enforced machine-capacity preflight without
adding Cloudflare, AWS, or root-scoped shadcn MCPs.
