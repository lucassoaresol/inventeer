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

contract_path='session-context/portal/<INV-ID>/tlc/'

grep -A24 '^### AD-031$' .specs/STATE.md \
  | grep -q '^\- \*\*Status\*\*: superseded by AD-045$' \
  || fail "AD-031 is not superseded by AD-045"
grep -A32 '^### AD-045$' .specs/STATE.md \
  | grep -q '^\- \*\*Status\*\*: active$' \
  || fail "AD-045 is not active"
ok "a rota Portal TLC consolidada esta ativa"

for file in AGENTS.md README.md .agents/skills/portal-task-context/SKILL.md; do
  grep -Fq "$contract_path" "$file" \
    || fail "$file does not declare the Portal TLC session path"
done
ok "instrucoes, documentacao e skill usam o mesmo path"

grep -q 'Codex or Claude Code' .agents/skills/portal-task-context/SKILL.md \
  || fail "portal-task-context does not apply the TLC route to both engines"
grep -q 'Codex and Claude Code' .agents/skills/portal-task-context/references/specification-policy.md \
  || fail "specification policy does not apply the TLC route to both engines"
grep -q 'compartilhada pelos dois engines' README.md \
  || fail "README.md does not apply the Portal TLC route to both engines"
ok "Codex e Claude compartilham o contrato Portal TLC"

grep -q 'Esse material é local' AGENTS.md \
  || fail "AGENTS.md does not classify the artifacts as local"
grep -q 'efêmero, não canônico e não durável' AGENTS.md \
  || fail "AGENTS.md does not classify the artifacts as ephemeral"
grep -q 'canônicos, oficiais nem duráveis' README.md \
  || fail "README.md does not reject canonical and durable status"
grep -q 'must not be presented as canonical, durable, or official APEX evidence' \
  .agents/skills/portal-task-context/SKILL.md \
  || fail "portal-task-context does not preserve the authority boundary"
grep -q 'Código, testes, ADRs e' README.md \
  || fail "README.md does not preserve product repositories as official surfaces"
grep -q 'Linear e a PR preservam o resumo oficial' README.md \
  || fail "README.md does not preserve Linear and the PR as official surfaces"
ok "o lifecycle local nao concorre com evidencia oficial"

# shellcheck disable=SC2016 # Backticks are literal Markdown in the searched text.
for forbidden_root in \
  'repos/inventeer-ops/artifacts/products/portal' \
  'repos/portal-api' \
  'repos/portal-web'; do
  grep -Fq "\`$forbidden_root\`" .agents/skills/portal-task-context/SKILL.md \
    || fail "portal-task-context does not forbid TLC specs in $forbidden_root"
done
grep -q 'Working TLC artifacts are not product specifications' \
  .agents/skills/portal-task-context/references/specification-policy.md \
  || fail "specification policy conflates TLC working state with product specs"
grep -q 'surface the durable' \
  .agents/skills/portal-task-context/references/specification-policy.md \
  || fail "specification policy does not surface durable artifacts as a delivery constraint"
grep -q 'Create files there only' .agents/skills/portal-task-context/SKILL.md \
  || fail "portal-task-context does not preserve inline TLC operation"
ok "nenhum artifact TLC local vira spec de produto"

grep -Fq 'session-context/portal/<INV-ID>/review/' README.md \
  || fail "README.md does not group review evidence by Portal issue"
grep -q 'merge.*encerr' README.md \
  || fail "README.md does not define post-delivery cleanup"
grep -q 'não sincroniza artifacts' README.md \
  || fail "README.md does not preserve the cross-machine limitation"
grep -q 'On another machine, reconstruct state from canonical sources' \
  .agents/skills/portal-task-context/SKILL.md \
  || fail "portal-task-context does not define cross-machine reconstruction"
ok "review, limpeza e retomada cross-machine possuem lifecycle explicito"

grep -q 'APEX permanece diagnóstico até uma nova decisão' AGENTS.md \
  || fail "AGENTS.md does not preserve the APEX diagnostic boundary"
grep -q 'futura adoção de APEX exige nova decisão' README.md \
  || fail "README.md does not bind APEX adoption to a new decision"
grep -q 'outros produtos permanecem inalterados' README.md \
  || fail "README.md does not preserve the non-Portal boundary"
ok "a rota e compartilhada entre engines e restrita ao Portal"

if rg -q 'session-context/portal/<INV-ID>/tlc/' .agents/skills/tlc-spec-driven; then
  fail "the vendored TLC skill contains the Portal-specific path"
fi
ok "a TLC generica permanece sem politica especifica do Portal"

if git ls-files 'session-context/**' | grep -q .; then
  fail "session-context artifacts are tracked by Git"
fi
ok "nenhum artifact efemero esta versionado"

codex_skill_root="${CODEX_HOME:-${HOME}/.codex}/skills"
python3 "$codex_skill_root/.system/skill-creator/scripts/quick_validate.py" \
  .agents/skills/portal-task-context >/dev/null
ok "portal-task-context passa na validacao estrutural"

echo
echo "$passed teste(s) passaram."
