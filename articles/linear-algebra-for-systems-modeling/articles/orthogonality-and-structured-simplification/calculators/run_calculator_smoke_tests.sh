#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

if command -v python3 >/dev/null 2>&1; then
  python3 python/orthogonality_calculator.py > outputs/python_orthogonality_calculator.txt
else
  echo "python3 not found; skipping Python calculator."
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/orthogonality_calculator.R > outputs/r_orthogonality_calculator.txt
else
  echo "Rscript not found; skipping R calculator."
fi

echo "Calculator smoke tests complete."
