#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py vector-field --x 1 --y 0 --z 0 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py curl-field --x 1 --y 0 --z 0 > outputs/smoke_curl_field.txt
  python3 python/article_calculator.py boundary-circulation --radius 1 --segments 128 > outputs/smoke_boundary_circulation.txt
  python3 python/article_calculator.py surface-curl-flux --radius 1 --radial-steps 32 > outputs/smoke_surface_curl_flux.txt
  python3 python/article_calculator.py stokes-audit --radius 1 --segments 128 --radial-steps 32 > outputs/smoke_stokes_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R boundary-circulation 1 128 > outputs/smoke_r_boundary_circulation.txt
  Rscript r/article_calculator.R surface-curl-flux 1 32 > outputs/smoke_r_surface_curl_flux.txt
  Rscript r/article_calculator.R stokes-audit 1 128 32 > outputs/smoke_r_stokes_audit.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
