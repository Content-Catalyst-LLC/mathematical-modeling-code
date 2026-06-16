#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-derivative > outputs/smoke_logistic_derivative.txt
  python3 python/article_calculator.py logistic-equilibria > outputs/smoke_logistic_equilibria.txt
  python3 python/article_calculator.py capacity-limit > outputs/smoke_capacity_limit.txt
  python3 python/article_calculator.py jacobian-record > outputs/smoke_jacobian_record.txt
  python3 python/article_calculator.py domain-warning --expression "r*x*(1 - x/K)" > outputs/smoke_domain_warning.txt
  python3 python/article_calculator.py symbolic-inspection-report > outputs/smoke_symbolic_inspection_report.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-derivative > outputs/smoke_r_logistic_derivative.txt
  Rscript r/article_calculator.R logistic-equilibria > outputs/smoke_r_logistic_equilibria.txt
  Rscript r/article_calculator.R capacity-limit > outputs/smoke_r_capacity_limit.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
