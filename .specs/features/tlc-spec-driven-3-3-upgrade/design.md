# TLC Spec-Driven 3.3.0 Upgrade Design

## Architecture

The upgrade keeps the existing AD-016 fork model:

```text
upstream 3.2.0 base ──┐
                      ├─ three-way merge ──> reviewed local 3.3.0 fork
Inventeer extensions ─┘                         │
upstream 3.3.0 incoming ────────────────────────┘
                                                │
                                                ├─ focused validator harness
                                                └─ root workspace gate
```

The canonical update script resolves and downloads both pinned revisions, replaces the package with
the incoming tree, and reapplies the base-to-local patch. The resulting worktree is reviewed before
the manifest update is accepted as evidence.

## Merge Boundaries

Upstream changes overlap `SKILL.md`, `references/specify.md`, `references/tasks.md`,
`references/implement.md`, and `references/validate.md`. The merge must retain local review
lifecycle, provenance, operational enablement, exact-diff, and resource-aware execution guidance.
Unchanged local references and scripts remain intact. The four new upstream validator scripts are
then hardened locally with narrowly scoped compatibility changes.

## Validator Contract

`validate_spec.py` accepts the canonical Markdown variants used for acceptance-criteria headings
while retaining EARS `SHALL`, required-section, assumptions-table, and traceability checks.

`validate_state.py` ranks explicit overall labels (`Overall`, `Verdict`, or validation status) above
generic result lines. Subordinate sensor or gate results cannot override an explicit overall FAIL.
A completed PASS still requires at least one concrete `file:line` citation.

`validate_tasks.py` and `check_commit.py` retain upstream behavior and receive behavioral fixtures
for both accepting and rejecting paths. Tests invoke the scripts as command-line tools so exit code
and diagnostic behavior are covered together.

## Prospective Compatibility

The new validators are transition gates for artifacts created or materially revised with TLC 3.3.0.
They are not a migration rule for the historical `.specs/features/` archive. The root gate therefore
runs self-contained temporary fixtures plus this upgrade's current artifacts; it does not enumerate
all old specs.

## Verification Strategy

- Run focused validator tests after every script change.
- Run the vendored skill structural validator and `git diff --check`.
- Run the complete root gate after a machine resource snapshot.
- Copy the relevant scripts and tests to disposable directories, inject representative regressions,
  and require the harness to fail for each mutant.
- Bind the final validation report to the exact functional commit and diff range.

## Failure and Rollback

If the merge has unresolved markers, manifest acceptance is blocked. If any compatibility test or
root gate fails, the new base is not delivered. Each semantic increment is committed separately so
the vendor import, local hardening, and policy/evidence can be inspected or reverted independently.
