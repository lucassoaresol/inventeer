#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT_DIR/.agents/vendor.json"
SKILL="tlc-spec-driven"
MODE="${1:---check}"
REQUESTED_REF="${2:-main}"

usage() {
  echo "Uso: $0 [--check|--merge|--accept] [ref]" >&2
  exit 2
}

[[ "$MODE" == "--check" || "$MODE" == "--merge" || "$MODE" == "--accept" ]] || usage

for command in git curl tar rsync jq patch; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "Erro: comando obrigatório não encontrado: $command" >&2
    exit 2
  }
done

repository="$(jq -er --arg skill "$SKILL" '.[$skill].repository' "$MANIFEST")"
source_path="$(jq -er --arg skill "$SKILL" '.[$skill].source_path' "$MANIFEST")"
target_rel="$(jq -er --arg skill "$SKILL" '.[$skill].target_path' "$MANIFEST")"
base_ref="$(jq -er --arg skill "$SKILL" '.[$skill].base_ref' "$MANIFEST")"
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

update_manifest() {
  local ref="$1"
  local version="$2"
  local manifest_tmp="$3"

  jq --arg skill "$SKILL" \
    --arg ref "$ref" \
    --arg version "$version" \
    --arg synced_at "$(date +%F)" \
    '.[$skill].base_ref = $ref | .[$skill].upstream_version = $version | .[$skill].merged_at = $synced_at' \
    "$MANIFEST" > "$manifest_tmp"
  mv "$manifest_tmp" "$MANIFEST"
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

target_ref="$(resolve_ref "$REQUESTED_REF")"
base_dir="$(download_skill "$base_ref" "$tmp_dir/base-download")"
incoming_dir="$(download_skill "$target_ref" "$tmp_dir/incoming-download")"
incoming_version="$(awk '/^  version: / {print $2; exit}' "$incoming_dir/SKILL.md")"

echo "Base upstream: $base_ref"
echo "Incoming:      $target_ref (versão $incoming_version)"

if diff -qr "$base_dir" "$target_dir" >/dev/null; then
  echo "Customizações locais: nenhuma"
else
  echo "Customizações locais:"
  diff -qr "$base_dir" "$target_dir" || true
fi

if diff -qr "$base_dir" "$incoming_dir" >/dev/null; then
  echo "Atualizações upstream: nenhuma"
  exit 0
fi

echo "Atualizações upstream disponíveis:"
diff -qr "$base_dir" "$incoming_dir" || true

if [[ "$MODE" == "--check" ]]; then
  echo "Nenhum arquivo foi alterado. Use --merge após revisar os dois lados."
  exit 1
fi

if [[ "$MODE" == "--accept" ]]; then
  if grep -R -n -E '^(<<<<<<<|=======|>>>>>>>)' "$target_dir" >/dev/null; then
    echo "Erro: ainda existem marcadores de conflito no fork local." >&2
    exit 2
  fi
  update_manifest "$target_ref" "$incoming_version" "$tmp_dir/vendor.json"
  echo "[ACEITO] $SKILL agora usa $target_ref como nova base upstream."
  exit 0
fi

if [[ -n "$(git -C "$ROOT_DIR" status --porcelain)" ]]; then
  echo "Erro: --merge exige o worktree limpo." >&2
  exit 2
fi

merge_dir="$tmp_dir/merge"
mkdir -p "$merge_dir/base" "$merge_dir/local"
rsync -a "$base_dir/" "$merge_dir/base/"
rsync -a "$target_dir/" "$merge_dir/local/"
(
  cd "$merge_dir"
  diff -ruN base local > local-customizations.patch || [[ $? -eq 1 ]]
)

rsync -a --delete "$incoming_dir/" "$target_dir/"

if [[ -s "$merge_dir/local-customizations.patch" ]]; then
  if ! patch --directory="$target_dir" -p1 --merge --forward < "$merge_dir/local-customizations.patch"; then
    echo "[CONFLITO] O upstream foi aplicado, mas algumas personalizações exigem merge manual." >&2
    echo "Resolva os marcadores no worktree e execute: $0 --accept $target_ref" >&2
    exit 1
  fi
fi

update_manifest "$target_ref" "$incoming_version" "$tmp_dir/vendor.json"
echo "[MESCLADO] $SKILL -> base $target_ref com personalizações locais reaplicadas."
echo "Revise e valide o diff; o script não cria commits."
