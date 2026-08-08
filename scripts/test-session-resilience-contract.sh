#!/usr/bin/env bash
set -euo pipefail

workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_root"

passed=0

fail() {
  echo "not ok - $*" >&2
  exit 1
}

ok() {
  passed=$((passed + 1))
  echo "ok $passed - $*"
}

agents_text="$(tr '\n' ' ' < AGENTS.md | tr -s '[:space:]' ' ')"

grep -Fq 'não repita o valor' <<<"$agents_text" \
  || fail "potential secrets could be repeated"
grep -Fq 'use `[REDACTED]`' <<<"$agents_text" \
  || fail "potential secrets have no redaction marker"
ok "potential secrets are never repeated and use the canonical redaction marker"

grep -Fq 'natureza incerta como potencial segredo' <<<"$agents_text" \
  || fail "uncertain secret-like values are not contained"
ok "uncertain values are treated as potential secrets"

grep -Fq 'comandos exibidos, logs, commits, checkpoints ou artifacts versionados' <<<"$agents_text" \
  || fail "potential secrets could enter a durable or displayed surface"
ok "displayed and durable surfaces reject potential secrets"

grep -Fq '`.env` ignorado ou entrada interativa' <<<"$agents_text" \
  || fail "safe local credential input channels are not preferred"
ok "local credential use is routed to ignored or interactive input"

grep -Fq 'oriente a rotação de forma condicional' <<<"$agents_text" \
  || fail "potential exposure has no conditional rotation guidance"
grep -Fq 'sem afirmar que a credencial continua ativa' <<<"$agents_text" \
  || fail "rotation guidance could assert unknown credential state"
ok "rotation guidance remains conditional and evidence-bounded"

echo
echo "$passed teste(s) passaram."
