#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py rk4-step --t 0 --y 100 --h 0.5 --decay-rate 0.35 > outputs/smoke_rk4_step.txt
  python3 python/article_calculator.py midpoint-step --t 0 --y 100 --h 0.5 --decay-rate 0.35 > outputs/smoke_midpoint_step.txt
  python3 python/article_calculator.py heun-step --t 0 --y 100 --h 0.5 --decay-rate 0.35 > outputs/smoke_heun_step.txt
  python3 python/article_calculator.py stage-values --t 0 --y 100 --h 0.5 --decay-rate 0.35 > outputs/smoke_stage_values.txt
  python3 python/article_calculator.py euler-vs-rk4-audit --y0 100 --decay-rate 0.35 --h 0.5 --stop-time 20 > outputs/smoke_euler_vs_rk4_audit.txt
  python3 python/article_calculator.py step-size-comparison --y0 100 --decay-rate 0.35 --stop-time 20 > outputs/smoke_step_size_comparison.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R rk4-step 0 100 0.5 0.35 > outputs/smoke_r_rk4_step.txt
  Rscript r/article_calculator.R midpoint-step 0 100 0.5 0.35 > outputs/smoke_r_midpoint_step.txt
  Rscript r/article_calculator.R heun-step 0 100 0.5 0.35 > outputs/smoke_r_heun_step.txt
  Rscript r/article_calculator.R stage-values 0 100 0.5 0.35 > outputs/smoke_r_stage_values.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
