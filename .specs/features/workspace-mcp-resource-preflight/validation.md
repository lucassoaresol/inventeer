# Workspace MCP and Resource Preflight Validation

**Date:** 2026-07-28
**Spec:** `.specs/features/workspace-mcp-resource-preflight/spec.md`
**Implementation range:** `e59e61f..9822ae1`
**Implementation head:** `9822ae1`
**Verifier:** standalone fresh-eyes fallback, without sub-agent by user request

## Verdict

**PASS.** All eight requirements match their specified outcomes. The complete workspace gate has 41
behavioral checks passing, static checks are green, the shadcn process starts from Portal Web and
waits for an MCP client, and all three disposable-copy mutants were killed.

## Delivery Evidence

- **Validation state:** `pass`
- **Evidence binding:** implementation range `e59e61f..9822ae1`; the following closure commit contains
  only this report and workspace handoff reconciliation
- **Requirement contract:** revised `spec.md` and AD-030 at `71f129a`
- **Gate state:** green; 41/41 behavioral checks, ShellCheck, skill validation, shadcn smoke, and
  `git diff --check e59e61f..9822ae1`
- **Pending delivery conditions:** none; report closure does not change implementation behavior
- **High-risk paths:** shadcn startup requires `repos/portal-web`, Node/npm, and network/package
  availability; writes remain approval-gated and product-owned

## Requirement Evidence

| Requirement | Spec-defined outcome | Evidence | Result |
| --- | --- | --- | --- |
| WMR-01 | One read-only snapshot reports CPU, load, memory, swap, and filesystem | `scripts/test-machine-resource-preflight.sh:20-25` asserts all five numeric dimensions | PASS |
| WMR-02 | Workspace and TLC require a snapshot before heavy work | `AGENTS.md:92-99`; `scripts/test-machine-resource-preflight.sh:27-40` | PASS |
| WMR-03 | Resource routing may schedule differently but cannot reduce gate coverage | `implement.md` requires every shard and aggregation; resource gate lines 33-40 assert the contract | PASS |
| WMR-04 | Codex and Claude receive identical credential-free Context7 definitions | `.codex/config.toml:10-13`; `.mcp.json:7-9`; `scripts/test-mcp-config.py:30-35` | PASS |
| WMR-05 | Context7 follows codebase and project docs | `scripts/test-mcp-config.py:95-99`; `README.md:132-135` | PASS |
| WMR-06 | Both shadcn configs resolve to Portal Web with approval and ownership guards | configs at `.codex/config.toml:15-20` and `.mcp.json:11-14`; exact resolution assertions at `scripts/test-mcp-config.py:37-54`; guards at lines 66-85 | PASS |
| WMR-07 | Cloudflare/AWS remain absent without canonical need and authority | `scripts/test-mcp-config.py:56-64`; rationale at `README.md:143-148` and AD-030 | PASS |
| WMR-08 | Automated parsing proves config, target resolution, preflight, skill, integrity, and mutation behavior | gate and sensor evidence below | PASS |

**Status:** 8/8 requirements match precise outcomes; zero spec-precision gaps.

## Test Adequacy

| Assertion evidence | Maps to | Necessary and sufficient? |
| --- | --- | --- |
| `test-mcp-config.py:43-49` — server presence, exact command/cwd, strict target resolution and equality | WMR-06, WMR-08 | Yes |
| `test-mcp-config.py:53` — approval mode equals `writes` | WMR-06 | Yes |
| `test-mcp-config.py:56-64` — provider servers and credential markers absent | WMR-07 | Yes |
| `test-mcp-config.py:66-85` — source precedence, routing, approval, worktree, and ownership phrases present | WMR-05, WMR-06, WMR-07 | Yes |
| `test-mcp-config.py:87-99` — active decisions and knowledge-chain order | WMR-02, WMR-04, WMR-05, WMR-06 | Yes |

No assertion is shallow, speculative, or outside the eight requirements. Every changed test maps to a
spec criterion, and every revised criterion has exact assertion evidence.

## Gate Check

- `./scripts/test-machine-resource-preflight.sh` — 4 passed
- `python3 scripts/test-mcp-config.py` — 10 passed
- `./scripts/test-engine-routing.sh` — 9 passed
- `./scripts/test-sync-apex-commands.sh` — 15 passed
- `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` — 2 passed
- `python3 .agents/skills/tlc-spec-driven/scripts/test-validation-guidance.py` — 1 passed
- ShellCheck over the five Bash scripts in the feature gate — passed
- skill-creator `quick_validate.py` for `tlc-spec-driven` — passed
- `git diff --check e59e61f..9822ae1` — passed
- Shadcn stdio smoke from `repos/portal-web`: `timeout 15s npx shadcn@latest mcp` remained active
  for 15 seconds awaiting an MCP client — passed
- **Result:** 41 passed, 0 failed, 0 skipped; all static and smoke gates green

Test count increased from 37 to 41 because the MCP suite grew from 6 to 10 checks. No test was
deleted, skipped, or weakened.

## Discrimination Sensor

Each mutation ran in a separate `git archive 9822ae1` export under `/tmp`, with only the canonical
Portal Web `components.json` copied into the ignored target path. The real worktree was never edited
or stashed, and all three directories were removed after the run.

| Mutation | Fault | Covering assertion | Result |
| --- | --- | --- | --- |
| M1 | Rename Claude's `shadcn` server to `shadcn-disabled` | `scripts/test-mcp-config.py:42-43` requires the named server | KILLED — `Claude omits shadcn` |
| M2 | Route Codex shadcn to `repos/portal-api` | `scripts/test-mcp-config.py:46` requires the engine-specific Portal Web cwd | KILLED — cwd equality assertion |
| M3 | Change Codex shadcn approval from `writes` to `prompt` | `scripts/test-mcp-config.py:53` requires write approval mode | KILLED — approval assertion |

**Sensor depth:** lightweight, three targeted configuration mutations. **Result:** 3/3 killed.

## Code Quality and Boundaries

| Check | Result |
| --- | --- |
| Minimum scope; no product-repo changes | PASS |
| No credentials or provider-account authority | PASS |
| Context7 remains secondary to canonical local sources | PASS |
| Both shadcn cwd values resolve to the product-owned config | PASS |
| Writes require approval, local instructions, and worktree inspection | PASS |
| Cloudflare and AWS remain deferred | PASS |
| Preflight changes scheduling, never gate coverage | PASS |
| Existing APEX, engine, and lesson routing remains green | PASS |

## Lessons Handoff

No failed criterion, surviving mutant, spec-precision gap, `SPEC_DEVIATION`, or external-review
finding was produced by this continuation. No new lesson is warranted.

## Summary

**Overall:** PASS. **Spec check:** 8/8. **Gate:** 41/41 plus static and smoke checks.
**Sensor:** 3/3 killed. The workspace now exposes Context7 and approval-gated shadcn in both engines,
routes shadcn to Portal Web's canonical `components.json`, and continues to exclude Cloudflare and AWS.
