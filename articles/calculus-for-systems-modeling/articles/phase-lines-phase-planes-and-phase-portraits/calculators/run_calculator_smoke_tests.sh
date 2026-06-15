#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py predator-prey-vector --x 40 --y 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 > outputs/smoke_predator_prey_vector.txt
  python3 python/article_calculator.py phase-speed --dxdt 3 --dydt 4 > outputs/smoke_phase_speed.txt
  python3 python/article_calculator.py coexistence-equilibrium --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 > outputs/smoke_coexistence_equilibrium.txt
  python3 python/article_calculator.py grid-summary --x-max 60 --y-max 30 --x-step 5 --y-step 3 > outputs/smoke_grid_summary.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R predator-prey-vector 40 9 0.7 0.05 0.02 0.5 > outputs/smoke_r_predator_prey_vector.txt
  Rscript r/article_calculator.R phase-speed 3 4 > outputs/smoke_r_phase_speed.txt
  Rscript r/article_calculator.R coexistence-equilibrium 0.7 0.05 0.02 0.5 > outputs/smoke_r_coexistence_equilibrium.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
