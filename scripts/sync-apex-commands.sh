#!/usr/bin/env bash

# Mantém um único inspector experimental APEX em .agents/skills/apex-all-tools/ para o Codex.
#
# O Claude Code recebe os mesmos workflows nativamente, como prompts MCP do servidor apex; o Codex
# CLI consome apenas tools e resources, então os wrappers preservam descoberta e diagnóstico em
# arquivo, mas não constituem execução suportada do workflow. Por isso eles não são expostos em
# .claude/skills/: lá apenas duplicariam comandos nativos já existentes.
#
# O inspector não copia o corpo dos workflows. Ele aponta para
# apex://framework/workflows/all-tools, mantendo o APEX como fonte canônica e evitando que um
# wrapper por workflow domine a descoberta de skills.
#
# Este script não fala MCP. O catálogo é obtido pelo agente e entregue como JSON; ver
# --print-contract para o contrato de aquisição.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$ROOT_DIR/.agents/skills"
PREFIX="apex-"
RESOURCE_BASE="apex://framework/workflows"

MODE=""
CATALOG=""
PRUNE_ORPHANS=""

usage() {
  cat >&2 <<'EOF'
Uso: sync-apex-commands.sh --check  --catalog <arquivo.json> [--skills-dir <dir>]
     sync-apex-commands.sh --apply  --catalog <arquivo.json> [--skills-dir <dir>]
     sync-apex-commands.sh --check|--apply --prune-orphans [--skills-dir <dir>]
     sync-apex-commands.sh --print-contract

  --check          Relata criações, atualizações e remoções sem escrever. Sai 1 se houver divergência.
  --apply          Reconcilia os wrappers no disco. Não cria commits.
  --prune-orphans  Remove apenas diretórios apex-* sem SKILL.md. Não aceita --catalog: nenhum
                   catálogo válido produz um wrapper sem manifesto, então o órfão é indesejado
                   independentemente do catálogo. Use quando o MCP não estiver disponível.
  --skills-dir     Diretório alvo dos wrappers. Padrão: .agents/skills. Use apenas em testes.
EOF
  exit 2
}

print_contract() {
  cat <<EOF
Contrato de aquisição do catálogo
=================================

O catálogo vem da tool MCP apex_framework_index, disponível de forma idêntica no Claude Code e no
Codex. Não use resources/read direto, arquivos de credencial nem chamadas HTTP ao gateway: o campo
config.command de apex://framework/runtime não é visível de forma igual nos dois clientes, e ler
credenciais do host não é reproduzível.

Passos para o agente:

1. Chamar apex_framework_index.
2. Emitir o array .workflows como JSON no formato abaixo.
3. Executar este script apontando para o arquivo gerado.

Formato:

{
  "source": "apex_framework_index",
  "fetched_at": "YYYY-MM-DD",
  "workflows": [
    { "id": "eng-start", "description": "Initiates planning for a task by creating the architecture.md" }
  ]
}

Campos opcionais por entrada, aplicados quando presentes:

  "bytes":          tamanho do recurso; 0 rejeita a entrada
  "frontmatter_ok": false rejeita a entrada

Filtros aplicados pelo script:

  - id fora de ^[a-z0-9][a-z0-9-]*\$        -> rejeitado
  - description ausente ou vazia            -> rejeitado (remove sentinelas como README)
  - id diferente de all-tools               -> ignorado; não gera skill
  - description contendo DEPRECATED         -> rejeitado
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check|--apply)
      [[ -z "$MODE" ]] || usage
      MODE="${1#--}"
      shift
      ;;
    --catalog)
      [[ $# -ge 2 ]] || usage
      CATALOG="$2"
      shift 2
      ;;
    --skills-dir)
      [[ $# -ge 2 ]] || usage
      SKILLS_DIR="$2"
      shift 2
      ;;
    --prune-orphans)
      [[ -z "$PRUNE_ORPHANS" ]] || usage
      PRUNE_ORPHANS=1
      shift
      ;;
    --print-contract)
      print_contract
      ;;
    *)
      usage
      ;;
  esac
done

[[ -n "$MODE" ]] || usage

# Reconciliação de órfãos: independente do catálogo, porque nenhum catálogo válido pode produzir um
# diretório apex-* sem SKILL.md. Um wrapper sem manifesto não é descoberto como skill por nenhuma
# engine, então só resta como resíduo de uma consolidação anterior.
if [[ -n "$PRUNE_ORPHANS" ]]; then
  [[ -z "$CATALOG" ]] || usage

  [[ -d "$SKILLS_DIR" ]] || {
    echo "Erro: diretório de skills não encontrado: $SKILLS_DIR" >&2
    exit 2
  }

  declare -a orphans=()
  for dir in "$SKILLS_DIR/$PREFIX"*/; do
    [[ -d "$dir" ]] || continue
    [[ -f "$dir/SKILL.md" ]] && continue
    orphans+=("$(basename "$dir")")
  done

  echo "Diretório: $SKILLS_DIR"
  echo "Modo:      prune-orphans"
  echo

  if ((${#orphans[@]} == 0)); then
    echo "Nenhum diretório órfão; nada a fazer."
    exit 0
  fi

  printf '[ORFAO] (%d):\n' "${#orphans[@]}"
  printf '  %s\n' "${orphans[@]}"

  if [[ "$MODE" == "check" ]]; then
    echo
    echo "Nenhum arquivo foi alterado. Execute --apply após revisar."
    exit 1
  fi

  for name in "${orphans[@]}"; do
    rm -rf "${SKILLS_DIR:?}/$name"
  done

  echo
  echo "[REMOVIDO] ${#orphans[@]} diretório(s) órfão(s). O script não cria commits."
  exit 0
fi

[[ -n "$CATALOG" ]] || usage

command -v jq >/dev/null 2>&1 || {
  echo "Erro: comando obrigatório não encontrado: jq" >&2
  exit 2
}

[[ -f "$CATALOG" ]] || {
  echo "Erro: catálogo não encontrado: $CATALOG" >&2
  exit 2
}

jq -e 'has("workflows") and (.workflows | type == "array") and (.workflows | length > 0)' \
  "$CATALOG" >/dev/null || {
  echo "Erro: catálogo inválido; esperado objeto com .workflows não vazio." >&2
  echo "Use --print-contract para ver o formato." >&2
  exit 2
}

# Aplica os filtros e emite "id<TAB>description" para as entradas aceitas.
selected="$(jq -r '
  .workflows[]
  | select(.id | type == "string")
  | select(.id | test("^[a-z0-9][a-z0-9-]*$"))
  | select((.description // "") | length > 0)
  | select((.description | ascii_upcase | contains("DEPRECATED")) | not)
  | select((has("bytes") | not) or (.bytes > 0))
  | select((has("frontmatter_ok") | not) or (.frontmatter_ok == true))
  | select(.id == "all-tools")
  | [.id, .description]
  | @tsv
' "$CATALOG")"

[[ -n "$selected" ]] || {
  echo "Erro: o catálogo não contém o workflow válido all-tools." >&2
  exit 2
}

rejected="$(jq -r '
  .workflows[]
  | select(
      ((.id | type) != "string")
      or ((.id | test("^[a-z0-9][a-z0-9-]*$")) | not)
      or (((.description // "") | length) == 0)
      or (.description | ascii_upcase | contains("DEPRECATED"))
      or ((has("bytes")) and (.bytes == 0))
      or ((has("frontmatter_ok")) and (.frontmatter_ok == false))
    )
  | .id // "(sem id)"
' "$CATALOG")"

ignored="$(jq -r '
  .workflows[]
  | select(.id | type == "string")
  | select(.id | test("^[a-z0-9][a-z0-9-]*$"))
  | select((.description // "") | length > 0)
  | select((.description | ascii_upcase | contains("DEPRECATED")) | not)
  | select((has("bytes") | not) or (.bytes > 0))
  | select((has("frontmatter_ok") | not) or (.frontmatter_ok == true))
  | select(.id != "all-tools")
  | .id
' "$CATALOG")"

render_wrapper() {
  local id="$1"
  local description="$2"
  local summary

  summary="$(printf 'APEX · %s Wrapper experimental: inspeciona %s/%s no Codex; não use como executor de entrega.' \
    "$description" "$RESOURCE_BASE" "$id" | jq -Rs .)"

  cat <<EOF
---
name: $PREFIX$id
description: $summary
---

# APEX · $id

$description

Arquivo gerado por \`scripts/sync-apex-commands.sh\` a partir de \`apex_framework_index\`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP \`$RESOURCE_BASE/$id\` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use \`tlc-spec-driven\` como executor.
EOF
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

declare -a to_create=() to_update=() to_remove=()
declare -A wanted=()

while IFS=$'\t' read -r id description; do
  [[ -n "$id" ]] || continue
  wanted["$id"]=1
  target="$SKILLS_DIR/$PREFIX$id/SKILL.md"
  render_wrapper "$id" "$description" > "$tmp_dir/$PREFIX$id.md"

  if [[ ! -f "$target" ]]; then
    to_create+=("$id")
  elif ! cmp -s "$tmp_dir/$PREFIX$id.md" "$target"; then
    to_update+=("$id")
  fi
done <<< "$selected"

for dir in "$SKILLS_DIR/$PREFIX"*/; do
  [[ -d "$dir" ]] || continue
  name="$(basename "$dir")"
  id="${name#"$PREFIX"}"
  [[ -z "${wanted[$id]:-}" ]] || continue
  to_remove+=("$id")
done

echo "Catálogo:  $CATALOG"
echo "Aceitos:   $(wc -l <<< "$selected") workflow(s)"
if [[ -n "$rejected" ]]; then
  echo "Rejeitados: $(tr '\n' ' ' <<< "$rejected")"
fi
if [[ -n "$ignored" ]]; then
  echo "Ignorados:  $(tr '\n' ' ' <<< "$ignored")"
fi
echo

report() {
  local label="$1"
  shift
  (($# > 0)) || return 0
  printf '%s (%d):\n' "$label" "$#"
  printf '  %s\n' "$@"
}

report "[CRIAR]"     ${to_create[@]+"${to_create[@]}"}
report "[ATUALIZAR]" ${to_update[@]+"${to_update[@]}"}
report "[REMOVER]"   ${to_remove[@]+"${to_remove[@]}"}

total=$(( ${#to_create[@]} + ${#to_update[@]} + ${#to_remove[@]} ))

if ((total == 0)); then
  echo "Wrappers já sincronizados; nada a fazer."
  exit 0
fi

if [[ "$MODE" == "check" ]]; then
  echo
  echo "Nenhum arquivo foi alterado. Execute --apply após revisar."
  exit 1
fi

for id in ${to_create[@]+"${to_create[@]}"} ${to_update[@]+"${to_update[@]}"}; do
  mkdir -p "$SKILLS_DIR/$PREFIX$id"
  mv "$tmp_dir/$PREFIX$id.md" "$SKILLS_DIR/$PREFIX$id/SKILL.md"
done

for id in ${to_remove[@]+"${to_remove[@]}"}; do
  rm -rf "${SKILLS_DIR:?}/$PREFIX$id"
done

echo
echo "[SINCRONIZADO] $total alteração(ões) aplicada(s). O script não cria commits."
