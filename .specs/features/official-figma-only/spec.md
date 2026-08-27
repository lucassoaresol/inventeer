# Official Figma MCP Only Specification

**Status:** Implemented
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The local Figma bridge pilot cannot be used because the Desktop plugin entry point is unavailable in
the user's Figma installation. The user has a Pro account and chose to keep only the official OAuth
MCP instead of retaining an unusable parallel configuration.

## Goals

- [x] Remove `figma-local` from both engine configurations and active workspace guidance.
- [x] Preserve the official `figma` OAuth server enabled and unchanged.
- [x] Record that the local-pilot portion of AD-051 is superseded without discarding its history.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Deleting the downloaded Windows plugin files | External deletion is separate from retiring the workspace integration. |
| Mutating or validating a Figma file | The official MCP remains the selected integration; no design target was authorized. |
| Changes under `repos/` | This is a workspace configuration decision only. |
| Changing Figma account or seat settings | Account administration is outside this workspace. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Selected integration | Official `figma` OAuth MCP only | The user explicitly discarded the plugin-based pilot. | y |
| Official server state | Enabled and unchanged | It is already the supported default and does not require the Desktop plugin. | y |
| Local plugin files | Retain | Removing external files is unnecessary and destructive. | y |

**Open questions:** none.

## User Stories

### P1: Keep one usable Figma integration

**User Story:** As the workspace maintainer, I want only the official Figma MCP configured so that
engines do not advertise a local integration that cannot be activated.

**Acceptance Criteria:**

1. WHEN either engine loads workspace MCP configuration THEN it SHALL find the official `figma` OAuth endpoint and SHALL NOT find `figma-local`.
2. WHILE the official-only decision is active, the workspace SHALL keep the official Figma server enabled with its existing write-approval boundary.
3. WHEN workspace guidance describes Figma THEN it SHALL route usage only to the authenticated official MCP and SHALL NOT instruct operators to install or connect the local Desktop plugin.
4. WHEN the decision log is read THEN it SHALL preserve AD-051 and record that AD-052 supersedes only its local Figma pilot portion.

**Independent Test:** Run the MCP configuration suite and observe official-server parity plus the
absence of `figma-local` from both engine configurations and active guidance.

## Edge Cases

- IF a future edit reintroduces `figma-local` to either engine THEN the MCP configuration gate SHALL fail.
- IF the official endpoint, enabled state, or write approval changes THEN the MCP configuration gate SHALL fail.
- IF active guidance still instructs operators to install the local plugin THEN the documentation contract SHALL fail.

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| OFO-01 | Official-only configuration | DECISION | MCP suite asserts absence in both engines | Execute | Verified |
| OFO-02 | Preserve official MCP | INHERITED | MCP suite asserts endpoint, enabled state and approval | Execute | Verified |
| OFO-03 | Remove active pilot guidance | DECISION | README and AGENTS contract assertions | Execute | Verified |
| OFO-04 | Preserve decision history | INHERITED | AD-051 and AD-052 contract assertions | Execute | Verified |
| OFO-05 | Preserve repo boundary | SAFETY | Scoped diff inspection | Execute | Verified |

**Coverage:** 5 total, 5 mapped to the inline execution plan, 0 unmapped.

## Success Criteria

- [x] Both engine configurations expose only the official Figma MCP.
- [x] Active instructions contain no local-plugin activation path.
- [x] AD-052 narrows AD-051 without deleting history.
- [x] Focal and aggregate workspace gates pass.
