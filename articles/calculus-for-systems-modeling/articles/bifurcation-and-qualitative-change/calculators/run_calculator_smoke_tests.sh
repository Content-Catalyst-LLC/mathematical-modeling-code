#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "[calculator smoke] Python calculators"
if command -v python3 >/dev/null 2>&1; then
  python3 python/article_calculator.py saddle-node-equilibria --mu 4 > outputs/smoke_saddle_node_equilibria.txt
  python3 python/article_calculator.py transcritical-equilibria --mu 2 > outputs/smoke_transcritical_equilibria.txt
  python3 python/article_calculator.py pitchfork-equilibria --mu 4 > outputs/smoke_pitchfork_equilibria.txt
  python3 python/article_calculator.py classify-derivative --derivative-value -2 > outputs/smoke_classify_derivative.txt
  python3 python/article_calculator.py saddle-node-sweep --mu-min -2 --mu-max 4 --mu-step 0.5 > outputs/smoke_saddle_node_sweep.txt
else
  echo "python3 not found; skipping Python calculator smoke tests"
fi

echo "[calculator smoke] R calculators"
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/article_calculator.R saddle-node-equilibria 4 > outputs/smoke_r_saddle_node_equilibria.txt
  Rscript r/article_calculator.R transcritical-equilibria 2 > outputs/smoke_r_transcritical_equilibria.txt
  Rscript r/article_calculator.R pitchfork-equilibria 4 > outputs/smoke_r_pitchfork_equilibria.txt
  Rscript r/article_calculator.R classify-derivative -2 > outputs/smoke_r_classify_derivative.txt
else
  echo "Rscript not found; skipping R calculator smoke tests"
fi

echo "[calculator smoke] done"
