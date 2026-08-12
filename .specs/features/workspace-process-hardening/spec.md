# Workspace Process Hardening Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

The bounded resilience pilot reached its closing trigger but remained marked active, while recent
sessions continued to require resumptions and the workspace still loads broad context manually.
The EDREN repository validated bounded context packages, staged-content guardrails, pre-heavy
checkpoints, and recoverable gate evidence, but those mechanisms must be adapted to this workspace's
dual-engine, multi-repository, and ownership boundaries.

## Goals

- [x] Close the resilience pilot with a reproducible aggregate comparison and an explicit decision.
- [x] Route each common workflow through a deterministic, reference-only context package.
- [x] Prevent likely sensitive or unsuitable staged content through an opt-in local Git hook.
- [x] Require a fresh Portal TLC checkpoint before a heavy stage.
- [ ] Preserve a sanitized, state-bound receipt for the root workspace gate.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Gate runners for repositories under `repos/` | Product repositories remain canonical for their commands, tests, and local decisions. |
| Automatic hook installation | Changing a clone's Git configuration remains an explicit local action. |
| Transcript or session-identity persistence | AD-027 and AD-041 prohibit turning histories into durable workspace evidence. |
| Replacing fresh terminal validation | A reusable receipt cannot replace validation that is explicitly fresh, external, or bound to a new diff. |
| Codex-only or single-agent workspace policy | AD-024 and AD-026 preserve dual-engine routing. |
| Replacing TLC atomic commits with EDREN value increments | Issue, repository, and PR boundaries remain the safer delivery unit here. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Delivery scope | Implement the five-step sequence recommended in the retrospective | The user approved proceeding after reviewing that exact sequence. | y |
| Context representation | Versioned JSON manifests containing references, sections, reasons, and gates, never source contents | This preserves canonical ownership and makes routing deterministic. | y |
| Context routes | Cover Portal task, Assistants task, PR review, cycle triage, and delivery-front continuation | These are the workspace's five explicit operational routes. | y |
| Hook lifecycle | Version the hook and installer, but never run the installer automatically | This preserves clone-local consent and is consistent with EDREN's validated approach. | y |
| Gate evidence scope | Support only the root `workspace` profile | A cross-repository runner would duplicate product authority. | y |
| Gate evidence location | Store the ignored receipt below `session-context/runtime/` | AD-017 already owns ephemeral session material and the path is excluded from Git. | y |
| Existing dirty changes | Preserve and exclude the in-progress Figma changes from this feature's commits | Existing work belongs to the user and is outside this feature. | y |
| Remaining implicit dimensions | Auth, rate limits, remote dependencies, and customer-data lifecycle are N/A because all new operations are local, offline, and metadata-only | The feature adds no remote interface, account access, or product data flow. | y |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: Close the Resilience Pilot

**User Story:** As the workspace maintainer, I want the bounded pilot closed from its approved
evidence boundary so that later automation rests on an explicit decision.

**Acceptance Criteria:**

1. WHEN the closing review is recorded THEN the pilot SHALL contain contract version 2, the exact post-baseline window, one excluded current session, and aggregate Codex and Claude results. `WPH-01`
2. WHEN post-pilot interruption concentration is compared with the baseline THEN the pilot SHALL report abort and compaction rates, maxima, continuations, and the measurement limitations without persisting session identity or transcript location. `WPH-02`
3. WHEN the closing trigger and recurring reconstruction threshold are satisfied THEN the workspace decision log SHALL close the pilot and authorize only the scoped automation defined by this feature. `WPH-03`

**Independent Test:** The session-resilience contract asserts the closed lifecycle, exact aggregate
values, privacy boundary, trigger, limitations, and decision-log authorization.

### P1: Route Bounded Context

**User Story:** As an agent starting workspace work, I want a deterministic context package so that
I load the canonical sources for one route without copying unrelated content.

**Acceptance Criteria:**

1. WHEN a supported route is planned THEN the context planner SHALL emit a stable ordered list of source, optional section, reason, and gate references without emitting source contents. `WPH-04`
2. IF a manifest contains an unknown route, duplicate source, absolute path, path traversal, missing local reference, or unknown field THEN the context planner SHALL fail closed with exit code 2. `WPH-05`
3. WHEN the context manifest is audited THEN it SHALL cover exactly the Portal task, Assistants task, PR review, cycle triage, and delivery-front routes. `WPH-06`
4. WHEN workspace feature or decision navigation is requested THEN versioned indexes SHALL classify every feature directory and every active or superseded decision without becoming a second source of truth. `WPH-07`

**Independent Test:** Fixture manifests exercise deterministic output and every invalid lifecycle;
the workspace-structure test verifies complete feature and decision index coverage.

### P1: Guard Staged Content

**User Story:** As the workspace maintainer, I want a fast local staged-content guard so that likely
credentials and unsuitable artifacts are rejected before commit.

**Acceptance Criteria:**

1. WHEN staged content contains a forbidden environment/key/dump path, a private-key marker, a high-confidence token, an unexpected binary, or a blob larger than 5 MiB THEN the guard SHALL reject the commit with a path-only diagnostic and exit code 1. `WPH-08`
2. WHEN staged content is text without a forbidden signal THEN the guard SHALL exit 0 without changing the index or worktree. `WPH-09`
3. WHEN hook installation is explicitly invoked THEN the installer SHALL set only `core.hooksPath=.githooks`, and repeated installation SHALL be idempotent. `WPH-10`
4. IF the guard cannot inspect the Git index or encounters an unsafe filename encoding THEN it SHALL fail closed without printing staged content. `WPH-11`

**Independent Test:** A temporary repository stages safe, forbidden, binary, oversized, and
credential-shaped fixtures and verifies exact outcomes plus index/worktree preservation.

### P1: Preserve Stable Transitions

**User Story:** As an agent running a long Portal delivery, I want a fresh checkpoint before heavy
work and a recoverable root-gate result so that a platform interruption does not force unsafe
reconstruction or unnecessary repetition.

**Acceptance Criteria:**

1. WHEN a Portal Codex TLC workflow is about to start a heavy stage THEN the checkpoint helper SHALL accept `pre-heavy` and persist the same sanitized handoff schema used by other successful transitions. `WPH-12`
2. IF a checkpoint event is unknown, a field is multiline, or a resolved path escapes the workspace THEN the checkpoint helper SHALL reject the update without changing prior state. `WPH-13`
3. WHEN the allowlisted root workspace gate terminates THEN the runner SHALL atomically persist its latest terminal result before returning, including only schema, profile, result, exit code, integer duration, UTC time, state hash, and contract hash. `WPH-14`
4. WHEN the latest root-gate receipt passed and current state and contract hashes match THEN the status command SHALL return `reusable` with exit code 0. `WPH-15`
5. IF the receipt is absent, failed, interrupted, malformed, symlinked, too permissive, or bound to changed state or contract THEN the status command SHALL return `rerun-required` with an allowlisted reason and a non-zero exit code. `WPH-16`
6. WHILE the root gate evidence feature is in use, it SHALL NOT persist or emit transcript content, child output, commands, session IDs, history paths, workspace paths, filenames, credentials, or product data. `WPH-17`

**Independent Test:** Checkpoint fixtures cover the new event and all existing guards; gate-evidence
fixtures cover pass, fail, invalidation, corruption, permissions, symlinks, atomic failure, and the
closed output schema.

## Edge Cases

- IF a route points to a repository that is intentionally absent THEN the planner SHALL report the missing reference without cloning or mutating anything. `WPH-18`
- IF the root workspace changes while its gate is running THEN the runner SHALL persist a non-reusable `state-changed` result. `WPH-19`
- IF a new failed gate follows a reusable success THEN the latest failed result SHALL invalidate the earlier success. `WPH-20`
- WHEN validation is explicitly required to be fresh THEN a reusable receipt SHALL NOT satisfy that validation requirement. `WPH-21`

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| WPH-01 | Close pilot | DECISION | User-approved retrospective and AD-041 | Execute | Verified |
| WPH-02 | Close pilot | DECISION | User-approved retrospective and AD-041 | Execute | Verified |
| WPH-03 | Close pilot | DECISION | User-approved retrospective and AD-041 | Execute | Verified |
| WPH-04 | Bounded context | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-05 | Bounded context | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-06 | Bounded context | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-07 | Bounded context | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-08 | Staged guard | SAFETY | Workspace security contract and user approval | Execute | Verified |
| WPH-09 | Staged guard | SAFETY | Workspace security contract and user approval | Execute | Verified |
| WPH-10 | Staged guard | SAFETY | Workspace security contract and user approval | Execute | Verified |
| WPH-11 | Staged guard | SAFETY | Workspace security contract and user approval | Execute | Verified |
| WPH-12 | Pre-heavy checkpoint | DECISION | User-approved EDREN adaptation and AD-036 | Execute | Verified |
| WPH-13 | Pre-heavy checkpoint | DECISION | User-approved EDREN adaptation and AD-036 | Execute | Verified |
| WPH-14 | Recoverable gate | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-15 | Recoverable gate | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-16 | Recoverable gate | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-17 | Recoverable gate | DECISION | User-approved EDREN adaptation | Execute | Verified |
| WPH-18 | Edge cases | SAFETY | Ownership, integrity, and freshness boundaries | Execute | Verified |
| WPH-19 | Edge cases | SAFETY | Ownership, integrity, and freshness boundaries | Execute | Verified |
| WPH-20 | Edge cases | SAFETY | Ownership, integrity, and freshness boundaries | Execute | Verified |
| WPH-21 | Edge cases | SAFETY | Ownership, integrity, and freshness boundaries | Execute | Verified |

**Coverage:** 21 total, 21 mapped to tasks, 0 unmapped.

## Success Criteria

- [x] The AD-041 pilot is closed with a reproducible aggregate comparison and explicit limitations.
- [x] Five supported workflow routes produce deterministic reference-only context plans.
- [x] Staged sensitive and unsuitable fixtures fail while safe staged text passes unchanged.
- [x] Portal checkpoints support `pre-heavy` without weakening existing validation.
- [x] A passed root gate is reusable only for the identical workspace state and gate contract.
- [ ] `bash scripts/test-workspace.sh` and independent validation pass.
