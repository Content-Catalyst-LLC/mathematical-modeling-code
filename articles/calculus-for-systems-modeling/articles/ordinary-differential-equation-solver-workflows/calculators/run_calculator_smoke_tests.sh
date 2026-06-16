#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py rk4-solver-step --t 0 --y 100 --h 0.5 --decay-rate 0.35 > outputs/smoke_rk4_solver_step.txt
  python3 python/article_calculator.py solver-benchmark --y0 100 --decay-rate 0.35 --h 0.5 --stop-time 20 > outputs/smoke_solver_benchmark.txt
  python3 python/article_calculator.py step-size-comparison --y0 100 --decay-rate 0.35 --stop-time 20 > outputs/smoke_step_size_comparison.txt
  python3 python/article_calculator.py tolerance-threshold --atol 1e-8 --rtol 1e-6 --state 100 > outputs/smoke_tolerance_threshold.txt
  python3 python/article_calculator.py stiffness-indicator --fast-rate 100 --slow-rate 1 > outputs/smoke_stiffness_indicator.txt
  python3 python/article_calculator.py solver-config-record --method fixed_step_rk4 --h 0.5 --atol 1e-8 --rtol 1e-6 > outputs/smoke_solver_config_record.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R rk4-solver-step 0 100 0.5 0.35 > outputs/smoke_r_rk4_solver_step.txt
  Rscript r/article_calculator.R tolerance-threshold 1e-8 1e-6 100 > outputs/smoke_r_tolerance_threshold.txt
  Rscript r/article_calculator.R stiffness-indicator 100 1 > outputs/smoke_r_stiffness_indicator.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
