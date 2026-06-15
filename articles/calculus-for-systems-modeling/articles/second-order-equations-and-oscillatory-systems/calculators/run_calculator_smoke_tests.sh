#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py damping-classification --damping-ratio 0.2 > outputs/smoke_damping_classification.txt
  python3 python/article_calculator.py period --natural-frequency 1.0 > outputs/smoke_period.txt
  python3 python/article_calculator.py acceleration --position 1 --velocity 0 --time 0 --damping-ratio 0.2 --natural-frequency 1 --forcing-amplitude 0 --forcing-frequency 1 > outputs/smoke_acceleration.txt
  python3 python/article_calculator.py euler-step --position 1 --velocity 0 --dt 0.02 --damping-ratio 0.2 --natural-frequency 1 --forcing-amplitude 0 --forcing-frequency 1 > outputs/smoke_euler_step.txt
  python3 python/article_calculator.py simulate-oscillator --scenario underdamped --position 1 --velocity 0 --damping-ratio 0.2 --natural-frequency 1 --forcing-amplitude 0 --forcing-frequency 1 --dt 0.02 --steps 50 > outputs/smoke_simulate_oscillator.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R damping-classification 0.2 > outputs/smoke_r_damping_classification.txt
  Rscript r/article_calculator.R period 1 > outputs/smoke_r_period.txt
  Rscript r/article_calculator.R acceleration 1 0 0 0.2 1 0 1 > outputs/smoke_r_acceleration.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
