# Article Calculators

Reusable calculator layer for **Constrained Optimization and Lagrange Multipliers**.

## Python examples

```bash
python3 python/article_calculator.py solve --target 12
python3 python/article_calculator.py objective --x 8 --y 4
python3 python/article_calculator.py constraint --x 8 --y 4 --target 12
python3 python/article_calculator.py gradients --x 8 --y 4
python3 python/article_calculator.py stationarity --target 12
python3 python/article_calculator.py multiplier --target 12
python3 python/article_calculator.py shadow-value --target 12 --delta 0.1
python3 python/article_calculator.py feasibility --x 8 --y 4 --target 12
python3 python/article_calculator.py active-status --value 12 --limit 12
python3 python/article_calculator.py tradeoff-scan --targets 12 18 24
```

## R examples

```bash
Rscript r/article_calculator.R solve 12
Rscript r/article_calculator.R multiplier 12
Rscript r/article_calculator.R stationarity 12
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
