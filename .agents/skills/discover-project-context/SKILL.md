---
name: discover-project-context
description: Discover and explain an Inventeer project, workflow, integration, ownership boundary, or current implementation when no Linear issue exists or an issue identifier is intentionally unavailable. Use for architecture and process discovery, as-is flow mapping, cross-repository ownership analysis, preparing a discussion document, or deciding where a future task belongs. Do not use to bypass an existing issue's hierarchy or to implement changes; switch to the matching product task-context skill once an INV-* issue is in scope.
---

# Project Context Discovery

Build an evidence-backed model of a project or workflow without requiring a Linear issue and without
turning discovery into an implicit implementation task.

## Required Input

Require a registered project or product and a discovery question, workflow, component, or decision
to understand. Capture the intended audience and output when stated.

## Workflow

1. Read `projects/README.md` and the matching `projects/<project>.md` entry point. If no project is
   registered, report the missing route instead of guessing repositories.
2. Run `./scripts/update-repos.sh`. Continue with an explicit freshness warning for required repos
   that were skipped; stop when a required repo fails to update. Ignore the expected
   `inventeer-hub` skip.
3. Resolve the product, implementation, foundation, and conditional dependency repos from the
   project entry point. Read local instructions and check each repo worktree before analysis.
4. Establish authority before tracing behavior: identify which source owns product meaning, code,
   shared contracts, standards, tests, and operational state.
5. Follow the current flow from its observable entry point through repository and service
   boundaries. Prefer current code and tests, then active ADRs and artifacts, then Git history when
   the current rationale remains unclear.
6. Load IDS or foundation context only when the discovered behavior crosses a governed boundary.
   Reference canonical material without copying contract bodies.
7. Separate:
   - observed current behavior and ownership;
   - supported inferences;
   - proposed future boundaries or hypotheses;
   - unresolved questions and missing external context.
8. When an external system or absent repository is involved, describe only the observed interface
   and explicitly label assumptions about its internals.
9. Recommend where a durable output belongs: chat only, `session-context/`, a product discovery
   workspace, a canonical artifact, or a new Linear issue. Do not create the output unless requested.

## Discovery Package

Return a concise report containing:

1. Discovery objective, audience, project, and freshness evidence.
2. Sources consulted and their authority.
3. Repository or component ownership map.
4. Current end-to-end flow with inputs, outputs, state, and external boundaries.
5. Facts, supported inferences, hypotheses, and unresolved questions.
6. Risks, constraints, and missing evidence.
7. Recommended durable destination, if any.
8. One recommended next action.

Use a small flow, sequence, or swimlane visualization when it materially clarifies three or more
actors or state transitions.

## Handoff

If discovery identifies an existing `INV-*` issue, switch to the matching product task-context skill.
If it establishes enough evidence for new work, recommend creating or clarifying a Linear issue
before implementation. Hand approved specifications or implementation requests to
`tlc-spec-driven` only after the canonical work item and ownership boundary are clear.

## Boundaries

- Do not require or invent a Linear issue for discovery.
- Do not use discovery to bypass an existing issue, inherited DoDs, or approval requirements.
- Do not modify Linear or repositories unless the user separately authorizes that change.
- Do not silently turn a future-state hypothesis into current behavior or approved architecture.
- Do not copy governed contracts or standards into the workspace or product repos.
- Do not assume every repo in a multi-repo product is in scope.
