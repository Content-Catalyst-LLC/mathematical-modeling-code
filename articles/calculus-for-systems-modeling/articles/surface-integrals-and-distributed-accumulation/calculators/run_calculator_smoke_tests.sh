#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py height --x 1 --y 1 > outputs/smoke_height.txt
  python3 python/article_calculator.py scalar-field --x 1 --y 1 > outputs/smoke_scalar_field.txt
  python3 python/article_calculator.py vector-field --x 1 --y 1 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py normal-area-vector --x 1 --y 1 --step 0.25 > outputs/smoke_normal_area_vector.txt
  python3 python/article_calculator.py patch-area --x 1 --y 1 --step 0.25 > outputs/smoke_patch_area.txt
  python3 python/article_calculator.py scalar-patch --x 1 --y 1 --step 0.25 > outputs/smoke_scalar_patch.txt
  python3 python/article_calculator.py flux-patch --x 1 --y 1 --step 0.25 > outputs/smoke_flux_patch.txt
  python3 python/article_calculator.py surface-audit --step 0.25 > outputs/smoke_surface_audit.txt
  python3 python/article_calculator.py surface-area --step 0.25 > outputs/smoke_surface_area.txt
  python3 python/article_calculator.py flux-approx --step 0.25 > outputs/smoke_flux_approx.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R height 1 1 > outputs/smoke_r_height.txt
  Rscript r/article_calculator.R patch-area 1 1 0.25 > outputs/smoke_r_patch_area.txt
  Rscript r/article_calculator.R scalar-field 1 1 > outputs/smoke_r_scalar_field.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
