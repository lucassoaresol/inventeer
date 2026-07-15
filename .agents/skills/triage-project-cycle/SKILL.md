---
name: triage-project-cycle
description: Compare multiple Inventeer Linear issues from one project, cycle, backlog slice, or delivery front; identify formal dependencies, code-level collisions, clarification gaps, readiness, and a recommended execution order without preparing every issue as a full single-task context package. Use for cycle planning, backlog triage, choosing among several INV-* issues, sequencing a delivery wave, or reviewing whether a group of tasks is ready to start. Do not use for implementing one selected issue; hand that issue to its product task-context skill.
---

# Project Cycle Triage

Prepare an evidence-backed comparative plan for a group of issues without mutating Linear or product
repositories.

## Required Input

Require a project or product identity and one issue selection mechanism:

- explicit `INV-*` identifiers;
- Linear cycle, initiative, project, milestone, assignee, or backlog filter;
- a user-provided issue list.

If the selection spans products, split the report by product and flag cross-product dependencies.

## Workflow

1. Read `projects/README.md` and the matching `projects/<project>.md` entry point. Treat the registry
   as routing metadata, not as a canonical product source.
2. Run `./scripts/update-repos.sh`. Continue with an explicit freshness warning for required repos
   that were skipped; stop when a required repo fails to update. Ignore the expected
   `inventeer-hub` skip.
3. Retrieve the selected issues and their relations from Linear without mutating them. Confirm each
   issue belongs to the expected product root. Resolve only the ancestry needed to establish shared
   outcomes, inherited DoDs, or a governance boundary; do not expand every issue into a full context
   package.
4. Normalize the comparison set: identity, type, status, priority, estimate, owner, objective,
   parent outcome, formal blockers, blocked issues, and related issues.
5. Read local instructions and check the worktree for each likely implementation repo. Inspect code,
   tests, ADRs, artifacts, and specs only deeply enough to validate dependencies, shared contracts,
   likely file ownership, and collision risks.
6. Distinguish evidence explicitly:
   - `FORMAL`: represented by Linear hierarchy or relations;
   - `INHERITED`: imposed by a parent outcome, DoD, canonical contract, or active decision;
   - `CODE`: supported by current implementation, tests, or shared files;
   - `INFERENCE`: a reasoned sequencing or collision hypothesis;
   - `QUESTION`: missing information that changes readiness or order.
7. Evaluate every issue for objective clarity, acceptance criteria, dependency closure, testability,
   operational prerequisites, and ownership. Do not treat `Ready to Start` as proof of readiness.
8. Build execution waves from formal blockers first, then code-level collision and integration risk.
   Keep independent work parallelizable and explain every inferred ordering constraint.
9. Recommend the first issue or clarification action that maximizes safe downstream progress.

## Triage Package

Return a concise report containing:

1. Selection identity, project, freshness evidence, and issues included or excluded.
2. Shared outcome and governing context.
3. Comparison table with readiness and the primary reason for each verdict.
4. Formal dependency graph or ordered list.
5. Code-level collisions and cross-repo risks, clearly separated from Linear relations.
6. Execution waves with parallelizable and sequential work.
7. Clarifications required before starting, grouped by issue.
8. One recommended first action.

## Handoff

After the user selects one issue, invoke the matching product task-context skill and pass only the
triage evidence relevant to that issue. Use `tlc-spec-driven` only after the single-issue context is
prepared and its recommended next action requires specification, implementation, or validation.

## Boundaries

- Do not modify Linear or any repository during triage.
- Do not create specs, branches, commits, or implementation plans for every issue.
- Do not invent dependencies from shared labels, dates, or proximity in a cycle.
- Do not present a code collision as a formal Linear blocker.
- Do not load complete canonical contracts for every issue; load only what can change comparative
  readiness or ordering.
- Do not replace the product task-context skill for the issue ultimately selected.
