#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py approximation-error --true-value 2.718281828 --approximation 2.716666667 > outputs/smoke_approximation_error.txt
  python3 python/article_calculator.py relative-error --true-value 2.718281828 --approximation 2.716666667 > outputs/smoke_relative_error.txt
  python3 python/article_calculator.py taylor-exp --x 1 --order 10 > outputs/smoke_taylor_exp.txt
  python3 python/article_calculator.py truncation-sweep --x 1 --max-order 12 > outputs/smoke_truncation_sweep.txt
  python3 python/article_calculator.py derivative-step --x 2 --h 0.01 > outputs/smoke_derivative_step.txt
  python3 python/article_calculator.py integral-step --a 0 --b 1 --steps 100 > outputs/smoke_integral_step.txt
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
  Rscript r/article_calculator.R approximation-error 2.718281828 2.716666667 > outputs/smoke_r_approximation_error.txt
  Rscript r/article_calculator.R taylor-exp 1 10 > outputs/smoke_r_taylor_exp.txt
  Rscript r/article_calculator.R logistic 10 100 0.25 5 > outputs/smoke_r_logistic.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
