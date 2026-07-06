#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

if command -v python3 >/dev/null 2>&1; then
  python3 python/linearity_distortion_calculator.py > outputs/python_when_linear_models_clarify_and_when_they_distort_calculator.txt
else
  echo "python3 not found; skipping Python calculator."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/linearity_distortion_calculator.R > outputs/r_when_linear_models_clarify_and_when_they_distort_calculator.txt
else
  echo "Rscript not found; skipping R calculator."
fi

echo "Calculator smoke tests complete."
