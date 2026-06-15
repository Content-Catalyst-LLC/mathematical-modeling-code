#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py vector-field --x 1 --y 0 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py normal-alignment --x 1 --y 0 > outputs/smoke_normal_alignment.txt
  python3 python/article_calculator.py tangent-alignment --x 1 --y 0 > outputs/smoke_tangent_alignment.txt
  python3 python/article_calculator.py flux-segment --radius 1 --segments 64 --index 0 > outputs/smoke_flux_segment.txt
  python3 python/article_calculator.py circulation-segment --radius 1 --segments 64 --index 0 > outputs/smoke_circulation_segment.txt
  python3 python/article_calculator.py circle-flux --radius 1 --segments 64 > outputs/smoke_circle_flux.txt
  python3 python/article_calculator.py circle-circulation --radius 1 --segments 64 > outputs/smoke_circle_circulation.txt
  python3 python/article_calculator.py flow-audit --radius 1 --segments 64 > outputs/smoke_flow_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R vector-field 1 0 > outputs/smoke_r_vector_field.txt
  Rscript r/article_calculator.R circle-circulation 1 64 > outputs/smoke_r_circle_circulation.txt
  Rscript r/article_calculator.R circle-flux 1 64 > outputs/smoke_r_circle_flux.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
