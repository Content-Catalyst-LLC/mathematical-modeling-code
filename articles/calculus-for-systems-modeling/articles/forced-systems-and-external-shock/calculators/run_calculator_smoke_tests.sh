#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py impulse-shock --time 10 --shock-time 10 --shock-magnitude -30 > outputs/smoke_impulse_shock.txt
  python3 python/article_calculator.py step-forcing --time 12 --start-time 10 --level 5 > outputs/smoke_step_forcing.txt
  python3 python/article_calculator.py periodic-forcing --time 1.57079632679 --amplitude 2 --angular-frequency 1 --phase 0 > outputs/smoke_periodic_forcing.txt
  python3 python/article_calculator.py forced-recovery --initial-state 100 --equilibrium 100 --recovery-rate 0.15 --shock-time 10 --shock-magnitude -30 --dt 0.1 --steps 300 > outputs/smoke_forced_recovery.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R impulse-shock 10 10 -30 > outputs/smoke_r_impulse_shock.txt
  Rscript r/article_calculator.R step-forcing 12 10 5 > outputs/smoke_r_step_forcing.txt
  Rscript r/article_calculator.R periodic-forcing 1.57079632679 2 1 0 > outputs/smoke_r_periodic_forcing.txt
  Rscript r/article_calculator.R forced-recovery 100 100 0.15 10 -30 0.1 300 > outputs/smoke_r_forced_recovery.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
