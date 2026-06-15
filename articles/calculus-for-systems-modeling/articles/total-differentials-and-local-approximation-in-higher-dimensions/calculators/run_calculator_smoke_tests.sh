#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py evaluate --x 4 --y 3 > outputs/smoke_evaluate.txt
  python3 python/article_calculator.py total-differential --x 4 --y 3 --dx 0.2 --dy -0.1 > outputs/smoke_total_differential.txt
  python3 python/article_calculator.py local-linear --x 4 --y 3 --dx 0.2 --dy -0.1 > outputs/smoke_local_linear.txt
  python3 python/article_calculator.py approximation-error --x 4 --y 3 --dx 1 --dy 1 > outputs/smoke_approximation_error.txt
  python3 python/article_calculator.py gradient-dot --gradient 4.5,4 --displacement 0.2,-0.1 > outputs/smoke_gradient_dot.txt
  python3 python/article_calculator.py feasible-displacement --x 8 --y 1 --dx 1 --dy 1 --budget 10 > outputs/smoke_feasible_displacement.txt
  python3 python/article_calculator.py perturbation-sweep --x 4 --y 3 --scale-max 2 --samples 10 > outputs/smoke_perturbation_sweep.txt
  python3 python/article_calculator.py uncertainty-propagation --x 4 --y 3 --dx-error 0.1 --dy-error 0.2 > outputs/smoke_uncertainty_propagation.txt
  python3 python/article_calculator.py tangent-plane --x0 4 --y0 3 --x 4.2 --y 2.9 > outputs/smoke_tangent_plane.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R total-differential 4 3 0.2 -0.1 > outputs/smoke_r_total_differential.txt
  Rscript r/article_calculator.R local-linear 4 3 0.2 -0.1 > outputs/smoke_r_local_linear.txt
  Rscript r/article_calculator.R approximation-error 4 3 1 1 > outputs/smoke_r_approximation_error.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
