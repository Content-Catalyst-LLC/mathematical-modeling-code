#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py co2-forcing --concentration 560 --baseline 280 > outputs/smoke_co2_forcing.txt
  python3 python/article_calculator.py one-box --forcing 3.7 --feedback 1.2 --heat-capacity 8 --time 80 > outputs/smoke_one_box.txt
  python3 python/article_calculator.py ecs --forcing 3.7 --feedback 1.2 > outputs/smoke_ecs.txt
  python3 python/article_calculator.py feedback-sensitivity --forcing 3.7 --feedback 1.2 > outputs/smoke_feedback_sensitivity.txt
  python3 python/article_calculator.py two-box --forcing 3.7 --feedback 1.2 --surface-capacity 8 --deep-capacity 100 --exchange 0.7 --time 80 > outputs/smoke_two_box.txt
  python3 python/article_calculator.py carbon-feedback --forcing 3.7 --temperature 3 --beta-carbon 0.15 > outputs/smoke_carbon_feedback.txt
  python3 python/article_calculator.py sign-warning --convention restoring_positive > outputs/smoke_sign_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R co2-forcing 560 280 > outputs/smoke_r_co2_forcing.txt
  Rscript r/article_calculator.R one-box 3.7 1.2 8 80 > outputs/smoke_r_one_box.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
