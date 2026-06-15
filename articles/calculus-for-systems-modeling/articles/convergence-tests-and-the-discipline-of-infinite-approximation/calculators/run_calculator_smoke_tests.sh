#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py geometric --a 10 --r 0.6 --terms 25 > outputs/smoke_geometric.txt
  python3 python/article_calculator.py pseries --p 1.25 --terms 1000 > outputs/smoke_pseries.txt
  python3 python/article_calculator.py alternating --terms 1000 > outputs/smoke_alternating.txt
  python3 python/article_calculator.py derivative --x 2 --h 0.0001 > outputs/smoke_derivative.txt
  python3 python/article_calculator.py integral --a 0 --b 1 --steps 100 > outputs/smoke_integral.txt
  python3 python/article_calculator.py euler --x0 1 --rate 0.5 --dt 0.1 --steps 5 > outputs/smoke_euler.txt
  python3 python/article_calculator.py rk4 --x0 1 --rate 0.5 --dt 0.1 --steps 5 > outputs/smoke_rk4.txt
  python3 python/article_calculator.py logistic --initial 10 --carrying-capacity 100 --rate 0.25 --steps 5 > outputs/smoke_logistic.txt
  python3 python/article_calculator.py finite-diff --values 1,2,4,7,11 > outputs/smoke_finite_diff.txt
  python3 python/article_calculator.py sensitivity --parameter-min 0.1 --parameter-max 1.0 --samples 5 > outputs/smoke_sensitivity.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R geometric 10 0.6 25 > outputs/smoke_r_geometric.txt
  Rscript r/article_calculator.R pseries 1.25 1000 > outputs/smoke_r_pseries.txt
  Rscript r/article_calculator.R logistic 10 100 0.25 5 > outputs/smoke_r_logistic.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
