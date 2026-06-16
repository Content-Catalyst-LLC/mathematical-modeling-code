# Article Calculators

Reusable calculator layer for **Euler's Method**.

## Python examples

```bash
python3 python/article_calculator.py euler-step --t 0 --y 100 --h 0.1 --decay-rate 0.35
python3 python/article_calculator.py decay-audit --y0 100 --decay-rate 0.35 --h 0.1 --stop-time 20
python3 python/article_calculator.py step-size-comparison --y0 100 --decay-rate 0.35 --stop-time 20
python3 python/article_calculator.py stability-check --h 0.1 --decay-rate 0.35
python3 python/article_calculator.py logistic-step --y 10 --r 0.2 --k 100 --h 1
```

## R examples

```bash
Rscript r/article_calculator.R euler-step 0 100 0.1 0.35
Rscript r/article_calculator.R stability-check 0.1 0.35
Rscript r/article_calculator.R logistic-step 10 0.2 100 1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
