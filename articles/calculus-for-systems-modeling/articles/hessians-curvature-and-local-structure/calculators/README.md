# Article Calculators

Reusable calculator layer for **Hessians, Curvature, and Local Structure**.

## Python examples

```bash
python3 python/article_calculator.py evaluate --x 2 --y 1
python3 python/article_calculator.py gradient --x 2 --y 1
python3 python/article_calculator.py hessian --x 2 --y 1
python3 python/article_calculator.py determinant --x 2 --y 1
python3 python/article_calculator.py classify --x 2 --y 1
python3 python/article_calculator.py quadratic-term --x 2 --y 1 --dx 0.1 --dy -0.05
python3 python/article_calculator.py first-order --x 2 --y 1 --dx 0.1 --dy -0.05
python3 python/article_calculator.py second-order --x 2 --y 1 --dx 0.1 --dy -0.05
python3 python/article_calculator.py approximation-error --x 2 --y 1 --dx 0.5 --dy 0.5
python3 python/article_calculator.py eigen-2x2 --x 2 --y 1
python3 python/article_calculator.py conditioning-check --x 2 --y 1
python3 python/article_calculator.py cross-partial --x 2 --y 1
```

## R examples

```bash
Rscript r/article_calculator.R hessian 2 1
Rscript r/article_calculator.R classify 2 1
Rscript r/article_calculator.R second-order 2 1 0.1 -0.05
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
