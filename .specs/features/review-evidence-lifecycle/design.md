# Review Evidence Lifecycle Design

## Architecture

Keep the existing ownership boundaries and add one narrow contract between them:

```text
TLC validation
  -> Delivery Evidence Block (exact head/range, verdict, gates, pending conditions, risk paths)

create-review-bundle
  -> Ephemeral review snapshot + optional parent lineage

advance-delivery-front
  -> Combines live Linear/GitHub/Git with validation maturity and historical bundle evidence
  -> Recommends or blocks one transition; performs no mutation
```

## Delivery Evidence Lifecycle

Track two independent axes:

| Axis | States | Meaning |
| --- | --- | --- |
| Implementation | `working-tree`, `committed`, `pushed`, `pr-observed` | Highest state directly supported by current evidence. |
| Validation | `missing`, `pass`, `fail`, `stale`, `pending-delivery` | State bound to an exact work SHA/review surface and requirement contract. |

Any change to work SHA, dirty diff fingerprint, governing requirement, or gate set invalidates the
previous PASS. `pending-delivery` represents verified behavior with a remaining delivery-only guard,
such as a same-commit invariant or an uncommitted validation artifact.

## Inspector Schema v2

Preserve the tab-separated, shell-quoted stream and add:

- `schema_version=2`;
- `review_commit` for `merge-base..work`;
- `changed_entry` for `git diff --name-status -z -M integration...work`;
- `worktree_staged_path`, `worktree_unstaged_path`, and `worktree_untracked_path`;
- existing final `changed_path`, boundary, task commit, and task path fields.

The inspector remains read-only and produces no stdout on invalid input.

## Bundle Lineage Contract

Add optional `--parent-bundle` and `--review-stage` inputs. Every generated archive contains
`lineage.tsv`. Without a parent, it records `parent_status=none`. With a parent, it records:

- parent bundle basename and computed SHA-256;
- adjacent checksum status (`verified` or `missing`); checksum mismatch is fatal;
- parent/current head SHAs;
- one `path_status` row per union path (`added`, `removed`, `retained`).

Parent parsing accepts exactly one `files.tsv` and one `README.md` in the archive. Parsing occurs in
temporary storage and never extracts into the source repository.

## Typed Scope Surface

Delivery contracts describe expected surface through five optional collections:

1. exact paths;
2. path families/globs;
3. expected old→new renames;
4. allowed generated artifacts;
5. forbidden local/validation artifacts.

Promotion compares rename-aware actual entries with this contract. File count is informational.

## TLC Changes

- Add compatibility/representation to the implicit-requirement rubric.
- Replace file-count atomicity with reversible semantic atomicity.
- Require resource-aware but coverage-equivalent full-gate recipes when necessary.
- Remove stash-based mutation guidance.
- Add a standard Delivery Evidence Block to validation output.
- Add `review_finding` to the deterministic lessons signal set, accepted only when validation cites
  a confirmed external finding.

## Verification Strategy

- Extend the inspector harness with review commits, rename-aware entries, and split dirty paths.
- Extend the bundle harness with no-parent lineage, verified parent lineage, path delta, missing
  checksum, checksum mismatch, malformed parent, and source fingerprint preservation.
- Add a deterministic lessons probe for `review_finding` and validate all three skill folders.
- Use a fresh independent verifier for spec evidence and behavior-level mutations.

