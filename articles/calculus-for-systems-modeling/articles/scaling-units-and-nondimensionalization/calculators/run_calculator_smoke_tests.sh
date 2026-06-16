#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py scale-value --value 40 --scale 100 > outputs/smoke_scale_value.txt
  python3 python/article_calculator.py unscale-value --dimensionless 0.4 --scale 100 > outputs/smoke_unscale_value.txt
  python3 python/article_calculator.py rate-conversion --rate 0.01 --from-unit day --to-unit year > outputs/smoke_rate_conversion.txt
  python3 python/article_calculator.py logistic-nondimensional --stock 40 --capacity 100 --time 20 --growth-rate 0.35 > outputs/smoke_logistic_nondimensional.txt
  python3 python/article_calculator.py conditioning-ratio --largest 1000000 --smallest 0.001 > outputs/smoke_conditioning_ratio.txt
  python3 python/article_calculator.py scaling-warning --pattern empirical_validity > outputs/smoke_scaling_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R scale-value 40 100 > outputs/smoke_r_scale_value.txt
  Rscript r/article_calculator.R logistic-nondimensional 40 100 20 0.35 > outputs/smoke_r_logistic_nondimensional.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
