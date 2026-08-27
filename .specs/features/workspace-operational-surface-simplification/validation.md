# Workspace Operational Surface Simplification Validation

**Verdict:** PASS
**Date:** 2026-08-27
**Spec:** `.specs/features/workspace-operational-surface-simplification/spec.md`
**Diff range:** `7bff83709ab5701b15871625d22c5f9845ea1cfd..f9a7a65a9aabb9c9d36b1b665b14d841e5adce0c`
**Verifier:** standalone TLC fresh-eyes fallback; multi-agent delegation was not authorized

## Delivery Evidence

- **Validation state:** `pass`
- **Evidence binding:** behavioral commit `f9a7a65a9aabb9c9d36b1b665b14d841e5adce0c`
- **Gate state:** focal gates, skill validators, complete-range diff check and the post-commit root evidence gate passed
- **Pending delivery conditions:** manual Desktop plugin installation and live Figma validation remain outside this delivery
- **Excluded state:** `.specs/LESSONS.md` and `.specs/lessons.json` remain user-owned staged and unstaged changes outside the behavioral commit

## Task Completion

| Task | Status | Evidence |
| --- | --- | --- |
| T1 | PASS | Context suite passed 11 groups; discovery skill validator passed |
| T2 | PASS | APEX synchronization suite passed 16 groups; `apex-all-tools` validator passed |
| T3 | PASS | Hygiene suite passed 3 groups and the real inventory reported `mutation: none` |
| T4 | PASS | MCP configuration suite passed 16 groups |
| T5 | PASS | AD-051, indexes, documentation, TLC gates and aggregate gate passed |

## Spec-Anchored Evidence

| Requirement | Spec-defined outcome | Evidence and assertion | Result |
| --- | --- | --- | --- |
| WOSS-01 | Discovery has a bounded sixth route | `scripts/test-workspace-context.py:74` asserts the exact route order; `:85` asserts six audited routes; `:88`-`:101` asserts stable metadata-only plans | PASS |
| WOSS-02 | Discovery freshness remains read-only | `.agents/skills/discover-project-context/SKILL.md:18`-`:26` requires route planning and forbids update, fetch and pull without separate authorization | PASS |
| WOSS-03 | One APEX inspector replaces per-workflow wrappers | `scripts/test-sync-apex-commands.sh:53`-`:76` asserts one accepted `all-tools` entry and no per-workflow wrapper; `:114`-`:119` asserts legacy removal | PASS |
| WOSS-04 | Lesson inventory is sanitized | `scripts/test-workspace-hygiene.py:73`-`:81` rejects stored prose and asserts only counts, retention and candidate IDs | PASS |
| WOSS-05 | Cleanup eligibility requires explicit lifecycle evidence and never mutates | `scripts/test-workspace-hygiene.py:82`-`:115` asserts merge-and-close conjunction, runtime evidence, protected states and byte-identical fingerprints | PASS |
| WOSS-06 | Official Figma stays enabled and unchanged | `.codex/config.toml:30`-`:33` retains the OAuth endpoint and enabled state; `scripts/test-mcp-config.py:87`-`:97` asserts parity and write approval | PASS |
| WOSS-07 | Local Figma is pinned, loopback-only and opt-in | `.codex/config.toml:35`-`:39` and `.mcp.json:29`-`:31` define the exact `0.2.0`, `127.0.0.1:1994` command; `scripts/test-mcp-config.py:99`-`:109` asserts pin, disabled state, prompt approval and no Claude auto-enable | PASS |
| WOSS-08 | Desktop plugin remains an explicit manual dependency | `scripts/test-mcp-config.py:122`-`:163` asserts README and AGENTS guidance for disposable file, disconnected plugin and target approval | PASS |
| WOSS-09 | `inventeer-ops` is excluded | `.specs/STATE.md:843`-`:845` records the boundary; complete-range diff inspection contains no path under `repos/` | PASS |

**Spec-anchored status:** 9/9 requirements pass with direct behavior or exact contract evidence.

## Edge Cases

- Missing `all-tools` fails closed in APEX synchronization.
- Invalid or unprovable hygiene evidence exits 2 without mutation; unknown directories remain protected.
- `latest`, a non-loopback address, pilot auto-enable or official Figma drift fail the MCP contract.
- Empty legacy APEX directories are not treated as skills; structural validation follows actual `SKILL.md` files.

## Gate Check

- `python3 scripts/test-workspace-context.py`: PASS, 11 groups.
- `bash scripts/test-sync-apex-commands.sh`: PASS, 16 groups.
- `python3 scripts/test-workspace-hygiene.py`: PASS, 3 groups.
- `python3 scripts/test-mcp-config.py`: PASS, 16 groups.
- Both changed skill folders passed the `skill-creator` quick validator.
- TLC spec and tasks validators returned 0 errors and 0 warnings; the commit message validator passed.
- `git diff --check 7bff83709ab5701b15871625d22c5f9845ea1cfd..f9a7a65a9aabb9c9d36b1b665b14d841e5adce0c`: PASS.
- Post-commit `python3 scripts/workspace-gate-evidence.py run --profile workspace`: PASS with schema 1 receipt.
- Resource preflight observed 12 CPUs, load 0.06, 2,775,171,072 bytes available memory and 1,073,647,616 bytes free swap; execution remained sequential.

## Discrimination Sensor

All mutations ran in the disposable clone `/tmp/woss-sensor.COhMbz/repo`; the real worktree and index were not mutated.

| Mutation | Behavior-level fault | Result |
| --- | --- | --- |
| M1 | Removed `project-discovery` from the planner's approved route order | KILLED: the context suite failed at the approved-order assertion |
| M2 | Changed the local Figma bind address from `127.0.0.1` to `0.0.0.0` | KILLED: the MCP suite failed the exact command assertion |
| M3 | Weakened Portal eligibility from merged **and** closed to merged **or** closed | KILLED: the hygiene suite failed its exact lifecycle-state assertion |

**Sensor result:** 3/3 killed, 0 survived.

**Isolation:** real porcelain before and after remained exactly `MM .specs/LESSONS.md` and
`MM .specs/lessons.json`; both are pre-existing user-owned surfaces.

## Code Quality

- Scope is confined to the workspace root; no repository under `repos/` changed.
- Tests name every authority and lifecycle boundary introduced by the implementation.
- Official Figma remains the managed default; the local bridge adds no automatic execution.
- The hygiene command reports eligibility only and contains no delete path.
- No focal or aggregate test was skipped or weakened.

## Ranked Gaps

None in the versioned contract. Live validation of `figma-local` remains intentionally pending on
manual installation and connection of the Desktop plugin in a disposable Figma file.

## Summary

**Overall:** PASS. All 9 requirements are verified, the aggregate gate is green, and all three
behavior-level mutants were killed without touching product repositories or the user's lesson files.
