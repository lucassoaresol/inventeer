#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
subject="$script_dir/create-review-bundle.sh"
tmp_dir="$(mktemp -d /tmp/test-create-review-bundle.XXXXXX)"
trap 'rm -rf "$tmp_dir"' EXIT

fail() {
  echo "not ok - $*" >&2
  exit 1
}

repo="$tmp_dir/repo"
out="$tmp_dir/out"
git init --initial-branch=main "$repo" >/dev/null
git -C "$repo" config user.name Test
git -C "$repo" config user.email test@example.com
printf 'before\n' >"$repo/changed.txt"
printf 'remove me\n' >"$repo/removed.txt"
git -C "$repo" add changed.txt removed.txt
git -C "$repo" commit -m initial >/dev/null

printf 'after\n' >"$repo/changed.txt"
git -C "$repo" add changed.txt
rm "$repo/removed.txt"
printf 'new file\n' >"$repo/untracked file.txt"
status_before="$(git -C "$repo" status --porcelain=v1)"

"$subject" --repo "$repo" --base HEAD --output-dir "$out" --label Sample >/dev/null
zip_file="$(find "$out" -maxdepth 1 -type f -name 'sample-review-*.zip' -print -quit)"
[[ -n "$zip_file" ]] || fail "bundle ZIP was not created"
[[ -f "$zip_file.sha256" ]] || fail "checksum sidecar was not created"
echo "ok 1 - creates ZIP and checksum"

extract="$tmp_dir/extract"
mkdir "$extract"
unzip -q "$zip_file" -d "$extract"
bundle_dir="$(find "$extract" -mindepth 1 -maxdepth 1 -type d -print -quit)"
[[ -f "$bundle_dir/README.md" ]] || fail "README missing"
[[ -f "$bundle_dir/files.tsv" ]] || fail "files.tsv missing"
[[ "$(find "$bundle_dir/diffs" -type f -name '*.diff' | wc -l)" -eq 3 ]] || fail "expected three per-file diffs"
grep -F $'tracked\tchanged.txt\t' "$bundle_dir/files.tsv" >/dev/null || fail "tracked file missing"
grep -F $'tracked\tremoved.txt\t' "$bundle_dir/files.tsv" >/dev/null || fail "removed file missing"
grep -F $'untracked\tuntracked file.txt\t' "$bundle_dir/files.tsv" >/dev/null || fail "untracked file missing"
echo "ok 2 - captures tracked, removed, and untracked files"

(cd "$out" && sha256sum -c "$(basename "$zip_file").sha256" >/dev/null) || fail "checksum verification failed"
status_after="$(git -C "$repo" status --porcelain=v1)"
[[ "$status_before" == "$status_after" ]] || fail "source worktree was mutated"
echo "ok 3 - checksum passes and source status is unchanged"

clean_repo="$tmp_dir/clean"
git init --initial-branch=main "$clean_repo" >/dev/null
git -C "$clean_repo" config user.name Test
git -C "$clean_repo" config user.email test@example.com
printf 'clean\n' >"$clean_repo/file.txt"
git -C "$clean_repo" add file.txt
git -C "$clean_repo" commit -m initial >/dev/null
if "$subject" --repo "$clean_repo" --output-dir "$tmp_dir/clean-out" >/dev/null 2>&1; then
  fail "clean repository should be rejected"
fi
echo "ok 4 - rejects an empty change set"

if "$subject" --repo "$repo" --base missing-ref --output-dir "$tmp_dir/bad-base" >/dev/null 2>&1; then
  fail "invalid base should be rejected"
fi
echo "ok 5 - rejects an invalid base"

printf 'token=value\n' >"$clean_repo/.env"
if "$subject" --repo "$clean_repo" --output-dir "$tmp_dir/sensitive" >/dev/null 2>&1; then
  fail "sensitive path should be rejected"
fi
echo "ok 6 - rejects likely credential files"
