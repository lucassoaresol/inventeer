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
if grep -A24 '^### AD-036$' .specs/STATE.md | grep -q '\*\*Status\*\*: active'; then
  fail "AD-036 must be superseded"
fi
grep -A24 '^### AD-036$' .specs/STATE.md | grep -q '\*\*Status\*\*: superseded by AD-045' \
  || fail "AD-036 must be superseded by AD-045"
grep -A32 '^### AD-045$' .specs/STATE.md | grep -q '\*\*Status\*\*: active' \
  || fail "AD-045 must be active"
pass "AD-045 records the active checkpoint decision"

agent_checkpoint=$(grep -A16 'checkpoints TLC resilientes' AGENTS.md | tr '\n' ' ' | tr -s '[:space:]' ' ')
for trigger in gate commit bundle PR validation pre-heavy; do
  grep -Fq "$trigger" <<<"$agent_checkpoint" \
    || fail "AGENTS.md is missing checkpoint trigger: $trigger"
done
grep -q 'somente depois.*sucesso' <<<"$agent_checkpoint" \
  || fail "AGENTS.md does not require successful transitions"
grep -q 'Não avance.*falh' <<<"$agent_checkpoint" \
  || fail "AGENTS.md does not prohibit checkpoint advancement on failure"
grep -q 'Imediatamente antes.*etapa pesada' <<<"$agent_checkpoint" \
  || fail "AGENTS.md does not require a checkpoint immediately before heavy work"
grep -q 'preflight de recursos.*reconciliação do estado atual' <<<"$agent_checkpoint" \
  || fail "AGENTS.md does not gate pre-heavy on preflight and reconciliation"
pass "workspace instructions require all six stable-transition checkpoints"

grep -A16 'checkpoints TLC resilientes' AGENTS.md | grep -q 'qualquer uma das duas engines' \
  || fail "AGENTS.md does not require checkpoints in both engines"
grep -A50 'Checkpoints resilientes da TLC' README.md | grep -q 'qualquer uma das duas engines' \
  || fail "README.md does not document checkpoints in both engines"
pass "Codex e Claude compartilham os checkpoints Portal TLC"

grep -Fq 'scripts/update-tlc-checkpoint.py' README.md \
  || fail "README.md does not document the checkpoint helper"
grep -Fq 'session-context/portal/<INV-ID>/tlc/STATE.md' README.md \
  || fail "README.md does not document the exact checkpoint target"
for trigger in gate commit bundle pr validation pre-heavy; do
  grep -A45 'Checkpoints resilientes da TLC' README.md | grep -Fq "$trigger" \
    || fail "README.md is missing helper event: $trigger"
done
pass "README documents the deterministic helper, target, and events"

checkpoint_docs_normalized=$(grep -A50 'Checkpoints resilientes da TLC' README.md | tr '\n' ' ' | tr -s '[:space:]' ' ')
grep -q 'preflight de recursos.*reconciliação do estado atual' <<<"$checkpoint_docs_normalized" \
  || fail "README.md does not document the pre-heavy prerequisites"
pass "README requires fresh state before pre-heavy work"

checkpoint_docs=$(grep -A45 'Checkpoints resilientes da TLC' README.md)
for property in 'local' 'efêmero' 'não canônico' 'não oferece portabilidade cross-machine'; do
  grep -Fq "$property" <<<"$checkpoint_docs" \
    || fail "README.md is missing checkpoint lifecycle property: $property"
done
grep -q 'merge.*issue encerrada' <<<"$checkpoint_docs" \
  || fail "README.md does not preserve AD-031 cleanup timing"
grep -q 'pode perder trabalho posterior' <<<"$checkpoint_docs" \
  || fail "README.md does not disclose the residual checkpoint window"
grep -q 'liveness' <<<"$checkpoint_docs" \
  || fail "README.md does not require stale-process revalidation"
grep -A24 '^### AD-036$' .specs/STATE.md | grep -q 'single-writer' \
  || fail "AD-036 does not preserve the single-writer boundary"
pass "checkpoint lifecycle remains local, ephemeral, non-canonical, and non-portable"

grep -A12 'checkpoints TLC resilientes' AGENTS.md | grep -q 'somente paths' \
  || fail "AGENTS.md does not constrain uncommitted state to path labels"
grep -A45 'Checkpoints resilientes da TLC' README.md | grep -q 'transcripts.*diffs.*credenciais' \
  || fail "README.md does not preserve the checkpoint privacy boundary"
pass "checkpoint content is constrained to sanitized execution metadata"

grep -A24 '^### AD-031$' .specs/STATE.md | grep -q '\*\*Status\*\*: superseded by AD-045' \
  || fail "AD-031 must be superseded by AD-045"
grep -A24 '^### AD-032$' .specs/STATE.md | grep -q '\*\*Status\*\*: active' \
  || fail "AD-032 must remain active"
if rg -q 'update-tlc-checkpoint|portal/<INV-ID>/tlc/STATE.md' .agents/skills/tlc-spec-driven; then
  fail "vendored TLC must remain free of the workspace-specific checkpoint contract"
fi
pass "AD-045, AD-032, and the vendored TLC preserve their authority boundaries"

test -z "$(git ls-files session-context)" \
  || fail "session-context checkpoint state must remain untracked"
git check-ignore -q session-context/portal/INV-3145/tlc/STATE.md \
  || fail "checkpoint target must be ignored by Git"
pass "checkpoint runtime state stays outside Git"

echo
echo "$passed teste(s) passaram."
