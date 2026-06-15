#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py evaluate --x 2 --y 1 > outputs/smoke_evaluate.txt
  python3 python/article_calculator.py jacobian --x 2 --y 1 > outputs/smoke_jacobian.txt
  python3 python/article_calculator.py determinant --x 2 --y 1 > outputs/smoke_determinant.txt
  python3 python/article_calculator.py local-linear --x 2 --y 1 --dx 0.1 --dy -0.05 > outputs/smoke_local_linear.txt
  python3 python/article_calculator.py approximation-error --x 2 --y 1 --dx 0.5 --dy 0.5 > outputs/smoke_approximation_error.txt
  python3 python/article_calculator.py area-scaling --x 2 --y 1 --area 3 > outputs/smoke_area_scaling.txt
  python3 python/article_calculator.py singularity-check --x 0 --y 0 > outputs/smoke_singularity_check.txt
  python3 python/article_calculator.py polar-jacobian --r 3 --theta 0.785398163 > outputs/smoke_polar_jacobian.txt
  python3 python/article_calculator.py sensitivity-column --x 2 --y 1 --input-index 1 > outputs/smoke_sensitivity_column.txt
  python3 python/article_calculator.py sensitivity-row --x 2 --y 1 --output-index 2 > outputs/smoke_sensitivity_row.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R jacobian 2 1 > outputs/smoke_r_jacobian.txt
  Rscript r/article_calculator.R determinant 2 1 > outputs/smoke_r_determinant.txt
  Rscript r/article_calculator.R local-linear 2 1 0.1 -0.05 > outputs/smoke_r_local_linear.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
