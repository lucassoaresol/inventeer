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
    { "id": "all-tools", "description": "Summary of all workflows and tools" },
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
grep -q 'Aceitos:   1 workflow' <<<"$output" || fail "expected 1 accepted, got: $output"
ok "somente all-tools sobrevive como inspector agregado"

grep -q 'Rejeitados: README warm-up' <<<"$output" || fail "rejected list wrong: $output"
grep -q 'Ignorados:  eng-start eng-work init-apex' <<<"$output" || fail "ignored list wrong: $output"
ok "entradas rejeitadas sao relatadas por id"

[[ -z "$(ls -A "$skills")" ]] || fail "--check wrote to disk"
ok "--check nao escreve no disco"

# --- Criação -----------------------------------------------------------------

run --apply --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--apply failed: $output"
[[ -f "$skills/apex-all-tools/SKILL.md" ]] || fail "aggregate inspector not created"
for id in eng-start eng-work init-apex; do
  [[ ! -e "$skills/apex-$id" ]] || fail "per-workflow wrapper apex-$id was created"
done
[[ ! -e "$skills/apex-README" ]] || fail "README wrapper was created"
[[ ! -e "$skills/apex-warm-up" ]] || fail "deprecated wrapper was created"
ok "--apply cria somente o inspector agregado"

grep -q 'apex://framework/workflows/all-tools' "$skills/apex-all-tools/SKILL.md" \
  || fail "wrapper does not reference its MCP resource"
ok "wrapper aponta para o recurso MCP em vez de copiar o corpo"

grep -q 'não use como executor de entrega' "$skills/apex-all-tools/SKILL.md" \
  || fail "wrapper claims or implies supported APEX execution"
# shellcheck disable=SC2016 # Backticks are literal Markdown in the generated wrapper.
grep -Fq 'Use `tlc-spec-driven` como executor' "$skills/apex-all-tools/SKILL.md" \
  || fail "wrapper omits the Codex execution fallback"
ok "wrapper declara o limite experimental e roteia entrega Codex para TLC"

grep -qE '^name: apex-all-tools$' "$skills/apex-all-tools/SKILL.md" \
  || fail "wrapper frontmatter name wrong"
ok "frontmatter usa o nome prefixado"

# --- Idempotência ------------------------------------------------------------

run --check --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--check should exit 0 when synced: $output"
grep -q 'já sincronizados' <<<"$output" || fail "expected no-op report, got: $output"
ok "segunda execucao e no-op e sai 0"

# --- Atualização -------------------------------------------------------------

printf 'drift\n' >>"$skills/apex-all-tools/SKILL.md"
if run --check --catalog "$fixture_dir/full.json" --skills-dir "$skills"; then
  fail "--check should exit 1 after manual drift"
fi
grep -q '\[ATUALIZAR\] (1)' <<<"$output" || fail "drift not detected: $output"
run --apply --catalog "$fixture_dir/full.json" --skills-dir "$skills" \
  || fail "--apply failed: $output"
grep -q 'drift' "$skills/apex-all-tools/SKILL.md" && fail "manual drift survived --apply"
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
    { "id": "all-tools", "description": "ok" },
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
[[ -f "$guarded/apex-all-tools/SKILL.md" ]] || fail "valid entry rejected"
for id in eng-vazio eng-quebrado Eng_Invalido; do
  [[ ! -e "$guarded/apex-$id" ]] || fail "entry $id should have been rejected"
done
ok "bytes=0, frontmatter_ok=false e id malformado sao rejeitados"

# --- Falhas ------------------------------------------------------------------

# Sai 2 para qualquer uso inválido; usado pelas seções de órfãos e de falhas.
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

printf '{"workflows":[{"id":"eng-start","description":"valid but not aggregate"}]}' \
  >"$fixture_dir/sem-all-tools.json"
assert_exit_2 "catalogo sem all-tools" --check --catalog "$fixture_dir/sem-all-tools.json" \
  --skills-dir "$fixture_dir/sem-inspector"
[[ ! -e "$fixture_dir/sem-inspector" ]] || fail "missing all-tools still created the skills dir"
ok "ausencia de all-tools falha fechada"

# --- Órfãos sem catálogo -----------------------------------------------------

# O resíduo de uma consolidação anterior é um diretório apex-* sem SKILL.md. Ele não é descoberto
# como skill, o Git não versiona diretório vazio e o validador estrutural do gate agregado só
# percorre diretórios que já têm SKILL.md — então nenhuma superfície existente o alcança.

orphans="$fixture_dir/orfaos"
mkdir -p "$orphans/apex-vazio" "$orphans/apex-sem-manifesto" "$orphans/apex-valido" \
  "$orphans/nao-apex" "$orphans/apex-com-subdir/nested"
printf 'residuo\n' >"$orphans/apex-sem-manifesto/README.md"
printf 'manter\n' >"$orphans/apex-valido/SKILL.md"
printf 'manter\n' >"$orphans/nao-apex/SKILL.md"
printf 'arquivo\n' >"$orphans/apex-arquivo-regular"

if run --check --prune-orphans --skills-dir "$orphans"; then
  fail "--check --prune-orphans should exit 1 while orphans exist"
fi
grep -q '\[ORFAO\] (3)' <<<"$output" || fail "expected 3 orphans listed, got: $output"
for name in apex-vazio apex-sem-manifesto apex-com-subdir; do
  grep -q "  $name" <<<"$output" || fail "orphan $name not listed: $output"
  [[ -d "$orphans/$name" ]] || fail "--check removed $name; it must write nothing"
done
ok "--check --prune-orphans lista cada orfao, nao escreve e sai 1"

run --apply --prune-orphans --skills-dir "$orphans" || fail "--apply --prune-orphans failed: $output"
[[ ! -e "$orphans/apex-vazio" ]] || fail "empty orphan survived"
[[ ! -e "$orphans/apex-sem-manifesto" ]] || fail "orphan holding files survived"
[[ ! -e "$orphans/apex-com-subdir" ]] || fail "orphan holding a subdirectory survived"
ok "--apply --prune-orphans remove diretorio vazio, com arquivos e com subdiretorio"

[[ -f "$orphans/apex-valido/SKILL.md" ]] || fail "wrapper with SKILL.md was deleted"
[[ -f "$orphans/nao-apex/SKILL.md" ]] || fail "non-apex directory was deleted"
[[ -f "$orphans/apex-arquivo-regular" ]] || fail "regular file named apex-* was deleted"
ok "wrapper com manifesto, diretorio sem prefixo e arquivo regular sobrevivem"

run --check --prune-orphans --skills-dir "$orphans" \
  || fail "--check --prune-orphans should exit 0 when clean: $output"
grep -q 'Nenhum diretório órfão' <<<"$output" || fail "clean report wrong: $output"
ok "arvore limpa reporta estado limpo e sai 0"

# A poda nunca depende do catálogo: exigir um acoplaria a limpeza à disponibilidade do MCP, que é
# exatamente a razão pela qual os órfãos sobreviveram.
assert_exit_2 "--prune-orphans com --catalog" --check --prune-orphans \
  --catalog "$fixture_dir/full.json" --skills-dir "$orphans"
assert_exit_2 "--prune-orphans sem modo" --prune-orphans --skills-dir "$orphans"
assert_exit_2 "--prune-orphans repetido" --check --prune-orphans --prune-orphans \
  --skills-dir "$orphans"
assert_exit_2 "--prune-orphans com diretorio inexistente" --check --prune-orphans \
  --skills-dir "$orphans/nao-existe"
[[ ! -e "$orphans/nao-existe" ]] || fail "missing skills dir was created"
ok "prune-orphans rejeita catalogo, modo ausente, flag repetida e diretorio inexistente"

# --- Contrato ----------------------------------------------------------------

run --print-contract || fail "--print-contract failed"
grep -q 'apex_framework_index' <<<"$output" || fail "contract omits the acquisition tool"
grep -q 'credenciais' <<<"$output" || fail "contract omits the credential prohibition"
ok "--print-contract documenta a aquisicao e as rotas proibidas"

echo
echo "$passed teste(s) passaram."
