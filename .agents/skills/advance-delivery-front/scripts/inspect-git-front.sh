#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: inspect-git-front.sh --repo PATH --integration-ref REF [options]

Options:
  --repo PATH             Git repository to inspect (required)
  --integration-ref REF  Integration ref used for comparison (required)
  --work-ref REF         Work ref to inspect (default: HEAD)
  --boundary-ref REF     Optional boundary for dependent-task commits and paths
  --captured-at VALUE    Optional timestamp override for deterministic capture
  -h, --help             Show this help
EOF
}

die() {
  echo "Error: $*" >&2
  exit 2
}

emit() {
  local key="$1"
  local value="$2"

  printf '%s\t%q\n' "$key" "$value" >>"$snapshot_file"
}

resolve_commit() {
  local repo_path="$1"
  local ref="$2"

  git -C "$repo_path" rev-parse --verify --end-of-options "${ref}^{commit}" 2>/dev/null
}

repo=""
integration_ref=""
work_ref="HEAD"
boundary_ref=""
captured_at=""

while (($# > 0)); do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || die "--repo requires a value"
      repo="$2"
      shift 2
      ;;
    --integration-ref)
      [[ $# -ge 2 ]] || die "--integration-ref requires a value"
      integration_ref="$2"
      shift 2
      ;;
    --work-ref)
      [[ $# -ge 2 ]] || die "--work-ref requires a value"
      work_ref="$2"
      shift 2
      ;;
    --boundary-ref)
      [[ $# -ge 2 ]] || die "--boundary-ref requires a value"
      boundary_ref="$2"
      shift 2
      ;;
    --captured-at)
      [[ $# -ge 2 ]] || die "--captured-at requires a value"
      captured_at="$2"
      shift 2
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

[[ -n "$repo" ]] || die "--repo is required"
[[ -n "$integration_ref" ]] || die "--integration-ref is required"
[[ "$captured_at" != *$'\n'* && "$captured_at" != *$'\t'* ]] || die "--captured-at must be one line"

repo_root="$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)" || die "invalid Git repository: $repo"
integration_sha="$(resolve_commit "$repo_root" "$integration_ref")" || die "invalid integration ref: $integration_ref"
work_sha="$(resolve_commit "$repo_root" "$work_ref")" || die "invalid work ref: $work_ref"
merge_base_sha="$(git -C "$repo_root" merge-base "$integration_sha" "$work_sha" 2>/dev/null)" || {
  die "integration and work refs have no merge base"
}

boundary_sha=""
if [[ -n "$boundary_ref" ]]; then
  boundary_sha="$(resolve_commit "$repo_root" "$boundary_ref")" || die "invalid boundary ref: $boundary_ref"
  git -C "$repo_root" merge-base --is-ancestor "$boundary_sha" "$work_sha" 2>/dev/null || {
    die "boundary ref is not an ancestor of work ref: $boundary_ref"
  }
fi

captured_at="${captured_at:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
current_branch="$(git -C "$repo_root" branch --show-current)"
current_branch="${current_branch:-detached-HEAD}"

snapshot_file="$(mktemp /tmp/inspect-git-front.XXXXXX)"
trap 'rm -f "$snapshot_file"' EXIT

emit schema_version 1
emit captured_at "$captured_at"
emit repo_root "$repo_root"
emit current_branch "$current_branch"
emit integration_ref "$integration_ref"
emit integration_sha "$integration_sha"
emit work_ref "$work_ref"
emit work_sha "$work_sha"
emit merge_base_sha "$merge_base_sha"

if [[ -n "$boundary_ref" ]]; then
  emit boundary_ref "$boundary_ref"
  emit boundary_sha "$boundary_sha"
fi

while IFS= read -r -d '' status_record; do
  emit worktree_status "$status_record"
done < <(git -C "$repo_root" status --porcelain=v1 -z --untracked-files=all)

while IFS= read -r -d '' worktree_record; do
  emit worktree_entry "$worktree_record"
done < <(git -C "$repo_root" worktree list --porcelain -z)

while IFS= read -r -d '' changed_path; do
  emit changed_path "$changed_path"
done < <(git -C "$repo_root" diff --name-only -z "$integration_sha...$work_sha" --)

if [[ -n "$boundary_sha" ]]; then
  while IFS= read -r commit_sha; do
    emit task_commit "$commit_sha"
  done < <(git -C "$repo_root" rev-list --reverse "$boundary_sha..$work_sha")

  while IFS= read -r -d '' task_path; do
    emit task_changed_path "$task_path"
  done < <(git -C "$repo_root" diff --name-only -z "$boundary_sha..$work_sha" --)
fi

cat "$snapshot_file"
