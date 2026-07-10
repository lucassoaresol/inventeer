#!/usr/bin/env bash

set -u

ROOT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/repos}"

updated=0
skipped=0
failed=0

if [[ ! -d "$ROOT_DIR" ]]; then
  echo "Erro: diretório de repositórios não encontrado: $ROOT_DIR" >&2
  exit 2
fi

for repo in "$ROOT_DIR"/*; do
  [[ -d "$repo" ]] || continue

  name="$(basename "$repo")"
  if [[ "$name" == "inventeer-hub" ]]; then
    echo "[PULADO] $name: atualizações indisponíveis enquanto as políticas de acesso são definidas"
    ((skipped += 1))
    continue
  fi

  if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[PULADO] $name: não é um repositório Git"
    ((skipped += 1))
    continue
  fi

  echo "[ATUALIZANDO] $name"

  if ! git -C "$repo" remote get-url origin >/dev/null 2>&1; then
    echo "[PULADO] $name: remote 'origin' não encontrado"
    ((skipped += 1))
    continue
  fi

  if ! git -C "$repo" fetch origin --prune; then
    echo "[ERRO] $name: falha no fetch" >&2
    ((failed += 1))
    continue
  fi

  current_branch="$(git -C "$repo" branch --show-current)"
  if [[ -n "$(git -C "$repo" status --porcelain)" ]]; then
    echo "[PULADO] $name: há alterações locais"
    ((skipped += 1))
    continue
  fi

  if git -C "$repo" show-ref --verify --quiet refs/heads/develop; then
    branch="develop"
  else
    default_ref="$(git -C "$repo" symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)"
    branch="${default_ref#refs/remotes/origin/}"
    if [[ -z "$default_ref" || "$branch" == "$default_ref" ]]; then
      if git -C "$repo" show-ref --verify --quiet refs/remotes/origin/main; then
        branch="main"
      elif git -C "$repo" show-ref --verify --quiet refs/remotes/origin/develop; then
        branch="develop"
      else
        echo "[PULADO] $name: branch padrão não detectada (main/develop ausentes)"
        ((skipped += 1))
        continue
      fi
    fi
  fi

  if ! git -C "$repo" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
    echo "[PULADO] $name: 'origin/$branch' não existe"
    ((skipped += 1))
    continue
  fi

  if [[ "$current_branch" != "$branch" ]]; then
    echo "[TROCANDO] $name: '${current_branch:-HEAD destacado}' -> '$branch'"
    if ! git -C "$repo" switch "$branch"; then
      echo "[ERRO] $name: não foi possível trocar para '$branch'" >&2
      ((failed += 1))
      continue
    fi
  fi

  if git -C "$repo" merge --ff-only "origin/$branch"; then
    echo "[OK] $name ($branch)"
    ((updated += 1))
  else
    echo "[ERRO] $name: '$branch' divergiu de 'origin/$branch'" >&2
    ((failed += 1))
  fi
done

echo
echo "Resumo: $updated atualizado(s), $skipped pulado(s), $failed erro(s)."

((failed == 0))
