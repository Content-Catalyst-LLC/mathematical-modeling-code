#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py equilibrium-temperature --forcing 3.7 --feedback 1.2 > outputs/smoke_equilibrium_temperature.txt
  python3 python/article_calculator.py adjustment-time --heat-capacity 10 --feedback 1.2 > outputs/smoke_adjustment_time.txt
  python3 python/article_calculator.py absorbed-solar --solar-constant 1361 --albedo 0.30 > outputs/smoke_absorbed_solar.txt
  python3 python/article_calculator.py one-layer-step --temperature 0 --forcing 3.7 --feedback 1.2 --heat-capacity 10 > outputs/smoke_one_layer_step.txt
  python3 python/article_calculator.py surface-partition --net-radiation 500 --sensible 120 --latent 300 --ground 40 > outputs/smoke_surface_partition.txt
  python3 python/article_calculator.py building-step --temperature 20 --heat-capacity 1000 --q-heat 300 --q-solar 150 --q-internal 80 --q-loss 420 > outputs/smoke_building_step.txt
  python3 python/article_calculator.py governance-warning --context boundary > outputs/smoke_governance_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi
echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R equilibrium-temperature 3.7 1.2 > outputs/smoke_r_equilibrium_temperature.txt
  Rscript r/article_calculator.R adjustment-time 10 1.2 > outputs/smoke_r_adjustment_time.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi
echo "[calculator smoke] done"
