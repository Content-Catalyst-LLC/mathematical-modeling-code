#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py rectangle-total --density 12 --width 4 --height 3 > outputs/smoke_rectangle_total.txt
  python3 python/article_calculator.py volume-total --density 5 --length 4 --width 3 --height 2 > outputs/smoke_volume_total.txt
  python3 python/article_calculator.py polar-area --radius 3 > outputs/smoke_polar_area.txt
  python3 python/article_calculator.py polar-density-total --density 2 --radius 3 > outputs/smoke_polar_density_total.txt
  python3 python/article_calculator.py grid-total --step 0.5 > outputs/smoke_grid_total.txt
  python3 python/article_calculator.py area-average --step 0.5 > outputs/smoke_area_average.txt
  python3 python/article_calculator.py population-weighted --step 0.5 > outputs/smoke_population_weighted.txt
  python3 python/article_calculator.py cell-sum --values 1 2 3 4 --cell-area 0.25 > outputs/smoke_cell_sum.txt
  python3 python/article_calculator.py weighted-average --values 10 20 30 --weights 1 2 3 > outputs/smoke_weighted_average.txt
  python3 python/article_calculator.py resolution-scan --steps 1.0 0.5 0.25 > outputs/smoke_resolution_scan.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R rectangle-total 12 4 3 > outputs/smoke_r_rectangle_total.txt
  Rscript r/article_calculator.R grid-total 0.5 > outputs/smoke_r_grid_total.txt
  Rscript r/article_calculator.R population-weighted 0.5 > outputs/smoke_r_population_weighted.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
