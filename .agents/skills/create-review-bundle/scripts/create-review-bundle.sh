#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: create-review-bundle.sh --repo PATH [options]

Options:
  --repo PATH        Git repository to review (required)
  --base REF         Compare REF to the current worktree (default: HEAD)
  --output-dir PATH  Destination directory (default: workspace/session-context)
  --label TEXT       Short filename label (default: repository name)
  -h, --help         Show this help
EOF
}

is_sensitive_path() {
  local path="$1"
  local name

  name="$(basename "$path")"
  case "$name" in
    .env.example | .env.sample | .env.template)
      return 1
      ;;
    .env | .env.* | *.pem | *.key | *.p12 | *.pfx | id_rsa | id_ed25519 | credentials.json | secrets.json | *.dump)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

repo=""
base_ref="HEAD"
output_dir=""
label=""

while (($# > 0)); do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || { echo "Erro: --repo exige um valor" >&2; exit 2; }
      repo="$2"
      shift 2
      ;;
    --base)
      [[ $# -ge 2 ]] || { echo "Erro: --base exige um valor" >&2; exit 2; }
      base_ref="$2"
      shift 2
      ;;
    --output-dir)
      [[ $# -ge 2 ]] || { echo "Erro: --output-dir exige um valor" >&2; exit 2; }
      output_dir="$2"
      shift 2
      ;;
    --label)
      [[ $# -ge 2 ]] || { echo "Erro: --label exige um valor" >&2; exit 2; }
      label="$2"
      shift 2
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Erro: argumento desconhecido: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$repo" ]] || { echo "Erro: --repo é obrigatório" >&2; exit 2; }
repo="$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Erro: repositório Git inválido: $repo" >&2
  exit 2
}

base_sha="$(git -C "$repo" rev-parse --verify "${base_ref}^{commit}" 2>/dev/null)" || {
  echo "Erro: base Git inválida: $base_ref" >&2
  exit 2
}
head_sha="$(git -C "$repo" rev-parse HEAD)"
branch="$(git -C "$repo" branch --show-current)"
branch="${branch:-detached-HEAD}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace_root="$(cd "$script_dir/../../../.." && pwd)"
output_dir="${output_dir:-$workspace_root/session-context}"
output_dir="$(realpath -m "$output_dir")"

if [[ "$output_dir" == "$repo" ]]; then
  echo "Erro: output-dir não pode ser a raiz do repositório analisado" >&2
  exit 4
fi
if [[ "$output_dir" == "$repo/"* ]]; then
  relative_output="${output_dir#"$repo/"}"
  ignore_probe="$relative_output/.review-bundle-probe"
  if ! git -C "$repo" check-ignore --quiet --no-index -- "$ignore_probe"; then
    echo "Erro: output-dir dentro do repositório precisa estar ignorado pelo Git: $relative_output" >&2
    exit 4
  fi
fi

mkdir -p "$output_dir"
output_dir="$(cd "$output_dir" && pwd)"

label="${label:-$(basename "$repo")}"
safe_label="$(printf '%s' "$label" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')"
[[ -n "$safe_label" ]] || { echo "Erro: label não produz um nome seguro" >&2; exit 2; }

declare -A change_kind=()
while IFS= read -r -d '' path; do
  change_kind["$path"]="tracked"
done < <(git -C "$repo" diff --name-only -z --diff-filter=ACDMRTUXB "$base_sha" --)
while IFS= read -r -d '' path; do
  [[ -n "${change_kind[$path]:-}" ]] || change_kind["$path"]="untracked"
done < <(git -C "$repo" ls-files --others --exclude-standard -z)

((${#change_kind[@]} > 0)) || {
  echo "Erro: nenhuma alteração encontrada em relação a $base_ref" >&2
  exit 3
}

mapfile -d '' changed_paths < <(printf '%s\0' "${!change_kind[@]}" | sort -z)
for path in "${changed_paths[@]}"; do
  if is_sensitive_path "$path"; then
    echo "Erro: caminho potencialmente sensível não pode entrar no bundle: $path" >&2
    exit 4
  fi
done

timestamp="$(date +%Y%m%d-%H%M%S%z)"
bundle_name="${safe_label}-review-${timestamp}"
tmp_dir="$(mktemp -d /tmp/create-review-bundle.XXXXXX)"
trap 'rm -rf "$tmp_dir"' EXIT
bundle_dir="$tmp_dir/$bundle_name"
mkdir -p "$bundle_dir/diffs"

git -C "$repo" status --short --branch >"$bundle_dir/status.txt"
git -C "$repo" log --oneline --decorate "$base_sha..HEAD" >"$bundle_dir/commits.txt"

printf 'kind\tpath\tdiff\n' >"$bundle_dir/files.tsv"
counter=0
for path in "${changed_paths[@]}"; do
  ((counter += 1))
  safe_path="$(printf '%s' "$path" | sed -E 's#[/[:space:]]+#-#g; s#[^A-Za-z0-9._-]+#-#g')"
  diff_name="$(printf '%03d-%s.diff' "$counter" "$safe_path")"
  diff_path="$bundle_dir/diffs/$diff_name"

  if [[ "${change_kind[$path]}" == "tracked" ]]; then
    git -C "$repo" diff --no-ext-diff --no-color "$base_sha" -- "$path" >"$diff_path"
  else
    set +e
    (cd "$repo" && git diff --no-index --no-ext-diff --no-color -- /dev/null "$path") >"$diff_path"
    diff_exit=$?
    set -e
    if [[ $diff_exit -ne 0 && $diff_exit -ne 1 ]]; then
      echo "Erro: falha ao gerar diff para $path" >&2
      exit 5
    fi
  fi

  printf '%s\t%s\t%s\n' "${change_kind[$path]}" "$path" "diffs/$diff_name" >>"$bundle_dir/files.tsv"
done

set +e
git -C "$repo" diff --check "$base_sha" -- >"$bundle_dir/diff-check.txt" 2>&1
diff_check_exit=$?
set -e
printf '\nexit_code=%s\n' "$diff_check_exit" >>"$bundle_dir/diff-check.txt"

cat >"$bundle_dir/commands.txt" <<EOF
git status --short --branch
git rev-parse HEAD
git rev-parse ${base_ref}^{commit}
git log --oneline --decorate ${base_sha}..HEAD
git diff --name-only ${base_sha}
git diff --check ${base_sha}
git diff ${base_sha} -- <path>
git ls-files --others --exclude-standard
git diff --no-index /dev/null <untracked-path>
EOF

cat >"$bundle_dir/README.md" <<EOF
# Git Review Bundle

- Generated: $timestamp
- Repository: $repo
- Branch: $branch
- Base ref: $base_ref
- Base SHA: $base_sha
- HEAD SHA: $head_sha
- Changed files: ${#changed_paths[@]}
- Diff check exit: $diff_check_exit

This bundle is review evidence only. It does not assert that tests passed or that the change is
approved. Paths classified as likely credentials, private keys, or dumps are rejected before archive
creation.
EOF

zip_path="$output_dir/$bundle_name.zip"
(cd "$tmp_dir" && zip -qr "$zip_path" "$bundle_name")
(
  cd "$output_dir"
  sha256sum "$(basename "$zip_path")" >"$(basename "$zip_path").sha256"
)

printf 'Bundle: %s\n' "$zip_path"
printf 'Checksum: %s.sha256\n' "$zip_path"
printf 'Changed files: %s\n' "${#changed_paths[@]}"
printf 'Base: %s (%s)\n' "$base_ref" "$base_sha"
