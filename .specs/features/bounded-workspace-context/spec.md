# Bounded Workspace Context Specification

**Status:** Validated
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The workspace routes canonical sources deterministically, but the planner cannot quantify the
selected context or reject an oversized route. Recent sessions still compact frequently, so route
metadata needs enforceable heading selection and a bounded, content-free measurement contract.

## Goals

- [x] Measure every supported route with deterministic per-source and total estimates.
- [x] Reject routes whose selected context exceeds their declared budget.
- [x] Preserve metadata-only output and the existing ownership and path boundaries.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Loading or emitting selected source content | Canonical sources remain read directly by the active workflow. |
| RAG, embeddings, caches, or transcript indexing | The feature is a local deterministic planner, not a knowledge store. |
| Product-repository context manifests | Each product repository owns its code, tests, and local workflow. |
| Checkpoint-policy or gate-telemetry changes | Those are separate Value Increments with independent evidence. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Estimator | One estimated token per four Unicode code points, rounded up | The rule is deterministic, conservative, dependency-free, and already proven in EDREN. | y |
| Route budget | 20,000 estimated tokens for each supported task route | It matches the TLC task-context target and keeps current routes viable. | y |
| Heading selection | A heading selects its line and body through the next heading of the same or higher level | This matches Markdown section semantics and avoids copied snapshots. | y |
| Whole-file selection | An empty headings list measures the complete source | Some skill entrypoints are intentionally consumed as a whole. | y |
| Existing dirty changes | Preserve `.specs/LESSONS.md` and `.specs/lessons.json` outside this increment | The changes predate this feature and belong to the user. | y |
| Remaining implicit dimensions | Auth, concurrency, external calls, persistence, and customer-data lifecycle are N/A because the planner is local, read-only, and metadata-only | No remote or product-data boundary is added. | y |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: Measure Bounded Route Context

**User Story:** As an agent selecting a workspace route, I want a deterministic size report so that
I can load the intended sources without silently exhausting the session context.

**Why P1:** Context compaction remains a recurring source of session reconstruction.

**Acceptance Criteria:**

1. WHEN a supported route is planned THEN the planner SHALL emit its ordered metadata, declared budget, and estimator without source content. `BWC-01`
2. WHEN a supported route is measured THEN the planner SHALL emit each selected source's code-point count and rounded-up token estimate plus exact route totals and pass status. `BWC-02`
3. WHEN all supported routes are checked within their budgets THEN the planner SHALL report five passing routes and exit with code 0. `BWC-03`
4. IF a selected route exceeds its declared budget THEN the planner SHALL report only bounded source contributions, return fail status, and exit with code 1. `BWC-04`

**Independent Test:** Fixture manifests measure exact whole-file and heading-selected character counts,
then prove the same route passes and fails at adjacent budget boundaries.

### P1: Preserve Closed Context Boundaries

**User Story:** As the workspace maintainer, I want heading and manifest failures to remain closed so
that context budgeting cannot disclose contents or weaken existing path safety.

**Why P1:** Measurement reads canonical sources and therefore must preserve the planner's current
privacy and ownership contract.

**Acceptance Criteria:**

1. IF a configured heading is absent, duplicated, malformed, repeated in one reference, or applied to a non-Markdown source THEN the planner SHALL fail with exit code 2 without emitting source content. `BWC-05`
2. IF a manifest contains an unsafe path, missing source, duplicate source, unknown field, invalid estimator, invalid budget, or unsupported route order THEN the planner SHALL fail with exit code 2 without mutating the workspace. `BWC-06`
3. WHILE context planning, measurement, or checking is in use, the planner SHALL NOT emit selected source content, credentials, transcripts, session IDs, or physical workspace paths. `BWC-07`
4. WHEN the canonical manifest is audited THEN it SHALL define exactly the five existing routes with a positive budget and explicit heading list for every reference. `BWC-08`

**Independent Test:** Hostile fixtures exercise every schema, path, heading, budget, and privacy
boundary while comparing the fixture tree before and after each call.

## Edge Cases

- WHEN a selected section ends at end-of-file THEN the planner SHALL include all code points through end-of-file. `BWC-09`
- WHEN two selected headings are adjacent THEN the planner SHALL measure each heading without inserting source content or synthetic separators. `BWC-10`
- IF checking all routes finds both passing and oversized routes THEN the planner SHALL report every route deterministically and exit with code 1. `BWC-11`

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| BWC-01 | Measure routes | DECISION | User-approved retrospective implementation | Execute | Verified |
| BWC-02 | Measure routes | DECISION | User-approved retrospective implementation | Execute | Verified |
| BWC-03 | Measure routes | DECISION | User-approved retrospective implementation | Execute | Verified |
| BWC-04 | Measure routes | DECISION | User-approved retrospective implementation | Execute | Verified |
| BWC-05 | Closed boundaries | SAFETY | Existing planner fail-closed contract | Execute | Verified |
| BWC-06 | Closed boundaries | INHERITED | AD-044 and workspace ownership rules | Execute | Verified |
| BWC-07 | Closed boundaries | SAFETY | Workspace security and retrospective privacy rules | Execute | Verified |
| BWC-08 | Closed boundaries | INHERITED | L-008 and five-route workspace contract | Execute | Verified |
| BWC-09 | Edge cases | DECISION | Approved heading-selection semantics | Execute | Verified |
| BWC-10 | Edge cases | DECISION | Approved heading-selection semantics | Execute | Verified |
| BWC-11 | Edge cases | SAFETY | Complete fail-closed audit behavior | Execute | Verified |

**Coverage:** 11 total, 11 mapped to tasks, 0 unmapped.

## Success Criteria

- [x] All five canonical routes pass a deterministic context-budget check.
- [x] Adjacent budget boundaries discriminate pass from fail.
- [x] Heading, schema, privacy, and no-mutation fixtures pass.
- [x] The root workspace gate and independent validation pass.
