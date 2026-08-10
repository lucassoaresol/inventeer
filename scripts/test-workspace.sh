#!/usr/bin/env bash
set -euo pipefail

workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_root"
export PYTHONDONTWRITEBYTECODE=1

suite_count=0

run_suite() {
  local label="$1"
  shift
  echo "[workspace] $label"
  "$@"
  suite_count=$((suite_count + 1))
}

run_suite "engine routing" bash scripts/test-engine-routing.sh
run_suite "machine resource preflight" bash scripts/test-machine-resource-preflight.sh
run_suite "MCP configuration" python3 scripts/test-mcp-config.py
run_suite "consolidated documentation topology" bash scripts/test-consolidated-documentation-topology.sh
run_suite "Portal TLC session artifacts" bash scripts/test-portal-tlc-session-artifacts.sh
run_suite "PR review pilot behavior" python3 scripts/test-pr-review-pilot.py
run_suite "PR review workflow contract" python3 scripts/test-pr-review-workflow.py
run_suite "session history audit" python3 scripts/test-session-history-audit.py
run_suite "session resilience contract" bash scripts/test-session-resilience-contract.sh
run_suite "APEX command synchronization" bash scripts/test-sync-apex-commands.sh
run_suite "TLC checkpoint contract" bash scripts/test-tlc-checkpoint-contract.sh
run_suite "TLC checkpoint behavior" python3 scripts/test-tlc-checkpoint.py
run_suite "delivery-front inspector" bash .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh
run_suite "review bundle" bash .agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh
run_suite "TLC lessons" python3 .agents/skills/tlc-spec-driven/scripts/test-lessons.py
run_suite "TLC validation guidance" python3 .agents/skills/tlc-spec-driven/scripts/test-validation-guidance.py
run_suite "TLC deterministic gates" python3 scripts/test-tlc-deterministic-gates.py
run_suite "workspace structure" python3 scripts/test-workspace-structure.py

codex_skill_root="${CODEX_HOME:-${HOME}/.codex}/skills"
skill_validator="$codex_skill_root/.system/skill-creator/scripts/quick_validate.py"
if [[ ! -f "$skill_validator" ]]; then
  echo "skill validator not found: $skill_validator" >&2
  exit 1
fi
while IFS= read -r skill_dir; do
  python3 "$skill_validator" "$skill_dir" >/dev/null
done < <(find .agents/skills -mindepth 1 -maxdepth 1 -type d | sort)
suite_count=$((suite_count + 1))
echo "[workspace] all skill folders are structurally valid"

while IFS= read -r shell_file; do
  bash -n "$shell_file"
done < <(find scripts .agents/skills -type f -name '*.sh' | sort)
suite_count=$((suite_count + 1))
echo "[workspace] all shell files pass bash -n"

git diff --check
suite_count=$((suite_count + 1))
echo "[workspace] git diff --check passed"

echo "[workspace] $suite_count suites passed"
