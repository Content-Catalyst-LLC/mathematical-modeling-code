# Article Calculators

Reusable calculator layer for **Gradient, Divergence, and Curl**.

## Python examples

```bash
python3 python/article_calculator.py scalar-field --x 1 --y 1
python3 python/article_calculator.py vector-field --x 1 --y 1
python3 python/article_calculator.py gradient --x 1 --y 1
python3 python/article_calculator.py gradient-magnitude --x 1 --y 1
python3 python/article_calculator.py divergence --x 1 --y 1
python3 python/article_calculator.py curl-2d --x 1 --y 1
python3 python/article_calculator.py finite-difference-gradient --x 1 --y 1 --h 0.01
python3 python/article_calculator.py finite-difference-divergence --x 1 --y 1 --h 0.01
python3 python/article_calculator.py finite-difference-curl --x 1 --y 1 --h 0.01
python3 python/article_calculator.py field-audit --step 0.25
```

## R examples

```bash
Rscript r/article_calculator.R scalar-field 1 1
Rscript r/article_calculator.R gradient 1 1
Rscript r/article_calculator.R curl-2d 1 1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
