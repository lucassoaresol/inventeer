# Consolidated Documentation Topology Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The workspace still routes IDS and Portal documentation through the retired `ids` and `portal`
repositories. INV-3713 moved those documentation surfaces into `inventeer-ops`, and INV-3770
requires stale cross-repository references to resolve under the consolidated topology.

## Goals

- [x] Route every active IDS and Portal documentation lookup through `repos/inventeer-ops`.
- [x] Preserve logical project boundaries and the independent Portal implementation repositories.
- [x] Enforce the topology through a deterministic workspace contract test.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Editing `inventeer-ops` content | This workspace consumes the relocated documentation; INV-3757 and follow-up tenant tasks own its content. |
| Changing Portal API or Web code | The consolidation changes documentation ownership, not product implementation. |
| Rewriting historical feature specs | Historical evidence preserves the topology that applied when it was produced. |
| Building or redesigning moved plugins | INV-3713 preserves plugin identity and defers composition changes. |
| Creating symlinks for retired repositories | `repos/` contains real Git roots; aliases would obscure ownership and Git boundaries. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| INV-3770 applies to this workspace | Treat the issue as the canonical repointing contract | The user approved proceeding from the evidence-backed impact analysis, and the issue explicitly covers skills, scripts, and governed documents | yes |
| Logical projects after repository consolidation | Keep `projects/ids.md` and `projects/portal.md` | AD-006 and AD-008 separate project navigation from repository count | yes |
| Active-reference scan boundary | Exclude historical `.specs/features/` artifacts and superseded decision text | Rewriting historical evidence would erase the topology that governed past work | yes |
| Remaining implicit-requirement dimensions | N/A for this documentation-routing change | No runtime state, auth, persistence, external API, concurrency, or customer-data behavior changes | yes |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: Resolve Canonical Documentation Ownership

**User Story**: As an engineer, I want the workspace registry and instructions to name the
consolidated documentation roots so that discovery starts from current canonical sources.

**Why P1**: Stale roots can make task preparation stop on archived clones or load frozen contracts.

**Acceptance Criteria**:

1. WHEN the workspace resolves IDS documentation THEN it SHALL use `repos/inventeer-ops/artifacts/products/ids/` as the canonical root.
2. WHEN the workspace resolves Portal product documentation THEN it SHALL use `repos/inventeer-ops/artifacts/products/portal/` as the canonical root.
3. The workspace SHALL retain `projects/ids.md` and `projects/portal.md` as logical project entry points.
4. The workspace SHALL retain `repos/portal-api` and `repos/portal-web` as the Portal implementation repositories.
5. WHEN a new local setup follows `README.md` THEN it SHALL clone `inventeer-ops` and SHALL NOT instruct cloning the retired `ids` or `portal` repositories.

**Independent Test**: Run the focused topology contract and inspect the registry mappings and clone
commands it asserts.

### P1: Prepare Tasks Against Consolidated Sources

**User Story**: As an engineer preparing Assistants or Portal work, I want the context skills to
load product and IDS material from `inventeer-ops` so that inherited constraints remain current.

**Why P1**: Both task-context skills currently require retired repositories and can block valid work.

**Acceptance Criteria**:

1. WHEN an Assistants task has an IDS dimension THEN `assistants-task-context` SHALL resolve `repos/inventeer-ops` and load IDS material from `artifacts/products/ids/`.
2. WHEN a Portal task is prepared THEN `portal-task-context` SHALL resolve `repos/inventeer-ops`, `repos/portal-api`, and `repos/portal-web` without requiring `repos/portal`.
3. WHEN a Portal task has an IDS dimension THEN `portal-task-context` SHALL load IDS material from `repos/inventeer-ops/artifacts/products/ids/`.
4. WHEN a Portal task needs product meaning THEN `portal-task-context` SHALL load it from `repos/inventeer-ops/artifacts/products/portal/`.
5. WHILE Portal work runs through Codex and TLC, the workspace SHALL keep working artifacts under `session-context/portal/<INV-ID>/` and SHALL NOT promote `.specs/` into either Portal code repository or the Portal documentation subtree.

**Independent Test**: Run the focused topology contract plus the Portal TLC artifact contract.

### P1: Prevent Topology Regression

**User Story**: As a workspace maintainer, I want deterministic checks for the consolidated paths so
that archived repository references cannot silently return.

**Why P1**: Confirmed lesson L-008 requires contract tests to cover every named authority surface.

**Acceptance Criteria**:

1. WHEN the aggregate workspace gate runs THEN it SHALL execute the consolidated documentation topology contract.
2. IF an active instruction, project pointer, or task-context skill references `repos/ids` or the standalone `repos/portal` root THEN the focused contract SHALL fail.
3. The focused contract SHALL assert the exact IDS root, Portal documentation root, Portal implementation repositories, and `inventeer-ops` clone command.

**Independent Test**: Mutate one asserted path in a disposable worktree and confirm the focused
contract exits non-zero.

## Edge Cases

- WHEN the path scan encounters `repos/portal-api` or `repos/portal-web` THEN it SHALL keep those implementation references valid.
- WHEN historical `.specs/features/` artifacts mention the retired roots THEN the migration SHALL leave those records unchanged.
- IF `inventeer-ops` is unavailable locally THEN task-context skills SHALL report the missing required clone rather than fall back to archived repositories.

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| CDT-01 | Canonical ownership | ISSUE | INV-3770 AC2/AC5; INV-3713 MD2/MD3 | Execute | Implementing |
| CDT-02 | Logical projects | INHERITED | AD-006 and AD-008 | Execute | Implementing |
| CDT-03 | Portal implementation boundary | INHERITED | AD-010 and current Portal code ownership | Execute | Implementing |
| CDT-04 | Assistants IDS routing | ISSUE | INV-3770 AC3/AC5 | Execute | Implementing |
| CDT-05 | Portal context routing | ISSUE | INV-3770 AC3/AC5 | Execute | Implementing |
| CDT-06 | TLC artifact boundary | INHERITED | AD-031 and AD-036 | Execute | Implementing |
| CDT-07 | Regression contract | INHERITED | L-008 and root aggregate-gate policy | Execute | Implementing |
| CDT-08 | Historical evidence preservation | INHERITED | AD-040 | Execute | Implementing |

**Coverage:** 8 total, 8 mapped to tasks, 0 unmapped.

## Success Criteria

- [x] Active workspace sources contain zero standalone `repos/ids` or `repos/portal` references.
- [x] Focused topology and Portal TLC contracts pass.
- [x] The complete workspace gate passes with the new contract included.
