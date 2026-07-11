#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT_DIR/.agents/vendor.json"
SKILL="tlc-spec-driven"
MODE="${1:---check}"
REQUESTED_REF="${2:-main}"

usage() {
  echo "Uso: $0 [--check|--apply] [ref]" >&2
  exit 2
}

[[ "$MODE" == "--check" || "$MODE" == "--apply" ]] || usage

for command in git curl tar rsync jq; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "Erro: comando obrigatório não encontrado: $command" >&2
    exit 2
  }
done

repository="$(jq -er --arg skill "$SKILL" '.[$skill].repository' "$MANIFEST")"
source_path="$(jq -er --arg skill "$SKILL" '.[$skill].source_path' "$MANIFEST")"
target_rel="$(jq -er --arg skill "$SKILL" '.[$skill].target_path' "$MANIFEST")"
current_ref="$(jq -er --arg skill "$SKILL" '.[$skill].ref' "$MANIFEST")"
target_dir="$ROOT_DIR/$target_rel"

resolve_ref() {
  local requested="$1"
  local resolved

  if [[ "$requested" =~ ^[0-9a-f]{40}$ ]]; then
    echo "$requested"
    return
  fi

  resolved="$(git ls-remote "$repository" "$requested" "refs/heads/$requested" "refs/tags/$requested^{}" "refs/tags/$requested" | awk 'NR == 1 {print $1}')"
  [[ -n "$resolved" ]] || {
    echo "Erro: referência upstream não encontrada: $requested" >&2
    exit 2
  }
  echo "$resolved"
}

download_skill() {
  local ref="$1"
  local destination="$2"
  local archive="$destination/upstream.tar.gz"
  local extracted="$destination/repository"

  mkdir -p "$extracted"
  curl -L --fail --silent --show-error \
    "https://github.com/tech-leads-club/agent-skills/archive/$ref.tar.gz" \
    -o "$archive"
  tar -xzf "$archive" -C "$extracted" --strip-components=1
  [[ -f "$extracted/$source_path/SKILL.md" ]] || {
    echo "Erro: pacote não encontrado no caminho esperado: $source_path" >&2
    exit 2
  }
  echo "$extracted/$source_path"
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

target_ref="$(resolve_ref "$REQUESTED_REF")"
candidate_dir="$(download_skill "$target_ref" "$tmp_dir/candidate")"
candidate_version="$(awk '/^  version: / {print $2; exit}' "$candidate_dir/SKILL.md")"

if diff -qr "$candidate_dir" "$target_dir" >/dev/null; then
  echo "[OK] $SKILL já corresponde a $target_ref (versão $candidate_version)."
  exit 0
fi

echo "[DIFERENTE] $SKILL: local não corresponde a $target_ref (versão $candidate_version)."
diff -qr "$candidate_dir" "$target_dir" || true

if [[ "$MODE" == "--check" ]]; then
  echo "Nenhum arquivo foi alterado. Revise o diff antes de executar --apply."
  exit 1
fi

if [[ -n "$(git -C "$ROOT_DIR" status --porcelain)" ]]; then
  echo "Erro: --apply exige o worktree limpo." >&2
  exit 2
fi

current_dir="$(download_skill "$current_ref" "$tmp_dir/current")"
if ! diff -qr "$current_dir" "$target_dir" >/dev/null; then
  echo "Erro: o mirror local divergiu da revisão fixada $current_ref; restaure ou classifique as diferenças antes de atualizar." >&2
  diff -qr "$current_dir" "$target_dir" || true
  exit 2
fi

rsync -a --delete "$candidate_dir/" "$target_dir/"
manifest_tmp="$tmp_dir/vendor.json"
jq --arg skill "$SKILL" \
  --arg ref "$target_ref" \
  --arg version "$candidate_version" \
  --arg synced_at "$(date +%F)" \
  '.[$skill].ref = $ref | .[$skill].version = $version | .[$skill].synced_at = $synced_at' \
  "$MANIFEST" > "$manifest_tmp"
mv "$manifest_tmp" "$MANIFEST"

echo "[ATUALIZADO] $SKILL -> $target_ref (versão $candidate_version)."
echo "Revise e valide o diff; o script não cria commits."
