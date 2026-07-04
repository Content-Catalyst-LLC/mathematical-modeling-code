#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

if command -v python3 >/dev/null 2>&1; then
  python3 python/large_scale_matrix_computation_calculator.py > outputs/python_large_scale_matrix_computation_calculator.txt
else
  echo "python3 not found; skipping Python calculator."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/large_scale_matrix_computation_calculator.R > outputs/r_large_scale_matrix_computation_calculator.txt
else
  echo "Rscript not found; skipping R calculator."
fi

echo "Calculator smoke tests complete."
