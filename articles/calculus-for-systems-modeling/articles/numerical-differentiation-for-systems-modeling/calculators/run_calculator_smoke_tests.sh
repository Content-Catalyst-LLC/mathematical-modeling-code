#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py forward-difference --f-current 1 --f-next 1.12 --h 0.1 > outputs/smoke_forward_difference.txt
  python3 python/article_calculator.py backward-difference --f-previous 0.89 --f-current 1 --h 0.1 > outputs/smoke_backward_difference.txt
  python3 python/article_calculator.py central-difference --f-previous 0.89 --f-next 1.12 --h 0.1 > outputs/smoke_central_difference.txt
  python3 python/article_calculator.py second-central-difference --f-previous 0.89 --f-current 1 --f-next 1.12 --h 0.1 > outputs/smoke_second_central_difference.txt
  python3 python/article_calculator.py benchmark-audit --start 0 --stop 10 --h 0.1 > outputs/smoke_benchmark_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R forward-difference 1 1.12 0.1 > outputs/smoke_r_forward_difference.txt
  Rscript r/article_calculator.R central-difference 0.89 1.12 0.1 > outputs/smoke_r_central_difference.txt
  Rscript r/article_calculator.R second-central-difference 0.89 1 1.12 0.1 > outputs/smoke_r_second_central_difference.txt
  Rscript r/article_calculator.R benchmark-audit 0 10 0.1 > outputs/smoke_r_benchmark_audit.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
