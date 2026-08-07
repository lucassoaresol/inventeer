---
name: portal-task-context
description: Prepare an Inventeer Portal Linear issue for understanding, specification, implementation, solution/context review, or validation by resolving its ancestry to PROD INV-254, loading product context from repos/portal, consulting canonical IDS standards when the behavior touches the delivery pipeline, identifying implementation ownership across repos/portal-api and repos/portal-web, and locating relevant code, tests, contracts, decisions, artifacts, and specs. Use when starting, resuming, reviewing the task contract or implementation context, or clarifying an INV-* issue that belongs to the Portal product. For review or re-review of an existing GitHub pull request, use review-pull-request first and invoke this skill only when full hierarchy, inherited DoD, IDS, or ownership preparation is materially required.
---

# Portal Task Context

Prepare evidence-backed, cross-repository development context before proposing or changing Portal
implementation.

## Required Input

Require one Linear issue identifier in the form `INV-NNNN`. Capture the user's intent when stated:
understand, specify, design, implement, review, or validate.

Treat `review` here as full task-contract or implementation-context preparation. For an existing
GitHub PR, defer to `review-pull-request`; if it escalates here, return the full ancestry context it
requested without re-collecting GitHub diff, reviews, threads, commits, or checks.

## Workflow

1. From the workspace root, run `./scripts/update-repos.sh` before retrieving context. Inspect its
   output: stop and report when `portal`, `portal-api`, `portal-web`, or a required `ids` repo fails
   to update; continue with an explicit freshness warning when a required repo is skipped. Ignore
   the expected `inventeer-hub` skip.
2. Retrieve the issue from Linear without mutating it.
3. Resolve its complete parent chain until reaching `INV-254`.
4. Read [linear-context.md](references/linear-context.md) and validate hierarchy and inherited DoD
   coverage.
5. Resolve `repos/portal`, `repos/portal-api`, `repos/portal-web`, and, when required by the domain,
   `repos/ids`. If a required repo is absent, report it and stop; never clone automatically.
6. Read [repository-topology.md](references/repository-topology.md).
7. Load product meaning and constraints from `repos/portal` before deciding implementation ownership.
8. Read [ids-context.md](references/ids-context.md), classify whether the task has an IDS dimension,
   and load only the relevant canonical standards from `repos/ids` when it does.
9. Classify the target behavior as product/docs, API/backend, web/frontend, or cross-repo.
10. For every repo in scope, read its local agent instructions and check its Git worktree before any
   proposed mutation.
11. Follow the code-first verification chain in the implementation repo or repos:
   - existing implementation and neighboring patterns;
   - relevant tests and shared contracts;
   - local specs, ADRs, artifacts, and documentation;
   - Git history only when the current rationale remains unclear.
12. Establish the review contract before creating artifacts or asking the user to decide gray areas:
    - default the review language to Portuguese and the canonical artifact language to English;
    - honor an explicit user preference over those defaults;
    - infer the user's domain familiarity and include a functional walkthrough when understanding is
      not already demonstrated;
    - mark artifacts as `Draft` until the user explicitly approves their content;
    - state the contract in the context package handed to downstream workflows.
    Present the review package in chat by default. Create a separate review file only when the user
    requests one. After approval, hand the approved package to the downstream workflow to create or
    update canonical artifacts in the canonical language; do not require a second approval solely for
    translation unless meaning changes.
    When the active engine is Codex and the downstream executor is TLC, include the transitional
    artifact contract in the handoff: route file-backed TLC working artifacts to
    `session-context/portal/<INV-ID>/tlc/` from the workspace root and review bundles to
    `session-context/portal/<INV-ID>/review/`. These files support local execution, recovery, and
    review; they must not be presented as canonical, durable, or official APEX evidence. Do not
    create or promote `.specs/` in `repos/portal`, `repos/portal-api`, or `repos/portal-web` for TLC.
    Keep Claude/APEX and non-Portal routes unchanged. Mark the local task directory eligible for
    cleanup only after merge and issue closure, and retire this substitution when Codex supports an
    end-to-end APEX execution.
13. Build the user's mental model before requesting decisions: explain the problem, current and
    expected behavior, end-to-end flow, repository ownership, dependencies, scope boundaries, and
    why each unresolved choice matters. Orient with evidence, present options and consequences,
    recommend, then ask for a decision. Keep this adaptive for simple tasks and experienced users.
14. When the task involves an external tool, service, runtime, environment, credential, or network
    boundary, assess operational readiness: where it runs, required binary/configuration, identity
    and credentials, connectivity, local reproduction, staging validation, and dependencies on
    other teams. Separate code changes from provisioning or access work.
15. Separate discovered facts, supported inferences, and unresolved questions. Classify each
    requirement or constraint by provenance: `ISSUE`, `INHERITED`, `SAFETY`, `DECISION`,
    `DEPENDENCY`, or `RECOMMENDATION`. Do not silently promote a recommendation or dependency into
    issue scope.
16. Read [specification-policy.md](references/specification-policy.md) and determine readiness for
    the user's intended action.
17. Return the context package below and recommend exactly one next action.

## Provenance

Use exactly one primary provenance for each requirement or constraint:

- `ISSUE`: stated directly by the target Linear issue.
- `INHERITED`: imposed by its ancestry, declared DoD, canonical IDS standard, or active decision.
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
2. Full ancestry from `INV-254` to the target issue.
3. Inherited INIT, PROJ, and MILE outcomes and declared DoD coverage.
4. Product behavior and constraints found in `repos/portal`.
5. IDS standards consulted and constraints inherited, or `IDS context: not applicable` with reason.
6. Repository ownership verdict: portal, portal-api, portal-web, or an explicit combination.
7. Relevant implementation files, contracts, and observed patterns.
8. Relevant tests and currently asserted behaviors.
9. Applicable decisions, artifacts, ADRs, and specs.
10. Review contract: review language, canonical language, required walkthrough depth, artifact
    status, approval gate, and, for Codex + TLC, the Portal session-artifact path and authority
    boundary.
11. Mental model: problem, current behavior, expected behavior, end-to-end flow, repository
    ownership, dependencies, and scope boundaries. Omit only details the user has demonstrated.
12. Operational readiness when applicable: execution location, binary/configuration, identity,
    credentials, connectivity, local reproduction, staging validation, external ownership, and the
    boundary between code and provisioning.
13. Requirements and constraints with provenance (`ISSUE`, `INHERITED`, `SAFETY`, `DECISION`,
    `DEPENDENCY`, or `RECOMMENDATION`).
14. Ambiguities, cross-repo risks, conflicts, missing information, and decisions still required,
    each explained before asking the user to choose.
15. Readiness verdict with evidence.
16. Exactly one recommended next action.

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
recommended action, hand off the prepared context and review contract to it. Keep review artifacts
in the review language. After explicit content approval, let the downstream workflow create or
update canonical artifacts in the canonical language. Do not duplicate its workflow.

For Portal work executed by Codex + TLC, treat `session-context/portal/<INV-ID>/tlc/` as a
Portal-specific substitution for TLC's file-backed working-artifact root. Create files there only
when the auto-sized TLC flow needs them. This substitution does not make the workspace a product
source and does not apply to official specifications or APEX artifacts.

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
- Do not create or promote `.specs/` in `repos/portal`, `repos/portal-api`, or `repos/portal-web`
  for a Codex + TLC delivery.
- Do not use this full-preparation workflow as the default entry point for an existing GitHub PR;
  preserve `review-pull-request` as the owner of progressive Linear scope and GitHub evidence.
- Flag conflicts between product intent, contracts, code, and governing standards.
