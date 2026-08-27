# Workspace Operational Surface Simplification Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill and validate changed skill instructions with
`skill-creator`. TLC remains the execution source of truth.

**Design:** `.specs/features/workspace-operational-surface-simplification/design.md`
**Status:** Complete

## Test Coverage Matrix

> Generated from `AGENTS.md`, root scripts, existing contract tests, and confirmed lesson L-008.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Context manifest/planner | contract | All named routes, budgets, closed schema, metadata-only output | `scripts/test-workspace-context.py` | `python3 scripts/test-workspace-context.py` |
| Generated skill sync | integration | Selection, removal, idempotency, invalid catalog, boundary wording | `scripts/test-sync-apex-commands.sh` | `bash scripts/test-sync-apex-commands.sh` |
| Hygiene inventory | unit/integration | Status combinations, sanitization, invalid input, non-mutation | `scripts/test-workspace-hygiene.py` | `python3 scripts/test-workspace-hygiene.py` |
| MCP configuration | contract | Both engines, exact pin/address/port/activation/approval boundaries | `scripts/test-mcp-config.py` | `python3 scripts/test-mcp-config.py` |
| Documentation/decisions | contract | Named boundaries and lifecycle statements | existing root contract tests | focal tests plus aggregate gate |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | Per task | Relevant focal command from matrix | Same command |
| Full | Increment terminal gate | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | Sequential execution selected after resource preflight |
| Build | Skill/config structure | Skill quick validator plus root aggregate gate | Same commands |
| Diff integrity | Feature validation | `git diff --check <evidence-base>..<evidence-head>` plus uncommitted surfaces | N/A |

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | Workspace exposes bounded discovery, one APEX inspector, read-only hygiene, and an opt-in local Figma pilot | WOSS-01..09 | T1, T2, T3, T4, T5 | Full | Revert the single workspace behavior commit | `feat(workspace): simplify operational surfaces` |

## Execution Plan

### Phase 1: Context and diagnostics

```text
T1 → T2
```

### Phase 2: Hygiene and pilot

```text
T3 → T4
```

### Phase 3: Durable contract

```text
T5
```

## Task Breakdown

### T1: Bound project discovery

**What:** Add and enforce a deterministic `project-discovery` context route and read-only freshness workflow.
**Where:** `.specs/context/routes.json`
**Depends on:** None
**Reuses:** Existing route manifest and planner schema
**Requirement:** WOSS-01, WOSS-02, WOSS-09
**Value Increment:** VI-001
**Tools:** apply_patch, shell; skills `tlc-spec-driven`, `skill-creator`
**Done when:** Six routes pass, discovery plans before source loading, and repo synchronization requires separate authorization.
**Tests:** contract
**Gate:** quick

### T2: Collapse APEX wrapper discovery

**What:** Keep one aggregate APEX inspector and make synchronization reconcile only that inspector.
**Where:** `scripts/sync-apex-commands.sh`
**Depends on:** T1
**Reuses:** Existing `apex-all-tools` wrapper and catalog contract
**Requirement:** WOSS-03
**Value Increment:** VI-001
**Tools:** apply_patch, shell; skills `tlc-spec-driven`, `skill-creator`
**Done when:** Exactly one APEX skill remains, sync is idempotent, and missing `all-tools` fails closed.
**Tests:** integration
**Gate:** quick

### T3: Add sanitized hygiene inventory

**What:** Add a report-only inventory for lesson status and ephemeral lifecycle evidence.
**Where:** `scripts/workspace-hygiene.py`
**Depends on:** T2
**Reuses:** `.specs/lessons.json` schema and `session-context/` lifecycle rules
**Requirement:** WOSS-04, WOSS-05
**Value Increment:** VI-001
**Tools:** apply_patch, shell; skill `tlc-spec-driven`
**Done when:** Fixture tests cover eligibility conjunctions, sanitization, invalid input, symlinks, and byte-identical non-mutation.
**Tests:** unit/integration
**Gate:** quick

### T4: Register the local Figma pilot

**What:** Add the pinned, loopback, opt-in server beside the official server and document its manual dependency.
**Where:** `.codex/config.toml`
**Depends on:** T3
**Reuses:** Existing Figma OAuth integration and MCP approval tests
**Requirement:** WOSS-06, WOSS-07, WOSS-08
**Value Increment:** VI-001
**Tools:** apply_patch, shell; skills `tlc-spec-driven`, `skill-creator`
**Done when:** Both configs use the exact pin and loopback flags, Codex keeps the pilot disabled with prompt approval, Claude does not auto-enable it, and official Figma remains unchanged.
**Tests:** contract
**Gate:** quick

### T5: Close the durable workspace contract

**What:** Record one transversal decision, update indexes/routing documentation, validate all skill folders, and run the aggregate gate.
**Where:** `.specs/STATE.md`
**Depends on:** T3, T4
**Reuses:** Existing decision, feature index, Handoff, and gate evidence contracts
**Requirement:** WOSS-01, WOSS-02, WOSS-03, WOSS-04, WOSS-05, WOSS-06, WOSS-07, WOSS-08, WOSS-09
**Value Increment:** VI-001
**Tools:** apply_patch, shell; skills `tlc-spec-driven`, `skill-creator`
**Done when:** Traceability is verified, all focal and aggregate gates pass, and the user's lesson changes remain untouched.
**Tests:** contract
**Gate:** full

## Phase Execution Map

```text
Phase 1: T1 → T2
Phase 2: T3 → T4
Phase 3: T5

T2 → T3
T3 → T5
T4 → T5
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | One context route | Context focal gate | Granular |
| T2 | One skill-discovery invariant | Sync focal gate | Granular |
| T3 | One read-only inventory | Hygiene focal gate | Granular |
| T4 | One opt-in external integration | MCP focal gate | Granular |
| T5 | One durable closure | Aggregate gate | Granular |

## Execution Status

| Task | Status | Evidence |
| --- | --- | --- |
| T1 | Complete | Context suite: 11 groups passed; discovery skill valid |
| T2 | Complete | APEX sync suite: 16 groups passed; aggregate inspector valid |
| T3 | Complete | Hygiene suite: 3 groups passed; real inventory made no mutation |
| T4 | Complete | MCP suite: 16 groups passed; official and pilot boundaries verified |
| T5 | Complete | Decision, indexes and docs updated; aggregate workspace gate passed |

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | Start | Match |
| T2 | T1 | T1 → T2 | Match |
| T3 | T2 | T2 → T3 | Match |
| T4 | T3 | T3 → T4 | Match |
| T5 | T3, T4 | T3 → T5 and T4 → T5 | Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Context manifest/planner | contract | contract | OK |
| T2 | Generated skill sync | integration | integration | OK |
| T3 | Hygiene inventory | unit/integration | unit/integration | OK |
| T4 | MCP configuration | contract | contract | OK |
| T5 | Documentation/decisions | contract | contract | OK |
