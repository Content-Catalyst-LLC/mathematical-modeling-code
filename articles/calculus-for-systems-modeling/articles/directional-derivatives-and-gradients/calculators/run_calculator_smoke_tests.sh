#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py evaluate --x 4 --y 3 > outputs/smoke_evaluate.txt
  python3 python/article_calculator.py gradient --x 4 --y 3 > outputs/smoke_gradient.txt
  python3 python/article_calculator.py gradient-norm --x 4 --y 3 > outputs/smoke_gradient_norm.txt
  python3 python/article_calculator.py normalize --vx 2 --vy -1 > outputs/smoke_normalize.txt
  python3 python/article_calculator.py directional-derivative --x 4 --y 3 --vx 1 --vy 1 > outputs/smoke_directional_derivative.txt
  python3 python/article_calculator.py estimated-change --x 4 --y 3 --vx 1 --vy 1 --step 0.25 > outputs/smoke_estimated_change.txt
  python3 python/article_calculator.py feasible-direction --x 8 --y 1 --vx 1 --vy 1 --step 1 --budget 10 > outputs/smoke_feasible_direction.txt
  python3 python/article_calculator.py gradient-ascent-step --x 4 --y 3 --step 0.25 > outputs/smoke_gradient_ascent_step.txt
  python3 python/article_calculator.py gradient-descent-step --x 4 --y 3 --step 0.25 > outputs/smoke_gradient_descent_step.txt
  python3 python/article_calculator.py compare-directions --x 4 --y 3 > outputs/smoke_compare_directions.txt
  python3 python/article_calculator.py contour-tangent --x 4 --y 3 > outputs/smoke_contour_tangent.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R gradient 4 3 > outputs/smoke_r_gradient.txt
  Rscript r/article_calculator.R directional-derivative 4 3 1 1 > outputs/smoke_r_directional_derivative.txt
  Rscript r/article_calculator.R estimated-change 4 3 1 1 0.25 > outputs/smoke_r_estimated_change.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
