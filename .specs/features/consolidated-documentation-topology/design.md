# Consolidated Documentation Topology Design

**Spec**: `.specs/features/consolidated-documentation-topology/spec.md`
**Status**: Approved

## Architecture Overview

The workspace will preserve project-level entry points while changing their documentation roots to
subdirectories of one shared Git repository. Repository operations remain attached to real Git
roots. Skills resolve `inventeer-ops` once, then select the IDS or Portal subtree by domain.

```text
projects/ids.md ---------------------> repos/inventeer-ops/artifacts/products/ids/
projects/assistants.md ---- IDS ----^                   |
portal-task-context ------ IDS -----^                   +--> clients/ and plugin/ids-delivery/

projects/portal.md ------------------> repos/inventeer-ops/artifacts/products/portal/
portal-task-context -----------------+--> repos/portal-api
                                     +--> repos/portal-web
```

The approved alternative was explicit subpaths. Rejected alternatives were keeping archived clones
as compatibility shims and creating symlinks that look like repository roots. Both would preserve
the ambiguity INV-3770 is intended to remove.

## Code Reuse Analysis

| Component | Location | How to Use |
| --- | --- | --- |
| Project registry | `projects/README.md` | Keep logical project routing and add a shared operations entry point |
| Safe clone updater | `scripts/update-repos.sh` | Continue updating real roots; no path alias or parser change |
| Portal TLC contract | `scripts/test-portal-tlc-session-artifacts.sh` | Preserve session lifecycle while replacing the retired documentation root |
| Aggregate gate | `scripts/test-workspace.sh` | Add the focused topology contract as one suite |
| Shell contract style | `scripts/test-*.sh` | Use exact `grep` assertions and fail-fast diagnostics |

## Components

### Authority and Project Navigation

- **Purpose**: Define which repo or subtree owns operations, IDS, Portal product documentation, and Portal implementation.
- **Location**: `AGENTS.md`, `README.md`, `projects/`
- **Dependencies**: INV-3713 topology, AD-006, AD-008
- **Reuses**: Existing lightweight project-pointer model

### Product Context Routing

- **Purpose**: Resolve Assistants and Portal preparation against consolidated documentation without changing task semantics.
- **Location**: `.agents/skills/assistants-task-context/`, `.agents/skills/portal-task-context/`
- **Dependencies**: Authority and Project Navigation
- **Reuses**: Existing conditional IDS loading and repository ownership classification

### Topology Contract

- **Purpose**: Fail when active workspace sources regress to retired roots or omit required current roots.
- **Location**: `scripts/test-consolidated-documentation-topology.sh`, `scripts/test-workspace.sh`
- **Dependencies**: All declared authority surfaces
- **Reuses**: Existing shell contract tests and aggregate gate

## Error Handling Strategy

| Error Scenario | Handling | User Impact |
| --- | --- | --- |
| `inventeer-ops` clone missing | Context skill reports the missing required clone and stops | No fallback to archived, stale documentation |
| Active source uses retired root | Focused contract exits non-zero with the offending path | Gate blocks the regression |
| Portal implementation path resembles retired root prefix | Scan distinguishes `portal-api` and `portal-web` from standalone `portal` | Valid code ownership remains unchanged |

## Risks & Concerns

| Concern | Location | Impact | Mitigation |
| --- | --- | --- | --- |
| Historical decisions contain retired paths | `.specs/STATE.md` | A naive global scan would require rewriting history | Limit the zero-stale-path invariant to active sources and append AD-042 |
| Shared documentation repo can be mistaken for a code repo | Portal context skill and project registry | Docs-only tasks could broaden implementation scope | State subtree ownership separately from API/Web ownership |
| Existing Portal TLC test asserts the retired root | `scripts/test-portal-tlc-session-artifacts.sh` | Correct skill changes would fail the old contract | Update the assertion to cover the shared docs subtree and both code repos |
| Root clone list is stale | `README.md` | New machines recreate archived clones | Replace `ids`/`portal` clone commands with `inventeer-ops` and test exact commands |

## Tech Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Repository representation | Explicit subpaths under `repos/inventeer-ops` | Preserves real Git boundaries and makes ownership visible |
| Project representation | Keep IDS and Portal logical pointers | Projects and repos remain separate concepts under AD-006/AD-008 |
| Regression protection | Focused shell contract included in the aggregate gate | Matches existing workspace tests and confirmed lesson L-008 |
| Historical references | Preserve feature history; supersede active path decisions through AD-042 | Maintains the decision audit trail required by the workspace |

