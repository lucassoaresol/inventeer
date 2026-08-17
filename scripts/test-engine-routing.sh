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

grep -A18 '^### AD-025$' .specs/STATE.md \
  | grep -q '^\- \*\*Status\*\*: superseded by AD-026$' \
  || fail "AD-025 is not superseded by AD-026"
grep -A26 '^### AD-026$' .specs/STATE.md \
  | grep -q '^\- \*\*Status\*\*: superseded by AD-045$' \
  || fail "AD-026 is not superseded by AD-045"
grep -A32 '^### AD-045$' .specs/STATE.md \
  | grep -q '^\- \*\*Status\*\*: active$' \
  || fail "AD-045 is not active"
ok "as rotas antigas foram supersedidas e o executor unificado esta ativo"

# shellcheck disable=SC2016 # Backticks are literal Markdown in the searched text.
grep -Fq 'Use sempre `tlc-spec-driven` como executor' AGENTS.md \
  || fail "AGENTS.md does not declare TLC as the shared executor"
grep -q 'no Codex e' AGENTS.md \
  || fail "AGENTS.md does not include Codex in shared TLC routing"
grep -q 'no Claude Code' AGENTS.md \
  || fail "AGENTS.md does not include Claude Code in shared TLC routing"
grep -q 'A preparação continua sendo das skills locais de' AGENTS.md \
  || fail "AGENTS.md does not preserve context-skill preparation before execution"
ok "AGENTS.md usa TLC nos dois engines"

grep -q 'não criam uma execução APEX suportada' AGENTS.md \
  || fail "AGENTS.md conflates APEX resource access with supported execution"
grep -q 'invocação, contexto de' README.md \
  || fail "README.md omits workflow invocation and session context requirements"
grep -q 'sessão, artifacts e gates completos' README.md \
  || fail "README.md omits artifact and gate requirements"
grep -q 'Codex e Claude Code usam TLC' README.md \
  || fail "README.md does not state the shared TLC executor"
grep -q 'APEX permanece disponível para inspeção e diagnóstico' README.md \
  || fail "README.md does not preserve the diagnostic APEX boundary"
grep -q 'Uma chamada bem-sucedida isolada também não conclui um workflow' README.md \
  || fail "README.md conflates isolated APEX success with workflow execution"
ok "README.md documenta o executor compartilhado e o limite APEX"

mapfile -t wrappers < <(find .agents/skills -mindepth 2 -maxdepth 2 -path '*/apex-*/SKILL.md' | sort)
((${#wrappers[@]} > 0)) || fail "no generated APEX wrappers found"
for wrapper in "${wrappers[@]}"; do
  grep -q 'não use como executor de entrega' "$wrapper" \
    || fail "$wrapper omits the experimental boundary"
  # shellcheck disable=SC2016 # Backticks are literal Markdown in the wrapper.
  grep -Fq 'Use `tlc-spec-driven` como executor' "$wrapper" \
    || fail "$wrapper omits the Codex executor"
done
ok "todos os wrappers declaram o limite experimental e o fallback TLC"

if rg -q 'lê e executa|Siga integralmente o workflow retornado' .agents/skills/apex-*; then
  fail "a generated wrapper still claims supported workflow execution"
fi
ok "nenhum wrapper preserva a alegacao antiga de execucao"

if find .claude/skills -maxdepth 1 -name 'apex-*' -print -quit | grep -q .; then
  fail "APEX wrappers should not be exposed to Claude Code"
fi
grep -q 'No Claude Code, trate também os workflows nativos' AGENTS.md \
  || fail "Claude native APEX workflows are not bounded to diagnostics"
ok "Claude preserva comandos nativos apenas como diagnostico, sem wrappers duplicados"

# shellcheck disable=SC2088 # Tildes are literal documentation text, not filesystem paths.
for path in '~/.codex/sessions/' '~/.claude/projects/'; do
  grep -Fq "$path" AGENTS.md || fail "AGENTS.md omits history source $path"
  grep -Fq "$path" README.md || fail "README.md omits history source $path"
done
grep -q 'sessões principais, continuations e cópias' AGENTS.md \
  || fail "AGENTS.md does not distinguish primary sessions from continuations and copies"
grep -q 'não conte a própria retrospectiva como evidência' AGENTS.md \
  || fail "AGENTS.md does not exclude the current retrospective"
grep -q 'Sessions retomadas,' README.md \
  || fail "README.md does not identify resumed sessions"
grep -q 'sidechains e cópias' README.md \
  || fail "README.md does not distinguish sidechains and copies"
grep -q 'retrospectiva é excluída do recorte' README.md \
  || fail "README.md does not exclude the current retrospective"
ok "as duas fontes de historico participam das retrospectivas"

grep -q 'decisão transversal em.*STATE.md' AGENTS.md \
  || fail "AGENTS.md does not route transversal decisions to STATE.md"
grep -q 'lesson de' AGENTS.md \
  || fail "AGENTS.md does not route confirmed execution lessons through TLC"
grep -q 'achado de produto na fonte do produto' AGENTS.md \
  || fail "AGENTS.md does not keep product findings in the product source"
grep -q 'decisões transversais em.*STATE.md' README.md \
  || fail "README.md does not route transversal decisions to STATE.md"
grep -q 'falhas de execução confirmadas por' README.md \
  || fail "README.md does not route confirmed execution failures through TLC"
grep -q 'achados específicos de produto no repositório ou fonte' README.md \
  || fail "README.md does not keep product findings in the product source"
ok "cada classe de aprendizado tem destino canonico explicito"

if git ls-files '*.jsonl' | grep -q .; then
  fail "raw session transcripts are tracked by Git"
fi
ok "nenhum transcript JSONL bruto foi versionado"

echo
echo "$passed teste(s) passaram."
