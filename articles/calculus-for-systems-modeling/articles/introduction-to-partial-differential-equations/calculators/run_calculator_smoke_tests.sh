#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py stability-ratio --diffusivity 0.1 --dt 0.25 --dx 1 > outputs/smoke_stability_ratio.txt
  python3 python/article_calculator.py diffusion-step --left 0 --center 1 --right 0 --stability-ratio 0.025 > outputs/smoke_diffusion_step.txt
  python3 python/article_calculator.py explicit-diffusion --grid-points 51 --diffusivity 0.1 --dx 1 --dt 0.25 --steps 100 > outputs/smoke_explicit_diffusion.txt
  python3 python/article_calculator.py boundary-condition-note --kind dirichlet > outputs/smoke_boundary_condition_note.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R stability-ratio 0.1 0.25 1 > outputs/smoke_r_stability_ratio.txt
  Rscript r/article_calculator.R diffusion-step 0 1 0 0.025 > outputs/smoke_r_diffusion_step.txt
  Rscript r/article_calculator.R explicit-diffusion 51 0.1 1 0.25 100 > outputs/smoke_r_explicit_diffusion.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
