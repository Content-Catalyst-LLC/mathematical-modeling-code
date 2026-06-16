#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py validate-parameter --name growth_rate --value 0.35 --minimum 0 > outputs/smoke_validate_parameter.txt
  python3 python/article_calculator.py logistic-step --stock 10 --growth-rate 0.35 --carrying-capacity 100 --time-step 0.25 > outputs/smoke_logistic_step.txt
  python3 python/article_calculator.py simulate-final --growth-rate 0.35 --carrying-capacity 100 > outputs/smoke_simulate_final.txt
  python3 python/article_calculator.py diagnostic-status --review-required false > outputs/smoke_diagnostic_status.txt
  python3 python/article_calculator.py record-completeness --present 7 --required 7 > outputs/smoke_record_completeness.txt
  python3 python/article_calculator.py type-safety-warning --pattern empirical_validity > outputs/smoke_type_safety_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R validate-parameter growth_rate 0.35 0 > outputs/smoke_r_validate_parameter.txt
  Rscript r/article_calculator.R logistic-step 10 0.35 100 0.25 > outputs/smoke_r_logistic_step.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
