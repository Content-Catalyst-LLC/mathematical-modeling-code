#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py absolute-error --numeric 0.912 --exact 0.9119 > outputs/smoke_absolute_error.txt
  python3 python/article_calculator.py relative-error --numeric 0.912 --exact 0.9119 > outputs/smoke_relative_error.txt
  python3 python/article_calculator.py euler-stability-factor --step-size 0.1 --eigenvalue -1 > outputs/smoke_euler_stability_factor.txt
  python3 python/article_calculator.py convergence-ratio --previous-error 0.01 --current-error 0.000625 > outputs/smoke_convergence_ratio.txt
  python3 python/article_calculator.py rk4-final-error --step-size 0.5 > outputs/smoke_rk4_final_error.txt
  python3 python/article_calculator.py refinement-table > outputs/smoke_refinement_table.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R absolute-error 0.912 0.9119 > outputs/smoke_r_absolute_error.txt
  Rscript r/article_calculator.R convergence-ratio 0.01 0.000625 > outputs/smoke_r_convergence_ratio.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
