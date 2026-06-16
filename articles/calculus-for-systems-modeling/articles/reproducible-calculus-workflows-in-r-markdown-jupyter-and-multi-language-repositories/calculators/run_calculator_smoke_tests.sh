#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py artifact-count --source 2 --generated 4 > outputs/smoke_artifact_count.txt
  python3 python/article_calculator.py clean-run-status --expected 6 --found 6 > outputs/smoke_clean_run_status.txt
  python3 python/article_calculator.py output-register-score --documented 6 --total 6 > outputs/smoke_output_register_score.txt
  python3 python/article_calculator.py notebook-drift-risk --executed-out-of-order true > outputs/smoke_notebook_drift_risk.txt
  python3 python/article_calculator.py governance-queue-count --warnings 3 > outputs/smoke_governance_queue_count.txt
  python3 python/article_calculator.py reproducibility-warning --pattern validity > outputs/smoke_reproducibility_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R artifact-count 2 4 > outputs/smoke_r_artifact_count.txt
  Rscript r/article_calculator.R clean-run-status 6 6 > outputs/smoke_r_clean_run_status.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
