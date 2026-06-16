#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py logistic-point --time 10 --x0 10 --growth-rate 0.35 --carrying-capacity 100 > outputs/smoke_logistic_point.txt
  python3 python/article_calculator.py trajectory-series --x0 10 --growth-rate 0.35 --carrying-capacity 100 > outputs/smoke_trajectory_series.txt
  python3 python/article_calculator.py scenario-comparison > outputs/smoke_scenario_comparison.txt
  python3 python/article_calculator.py figure-audit-record --visual-type trajectory_plot > outputs/smoke_figure_audit_record.txt
  python3 python/article_calculator.py visualization-risk-score --axis-risk 2 --uncertainty-risk 3 --smoothing-risk 1 --metadata-risk 2 > outputs/smoke_visualization_risk_score.txt
  python3 python/article_calculator.py uncertainty-band-note --band-type scenario_range > outputs/smoke_uncertainty_band_note.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R logistic-point 10 10 0.35 100 > outputs/smoke_r_logistic_point.txt
  Rscript r/article_calculator.R visualization-risk-score 2 3 1 2 > outputs/smoke_r_visualization_risk_score.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
