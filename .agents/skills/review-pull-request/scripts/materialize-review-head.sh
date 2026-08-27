#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "usage: materialize-review-head.sh --source <git-path-or-url> --base-sha <40-hex> --head-sha <40-hex> --destination <new-directory>" >&2
  exit 2
}

source_ref=""
base_sha=""
head_sha=""
destination=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) [[ $# -ge 2 ]] || usage; source_ref="$2"; shift 2 ;;
    --base-sha) [[ $# -ge 2 ]] || usage; base_sha="$2"; shift 2 ;;
    --head-sha) [[ $# -ge 2 ]] || usage; head_sha="$2"; shift 2 ;;
    --destination) [[ $# -ge 2 ]] || usage; destination="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[[ -n "$source_ref" && -n "$destination" ]] || usage
[[ "$base_sha" =~ ^[0-9a-f]{40}$ ]] || { echo "base SHA must be 40 lowercase hexadecimal characters" >&2; exit 2; }
[[ "$head_sha" =~ ^[0-9a-f]{40}$ ]] || { echo "head SHA must be 40 lowercase hexadecimal characters" >&2; exit 2; }
[[ ! -e "$destination" ]] || { echo "destination already exists: $destination" >&2; exit 2; }

destination_parent="$(dirname "$destination")"
[[ -d "$destination_parent" ]] || { echo "destination parent does not exist: $destination_parent" >&2; exit 2; }

git clone --no-hardlinks --no-checkout --quiet -- "$source_ref" "$destination"

git -C "$destination" cat-file -e "$base_sha^{commit}" 2>/dev/null || {
  echo "base commit is unavailable from the authorized source: $base_sha" >&2
  exit 1
}
git -C "$destination" cat-file -e "$head_sha^{commit}" 2>/dev/null || {
  echo "head commit is unavailable from the authorized source: $head_sha" >&2
  exit 1
}
git -C "$destination" checkout --detach --quiet "$head_sha"

resolved_head="$(git -C "$destination" rev-parse HEAD)"
[[ "$resolved_head" == "$head_sha" ]] || {
  echo "materialized HEAD differs from requested head" >&2
  exit 1
}

printf 'destination\t%s\n' "$destination"
printf 'base_sha\t%s\n' "$base_sha"
printf 'head_sha\t%s\n' "$resolved_head"
