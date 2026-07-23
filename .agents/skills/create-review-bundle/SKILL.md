---
name: create-review-bundle
description: Create a timestamped ZIP review bundle for a Git repository with provenance, branch and SHA metadata, worktree status, commits, per-file diffs, SHA-256, and optional lineage to an earlier bundle. Use when a user asks to package implemented or uncommitted work for external review, requests a review ZIP in session-context, needs portable diff evidence before commit or PR, or wants to link corrective/final review generations. The workflow is read-only for the source repository and rejects likely credential or dump files.
---

# Create Review Bundle

Package review evidence without changing the repository being reviewed.

## Workflow

1. Resolve the source Git repository and inspect its local instructions and worktree.
2. Choose the comparison base:
   - use the user-provided ref when present;
   - use `HEAD` for uncommitted-only review;
   - use the target branch or its merge base for committed feature-branch review.
3. Inspect changed file names before bundling. Stop if the change set may contain credentials,
   customer data, production output, or another prohibited artifact.
4. Run the bundled script from this skill's own directory:

   ```bash
   scripts/create-review-bundle.sh \
     --repo <repo> \
     --base <ref> \
     --output-dir <workspace>/session-context \
     --label <short-label> \
     --review-stage <initial|corrective|final> \
     [--parent-bundle <earlier.zip>]
   ```

   `--base` defaults to `HEAD`; `--output-dir` defaults to this workspace's `session-context/`.
5. For a later review generation, supply the immediately preceding bundle. Treat its lineage as
   historical `CODE` evidence, not current source or approval evidence.
6. Inspect the resulting ZIP listing, `README.md`, `files.tsv`, `lineage.tsv`, and checksum. Confirm
   the source worktree status is unchanged.
7. Return the ZIP path, comparison base, changed-file count, review stage, parent checksum/status,
   checksum path, and any warning recorded
   by `diff-check.txt`.

## Bundle Contract

The archive contains:

- `README.md`: timestamp, repo, branch, base and HEAD SHAs, and file count;
- `status.txt`: source worktree status at capture time;
- `commits.txt`: commits between the base and `HEAD`;
- `files.tsv`: changed path, provenance (`tracked` or `untracked`), and diff filename;
- `lineage.tsv`: review stage, parent identity/checksum status, head binding, and added/removed/retained paths;
- `diffs/*.diff`: one text diff per changed file;
- `diff-check.txt`: `git diff --check` output and exit status;
- `commands.txt`: read-only commands represented by the bundle.

The adjacent `.sha256` file verifies the completed ZIP.

## Boundaries

- Do not stage, stash, commit, switch branches, reset, clean, or edit the source repository.
- Do not write to a non-ignored path inside the source repository; the script rejects that destination
  before creating it.
- Do not include raw files beyond their Git diff representation.
- Do not bypass the script's sensitive-path rejection.
- Do not claim tests were executed unless their evidence was independently supplied and verified.
- Do not treat a bundle as approval, validation, or a canonical product artifact.
- Do not treat parent lineage as proof that either snapshot is current.
- Keep the bundle in `session-context/` unless the user names another ephemeral destination.
