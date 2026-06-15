#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py predator-prey-rates --prey 40 --predator 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 > outputs/smoke_predator_prey_rates.txt
  python3 python/article_calculator.py coexistence-equilibrium --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 > outputs/smoke_coexistence_equilibrium.txt
  python3 python/article_calculator.py euler-step --prey 40 --predator 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 --dt 0.01 > outputs/smoke_euler_step.txt
  python3 python/article_calculator.py simulate-predator-prey --prey 40 --predator 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 --dt 0.01 --steps 100 > outputs/smoke_simulate_predator_prey.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R predator-prey-rates 40 9 0.7 0.05 0.02 0.5 > outputs/smoke_r_predator_prey_rates.txt
  Rscript r/article_calculator.R coexistence-equilibrium 0.7 0.05 0.02 0.5 > outputs/smoke_r_coexistence_equilibrium.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
