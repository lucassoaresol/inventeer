# Unified Dual-Engine Delivery Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The workspace currently routes Codex delivery through TLC but still routes eligible Claude Code
repositories through APEX. Session history and the native APEX pilot have not established a complete
APEX workflow in either engine, while Portal delivery already has a tested TLC working-artifact and
checkpoint route. The workspace needs one delivery contract for both engines so execution, review,
and continuation do not depend on which machine or engine starts the task.

## Goals

- Route specification, implementation, and validation through `tlc-spec-driven` in both engines.
- Use the Portal issue-local `session-context/portal/<INV-ID>/` layout in both engines.
- Preserve local recovery checkpoints after stable TLC transitions in both engines.
- Keep APEX available for inspection and diagnostics without presenting tool calls as workflow
  execution.
- Preserve canonical delivery evidence in Linear, Git, pull requests, product repositories, and
  approved product artifacts.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Removing the APEX MCP or generated Codex wrappers | Diagnostic access remains useful and does not imply execution. |
| Synchronizing `session-context/` between machines | The directory remains ignored, local, ephemeral, and non-canonical. |
| Changing repositories under `repos/` | This decision governs the personal engineering workspace only. |
| Extending the Portal artifact layout to other products | No equivalent product-specific need has been established. |
| Treating isolated APEX tool success as workflow completion | AD-034 requires context, every required tool, and structured gate results. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Delivery executor | TLC in Codex and Claude Code | The available history does not prove end-to-end APEX execution in either engine. | Yes |
| Portal working-artifact root | `session-context/portal/<INV-ID>/tlc/` in both engines | One issue-local layout makes continuation engine-independent on a given machine. | Yes |
| Review bundle root | `session-context/portal/<INV-ID>/review/` in both engines | Review evidence remains grouped with the issue's local working state. | Yes |
| Cross-machine continuity | Reconstruct from canonical sources or explicitly transfer a sanitized temporary package | Ignored session files do not synchronize through Git. | Yes |
| APEX lifecycle | Diagnostic only until a new end-to-end validation and decision | Tool availability alone is not an executable workflow. | Yes |

**Open questions:** none.

## User Stories

### P1: Use One Delivery Executor

**User Story:** As the workspace owner, I want Codex and Claude Code to use the same delivery
executor so that task construction, execution, review support, and continuation follow one contract.

**Acceptance Criteria:**

1. WHEN either Codex or Claude Code specifies, implements, or validates workspace or product work,
   THEN the workspace SHALL route the action through `tlc-spec-driven` after the applicable context
   skill.
2. WHEN either engine discovers APEX tools, resources, commands, or wrappers, THEN the workspace
   SHALL classify them as diagnostic or experimental and SHALL NOT present them as a supported
   delivery execution.
3. WHEN a future APEX pilot satisfies AD-034 end to end, THEN the workspace SHALL require a new
   transversal decision before changing the executor.

**Independent Test:** Run `scripts/test-engine-routing.sh` and confirm the same TLC executor and
APEX boundary are asserted for both engines.

### P1: Share the Portal Continuation Contract

**User Story:** As a Portal developer, I want either engine to use the same issue-local working
layout so that switching engine or starting on another machine does not change the delivery method.

**Acceptance Criteria:**

1. WHEN either engine creates file-backed TLC working artifacts for a Portal task, THEN the
   workspace SHALL store them under `session-context/portal/<INV-ID>/tlc/`.
2. WHEN either engine creates Portal review bundles, THEN the workspace SHALL group them under
   `session-context/portal/<INV-ID>/review/`.
3. WHEN either engine completes a declared stable TLC transition, THEN the workspace SHALL require
   the applicable `scripts/update-tlc-checkpoint.py` checkpoint after the transition succeeds.
4. IF a Portal task resumes on a machine without the prior local directory, THEN the engine SHALL
   reconstruct the task from Linear, Git, pull requests, product sources, and approved artifacts,
   or SHALL consume an explicitly transferred sanitized temporary package.
5. WHEN local Portal task state is documented, THEN the workspace SHALL classify it as ignored,
   local, ephemeral, non-canonical, non-durable, and not automatically portable across machines.
6. WHEN a Portal issue is merged and closed, THEN the issue-local session directory SHALL become
   eligible for cleanup.

**Independent Test:** Run `scripts/test-portal-tlc-session-artifacts.sh` and
`scripts/test-tlc-checkpoint-contract.sh` and confirm both engines share the same route, authority,
recovery, and cleanup boundaries.

## Edge Cases

- Switching from Codex to Claude Code on the same machine reuses the same local Portal issue path
  after reconciling it with canonical state.
- Starting on another machine follows the same path convention but does not assume prior local files
  exist.
- A successful isolated APEX tool call remains diagnostic evidence and does not override TLC routing.
- A durable product specification remains in its approved canonical source; a TLC working file is
  never promoted solely because both engines can read it.

## Requirement Traceability

| Requirement | Provenance | Evidence | Status |
| --- | --- | --- | --- |
| UDDE-01 | DECISION | User request to consolidate Codex and Claude execution | Implementing |
| UDDE-02 | INHERITED | AD-034 executable-workflow threshold | Implementing |
| UDDE-03 | DECISION | User request to continue through `session-context` for Portal | Implementing |
| UDDE-04 | INHERITED | AD-017 local session-context lifecycle | Implementing |
| UDDE-05 | INHERITED | AD-036 stable-transition checkpoints | Implementing |
| UDDE-06 | INHERITED | Workspace canonical-source boundaries | Implementing |

