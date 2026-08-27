# Workspace Operational Surface Simplification Specification

**Status:** Validated
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The workspace has reliable delivery controls, but discovery is the only broad context workflow
without a deterministic route, APEX exposes twenty-eight diagnostic skills despite not being a
supported executor, ephemeral state has no read-only eligibility inventory, and the rate-limited
official Figma server has no bounded local pilot path. These gaps increase context cost and manual
reconstruction without changing product ownership.

## Goals

- [x] Bound project discovery with the same deterministic planning and budget contract as other routes.
- [x] Reduce APEX skill discovery to one explicit diagnostic inspector.
- [x] Inventory lesson and session-context hygiene without deleting or disclosing content.
- [x] Add an opt-in, pinned, loopback-only local Figma pilot alongside the official server.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Changes to `repos/inventeer-ops` or its documentation | The user explicitly excluded that repository from their scope. |
| Replacing or disabling the official Figma MCP | The local bridge is a pilot with narrower capabilities and a different trust model. |
| Installing the Figma Desktop plugin | Installation is an external manual action in the user's Figma environment. |
| Deleting lessons or `session-context/` content | Eligibility needs explicit evidence and destructive cleanup requires separate authorization. |
| Executing APEX delivery workflows | AD-045 keeps TLC as executor and APEX diagnostic only. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Local Figma server identity | `figma-local` | Keeps the official `figma` server and its OAuth workflow unchanged. | y |
| Local Figma release | Pin `@alvinindra/figma-mcp-rust@0.2.0` | Avoids mutable `latest` resolution during an experimental pilot. | y |
| Local bridge network boundary | `127.0.0.1:1994` only | The bridge has no authentication and warns on non-loopback binding. | y |
| Pilot activation | Disabled by default in Codex and not auto-enabled in Claude | Avoids tool noise and accidental writes before the Desktop plugin is installed. | y |
| APEX discovery surface | Keep only `apex-all-tools` | One explicit inspector preserves diagnostics without one skill per workflow. | y |
| Hygiene eligibility | Require explicit merge/closure or runtime-end evidence | Local timestamps and directory names cannot prove lifecycle completion. | y |
| Remaining implicit dimensions | N/A for this scope | No product state, production calls, payments, migrations, or user data are changed. | y |

**Open questions:** none.

## User Stories

### P1: Bounded discovery and diagnostic skill surface

**User Story:** As the workspace maintainer, I want discovery and experimental diagnostics to load
only bounded context so that routine sessions do not pay for irrelevant workflow metadata.

**Why P1:** Context reconstruction and compaction are the dominant session-level cost.

**Acceptance Criteria:**

1. WHEN the context manifest is checked THEN the workspace SHALL validate a `project-discovery` route with an explicit token budget and closed source list.
2. WHEN project discovery starts THEN the skill SHALL plan the `project-discovery` route before reading registered project sources.
3. WHILE discovery is read-only, the skill SHALL inspect repository freshness without updating repositories unless the user separately authorizes synchronization.
4. WHEN APEX skills are discovered THEN the workspace SHALL expose exactly one `apex-all-tools` diagnostic skill and zero per-workflow APEX skills.
5. WHEN the APEX synchronization helper processes a catalog THEN it SHALL reconcile only the `all-tools` inspector and remove legacy generated APEX wrappers from its target.

**Independent Test:** Run the context and APEX synchronization focal suites and observe one bounded
discovery route plus one generated APEX inspector.

### P1: Read-only workspace hygiene inventory

**User Story:** As the workspace maintainer, I want a sanitized hygiene inventory so that I can
review stale lessons and ephemeral directories without accidental deletion or content disclosure.

**Why P1:** The current lifecycle is documented but not observable through one deterministic command.

**Acceptance Criteria:**

1. WHEN the hygiene inventory runs THEN the workspace SHALL emit lesson status counts and candidate expiry identifiers without lesson prose or evidence bodies.
2. WHEN a Portal issue directory lacks explicit merged and closed evidence THEN the inventory SHALL classify it as requiring external confirmation.
3. WHEN a Portal issue directory has both explicit merged and closed evidence THEN the inventory SHALL classify it as eligible without deleting it.
4. WHEN an OMC runtime directory lacks explicit ended-session evidence THEN the inventory SHALL classify it as requiring liveness confirmation.
5. WHEN the inventory completes THEN the workspace SHALL preserve a byte-identical source tree.

**Independent Test:** Run the hygiene focal suite against disposable fixtures and compare the tree
fingerprint before and after inventory.

### P1: Parallel local Figma pilot

**User Story:** As the workspace maintainer, I want a constrained local Figma bridge available on
demand so that high-volume reads can be evaluated without weakening the managed official workflow.

**Why P1:** Official read limits can be too low for design-intensive work, while the local bridge
has a materially larger local trust surface.

**Acceptance Criteria:**

1. WHILE the pilot exists, the workspace SHALL keep the official `figma` OAuth server enabled and unchanged.
2. WHEN Codex loads configuration THEN it SHALL define `figma-local` with version `0.2.0`, loopback address `127.0.0.1`, port `1994`, prompt approval, and disabled-by-default state.
3. WHEN Claude reads `.mcp.json` THEN it SHALL find the same pinned loopback command without automatic enablement in project settings.
4. WHEN the local bridge is prepared for use THEN workspace guidance SHALL require a disposable Figma file, explicit file and node targets, and approval for every tool during the pilot.
5. IF the Desktop plugin is absent or disconnected THEN workspace guidance SHALL report the manual dependency instead of claiming the pilot was validated.

**Independent Test:** Run MCP configuration tests and inspect the exact server arguments and
activation boundaries without starting the external server.

## Edge Cases

- IF the APEX catalog omits `all-tools` THEN synchronization SHALL fail without creating an alternative wrapper.
- IF hygiene evidence names an invalid issue or runtime THEN the inventory SHALL fail without mutation.
- IF an unknown `session-context/portal` directory is present THEN the inventory SHALL preserve and classify it as protected/unclassified.
- IF a configuration uses `latest`, a non-loopback address, or auto-enables `figma-local` THEN the MCP configuration gate SHALL fail.

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| WOSS-01 | Bounded discovery | ISSUE | T1; context focal gate | Execute | Verified |
| WOSS-02 | Read-only discovery freshness | INHERITED | T1; discovery skill contract | Execute | Verified |
| WOSS-03 | Single APEX inspector | DECISION | T2; sync focal gate | Execute | Verified |
| WOSS-04 | Sanitized lesson inventory | ISSUE | T3; hygiene focal gate | Execute | Verified |
| WOSS-05 | Evidence-gated session cleanup eligibility | SAFETY | T3; conjunction and non-mutation fixtures | Execute | Verified |
| WOSS-06 | Preserve official Figma | DECISION | T4; MCP configuration gate | Execute | Verified |
| WOSS-07 | Pinned loopback local Figma | SAFETY | T4; exact configuration assertions | Execute | Verified |
| WOSS-08 | Manual plugin dependency | DEPENDENCY | T4; README and AGENTS contract | Execute | Verified |
| WOSS-09 | Exclude `inventeer-ops` | DECISION | T1–T5 scope and diff inspection | Execute | Verified |

**Coverage:** 9 total, 9 mapped to tasks, 0 unmapped.

## Success Criteria

- [x] Six deterministic context routes pass within budget.
- [x] Exactly one APEX diagnostic skill remains and its sync is idempotent.
- [x] Hygiene inventory proves no mutation and never emits stored content.
- [x] Official and local Figma configurations coexist with the pilot disabled by default.
- [x] The aggregate workspace gate passes without modifying the user's lesson files.
