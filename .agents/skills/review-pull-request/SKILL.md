---
name: review-pull-request
description: Review an existing pull request, especially another developer's work, using GitHub, issue context, repository code, tests, and CI as read-only evidence anchored to exact base and head SHAs. Use when asked to review, re-review, assess, audit, or give a verdict on a PR; inspect whether requested changes were addressed; or follow up review outcomes after merge. Do not use to implement fixes, create a PR, post comments, approve, merge, or coordinate the next delivery task.
---

# Review Pull Request

Review the submitted change as an independent reviewer. Prefer concrete behavioral defects over
style preferences, and keep every conclusion traceable to the exact code surface observed.

Read [references/review-contract.md](references/review-contract.md) completely before reviewing.

## Workflow

1. Resolve the GitHub owner, repository, and PR number. If no unique PR can be identified, stop and
   request the missing reference.
2. Read the PR through the read-only GitHub MCP. Capture the observation time, state, author, base
   ref/SHA, head ref/SHA, commits, changed files, existing reviews, review threads, comments, and
   check runs. Treat missing or unavailable evidence explicitly; do not silently replace it with an
   assumption.
3. Extract any `INV-*` issue reference and load Linear context progressively:
   - read the target issue once and record its `updatedAt`, parent, relations, acceptance criteria,
     declared DoD coverage, and explicit dependencies;
   - use the PR linkback only to locate or cross-check the issue, never as a fresher replacement for
     Linear;
   - expand to a parent or related issue only when the target omits a requirement needed to judge the
     diff, explicitly inherits a DoD, exposes a relevant dependency, or leaves product ownership
     ambiguous; record each fetched identifier and the reason;
   - invoke the matching product task-context skill for full ancestry only when hierarchy validity,
     inherited outcome traceability, governed IDS behavior, or cross-repository ownership materially
     affects the verdict. Do not run full task preparation by default for an ordinary PR review.
   Keep Linear canonical for issue scope and GitHub canonical for the submitted review surface. Do
   not use Linear's PR mirror for diffs, commits, reviews, threads, or checks when GitHub is available.
   If no issue exists, use repository documentation and the PR contract; do not invent requirements.
4. Locate the repository clone when available. Read its local instructions and inspect its worktree
   before running commands. Never modify product files, branches, worktrees, GitHub, or Linear as
   part of this skill. Prefer the GitHub diff for remote identity and local code for surrounding
   context. If the exact head object is unavailable locally, declare the limitation instead of
   reviewing a different checkout as if it were the PR head.
5. Build a risk map from the requirements and diff. Prioritize behavior, data integrity, security,
   authorization, concurrency, compatibility, migrations, error handling, operations, and tests.
   Inspect unchanged callers and contracts when the changed code can affect them.
6. Run proportionate local validation only when it can be bound to the reviewed head. Before a
   heavy suite, build, container, browser, or high-concurrency step, run the workspace resource
   preflight and adapt concurrency without reducing required coverage. Keep remote checks distinct
   from local validation.
7. Record only actionable defects as findings. Put uncertain items under questions or limitations.
   Do not promote taste, optional refactoring, or undocumented preference into a defect. Present
   findings first, ordered by severity, using the contract format.
8. Immediately before the verdict, read the PR again and compare its current base SHA and head SHA
   with the reviewed identity. If either SHA changed, mark the review stale and inspect the changed
   surface before issuing a fresh verdict. Bind every PASS or approval recommendation to the final
   observed base and head SHAs.
9. Return the review in chat by default. During the pilot, append only the sanitized metadata schema
   from the contract below `session-context/review-pilot/` with
   `python3 scripts/pr-review-pilot.py record --input <json-file>` and report when recording is
   unavailable. This local ledger is ignored, ephemeral, non-canonical, and contains no comments,
   diffs, finding prose, credentials, customer data, production output, or transcripts. Do not post
   comments, request changes, approve, merge, or create durable product artifacts unless the user
   starts a separately authorized workflow with an appropriate writable integration.

## Re-review and outcome follow-up

For a re-review, preserve the earlier reviewed SHA and inspect only the delta plus affected context;
re-run any evidence invalidated by the new head. Re-read the target Linear issue once to compare its
`updatedAt`; reuse the previously fetched ancestry and dependencies when it is unchanged, and expand
only for a newly introduced requirement. Classify each earlier finding with the evidence states in
the contract rather than inferring acceptance from a resolved thread alone.

For post-merge follow-up, search later commits, PRs, issues, and checks for attributable corrections.
Count an escaped defect only with a linked corrective artifact or reproduced regression. Report
`no confirmed escape in the observed window` when none is found; never translate that into proven
zero defects.

## Boundaries

- Keep this workflow read-only. A request to fix findings belongs to the applicable product context
  plus delivery executor, not to this skill.
- Do not use `create-review-bundle` unless the user asks for a portable ZIP or external review
  package. GitHub evidence is sufficient for ordinary PR review.
- Do not use `advance-delivery-front` unless the question is what to work on while this PR waits.
- Do not treat an `apex-eng-review` resource inspection as an executed APEX workflow.
- Do not record an external review finding as a TLC lesson until an independent verifier confirms
  it under the TLC validation contract.
