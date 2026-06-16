#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py smoothness-risk --breaks 1 --thresholds 1 --heterogeneity 1 --solver-warnings 0 > outputs/smoke_smoothness_risk.txt
  python3 python/article_calculator.py threshold-warning --value 0.92 --critical 1.0 --margin 0.1 > outputs/smoke_threshold_warning.txt
  python3 python/article_calculator.py equilibrium-bias --has-equilibrium 1 --path-analyzed 0 --stability-tested 0 > outputs/smoke_equilibrium_bias.txt
  python3 python/article_calculator.py aggregation-risk --mean 50 --maximum 95 --threshold 80 > outputs/smoke_aggregation_risk.txt
  python3 python/article_calculator.py solver-risk --step-check 0 --convergence-flag 1 --stiffness-warning 1 > outputs/smoke_solver_risk.txt
  python3 python/article_calculator.py continuous-model-warning --pattern false_smoothness > outputs/smoke_continuous_model_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R smoothness-risk 1 1 1 0 > outputs/smoke_r_smoothness_risk.txt
  Rscript r/article_calculator.R aggregation-risk 50 95 80 > outputs/smoke_r_aggregation_risk.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
