---
name: advance-delivery-front
description: Coordinate continuity across Inventeer tasks while pull requests await review or merge by inspecting Linear, GitHub, and local Git read-only; classifying work as independent, dependent, conflicting, or blocked; producing branch/PR delivery contracts; and planning post-merge reconciliation. Use when continuing a cycle without waiting, preparing a dependent draft PR, reassessing after an upstream PR changes, merges, or closes, or verifying that a PR promotion contains only its own task. Do not use to implement the selected issue or mutate delivery state.
---

# Advance Delivery Front

Coordinate the active topology between cycle triage, single-task preparation, implementation, and
review without changing Linear, GitHub, Git, or product repositories.

## Required Input

Resolve a project/cycle/issue set, the active or recently terminal PRs, and the likely repositories.
Accept an existing `triage-project-cycle` package when supplied. If multiple unprepared issues still
need comparison, use that skill first and consume only the relevant comparison evidence.

Require explicit repository paths and integration refs before local inspection. Do not clone a
missing repository, fetch a remote, or assume that `develop` is universal. Read the matching project
entry point and repository-local instructions to establish inherited branch, merge, and gate rules.

## Workflow

1. **Bound the context.** Run `python3 scripts/workspace-context.py check` and
   `python3 scripts/workspace-context.py plan --route delivery-front`. Stop on a non-zero result;
   these commands emit metadata only and do not replace reading the selected sources.
2. **Resolve the request mode.** Treat the request as assessing the current front, selecting the next
   merge-safe issue, preparing a delivery contract, or reassessing after a PR event. Do not broaden
   a reassessment into full cycle triage unless the candidate set itself is unresolved.
3. **Read the policy.** Read [continuity-policy.md](references/continuity-policy.md) completely before
   classifying candidates, creating a contract, evaluating a transition, or planning reconciliation.
4. **Gather Linear evidence read-only.** Read each issue once per timestamped snapshot. Reuse a
   supplied triage result only when it records retrieval time and issue `updatedAt`, no later event
   or user request indicates that a bound input changed, and the current decision needs no newer
   state; otherwise refresh the target issue. Elapsed time alone never proves freshness. Record
   retrieval time, issue identity, `updatedAt`, state, owner, cycle/order, ancestry
   needed for the shared outcome, and formal blockers/relations. Expand ancestry or relations only
   when they can change topology or classification; record every additional issue identifier and
   reason. If Linear is unavailable, mark the source missing instead of inferring its state.
5. **Gather GitHub evidence read-only.** Record retrieval time, PR number, open/merged/closed state,
   draft status, base, head branch and SHA, review state, and CI checks. Use only read operations.
6. **Inspect each local repository.** Read its instructions and worktree status, then run the bundled
   inspector with explicit refs:

   ```bash
   scripts/inspect-git-front.sh \
     --repo <absolute-repo-path> \
     --integration-ref <ref> \
     --work-ref <ref> \
     [--boundary-ref <ref>]
   ```

   Treat the output as local evidence, not proof that a remote-tracking ref is current. Preserve a
   dirty worktree and report its paths.
7. **Normalize the snapshot.** Build one timestamped view of sources, repo SHAs/worktrees, PRs,
   issues, inherited rules, WIP, stack depth, implementation maturity, and validation maturity. Bind
   validation to its exact evidence SHA/range and treat review bundles only as historical `CODE`
   evidence. Keep each repository's branch, PR, gates, and merge order separate.
8. **Apply classification precedence.** Follow the policy's `blocked → dependent → conflicting →
   independent` order. Cite evidence class, source, confidence, missing evidence, and rejected
   alternatives. Never turn code overlap into a formal dependency or missing evidence into
   independence.
9. **Choose the safe continuation.** Prefer a cycle-compatible independent issue. Enforce one ready
   PR plus one active/draft task per repository and one dependency level. If no safe transition
   exists, recommend recovering the earliest missing evidence or completing the current front.
10. **Produce a contract or reconciliation plan.** Include every policy field and keep conceptual Git
   operations explanatory only. For dependent work, require the exact upstream head as boundary;
   block squash-aware reconciliation when it is absent.
11. **Recheck freshness.** Before recommending promotion or reconciliation, re-read the PR head,
    base, and state and compare the current review surface, gates, and validation binding. Mark the
    plan and affected validation stale when any bound input differs from the snapshot.
12. **Return one next action.** Do not offer several simultaneous actions or imply that any proposed
    state change has already happened.

## Output

Return these sections in order:

1. **Scope and freshness**
2. **Current topology**
3. **Candidate classifications**
4. **Delivery contract or blocked transition**
5. **Reconciliation plan**, only when a base event is relevant
6. **Next action**, exactly one
7. **Approval boundary**

For partial evidence, say which conclusions remain valid and which transitions are blocked. For
multi-repo work, show the inherited merge order without merging their gates or PR surfaces.

## Handoffs

- Hand a selected issue and its delivery contract to `portal-task-context` or
  `assistants-task-context` for full single-issue preparation.
- Hand prepared specification, implementation, or validation work to `tlc-spec-driven`.
- Reassess this front after implementation, review changes, base updates, merge, or closure.
- Keep `triage-project-cycle` responsible for broad issue comparison and delivery waves; keep this
  skill responsible for active PR/task topology, WIP, contracts, and reconciliation.

## Boundaries

- Do not create, edit, promote, close, approve, or merge a PR.
- Do not create, switch, update, rebase, reset, clean, commit, or push a branch or worktree.
- Do not update Linear issues, relations, states, owners, or comments.
- Do not repeat an unchanged Linear issue read inside one snapshot or expand full ancestry merely
  because it is available; refresh when a bound input or decision-relevant event changes, or when
  the supplied snapshot lacks retrieval time or `updatedAt`.
- Do not run `scripts/update-repos.sh`, `git fetch`, `git pull`, or another freshness command that
  mutates local refs.
- Do not edit product files, delete artifacts, or store operational state in this workspace.
- Do not treat a delivery contract as authorization. List every later mutation under the approval
  boundary and require a separate explicit request.
