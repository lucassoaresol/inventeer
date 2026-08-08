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

state_section="$(sed -n '/^### AD-041$/,/^### AD-042$/p' .specs/STATE.md | tr '\n' ' ' | tr -s '[:space:]' ' ')"
[[ -n "$state_section" ]] || fail "AD-041 is missing"
grep -Fq 'preservar todos os outcomes APEX existentes' <<<"$state_section" \
  || fail "AD-041 does not preserve APEX compatibility"
grep -Fq 'janela UTC semiaberta `[since, until)`' <<<"$state_section" \
  || fail "AD-041 does not require reproducible closed cohorts"
grep -Fq 'somente agregados sanitizados' <<<"$state_section" \
  || fail "AD-041 does not bound persisted evidence"
grep -Fq 'dez sessões primárias elegíveis ou a próxima feature longa' <<<"$state_section" \
  || fail "AD-041 does not bound the pilot"
ok "AD-041 binds compatibility, privacy, reproducibility, and pilot duration"

grep -Fq 'recorte temporal fechado com `--since` e `--until`' AGENTS.md \
  || fail "retrospectives do not require a closed cohort"
grep -Fq '`contract_version`' AGENTS.md \
  || fail "retrospectives do not record the auditor contract"
ok "retrospectives require versioned closed cohorts"

pilot=.specs/features/workspace-session-resilience-v2/pilot.md
[[ -f "$pilot" ]] || fail "session resilience pilot is missing"
grep -Fq '**Status:** active' "$pilot" || fail "pilot is not active"
grep -Fq '**Baseline auditor contract:** 2' "$pilot" || fail "pilot contract is not versioned"
grep -Fq '**Baseline window:** `[2026-07-10T00:00:00Z, 2026-08-08T05:44:16Z)`' "$pilot" \
  || fail "pilot baseline window is not closed"
grep -Fq '**Excluded sessions:** 1' "$pilot" || fail "pilot exclusion count is missing"
grep -Fq '**Progress:** 0/10 eligible primary sessions' "$pilot" \
  || fail "pilot observation bound is missing"
ok "pilot provenance is exact and reproducible"

grep -Fq 'Primary sessions | 107' "$pilot" || fail "primary baseline is missing"
grep -Fq 'Sessions with aborts | 67 (62.62%)' "$pilot" || fail "abort baseline is missing"
grep -Fq 'Sessions with compactions | 38 (35.51%)' "$pilot" \
  || fail "compaction baseline is missing"
grep -Fq 'Claude primary sessions | 15' "$pilot" || fail "Claude baseline is missing"
grep -Fq 'source drift' "$pilot" || fail "pilot cannot classify closed-window backfill"
ok "pilot records exact sanitized aggregates and source-drift semantics"

grep -Fq 'ten eligible primary sessions or the next long workspace feature' "$pilot" \
  || fail "pilot closing trigger is missing"
grep -Fq 'two heavy gates started without a resource preflight' "$pilot" \
  || fail "preflight automation threshold is missing"
grep -Fq 'two status requests caused by silent long-running work' "$pilot" \
  || fail "progress automation threshold is missing"
grep -Fq 'one stale checkpoint after an interruption' "$pilot" \
  || fail "checkpoint automation threshold is missing"
grep -Fq 'recurring manual reconstruction' "$pilot" \
  || fail "manual reconstruction threshold is missing"
ok "pilot has an explicit closing review and bounded automation thresholds"

if grep -Eq '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|\.jsonl|~/\.codex|~/\.claude|/root/lucas' "$pilot"; then
  fail "pilot leaks session identity or transcript locations"
fi
ok "pilot persists no session identity or transcript location"

echo
echo "$passed teste(s) passaram."
