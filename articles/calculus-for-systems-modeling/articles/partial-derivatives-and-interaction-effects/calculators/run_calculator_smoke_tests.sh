#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py evaluate --x 4 --y 3 > outputs/smoke_evaluate.txt
  python3 python/article_calculator.py partial-x --x 4 --y 3 > outputs/smoke_partial_x.txt
  python3 python/article_calculator.py partial-y --x 4 --y 3 > outputs/smoke_partial_y.txt
  python3 python/article_calculator.py cross-partial --x 4 --y 3 > outputs/smoke_cross_partial.txt
  python3 python/article_calculator.py interaction --x 4 --y 3 > outputs/smoke_interaction.txt
  python3 python/article_calculator.py grid --max-x 10 --max-y 10 --step 2 > outputs/smoke_grid.txt
  python3 python/article_calculator.py numeric-partial-x --x 4 --y 3 --h 0.001 > outputs/smoke_numeric_partial_x.txt
  python3 python/article_calculator.py numeric-partial-y --x 4 --y 3 --h 0.001 > outputs/smoke_numeric_partial_y.txt
  python3 python/article_calculator.py feasible --x 8 --y 4 --budget 10 > outputs/smoke_feasible.txt
  python3 python/article_calculator.py local-neighborhood --x 4 --y 3 --center-x 3 --center-y 3 --radius 2 > outputs/smoke_local_neighborhood.txt
  python3 python/article_calculator.py sensitivity --x-min 0 --x-max 10 --y 3 --samples 10 > outputs/smoke_sensitivity.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R evaluate 4 3 > outputs/smoke_r_evaluate.txt
  Rscript r/article_calculator.R partial-x 4 3 > outputs/smoke_r_partial_x.txt
  Rscript r/article_calculator.R partial-y 4 3 > outputs/smoke_r_partial_y.txt
  Rscript r/article_calculator.R cross-partial 4 3 > outputs/smoke_r_cross_partial.txt
  Rscript r/article_calculator.R interaction 4 3 > outputs/smoke_r_interaction.txt
  Rscript r/article_calculator.R grid 10 10 2 > outputs/smoke_r_grid.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
