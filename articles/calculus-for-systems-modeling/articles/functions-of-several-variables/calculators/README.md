# Article Calculators

Reusable calculator layer for **Functions of Several Variables**.

## Python examples

```bash
python3 python/article_calculator.py evaluate --x 4 --y 3
python3 python/article_calculator.py feasible --x 8 --y 4 --budget 10
python3 python/article_calculator.py grid --max-x 10 --max-y 10 --step 2
python3 python/article_calculator.py level-curve --target 30 --max-x 10 --max-y 10 --step 1 --tolerance 1
python3 python/article_calculator.py interaction --x 4 --y 3
python3 python/article_calculator.py local-neighborhood --x 4 --y 3 --center-x 3 --center-y 3 --radius 2
python3 python/article_calculator.py partial-x --x 4 --y 3 --h 0.001
python3 python/article_calculator.py partial-y --x 4 --y 3 --h 0.001
python3 python/article_calculator.py sensitivity --x-min 0 --x-max 10 --y 3 --samples 10
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
