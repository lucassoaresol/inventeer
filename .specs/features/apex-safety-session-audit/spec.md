# APEX Safety and Session Audit Specification

**Status:** Approved and amended by the user's 2026-08-02 native APEX pilot request
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The Codex APEX surface has expanded from diagnostic reads to include Git, pull-request, task, and
multi-repository mutations, but its workspace configuration does not explicitly require approval
for writes. Retrospectives also depend on repeated ad hoc parsing of local Codex and Claude history,
which makes continuation deduplication and actual APEX usage counts expensive and error-prone.
A native Claude pilot also showed that a structured tool request is not evidence of execution when
the call is denied, fails, remains unresolved, or the workflow requires a tool the server does not
publish.

## Goals

- Keep APEX diagnostic reads available in Codex while requiring approval for mutating tools.
- Produce a repeatable, content-safe inventory of workspace sessions across Codex and Claude.
- Distinguish main sessions, continuations, sub-agent/sidechain sessions, and logical work streams.
- Count observed APEX outcomes from structured tool-call and result records instead of tool
  descriptions in prompts.
- Preserve a sanitized native-pilot verdict that tests workflow/resource/tool coherence without
  copying the Claude transcript.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Promoting APEX to Codex delivery executor | End-to-end session, artifact, and gate support remains absent. |
| Changing Claude/APEX execution | Claude remains the supported APEX executor for eligible repositories. |
| Persisting transcripts or prompt excerpts | Session contents may contain sensitive or irrelevant context. |
| Automatically interpreting product outcomes | Product findings still belong in their canonical product sources. |
| Repairing Codex session stability | The workspace can preserve continuity but does not own the engine runtime. |

## Assumptions and Decisions

| Decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Codex APEX approval | `default_tools_approval_mode = "writes"` | Allows read-only diagnosis while gating mutations. | Yes, inferred from the explicit tooling-improvement request and existing shadcn pattern. |
| Report content | Aggregate metadata only | Prevents prompts, outputs, credentials, and customer data from being copied. | Yes, inherited from AD-027. |
| Continuation detection | Recognize a referenced session UUID together with drop/continue wording | Codex continuations are new CLI sessions without a structured parent link. | Yes, best available local evidence. |
| Current retrospective | Explicit `--exclude-session` input | The running session must not count as its own evidence. | Yes, inherited from AD-027. |

**Open questions:** none for this workspace-only improvement.

## P1: Approval-Gate Codex APEX Writes

**User Story:** As the workspace owner, I want APEX mutations in Codex to require approval so that
an experimental diagnostic integration cannot silently change Git, GitHub, Linear, or multiple
repositories.

**Acceptance Criteria:**

1. WHEN Codex loads the project-scoped APEX server, THEN its configuration SHALL set
   `default_tools_approval_mode` to `writes`.
2. WHEN workspace guardrails describe APEX in Codex, THEN they SHALL state that mutating APEX tools
   require approval and do not broaden product ownership or delivery authority.
3. WHEN the MCP configuration test runs, THEN it SHALL fail if the APEX write-approval mode is
   absent or weakened.
4. WHEN the approval guard changes, THEN Claude's native APEX execution configuration SHALL remain
   unchanged.

## P1: Sanitized Session-History Audit

**User Story:** As a tooling maintainer, I want one deterministic session-history audit so that I
can learn from real usage without manually copying or over-counting transcripts.

**Acceptance Criteria:**

1. WHEN the audit scans Codex history for the workspace cwd, THEN it SHALL report main sessions,
   continuations, sub-agents, logical work streams, APEX-using sessions, and APEX calls by tool.
2. WHEN the audit scans the matching Claude project, THEN it SHALL report sessions, sidechains,
   logical sessions, APEX-using sessions, and APEX calls by tool.
3. WHEN a Codex continuation references an earlier UUID with drop/continue wording, THEN the audit
   SHALL count it as a continuation instead of an independent logical work stream.
4. WHEN `--exclude-session <id>` is supplied, THEN the matching session SHALL not contribute to any
   count.
5. WHEN the audit emits text or JSON, THEN it SHALL NOT include user prompts, assistant responses,
   tool results, or transcript bodies.
6. WHEN APEX usage is counted, THEN only structured observed tool-call records SHALL contribute;
   tool names present in injected instructions or descriptions SHALL not count.
7. WHEN fixture-based tests run, THEN they SHALL detect broken continuation classification,
   exclusion, sidechain classification, APEX counting, and content leakage.
8. WHEN a structured APEX request has a result, THEN the audit SHALL distinguish successful calls
   from failures and denials; requests without a result SHALL be reported as unresolved rather than
   successful usage.

## P1: Native APEX Pilot Evidence

**User Story:** As a tooling maintainer, I want a real Claude/APEX pilot so that executor policy is
based on the server contract actually exposed to an eligible Portal repository.

**Acceptance Criteria:**

1. WHEN the pilot invokes `eng-ready`, THEN it SHALL fetch the canonical workflow resource and try
   the required read-only gate without editing product files or mutating external systems.
2. WHEN a required workflow tool is absent, THEN the pilot SHALL fail closed and identify the
   contract mismatch instead of presenting a filesystem approximation as APEX execution.
3. WHEN pilot evidence is versioned, THEN it SHALL contain only sanitized metadata, outcomes, and
   routes; it SHALL NOT contain transcript bodies, credentials, or tool-result payloads.

## Edge Cases

- Sessions outside the requested cwd or before the cutoff are ignored.
- A continuation whose parent predates the cutoff is still classified as a continuation when its
  user message contains the referenced UUID and drop/continue markers.
- Claude histories do not expose the same continuation convention as Codex; the audit reports
  sidechains but does not invent resume relationships.
- Missing history directories produce an empty engine summary rather than exposing host paths.

## Requirement Traceability

| Requirement | Provenance | Evidence | Status |
| --- | --- | --- | --- |
| ASSA-01 | SAFETY | Current APEX mutation surface and `.codex/config.toml` | Verified |
| ASSA-02 | INHERITED | AD-026 ownership and executor boundary | Verified |
| ASSA-03 | SAFETY | `scripts/test-mcp-config.py` regression gate | Verified |
| ASSA-04 | INHERITED | Claude/APEX route in AD-026 | Verified |
| ASSA-05 | ISSUE | User requested session-based learning | Verified |
| ASSA-06 | INHERITED | AD-027 deduplication and privacy boundary | Verified |
| ASSA-07 | INHERITED | AD-027 excludes the current retrospective | Verified |
| ASSA-08 | SAFETY | Structured call records avoid prompt contamination | Verified |
| ASSA-09 | SAFETY | Native pilot distinguishes requested, denied, failed, unresolved, and successful calls | Verified |
| ASSA-10 | ISSUE | User requested a real APEX workflow pilot against Portal | Verified |

## Success Criteria

- Existing APEX read-only inspection remains usable after a Codex restart.
- Every Codex APEX mutation requires engine approval.
- The audit reproduces the retrospective counts from synthetic fixtures without emitting content.
- A denied, failed, or unresolved APEX request never inflates successful usage.
- The native pilot either completes the canonical gate or fails closed on an exact contract gap.
- All workspace contract tests and the feature discrimination sensor pass.
