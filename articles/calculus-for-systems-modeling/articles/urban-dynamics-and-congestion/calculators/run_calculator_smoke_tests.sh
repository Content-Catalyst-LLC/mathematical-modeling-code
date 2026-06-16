#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py traffic-flow --density 35 --free-flow-speed 60 --jam-density 140 > outputs/smoke_traffic_flow.txt
  python3 python/article_calculator.py critical-density --jam-density 140 > outputs/smoke_critical_density.txt
  python3 python/article_calculator.py queue-step --queue 0 --arrival-rate 2300 --service-rate 2000 --dt 0.01 > outputs/smoke_queue_step.txt
  python3 python/article_calculator.py bpr-travel-time --free-flow-time 20 --volume 2300 --capacity 2000 > outputs/smoke_bpr_travel_time.txt
  python3 python/article_calculator.py accessibility --opportunities 1000,500,250 --travel-times 10,25,45 --theta 0.08 > outputs/smoke_accessibility.txt
  python3 python/article_calculator.py induced-demand-step --volume 2300 --target-volume 2600 --adjustment-rate 0.15 --dt 1 > outputs/smoke_induced_demand_step.txt
  python3 python/article_calculator.py distributional-delay --delays 10,20,35 --weights 1,1.5,2 > outputs/smoke_distributional_delay.txt
  python3 python/article_calculator.py governance-warning --context equity > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R traffic-flow 35 60 140 > outputs/smoke_r_traffic_flow.txt
  Rscript r/article_calculator.R bpr-travel-time 20 2300 2000 > outputs/smoke_r_bpr_travel_time.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
