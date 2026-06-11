#!/usr/bin/env bash
# Detect the GPU resource pool. Prints ONE JSON line:
#   {"type":"gpu","units":[0,1],"vram_total_mb":24210}
# units = physical GPU ids (filtered by $GPUS if set, e.g. GPUS=2,3,5);
# vram_total_mb = smallest GPU's total VRAM (heterogeneous-safe).
set -euo pipefail

mapfile -t rows < <(nvidia-smi --query-gpu=index,memory.total --format=csv,noheader,nounits)
[ "${#rows[@]}" -gt 0 ] || { echo '{"error":"no GPUs visible"}' >&2; exit 1; }

declare -a units=()
min_vram=""
for row in "${rows[@]}"; do
  idx="${row%%,*}"; vram="${row##*, }"
  if [ -n "${GPUS:-}" ]; then
    case ",$GPUS," in *",$idx,"*) ;; *) continue ;; esac
  fi
  units+=("$idx")
  if [ -z "$min_vram" ] || [ "$vram" -lt "$min_vram" ]; then min_vram="$vram"; fi
done

[ "${#units[@]}" -gt 0 ] || { echo '{"error":"GPUS filter matched nothing"}' >&2; exit 1; }

printf '{"type":"gpu","units":[%s],"vram_total_mb":%s}\n' "$(IFS=,; echo "${units[*]}")" "$min_vram"
