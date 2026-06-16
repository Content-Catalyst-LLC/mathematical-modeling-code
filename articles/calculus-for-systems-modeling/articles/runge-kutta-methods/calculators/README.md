# Article Calculators

Reusable calculator layer for **Runge–Kutta Methods**.

## Python examples

```bash
python3 python/article_calculator.py rk4-step --t 0 --y 100 --h 0.5 --decay-rate 0.35
python3 python/article_calculator.py midpoint-step --t 0 --y 100 --h 0.5 --decay-rate 0.35
python3 python/article_calculator.py heun-step --t 0 --y 100 --h 0.5 --decay-rate 0.35
python3 python/article_calculator.py stage-values --t 0 --y 100 --h 0.5 --decay-rate 0.35
python3 python/article_calculator.py euler-vs-rk4-audit --y0 100 --decay-rate 0.35 --h 0.5 --stop-time 20
python3 python/article_calculator.py step-size-comparison --y0 100 --decay-rate 0.35 --stop-time 20
```

## R examples

```bash
Rscript r/article_calculator.R rk4-step 0 100 0.5 0.35
Rscript r/article_calculator.R midpoint-step 0 100 0.5 0.35
Rscript r/article_calculator.R heun-step 0 100 0.5 0.35
Rscript r/article_calculator.R stage-values 0 100 0.5 0.35
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
