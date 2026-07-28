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

grep -q 'no Codex, use sempre `tlc-spec-driven`' AGENTS.md \
  || fail "AGENTS.md does not route Codex delivery to TLC"
grep -q 'no Claude Code, use APEX quando o repo tiver' AGENTS.md \
  || fail "AGENTS.md does not route eligible Claude delivery to APEX"
ok "AGENTS.md diferencia o executor por engine"

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
  grep -q 'Use `tlc-spec-driven` como executor' "$wrapper" \
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

for path in '~/.codex/sessions/' '~/.claude/projects/'; do
  grep -Fq "$path" AGENTS.md || fail "AGENTS.md omits history source $path"
  grep -Fq "$path" README.md || fail "README.md omits history source $path"
done
ok "as duas fontes de historico participam das retrospectivas"

if git ls-files '*.jsonl' | grep -q .; then
  fail "raw session transcripts are tracked by Git"
fi
ok "nenhum transcript JSONL bruto foi versionado"

echo
echo "$passed teste(s) passaram."
