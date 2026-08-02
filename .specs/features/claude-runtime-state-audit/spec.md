# Claude Runtime State and Session Audit Specification

**Status:** Approved by the user's 2026-08-02 implementation authorization
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

Claude sessions started from this workspace can change their working directory while OMC hooks are
running. Without a centralized state root, those hooks create `.omc/` runtime files in the workspace
or nested product repositories. The sanitized session-history auditor also retains the last Claude
`cwd`, causing a session that started at the workspace root to disappear from the audit after it
changes directory. Finally, the audit's current field names can be misread as evidence that an APEX
workflow completed when they only prove that individual APEX tools returned successfully.

## Goals

- Keep OMC runtime state under the workspace's ignored `session-context/` surface.
- Load the OMC state root automatically whenever Claude starts from the workspace root.
- Prevent working-directory changes from changing the OMC state location.
- Associate Claude histories with the workspace where the session started.
- Report APEX tool outcomes with names that do not imply workflow completion.
- Count Claude's generic MCP resource reads when the selected server is APEX.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Publishing missing APEX tools or workspace context | The APEX gateway is externally owned. |
| Inferring APEX workflow completion | No structured completion marker is currently published. |
| Changing repositories under `repos/` | This is a workspace runtime and audit improvement only. |
| Persisting OMC state in Git | Runtime state is local, ephemeral, and non-canonical. |
| Automatically deleting legacy `.omc/` state | Cleanup is destructive and requires target verification and user authorization. |

## Assumptions and Decisions

| Decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Claude launch location | Workspace root | The user always starts Claude from this root. | Yes |
| Runtime root | `session-context/runtime/omc/` | It is ignored, local, predictable, and outside product worktrees. | Yes |
| Environment configuration | Absolute `OMC_STATE_DIR` in `.claude/settings.local.json` | It loads before OMC hooks and remains stable after `cwd` changes. | Yes |
| Durable contract | AD-035 plus workspace documentation | Machine-local configuration remains ignored while the policy is reviewable. | Yes |
| Claude session ownership | First non-empty recorded `cwd` | Session origin is stable; later tool-driven directory changes are not. | Yes |
| Existing `.omc/` directories | Leave in place until a separately authorized cleanup | Avoids destructive migration or deletion during the feature. | Yes |

**Open questions:** none for implementation. Legacy cleanup remains a separately authorized action.

## P1: Isolate OMC Runtime State

**User Story:** As the workspace owner, I want Claude's OMC runtime state centralized under
`session-context/` so that hooks do not dirty product worktrees when Claude changes directory.

**Acceptance Criteria:**

1. WHEN Claude starts from the workspace root, THEN project-local settings SHALL provide an absolute
   `OMC_STATE_DIR` equal to
   `/root/lucas/inventeer/repo/inventeer/session-context/runtime/omc`.
2. WHEN an OMC hook runs after Claude changes into `repos/` or a nested repository, THEN OMC SHALL
   resolve its state beneath `session-context/runtime/omc/<project-id>/` and SHALL NOT create a new
   `.omc/` directory at the later working directory.
3. WHEN the runtime-state policy is inspected, THEN AD-035, `AGENTS.md`, and `README.md` SHALL state
   that this state is local, ephemeral, ignored by Git, non-canonical, and eligible for cleanup only
   after the relevant sessions stop.
4. WHEN this feature is implemented, THEN AD-031's Portal-specific Codex + TLC artifact contract
   SHALL remain unchanged.
5. WHEN local OMC state is redirected, THEN no credential, customer data, production output, or
   transcript body SHALL be added to the workspace Git history.

## P1: Harden Claude Session Attribution

**User Story:** As a tooling maintainer, I want the history auditor to retain the session's origin so
that a later `cwd` change does not silently remove valid evidence from a workspace retrospective.

**Acceptance Criteria:**

1. WHEN a Claude session's first non-empty `cwd` equals the requested workspace and a later record
   uses another `cwd`, THEN the audit SHALL include the session.
2. WHEN a Claude session's first non-empty `cwd` does not equal the requested workspace, THEN a later
   visit to the workspace SHALL NOT make the session eligible.
3. WHEN the fixture reproduces session `ea1175a4-a93b-4a29-8968-aa3c59bde4ba`'s directory drift,
   THEN the audit SHALL report one logical Claude session rather than zero.

## P1: Make APEX Tool Evidence Explicit

**User Story:** As a tooling maintainer, I want audit fields to describe individual tool outcomes so
that a successful MCP response is never presented as proof of completed APEX workflow execution.

**Acceptance Criteria:**

1. WHEN the audit emits text or JSON, THEN its success-session and outcome fields SHALL use
   `apex_tool_*` names and SHALL NOT expose the ambiguous `apex_sessions` or `apex_calls` fields.
2. WHEN Claude calls `ReadMcpResourceTool` with `input.server == "apex"`, THEN the paired structured
   result SHALL be counted as an APEX tool outcome named `read_mcp_resource`.
3. WHEN `ReadMcpResourceTool` targets a server other than APEX, THEN it SHALL NOT contribute to any
   APEX count.
4. WHEN an APEX tool returns a successful transport result whose payload describes an unavailable
   operational state, THEN the audit SHALL report only the tool success and SHALL NOT infer workflow
   readiness or completion.
5. WHEN an APEX request is denied, fails, or lacks a paired result, THEN the existing distinct
   denial, failure, and unresolved classifications SHALL remain intact under explicit `apex_tool_*`
   field names.

## Edge Cases

- Claude records without a `cwd` before the first valid directory do not lock the session origin.
- A generic MCP resource read is identified by both its tool shape and `input.server`; its name alone
  is insufficient.
- OMC may add its own project identifier below `OMC_STATE_DIR`; the configured directory is the
  centralized base, not the final per-session leaf.
- Existing legacy `.omc/` directories are evidence from earlier sessions and are not treated as a
  failure of the new configuration until a post-change session creates new files there.

## Requirement Traceability

| Requirement | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- |
| CRSA-01 | DECISION | User selected `session-context/` and confirmed root launches | Runtime | Pending |
| CRSA-02 | INHERITED | AD-017 ephemeral context boundary | Runtime | Pending |
| CRSA-03 | INHERITED | AD-031 Portal-specific scope boundary | Runtime | Pending |
| CRSA-04 | ISSUE | `.omc/` files created by Claude hooks in two observed sessions | Runtime | Pending |
| CRSA-05 | ISSUE | Claude session lost when final `cwd` changed to `repos/` | Audit | Pending |
| CRSA-06 | SAFETY | Tool success must not imply workflow completion | Audit | Pending |
| CRSA-07 | ISSUE | Claude resource reads use `ReadMcpResourceTool` | Audit | Pending |
| CRSA-08 | INHERITED | AD-027 transcript and credential privacy boundary | Validation | Pending |

**Coverage:** 8 requirements; all mapped to runtime, audit, or validation work.

## Success Criteria

- A new Claude session started at the workspace root writes OMC state only under
  `session-context/runtime/omc/`, even after a working-directory change.
- The real directory-drift session is included by the sanitized auditor.
- Every APEX aggregate field explicitly describes tool-level evidence.
- Claude APEX resource reads are counted without counting non-APEX resources.
- Targeted fixtures, the full workspace gate, and focused discrimination mutants pass.
- The workspace Git history contains no local settings, runtime state, transcripts, or secrets.
