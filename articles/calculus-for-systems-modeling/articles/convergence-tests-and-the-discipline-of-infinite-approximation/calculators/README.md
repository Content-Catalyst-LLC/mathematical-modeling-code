# Article Calculators

Reusable calculator layer for **Convergence Tests and the Discipline of Infinite Approximation**.

These calculators are self-contained, command-line runnable, and designed to become a computational source layer for future website widgets.

## Python examples

```bash
python3 python/article_calculator.py geometric --a 10 --r 0.6 --terms 25
python3 python/article_calculator.py pseries --p 1.25 --terms 10000
python3 python/article_calculator.py alternating --terms 10000
python3 python/article_calculator.py derivative --x 2 --h 0.0001
python3 python/article_calculator.py integral --a 0 --b 1 --steps 1000
python3 python/article_calculator.py euler --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py rk4 --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py logistic --initial 10 --carrying-capacity 100 --rate 0.25 --steps 20
python3 python/article_calculator.py finite-diff --values 1,2,4,7,11
python3 python/article_calculator.py sensitivity --parameter-min 0.1 --parameter-max 1.0 --samples 10
```

## R examples

```bash
Rscript r/article_calculator.R geometric 10 0.6 25
Rscript r/article_calculator.R pseries 1.25 10000
Rscript r/article_calculator.R logistic 10 100 0.25 20
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
