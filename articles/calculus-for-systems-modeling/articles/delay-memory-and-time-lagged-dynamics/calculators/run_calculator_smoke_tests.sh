#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py delay-steps --delay 5 --dt 0.1 > outputs/smoke_delay_steps.txt
  python3 python/article_calculator.py delayed-lookup --initial-state 80 --delay-steps 50 --step 10 > outputs/smoke_delayed_lookup.txt
  python3 python/article_calculator.py memory-kernel --age 3 --decay-rate 0.4 > outputs/smoke_memory_kernel.txt
  python3 python/article_calculator.py delayed-adjustment --initial-state 80 --target 100 --adjustment-rate 0.2 --delay 5 --dt 0.1 --steps 300 > outputs/smoke_delayed_adjustment.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R delay-steps 5 0.1 > outputs/smoke_r_delay_steps.txt
  Rscript r/article_calculator.R memory-kernel 3 0.4 > outputs/smoke_r_memory_kernel.txt
  Rscript r/article_calculator.R delayed-adjustment 80 100 0.2 5 0.1 300 > outputs/smoke_r_delayed_adjustment.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
