# Article Calculators

Reusable calculator layer for **Case Study: Modeling Population Dynamics**.

## Python examples

```bash
python3 python/article_calculator.py exponential --n0 100 --r 0.08 --t 40
python3 python/article_calculator.py logistic --n0 100 --r 0.08 --k 1000 --t 40
python3 python/article_calculator.py per-capita --growth 8 --population 100
python3 python/article_calculator.py equilibrium --r 0.08 --k 1000
python3 python/article_calculator.py sensitivity-r --n0 100 --r 0.08 --k 1000 --t 40 --delta 0.01
python3 python/article_calculator.py capacity-warning --n 900 --k 1000 --margin 0.15
```

## R examples

```bash
Rscript r/article_calculator.R exponential 100 0.08 40
Rscript r/article_calculator.R logistic 100 0.08 1000 40
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
