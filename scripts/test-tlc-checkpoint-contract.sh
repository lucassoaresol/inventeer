#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

passed=0

pass() {
  passed=$((passed + 1))
  echo "ok $passed - $1"
}

fail() {
  echo "not ok $((passed + 1)) - $1" >&2
  exit 1
}

test "$(grep -c '^### AD-036$' .specs/STATE.md)" -eq 1 \
  || fail "AD-036 must exist exactly once"
grep -A24 '^### AD-036$' .specs/STATE.md | grep -q '\*\*Status\*\*: active' \
  || fail "AD-036 must be active"
pass "AD-036 records the active checkpoint decision"

for trigger in gate commit bundle PR validation; do
  grep -A12 'checkpoints TLC resilientes' AGENTS.md | grep -Fq "$trigger" \
    || fail "AGENTS.md is missing checkpoint trigger: $trigger"
done
grep -A12 'checkpoints TLC resilientes' AGENTS.md | grep -q 'somente depois.*sucesso' \
  || fail "AGENTS.md does not require successful transitions"
grep -A12 'checkpoints TLC resilientes' AGENTS.md | grep -q 'não avance.*falh' \
  || fail "AGENTS.md does not prohibit checkpoint advancement on failure"
pass "workspace instructions require all five successful-transition checkpoints"

grep -Fq 'scripts/update-tlc-checkpoint.py' README.md \
  || fail "README.md does not document the checkpoint helper"
grep -Fq 'session-context/portal/<INV-ID>/tlc/STATE.md' README.md \
  || fail "README.md does not document the exact checkpoint target"
for trigger in gate commit bundle pr validation; do
  grep -A45 'Checkpoints resilientes da TLC' README.md | grep -Fq "$trigger" \
    || fail "README.md is missing helper event: $trigger"
done
pass "README documents the deterministic helper, target, and events"

checkpoint_docs=$(grep -A45 'Checkpoints resilientes da TLC' README.md)
for property in 'local' 'efêmero' 'não canônico' 'não oferece portabilidade cross-machine'; do
  grep -Fq "$property" <<<"$checkpoint_docs" \
    || fail "README.md is missing checkpoint lifecycle property: $property"
done
grep -q 'merge.*issue encerrada' <<<"$checkpoint_docs" \
  || fail "README.md does not preserve AD-031 cleanup timing"
pass "checkpoint lifecycle remains local, ephemeral, non-canonical, and non-portable"

grep -A12 'checkpoints TLC resilientes' AGENTS.md | grep -q 'somente paths' \
  || fail "AGENTS.md does not constrain uncommitted state to path labels"
grep -A45 'Checkpoints resilientes da TLC' README.md | grep -q 'transcripts.*diffs.*credenciais' \
  || fail "README.md does not preserve the checkpoint privacy boundary"
pass "checkpoint content is constrained to sanitized execution metadata"

grep -A24 '^### AD-031$' .specs/STATE.md | grep -q '\*\*Status\*\*: active' \
  || fail "AD-031 must remain active"
grep -A24 '^### AD-032$' .specs/STATE.md | grep -q '\*\*Status\*\*: active' \
  || fail "AD-032 must remain active"
if rg -q 'update-tlc-checkpoint|portal/<INV-ID>/tlc/STATE.md' .agents/skills/tlc-spec-driven; then
  fail "vendored TLC must remain free of the workspace-specific checkpoint contract"
fi
pass "AD-031, AD-032, and the vendored TLC remain unchanged in authority"

test -z "$(git ls-files session-context)" \
  || fail "session-context checkpoint state must remain untracked"
git check-ignore -q session-context/portal/INV-3145/tlc/STATE.md \
  || fail "checkpoint target must be ignored by Git"
pass "checkpoint runtime state stays outside Git"

echo
echo "$passed teste(s) passaram."
