#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py scalar-field --x 1 --y 1 > outputs/smoke_scalar_field.txt
  python3 python/article_calculator.py vector-field --x 1 --y 1 > outputs/smoke_vector_field.txt
  python3 python/article_calculator.py gradient --x 1 --y 1 > outputs/smoke_gradient.txt
  python3 python/article_calculator.py gradient-magnitude --x 1 --y 1 > outputs/smoke_gradient_magnitude.txt
  python3 python/article_calculator.py divergence --x 1 --y 1 > outputs/smoke_divergence.txt
  python3 python/article_calculator.py curl-2d --x 1 --y 1 > outputs/smoke_curl_2d.txt
  python3 python/article_calculator.py finite-difference-gradient --x 1 --y 1 --h 0.01 > outputs/smoke_fd_gradient.txt
  python3 python/article_calculator.py finite-difference-divergence --x 1 --y 1 --h 0.01 > outputs/smoke_fd_divergence.txt
  python3 python/article_calculator.py finite-difference-curl --x 1 --y 1 --h 0.01 > outputs/smoke_fd_curl.txt
  python3 python/article_calculator.py field-audit --step 0.25 > outputs/smoke_field_audit.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R scalar-field 1 1 > outputs/smoke_r_scalar_field.txt
  Rscript r/article_calculator.R gradient 1 1 > outputs/smoke_r_gradient.txt
  Rscript r/article_calculator.R curl-2d 1 1 > outputs/smoke_r_curl.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
