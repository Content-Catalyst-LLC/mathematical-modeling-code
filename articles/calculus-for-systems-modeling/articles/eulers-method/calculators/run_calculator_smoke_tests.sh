#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py euler-step --t 0 --y 100 --h 0.1 --decay-rate 0.35 > outputs/smoke_euler_step.txt
  python3 python/article_calculator.py decay-audit --y0 100 --decay-rate 0.35 --h 0.1 --stop-time 20 > outputs/smoke_decay_audit.txt
  python3 python/article_calculator.py step-size-comparison --y0 100 --decay-rate 0.35 --stop-time 20 > outputs/smoke_step_size_comparison.txt
  python3 python/article_calculator.py stability-check --h 0.1 --decay-rate 0.35 > outputs/smoke_stability_check.txt
  python3 python/article_calculator.py logistic-step --y 10 --r 0.2 --k 100 --h 1 > outputs/smoke_logistic_step.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R euler-step 0 100 0.1 0.35 > outputs/smoke_r_euler_step.txt
  Rscript r/article_calculator.R stability-check 0.1 0.35 > outputs/smoke_r_stability_check.txt
  Rscript r/article_calculator.R logistic-step 10 0.2 100 1 > outputs/smoke_r_logistic_step.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
