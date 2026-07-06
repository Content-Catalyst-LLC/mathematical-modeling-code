#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

if command -v python3 >/dev/null 2>&1; then
  python3 python/dimensionality_reduction_calculator.py > outputs/python_case_study_dimensionality_reduction_calculator.txt
else
  echo "python3 not found; skipping Python calculator."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/dimensionality_reduction_calculator.R > outputs/r_case_study_dimensionality_reduction_calculator.txt
else
  echo "Rscript not found; skipping R calculator."
fi

echo "Calculator smoke tests complete."
