#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py solve --target 12 > outputs/smoke_solve.txt
  python3 python/article_calculator.py objective --x 8 --y 4 > outputs/smoke_objective.txt
  python3 python/article_calculator.py constraint --x 8 --y 4 --target 12 > outputs/smoke_constraint.txt
  python3 python/article_calculator.py gradients --x 8 --y 4 > outputs/smoke_gradients.txt
  python3 python/article_calculator.py stationarity --target 12 > outputs/smoke_stationarity.txt
  python3 python/article_calculator.py multiplier --target 12 > outputs/smoke_multiplier.txt
  python3 python/article_calculator.py shadow-value --target 12 --delta 0.1 > outputs/smoke_shadow_value.txt
  python3 python/article_calculator.py feasibility --x 8 --y 4 --target 12 > outputs/smoke_feasibility.txt
  python3 python/article_calculator.py active-status --value 12 --limit 12 > outputs/smoke_active_status.txt
  python3 python/article_calculator.py tradeoff-scan --targets 12 18 24 > outputs/smoke_tradeoff_scan.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R solve 12 > outputs/smoke_r_solve.txt
  Rscript r/article_calculator.R multiplier 12 > outputs/smoke_r_multiplier.txt
  Rscript r/article_calculator.R stationarity 12 > outputs/smoke_r_stationarity.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
