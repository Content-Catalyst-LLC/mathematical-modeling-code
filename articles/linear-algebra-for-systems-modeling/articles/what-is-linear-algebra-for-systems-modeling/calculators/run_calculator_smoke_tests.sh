#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

if command -v python3 >/dev/null 2>&1; then
  python3 python/matrix_calculator.py
else
  echo "python3 not found; skipping Python calculator."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/matrix_calculator.R
else
  echo "Rscript not found; skipping R calculator."
fi

echo "calculator smoke tests complete" > outputs/calculator_smoke_test.txt
