---
name: portal-task-context
description: Prepare an Inventeer Portal Linear issue for understanding, specification, implementation, review, or validation by resolving its ancestry to PROD INV-254, loading product context from repos/portal, consulting canonical IDS standards when the behavior touches the delivery pipeline, identifying implementation ownership across repos/portal-api and repos/portal-web, and locating relevant code, tests, contracts, decisions, artifacts, and specs. Use when starting, resuming, reviewing, or clarifying an INV-* issue that belongs to the Portal product.
---

# Portal Task Context

Prepare evidence-backed, cross-repository development context before proposing or changing Portal
implementation.

## Required Input

Require one Linear issue identifier in the form `INV-NNNN`. Capture the user's intent when stated:
understand, specify, design, implement, review, or validate.

## Workflow

1. Retrieve the issue from Linear without mutating it.
2. Resolve its complete parent chain until reaching `INV-254`.
3. Read [linear-context.md](references/linear-context.md) and validate hierarchy and inherited DoD
   coverage.
4. Resolve `repos/portal`, `repos/portal-api`, `repos/portal-web`, and, when required by the domain,
   `repos/ids`. If a required repo is absent, report it and stop; never clone automatically.
5. Read [repository-topology.md](references/repository-topology.md).
6. Load product meaning and constraints from `repos/portal` before deciding implementation ownership.
7. Read [ids-context.md](references/ids-context.md), classify whether the task has an IDS dimension,
   and load only the relevant canonical standards from `repos/ids` when it does.
8. Classify the target behavior as product/docs, API/backend, web/frontend, or cross-repo.
9. For every repo in scope, read its local agent instructions and check its Git worktree before any
   proposed mutation.
10. Follow the code-first verification chain in the implementation repo or repos:
   - existing implementation and neighboring patterns;
   - relevant tests and shared contracts;
   - local specs, ADRs, artifacts, and documentation;
   - Git history only when the current rationale remains unclear.
11. Separate discovered facts, supported inferences, and unresolved questions.
12. Read [specification-policy.md](references/specification-policy.md) and determine readiness for
    the user's intended action.
13. Return the context package below and recommend exactly one next action.

## Context Package

Return a concise report containing:

1. Issue identity, type, status, owner, and stated objective.
2. Full ancestry from `INV-254` to the target issue.
3. Inherited INIT, PROJ, and MILE outcomes and declared DoD coverage.
4. Product behavior and constraints found in `repos/portal`.
5. IDS standards consulted and constraints inherited, or `IDS context: not applicable` with reason.
6. Repository ownership verdict: portal, portal-api, portal-web, or an explicit combination.
7. Relevant implementation files, contracts, and observed patterns.
8. Relevant tests and currently asserted behaviors.
9. Applicable decisions, artifacts, ADRs, and specs.
10. Ambiguities, cross-repo risks, conflicts, and missing information.
11. Readiness verdict with evidence.
12. Exactly one recommended next action.

## Allowed Next Actions

- Implement directly in one identified repo.
- Plan an explicit cross-repo change.
- Complete or clarify the Linear issue.
- Create or complete a feature specification.
- Produce a technical design.
- Record an architectural decision.
- Resolve a governance or ownership conflict.
- Validate an existing implementation.

When `tlc-spec-driven` is available and specification, design, implementation, or validation is the
recommended action, hand off the prepared context to it. Do not duplicate its workflow.

## Boundaries

- Do not modify Linear during discovery.
- Do not modify any repo unless the user requested a change or implementation.
- Do not assume that one Portal task requires changes in all three repos.
- Do not move backend business rules or governance enforcement into `portal-web`.
- Do not redefine API-owned shared contracts locally in `portal-web`.
- Do not treat product artifacts in `portal` as substitutes for implementation and tests.
- Do not restate or copy IDS standards into Portal; reference canonical files and applicable sections.
- Do not infer IDS rules from Portal code when a canonical IDS standard exists.
- Do not invent missing parent relationships, outcomes, DoDs, or ownership.
- Do not create a local spec when Linear already defines a precise, testable contract.
- Flag conflicts between product intent, contracts, code, and governing standards.
