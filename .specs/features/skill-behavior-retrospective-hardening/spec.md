# Skill Behavior Retrospective Hardening Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The dual-engine retrospective exposed three operational gaps that structural validation does not
currently prevent: TLC validation can claim an independent Verifier without observable provenance,
lesson candidates do not recur across semantically equivalent wording, and local PR validation is
often not bound to the reviewed head. Session-history analysis also remains a repeated manual
workflow without a dedicated skill or engine-aware skill-use evidence.

## Goals

- [ ] Make TLC completion fail closed when Verifier independence is undeclared or unsupported.
- [ ] Merge future lesson recurrences by a stable semantic pattern across distinct features.
- [ ] Close the PR-review pilot with exact-head materialization and explicit local-validation reasons.
- [ ] Provide a discoverable, sanitized retrospective skill backed by conservative engine metrics.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Revalidating historical TLC features | Provenance did not exist when those reports were created. |
| Rewriting the existing lessons store | Legacy entries remain compatible and acquire semantic keys only through future grounded observations. |
| Automatically fetching private PRs | Network access and credentials remain separately authorized at execution time. |
| Posting reviews or mutating product repositories | The review workflow remains read-only. |
| Persisting transcripts or session identifiers | AD-027 and AD-046 require sanitized aggregate evidence. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Scope approval | Implement all four recommendations from the accepted retrospective | The user explicitly authorized proceeding after reviewing the prioritized package | yes |
| Verifier provenance | Require a declared `independent-agent` or `standalone-fallback` mode plus evidence; fallback requires a capability limitation | A prose mention of Verifier did not discriminate the observed failure | yes |
| Lesson identity | Require a kebab-case `pattern_key` for new observations and merge on signal plus key before text heuristics | Stable semantics are safer than lowering a similarity threshold | yes |
| Existing lessons | Preserve schema-1 entries and text-based fallback | A forced migration would invent semantic judgments for historical records | yes |
| Review checkout | Materialize base/head in a separate explicit directory and never alter the source worktree | This binds local evidence while preserving the review skill's read-only boundary | yes |
| Skill-use parity | Report structured invocation only where the engine exposes it and mark the other engine unsupported | `null` must mean unmeasured rather than a fabricated zero | yes |
| Retrospective skill routing | Keep it unrouted initially | The history auditor supplies bounded dynamic evidence and no canonical product route applies | yes |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: Verifiable TLC independence

**User Story**: As the workspace maintainer, I want completion evidence to distinguish independent
verification from self-verification so that a structurally valid report cannot silently violate
`author != verifier`.

**Why P1**: The referenced Claude session produced three validation reports without any independent
agent execution.

**Acceptance Criteria**:

1. WHEN a TLC validation report declares `independent-agent` THEN the completion gate SHALL require non-placeholder independent execution evidence.
2. WHEN a TLC validation report declares `standalone-fallback` THEN the completion gate SHALL require a concrete unavailable-capability reason.
3. IF a completed TLC validation report omits Verifier mode or its required evidence THEN the completion gate SHALL exit non-zero.
4. WHILE historical validation reports predate this contract the workspace-wide gate SHALL preserve their prior validity without rewriting them.

**Independent Test**: Fixtures for independent, fallback, missing, placeholder, and historical reports
produce the specified deterministic outcomes.

### P1: Semantic lesson recurrence

**User Story**: As a future TLC execution, I want differently worded observations of the same failure
pattern to share a stable identity so that confirmed lessons become usable memory without unsafe
text-threshold tuning.

**Why P1**: All 32 current entries have recurrence one, leaving 31 candidates unloaded.

**Acceptance Criteria**:

1. WHEN a new lesson is added THEN the lesson store SHALL require a normalized kebab-case `pattern_key`.
2. WHEN two lessons from distinct features share signal and `pattern_key` THEN the lesson store SHALL merge them regardless of wording.
3. IF two lessons share a `pattern_key` but have different signals THEN the lesson store SHALL keep them separate.
4. WHILE legacy lessons lack `pattern_key` the lesson store SHALL continue loading, rendering, pruning, and matching them through the existing compatibility path.
5. IF a `pattern_key` is empty, malformed, or contains sensitive free-form content THEN the lesson store SHALL reject it before writing.

**Independent Test**: Script tests cover semantic recurrence, cross-signal separation, malformed keys,
legacy compatibility, promotion, and unchanged-store-on-error behavior.

### P1: Head-bound PR review evidence

**User Story**: As an independent PR reviewer, I want local validation to run against the exact
reviewed head or state why it did not so that passing tests from another checkout cannot support the
verdict.

**Why P1**: Three of nine pilot reviews recorded unbound local validation.

**Acceptance Criteria**:

1. WHEN exact base and head objects are available from an authorized source THEN the review helper SHALL create a detached checkout in an explicit ephemeral destination and verify both SHAs without changing the source worktree.
2. IF the source, destination, base SHA, or head SHA is invalid THEN the review helper SHALL fail before claiming a materialized review surface.
3. WHEN a schema-v2 review record reports local validation as `unbound`, `not-run`, or `not-applicable` THEN the record SHALL include a bounded reason.
4. WHEN a schema-v2 review record reports local validation as `passed` or `failed` THEN the record SHALL bind it to the final head SHA.
5. WHILE schema-v1 pilot records are summarized the helper SHALL preserve their existing meaning and metrics.
6. WHEN the nine-record pilot is evaluated THEN the workspace decision SHALL record the promotion outcome and remaining exact-head limitation.

**Independent Test**: A local Git fixture proves detached exact-SHA materialization and source
porcelain preservation; ledger fixtures prove schema-v1 compatibility and schema-v2 reason/binding
rules.

### P1: Engine-aware skill retrospective

**User Story**: As the workspace maintainer, I want a dedicated retrospective skill to distinguish
real skill activation from mentions and engine limitations so that workflow changes rely on
reproducible evidence instead of ad hoc transcript searches.

**Why P1**: Retrospective behavior has recurred across AD-027, AD-033, AD-041, AD-046 and the current
analysis, while no existing skill owns it.

**Acceptance Criteria**:

1. WHEN the session auditor reads a structured Claude `Skill` tool call THEN it SHALL aggregate the skill name and distinct session count without emitting prompt or result content.
2. WHILE Codex exposes no structured skill-invocation event the auditor SHALL report invocation metrics as `null` with an unsupported reason rather than infer zero.
3. WHEN Codex or Claude evidence only shows a `SKILL.md` path in a shell or tool input THEN the retrospective SHALL classify it as a load proxy rather than an invocation.
4. IF a transcript merely mentions a skill name in user, developer, assistant prose, or tool output THEN the auditor SHALL not count an invocation.
5. WHEN a retrospective is requested THEN `retrospect-skill-usage` SHALL require a closed UTC window, current-session exclusion accounting, engine limitations, opportunity-aware interpretation, and sanitized chat output.
6. The retrospective skill SHALL remain read-only and SHALL not persist transcripts, mutate histories, alter product repositories, or implement its own recommendations.
7. WHEN the new skill is created THEN both Codex metadata and the Claude relative symlink SHALL expose the same source skill.

**Independent Test**: Engine fixtures discriminate structured invocations, path-load proxies,
decoys, unsupported values, exclusions, and sensitive transcript content; skill validators confirm
both engine surfaces.

## Edge Cases

- IF a Verifier evidence field contains a template token THEN the completion gate SHALL reject it.
- IF two semantic lesson keys collide across different signals THEN no cross-signal merge SHALL occur.
- IF review materialization cannot resolve either exact SHA THEN the helper SHALL remove no source data and return non-zero.
- IF an excluded session contains the only structured skill invocation THEN the audit SHALL report zero matched invocations for supported engines.
- IF a history root or invocation metric is unsupported THEN the receipt SHALL distinguish unavailable, unsupported, and measured zero states.

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| SBRH-01 | Verifiable TLC independence | INHERITED | TLC `author != verifier` contract and session `6f9dd839…` | Execute | Implementing |
| SBRH-02 | Historical TLC compatibility | DECISION | Approved retrospective recommendation | Execute | Implementing |
| SBRH-03 | Semantic lesson recurrence | DECISION | 31 candidates, one confirmed, all recurrence one | Execute | Implementing |
| SBRH-04 | Lesson input safety and compatibility | SAFETY | Machine-owned store and existing schema | Execute | Implementing |
| SBRH-05 | Exact-head review checkout | DECISION | 3/9 unbound local validations | Tasks | Pending |
| SBRH-06 | Review ledger v2 and v1 compatibility | INHERITED | AD-038/AD-039 pilot evidence | Tasks | Pending |
| SBRH-07 | Pilot promotion decision | DECISION | Nine reviewed PRs satisfy the pilot size | Tasks | Pending |
| SBRH-08 | Structured Claude invocation metrics | DECISION | Claude `Skill` tool event is observable | Tasks | Pending |
| SBRH-09 | Unsupported Codex invocation semantics | INHERITED | Audit contract v4 null semantics | Tasks | Pending |
| SBRH-10 | Conservative load-proxy classification | SAFETY | Raw name/path searches overcount usage | Tasks | Pending |
| SBRH-11 | Retrospective skill and dual-engine surface | DECISION | Recurrent manual workflow and AD-024 | Tasks | Pending |
| SBRH-12 | Privacy and read-only boundaries | INHERITED | AD-027, AD-046 and workspace security policy | Tasks | Pending |

## Implicit Requirement Dimensions

| Dimension | Resolution |
| --- | --- |
| Input validation & bounds | Exact enum, SHA, pattern-key, reason-length, UTC-window, and path validation are required. |
| Compatibility & representation | Historical validation, schema-v1 review records, legacy lessons, and receipt null semantics remain readable. |
| Failure / partial-failure states | Every helper fails closed before claiming evidence; incomplete evidence is explicit. |
| Idempotency / retry / duplicate handling | Lesson recurrence uses distinct features; materialization rejects a populated destination; audit remains read-only. |
| Auth boundaries & rate limits | Network fetch remains separately authorized and no credentials are persisted. |
| Concurrency / ordering | One machine-owned lesson write and explicit review destination; no concurrent writer guarantee is introduced. |
| Data lifecycle / expiry | Review checkout is ephemeral; transcript content and identifiers are not persisted. |
| Observability | Receipts expose supported, unsupported, proxy, and exclusion counts without content. |
| External-dependency failure | Missing Git objects, history roots, or agent capability produce explicit non-success states. |
| Operational enablement | Both engines receive the skill surface; scripts remain standard-library or shell/Git based. |
| State-transition integrity | Validation cannot move to PASS without provenance; lessons promote only across distinct features. |
