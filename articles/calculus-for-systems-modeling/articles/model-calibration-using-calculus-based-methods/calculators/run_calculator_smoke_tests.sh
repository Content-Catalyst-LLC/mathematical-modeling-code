#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py residual --observed 17.5 --predicted 17.2 > outputs/smoke_residual.txt
  python3 python/article_calculator.py squared-loss --residuals "1.0,-0.5,0.25" > outputs/smoke_squared_loss.txt
  python3 python/article_calculator.py logistic-prediction --time 8 --growth-rate 0.34 --carrying-capacity 105 > outputs/smoke_logistic_prediction.txt
  python3 python/article_calculator.py candidate-loss --growth-rate 0.34 --carrying-capacity 105 > outputs/smoke_candidate_loss.txt
  python3 python/article_calculator.py grid-search > outputs/smoke_grid_search.txt
  python3 python/article_calculator.py calibration-warning --pattern validation > outputs/smoke_calibration_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R residual 17.5 17.2 > outputs/smoke_r_residual.txt
  Rscript r/article_calculator.R candidate-loss 0.34 105 > outputs/smoke_r_candidate_loss.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
