#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py polar-jacobian --radius 3 > outputs/smoke_polar_jacobian.txt
  python3 python/article_calculator.py polar-area-element --radius 3 --dr 0.1 --dtheta 0.05 > outputs/smoke_polar_area_element.txt
  python3 python/article_calculator.py circular-area --radius 3 > outputs/smoke_circular_area.txt
  python3 python/article_calculator.py polar-density-total --density 2 --radius 3 > outputs/smoke_polar_density_total.txt
  python3 python/article_calculator.py cylindrical-volume --radius 3 --height 4 > outputs/smoke_cylindrical_volume.txt
  python3 python/article_calculator.py spherical-volume --radius 3 > outputs/smoke_spherical_volume.txt
  python3 python/article_calculator.py linear-det --a 2 --b 1 --c 0 --d 3 > outputs/smoke_linear_det.txt
  python3 python/article_calculator.py orientation-check --determinant -2 > outputs/smoke_orientation_check.txt
  python3 python/article_calculator.py singularity-check --determinant 0.000001 > outputs/smoke_singularity_check.txt
  python3 python/article_calculator.py polar-audit --radius 3 --dr 0.25 --dtheta 0.0654498469 > outputs/smoke_polar_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R polar-jacobian 3 > outputs/smoke_r_polar_jacobian.txt
  Rscript r/article_calculator.R circular-area 3 > outputs/smoke_r_circular_area.txt
  Rscript r/article_calculator.R linear-det 2 1 0 3 > outputs/smoke_r_linear_det.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
