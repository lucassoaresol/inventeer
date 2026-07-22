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

  : >"$output_file"
  if bash "$subject" "$@" >"$output_file" 2>/dev/null; then
    fail "$label should fail"
  fi
  [[ ! -s "$output_file" ]] || fail "$label emitted partial stdout"
}

repo="$fixture_dir/repo"
linked="$fixture_dir/linked worktree"
git init --initial-branch=main "$repo" >/dev/null
git -C "$repo" config user.name Test
git -C "$repo" config user.email test@example.com
printf 'initial\n' >"$repo/tracked.txt"
printf 'remove\n' >"$repo/deleted.txt"
git -C "$repo" add tracked.txt deleted.txt
git -C "$repo" commit -m initial >/dev/null
integration_sha="$(git -C "$repo" rev-parse main)"

git -C "$repo" switch -c feature/base >/dev/null
printf 'base\n' >"$repo/base.txt"
git -C "$repo" add base.txt
git -C "$repo" commit -m 'base task' >/dev/null
boundary_sha="$(git -C "$repo" rev-parse HEAD)"

git -C "$repo" switch -c feature/dependent >/dev/null
printf 'dependent\n' >"$repo/dependent.txt"
git -C "$repo" add dependent.txt
git -C "$repo" commit -m 'dependent task' >/dev/null
work_sha="$(git -C "$repo" rev-parse HEAD)"

git -C "$repo" worktree add -b linked "$linked" main >/dev/null
printf 'changed\n' >"$repo/tracked.txt"
rm "$repo/deleted.txt"
printf 'local\n' >"$repo/untracked file.txt"

fingerprint_before="$(fingerprint_repo "$repo")"
captured_at="2026-07-22T12:00:00Z"
output="$(bash "$subject" \
  --repo "$repo" \
  --integration-ref main \
  --work-ref feature/dependent \
  --boundary-ref feature/base \
  --captured-at "$captured_at")"

grep -F $'schema_version\t1' <<<"$output" >/dev/null || fail "schema version missing"
grep -F $'integration_sha\t'"$integration_sha" <<<"$output" >/dev/null || fail "integration SHA missing"
grep -F $'work_sha\t'"$work_sha" <<<"$output" >/dev/null || fail "work SHA missing"
echo "ok 1 - resolves refs and emits the versioned snapshot"

grep -F 'tracked.txt' <<<"$output" >/dev/null || fail "tracked dirty path missing"
grep -F 'deleted.txt' <<<"$output" >/dev/null || fail "deleted dirty path missing"
grep -F 'untracked\ file.txt' <<<"$output" >/dev/null || fail "space-containing untracked path is not quoted"
echo "ok 2 - captures tracked, deleted, untracked, and quoted paths"

grep -F 'linked\ worktree' <<<"$output" >/dev/null || fail "linked worktree missing"
echo "ok 3 - captures linked worktrees"

grep -F $'boundary_sha\t'"$boundary_sha" <<<"$output" >/dev/null || fail "boundary SHA missing"
grep -F $'task_commit\t'"$work_sha" <<<"$output" >/dev/null || fail "task-only commit missing"
grep -F $'task_changed_path\tdependent.txt' <<<"$output" >/dev/null || fail "task-only path missing"
echo "ok 4 - isolates commits and paths after the boundary"

second_output="$(bash "$subject" \
  --repo "$repo" \
  --integration-ref main \
  --work-ref feature/dependent \
  --boundary-ref feature/base \
  --captured-at "$captured_at")"
[[ "$output" == "$second_output" ]] || fail "same snapshot and timestamp should be deterministic"
echo "ok 5 - produces deterministic output for the same snapshot"

assert_failed_without_stdout "invalid repository" \
  --repo "$fixture_dir/missing" --integration-ref main
echo "ok 6 - rejects an invalid repository without partial output"

assert_failed_without_stdout "missing integration ref" \
  --repo "$repo" --integration-ref missing-integration
echo "ok 7 - rejects a missing integration ref without partial output"

assert_failed_without_stdout "missing work ref" \
  --repo "$repo" --integration-ref main --work-ref missing-work
echo "ok 8 - rejects a missing work ref without partial output"

assert_failed_without_stdout "missing boundary ref" \
  --repo "$repo" --integration-ref main --boundary-ref missing-boundary
echo "ok 9 - rejects a missing boundary ref without partial output"

fingerprint_after="$(fingerprint_repo "$repo")"
[[ "$fingerprint_before" == "$fingerprint_after" ]] || fail "inspector mutated repository state"
echo "ok 10 - preserves status, refs, config, tracked tree, and untracked files"
