#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py diffusion-ratio --diffusivity 0.08 --dt 0.2 --dx 1 > outputs/smoke_diffusion_ratio.txt
  python3 python/article_calculator.py forward-difference --f-current 1 --f-next 1.2 --dx 0.1 > outputs/smoke_forward_difference.txt
  python3 python/article_calculator.py central-difference --f-previous 1 --f-next 1.2 --dx 0.1 > outputs/smoke_central_difference.txt
  python3 python/article_calculator.py second-central-difference --f-previous 1 --f-current 1.2 --f-next 1.4 --dx 0.1 > outputs/smoke_second_central_difference.txt
  python3 python/article_calculator.py explicit-diffusion-step --left 0 --center 1 --right 0 --ratio 0.016 > outputs/smoke_explicit_diffusion_step.txt
  python3 python/article_calculator.py stability-check --diffusivity 0.08 --dt 0.2 --dx 1 > outputs/smoke_stability_check.txt
  python3 python/article_calculator.py diffusion-simulation --grid-points 61 --diffusivity 0.08 --dx 1 --dt 0.2 --steps 120 > outputs/smoke_diffusion_simulation.txt
fi
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R diffusion-ratio 0.08 0.2 1 > outputs/smoke_r_diffusion_ratio.txt
  Rscript r/article_calculator.R central-difference 1 1.2 0.1 > outputs/smoke_r_central_difference.txt
  Rscript r/article_calculator.R second-central-difference 1 1.2 1.4 0.1 > outputs/smoke_r_second_central_difference.txt
  Rscript r/article_calculator.R explicit-diffusion-step 0 1 0 0.016 > outputs/smoke_r_explicit_diffusion_step.txt
  Rscript r/article_calculator.R stability-check 0.08 0.2 1 > outputs/smoke_r_stability_check.txt
fi
echo "[calculator smoke] done"
