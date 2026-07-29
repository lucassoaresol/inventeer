# Workspace MCP and Resource Preflight Validation

**Date:** 2026-07-28
**Spec:** `.specs/features/workspace-mcp-resource-preflight/spec.md`
**Correction range:** `1a49117..4d53a1c`
**Correction head:** `4d53a1c`
**Verifier:** standalone fresh-eyes fallback, without sub-agent by user request

## Verdict

**PASS.** The Codex shadcn working directory now resolves from the workspace root, the complete gate
has 41 behavioral checks passing, the real shadcn process starts from Portal Web, and the exact
previous-path mutant is killed.

## Delivery Evidence

- **Validation state:** `pass`
- **Evidence binding:** correction range `1a49117..4d53a1c`; the following closure commit contains
  only evidence, lesson bookkeeping, and handoff reconciliation
- **Requirement contract:** corrected WMR-06 at `4d53a1c`, aligned with active AD-030
- **Gate state:** green; 41/41 behavioral checks, ShellCheck, skill validation, shadcn smoke, and
  `git diff --check 1a49117..4d53a1c`
- **Pending delivery conditions:** none; report closure does not change implementation behavior
- **High-risk paths:** relative MCP working directories depend on the engine's operational root;
  startup still requires the cloned Portal Web repo, Node/npm, and package availability

## Runtime Finding

After the earlier implementation was published, Codex reported `No such file or directory (os
error 2)` while starting shadcn. The previous test resolved Codex's `cwd` from `.codex/`, but the
runtime resolves it from the trusted workspace root. Consequently, `../repos/portal-web` targeted a
nonexistent sibling of the workspace, while `repos/portal-web` targets the registered product repo.
The finding was independently reproduced by comparing both resolved paths and by observing the
effective `codex mcp get shadcn` configuration before and after the correction.

## Spec-Anchored Evidence

| Requirement | Spec-defined outcome | Assertion evidence | Result |
| --- | --- | --- | --- |
| WMR-04 | Context7 remains identical and credential-free in both engines | `scripts/test-mcp-config.py:30-35` | PASS |
| WMR-06 | Both shadcn configs use workspace-relative `repos/portal-web`, resolve the canonical `components.json`, and keep writes approval-gated | `scripts/test-mcp-config.py:39-54` | PASS |
| WMR-07 | Cloudflare, AWS, and credential markers remain absent | `scripts/test-mcp-config.py:56-64` | PASS |
| WMR-08 | Parsing, strict target resolution, complete gates, startup smoke, and mutation detect regressions | gate and sensor evidence below | PASS |

WMR-01 through WMR-03 and WMR-05 were unchanged and revalidated by their existing gate assertions.
**Status:** 8/8 requirements match precise outcomes; zero spec-precision gaps.

## Test Adequacy

| Assertion | Maps to | Verdict |
| --- | --- | --- |
| `test-mcp-config.py:39-46` — both entries use `ROOT` and exact `repos/portal-web` | WMR-06 | Necessary and sufficient |
| `test-mcp-config.py:47-49` — `resolve(strict=True)` and equality with the canonical target | WMR-06, WMR-08 | Necessary and sufficient |
| `test-mcp-config.py:53` — approval mode equals `writes` | WMR-06 | Necessary and sufficient |

The corrected assertion failed against the published bad value before implementation, then passed
after the config change. No test was removed, skipped, or weakened.

## Gate Check

- `./scripts/test-machine-resource-preflight.sh` — 4 passed
- `python3 scripts/test-mcp-config.py` — 10 passed
- `./scripts/test-engine-routing.sh` — 9 passed
- `./scripts/test-sync-apex-commands.sh` — 15 passed
- `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` — 2 passed
- `python3 .agents/skills/tlc-spec-driven/scripts/test-validation-guidance.py` — 1 passed
- ShellCheck over the five Bash scripts in the feature gate — passed
- skill-creator `quick_validate.py` for `tlc-spec-driven` — passed
- `git diff --check 1a49117..4d53a1c` — passed
- `codex mcp get shadcn` — reports `cwd: repos/portal-web`
- Shadcn stdio smoke from `repos/portal-web` remained active for 15 seconds awaiting a client
- **Result:** 41 passed, 0 failed, 0 skipped; all static and smoke gates green

## Discrimination Sensor

The mutation ran in a `git archive 4d53a1c` export under `/tmp`, with the canonical Portal Web
`components.json` copied into the ignored target path. The real worktree was never edited or stashed,
and the disposable directory was removed after the run.

| Mutation | Fault | Covering assertion | Result |
| --- | --- | --- | --- |
| M1 | Restore Codex cwd to `../repos/portal-web` | `scripts/test-mcp-config.py:46` requires workspace-relative `repos/portal-web` | KILLED — cwd equality assertion |

**Sensor depth:** lightweight, one targeted regression mutation. **Result:** 1/1 killed.

## Code Quality and Boundaries

| Check | Result |
| --- | --- |
| Minimum three-file functional correction | PASS |
| No product-repo changes | PASS |
| No credentials or provider authority added | PASS |
| Spec, test, effective config, and runtime agree | PASS |
| Existing Context7, engine, APEX, and lesson gates remain green | PASS |

## Lessons Handoff

The independently confirmed runtime finding above qualifies as `review_finding`. Record one
candidate lesson requiring MCP cwd checks to use the engine's operational workspace root and prove
the configured directory exists before publication.

## Summary

**Overall:** PASS. **Spec check:** 8/8. **Gate:** 41/41 plus static and smoke checks.
**Sensor:** 1/1 killed. Codex and Claude now use `repos/portal-web`, which resolves to the canonical
shadcn configuration from the workspace root.
