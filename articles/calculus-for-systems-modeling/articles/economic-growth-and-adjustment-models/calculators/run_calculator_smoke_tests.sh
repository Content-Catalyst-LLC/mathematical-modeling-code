#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py exponential-growth --y0 100 --g 0.025 --years 40 > outputs/smoke_exponential_growth.txt
  python3 python/article_calculator.py doubling-time --g 0.025 > outputs/smoke_doubling_time.txt
  python3 python/article_calculator.py logistic-growth --y0 100 --r 0.06 --k 240 --years 40 > outputs/smoke_logistic_growth.txt
  python3 python/article_calculator.py capital-step --capital 300 --output 100 --savings-rate 0.22 --depreciation 0.05 > outputs/smoke_capital_step.txt
  python3 python/article_calculator.py cobb-douglas --a 1.2 --k 450 --l 180 --alpha 0.35 > outputs/smoke_cobb_douglas.txt
  python3 python/article_calculator.py growth-accounting --a-growth 0.01 --k-growth 0.03 --l-growth 0.02 --alpha 0.35 > outputs/smoke_growth_accounting.txt
  python3 python/article_calculator.py adjustment-step --x 100 --target 160 --lambda-rate 0.35 > outputs/smoke_adjustment_step.txt
  python3 python/article_calculator.py governance-warning --context output_welfare > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R exponential-growth 100 0.025 40 > outputs/smoke_r_exponential_growth.txt
  Rscript r/article_calculator.R doubling-time 0.025 > outputs/smoke_r_doubling_time.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
