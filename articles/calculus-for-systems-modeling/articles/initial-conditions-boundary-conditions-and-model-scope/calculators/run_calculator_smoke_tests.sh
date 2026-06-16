#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-final --initial-stock 10 --growth-rate 0.35 --carrying-capacity 100 --horizon 20 > outputs/smoke_logistic_final.txt
  python3 python/article_calculator.py initial-condition-effect --low 5 --baseline 10 --high 20 > outputs/smoke_initial_condition_effect.txt
  python3 python/article_calculator.py scope-check --value 0.35 --lower 0.1 --upper 0.6 > outputs/smoke_scope_check.txt
  python3 python/article_calculator.py boundary-warning --boundary-type no_flux > outputs/smoke_boundary_warning.txt
  python3 python/article_calculator.py horizon-warning --horizon 20 --maximum-supported 20 > outputs/smoke_horizon_warning.txt
  python3 python/article_calculator.py condition-scope-warning --pattern claim_boundary > outputs/smoke_condition_scope_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-final 10 0.35 100 20 > outputs/smoke_r_logistic_final.txt
  Rscript r/article_calculator.R scope-check 0.35 0.1 0.6 > outputs/smoke_r_scope_check.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
