#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py explicit-amplification --step-size 0.1 --eigenvalue -50 > outputs/smoke_explicit_amplification.txt
  python3 python/article_calculator.py implicit-amplification --step-size 0.1 --eigenvalue -50 > outputs/smoke_implicit_amplification.txt
  python3 python/article_calculator.py stiffness-ratio --eigenvalues -1,-50 > outputs/smoke_stiffness_ratio.txt
  python3 python/article_calculator.py stable-explicit-step-bound --eigenvalue -50 > outputs/smoke_stable_explicit_step_bound.txt
  python3 python/article_calculator.py method-comparison --step-size 0.1 --eigenvalue -50 > outputs/smoke_method_comparison.txt
  python3 python/article_calculator.py stiffness-warning-note --symptom step_rejection > outputs/smoke_stiffness_warning_note.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R explicit-amplification 0.1 -50 > outputs/smoke_r_explicit_amplification.txt
  Rscript r/article_calculator.R stiffness-ratio "-1,-50" > outputs/smoke_r_stiffness_ratio.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
