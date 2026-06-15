#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py linear-rate --state 20 --input-rate 12 --loss-rate 0.4 > outputs/smoke_linear_rate.txt
  python3 python/article_calculator.py equilibrium --input-rate 12 --loss-rate 0.4 > outputs/smoke_equilibrium.txt
  python3 python/article_calculator.py analytical-solution --time 2 --initial 20 --input-rate 12 --loss-rate 0.4 > outputs/smoke_analytical_solution.txt
  python3 python/article_calculator.py euler-step --state 20 --input-rate 12 --loss-rate 0.4 --dt 0.1 > outputs/smoke_euler_step.txt
  python3 python/article_calculator.py compare-euler --initial 20 --input-rate 12 --loss-rate 0.4 --dt 0.1 --steps 20 > outputs/smoke_compare_euler.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R linear-rate 20 12 0.4 > outputs/smoke_r_linear_rate.txt
  Rscript r/article_calculator.R equilibrium 12 0.4 > outputs/smoke_r_equilibrium.txt
  Rscript r/article_calculator.R analytical-solution 2 20 12 0.4 > outputs/smoke_r_analytical_solution.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
