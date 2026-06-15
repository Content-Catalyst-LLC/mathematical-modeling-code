#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py rotation-field --x 1 --y 1 > outputs/smoke_rotation_field.txt
  python3 python/article_calculator.py expansion-field --x 1 --y 1 > outputs/smoke_expansion_field.txt
  python3 python/article_calculator.py planar-curl --x 1 --y 1 > outputs/smoke_planar_curl.txt
  python3 python/article_calculator.py planar-divergence --x 1 --y 1 > outputs/smoke_planar_divergence.txt
  python3 python/article_calculator.py boundary-circulation --segments 32 > outputs/smoke_boundary_circulation.txt
  python3 python/article_calculator.py interior-curl --step 0.25 > outputs/smoke_interior_curl.txt
  python3 python/article_calculator.py boundary-flux --segments 32 > outputs/smoke_boundary_flux.txt
  python3 python/article_calculator.py interior-divergence --step 0.25 > outputs/smoke_interior_divergence.txt
  python3 python/article_calculator.py greens-audit --segments 32 --step 0.25 > outputs/smoke_greens_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R boundary-circulation 32 > outputs/smoke_r_boundary_circulation.txt
  Rscript r/article_calculator.R interior-curl 0.25 > outputs/smoke_r_interior_curl.txt
  Rscript r/article_calculator.R greens-audit 32 0.25 > outputs/smoke_r_greens_audit.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
