# Dual-engine Workspace Validation

**Date**: 2026-07-26
**Requirement contract**: `.specs/STATE.md` AD-024 and AD-025
**Diff range**: `0f3e85784512649b4804559b21aa2f24628eb05c..580936411c94be451486545e3d68c119d532ac75`
**Verifier**: standalone fresh-eyes fallback after two independent verifier runs were interrupted

## Delivery Evidence

- **Validation state**: `pending-delivery`
- **Evidence binding**: exact committed range above; work SHA `580936411c94be451486545e3d68c119d532ac75`
- **Gate state**: green — 14/14 sync tests, range-bound diff integrity, syntax/config checks
- **Pending delivery conditions**: commit this report with the validated delivery or intentionally
  retain it as local review evidence; push remains outside this validation's authorization
- **High-risk paths**: live APEX catalog/resource compatibility and generated-wrapper reconciliation

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | Evidence | Result |
| --- | --- | --- | --- |
| AD-024: one source for workspace skills | Claude's seven project skills resolve through relative symlinks to `.agents/skills/`; APEX wrappers remain Codex-only | `CLAUDE.md:11`; shell assertion `find -L .claude/skills -type l` returned no broken links; seven targets inspected | PASS |
| AD-024: APEX configured in both engines | Codex uses `.codex/config.toml`; Claude uses project `.mcp.json` with `apex` enabled | `.mcp.json:1`; `.claude/settings.json:1`; `CLAUDE.md:20` | PASS |
| AD-024: generated workflow wrappers | Useful live workflows become deterministic `apex-<id>` wrappers without copying workflow bodies | `scripts/test-sync-apex-commands.sh:52` selection; `:66` creation; `:75` resource assertion; `:85` idempotency; `:92` drift; `:104` removal | PASS |
| AD-024: APEX remains canonical | Every wrapper points to `apex://framework/workflows/<id>` and stops on missing/empty resources | `.agents/skills/apex-eng-start/SKILL.md:14`; all 28 wrappers inspected; all 28 live resources read successfully | PASS |
| AD-025: executor precedence is explicit | Repos with `ENV.md` use APEX; repos without it and this workspace use TLC; context skills remain preparatory | `AGENTS.md:64`; `.specs/STATE.md:272` | PASS |

No formal `spec.md` exists for this historical change. AD-024 and AD-025 are sufficiently precise
for the outcomes above; the absence of a separate spec is recorded but does not make an outcome
ambiguous.

## Live APEX Compatibility

- `apex_framework_index` returned 30 workflow entries.
- The implemented filters rejected `README` (no description) and `warm-up` (`DEPRECATED`), yielding
  exactly 28 wrappers.
- All 28 `apex://framework/workflows/<id>` resources were read through the configured MCP.
- Empty resources: 0; invalid/missing frontmatter: 0.
- Body-size range: 299–46,176 bytes.
- `eng-start` was inspected in detail and contains its workflow frontmatter, preflight gate, phases,
  constraints and handoffs.

## Discrimination Sensor

Mutations ran only in a disposable `/tmp/dual-engine-sensor.*` copy. The real worktree was not
mutated or stashed.

| Mutation | Expected detection | Result |
| --- | --- | --- |
| Remove the `DEPRECATED` selection filter | Selection test rejects the extra workflow | KILLED |
| Invert the `check`/`apply` branch | no-write and exit-code tests fail | KILLED |
| Corrupt wrapper prefix from `apex-` to `apexx-` | creation/frontmatter assertions fail | KILLED |

**Sensor result**: 3/3 killed — PASS.

## Gate Check

- `scripts/test-sync-apex-commands.sh`: 14 passed, 0 failed, 0 skipped.
- `git diff --check 0f3e857..5809364`: exit 0.
- `bash -n scripts/sync-apex-commands.sh scripts/test-sync-apex-commands.sh`: exit 0.
- `jq -e . .mcp.json .claude/settings.json`: exit 0.
- Broken Claude symlinks: 0.
- APEX wrappers with missing name/resource reference: 0/28.
- Test count before feature: 0 dedicated sync tests.
- Test count after feature: 14 dedicated sync tests.

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum code and no copied APEX workflow bodies | PASS |
| Surgical workspace-only changes | PASS |
| Generated content is visibly derived and reproducible | PASS |
| Tests cover selection, create/update/remove, idempotency and guards | PASS |
| Documentation matches implementation and engine boundaries | PASS |
| No product repository, Linear or GitHub state changed | PASS |

## Findings and Residual Risks

No correctness blocker was found.

1. `sync-apex-commands.sh` deliberately does not call MCP itself. A future sync depends on an agent
   acquiring and serializing `apex_framework_index` according to `--print-contract`.
2. `bytes` and `frontmatter_ok` are optional catalog fields. Runtime wrappers still stop safely on an
   empty resource, and this validation separately proved all 28 current resources are non-empty and
   well formed.
3. Project-level Claude skill discovery can again be shadowed by a global skill of the same name;
   this is documented in `CLAUDE.md` and remains an environment hygiene risk.
4. `codex mcp list` currently labels the remote servers' auth as `Unsupported`, while MCP tool and
   resource calls succeed in this active session. Treat the CLI label as a diagnostic inconsistency,
   not evidence that the APEX integration is unavailable.

## Summary

**Behavioral verdict**: PASS.

The three commits implement AD-024 and AD-025 correctly. Both engine exposure paths are coherent,
the generated wrapper lifecycle is discriminating under mutation, and the complete live APEX
workflow set used by the wrappers is available and well formed. Promotion remains
`pending-delivery` only because delivery/commit of this report and push were not authorized.
