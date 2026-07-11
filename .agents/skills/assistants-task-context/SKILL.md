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

1. From the workspace root, run `./scripts/update-repos.sh` before retrieving context. Inspect its
   output: stop and report when `assistants` or a required `ids` repo fails to update; continue with
   an explicit freshness warning when a required repo is skipped. Ignore the expected
   `inventeer-hub` skip.
2. Retrieve the issue from Linear without mutating it.
3. Resolve its complete parent chain until reaching `INV-2228`.
4. Read [linear-context.md](references/linear-context.md) and validate the hierarchy and inherited
   DoD coverage.
5. Resolve `repos/assistants` and, when required by the domain, `repos/ids`. If a required repo is
   absent, report the missing clone and stop; never clone automatically.
6. Read the target repository's local agent instructions and check its Git worktree before any
   proposed mutation.
7. Read [ids-context.md](references/ids-context.md), classify whether the task has an IDS dimension,
   and load only the relevant canonical contracts or standards from `repos/ids` when it does.
8. Follow the code-first verification chain:
   - existing implementation and neighboring patterns;
   - relevant tests;
   - project documentation, artifacts, ADRs, and existing specs;
   - Git history only when the current rationale remains unclear.
9. Establish the review contract before creating artifacts or asking the user to decide gray areas:
   - default the review language to Portuguese and the canonical artifact language to English;
   - honor an explicit user preference over those defaults;
   - infer the user's domain familiarity from the conversation and include a functional walkthrough
     when understanding is not already demonstrated;
   - mark artifacts as `Draft` until the user explicitly approves their content;
   - state the contract in the context package handed to downstream workflows.
   Present the review package in chat by default. Create a separate review file only when the user
   requests one. After approval, hand the approved package to the downstream workflow to create or
   update canonical artifacts in the canonical language; do not require a second approval solely for
   translation unless meaning changes.
10. Build the user's mental model before requesting decisions: explain the problem, current and
    expected behavior, end-to-end flow, components, dependencies, scope boundaries, and why each
    unresolved choice matters. Use the sequence: orient with evidence, present options and
    consequences, recommend, then ask for a decision. Keep this adaptive for simple tasks and
    experienced users.
11. When the task involves an external tool, service, runtime, environment, credential, or network
    boundary, assess operational readiness: where it runs, required binary/configuration, identity
    and credentials, connectivity, local reproduction, staging validation, and dependencies on
    other teams. Separate code changes from provisioning or access work.
12. Separate discovered facts, supported inferences, and unresolved questions. Classify each
    requirement or constraint by provenance: `ISSUE`, `INHERITED`, `SAFETY`, `DECISION`,
    `DEPENDENCY`, or `RECOMMENDATION`. Do not silently promote a recommendation or dependency into
    issue scope.
13. Read [specification-policy.md](references/specification-policy.md) and determine whether the
    Linear issue is ready for the user's intended action.
14. Return the context package below and recommend exactly one next action.

## Provenance

Use exactly one primary provenance for each requirement or constraint:

- `ISSUE`: stated directly by the target Linear issue.
- `INHERITED`: imposed by its ancestry, declared DoD, canonical IDS contract, or active decision.
- `SAFETY`: necessary to prevent an identified security, privacy, availability, or destructive risk
  not already classified as inherited.
- `DECISION`: explicitly chosen or approved by the user during preparation.
- `DEPENDENCY`: required access, provisioning, external work, or prior capability that enables the
  issue but is not silently added to its implementation scope.
- `RECOMMENDATION`: optional improvement proposed by the agent and not required for readiness or
  compliance.

When multiple sources apply, keep the strongest scope-authorizing source as primary and cite the
others as supporting evidence. Never use `SAFETY` or `RECOMMENDATION` to override a canonical rule.

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
8. Review contract: review language, canonical language, required walkthrough depth, artifact
   status, and approval gate.
9. Mental model: problem, current behavior, expected behavior, end-to-end flow, components,
   dependencies, and scope boundaries. Omit only details the user has already demonstrated.
10. Operational readiness when applicable: execution location, binary/configuration, identity,
    credentials, connectivity, local reproduction, staging validation, external ownership, and the
    boundary between code and provisioning.
11. Requirements and constraints with provenance (`ISSUE`, `INHERITED`, `SAFETY`, `DECISION`,
    `DEPENDENCY`, or `RECOMMENDATION`).
12. Ambiguities, conflicts, missing information, and decisions still required, each explained before
    asking the user to choose.
13. Readiness verdict with evidence.
14. Exactly one recommended next action.

## Allowed Next Actions

- Implement directly.
- Complete or clarify the Linear issue.
- Create or complete a feature specification.
- Produce a technical design.
- Record an architectural decision.
- Resolve a governance conflict.
- Validate an existing implementation.

When `tlc-spec-driven` is available and specification, design, implementation, or validation is the
recommended action, hand off the prepared context and review contract to it. Keep review artifacts
in the review language. After explicit content approval, let the downstream workflow create or
update canonical artifacts in the canonical language. Do not duplicate its workflow.

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
