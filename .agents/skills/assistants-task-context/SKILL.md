---
name: assistants-task-context
description: Prepare an Inventeer Assistants Linear issue for understanding, specification, implementation, review, or validation by resolving its ancestry to PROD INV-2228, tracing inherited DoDs, consulting canonical IDS contracts when the work touches governed delivery, inspecting the target repository, and locating relevant code, tests, decisions, artifacts, and existing specs. Use when starting, resuming, reviewing, or clarifying an INV-* issue that belongs to the Assistants product.
---

# Assistants Task Context

Prepare evidence-backed development context before proposing or changing implementation.

## Required Input

Require one Linear issue identifier in the form `INV-NNNN`. Capture the user's intent when stated:
understand, specify, design, implement, review, or validate.

## Workflow

1. Retrieve the issue from Linear without mutating it.
2. Resolve its complete parent chain until reaching `INV-2228`.
3. Read [linear-context.md](references/linear-context.md) and validate the hierarchy and inherited
   DoD coverage.
4. Resolve `repos/assistants` and, when required by the domain, `repos/ids`. If a required repo is
   absent, report the missing clone and stop; never clone automatically.
5. Read the target repository's local agent instructions and check its Git worktree before any
   proposed mutation.
6. Read [ids-context.md](references/ids-context.md), classify whether the task has an IDS dimension,
   and load only the relevant canonical contracts or standards from `repos/ids` when it does.
7. Follow the code-first verification chain:
   - existing implementation and neighboring patterns;
   - relevant tests;
   - project documentation, artifacts, ADRs, and existing specs;
   - Git history only when the current rationale remains unclear.
8. Separate discovered facts, supported inferences, and unresolved questions.
9. Read [specification-policy.md](references/specification-policy.md) and determine whether the
   Linear issue is ready for the user's intended action.
10. Return the context package below and recommend exactly one next action.

## Context Package

Return a concise report containing:

1. Issue identity, type, status, owner, and stated objective.
2. Full ancestry from `INV-2228` to the target issue.
3. Inherited INIT, PROJ, and MILE outcomes and declared DoD coverage.
4. IDS contracts or standards consulted and inherited constraints, or `IDS context: not applicable`
   with reason.
5. Relevant implementation files and observed patterns.
6. Relevant tests and currently asserted behaviors.
7. Applicable decisions, artifacts, ADRs, and specs.
8. Ambiguities, conflicts, and missing information.
9. Readiness verdict with evidence.
10. Exactly one recommended next action.

## Allowed Next Actions

- Implement directly.
- Complete or clarify the Linear issue.
- Create or complete a feature specification.
- Produce a technical design.
- Record an architectural decision.
- Resolve a governance conflict.
- Validate an existing implementation.

When `tlc-spec-driven` is available and specification, design, implementation, or validation is the
recommended action, hand off the prepared context to it. Do not duplicate its workflow.

## Boundaries

- Do not modify Linear during discovery.
- Do not modify a repository unless the user requested a change or implementation.
- Do not copy DAP, EPP, or DEP contract bodies into this workspace or a product repository.
- Do not infer governing IDS rules from Assistants artifacts or code when a canonical contract exists.
- Do not amend IDS contracts from an Assistants task; surface the governance dependency.
- Do not invent missing parent relationships, outcomes, or DoDs.
- Do not create a local spec when Linear already defines a precise, testable contract.
- Do not treat historical or superseded documents as current without explicit evidence.
- Flag conflicts between implemented reality and governing contracts instead of silently choosing.
