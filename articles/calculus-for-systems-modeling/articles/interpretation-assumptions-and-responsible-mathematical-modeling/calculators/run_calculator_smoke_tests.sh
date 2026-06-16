#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py purpose-fit --teaching 1 --exploratory 0 --predictive 0 --decision-support 0 > outputs/smoke_purpose_fit.txt
  python3 python/article_calculator.py assumption-risk --hidden-assumptions 2 --normative-assumptions 1 --solver-undocumented 1 > outputs/smoke_assumption_risk.txt
  python3 python/article_calculator.py claim-boundary --purpose predictive --validated 0 --uncertainty-recorded 1 --scope-recorded 1 > outputs/smoke_claim_boundary.txt
  python3 python/article_calculator.py parameter-evidence --has-unit 1 --has-source 1 --has-range 0 --has-uncertainty 0 > outputs/smoke_parameter_evidence.txt
  python3 python/article_calculator.py communication-risk --overprecision 1 --scenario-confusion 1 --hidden-values 0 --audience-mismatch 1 > outputs/smoke_communication_risk.txt
  python3 python/article_calculator.py responsibility-warning --pattern claim_boundary > outputs/smoke_responsibility_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R assumption-risk 2 1 1 > outputs/smoke_r_assumption_risk.txt
  Rscript r/article_calculator.R parameter-evidence 1 1 0 0 > outputs/smoke_r_parameter_evidence.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
