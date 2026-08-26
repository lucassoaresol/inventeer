# Versioned Cycle Task Clarifications Specification

**Status:** Validated
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

Portal task clarification has accumulated useful decisions under ignored `session-context/`
directories. The durable task contract is currently lost across machines together with operational
handoffs, TLC state, logs, and review evidence that correctly remain ephemeral.

## Goals

- [x] Version the durable clarification record for each Portal task clarified during Cycle 10.
- [x] Organize records by cycle, product, and Linear issue without changing canonical authority.
- [x] Define a repeatable promotion boundary that excludes session and execution state.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Versioning `session-context/` | Runtime, TLC artifacts, logs, bundles, and local evidence remain ephemeral. |
| Copying raw clarification handoffs | They contain superseded chronology and machine-local context. |
| Replacing Linear or product repositories | Linear remains canonical for execution; product sources remain canonical for intent, code, tests, and decisions. |
| Updating Linear, GitHub, Figma, or product repositories | This feature changes only the personal engineering workspace. |
| Promoting TLC specs, designs, tasks, or validation | The durable layer is a clarification record, not a delivery artifact. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Primary hierarchy | `cycles/<number>/<product>/tasks/INV-<id>.md` | The user confirmed that each INV belongs inside the Cycle 10 folder. | y |
| Cross-cycle issues | A materially re-clarified issue receives a new snapshot in the later cycle | Cycle records preserve planning history; Linear still answers the current cycle. | y |
| Initial population | Cycle 10 Portal issues with durable clarification evidence, including the supporting foundation INV-3875 | These are the first real records and expose gaps in the contract before future use. | y |
| Promotion method | Curate conclusions, decisions, boundaries, and canonical sources instead of copying raw handoffs | This removes stale chronology and keeps the durable layer portable and safe. | y |
| Remaining implicit dimensions | Auth, concurrency, external calls, and customer-data lifecycle are N/A because this feature writes documentation only and performs no remote operation | The records describe existing contracts without executing them. | y |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: Preserve Clarification by Cycle

**User Story:** As the workspace maintainer, I want each clarified INV recorded under its planning
cycle so that the reasoning survives session cleanup and machine changes.

**Why P1:** The current durable value is coupled to a directory explicitly eligible for deletion.

**Acceptance Criteria:**

1. WHEN Cycle 10 clarification is promoted THEN the workspace SHALL store each task record under `cycles/10/portal/tasks/INV-<id>.md`. `CTC-01`
2. WHEN the Cycle 10 index is read THEN it SHALL identify every promoted INV and its clarification snapshot without requiring `session-context/`. `CTC-02`
3. WHEN a task record is read THEN it SHALL distinguish its historical snapshot from current Linear state and name the applicable canonical sources. `CTC-03`
4. WHEN the first population is complete THEN it SHALL include INV-3828, INV-3830, INV-3831, INV-3832, INV-3833, INV-3834, INV-3847, and INV-3875. `CTC-04`

**Independent Test:** A workspace contract test discovers the Cycle 10 index and asserts the exact
initial task set and required authority sections.

### P1: Preserve the Ephemeral Boundary

**User Story:** As an engineer resuming work, I want operational state to remain separate so that a
clarification record never masquerades as fresh execution evidence.

**Why P1:** Versioning stale TLC state, logs, or PR instructions would weaken the existing
freshness and ownership contracts.

**Acceptance Criteria:**

1. WHILE cycle task records are versioned the workspace SHALL continue to ignore all of `/session-context/`. `CTC-05`
2. WHEN a clarification handoff is promoted THEN the durable record SHALL omit session identifiers, runtime instructions, raw logs, credentials, customer data, and TLC execution state. `CTC-06`
3. IF a future task is materially re-clarified in another cycle THEN the workspace SHALL preserve the earlier cycle record and create a new cycle-scoped snapshot instead of moving or silently rewriting history. `CTC-07`
4. WHEN agents prepare or resume a task THEN workspace instructions SHALL require revalidation in Linear and canonical product sources rather than treating the cycle record as current execution authority. `CTC-08`

**Independent Test:** The contract test rejects missing ignore rules, forbidden operational markers,
missing lifecycle guidance, and task records that omit authority or freshness language.

## Edge Cases

- IF an issue has no durable clarification outcome THEN the cycle index SHALL NOT imply that a raw session directory is versioned. `CTC-09`
- WHEN a supporting task is created during clarification of another task THEN the cycle SHALL permit an independent INV record when its contract is independently identifiable. `CTC-10`

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| CTC-01 | Preserve by cycle | DECISION | User clarification that INVs belong inside folder 10 | Execute | Verified |
| CTC-02 | Preserve by cycle | ISSUE | Requested durable promotion of task clarification | Execute | Verified |
| CTC-03 | Preserve by cycle | INHERITED | AGENTS.md canonical-source boundaries | Execute | Verified |
| CTC-04 | Preserve by cycle | DECISION | Cycle 10 local clarification inventory | Execute | Verified |
| CTC-05 | Ephemeral boundary | ISSUE | User explicitly retained ignored session context | Execute | Verified |
| CTC-06 | Ephemeral boundary | SAFETY | Workspace security and AD-017/AD-045 | Execute | Verified |
| CTC-07 | Ephemeral boundary | DECISION | Cycle-scoped historical snapshot model | Execute | Verified |
| CTC-08 | Ephemeral boundary | INHERITED | Linear and product-source authority rules | Execute | Verified |
| CTC-09 | Edge case | SAFETY | Avoid implying durability where no curated record exists | Execute | Verified |
| CTC-10 | Edge case | DECISION | INV-3875 emerged as an independent Cycle 10 foundation task | Execute | Verified |

**Coverage:** 10 total, 10 mapped to the implicit execution plan, 0 unmapped.

## Success Criteria

- [x] Eight Cycle 10 Portal task clarification records are versioned and indexed.
- [x] No promoted record depends on an ignored local path to be understandable.
- [x] Workspace instructions and deterministic tests enforce authority, lifecycle, and safety boundaries.
- [x] The root workspace gate passes without modifying product repositories or existing user changes.
