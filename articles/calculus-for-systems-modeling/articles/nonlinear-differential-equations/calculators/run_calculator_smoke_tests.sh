#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-rate --state 10 --growth-rate 0.6 --carrying-capacity 100 > outputs/smoke_logistic_rate.txt
  python3 python/article_calculator.py logistic-equilibria --carrying-capacity 100 > outputs/smoke_logistic_equilibria.txt
  python3 python/article_calculator.py bistable-rate --state 0.35 --threshold 0.4 > outputs/smoke_bistable_rate.txt
  python3 python/article_calculator.py bistable-equilibria --threshold 0.4 > outputs/smoke_bistable_equilibria.txt
  python3 python/article_calculator.py euler-step --model logistic --state 10 --growth-rate 0.6 --carrying-capacity 100 --dt 0.05 > outputs/smoke_euler_step.txt
  python3 python/article_calculator.py simulate --model logistic --state 10 --growth-rate 0.6 --carrying-capacity 100 --dt 0.05 --steps 100 > outputs/smoke_simulate.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-rate 10 0.6 100 > outputs/smoke_r_logistic_rate.txt
  Rscript r/article_calculator.R logistic-equilibria 100 > outputs/smoke_r_logistic_equilibria.txt
  Rscript r/article_calculator.R bistable-rate 0.35 0.4 > outputs/smoke_r_bistable_rate.txt
  Rscript r/article_calculator.R bistable-equilibria 0.4 > outputs/smoke_r_bistable_equilibria.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
