#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py vector-field --x 1 --y 2 --z 3 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py divergence --x 1 --y 2 --z 3 > outputs/smoke_divergence.txt
  python3 python/article_calculator.py boundary-flux --grid-steps 16 > outputs/smoke_boundary_flux.txt
  python3 python/article_calculator.py volume-divergence --grid-steps 16 > outputs/smoke_volume_divergence.txt
  python3 python/article_calculator.py conservation-audit --grid-steps 16 > outputs/smoke_conservation_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R boundary-flux 16 > outputs/smoke_r_boundary_flux.txt
  Rscript r/article_calculator.R volume-divergence 16 > outputs/smoke_r_volume_divergence.txt
  Rscript r/article_calculator.R conservation-audit 16 > outputs/smoke_r_conservation_audit.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
