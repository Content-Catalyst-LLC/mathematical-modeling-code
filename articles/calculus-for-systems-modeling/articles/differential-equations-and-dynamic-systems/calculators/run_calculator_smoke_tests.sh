#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py exponential-rate --state 10 --growth-rate 0.35 > outputs/smoke_exponential_rate.txt
  python3 python/article_calculator.py logistic-rate --state 10 --growth-rate 0.35 --capacity 100 > outputs/smoke_logistic_rate.txt
  python3 python/article_calculator.py euler-step --state 10 --rate 3.5 --dt 0.1 > outputs/smoke_euler_step.txt
  python3 python/article_calculator.py simulate-exponential --state 10 --growth-rate 0.35 --dt 0.1 --steps 20 > outputs/smoke_simulate_exponential.txt
  python3 python/article_calculator.py simulate-logistic --state 10 --growth-rate 0.35 --capacity 100 --dt 0.1 --steps 20 > outputs/smoke_simulate_logistic.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R exponential-rate 10 0.35 > outputs/smoke_r_exponential_rate.txt
  Rscript r/article_calculator.R logistic-rate 10 0.35 100 > outputs/smoke_r_logistic_rate.txt
  Rscript r/article_calculator.R euler-step 10 3.5 0.1 > outputs/smoke_r_euler_step.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
