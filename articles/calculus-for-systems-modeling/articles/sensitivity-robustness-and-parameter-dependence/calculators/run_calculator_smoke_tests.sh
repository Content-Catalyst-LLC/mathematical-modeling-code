#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-final --initial-stock 10 --growth-rate 0.35 --carrying-capacity 100 --horizon 20 > outputs/smoke_logistic_final.txt
  python3 python/article_calculator.py finite-difference --low-output 85.8 --high-output 99.7 --lower 0.2 --upper 0.5 > outputs/smoke_finite_difference.txt
  python3 python/article_calculator.py elasticity --sensitivity 46.3 --parameter 0.35 --output 99.2 > outputs/smoke_elasticity.txt
  python3 python/article_calculator.py robustness-classification --low-output 85.8 --high-output 99.7 --threshold 10 > outputs/smoke_robustness_classification.txt
  python3 python/article_calculator.py sweep-range --lower 0.2 --upper 0.5 --steps 7 > outputs/smoke_sweep_range.txt
  python3 python/article_calculator.py sensitivity-warning --pattern robustness_domain > outputs/smoke_sensitivity_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R finite-difference 85.8 99.7 0.2 0.5 > outputs/smoke_r_finite_difference.txt
  Rscript r/article_calculator.R robustness-classification 85.8 99.7 10 > outputs/smoke_r_robustness_classification.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
