#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py cumulative-linear --e0 40 --years 30 > outputs/smoke_cumulative_linear.txt
  python3 python/article_calculator.py cumulative-exponential --e0 40 --rate 0.08 --years 30 > outputs/smoke_cumulative_exponential.txt
  python3 python/article_calculator.py atmospheric-burden --cumulative 600 --airborne-fraction 0.45 > outputs/smoke_atmospheric_burden.txt
  python3 python/article_calculator.py budget-check --cumulative 600 --budget 500 > outputs/smoke_budget_check.txt
  python3 python/article_calculator.py overshoot --e0 40 --decline-years 30 --negative-years 20 --removal-rate 5 > outputs/smoke_overshoot.txt
  python3 python/article_calculator.py impulse-burden --e0 40 --years 30 --pathway linear > outputs/smoke_impulse_burden.txt
  python3 python/article_calculator.py removal-warning --gross 10 --removal 10 > outputs/smoke_removal_warning.txt
  python3 python/article_calculator.py accounting-warning --boundary global_co2 > outputs/smoke_accounting_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R cumulative-linear 40 30 > outputs/smoke_r_cumulative_linear.txt
  Rscript r/article_calculator.R budget-check 600 500 > outputs/smoke_r_budget_check.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
