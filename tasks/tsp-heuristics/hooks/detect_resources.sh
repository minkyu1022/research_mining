#!/usr/bin/env bash
# Detect the CPU resource pool. Prints ONE JSON line:
#   {"type":"cpu","units":[0,1,2,3],"cpus_per_slot":2}
# Slot count is capped by task.yml resources.slots; units listed here are
# the available worker indices. cpus_per_slot = floor(nproc / units).
set -euo pipefail

NPROC=$(nproc)
SLOTS=${SLOTS:-4}
[ "$SLOTS" -le "$NPROC" ] || SLOTS=$NPROC
CPUS_PER_SLOT=$(( NPROC / SLOTS ))
[ "$CPUS_PER_SLOT" -ge 1 ] || CPUS_PER_SLOT=1

units=$(seq -s, 0 $((SLOTS - 1)))
printf '{"type":"cpu","units":[%s],"cpus_per_slot":%d}\n' "$units" "$CPUS_PER_SLOT"
