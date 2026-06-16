#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-final --growth-rate 0.35 --carrying-capacity 100 > outputs/smoke_logistic_final.txt
  python3 python/article_calculator.py local-sensitivity --parameter growth_rate > outputs/smoke_local_sensitivity.txt
  python3 python/article_calculator.py elasticity --parameter carrying_capacity > outputs/smoke_elasticity.txt
  python3 python/article_calculator.py grid-sweep > outputs/smoke_grid_sweep.txt
  python3 python/article_calculator.py robustness-range --low 80 --high 100 > outputs/smoke_robustness_range.txt
  python3 python/article_calculator.py fragility-note --pattern threshold > outputs/smoke_fragility_note.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-final 0.35 100 > outputs/smoke_r_logistic_final.txt
  Rscript r/article_calculator.R local-sensitivity growth_rate > outputs/smoke_r_local_sensitivity.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
