# Consolidated Documentation Topology Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: activate it by name and follow its Execute
flow and Critical Rules. The skill is the source of truth for per-task gates, atomic commits,
independent verification, and the discrimination sensor.

**Design**: `.specs/features/consolidated-documentation-topology/design.md`
**Status**: Done

## Test Coverage Matrix

> Generated from `AGENTS.md`, `scripts/test-workspace.sh`, existing shell contract tests, the feature
> spec, and confirmed lesson L-008. Guidelines found: `AGENTS.md` requires focused tests plus the
> complete root gate and resource preflight before the full suite.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Workspace authority and registry | contract | Every named canonical documentation and implementation surface | `scripts/test-consolidated-documentation-topology.sh` | `bash scripts/test-consolidated-documentation-topology.sh` |
| Assistants context routing | contract | Exact shared repo and IDS subtree; no retired fallback | `scripts/test-consolidated-documentation-topology.sh` | `bash scripts/test-consolidated-documentation-topology.sh` |
| Portal context routing | contract | Product docs, conditional IDS, API/Web ownership, and TLC boundary | `scripts/test-consolidated-documentation-topology.sh`, `scripts/test-portal-tlc-session-artifacts.sh` | `bash scripts/test-consolidated-documentation-topology.sh && bash scripts/test-portal-tlc-session-artifacts.sh` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After one topology surface | `bash scripts/test-consolidated-documentation-topology.sh` | Same command |
| Full | After Portal routing | `bash scripts/test-consolidated-documentation-topology.sh && bash scripts/test-portal-tlc-session-artifacts.sh` | Run sequentially as written |
| Build | Last task and feature validation | `bash scripts/test-workspace.sh` | Run sequentially; no coverage reduction |
| Diff integrity | Feature validation | `git diff --check <evidence-base>..<evidence-head>` | N/A |

## Execution Plan

### Phase 1: Workspace Authority

```text
T1
```

### Phase 2: Product Context Routing

```text
T1 -> T2 -> T3
```

## Task Breakdown

### T1: Record the Consolidated Workspace Topology

**What**: Update active workspace authority, setup, project navigation, and the decision log to use the consolidated documentation roots, with a focused contract for those surfaces.
**Where**: `AGENTS.md`, `README.md`, `projects/`, `.specs/STATE.md`, `scripts/test-consolidated-documentation-topology.sh`, `scripts/test-workspace.sh`, `.specs/features/consolidated-documentation-topology/`
**Depends on**: None
**Reuses**: AD-006/AD-008 project-pointer model and shell contract-test style
**Requirement**: CDT-01, CDT-02, CDT-03, CDT-07, CDT-08

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] AD-042 records the shared documentation repo and supersedes literal retired-repo routing decisions without rewriting historical evidence.
- [x] Registry and setup docs distinguish documentation roots from implementation repos and omit retired clone commands.
- [x] The focused contract asserts the exact operations, IDS, Portal docs, API, and Web surfaces.
- [x] The focused contract participates in the aggregate workspace gate.

**Tests**: contract
**Gate**: quick
**Commit**: `docs(workspace): adopt consolidated documentation topology`

### T2: Repoint Assistants IDS Context

**What**: Make Assistants task preparation resolve IDS contracts from the IDS subtree in `inventeer-ops`.
**Where**: `projects/assistants.md`, `.agents/skills/assistants-task-context/SKILL.md`, `.agents/skills/assistants-task-context/references/ids-context.md`, `scripts/test-consolidated-documentation-topology.sh`, `.specs/features/consolidated-documentation-topology/`
**Depends on**: T1
**Reuses**: Existing conditional IDS trigger and read-only contract boundary
**Requirement**: CDT-04, CDT-07

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] The skill requires `repos/inventeer-ops` only when IDS context is applicable and reads the root repo instructions before the IDS subtree.
- [x] The Assistants project pointer resolves all client and standard paths under `artifacts/products/ids/`.
- [x] The focused contract rejects standalone `repos/ids` references in every active Assistants surface.

**Tests**: contract
**Gate**: quick
**Commit**: `docs(assistants): repoint IDS context to operations`

### T3: Repoint Portal Product and IDS Context

**What**: Make Portal task preparation resolve product and IDS documentation from `inventeer-ops` while preserving API/Web ownership and the local TLC lifecycle.
**Where**: `.agents/skills/portal-task-context/`, `scripts/test-consolidated-documentation-topology.sh`, `scripts/test-portal-tlc-session-artifacts.sh`, `.specs/features/consolidated-documentation-topology/`, `.specs/STATE.md`
**Depends on**: T2
**Reuses**: Existing Portal ownership classification and AD-031/AD-036 session-artifact contract
**Requirement**: CDT-05, CDT-06, CDT-07

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Portal product meaning resolves from `artifacts/products/portal/` and conditional IDS context resolves from `artifacts/products/ids/` in the same shared repo.
- [x] Repository ownership still assigns runtime implementation only to `portal-api`, `portal-web`, or an explicit combination.
- [x] TLC working artifacts remain under `session-context/portal/<INV-ID>/` and are forbidden from both code repos and the Portal documentation subtree.
- [x] Focused and aggregate workspace gates pass with zero active standalone retired-root references.

**Tests**: contract
**Gate**: build
**Commit**: `docs(portal): repoint product context to operations`

## Phase Execution Map

```text
Phase 1 -> Phase 2

Phase 1: T1
Phase 2: T1 -> T2 -> T3
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | One workspace topology invariant | Registry contract and one revert | Granular |
| T2 | One Assistants dependency route | Assistants contract and one revert | Granular |
| T3 | One Portal dependency topology | Portal contracts and one revert | Granular |

## Diagram-Definition Cross-Check

| Task | Depends On | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | Entry point | Match |
| T2 | T1 | T1 -> T2 | Match |
| T3 | T2 | T2 -> T3 | Match |

## Test Co-location Validation

| Task | Layer Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Workspace authority and registry | contract | contract | OK |
| T2 | Assistants context routing | contract | contract | OK |
| T3 | Portal context routing | contract | contract | OK |
