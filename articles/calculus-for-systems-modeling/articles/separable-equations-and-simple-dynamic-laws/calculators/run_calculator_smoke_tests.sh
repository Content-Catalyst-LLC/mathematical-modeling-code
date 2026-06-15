#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py exponential-solution --time 2 --initial 10 --growth-rate 0.25 > outputs/smoke_exponential_solution.txt
  python3 python/article_calculator.py exponential-rate --state 10 --growth-rate 0.25 > outputs/smoke_exponential_rate.txt
  python3 python/article_calculator.py logistic-solution --time 2 --initial 10 --growth-rate 0.25 --capacity 100 > outputs/smoke_logistic_solution.txt
  python3 python/article_calculator.py logistic-rate --state 10 --growth-rate 0.25 --capacity 100 > outputs/smoke_logistic_rate.txt
  python3 python/article_calculator.py compare-euler --model logistic --initial 10 --growth-rate 0.25 --capacity 100 --dt 0.1 --steps 20 > outputs/smoke_compare_euler.txt
fi
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R exponential-solution 2 10 0.25 > outputs/smoke_r_exponential_solution.txt
  Rscript r/article_calculator.R exponential-rate 10 0.25 > outputs/smoke_r_exponential_rate.txt
  Rscript r/article_calculator.R logistic-solution 2 10 0.25 100 > outputs/smoke_r_logistic_solution.txt
  Rscript r/article_calculator.R logistic-rate 10 0.25 100 > outputs/smoke_r_logistic_rate.txt
fi
echo "[calculator smoke] done"
