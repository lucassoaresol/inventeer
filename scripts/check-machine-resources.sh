#!/usr/bin/env bash

set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for command_name in awk date df free getconf; do
  command -v "$command_name" >/dev/null 2>&1 || {
    echo "Erro: comando obrigatório não encontrado: $command_name" >&2
    exit 2
  }
done

read -r load_1m load_5m load_15m _ < /proc/loadavg
read -r memory_total memory_available < <(free -b | awk '/^Mem:/ { print $2, $7 }')
read -r swap_total swap_free < <(free -b | awk '/^Swap:/ { print $2, $4 }')
read -r filesystem_total filesystem_available < <(
  df -B1 --output=size,avail "$root_dir" | awk 'NR == 2 { print $1, $2 }'
)

printf 'captured_at_utc\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'workspace\t%s\n' "$root_dir"
printf 'online_cpus\t%s\n' "$(getconf _NPROCESSORS_ONLN)"
printf 'load_average_1m\t%s\n' "$load_1m"
printf 'load_average_5m\t%s\n' "$load_5m"
printf 'load_average_15m\t%s\n' "$load_15m"
printf 'memory_total_bytes\t%s\n' "$memory_total"
printf 'memory_available_bytes\t%s\n' "$memory_available"
printf 'swap_total_bytes\t%s\n' "$swap_total"
printf 'swap_free_bytes\t%s\n' "$swap_free"
printf 'filesystem_total_bytes\t%s\n' "$filesystem_total"
printf 'filesystem_available_bytes\t%s\n' "$filesystem_available"
