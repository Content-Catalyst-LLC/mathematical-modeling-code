#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py position --t 1 > outputs/smoke_position.txt
  python3 python/article_calculator.py velocity --t 1 > outputs/smoke_velocity.txt
  python3 python/article_calculator.py acceleration --t 1 > outputs/smoke_acceleration.txt
  python3 python/article_calculator.py speed --t 1 > outputs/smoke_speed.txt
  python3 python/article_calculator.py distance --x1 0 --y1 0 --x2 3 --y2 4 > outputs/smoke_distance.txt
  python3 python/article_calculator.py displacement --start 0 --stop 6.283185307 > outputs/smoke_displacement.txt
  python3 python/article_calculator.py arc-length-approx --step 0.25 > outputs/smoke_arc_length_approx.txt
  python3 python/article_calculator.py path-efficiency --step 0.25 > outputs/smoke_path_efficiency.txt
  python3 python/article_calculator.py finite-difference-velocity --t 1 --dt 0.01 > outputs/smoke_finite_difference_velocity.txt
  python3 python/article_calculator.py trajectory-audit --step 0.25 > outputs/smoke_trajectory_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R position 1 > outputs/smoke_r_position.txt
  Rscript r/article_calculator.R speed 1 > outputs/smoke_r_speed.txt
  Rscript r/article_calculator.R distance 0 0 3 4 > outputs/smoke_r_distance.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
