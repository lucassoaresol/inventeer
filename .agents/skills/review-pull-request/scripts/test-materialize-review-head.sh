#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
subject="$script_dir/materialize-review-head.sh"
fixture_root="$(mktemp -d /tmp/test-materialize-review-head.XXXXXX)"
trap 'rm -rf "$fixture_root"' EXIT

fail() {
  echo "not ok - $*" >&2
  exit 1
}

source_repo="$fixture_root/source"
git init --initial-branch=main "$source_repo" >/dev/null
git -C "$source_repo" config user.name Test
git -C "$source_repo" config user.email test@example.com
printf 'base\n' >"$source_repo/value.txt"
git -C "$source_repo" add value.txt
git -C "$source_repo" commit -m base >/dev/null
base_sha="$(git -C "$source_repo" rev-parse HEAD)"
printf 'head\n' >"$source_repo/value.txt"
git -C "$source_repo" commit -am head >/dev/null
head_sha="$(git -C "$source_repo" rev-parse HEAD)"
printf 'preserve dirty state\n' >"$source_repo/untracked.txt"

source_head_before="$(git -C "$source_repo" rev-parse HEAD)"
source_status_before="$(git -C "$source_repo" status --porcelain=v1)"
destination="$fixture_root/materialized"
output="$($subject --source "$source_repo" --base-sha "$base_sha" --head-sha "$head_sha" --destination "$destination")"

[[ "$(git -C "$destination" rev-parse HEAD)" == "$head_sha" ]] || fail "checkout is not at the requested head"
git -C "$destination" cat-file -e "$base_sha^{commit}" || fail "base commit is absent"
[[ -z "$(git -C "$destination" symbolic-ref -q HEAD || true)" ]] || fail "checkout is not detached"
grep -F $'base_sha\t'"$base_sha" <<<"$output" >/dev/null || fail "base metadata missing"
grep -F $'head_sha\t'"$head_sha" <<<"$output" >/dev/null || fail "head metadata missing"
echo "ok 1 - materializes exact base and detached head"

[[ "$(git -C "$source_repo" rev-parse HEAD)" == "$source_head_before" ]] || fail "source HEAD changed"
[[ "$(git -C "$source_repo" status --porcelain=v1)" == "$source_status_before" ]] || fail "source porcelain changed"
echo "ok 2 - preserves source HEAD and worktree status"

if "$subject" --source "$source_repo" --base-sha bad --head-sha "$head_sha" --destination "$fixture_root/bad-sha" >/dev/null 2>&1; then
  fail "malformed SHA should fail"
fi
[[ ! -e "$fixture_root/bad-sha" ]] || fail "malformed SHA created a destination"
echo "ok 3 - rejects malformed identity before cloning"

mkdir "$fixture_root/existing"
if "$subject" --source "$source_repo" --base-sha "$base_sha" --head-sha "$head_sha" --destination "$fixture_root/existing" >/dev/null 2>&1; then
  fail "existing destination should fail"
fi
if "$subject" --source "$fixture_root/missing" --base-sha "$base_sha" --head-sha "$head_sha" --destination "$fixture_root/missing-source" >/dev/null 2>&1; then
  fail "missing source should fail"
fi
echo "ok 4 - rejects existing destinations and unavailable sources"

missing_head="$(printf 'f%.0s' {1..40})"
if "$subject" --source "$source_repo" --base-sha "$base_sha" --head-sha "$missing_head" --destination "$fixture_root/missing-head" >/dev/null 2>&1; then
  fail "unavailable head should fail"
fi
[[ "$(git -C "$source_repo" status --porcelain=v1)" == "$source_status_before" ]] || fail "failed materialization changed source"
echo "ok 5 - unavailable commits fail without changing source state"
