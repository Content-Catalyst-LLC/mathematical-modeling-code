#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py classify-derivative --derivative-value -0.6 > outputs/smoke_classify_derivative.txt
  python3 python/article_calculator.py logistic-stability --equilibrium 100 --growth-rate 0.6 --carrying-capacity 100 > outputs/smoke_logistic_stability.txt
  python3 python/article_calculator.py bistable-stability --equilibrium 0.4 --threshold 0.4 > outputs/smoke_bistable_stability.txt
  python3 python/article_calculator.py numerical-derivative --model bistable --state 0.4 --threshold 0.4 > outputs/smoke_numerical_derivative.txt
  python3 python/article_calculator.py equilibrium-table --growth-rate 0.6 --carrying-capacity 100 --threshold 0.4 > outputs/smoke_equilibrium_table.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R classify-derivative -0.6 > outputs/smoke_r_classify_derivative.txt
  Rscript r/article_calculator.R logistic-stability 100 0.6 100 > outputs/smoke_r_logistic_stability.txt
  Rscript r/article_calculator.R bistable-stability 0.4 0.4 > outputs/smoke_r_bistable_stability.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
