#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py exponential --n0 100 --r 0.08 --t 40 > outputs/smoke_exponential.txt
  python3 python/article_calculator.py logistic --n0 100 --r 0.08 --k 1000 --t 40 > outputs/smoke_logistic.txt
  python3 python/article_calculator.py allee --n0 100 --r 0.08 --k 1000 --a 75 --t 40 > outputs/smoke_allee.txt
  python3 python/article_calculator.py harvesting --n0 100 --r 0.08 --k 1000 --h 12 --t 40 > outputs/smoke_harvesting.txt
  python3 python/article_calculator.py stochastic --n0 100 --r 0.08 --k 1000 --sigma 0.12 --t 40 > outputs/smoke_stochastic.txt
  python3 python/article_calculator.py two-patch --n1 100 --n2 400 --r 0.08 --k 1000 --m 0.04 --t 40 > outputs/smoke_two_patch.txt
  python3 python/article_calculator.py leslie --steps 20 > outputs/smoke_leslie.txt
  python3 python/article_calculator.py capacity-warning --n 900 --k 1000 --margin 0.15 > outputs/smoke_capacity_warning.txt
  python3 python/article_calculator.py identifiability-warning --pattern short_series > outputs/smoke_identifiability.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic 100 0.08 1000 40 > outputs/smoke_r_logistic.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi
echo "[calculator smoke] done"
