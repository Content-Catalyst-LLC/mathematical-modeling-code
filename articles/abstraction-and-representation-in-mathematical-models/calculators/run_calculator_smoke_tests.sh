#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Python calculator smoke checks"
python3 python/model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
python3 python/model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 2 --method simpson --n 100
python3 python/model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 5 | head
python3 python/model_calculator.py finite-difference --values "1,1.4,2.1,3.2" --h 0.5 | head
python3 python/model_calculator.py sensitivity --expr "r*x*(1-x/k)" --param r --min 0.05 --max 0.5 --count 4 --x 25 --params "k=100" | head

if command -v Rscript >/dev/null 2>&1; then
  echo "R calculator smoke checks"
  Rscript r/model_calculator.R derivative --expr "sin(x)*exp(-x)" --x 1.5
  Rscript r/model_calculator.R integral --expr "x^2 + sin(x)" --a 0 --b 2 --method simpson --n 100
  Rscript r/model_calculator.R logistic --r 0.2 --k 100 --y0 10 --dt 0.1 --steps 5 | head
else
  echo "Rscript not found; skipping R smoke checks"
fi
