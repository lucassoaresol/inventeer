# Workspace Session Resilience v2 Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: activate it by name and follow its Execute
flow and Critical Rules. The skill is the source of truth for per-task gates, atomic commits,
independent verification, and the discrimination sensor.

**Design:** inline in the approved specification; no new architecture or dependency is introduced.
**Status:** Done

## Test Coverage Matrix

> Generated from `AGENTS.md`, `scripts/test-workspace.sh`, neighboring Python and shell contract
> tests, confirmed lesson L-008, and the approved spec.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Agent security contract | contract | Every named handling and lifecycle boundary | `scripts/test-session-resilience-contract.sh` | `bash scripts/test-session-resilience-contract.sh` |
| Session auditor | unit/contract | 1:1 requirement and edge-case fixtures; preserve every APEX outcome | `scripts/test-session-history-audit.py` | `python3 scripts/test-session-history-audit.py` |
| Decision and pilot | contract | Every authority, privacy, eligibility, and closing threshold | `scripts/test-session-resilience-contract.sh` | `bash scripts/test-session-resilience-contract.sh` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After one contract surface | `bash scripts/test-session-resilience-contract.sh` or `python3 scripts/test-session-history-audit.py` | Same command |
| Full | After integrated session-resilience work | `bash scripts/test-session-resilience-contract.sh && python3 scripts/test-session-history-audit.py` | Run sequentially as written |
| Build | Last task and feature validation | `bash scripts/test-workspace.sh` | Run sequentially; no coverage reduction |
| Diff integrity | Feature validation | `git diff --check <evidence-base>..<evidence-head>` | N/A |

## Execution Plan

### Phase 1: Security Contract

```text
T1
```

### Phase 2: Reproducible Audit

```text
T1 -> T2
```

### Phase 3: Decision and Pilot

```text
T2 -> T3
```

## Task Breakdown

### T1: Contain Potential Secrets

**What**: Add and enforce the complete handling contract for potential secrets received in chat.
**Where**: `AGENTS.md`, `scripts/test-session-resilience-contract.sh`, `scripts/test-workspace.sh`,
`.specs/features/workspace-session-resilience-v2/spec.md`,
`.specs/features/workspace-session-resilience-v2/tasks.md`
**Depends on**: None
**Reuses**: Existing workspace security section and shell contract-test style
**Requirement**: WSR-01, WSR-02, WSR-03, WSR-04

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] `AGENTS.md` requires non-repetition, `[REDACTED]`, safe local input, containment, and
  conditional rotation.
- [x] The focused contract test passes five named assertions with no transcript access.
- [x] The aggregate workspace gate invokes the focused contract.

**Tests**: contract
**Gate**: quick
**Commit**: `docs(security): contain chat-provided secrets`

### T2: Version and Bound the Session Auditor

**What**: Add contract provenance, a closed optional time window, deduplicated interruption
concentration, and availability state without changing existing APEX outcome semantics.
**Where**: `scripts/audit-session-history.py`, `scripts/test-session-history-audit.py`,
`.specs/features/workspace-session-resilience-v2/spec.md`,
`.specs/features/workspace-session-resilience-v2/tasks.md`
**Depends on**: T1
**Reuses**: Current APEX outcome parser and EDREN's validated generic metadata model
**Requirement**: WSR-05, WSR-06, WSR-07, WSR-08, WSR-09, WSR-10, WSR-11, WSR-12

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] `--until` applies an exclusive upper bound to both engines and rejects invalid windows with
  exact diagnostics.
- [x] Contract version, normalized window, exclusions, availability, copies, aborts, compactations,
  affected-primary counts, percentages, and maxima match exact fixture assertions.
- [x] All prior APEX success, failure, denial, and unresolved assertions remain exact.
- [x] Missing roots, duplicate IDs, subagent-only events, malformed timestamps, and sensitive
  sentinels satisfy the spec.

**Tests**: unit/contract
**Gate**: quick
**Commit**: `feat(sessions): audit reproducible interruption cohorts`

### T3: Adopt the Bounded Workspace Pilot

**What**: Record AD-041, persist the workspace-specific aggregate baseline and pilot boundaries,
and enforce their lifecycle contract.
**Where**: `.specs/STATE.md`,
`.specs/features/workspace-session-resilience-v2/pilot.md`,
`AGENTS.md`,
`scripts/test-session-resilience-contract.sh`,
`.specs/features/workspace-session-resilience-v2/spec.md`,
`.specs/features/workspace-session-resilience-v2/tasks.md`
**Depends on**: T2
**Reuses**: AD-027/033 retrospective privacy model and AD-038/039 bounded-pilot pattern
**Requirement**: WSR-13, WSR-14, WSR-15

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] AD-041 records compatibility, privacy, closed-cohort, and bounded-pilot decisions.
- [x] The pilot records a v2 closed-window baseline with no identity or transcript path.
- [x] Eligibility, success measures, closing comparison, and automation thresholds are explicit.
- [x] The focused contract test and aggregate workspace gate pass.

**Tests**: contract
**Gate**: build
**Commit**: `docs(sessions): adopt bounded resilience pilot`

## Phase Execution Map

```text
Phase 1 -> Phase 2 -> Phase 3

T1 -> T2 -> T3
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | One security handling invariant | Contract phrases and one revert | Granular |
| T2 | One report-contract evolution | Auditor fixtures and one revert | Granular |
| T3 | One transversal adoption decision | Decision, pilot, and lifecycle contract | Granular |

## Diagram-Definition Cross-Check

| Task | Depends On | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | First task | Match |
| T2 | T1 | T1 -> T2 | Match |
| T3 | T2 | T2 -> T3 | Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Agent security contract | contract | contract | OK |
| T2 | Session auditor | unit/contract | unit/contract | OK |
| T3 | Decision and pilot | contract | contract | OK |
