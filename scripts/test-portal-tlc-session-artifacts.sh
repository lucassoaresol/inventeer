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
  | grep -q '^\- \*\*Status\*\*: active$' \
  || fail "AD-031 is not active"
ok "a decisao transitoria esta ativa"

for file in AGENTS.md README.md .agents/skills/portal-task-context/SKILL.md; do
  grep -Fq "$contract_path" "$file" \
    || fail "$file does not declare the Portal TLC session path"
done
ok "instrucoes, documentacao e skill usam o mesmo path"

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
grep -q 'não oferece portabilidade cross-machine' .specs/STATE.md \
  || fail "AD-031 does not preserve the cross-machine limitation"
ok "review e limpeza possuem lifecycle explicito"

grep -q 'deve ser retirada quando o Codex executar APEX' AGENTS.md \
  || fail "AGENTS.md does not define the transition exit condition"
grep -q 'end-to-end; não a aplique' AGENTS.md \
  || fail "AGENTS.md does not bind the exit condition to end-to-end APEX"
grep -q 'Claude/APEX e outros produtos permanecem' README.md \
  || fail "README.md does not preserve the Claude/APEX route"
grep -q '^inalterados, e o lifecycle oficial do APEX' README.md \
  || fail "README.md does not keep the official APEX lifecycle"
ok "a rota e transitoria e restrita ao Portal no Codex"

if rg -q 'session-context/portal/<INV-ID>/tlc/' .agents/skills/tlc-spec-driven; then
  fail "the vendored TLC skill contains the Portal-specific path"
fi
ok "a TLC generica permanece sem politica especifica do Portal"

if git ls-files 'session-context/**' | grep -q .; then
  fail "session-context artifacts are tracked by Git"
fi
ok "nenhum artifact efemero esta versionado"

python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/portal-task-context >/dev/null
ok "portal-task-context passa na validacao estrutural"

echo
echo "$passed teste(s) passaram."
