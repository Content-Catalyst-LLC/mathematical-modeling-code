#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py evaluate --x 2 --y 1 > outputs/smoke_evaluate.txt
  python3 python/article_calculator.py gradient --x 2 --y 1 > outputs/smoke_gradient.txt
  python3 python/article_calculator.py hessian --x 2 --y 1 > outputs/smoke_hessian.txt
  python3 python/article_calculator.py determinant --x 2 --y 1 > outputs/smoke_determinant.txt
  python3 python/article_calculator.py classify --x 2 --y 1 > outputs/smoke_classify.txt
  python3 python/article_calculator.py quadratic-term --x 2 --y 1 --dx 0.1 --dy -0.05 > outputs/smoke_quadratic_term.txt
  python3 python/article_calculator.py first-order --x 2 --y 1 --dx 0.1 --dy -0.05 > outputs/smoke_first_order.txt
  python3 python/article_calculator.py second-order --x 2 --y 1 --dx 0.1 --dy -0.05 > outputs/smoke_second_order.txt
  python3 python/article_calculator.py approximation-error --x 2 --y 1 --dx 0.5 --dy 0.5 > outputs/smoke_approximation_error.txt
  python3 python/article_calculator.py eigen-2x2 --x 2 --y 1 > outputs/smoke_eigen_2x2.txt
  python3 python/article_calculator.py conditioning-check --x 2 --y 1 > outputs/smoke_conditioning_check.txt
  python3 python/article_calculator.py cross-partial --x 2 --y 1 > outputs/smoke_cross_partial.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R hessian 2 1 > outputs/smoke_r_hessian.txt
  Rscript r/article_calculator.R classify 2 1 > outputs/smoke_r_classify.txt
  Rscript r/article_calculator.R second-order 2 1 0.1 -0.05 > outputs/smoke_r_second_order.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
