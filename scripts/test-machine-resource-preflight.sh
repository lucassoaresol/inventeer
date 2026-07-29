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

output="$(./scripts/check-machine-resources.sh)"

for key in online_cpus load_average_1m memory_available_bytes swap_total_bytes filesystem_available_bytes; do
  grep -q "^${key}"$'\t''[0-9]' <<<"$output" || fail "snapshot omits numeric $key"
done
ok "snapshot reports CPU, load, memory, swap and filesystem capacity"

grep -q 'Antes de tarefas potencialmente pesadas' AGENTS.md \
  || fail "AGENTS.md omits the machine preflight trigger"
grep -q './scripts/check-machine-resources.sh' AGENTS.md \
  || fail "AGENTS.md omits the canonical preflight command"
ok "workspace instructions require the canonical preflight"

guidance=.agents/skills/tlc-spec-driven/references/implement.md
grep -q '^### Resource preflight before heavy work' "$guidance" \
  || fail "TLC implement guidance omits resource preflight"
grep -q 'run every required shard' "$guidance" \
  || fail "TLC preflight does not preserve complete gate coverage"
grep -q 'bounded concurrency' "$guidance" \
  || fail "TLC preflight does not constrain concurrency"
ok "TLC adapts concurrency without weakening the gate"

jq -e '."tlc-spec-driven".local_customizations | index("resource-aware execution preflight")' \
  .agents/vendor.json >/dev/null \
  || fail "vendor manifest omits the local TLC customization"
ok "vendored fork manifest tracks the preflight customization"

echo
echo "$passed teste(s) passaram."
