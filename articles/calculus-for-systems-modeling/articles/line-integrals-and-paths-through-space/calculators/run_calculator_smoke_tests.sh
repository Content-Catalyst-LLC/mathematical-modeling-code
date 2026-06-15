#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py path-point --t 1 > outputs/smoke_path_point.txt
  python3 python/article_calculator.py scalar-field --x 1 --y 2 > outputs/smoke_scalar_field.txt
  python3 python/article_calculator.py vector-field --x 1 --y 2 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py segment-length --x1 0 --y1 0 --x2 3 --y2 4 > outputs/smoke_segment_length.txt
  python3 python/article_calculator.py scalar-segment --x 1 --y 2 --segment-length 0.5 > outputs/smoke_scalar_segment.txt
  python3 python/article_calculator.py vector-segment --x 1 --y 2 --dx 0.25 --dy 0.1 > outputs/smoke_vector_segment.txt
  python3 python/article_calculator.py line-audit --step 0.25 > outputs/smoke_line_audit.txt
  python3 python/article_calculator.py path-length --step 0.25 > outputs/smoke_path_length.txt
  python3 python/article_calculator.py scalar-line-approx --step 0.25 > outputs/smoke_scalar_line_approx.txt
  python3 python/article_calculator.py vector-line-approx --step 0.25 > outputs/smoke_vector_line_approx.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R path-point 1 > outputs/smoke_r_path_point.txt
  Rscript r/article_calculator.R segment-length 0 0 3 4 > outputs/smoke_r_segment_length.txt
  Rscript r/article_calculator.R scalar-field 1 2 > outputs/smoke_r_scalar_field.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
