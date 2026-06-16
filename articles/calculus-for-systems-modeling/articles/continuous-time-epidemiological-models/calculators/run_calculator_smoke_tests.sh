#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py r0 --beta 0.32 --gamma 0.10 > outputs/smoke_r0.txt
  python3 python/article_calculator.py rt --beta 0.32 --gamma 0.10 --susceptible 85000 --population 100000 > outputs/smoke_rt.txt
  python3 python/article_calculator.py doubling-time --growth-rate 0.22 > outputs/smoke_doubling_time.txt
  python3 python/article_calculator.py herd-threshold --r0 3.2 > outputs/smoke_herd_threshold.txt
  python3 python/article_calculator.py force-of-infection --beta 0.32 --infectious 100 --population 100000 > outputs/smoke_force_of_infection.txt
  python3 python/article_calculator.py incidence --beta 0.32 --susceptible 99900 --infectious 100 --population 100000 > outputs/smoke_incidence.txt
  python3 python/article_calculator.py sir-step --susceptible 99900 --infectious 100 --recovered 0 --beta 0.32 --gamma 0.10 --population 100000 > outputs/smoke_sir_step.txt
  python3 python/article_calculator.py governance-warning --context reported_cases > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R r0 0.32 0.10 > outputs/smoke_r_r0.txt
  Rscript r/article_calculator.R doubling-time 0.22 > outputs/smoke_r_doubling_time.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
