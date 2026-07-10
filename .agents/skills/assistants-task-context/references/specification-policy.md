# Specification Policy

Read this reference after collecting Linear and repository context.

## Principle

Linear is the operational source for the task. A local spec complements missing behavioral precision;
it never copies the issue hierarchy or governance contracts.

## Linear is sufficient when

The issue provides all information needed for the intended change:

- one unambiguous objective;
- explicit scope and exclusions;
- precise and testable acceptance outcomes;
- relevant failure and edge-case behavior;
- declared MILE DoD coverage;
- applicable IDS constraints identified or explicitly not applicable;
- enough context to identify affected behavior;
- no unresolved architectural or governance conflict.

Recommend direct implementation when these conditions hold and the code scan reveals no additional
ambiguity.

## Create or complete a spec when

- behavior admits multiple valid interpretations;
- acceptance outcomes are missing, subjective, or not testable;
- external calls, authentication, persistence, concurrency, retries, or state transitions are
  underspecified;
- several modules participate in a behavior whose boundary is unclear;
- partial DoD coverage does not define the exact contribution;
- existing code or tests expose an unstated compatibility requirement.

When needed, write the spec inside the target product repository under its established `.specs/`
convention. Include the Linear identifier in the feature directory name when the project convention
allows it. Do not write product specs into this personal workspace.

## Design and ADR boundary

- Use a feature design for implementation choices scoped to one feature.
- Recommend an ADR when a decision affects multiple features, establishes a durable platform rule,
  changes module boundaries, selects infrastructure or persistence, or is expensive to reverse.
- Do not create an ADR for routine internal implementation choices.
- Stop and surface the issue when a proposed design contradicts a DAP, EPP, DEP, or accepted ADR.

## Relationship with TLC

Use `tlc-spec-driven` after context preparation when the recommended next action is specification,
design, implementation, or validation. Pass it:

- the target Linear issue and full ancestry;
- inherited outcomes and declared coverage;
- applicable canonical constraints from `ids`;
- relevant code and tests;
- applicable decisions and constraints;
- unresolved questions and readiness verdict.

Let TLC auto-size the depth. Do not recreate its Specify, Design, Tasks, Execute, or Verify phases in
this skill.
