# Workspace Process Hardening Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: activate it by name and follow its Execute
flow and Critical Rules. The skill is the source of truth for per-task gates, atomic commits,
independent verification, and the discrimination sensor.

**Design:** `.specs/features/workspace-process-hardening/design.md`
**Status:** Approved

## Test Coverage Matrix

> Generated from `AGENTS.md`, `scripts/test-workspace.sh`, existing Python and shell contract tests,
> and confirmed lesson L-008.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Pilot and decision lifecycle | contract | Every aggregate, privacy, trigger, limitation, and authority boundary | `scripts/test-session-resilience-contract.sh` | `bash scripts/test-session-resilience-contract.sh` |
| Context manifest and indexes | unit/contract | Every route, field, reference, invalid input, and completeness boundary | `scripts/test-workspace-context.py`, `scripts/test-workspace-structure.py` | `python3 scripts/test-workspace-context.py && python3 scripts/test-workspace-structure.py` |
| Staged-content guard and hook | integration | Safe path plus every forbidden signal, failure path, idempotency, and no-mutation invariant | `scripts/test-staged-content-guard.py` | `python3 scripts/test-staged-content-guard.py` |
| Portal checkpoint | unit/contract | Every event and existing input/path/atomicity boundary | `scripts/test-tlc-checkpoint.py`, `scripts/test-tlc-checkpoint-contract.sh` | `python3 scripts/test-tlc-checkpoint.py && bash scripts/test-tlc-checkpoint-contract.sh` |
| Root gate evidence | unit/integration | Pass, fail, invalidation, corruption, permissions, atomicity, privacy, and state-race outcomes | `scripts/test-workspace-gate-evidence.py` | `python3 scripts/test-workspace-gate-evidence.py` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After one focused component | The task-specific command from the coverage matrix | Same command |
| Full | After integrated mechanism changes | All focused commands for completed tasks, sequentially | Same commands, sequentially |
| Build | Last task and feature validation | `bash scripts/test-workspace.sh` | Run sequentially after `./scripts/check-machine-resources.sh`; no coverage reduction |
| Diff integrity | Feature validation | `git diff --check 2745409..HEAD` plus `git diff --check` for the retained dirty surface | N/A |

## Execution Plan

### Phase 1: Evidence Boundary

```text
T1
```

### Phase 2: Preventive Controls

```text
T1 -> T2 -> T3
```

### Phase 3: Recovery Controls

```text
T3 -> T4 -> T5
```

## Task Breakdown

### T1: Close the Bounded Resilience Pilot

**What:** Record the exact closing comparison, limitations, trigger outcome, and scoped automation decision.
**Where:** `.specs/features/workspace-session-resilience-v2/pilot.md`, `.specs/STATE.md`,
`scripts/test-session-resilience-contract.sh`, `.specs/features/workspace-process-hardening/spec.md`,
`.specs/features/workspace-process-hardening/tasks.md`
**Depends on:** None
**Reuses:** Auditor v2 output, AD-041, and the existing lifecycle contract
**Requirement:** WPH-01, WPH-02, WPH-03

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] The pilot is closed with the exact post-baseline window and aggregate results.
- [x] The report states diagnostic improvements and every unmeasured success dimension.
- [x] The next decision closes AD-041's pilot without authorizing product-repository automation.
- [x] The focused lifecycle contract passes all named assertions.

**Tests:** contract
**Gate:** quick
**Commit:** `docs(process): close resilience pilot`

### T2: Add Deterministic Context Routing

**What:** Add complete feature/decision indexes and a closed-schema reference-only planner for five workflow routes.
**Where:** `.specs/features/INDEX.md`, `.specs/DECISIONS.md`, `.specs/context/routes.json`,
`scripts/workspace-context.py`, `scripts/test-workspace-context.py`,
`scripts/test-workspace-structure.py`, `scripts/test-workspace.sh`,
`.specs/features/workspace-process-hardening/spec.md`,
`.specs/features/workspace-process-hardening/tasks.md`
**Depends on:** T1
**Reuses:** Project pointers, skill entrypoints, existing Markdown-link validation, EDREN reference-only package model
**Requirement:** WPH-04, WPH-05, WPH-06, WPH-07, WPH-18

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] Exactly five supported routes produce byte-stable metadata-only plans.
- [x] Unknown fields/routes, duplicate or unsafe references, and missing paths fail closed.
- [x] Feature and decision indexes cover every canonical entry and point back to canonical sources.
- [x] Focused context and structure gates pass with no broken links.

**Tests:** unit/contract
**Gate:** quick
**Commit:** `feat(context): add deterministic workspace routes`

### T3: Add the Opt-in Staged Content Guard

**What:** Version a staged-index safety checker, an opt-in hook installer, and the hook entrypoint.
**Where:** `scripts/check-staged-content.py`, `scripts/install-git-hooks.sh`,
`scripts/test-staged-content-guard.py`, `.githooks/pre-commit`, `README.md`,
`scripts/test-workspace.sh`, `.specs/features/workspace-process-hardening/spec.md`,
`.specs/features/workspace-process-hardening/tasks.md`
**Depends on:** T2
**Reuses:** Existing security policy, Git plumbing, and EDREN opt-in hook lifecycle
**Requirement:** WPH-08, WPH-09, WPH-10, WPH-11

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [x] Safe staged text passes without index or worktree mutation.
- [x] Every forbidden path, content, binary, size, Git failure, and unsafe-name fixture fails closed with path-only diagnostics.
- [x] Explicit installation changes only `core.hooksPath` and is idempotent.
- [x] The focused integration gate passes and the root gate includes it.

**Tests:** integration
**Gate:** quick
**Commit:** `feat(security): guard staged workspace content`

### T4: Require Pre-heavy Portal Checkpoints

**What:** Extend the Portal Codex TLC checkpoint lifecycle with a sanitized `pre-heavy` event and exact policy assertions.
**Where:** `scripts/update-tlc-checkpoint.py`, `scripts/test-tlc-checkpoint.py`,
`scripts/test-tlc-checkpoint-contract.sh`, `AGENTS.md`, `README.md`,
`.specs/features/workspace-process-hardening/spec.md`,
`.specs/features/workspace-process-hardening/tasks.md`
**Depends on:** T3
**Reuses:** AD-036 checkpoint path, schema, validation, and atomic writer
**Requirement:** WPH-12, WPH-13

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [ ] `pre-heavy` renders the existing handoff schema and preserves decisions and following sections.
- [ ] All existing invalid enums, multiline input, path escape, symlink, no-op, and atomic failure checks remain green.
- [ ] Workspace instructions require freshness before heavy stages without widening the Portal-only route.
- [ ] Focused checkpoint gates pass.

**Tests:** unit/contract
**Gate:** quick
**Commit:** `feat(checkpoint): add pre-heavy transition`

### T5: Preserve Root Gate Evidence

**What:** Add the allowlisted root gate runner and same-state status contract with a sanitized ignored receipt.
**Where:** `scripts/workspace-gate-evidence.py`, `scripts/test-workspace-gate-evidence.py`,
`AGENTS.md`, `README.md`, `scripts/test-workspace.sh`,
`.specs/features/workspace-process-hardening/spec.md`,
`.specs/features/workspace-process-hardening/tasks.md`
**Depends on:** T4
**Reuses:** `scripts/check-machine-resources.sh`, `scripts/test-workspace.sh`, atomic-write patterns, and EDREN receipt semantics
**Requirement:** WPH-14, WPH-15, WPH-16, WPH-17, WPH-19, WPH-20, WPH-21

**Tools:**

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when:**

- [ ] The runner persists the closed receipt schema for pass, fail, interruption, and changed-state outcomes.
- [ ] Status is reusable only for an identical successful profile, state, contract, schema, path, and permission set.
- [ ] A newer failure invalidates an older success and every malformed or unsafe store fails closed.
- [ ] Focused evidence tests and the resource-aware root Build gate pass.

**Tests:** unit/integration
**Gate:** build
**Commit:** `feat(gates): preserve root workspace evidence`

## Phase Execution Map

```text
Phase 1 -> Phase 2 -> Phase 3

T1 -> T2 -> T3 -> T4 -> T5
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | One pilot-closing decision | Cohort lifecycle contract | Granular |
| T2 | One context-routing capability | Manifest and index contract | Granular |
| T3 | One staged-index safety boundary | Temporary Git repository integration | Granular |
| T4 | One checkpoint transition | Existing checkpoint fixture suite | Granular |
| T5 | One root-gate evidence lifecycle | Receipt and status fixture suite | Granular |

## Diagram-Definition Cross-Check

| Task | Depends On | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | First task | Match |
| T2 | T1 | T1 -> T2 | Match |
| T3 | T2 | T2 -> T3 | Match |
| T4 | T3 | T3 -> T4 | Match |
| T5 | T4 | T4 -> T5 | Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Pilot and decision lifecycle | contract | contract | OK |
| T2 | Context manifest and indexes | unit/contract | unit/contract | OK |
| T3 | Staged-content guard and hook | integration | integration | OK |
| T4 | Portal checkpoint | unit/contract | unit/contract | OK |
| T5 | Root gate evidence | unit/integration | unit/integration | OK |
