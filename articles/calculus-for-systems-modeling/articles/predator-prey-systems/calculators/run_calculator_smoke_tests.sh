#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py lotka-volterra-step --x 40 --y 9 --alpha 0.6 --beta 0.02 --gamma 0.5 --delta 0.01 --dt 0.02 > outputs/smoke_lotka_step.txt
  python3 python/article_calculator.py coexistence --alpha 0.6 --beta 0.02 --gamma 0.5 --delta 0.01 > outputs/smoke_coexistence.txt
  python3 python/article_calculator.py jacobian --x 50 --y 30 --alpha 0.6 --beta 0.02 --gamma 0.5 --delta 0.01 > outputs/smoke_jacobian.txt
  python3 python/article_calculator.py simulate --x0 40 --y0 9 --steps 4000 > outputs/smoke_simulate.txt
  python3 python/article_calculator.py type-ii-response --x 50 --a 0.04 --h 0.08 > outputs/smoke_type_ii_response.txt
  python3 python/article_calculator.py harvesting-risk --hx 1 --hy 0.05 > outputs/smoke_harvesting_risk.txt
  python3 python/article_calculator.py interaction-warning --pattern mass_action > outputs/smoke_interaction_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R coexistence 0.6 0.02 0.5 0.01 > outputs/smoke_r_coexistence.txt
  Rscript r/article_calculator.R type-ii-response 50 0.04 0.08 > outputs/smoke_r_type_ii_response.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
