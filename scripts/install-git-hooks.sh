#!/usr/bin/env bash
set -euo pipefail

workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  echo "hooks installer: $*" >&2
  exit 1
}

repository_root="$(git -C "$workspace_root" rev-parse --show-toplevel 2>/dev/null)" \
  || fail "script must run inside its repository"
[[ "$repository_root" == "$workspace_root" ]] \
  || fail "script must run from its repository root"
[[ -d "$workspace_root/.githooks" && ! -L "$workspace_root/.githooks" ]] \
  || fail "versioned hook directory is missing or unsafe"
[[ -f "$workspace_root/.githooks/pre-commit" && ! -L "$workspace_root/.githooks/pre-commit" ]] \
  || fail "versioned pre-commit hook is missing or unsafe"

set +e
current="$(git -C "$workspace_root" config --local --get core.hooksPath 2>/dev/null)"
status=$?
set -e
if [[ $status -eq 0 ]]; then
  [[ "$current" == ".githooks" ]] || fail "core.hooksPath already has a conflicting value"
  echo "hooks installer: already configured core.hooksPath=.githooks"
  exit 0
fi
[[ $status -eq 1 ]] || fail "could not inspect core.hooksPath"

git -C "$workspace_root" config --local core.hooksPath .githooks \
  || fail "could not configure core.hooksPath"
echo "hooks installer: configured core.hooksPath=.githooks"
