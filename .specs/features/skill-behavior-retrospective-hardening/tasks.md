# Skill Behavior Retrospective Hardening Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute
flow and Critical Rules.** Use `skill-creator` for T6. The user's approval to proceed selected these
skills and local filesystem/shell tools; no MCP is required for this workspace-only implementation.

**If either required skill cannot be activated, STOP and report the unavailable capability.**

**Design**: `.specs/features/skill-behavior-retrospective-hardening/design.md`
**Status**: Approved

## Test Coverage Matrix

> Generated from `AGENTS.md`, `scripts/test-workspace.sh`, adjacent Python/shell suites, and the spec.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| TLC deterministic gates | unit/contract | Every provenance mode, missing field, placeholder, historical compatibility, and exit path | `scripts/test-tlc-deterministic-gates.py` | `python3 scripts/test-tlc-deterministic-gates.py` |
| TLC lessons store | unit | Every pattern-key validation, match precedence, distinct-feature promotion, legacy path, and unchanged-on-error branch | `.agents/skills/tlc-spec-driven/scripts/test-lessons.py` | `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` |
| Review materializer | integration | Valid exact checkout, detached head, base presence, invalid SHA/source/destination, and source porcelain preservation | `.agents/skills/review-pull-request/scripts/test-materialize-review-head.sh` | `bash .agents/skills/review-pull-request/scripts/test-materialize-review-head.sh` |
| Review ledger/workflow | unit/contract | Schema-v1 compatibility and every schema-v2 state/reason/head invariant | `scripts/test-pr-review-*.py` | `python3 scripts/test-pr-review-pilot.py && python3 scripts/test-pr-review-workflow.py` |
| Session auditor | integration | Both formats, exclusions, decoys, supported zero, unsupported null, receipt privacy, and structured skill names | `scripts/test-session-history-audit.py` | `python3 scripts/test-session-history-audit.py` |
| Skill structure and engine surface | contract | Frontmatter, discriminating routing, Codex manifest, Claude symlink, dependencies, and referenced paths | `scripts/test-skill-engine-parity.py` | `python3 scripts/test-skill-engine-parity.py` |
| Governance/artifacts | contract | Active decision, feature lifecycle, privacy boundary, and aggregate inclusion | `scripts/test-workspace-structure.py` | `python3 scripts/test-workspace-structure.py` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After each task | The task's matrix command | Same; suites are bounded and single-process |
| Full | After each Value Increment | Relevant quick commands plus `git diff --check` | Same |
| Build | After T7 and before Verifier | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | Helper owns the complete workspace recipe; reduce concurrency, never coverage |
| Diff integrity | Feature validation | `git diff --check 2b6d00f..HEAD` plus staged/unstaged checks when present | N/A |

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | TLC completion distinguishes independent verification from unsupported fallback | SBRH-01, SBRH-02 | T1 | Full | Revert provenance schema, guidance, and its tests together | `feat(tlc): require verifier provenance` |
| VI-002 | Future lesson observations recur through a safe semantic identity | SBRH-03, SBRH-04 | T2 | Full | Revert pattern-key CLI/store behavior and guidance together | `feat(tlc): identify lesson patterns explicitly` |
| VI-003 | PR reviews can materialize and record exact-head local evidence | SBRH-05..07 | T3, T4 | Full | Revert review materializer, ledger v2, and promotion decision together | `feat(review): bind local validation to pull request heads` |
| VI-004 | Dual-engine retrospectives use sanitized structured skill evidence | SBRH-08..12 | T5, T6, T7 | Build | Revert audit v5, retrospective skill, and adoption decision together | `feat(workspace): add skill usage retrospectives` |

## Execution Plan

Phases run sequentially and tasks within each phase run in order.

### Phase 1: TLC evidence integrity

```text
T1 -> T2
```

### Phase 2: Review evidence binding

```text
T2 -> T3 -> T4
```

### Phase 3: Retrospective capability

```text
T4 -> T5 -> T6 -> T7
```

## Task Breakdown

### T1: Enforce Verifier provenance

**What**: Extend TLC completion evidence with deterministic independent-agent and standalone-fallback contracts while preserving historical cross-check compatibility.
**Where**: `.agents/skills/tlc-spec-driven/`
**Depends on**: None
**Reuses**: Existing `validate_state.py`, validation guidance, and deterministic gate fixtures
**Requirement**: SBRH-01, SBRH-02
**Value Increment**: VI-001

**Tools**:

- Local: `apply_patch`, Python
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Explicit active-feature PASS requires a valid mode and its mode-specific evidence.
- [x] Missing, placeholder, contradictory, and unsupported fallback fixtures fail.
- [x] Historical workspace cross-check remains green without rewriting old reports.
- [x] `python3 scripts/test-tlc-deterministic-gates.py` passes with its expected count intact or increased.

**Tests**: unit/contract
**Gate**: quick

### T2: Add semantic lesson pattern keys

**What**: Require and persist bounded pattern keys for new lessons, match them before legacy heuristics, and document the new distillation input.
**Where**: `.agents/skills/tlc-spec-driven/`
**Depends on**: T1
**Reuses**: Existing distinct-feature recurrence, normalization, calibrated similarity, and renderer
**Requirement**: SBRH-03, SBRH-04
**Value Increment**: VI-002

**Tools**:

- Local: `apply_patch`, Python
- Skill: `tlc-spec-driven`

**Done when**:

- [x] New `add` calls require a safe kebab-case key and persist it.
- [x] Same signal/key across distinct features promotes independently of text.
- [x] Cross-signal, malformed, legacy, and error atomicity paths are tested.
- [x] `python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py` passes.

**Tests**: unit
**Gate**: quick

### T3: Materialize an exact PR review surface

**What**: Add a review-owned helper that clones an authorized source into an explicit empty destination, verifies exact base/head commits, and detaches at head without changing source state.
**Where**: `.agents/skills/review-pull-request/scripts/`
**Depends on**: T2
**Reuses**: Git plumbing and the review skill's existing base/head identity contract
**Requirement**: SBRH-05
**Value Increment**: VI-003

**Tools**:

- Local: `apply_patch`, Bash, Git
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Valid local fixtures materialize both commits and detached head.
- [x] Invalid source, destination, and SHA cases fail before success output.
- [x] Source worktree status and HEAD remain unchanged.
- [x] `bash .agents/skills/review-pull-request/scripts/test-materialize-review-head.sh` passes.

**Tests**: integration
**Gate**: quick

### T4: Promote and version review evidence

**What**: Add schema-v2 local-validation binding and state-compatible reason enums, preserve schema-v1 summaries, and update the review contract and pilot decision from the nine-record evidence.
**Where**: `scripts/pr-review-pilot.py`
**Depends on**: T3
**Reuses**: Existing closed-schema validator, sanitized summary, skill contract, and AD-038/AD-039 evidence
**Requirement**: SBRH-06, SBRH-07
**Value Increment**: VI-003

**Tools**:

- Local: `apply_patch`, Python
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Schema-v2 states enforce exact final-head binding or a state-compatible sanitized reason.
- [x] Existing schema-v1 ledger and summary remain valid.
- [x] Review instructions use the materializer only when local validation is decision-relevant.
- [x] The active decision records pilot promotion and the remaining limitation.
- [x] Both PR review Python suites pass.

**Tests**: unit/contract
**Gate**: full

### T5: Measure structured skill evidence

**What**: Evolve the session auditor to a v5 contract with structured Claude invocations, conservative path-load proxies, and unsupported Codex invocation semantics.
**Where**: `scripts/audit-session-history.py`
**Depends on**: T4
**Reuses**: Existing cohort filtering, exclusions, engine blocks, receipt hashing, and null semantics
**Requirement**: SBRH-08, SBRH-09, SBRH-10, SBRH-12
**Value Increment**: VI-004

**Tools**:

- Local: `apply_patch`, Python
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Claude `Skill` calls aggregate by validated name and distinct accepted session.
- [x] Codex invocation fields are null with a reason, never inferred zero.
- [x] Exact path proxies are separately named and decoy prose/output never counts.
- [x] Exclusions, empty roots, receipt privacy, and canonical engine keys remain tested.
- [x] `python3 scripts/test-session-history-audit.py` passes.

**Tests**: integration
**Gate**: quick

### T6: Create the retrospective skill

**What**: Create one focused, read-only skill with Codex metadata and Claude exposure for sanitized opportunity-aware skill retrospectives.
**Where**: `.agents/skills/retrospect-skill-usage/`
**Depends on**: T5
**Reuses**: `audit-session-history.py`, AD-027/AD-046 privacy, and existing skill surface conventions
**Requirement**: SBRH-11, SBRH-12
**Value Increment**: VI-004

**Tools**:

- Local: `apply_patch`, skill validator
- Skill: `skill-creator`, `tlc-spec-driven`

**Done when**:

- [x] Description routes retrospectives and excludes product discovery, PR review, and implementation.
- [x] Workflow requires closed bounds, current-session exclusion, limitations, opportunity checks, and chat-only output.
- [x] `agents/openai.yaml` names `$retrospect-skill-usage` and the Claude relative symlink resolves.
- [x] Quick validation and `python3 scripts/test-skill-engine-parity.py` pass.

**Tests**: contract
**Gate**: quick

### T7: Adopt the retrospective contract

**What**: Record the transversal decision, expose the new route in workspace instructions, complete feature traceability, and include all new tests in the aggregate gate.
**Where**: `.specs/STATE.md`
**Depends on**: T6
**Reuses**: AD-027/033/038/046, feature index, workspace test runner, and Handoff helper
**Requirement**: SBRH-07, SBRH-11, SBRH-12
**Value Increment**: VI-004

**Tools**:

- Local: `apply_patch`, workspace helpers
- Skill: `tlc-spec-driven`

**Done when**:

- [x] AD-053 records Verifier, lesson, review-pilot, and retrospective boundaries without expanding product authority.
- [x] Workspace instructions route future skill/session retrospectives to the new skill.
- [x] Feature status and requirement traceability reflect implemented state before verification.
- [x] Aggregate runner includes the materializer test and all structural suites pass focally.

**Tests**: contract
**Gate**: build

## Phase Execution Map

```text
Phase 1: T1 -> T2
                 \
Phase 2:          -> T3 -> T4
                              \
Phase 3:                       -> T5 -> T6 -> T7
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | Verifier completion invariant | TLC gate plus fixtures | Granular |
| T2 | Lesson semantic identity | Store behavior plus fixtures | Granular |
| T3 | Exact checkout materialization | One helper plus integration fixture | Granular |
| T4 | Review evidence representation | Ledger/workflow/promotion as one pilot closure | Granular |
| T5 | Engine-aware audit measurement | Auditor contract plus fixtures | Granular |
| T6 | New skill surface | One skill exposed to both engines | Granular |
| T7 | Transversal adoption | One decision and aggregate contract | Granular |

## Diagram-Definition Cross-Check

| Task | Depends On | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | Start | Match |
| T2 | T1 | T1 -> T2 | Match |
| T3 | T2 | T2 -> T3 | Match |
| T4 | T3 | T3 -> T4 | Match |
| T5 | T4 | T4 -> T5 | Match |
| T6 | T5 | T5 -> T6 | Match |
| T7 | T6 | T6 -> T7 | Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | TLC deterministic gate | unit/contract | unit/contract | OK |
| T2 | Lessons store | unit | unit | OK |
| T3 | Git materializer | integration | integration | OK |
| T4 | Review ledger/workflow | unit/contract | unit/contract | OK |
| T5 | Session auditor | integration | integration | OK |
| T6 | Skill metadata/surface | contract | contract | OK |
| T7 | Governance/aggregate | contract | contract | OK |
