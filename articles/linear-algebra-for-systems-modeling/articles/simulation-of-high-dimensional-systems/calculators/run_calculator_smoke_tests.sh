#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

if command -v python3 >/dev/null 2>&1; then
  python3 python/high_dimensional_simulation_calculator.py > outputs/python_simulation_of_high_dimensional_systems_calculator.txt
else
  echo "python3 not found; skipping Python calculator."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/high_dimensional_simulation_calculator.R > outputs/r_simulation_of_high_dimensional_systems_calculator.txt
else
  echo "Rscript not found; skipping R calculator."
fi

echo "Calculator smoke tests complete."
