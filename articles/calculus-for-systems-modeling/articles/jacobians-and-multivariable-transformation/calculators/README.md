# Article Calculators

Reusable calculator layer for **Jacobians and Multivariable Transformation**.

## Python examples

```bash
python3 python/article_calculator.py evaluate --x 2 --y 1
python3 python/article_calculator.py jacobian --x 2 --y 1
python3 python/article_calculator.py determinant --x 2 --y 1
python3 python/article_calculator.py local-linear --x 2 --y 1 --dx 0.1 --dy -0.05
python3 python/article_calculator.py approximation-error --x 2 --y 1 --dx 0.5 --dy 0.5
python3 python/article_calculator.py area-scaling --x 2 --y 1 --area 3
python3 python/article_calculator.py singularity-check --x 0 --y 0
python3 python/article_calculator.py polar-jacobian --r 3 --theta 0.785398163
python3 python/article_calculator.py sensitivity-column --x 2 --y 1 --input-index 1
python3 python/article_calculator.py sensitivity-row --x 2 --y 1 --output-index 2
```

## R examples

```bash
Rscript r/article_calculator.R jacobian 2 1
Rscript r/article_calculator.R determinant 2 1
Rscript r/article_calculator.R local-linear 2 1 0.1 -0.05
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
