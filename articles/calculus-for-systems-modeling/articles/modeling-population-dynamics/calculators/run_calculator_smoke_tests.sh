#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py exponential --n0 100 --r 0.08 --t 40 > outputs/smoke_exponential.txt
  python3 python/article_calculator.py logistic --n0 100 --r 0.08 --k 1000 --t 40 > outputs/smoke_logistic.txt
  python3 python/article_calculator.py per-capita --growth 8 --population 100 > outputs/smoke_per_capita.txt
  python3 python/article_calculator.py equilibrium --r 0.08 --k 1000 > outputs/smoke_equilibrium.txt
  python3 python/article_calculator.py sensitivity-r --n0 100 --r 0.08 --k 1000 --t 40 --delta 0.01 > outputs/smoke_sensitivity_r.txt
  python3 python/article_calculator.py capacity-warning --n 900 --k 1000 --margin 0.15 > outputs/smoke_capacity_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R exponential 100 0.08 40 > outputs/smoke_r_exponential.txt
  Rscript r/article_calculator.R logistic 100 0.08 1000 40 > outputs/smoke_r_logistic.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
