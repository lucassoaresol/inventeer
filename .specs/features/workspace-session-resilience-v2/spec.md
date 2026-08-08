# Workspace Session Resilience v2 Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The workspace already audits local Codex and Claude histories, but its report cannot freeze a
reproducible cohort or quantify whether interruptions are concentrated in primary sessions. The
workspace also prohibits storing credentials without defining how an agent must handle a potential
secret supplied in chat.

## Goals

- [ ] Prevent agents from repeating or persisting potential secrets received in chat.
- [ ] Produce a versioned, reproducible session-history report with interruption concentration.
- [ ] Preserve every existing APEX outcome field and its semantics.
- [ ] Start a bounded, aggregate-only pilot before proposing additional session automation.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Generic checkpoint runner | The pilot must first establish whether more automation is justified. |
| Root lessons entrypoint | Valuable but independently reversible and outside session resilience. |
| Feature lifecycle index | Valuable governance improvement, but unrelated to this feature's runtime contract. |
| Product repository changes | This decision belongs only to the personal Inventeer workspace. |
| Importing EDREN baseline values | Session populations are workspace-specific and cannot be transferred. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Report compatibility | Add fields without removing or renaming existing APEX fields | Existing retrospective decisions depend on their exact distinction | yes |
| Upper time bound | Optional exclusive `--until`; omission preserves the unbounded behavior | Enables reproducible cohorts without breaking existing calls | yes |
| Interruption population | Deduplicated primary Codex sessions only | Copies and subagents are derived evidence, while Claude history has no equivalent structured interruption events | yes |
| Pilot boundary | Ten eligible primary sessions or the next long workspace feature, whichever comes first | Provides bounded evidence before new automation | yes |
| Artifact contents | Sanitized aggregates and contract metadata only | Session identity, transcript paths, content, tools, credentials, and production output are prohibited | yes |
| Remaining implicit dimensions | N/A for persistence, auth, concurrency, retries, and external dependencies | The feature is a read-only local metadata audit and repository instruction contract | yes |

**Open questions:** none.

## User Stories

### P1: Contain Potential Secrets Received in Chat

**User Story**: As the workspace maintainer, I want agents to contain potential secrets supplied in
chat so that the workspace, commands, and review artifacts cannot amplify an accidental exposure.

**Acceptance Criteria**:

1. WHEN a user supplies a credential or secret-like value in chat THEN the agent contract SHALL
   prohibit repeating the value and require `[REDACTED]` when a reference is necessary.
2. WHEN a potential secret needs local use THEN the agent contract SHALL prohibit placing it in
   displayed commands, logs, commits, checkpoints, or versioned artifacts.
3. WHEN a potential secret needs local use THEN the agent contract SHALL prefer an ignored `.env`
   file or interactive input.
4. IF chat exposure may have occurred THEN the agent contract SHALL recommend conditional rotation
   without asserting that the credential remains active.

**Independent Test**: Run the workspace session-resilience contract test and verify every required
security phrase is present without reading session transcripts.

### P1: Audit Reproducible Session Cohorts

**User Story**: As the workspace maintainer, I want a stable session-audit contract so that future
retrospectives can distinguish source drift from new work and retain existing APEX evidence.

**Acceptance Criteria**:

1. WHEN `--until` is supplied THEN the auditor SHALL include Codex and Claude sessions whose origin
   is in the UTC interval `[since, until)`.
2. IF `--until` is invalid THEN the auditor SHALL exit non-zero with
   `--until must be an ISO date or timestamp`.
3. IF `--until` is not later than `--since` THEN the auditor SHALL exit non-zero with
   `--until must be later than --since`.
4. WHEN the report is emitted THEN it SHALL include integer `contract_version` 2, normalized
   `since`, normalized `until` or `null`, and `excluded_sessions`.
5. WHEN Codex histories contain aborts or compactions THEN the auditor SHALL report deduplicated
   totals, affected-primary counts, primary percentages rounded to two decimals, and per-primary
   maxima.
6. WHEN copies or subagents contain interruption events THEN the auditor SHALL exclude them from
   affected-primary counts, percentages, and maxima.
7. WHEN the v2 report is emitted THEN the auditor SHALL preserve the existing Codex and Claude
   `apex_tool_successes`, `apex_tool_failures`, `apex_tool_denials`, and
   `apex_tool_unresolved` fields with their existing meanings.
8. WHEN a history root is absent or has no matching origins THEN the report SHALL distinguish root
   availability from matching-history availability and return zero interruption metrics.
9. WHEN JSON or text output is emitted THEN it SHALL omit transcript content, session identifiers,
   history paths, workspace paths, and credential values.

**Independent Test**: Run fixture histories spanning both time boundaries, duplicates, subagents,
interruption events, all APEX outcomes, missing roots, and sensitive sentinel values.

### P2: Observe Before Automating

**User Story**: As the workspace maintainer, I want a bounded pilot so that additional checkpoint or
gate-runner automation is proposed only from measured workflow failures.

**Acceptance Criteria**:

1. WHEN the v2 auditor is accepted THEN the workspace SHALL record AD-041 with the compatibility,
   privacy, and bounded-pilot decision.
2. WHILE the pilot is active, its artifact SHALL contain only contract metadata, sanitized
   aggregates, eligibility rules, success measures, and explicit automation thresholds.
3. WHEN ten eligible primary sessions or the next long workspace feature completes THEN the pilot
   SHALL require a closing comparison before any runner is proposed.

**Independent Test**: Run the session-resilience contract test and verify the decision and pilot
contain every lifecycle boundary while rejecting UUIDs and transcript-history paths.

## Edge Cases

- WHEN a session origin equals `until` THEN the auditor SHALL exclude it.
- IF a timestamp in a history record is malformed THEN the auditor SHALL ignore that record without
  leaking its content.
- WHEN the same primary session ID appears in more than one file THEN interruption and APEX session
  concentration SHALL count that primary session once.
- WHEN no primary Codex sessions match THEN all affected counts, percentages, and maxima SHALL be
  zero.
- WHEN `--until` is omitted THEN existing unbounded-after-`since` calls SHALL remain valid.

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| WSR-01 | P1: Secret non-repetition | SAFETY | Approved EDREN comparison | Execute | Implementing |
| WSR-02 | P1: Secret persistence boundary | SAFETY | Approved EDREN comparison | Execute | Implementing |
| WSR-03 | P1: Safe local input | SAFETY | Approved EDREN comparison | Execute | Implementing |
| WSR-04 | P1: Conditional rotation | SAFETY | Approved EDREN comparison | Execute | Implementing |
| WSR-05 | P1: Closed time window | DECISION | User approved recommendation | Execute | Implementing |
| WSR-06 | P1: Invalid upper bound | DECISION | User approved recommendation | Execute | Implementing |
| WSR-07 | P1: Report provenance | DECISION | User approved recommendation | Execute | Implementing |
| WSR-08 | P1: Interruption concentration | INHERITED | AD-027, AD-033, AD-036 | Execute | Implementing |
| WSR-09 | P1: Derived-history exclusion | INHERITED | AD-027 and confirmed lesson L-008 | Execute | Implementing |
| WSR-10 | P1: APEX compatibility | INHERITED | AD-033 and AGENTS.md retrospective contract | Execute | Implementing |
| WSR-11 | P1: Availability distinction | DECISION | User approved recommendation | Execute | Implementing |
| WSR-12 | P1: Sanitized output | INHERITED | AD-027 and AD-033 | Execute | Implementing |
| WSR-13 | P2: Transversal decision | INHERITED | Workspace AGENTS.md | Execute | Implementing |
| WSR-14 | P2: Aggregate-only pilot | DECISION | User approved recommendation | Execute | Implementing |
| WSR-15 | P2: Bounded automation gate | DECISION | User approved recommendation | Execute | Implementing |

**Coverage:** 15 total, 15 mapped to tasks, 0 unmapped.

## Success Criteria

- [x] Every security rule passes a repository contract test.
- [x] Every auditor fixture and prior APEX assertion passes under contract version 2.
- [x] The full workspace gate passes without skipped coverage.
- [ ] Independent validation matches all 15 requirements and kills targeted mutants.
