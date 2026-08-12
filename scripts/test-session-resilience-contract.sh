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

closing_decision="$(sed -n '/^### AD-044$/,/^## Handoff$/p' .specs/STATE.md | tr '\n' ' ' | tr -s '[:space:]' ' ')"
[[ -n "$closing_decision" ]] || fail "AD-044 is missing"
grep -Fq 'Encerrar o piloto delimitado da AD-041' <<<"$closing_decision" \
  || fail "AD-044 does not close the bounded pilot"
grep -Fq 'roteamento de contexto, guardrail staged, checkpoint `pre-heavy`' <<<"$closing_decision" \
  || fail "AD-044 does not name the authorized automation"
grep -Fq 'somente ao workspace raiz e à rota Portal + Codex + TLC já delimitada' <<<"$closing_decision" \
  || fail "AD-044 widens the automation authority"
grep -Fq 'não autoriza automação nos repositórios de produto' <<<"$closing_decision" \
  || fail "AD-044 does not preserve product-repository ownership"
ok "AD-044 closes the pilot and bounds the authorized automation"

grep -Fq 'recorte temporal fechado com `--since` e `--until`' AGENTS.md \
  || fail "retrospectives do not require a closed cohort"
grep -Fq '`contract_version`' AGENTS.md \
  || fail "retrospectives do not record the auditor contract"
ok "retrospectives require versioned closed cohorts"

pilot=.specs/features/workspace-session-resilience-v2/pilot.md
[[ -f "$pilot" ]] || fail "session resilience pilot is missing"
pilot_text="$(tr '\n' ' ' < "$pilot" | tr -s '[:space:]' ' ')"
grep -Fq '**Status:** closed' "$pilot" || fail "pilot is not closed"
grep -Fq '**Closed at (UTC):** 2026-08-12T12:02:51.057Z' "$pilot" \
  || fail "pilot closing boundary is missing"
grep -Fq '**Baseline auditor contract:** 2' "$pilot" || fail "pilot contract is not versioned"
grep -Fq '**Baseline window:** `[2026-07-10T00:00:00Z, 2026-08-08T05:44:16Z)`' "$pilot" \
  || fail "pilot baseline window is not closed"
grep -Fq '**Excluded sessions:** 1' "$pilot" || fail "pilot exclusion count is missing"
grep -Fq '**Closing window:** `[2026-08-08T05:44:16Z, 2026-08-12T12:02:51.057Z)`' "$pilot" \
  || fail "pilot closing window is not exact"
grep -Fq '**Closing excluded sessions:** 1' "$pilot" \
  || fail "pilot closing exclusion count is missing"
grep -Fq '**Closing trigger:** long workspace feature completed' "$pilot" \
  || fail "pilot closing trigger is missing"
ok "pilot closing provenance is exact and reproducible"

grep -Fq 'Primary sessions | 107' "$pilot" || fail "primary baseline is missing"
grep -Fq 'Sessions with aborts | 67 (62.62%)' "$pilot" || fail "abort baseline is missing"
grep -Fq 'Sessions with compactions | 38 (35.51%)' "$pilot" \
  || fail "compaction baseline is missing"
grep -Fq 'Claude primary sessions | 15' "$pilot" || fail "Claude baseline is missing"
grep -Fq 'source drift' "$pilot" || fail "pilot cannot classify closed-window backfill"
ok "pilot records exact sanitized aggregates and source-drift semantics"

for closing_aggregate in \
  '| Codex primary sessions | 107 | 34 |' \
  '| Codex continuations | 37 | 13 |' \
  '| Codex sessions with aborts | 67 (62.62%) | 15 (44.12%) |' \
  '| Maximum aborts in one Codex primary session | 6 | 4 |' \
  '| Codex sessions with compactions | 38 (35.51%) | 10 (29.41%) |' \
  '| Maximum compactions in one Codex primary session | 4 | 2 |' \
  '| Claude primary sessions | 15 | 4 |' \
  '| Claude sidechains | 0 | 0 |'
do
  grep -Fq "$closing_aggregate" <<<"$pilot_text" \
    || fail "pilot closing aggregate is missing: $closing_aggregate"
done
ok "pilot records the exact baseline and closing comparison"

for limitation in \
  'Verified work lost after an interruption' \
  'Heavy stages started without a resource preflight' \
  'Heavy stages started from a stale checkpoint' \
  'Status requests attributable to silent long-running work' \
  'Resumptions requiring more than one Git, Handoff, and tasks reconciliation' \
  'Potential secrets repeated or persisted by an agent'
do
  grep -Fq "| $limitation | Not prospectively measured |" <<<"$pilot_text" \
    || fail "pilot limitation is missing: $limitation"
done
grep -Fq 'The sanitized auditor cannot reconstruct these measures from history alone.' <<<"$pilot_text" \
  || fail "pilot overclaims its retrospective measurements"
ok "pilot states every unmeasured success dimension"

grep -Fq 'The recurring manual reconstruction threshold was satisfied.' <<<"$pilot_text" \
  || fail "pilot does not apply the automation decision gate"
grep -Fq 'The pilot authorizes only the scoped root-workspace and Portal checkpoint changes recorded in AD-044.' <<<"$pilot_text" \
  || fail "pilot closing outcome does not preserve the authority boundary"
ok "pilot records the closing trigger and scoped automation outcome"

for eligibility_rule in \
  'is a new primary Codex or Claude session originating from the exact workspace root after the pilot start;' \
  'performs material planning, implementation, validation, review, or workflow maintenance;' \
  'is not the retrospective performing the measurement;' \
  'is not a copy, continuation, sidechain, or subagent;' \
  'is classified by the sanitized auditor before transcript interpretation.'
do
  grep -Fq "$eligibility_rule" <<<"$pilot_text" \
    || fail "pilot eligibility rule is missing: $eligibility_rule"
done
ok "every pilot eligibility rule is exact"

for success_measure in \
  '| Verified work lost after an interruption | 0 |' \
  '| Heavy stages started without a resource preflight | 0 |' \
  '| Heavy stages started from a stale checkpoint | 0 |' \
  '| Status requests attributable to silent long-running work | 0 |' \
  '| Resumptions requiring more than one Git, Handoff, and tasks reconciliation | 0 |' \
  '| Potential secrets repeated or persisted by an agent | 0 |'
do
  grep -Fq "$success_measure" <<<"$pilot_text" \
    || fail "pilot success measure is missing: $success_measure"
done
ok "every pilot success measure is exact"

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

grep -Fq 'contract version 2, the exact closing window above, and one excluded current session' <<<"$pilot_text" \
  || fail "pilot does not record the completed auditor boundary"
grep -Fq 'No closed-window source drift was observed in the frozen comparison.' <<<"$pilot_text" \
  || fail "pilot does not classify source drift"
grep -Fq 'The comparison therefore does not claim that any zero target was met.' <<<"$pilot_text" \
  || fail "pilot does not bound unmeasured outcomes"
grep -Fq 'recorded in AD-044' <<<"$pilot_text" \
  || fail "pilot changed workflow without a recorded decision"
ok "pilot has a completed closing review and decision boundary"

if grep -Eq '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|\.jsonl|~/\.codex|~/\.claude|/root/lucas' "$pilot"; then
  fail "pilot leaks session identity or transcript locations"
fi
ok "pilot persists no session identity or transcript location"

echo
echo "$passed teste(s) passaram."
