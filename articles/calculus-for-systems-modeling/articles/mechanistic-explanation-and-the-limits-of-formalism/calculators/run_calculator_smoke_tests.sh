#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py mechanism-score --entities 1 --activities 1 --relations 1 --evidence 0 --scope 1 > outputs/smoke_mechanism_score.txt
  python3 python/article_calculator.py formalism-risk --parameter-meaning 0 --evidence-link 0 --validation-scope 1 --claim-boundary 0 > outputs/smoke_formalism_risk.txt
  python3 python/article_calculator.py claim-type --mechanism-evidence 1 --validation-data 0 --scenario-only 0 > outputs/smoke_claim_type.txt
  python3 python/article_calculator.py parameter-interpretation --source calibrated --has-unit 1 --has-range 1 > outputs/smoke_parameter_interpretation.txt
  python3 python/article_calculator.py black-box-risk --opaque-steps 2 --hidden-parameters 1 --missing-diagnostics 1 > outputs/smoke_black_box_risk.txt
  python3 python/article_calculator.py explanation-warning --pattern formal_precision > outputs/smoke_explanation_warning.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R mechanism-score 1 1 1 0 1 > outputs/smoke_r_mechanism_score.txt
  Rscript r/article_calculator.R formalism-risk 0 0 1 0 > outputs/smoke_r_formalism_risk.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
