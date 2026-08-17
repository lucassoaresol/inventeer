# Portal Specification Policy

Read this reference after collecting Linear, product, and repository context.

## Principle

Linear is the operational source for the task. Product artifacts define intended Portal behavior.
Repo-local specs complement missing implementation precision; none should duplicate the others.

## Linear is sufficient when

The issue provides:

- one unambiguous objective;
- explicit scope and exclusions;
- precise and testable acceptance outcomes;
- relevant failure and edge-case behavior;
- declared MILE DoD coverage;
- clear repository ownership;
- applicable IDS constraints identified or explicitly not applicable;
- enough contract detail for affected API/web surfaces;
- no unresolved architectural or governance conflict.

Recommend direct implementation when these conditions hold and the code scan reveals no additional
ambiguity.

## Create or complete a spec when

- product behavior admits multiple interpretations;
- acceptance outcomes are subjective or not testable;
- authority, lifecycle transitions, audit, authentication, persistence, concurrency, retries, or
  external calls are underspecified;
- API and web responsibilities or shared contract changes are unclear;
- partial DoD coverage does not define the exact contribution;
- existing code or tests expose an unstated compatibility requirement.

Portal does not accept TLC `.specs/` artifacts as official product artifacts. When TLC in Codex or
Claude Code needs a file-backed working specification, store it under
`session-context/portal/<INV-ID>/tlc/` and keep it explicitly local, ephemeral, non-canonical, and
non-durable. Working TLC artifacts are not product specifications and must not be promoted into
`repos/inventeer-ops/artifacts/products/portal`, `repos/portal-api`, or `repos/portal-web`.

If the task requires a durable official specification rather than a working TLC contract, follow
the APEX artifact lifecycle. Until that route is available in the active engine, surface the durable
artifact need as a delivery constraint instead of presenting the session copy as a substitute. Do
not write Portal product specs into this personal workspace.

## Design and ADR boundary

- Use feature design for implementation choices scoped to one delivery.
- Record durable API decisions in the API repo and durable frontend decisions in the Web repo.
- Recommend a cross-repo architectural decision when ownership or shared contract direction changes.
- Stop and surface contradictions with accepted product artifacts, IDS contracts, Hub standards, or
  existing ADRs.

## Relationship with TLC

Use `tlc-spec-driven` after context preparation when the next action is specification, design,
implementation, or validation. Pass it:

- the target Linear issue and full ancestry;
- inherited outcomes and declared coverage;
- product constraints from `repos/inventeer-ops/artifacts/products/portal`;
- applicable canonical constraints from `repos/inventeer-ops/artifacts/products/ids`;
- repository ownership and worktrees in scope;
- relevant code, tests, contracts, decisions, and specs;
- unresolved questions and readiness verdict.

Let TLC auto-size the depth. Do not recreate its phases in this skill.

In Codex and Claude Code, replace TLC's file-backed artifact root for this Portal task with
`session-context/portal/<INV-ID>/tlc/`. The replacement is a handoff constraint, not a modification
to the generic TLC skill. APEX remains diagnostic until a new decision follows an end-to-end
execution that satisfies AD-034.
