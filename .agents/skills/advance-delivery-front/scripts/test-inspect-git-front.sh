#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
subject="$script_dir/inspect-git-front.sh"
fixture_dir="$(mktemp -d /tmp/test-inspect-git-front.XXXXXX)"
trap 'rm -rf "$fixture_dir"' EXIT

fail() {
  echo "not ok - $*" >&2
  exit 1
}

fingerprint_repo() {
  local repo_path="$1"

  {
    git -C "$repo_path" status --porcelain=v1 -z --untracked-files=all
    git -C "$repo_path" show-ref
    git -C "$repo_path" config --local --null --list
    git -C "$repo_path" diff --binary HEAD --
    while IFS= read -r -d '' path; do
      printf '%s\0' "$path"
      sha256sum "$repo_path/$path"
    done < <(git -C "$repo_path" ls-files --others --exclude-standard -z | sort -z)
  } | sha256sum | cut -d' ' -f1
}

assert_failed_without_stdout() {
  local label="$1"
  shift
  local output_file="$fixture_dir/failure-output"
  local status

  : >"$output_file"
  if bash "$subject" "$@" >"$output_file" 2>/dev/null; then
    fail "$label should fail"
  else
    status=$?
  fi
  [[ "$status" -eq 2 ]] || fail "$label exited with $status instead of 2"
  [[ ! -s "$output_file" ]] || fail "$label emitted partial stdout"
}

repo="$fixture_dir/repo"
linked="$fixture_dir/linked worktree"
integration_worktree="$fixture_dir/integration worktree"
git init --initial-branch=main "$repo" >/dev/null
git -C "$repo" config user.name Test
git -C "$repo" config user.email test@example.com
printf 'initial\n' >"$repo/tracked.txt"
printf 'remove\n' >"$repo/deleted.txt"
printf 'rename\n' >"$repo/rename-source.txt"
printf 'stage later\n' >"$repo/staged.txt"
git -C "$repo" add tracked.txt deleted.txt rename-source.txt staged.txt
git -C "$repo" commit -m initial >/dev/null

git -C "$repo" switch -c feature/base >/dev/null
printf 'base\n' >"$repo/base.txt"
git -C "$repo" add base.txt
git -C "$repo" commit -m 'base task' >/dev/null
boundary_sha="$(git -C "$repo" rev-parse HEAD)"

git -C "$repo" switch -c feature/dependent >/dev/null
printf 'dependent\n' >"$repo/dependent.txt"
git -C "$repo" mv rename-source.txt rename-target.txt
git -C "$repo" add dependent.txt rename-target.txt
git -C "$repo" commit -m 'dependent task' >/dev/null
work_sha="$(git -C "$repo" rev-parse HEAD)"

git -C "$repo" worktree add -b linked "$linked" main >/dev/null
git -C "$repo" worktree add "$integration_worktree" main >/dev/null
printf 'integration only\n' >"$integration_worktree/integration-only.txt"
git -C "$integration_worktree" add integration-only.txt
git -C "$integration_worktree" commit -m 'advance integration' >/dev/null
integration_sha="$(git -C "$repo" rev-parse main)"
printf 'changed\n' >"$repo/tracked.txt"
rm "$repo/deleted.txt"
printf 'staged change\n' >"$repo/staged.txt"
git -C "$repo" add staged.txt
printf 'local\n' >"$repo/untracked file.txt"

fingerprint_before="$(fingerprint_repo "$repo")"
captured_at="2026-07-22T12:00:00Z"
output="$(bash "$subject" \
  --repo "$repo" \
  --integration-ref main \
  --work-ref feature/dependent \
  --boundary-ref feature/base \
  --captured-at "$captured_at")"

grep -F $'schema_version\t2' <<<"$output" >/dev/null || fail "schema version missing"
grep -F $'integration_sha\t'"$integration_sha" <<<"$output" >/dev/null || fail "integration SHA missing"
grep -F $'work_sha\t'"$work_sha" <<<"$output" >/dev/null || fail "work SHA missing"
review_paths="$(awk -F '\t' '$1 == "changed_path" { print $2 }' <<<"$output")"
[[ "$review_paths" == $'base.txt\ndependent.txt\nrename-target.txt' ]] || fail "review surface does not match the three-dot range"
echo "ok 1 - resolves refs and emits the versioned snapshot"

review_commits="$(awk -F '\t' '$1 == "review_commit" { print $2 }' <<<"$output")"
expected_review_commits="${boundary_sha}"$'\n'"${work_sha}"
[[ "$review_commits" == "$expected_review_commits" ]] || fail "review commits are not merge-base relative"
grep -F 'R100' <<<"$output" | grep -F 'rename-source.txt' | grep -F 'rename-target.txt' >/dev/null || {
  fail "rename-aware changed entry missing"
}
echo "ok 2 - captures review commits and rename-aware entries"

grep -F 'tracked.txt' <<<"$output" >/dev/null || fail "tracked dirty path missing"
grep -F 'deleted.txt' <<<"$output" >/dev/null || fail "deleted dirty path missing"
grep -F 'untracked\ file.txt' <<<"$output" >/dev/null || fail "space-containing untracked path is not quoted"
echo "ok 3 - captures tracked, deleted, untracked, and quoted paths"

grep -F $'worktree_staged_path\tstaged.txt' <<<"$output" >/dev/null || fail "staged path missing"
grep -F $'worktree_unstaged_path\ttracked.txt' <<<"$output" >/dev/null || fail "unstaged path missing"
grep -F 'worktree_untracked_path' <<<"$output" | grep -F 'untracked\ file.txt' >/dev/null || fail "untracked path class missing"
echo "ok 4 - separates staged, unstaged, and untracked paths"

grep -F 'linked\ worktree' <<<"$output" >/dev/null || fail "linked worktree missing"
echo "ok 5 - captures linked worktrees"

grep -F $'boundary_sha\t'"$boundary_sha" <<<"$output" >/dev/null || fail "boundary SHA missing"
grep -F $'task_commit\t'"$work_sha" <<<"$output" >/dev/null || fail "task-only commit missing"
grep -F $'task_changed_path\tdependent.txt' <<<"$output" >/dev/null || fail "task-only path missing"
echo "ok 6 - isolates commits and paths after the boundary"

second_output="$(bash "$subject" \
  --repo "$repo" \
  --integration-ref main \
  --work-ref feature/dependent \
  --boundary-ref feature/base \
  --captured-at "$captured_at")"
[[ "$output" == "$second_output" ]] || fail "same snapshot and timestamp should be deterministic"
echo "ok 7 - produces deterministic output for the same snapshot"

assert_failed_without_stdout "invalid repository" \
  --repo "$fixture_dir/missing" --integration-ref main
echo "ok 8 - rejects an invalid repository without partial output"

assert_failed_without_stdout "missing integration ref" \
  --repo "$repo" --integration-ref missing-integration
echo "ok 9 - rejects a missing integration ref without partial output"

assert_failed_without_stdout "missing work ref" \
  --repo "$repo" --integration-ref main --work-ref missing-work
echo "ok 10 - rejects a missing work ref without partial output"

assert_failed_without_stdout "missing boundary ref" \
  --repo "$repo" --integration-ref main --boundary-ref missing-boundary
echo "ok 11 - rejects a missing boundary ref without partial output"

assert_failed_without_stdout "non-ancestor boundary ref" \
  --repo "$repo" --integration-ref main --work-ref feature/dependent --boundary-ref main

fingerprint_after="$(fingerprint_repo "$repo")"
[[ "$fingerprint_before" == "$fingerprint_after" ]] || fail "inspector mutated repository state"
echo "ok 12 - preserves status, refs, config, tracked tree, and untracked files"
echo "ok 13 - reports the exact three-dot review surface on diverged history"
echo "ok 14 - rejects a resolvable non-ancestor boundary without partial output"
