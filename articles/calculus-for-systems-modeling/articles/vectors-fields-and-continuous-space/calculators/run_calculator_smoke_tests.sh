#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py vector-magnitude --vx 3 --vy 4 > outputs/smoke_vector_magnitude.txt
  python3 python/article_calculator.py vector-components --magnitude 5 --angle-degrees 53.130102354 > outputs/smoke_vector_components.txt
  python3 python/article_calculator.py dot-product --ax 1 --ay 2 --bx 3 --by 4 > outputs/smoke_dot_product.txt
  python3 python/article_calculator.py scalar-field --x 1 --y 2 > outputs/smoke_scalar_field.txt
  python3 python/article_calculator.py vector-field --x 1 --y 2 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py field-magnitude --x 1 --y 2 > outputs/smoke_field_magnitude.txt
  python3 python/article_calculator.py grid-audit --step 0.5 > outputs/smoke_grid_audit.txt
  python3 python/article_calculator.py resolution-scan --steps 1.0 0.5 0.25 > outputs/smoke_resolution_scan.txt
  python3 python/article_calculator.py unit-vector --vx 3 --vy 4 > outputs/smoke_unit_vector.txt
  python3 python/article_calculator.py projection --ax 3 --ay 4 --bx 1 --by 0 > outputs/smoke_projection.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R vector-magnitude 3 4 > outputs/smoke_r_vector_magnitude.txt
  Rscript r/article_calculator.R scalar-field 1 2 > outputs/smoke_r_scalar_field.txt
  Rscript r/article_calculator.R vector-field 1 2 > outputs/smoke_r_vector_field.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
