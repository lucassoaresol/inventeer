# Delivery Front Continuity Policy

## Contents

- [Evidence and freshness](#evidence-and-freshness)
- [Evidence maturity](#evidence-maturity)
- [Front invariants](#front-invariants)
- [Candidate classification](#candidate-classification)
- [Delivery states](#delivery-states)
- [Delivery contracts](#delivery-contracts)
- [Reconciliation plans](#reconciliation-plans)
- [Promotion guard](#promotion-guard)
- [Failure handling](#failure-handling)
- [Report contract](#report-contract)

## Evidence and Freshness

Classify every statement with exactly one evidence class:

- `FORMAL`: Linear hierarchy/relations/status or GitHub PR base/head/draft/review/CI/merge state.
- `INHERITED`: repository instructions, branch protection, merge strategy, inherited DoD, canonical
  contract, or active workspace decision.
- `CODE`: current files, symbols, tests, migrations, refs, ancestry, merge bases, or changed paths.
- `INFERENCE`: reasoned collision or sequencing hypothesis not represented as a formal relation.
- `QUESTION`: missing information that can change safety, base, order, or state.

Record the source and capture time for every evidence group. For GitHub, record PR number, base,
head branch, head SHA, draft state, review state, checks, and open/merged/closed state. For Linear,
record issue, state, owner, cycle/order, formal relations, and update time when available. For each
repository, record branch, HEAD, integration ref and SHA, merge base, worktree status, linked
worktrees, changed paths, and boundary SHA when applicable.

Do not claim that a remote-tracking ref is current merely because it resolves locally. State the
resolved SHA and the freshness limitation. Recheck a PR's head SHA, base, and state immediately
before recommending promotion or reconciliation. If a required source changed, mark the previous
plan stale and rebuild only the affected conclusions.

Missing evidence never implies independence. Use `QUESTION`, retain conclusions supported by the
available sources, and block only transitions that require the missing source.

## Evidence Maturity

Track implementation and validation on separate axes. Report only the highest implementation state
directly supported by the current snapshot:

| Implementation | Required evidence |
| --- | --- |
| `working-tree` | Dirty tracked or untracked task changes exist; no complete committed range is proven. |
| `committed` | A task-only commit range is present locally and the relevant worktree diff is clean. |
| `pushed` | GitHub observes the same head SHA, but no complete ready-PR snapshot is available. |
| `pr-observed` | GitHub PR head/base/state and local or remote commit evidence agree. |

Track validation as `missing`, `pass`, `fail`, `stale`, or `pending-delivery`. A PASS is valid only
for the exact work SHA or explicitly fingerprinted working-tree surface, requirement contract, and
gate set named by its evidence block. Mark it `stale` when any of those change. Use
`pending-delivery` when behavioral validation passed but a delivery-only condition remains, such as
same-commit placement, an uncommitted validation artifact, or a final-base gate.

A review bundle is historical `CODE` evidence. Record its generation stage, checksum, parent
lineage, base/head, and capture time when available, but never use it alone as proof of current
GitHub state, validation, or freshness.

## Front Invariants

Apply these invariants per repository:

1. Permit at most one PR ready for review plus one task in implementation or one draft PR.
2. Permit at most one pending dependency level: ready PR A may have draft PR B; do not start C on B.
3. Prefer an issue that is independent of the pending PR when it remains compatible with the cycle
   order and inherited delivery rules.
4. Keep a dependent draft issue `In Progress`; use `In Review` only when its final base, diff, gates,
   and review surface are ready.
5. Keep branches, PRs, gates, and merge order explicit per repository in a multi-repo front.
6. Treat a worktree as an isolation mechanism, not authorization to create/switch it or run parallel
   work. A dirty worktree blocks only recommendations that require switching that worktree.
7. Never mutate Linear, GitHub, Git refs, worktrees, index, config, or product files in this MVP.

When the WIP or stack-depth limit is reached, refuse another front and recommend finishing,
reconciling, or promoting the existing second front.

## Candidate Classification

Evaluate each candidate in this precedence order. Stop at the first class whose conditions are met.

### `blocked`

Use when any of these is true:

- an unresolved formal blocker prevents starting or delivering the issue;
- required Linear, GitHub, repository, integration-ref, or ownership evidence is unavailable;
- the front already reaches the WIP or stack-depth limit;
- no safe repository scope or merge order can be established;
- a required branch action would use a dirty worktree and no existing isolated worktree applies.

State the exact blocked transition and the evidence-recovery or completion action. Do not label the
issue itself formally blocked in Linear unless Linear represents that relation.

### `dependent`

Use only when a formal relation, inherited contract, or demonstrated code/runtime requirement means
the candidate must build on the pending PR's exact head. Record the PR-base, its head SHA as the
boundary, initial PR base, and final integration base. A shared file alone does not prove dependency.

### `conflicting`

Use when code evidence shows overlapping files, symbols, migrations, contracts, or mutually
exclusive changes, but no functional/base dependency is proven. Describe the collision as `CODE` or
`INFERENCE`, never `FORMAL`. Prefer another independent candidate; otherwise recommend explicit
waiting or clarification.

### `independent`

Use only after required evidence is available and no blocked, dependent, or conflicting condition
applies. Independence means the candidate can branch from the current integration SHA and produce a
task-only diff without relying on the pending PR.

For every verdict, include confidence (`high`, `medium`, or `low`), supporting evidence, missing
evidence, and rejected alternatives. Never hide low confidence behind a definitive label.

## Delivery States

| State | Linear | Pull request | Valid next transition |
| --- | --- | --- | --- |
| `ready` | Ready to Start | none | `active` after a task is selected |
| `active` | In Progress | none or draft | implement, validate, correct, or `waiting-base` |
| `waiting-base` | In Progress | draft against dependency | refresh plan, wait, `reconciling`, or `abandoned-base` |
| `reconciling` | In Progress | draft | re-evaluate base, task-only diff, gates, and freshness |
| `reviewable` | In Review | ready against final integration | review, `changes-requested`, or `merged` through canonical workflow |
| `changes-requested` | Per local policy | ready or draft | correct, mark prior validation stale, revalidate, then return to prior safe state |
| `merged` | Done through canonical workflow | merged | select the next task |
| `abandoned-base` | In Progress or Blocked | draft | replan against integration or cancel |

Reject these transitions:

- `waiting-base → reviewable` without reconciliation;
- `active → merged` without a reviewable PR and canonical merge workflow;
- any transition that creates a third active/dependent front in the repository;
- promotion when source freshness, boundary, task-only diff, gates, or final PR base is unresolved.
- promotion from `working-tree`, `committed`, or `pushed` without a matching `pr-observed` snapshot;
- promotion with validation `missing`, `fail`, `stale`, or `pending-delivery`.

## Delivery Contracts

Every contract contains:

- issue and repository;
- work branch and resolved base SHA;
- PR-base when present;
- initial PR base and final PR base;
- boundary SHA when dependent;
- intended Linear and PR states;
- expected path/symbol surface;
- implementation and validation maturity, including the validation evidence SHA/range;
- review generation or bundle lineage when supplied;
- applicable gates;
- promotion conditions;
- unresolved questions and confidence;
- future actions requiring explicit authorization;
- exactly one immediate next action.

Represent the expected surface with the applicable fields below instead of relying on a file count:

- exact paths;
- path families or globs;
- expected old-to-new renames;
- allowed generated artifacts;
- forbidden local or validation artifacts.

An expected mechanical rename may touch many files and remain task-only. File count is informational;
unexpected semantics, paths, or rename directions determine scope drift.

### Independent contract

- Base the work on the resolved current integration SHA.
- Target the final PR at the integration branch.
- Use draft only when inherited delivery order requires it; independence alone does not require a
  stacked PR.
- Require a task-only diff and applicable gates before `Ready for review` / `In Review`.

### Dependent contract

- Base the work on the exact head SHA of the ready PR-base.
- Record that SHA as the immutable boundary for separating base-task commits from dependent-task
  commits.
- Initially target the draft PR at the PR-base branch; record the integration branch as final base.
- Keep the issue `In Progress` and the PR draft until the PR-base reaches a terminal state and the
  dependent branch is reconciled.
- Block the contract when the boundary is absent or the front already has one dependent level.

These contracts are plans only. Do not create branches, worktrees, commits, PRs, or Linear updates.

## Reconciliation Plans

Describe conceptual operations and verification. Do not execute them.

### Independent work after another PR merges

1. Re-resolve the integration branch and merged PR state.
2. Mark the old plan stale if integration or the work head changed.
3. Plan updating the task branch onto the current integration state.
4. Recompute changed paths and task-only diff.
5. Re-run applicable gates and check the final PR base.
6. Recommend promotion only when the promotion guard passes.

### Dependent work after squash merge

1. Confirm the PR-base merged and capture the resulting integration SHA.
2. Confirm the stored boundary equals the upstream head from which the dependent work started, or
   refresh the assessment if the PR-base changed before merge.
3. Identify only commits after the boundary as dependent-task commits.
4. Describe reapplying that exclusive commit range onto the current integration branch, equivalent
   in intent to a boundary-aware `rebase --onto`; do not run or present it as authorized.
5. Compare pre/post commit set and changed paths, ensure base-task changes do not remain in the final
   PR surface, re-run gates, and recheck source freshness.
6. Recommend changing the PR to its final integration base and marking it ready only after every
   guard passes.

### Base PR updated before merge

Mark the previous plan stale. Re-read the base PR head and candidate impact. Establish a new boundary
only from evidence that the dependent work was actually rebased onto that exact head; never replace
the stored boundary merely because the PR-base advanced.

### Review correction changes a head or dirty surface

Mark validation and promotion evidence for that task stale. Recompute its review commits,
rename-aware surface, unexpected paths, applicable gates, and final PR head/base. If the changed PR
is a dependency boundary for another draft, also stale the dependent reconciliation plan; keep the
stored boundary as historical evidence until the dependent work is demonstrably based on the new
head. Independent work may continue, but its own promotion still requires a fresh final-base diff.

### Base PR closed without merge

Enter `abandoned-base`. Block automatic promotion. Reassess whether the work remains valid against
integration, whether the former dependency must be included elsewhere, or whether the issue should
be canceled/clarified.

### Future branch rewrite boundary

Any later phase that rewrites a published branch must be separately approved, limited to a draft
branch owned by the user, preceded by dry-run/diff evidence, and use lease-protected force push. The
MVP does not perform or authorize that action.

## Promotion Guard

Recommend promotion to `Ready for review` / `In Review` only when all checks pass:

1. Linear, GitHub, local Git, and inherited-rule evidence required for the transition is available.
2. PR head SHA, base, state, review, and CI observations are fresh and mutually consistent.
3. The final PR targets the intended integration branch.
4. A dependent stack has a valid boundary and completed post-terminal reconciliation.
5. The final commit range and changed paths contain only the selected task.
6. No commits or files exclusive to the PR-base remain in the review surface.
7. Unexpected files are listed and resolved; local/validation artifacts stay out of the proposed
   commit and PR without being deleted automatically.
8. All applicable repository gates and CI are green.
9. WIP and stack-depth invariants remain satisfied.
10. Implementation maturity is `pr-observed` and validation is a non-stale `pass` bound to the same
    head/review surface; no delivery-only condition remains.

If any check fails, return the failed checks and one next action that can recover evidence or resolve
the earliest blocking condition.

## Failure Handling

| Failure | Result |
| --- | --- |
| Linear or GitHub unavailable | Partial snapshot; block dependent classifications and transitions requiring that source |
| Repository absent | Do not clone; block recommendations for that repo |
| Git ref invalid | Stop local inspection and request/resolve the explicit ref |
| Worktree dirty | Preserve and list paths; block only branch-switching assumptions for that worktree |
| Snapshot changes during assessment | Mark stale and recollect affected evidence |
| WIP cap reached | Refuse a third front and recommend completing the second |
| Boundary missing | Block squash-aware dependent reconciliation |
| Base closed without merge | Enter `abandoned-base` and replan |
| Unexpected/base-task path remains | Block promotion and list the path |
| Tool denied or rate-limited | Treat its evidence as unavailable; never substitute a guess |

Repeating the assessment against the same input snapshot must produce the same classifications and
must not create state. Partial failure needs no rollback because the MVP is read-only.

## Report Contract

Return sections in this order:

1. **Scope and freshness** — identity, capture times, sources available/missing, resolved SHAs.
2. **Current topology** — ready PR, active/draft task, states, bases, WIP and stack depth per repo.
3. **Candidate classifications** — verdict, confidence, evidence class/source, missing evidence and
   rejected alternatives.
4. **Delivery contract or block** — every required contract field, or the exact blocked transition.
5. **Reconciliation plan** — only when a base update/merge/closure is in scope.
6. **Next action** — exactly one immediate recommendation.
7. **Approval boundary** — later state-changing actions that require explicit authorization.

Separate facts from inference. Do not call a code collision a formal blocker, do not call a report an
approval, and do not claim that read-only analysis changed Linear, GitHub, Git, or product state.
