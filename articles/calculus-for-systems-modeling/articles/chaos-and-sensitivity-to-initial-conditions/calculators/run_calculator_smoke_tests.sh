#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-next --x 0.2 --r 3.9 > outputs/smoke_logistic_next.txt
  python3 python/article_calculator.py trajectory-divergence --x0 0.2 --perturbation 1e-8 --r 3.9 --steps 30 > outputs/smoke_trajectory_divergence.txt
  python3 python/article_calculator.py lyapunov-estimate --x0 0.2 --r 3.9 --burn-in 100 --sample-steps 1000 > outputs/smoke_lyapunov_estimate.txt
  python3 python/article_calculator.py forecast-horizon --initial-uncertainty 1e-8 --acceptable-error 1e-2 --lyapunov 0.5 > outputs/smoke_forecast_horizon.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-next 0.2 3.9 > outputs/smoke_r_logistic_next.txt
  Rscript r/article_calculator.R trajectory-divergence 0.2 1e-8 3.9 30 > outputs/smoke_r_trajectory_divergence.txt
  Rscript r/article_calculator.R forecast-horizon 1e-8 1e-2 0.5 > outputs/smoke_r_forecast_horizon.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
