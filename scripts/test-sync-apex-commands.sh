#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
subject="$script_dir/sync-apex-commands.sh"
fixture_dir="$(mktemp -d /tmp/test-sync-apex-commands.XXXXXX)"
trap 'rm -rf "$fixture_dir"' EXIT

passed=0

fail() {
  echo "not ok - $*" >&2
  exit 1
}

ok() {
  passed=$((passed + 1))
  echo "ok $passed - $*"
}

# Executa o subject e captura status sem abortar o teste.
run() {
  local status=0
  output="$("$subject" "$@" 2>&1)" || status=$?
  return "$status"
}

catalog() {
  cat >"$fixture_dir/$1"
}

catalog full.json <<'EOF'
{
  "source": "apex_framework_index",
  "fetched_at": "2026-07-26",
  "workflows": [
    { "id": "README" },
    { "id": "eng-start", "description": "Initiates planning for a task" },
    { "id": "eng-work", "description": "Workflow for code implementation" },
    { "id": "init-apex", "description": "Initialize APEX in any repository" },
    { "id": "warm-up", "description": "DEPRECATED (ADR 0032) — manual session context refresh" }
  ]
}
EOF

skills="$fixture_dir/skills"
mkdir -p "$skills"

# --- Seleção -----------------------------------------------------------------

if run --check --catalog "$fixture_dir/full.json" --skills-dir "$skills"; then
  fail "--check should exit 1 when wrappers are missing"
fi
grep -q 'Aceitos:   3 workflow' <<<"$output" || fail "expected 3 accepted, got: $output"
ok "README sem description e warm-up depreciado sao rejeitados"

grep -q 'Rejeitados: README warm-up' <<<"$output" || fail "rejected list wrong: $output"
ok "entradas rejeitadas sao relatadas por id"

[[ -z "$(ls -A "$skills")" ]] || fail "--check wrote to disk"
ok "--check nao escreve no disco"

# --- Criação -----------------------------------------------------------------

run --apply --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--apply failed: $output"
for id in eng-start eng-work init-apex; do
  [[ -f "$skills/apex-$id/SKILL.md" ]] || fail "wrapper apex-$id not created"
done
[[ ! -e "$skills/apex-README" ]] || fail "README wrapper was created"
[[ ! -e "$skills/apex-warm-up" ]] || fail "deprecated wrapper was created"
ok "--apply cria um wrapper por workflow aceito"

grep -q 'apex://framework/workflows/eng-start' "$skills/apex-eng-start/SKILL.md" \
  || fail "wrapper does not reference its MCP resource"
ok "wrapper aponta para o recurso MCP em vez de copiar o corpo"

grep -qE '^name: apex-eng-start$' "$skills/apex-eng-start/SKILL.md" \
  || fail "wrapper frontmatter name wrong"
ok "frontmatter usa o nome prefixado"

# --- Idempotência ------------------------------------------------------------

run --check --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--check should exit 0 when synced: $output"
grep -q 'já sincronizados' <<<"$output" || fail "expected no-op report, got: $output"
ok "segunda execucao e no-op e sai 0"

# --- Atualização -------------------------------------------------------------

printf 'drift\n' >>"$skills/apex-eng-work/SKILL.md"
if run --check --catalog "$fixture_dir/full.json" --skills-dir "$skills"; then
  fail "--check should exit 1 after manual drift"
fi
grep -q '\[ATUALIZAR\] (1)' <<<"$output" || fail "drift not detected: $output"
run --apply --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--apply failed: $output"
grep -q 'drift' "$skills/apex-eng-work/SKILL.md" && fail "manual drift survived --apply"
ok "edicao manual e sobrescrita pelo sync"

# --- Remoção -----------------------------------------------------------------

mkdir -p "$skills/apex-obsoleto"
printf 'orfao\n' >"$skills/apex-obsoleto/SKILL.md"
run --apply --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--apply failed: $output"
[[ ! -e "$skills/apex-obsoleto" ]] || fail "orphan wrapper survived"
ok "wrapper fora do catalogo e removido"

mkdir -p "$skills/nao-apex"
printf 'preservar\n' >"$skills/nao-apex/SKILL.md"
run --apply --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--apply failed: $output"
[[ -f "$skills/nao-apex/SKILL.md" ]] || fail "non-apex skill was deleted"
ok "skills sem o prefixo apex- nao sao tocadas"

# --- Validações opcionais por entrada ----------------------------------------

catalog guarded.json <<'EOF'
{
  "workflows": [
    { "id": "eng-start", "description": "ok" },
    { "id": "eng-vazio", "description": "recurso vazio", "bytes": 0 },
    { "id": "eng-quebrado", "description": "frontmatter ruim", "frontmatter_ok": false },
    { "id": "Eng_Invalido", "description": "id fora do padrao" }
  ]
}
EOF

guarded="$fixture_dir/guarded"
mkdir -p "$guarded"
run --apply --catalog "$fixture_dir/guarded.json" --skills-dir "$guarded" \
  || fail "--apply failed: $output"
[[ -f "$guarded/apex-eng-start/SKILL.md" ]] || fail "valid entry rejected"
for id in eng-vazio eng-quebrado Eng_Invalido; do
  [[ ! -e "$guarded/apex-$id" ]] || fail "entry $id should have been rejected"
done
ok "bytes=0, frontmatter_ok=false e id malformado sao rejeitados"

# --- Falhas ------------------------------------------------------------------

assert_exit_2() {
  local label="$1"
  shift
  local status=0
  "$subject" "$@" >/dev/null 2>&1 || status=$?
  [[ "$status" -eq 2 ]] || fail "$label exited with $status instead of 2"
}

assert_exit_2 "sem argumentos"
assert_exit_2 "catalogo ausente" --check --catalog "$fixture_dir/inexistente.json"
assert_exit_2 "--catalog sem valor" --check --catalog
ok "usos invalidos saem 2"

printf '{"workflows":[]}' >"$fixture_dir/vazio.json"
assert_exit_2 "catalogo sem workflows" --check --catalog "$fixture_dir/vazio.json"
printf 'nao e json' >"$fixture_dir/lixo.json"
assert_exit_2 "catalogo nao-json" --check --catalog "$fixture_dir/lixo.json"
printf '{"workflows":[{"id":"README"}]}' >"$fixture_dir/so-readme.json"
assert_exit_2 "todas as entradas filtradas" --check --catalog "$fixture_dir/so-readme.json" \
  --skills-dir "$fixture_dir/nunca"
[[ ! -e "$fixture_dir/nunca" ]] || fail "rejected catalog still created the skills dir"
ok "catalogo invalido ou totalmente filtrado sai 2 sem escrever"

# --- Contrato ----------------------------------------------------------------

run --print-contract || fail "--print-contract failed"
grep -q 'apex_framework_index' <<<"$output" || fail "contract omits the acquisition tool"
grep -q 'credenciais' <<<"$output" || fail "contract omits the credential prohibition"
ok "--print-contract documenta a aquisicao e as rotas proibidas"

echo
echo "$passed teste(s) passaram."
