#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py utilization --arrival 95 --capacity 100 > outputs/smoke_utilization.txt
  python3 python/article_calculator.py delay --utilization 0.95 > outputs/smoke_delay.txt
  python3 python/article_calculator.py queue-step --queue 20 --arrival 95 --service 100 --dt 1 > outputs/smoke_queue_step.txt
  python3 python/article_calculator.py bottleneck --capacities 140,120,90,130 > outputs/smoke_bottleneck.txt
  python3 python/article_calculator.py buffer --inflow 120 --outflow 100 --capacity 300 --time 24 > outputs/smoke_buffer.txt
  python3 python/article_calculator.py capacity-decay --initial-capacity 100 --maintenance 1.5 --decay-rate 0.03 --years 20 > outputs/smoke_capacity_decay.txt
  python3 python/article_calculator.py resilience --delivered 80 --required 100 > outputs/smoke_resilience.txt
  python3 python/article_calculator.py governance-warning --context nominal_capacity > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R utilization 95 100 > outputs/smoke_r_utilization.txt
  Rscript r/article_calculator.R delay 0.95 > outputs/smoke_r_delay.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
