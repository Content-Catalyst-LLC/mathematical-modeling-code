# Article Calculators

Reusable calculator layer for **Parameter Sweeps and Sensitivity Analysis**.

## Python examples

```bash
python3 python/article_calculator.py logistic-final --growth-rate 0.35 --carrying-capacity 100
python3 python/article_calculator.py local-sensitivity --parameter growth_rate
python3 python/article_calculator.py elasticity --parameter carrying_capacity
python3 python/article_calculator.py grid-sweep
python3 python/article_calculator.py robustness-range --low 80 --high 100
python3 python/article_calculator.py fragility-note --pattern threshold
```

## R examples

```bash
Rscript r/article_calculator.R logistic-final 0.35 100
Rscript r/article_calculator.R local-sensitivity growth_rate
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
