#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-regeneration --stock 500 --r 0.18 --k 1000 > outputs/smoke_logistic_regeneration.txt
  python3 python/article_calculator.py msy --r 0.18 --k 1000 > outputs/smoke_msy.txt
  python3 python/article_calculator.py depletion-condition --regeneration 35 --harvest 45 --loss 5 > outputs/smoke_depletion_condition.txt
  python3 python/article_calculator.py simulate-renewable --stock0 600 --harvest 35 --steps 800 > outputs/smoke_simulate_renewable.txt
  python3 python/article_calculator.py simulate-nonrenewable --stock0 600 --extraction-rate 30 --steps 800 > outputs/smoke_simulate_nonrenewable.txt
  python3 python/article_calculator.py threshold-risk --stock 150 --threshold 180 > outputs/smoke_threshold_risk.txt
  python3 python/article_calculator.py efficiency-rebound --demand 60 --efficiency-gain 0.15 --rebound-factor 0.6 > outputs/smoke_efficiency_rebound.txt
  python3 python/article_calculator.py governance-warning --context msy > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-regeneration 500 0.18 1000 > outputs/smoke_r_logistic_regeneration.txt
  Rscript r/article_calculator.R msy 0.18 1000 > outputs/smoke_r_msy.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
