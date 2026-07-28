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
  | grep -q '^\- \*\*Status\*\*: active$' \
  || fail "AD-026 is not active"
ok "a decisao antiga foi supersedida e a rota engine-aware esta ativa"

# shellcheck disable=SC2016 # Backticks are literal Markdown in the searched text.
grep -Fq 'no Codex, use sempre `tlc-spec-driven`' AGENTS.md \
  || fail "AGENTS.md does not route Codex delivery to TLC"
grep -q 'no Claude Code, use APEX quando o repo tiver' AGENTS.md \
  || fail "AGENTS.md does not route eligible Claude delivery to APEX"
grep -q 'A preparação continua sendo das skills locais de contexto' AGENTS.md \
  || fail "AGENTS.md does not preserve context-skill preparation before execution"
ok "AGENTS.md diferencia o executor por engine"

grep -q 'não criam uma execução APEX suportada' AGENTS.md \
  || fail "AGENTS.md conflates APEX resource access with supported execution"
grep -q 'invocação, contexto de' README.md \
  || fail "README.md omits workflow invocation and session context requirements"
grep -q 'sessão, artifacts e gates completos' README.md \
  || fail "README.md omits artifact and gate requirements"
grep -q 'única engine deste workspace que usa APEX como executor de entrega' README.md \
  || fail "README.md does not state the current APEX execution boundary"
grep -q 'entregas no Codex usam TLC' README.md \
  || fail "README.md does not state the Codex fallback"
ok "README.md documenta o mesmo limite operacional"

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
ok "Claude continua usando comandos nativos, sem wrappers duplicados"

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
