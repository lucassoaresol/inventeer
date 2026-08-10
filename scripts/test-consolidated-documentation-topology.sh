#!/usr/bin/env bash

set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

passed=0

fail() {
  echo "not ok - $*" >&2
  exit 1
}

ok() {
  passed=$((passed + 1))
  echo "ok $passed - $*"
}

ops_root='repos/inventeer-ops'
ids_root="$ops_root/artifacts/products/ids"
portal_docs_root="$ops_root/artifacts/products/portal"

grep -Fq "\`$ids_root\`" AGENTS.md \
  || fail "AGENTS.md does not name the consolidated IDS authority"
grep -Fq "\`$portal_docs_root\`" AGENTS.md \
  || fail "AGENTS.md does not name the consolidated Portal documentation authority"
ok "workspace instructions declare both consolidated product documentation roots"

for required in \
  "\`$ops_root\`" \
  "\`$ids_root\`" \
  "\`$portal_docs_root\`" \
  '`repos/portal-api`' \
  '`repos/portal-web`'; do
  grep -Fq "$required" projects/README.md \
    || fail "project registry is missing $required"
done
ok "project registry distinguishes shared documentation from Portal implementation"

grep -Fq "git clone <inventeer-ops-url> $ops_root" README.md \
  || fail "README.md does not clone inventeer-ops"
if grep -Eq '^git clone <(ids|portal)-url> repos/(ids|portal)$' README.md; then
  fail "README.md still instructs cloning a retired documentation repository"
fi
ok "local setup clones operations and omits retired documentation repositories"

grep -Fq "$ids_root" projects/ids.md \
  || fail "IDS project pointer does not resolve under inventeer-ops"
grep -Fq "$portal_docs_root" projects/portal.md \
  || fail "Portal project pointer does not resolve under inventeer-ops"
grep -Fq "$ops_root" projects/inventeer-ops.md \
  || fail "inventeer-ops project pointer is missing its repository root"
ok "logical project pointers resolve to the consolidated repository"

ad042="$(sed -n '/^### AD-042$/,/^## Handoff$/p' .specs/STATE.md)"
grep -Fq '**Status**: active' <<<"$ad042" \
  || fail "AD-042 is not active"
for decision in AD-010 AD-011 AD-012; do
  sed -n "/^### $decision$/,/^### AD-/p" .specs/STATE.md \
    | grep -Fq '**Status**: superseded by AD-042' \
    || fail "$decision does not point to AD-042"
done
ok "decision history points retired literal topology to AD-042"

grep -Fq 'test-consolidated-documentation-topology.sh' scripts/test-workspace.sh \
  || fail "aggregate workspace gate does not run the topology contract"
ok "aggregate workspace gate includes the topology contract"

assistants_surfaces=(
  projects/assistants.md
  .agents/skills/assistants-task-context/SKILL.md
  .agents/skills/assistants-task-context/references/ids-context.md
)
for file in "${assistants_surfaces[@]}"; do
  grep -Fq "$ops_root" "$file" \
    || fail "$file does not resolve the shared operations repository"
  grep -Fq 'artifacts/products/ids' "$file" \
    || fail "$file does not resolve the IDS subtree"
done
if rg -q 'repos/ids([/`[:space:]]|$)' "${assistants_surfaces[@]}"; then
  fail "an active Assistants surface still references the retired IDS repository"
fi
grep -Fq "$ids_root/clients/Inventeer-Internal/Inventeer-Assistants/" projects/assistants.md \
  || fail "Assistants project pointer does not resolve its governed IDS workspace"
ok "Assistants context resolves IDS through inventeer-ops without retired fallback"

echo
echo "$passed teste(s) passaram."
