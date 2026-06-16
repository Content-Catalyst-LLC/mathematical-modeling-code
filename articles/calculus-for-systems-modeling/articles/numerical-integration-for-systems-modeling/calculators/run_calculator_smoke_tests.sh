#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py left-rectangle --rate-left 3.2 --h 0.25 > outputs/smoke_left_rectangle.txt
  python3 python/article_calculator.py trapezoid-step --rate-left 3 --rate-right 4 --h 0.25 > outputs/smoke_trapezoid_step.txt
  python3 python/article_calculator.py simpson-one-third --f0 2 --f1 3 --f2 2 --h 0.5 > outputs/smoke_simpson_one_third.txt
  python3 python/article_calculator.py benchmark-audit --start 0 --stop 10 --h 0.1 > outputs/smoke_benchmark_audit.txt
  python3 python/article_calculator.py conservation-check --initial-stock 100 --final-stock 130 --integrated-inflow 50 --integrated-outflow 20 > outputs/smoke_conservation_check.txt
fi
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R left-rectangle 3.2 0.25 > outputs/smoke_r_left_rectangle.txt
  Rscript r/article_calculator.R trapezoid-step 3 4 0.25 > outputs/smoke_r_trapezoid_step.txt
  Rscript r/article_calculator.R simpson-one-third 2 3 2 0.5 > outputs/smoke_r_simpson_one_third.txt
  Rscript r/article_calculator.R conservation-check 100 130 50 20 > outputs/smoke_r_conservation_check.txt
fi
echo "[calculator smoke] done"
