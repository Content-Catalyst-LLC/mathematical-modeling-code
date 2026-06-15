# Article Calculators

Reusable calculator layer for **Total Differentials and Local Approximation in Higher Dimensions**.

## Python examples

```bash
python3 python/article_calculator.py evaluate --x 4 --y 3
python3 python/article_calculator.py total-differential --x 4 --y 3 --dx 0.2 --dy -0.1
python3 python/article_calculator.py local-linear --x 4 --y 3 --dx 0.2 --dy -0.1
python3 python/article_calculator.py approximation-error --x 4 --y 3 --dx 1 --dy 1
python3 python/article_calculator.py gradient-dot --gradient 4.5,4 --displacement 0.2,-0.1
python3 python/article_calculator.py feasible-displacement --x 8 --y 1 --dx 1 --dy 1 --budget 10
python3 python/article_calculator.py perturbation-sweep --x 4 --y 3 --scale-max 2 --samples 10
python3 python/article_calculator.py uncertainty-propagation --x 4 --y 3 --dx-error 0.1 --dy-error 0.2
python3 python/article_calculator.py tangent-plane --x0 4 --y0 3 --x 4.2 --y 2.9
```

## R examples

```bash
Rscript r/article_calculator.R total-differential 4 3 0.2 -0.1
Rscript r/article_calculator.R local-linear 4 3 0.2 -0.1
Rscript r/article_calculator.R approximation-error 4 3 1 1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
