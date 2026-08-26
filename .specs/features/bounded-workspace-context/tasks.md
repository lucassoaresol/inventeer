# Bounded Workspace Context Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement with `tlc-spec-driven`. All tasks execute serially in one Value Increment; the terminal
workspace gate authorizes the single local commit.

**Status:** Complete

## Test Coverage Matrix

> Generated from `AGENTS.md`, `scripts/test-workspace.sh`, existing context fixtures, and confirmed
> lesson L-008.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Context manifest and Markdown selector | unit/contract | Every named route, exact estimator/budget schema, whole-file and heading boundaries | `scripts/test-workspace-context.py` | `python3 scripts/test-workspace-context.py` |
| Context CLI and privacy boundary | integration | Plan, measure, all-route check, adjacent budget outcomes, exit codes, stable metadata-only output, and no mutation | `scripts/test-workspace-context.py` | `python3 scripts/test-workspace-context.py` |
| Workspace navigation and operator contract | contract | Decision/feature index completeness, documentation, Python syntax, and root integration | `scripts/test-workspace-structure.py`, `scripts/test-workspace.sh` | `python3 scripts/test-workspace-structure.py && bash scripts/test-workspace.sh` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After planner or manifest changes | `python3 scripts/test-workspace-context.py` | N/A |
| Full | After workspace contract integration | `python3 scripts/test-workspace-context.py && python3 scripts/test-workspace-structure.py` | Same commands, sequentially |
| Build | VI-001 terminal gate | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | Run sequentially after `./scripts/check-machine-resources.sh`; no coverage reduction |
| Diff integrity | Feature validation | `git diff --check 7474992..<evidence-head>` plus `git diff --check` for retained dirty paths | N/A |

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | Every workspace route has deterministic heading selection, measurement, and an enforceable context budget without content disclosure. | BWC-01..11 | T1, T2, T3, T4 | Build | Revert planner schema, tests, documentation, and AD-048 together without changing product repositories. | `feat(context): enforce workspace context budgets` |

## Execution Plan

### Phase 1: Bounded context contract

```text
T1 -> T2 -> T3 -> T4
```

## Task Breakdown

### T1: Specify the versioned budget manifest

**What:** Upgrade the five canonical routes to an exact estimator, positive route budget, and explicit heading-list schema.
**Where:** `.specs/context/routes.json`, `scripts/test-workspace-context.py`
**Depends on:** None
**Reuses:** Existing route order, source references, reasons, gates, and L-008
**Requirement:** BWC-05, BWC-06, BWC-08
**Value Increment:** VI-001

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] Manifest version 2 defines one code-point estimator and a 20,000-token budget per route.
- [x] Every reference has an explicit, unique headings list.
- [x] All five named routes and all hostile schema fixtures are asserted.
- [x] Quick gate passes without deleting existing coverage.

**Tests:** unit/contract
**Gate:** quick

### T2: Add deterministic selection, measurement, and checks

**What:** Implement Markdown section selection plus content-free `plan`, `measure`, and `check` reports with distinct budget and contract exits.
**Where:** `scripts/workspace-context.py`, `scripts/test-workspace-context.py`
**Depends on:** T1
**Reuses:** Existing safe path resolver, closed-schema validation, JSON CLI, and EDREN estimator semantics
**Requirement:** BWC-01..07, BWC-09..11
**Value Increment:** VI-001

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] Whole files and exact Markdown sections produce deterministic code-point and rounded token totals.
- [x] `plan`, `measure`, and `check` never emit selected content or physical root paths.
- [x] Adjacent budget boundaries return pass/0 and fail/1; malformed contracts return 2.
- [x] Mixed all-route checks report all five routes before returning 1.
- [x] Quick gate passes without deleting existing coverage.

**Tests:** unit/contract
**Gate:** quick

### T3: Adopt the bounded context contract

**What:** Record AD-048, document the operator commands, index the feature, and close the integrated workspace contract.
**Where:** `.specs/STATE.md`, `.specs/DECISIONS.md`, `.specs/features/INDEX.md`, `AGENTS.md`, `README.md`, `.specs/features/bounded-workspace-context/`
**Depends on:** T2
**Reuses:** AD-044, AD-046, AD-047, root gate evidence, and workspace indexes
**Requirement:** BWC-01..11
**Value Increment:** VI-001

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] AD-048 makes bounded measurement the entry contract without changing product ownership.
- [x] README and AGENTS document `plan`, `measure`, and `check` and their exit semantics.
- [x] Feature and decision indexes remain complete.
- [x] Preexisting lesson changes remain outside the Value Increment.
- [x] Full focal checks and the resource-aware Build gate pass.

**Tests:** contract
**Gate:** build

### T4: Close selected-route and adjacent-heading validation gaps

**What:** Make an oversized selected measurement return exit 1 and add direct evidence for adjacent selected headings.
**Where:** `scripts/workspace-context.py`, `scripts/test-workspace-context.py`
**Depends on:** T3
**Reuses:** Verifier findings for BWC-04 and BWC-10
**Requirement:** BWC-04, BWC-10
**Value Increment:** VI-001

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] An oversized `measure --route` emits bounded fail metadata and returns exit 1.
- [x] Two adjacent selected headings have exact character and token assertions with no synthetic separator.
- [x] The focused and terminal gates pass before the local increment is amended.

**Tests:** unit/contract
**Gate:** build

## Phase Execution Map

```text
Phase 1
T1 -> T2 -> T3 -> T4
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | One manifest schema | Schema fixtures and manifest revert | PASS |
| T2 | One measurement capability | Planner fixtures and planner revert | PASS |
| T3 | One workspace adoption | Index/operator contracts and adoption revert | PASS |
| T4 | One verifier-gap correction | Selected exit and adjacency fixtures | PASS |

## Diagram-Definition Cross-Check

| Task | Depends On | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | Start | PASS |
| T2 | T1 | T1 -> T2 | PASS |
| T3 | T2 | T2 -> T3 | PASS |
| T4 | T3 | T3 -> T4 | PASS |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Manifest/schema | unit/contract | unit/contract | PASS |
| T2 | Planner/CLI | unit/contract | unit/contract | PASS |
| T3 | Workspace integration | contract | contract | PASS |
| T4 | Planner/CLI correction | unit/contract | unit/contract | PASS |
