#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py diffusion-ratio --diffusivity 0.08 --dt 0.2 --dx 1 > outputs/smoke_diffusion_ratio.txt
  python3 python/article_calculator.py transport-ratio --velocity 0.4 --dt 0.2 --dx 1 > outputs/smoke_transport_ratio.txt
  python3 python/article_calculator.py advection-diffusion-step --left 0 --center 1 --right 0 --diffusion-ratio 0.016 --transport-ratio 0.08 > outputs/smoke_advection_diffusion_step.txt
  python3 python/article_calculator.py advection-diffusion-simulation --grid-points 61 --diffusivity 0.08 --velocity 0.4 --dx 1 --dt 0.2 --steps 120 > outputs/smoke_advection_diffusion_simulation.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R diffusion-ratio 0.08 0.2 1 > outputs/smoke_r_diffusion_ratio.txt
  Rscript r/article_calculator.R transport-ratio 0.4 0.2 1 > outputs/smoke_r_transport_ratio.txt
  Rscript r/article_calculator.R advection-diffusion-step 0 1 0 0.016 0.08 > outputs/smoke_r_advection_diffusion_step.txt
  Rscript r/article_calculator.R advection-diffusion-simulation 61 0.08 0.4 1 0.2 120 > outputs/smoke_r_advection_diffusion_simulation.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
