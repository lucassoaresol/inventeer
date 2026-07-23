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
printf 'session-context/\n' >"$repo/.gitignore"
git -C "$repo" add .gitignore changed.txt removed.txt
git -C "$repo" commit -m initial >/dev/null

printf 'after\n' >"$repo/changed.txt"
git -C "$repo" add changed.txt
rm "$repo/removed.txt"
printf 'new file\n' >"$repo/untracked file.txt"
status_before="$(git -C "$repo" status --porcelain=v1)"

"$subject" --repo "$repo" --base HEAD --output-dir "$out" --label Sample --review-stage initial >/dev/null
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
[[ -f "$bundle_dir/lineage.tsv" ]] || fail "lineage.tsv missing"
[[ "$(find "$bundle_dir/diffs" -type f -name '*.diff' | wc -l)" -eq 3 ]] || fail "expected three per-file diffs"
grep -F $'tracked\tchanged.txt\t' "$bundle_dir/files.tsv" >/dev/null || fail "tracked file missing"
grep -F $'tracked\tremoved.txt\t' "$bundle_dir/files.tsv" >/dev/null || fail "removed file missing"
grep -F $'untracked\tuntracked file.txt\t' "$bundle_dir/files.tsv" >/dev/null || fail "untracked file missing"
echo "ok 2 - captures tracked, removed, and untracked files"

grep -F $'meta\treview_stage\tinitial' "$bundle_dir/lineage.tsv" >/dev/null || fail "initial review stage missing"
grep -F $'meta\tparent_status\tnone' "$bundle_dir/lineage.tsv" >/dev/null || fail "parent absence missing"
echo "ok 3 - records an explicit first-generation lineage"

(cd "$out" && sha256sum -c "$(basename "$zip_file").sha256" >/dev/null) || fail "checksum verification failed"
status_after="$(git -C "$repo" status --porcelain=v1)"
[[ "$status_before" == "$status_after" ]] || fail "source worktree was mutated"
echo "ok 4 - checksum passes and source status is unchanged"

printf 'remove me\n' >"$repo/removed.txt"
rm "$repo/untracked file.txt"
printf 'child only\n' >"$repo/child.txt"
lineage_status_before="$(git -C "$repo" status --porcelain=v1)"
"$subject" --repo "$repo" --base HEAD --output-dir "$out" --label Child \
  --review-stage corrective --parent-bundle "$zip_file" >/dev/null
child_zip="$(find "$out" -maxdepth 1 -type f -name 'child-review-*.zip' -print -quit)"
[[ -n "$child_zip" ]] || fail "child bundle was not created"
child_extract="$tmp_dir/child-extract"
mkdir "$child_extract"
unzip -q "$child_zip" -d "$child_extract"
child_dir="$(find "$child_extract" -mindepth 1 -maxdepth 1 -type d -print -quit)"
parent_hash="$(sha256sum "$zip_file" | cut -d' ' -f1)"
grep -F $'meta\tparent_status\tlinked' "$child_dir/lineage.tsv" >/dev/null || fail "linked parent status missing"
grep -F $'meta\tparent_sha256\t'"$parent_hash" "$child_dir/lineage.tsv" >/dev/null || fail "parent hash missing"
grep -F $'meta\tparent_checksum_status\tverified' "$child_dir/lineage.tsv" >/dev/null || fail "parent checksum not verified"
grep -F $'path\tretained\tchanged.txt' "$child_dir/lineage.tsv" >/dev/null || fail "retained path missing"
grep -F $'path\tadded\tchild.txt' "$child_dir/lineage.tsv" >/dev/null || fail "added path missing"
grep -F $'path\tremoved\tremoved.txt' "$child_dir/lineage.tsv" >/dev/null || fail "removed path missing"
grep -F $'path\tremoved\tuntracked file.txt' "$child_dir/lineage.tsv" >/dev/null || fail "removed untracked path missing"
[[ "$lineage_status_before" == "$(git -C "$repo" status --porcelain=v1)" ]] || fail "lineage creation mutated source"
echo "ok 5 - links a verified parent and classifies the path delta"

parent_without_checksum="$tmp_dir/parent-without-checksum.zip"
cp "$zip_file" "$parent_without_checksum"
"$subject" --repo "$repo" --base HEAD --output-dir "$out" --label MissingChecksum \
  --parent-bundle "$parent_without_checksum" >/dev/null
missing_zip="$(find "$out" -maxdepth 1 -type f -name 'missingchecksum-review-*.zip' -print -quit)"
missing_extract="$tmp_dir/missing-extract"
mkdir "$missing_extract"
unzip -q "$missing_zip" -d "$missing_extract"
missing_dir="$(find "$missing_extract" -mindepth 1 -maxdepth 1 -type d -print -quit)"
grep -F $'meta\tparent_checksum_status\tmissing' "$missing_dir/lineage.tsv" >/dev/null || fail "missing checksum status absent"
echo "ok 6 - records a missing adjacent parent checksum without losing computed lineage"

bad_parent="$tmp_dir/bad-parent.zip"
cp "$zip_file" "$bad_parent"
printf '%064d  %s\n' 0 "$(basename "$bad_parent")" >"$bad_parent.sha256"
bad_count_before="$(find "$out" -maxdepth 1 -type f -name 'bad-review-*.zip' | wc -l)"
if "$subject" --repo "$repo" --base HEAD --output-dir "$out" --label Bad \
  --parent-bundle "$bad_parent" >/dev/null 2>&1; then
  fail "invalid adjacent parent checksum should fail"
fi
bad_count_after="$(find "$out" -maxdepth 1 -type f -name 'bad-review-*.zip' | wc -l)"
[[ "$bad_count_before" -eq "$bad_count_after" ]] || fail "failed lineage left a child ZIP"
echo "ok 7 - fails closed on an invalid parent checksum without a child ZIP"

malformed_root="$tmp_dir/malformed-root"
mkdir -p "$malformed_root/one" "$malformed_root/two"
printf '# Git Review Bundle\n\n- HEAD SHA: %s\n' "$(git -C "$repo" rev-parse HEAD)" >"$malformed_root/one/README.md"
printf 'kind\tpath\tdiff\n' >"$malformed_root/one/files.tsv"
printf 'kind\tpath\tdiff\n' >"$malformed_root/two/files.tsv"
malformed_parent="$tmp_dir/malformed-parent.zip"
(cd "$malformed_root" && zip -qr "$malformed_parent" one two)
if "$subject" --repo "$repo" --base HEAD --output-dir "$out" --label Malformed \
  --parent-bundle "$malformed_parent" >/dev/null 2>&1; then
  fail "parent with duplicate files.tsv should fail"
fi
echo "ok 8 - rejects a parent without a unique manifest contract"

internal_before="$(git -C "$repo" status --porcelain=v1)"
if "$subject" --repo "$repo" --output-dir "$repo/review-output" >/dev/null 2>&1; then
  fail "non-ignored output inside source repository should be rejected"
fi
[[ ! -e "$repo/review-output" ]] || fail "rejected internal output left a directory behind"
internal_after="$(git -C "$repo" status --porcelain=v1)"
[[ "$internal_before" == "$internal_after" ]] || fail "rejected internal output changed source status"
echo "ok 9 - rejects non-ignored output inside the source repository without residue"

"$subject" --repo "$repo" --output-dir "$repo/session-context" --label internal >/dev/null
[[ -n "$(find "$repo/session-context" -maxdepth 1 -type f -name 'internal-review-*.zip' -print -quit)" ]] || fail "ignored internal output was not created"
ignored_after="$(git -C "$repo" status --porcelain=v1)"
[[ "$internal_before" == "$ignored_after" ]] || fail "ignored internal output changed source status"
echo "ok 10 - permits ignored output inside the source repository"

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
echo "ok 11 - rejects an empty change set"

if "$subject" --repo "$repo" --base missing-ref --output-dir "$tmp_dir/bad-base" >/dev/null 2>&1; then
  fail "invalid base should be rejected"
fi
echo "ok 12 - rejects an invalid base"

printf 'token=value\n' >"$clean_repo/.env"
if "$subject" --repo "$clean_repo" --output-dir "$tmp_dir/sensitive" >/dev/null 2>&1; then
  fail "sensitive path should be rejected"
fi
echo "ok 13 - rejects likely credential files"
