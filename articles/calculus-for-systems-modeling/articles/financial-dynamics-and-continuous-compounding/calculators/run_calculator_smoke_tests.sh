#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py continuous-future-value --v0 1000 --r 0.05 --t 30 > outputs/smoke_continuous_future_value.txt
  python3 python/article_calculator.py continuous-present-value --fv 5000 --r 0.05 --t 30 > outputs/smoke_continuous_present_value.txt
  python3 python/article_calculator.py discrete-compound-value --v0 1000 --r 0.05 --n 12 --t 30 > outputs/smoke_discrete_compound_value.txt
  python3 python/article_calculator.py real-rate --nominal-rate 0.06 --inflation-rate 0.025 > outputs/smoke_real_rate.txt
  python3 python/article_calculator.py npv --discount-rate 0.045 --cash-flows "0:-1000,5:300,10:500,15:900,20:1200" > outputs/smoke_npv.txt
  python3 python/article_calculator.py debt-step --balance 2000 --rate 0.07 --payment 120 > outputs/smoke_debt_step.txt
  python3 python/article_calculator.py geometric-return --returns "0.08,-0.12,0.15,0.04,-0.05,0.11" > outputs/smoke_geometric_return.txt
  python3 python/article_calculator.py governance-warning --context expected_return > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R continuous-future-value 1000 0.05 30 > outputs/smoke_r_continuous_future_value.txt
  Rscript r/article_calculator.R continuous-present-value 5000 0.05 30 > outputs/smoke_r_continuous_present_value.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
