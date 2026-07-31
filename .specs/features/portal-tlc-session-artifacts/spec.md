# Portal TLC Session Artifacts Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

Portal does not officially accept TLC `.specs/` artifacts in product branches, while Codex still
requires TLC for specification, implementation, and validation because it cannot execute the full
APEX workflow. The workspace needs a transitional, Portal-only location for TLC working artifacts
that supports local execution and session recovery without claiming canonical or durable status.

## Goals

- Keep Codex/TLC working artifacts outside `repos/portal`, `repos/portal-api`, and `repos/portal-web`.
- Give each Portal issue a predictable local path for TLC artifacts and review evidence.
- Preserve the authority of Linear, product repositories, and APEX artifacts.
- Pilot the route on a real Portal delivery before treating it as consolidated practice.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Making `session-context/` durable or portable | The directory is intentionally local and ignored by Git. |
| Changing the vendored TLC workflow | The policy is Portal-specific and belongs in the Portal handoff. |
| Changing Claude/APEX delivery | APEX already owns its official artifact lifecycle. |
| Applying the route to Assistants or IDS | No equivalent acceptance constraint has been established. |
| Creating product specifications in the personal workspace | Product meaning remains canonical in product sources. |

## Assumptions and Decisions

| Decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Artifact root | `session-context/portal/<INV-ID>/tlc/` | Keeps TLC working state outside product branches. | Yes |
| Review evidence | `session-context/portal/<INV-ID>/review/` | Keeps bundles and lineage grouped with the task. | Yes |
| Authority | Working support only | The local directory must not compete with Linear, product repos, or APEX. | Yes |
| Lifecycle | Remove after merge and issue closure | The directory is temporary session state. | Yes |
| Exit condition | Retire when Codex executes APEX end to end | APEX is the accepted official artifact mechanism. | Yes |

**Open questions:** none for the pilot. Cross-machine portability remains explicitly unsupported.

## P1: Route Portal TLC Working Artifacts

**User Story:** As a Portal developer using Codex, I want TLC working artifacts outside product
branches so that I can execute and resume a task without publishing unsupported `.specs/` files.

**Acceptance Criteria:**

1. WHEN Portal context hands specification, design, implementation, or validation to TLC in Codex,
   THEN the handoff SHALL route file-backed TLC artifacts to
   `session-context/portal/<INV-ID>/tlc/`.
2. WHEN TLC operates through this route, THEN it SHALL NOT create or promote `.specs/` in
   `repos/portal`, `repos/portal-api`, or `repos/portal-web`.
3. WHEN an artifact is stored in the session path, THEN workspace instructions SHALL classify it as
   local, ephemeral, non-canonical, and non-durable.
4. WHEN official delivery evidence is summarized, THEN Linear, product code/tests/docs, and the PR
   SHALL remain the official delivery surfaces; local TLC files SHALL NOT be presented as official
   APEX artifacts.
5. WHEN review bundles are generated for the task, THEN they SHOULD be stored under
   `session-context/portal/<INV-ID>/review/`.
6. WHEN the issue is merged and closed, THEN the local task directory SHALL be eligible for removal.
7. WHEN Codex can execute APEX end to end for Portal, THEN this transitional route SHALL be retired
   in favor of the official APEX artifact lifecycle.
8. WHEN the route is documented, THEN Claude/APEX, other products, and the vendored TLC skill SHALL
   remain unchanged.

**Independent Test:** Run `scripts/test-portal-tlc-session-artifacts.sh` and confirm every contract
assertion passes without creating a task directory or touching a product repository.

## Edge Cases

- A precise Linear issue may require only an inline TLC specification; file-backed artifacts use the
  session path only when TLC creates them.
- A task requiring an official durable specification cannot promote the local working copy; it must
  follow the Portal-approved artifact route or wait for APEX.
- A new machine cannot assume the local task directory exists and must reconstruct context from
  canonical sources or receive an explicitly transferred temporary package.

## Requirement Traceability

| Requirement | Provenance | Evidence | Status |
| --- | --- | --- | --- |
| PTSA-01 | DECISION | User-approved Portal path | Verified |
| PTSA-02 | INHERITED | Portal rejects TLC `.specs/` in product branches | Verified |
| PTSA-03 | INHERITED | AD-017 session-context lifecycle | Verified |
| PTSA-04 | INHERITED | Workspace canonical-source boundaries | Verified |
| PTSA-05 | DECISION | User-approved review grouping | Verified |
| PTSA-06 | DECISION | User-approved cleanup lifecycle | Verified |
| PTSA-07 | INHERITED | AD-026 APEX execution boundary | Verified |
| PTSA-08 | DECISION | Portal-only scope | Verified |
