# Article Calculators

Reusable calculator layer for **Sensitivity, Robustness, and Parameter Dependence**.

## Python examples

```bash
python3 python/article_calculator.py logistic-final --initial-stock 10 --growth-rate 0.35 --carrying-capacity 100 --horizon 20
python3 python/article_calculator.py finite-difference --low-output 85.8 --high-output 99.7 --lower 0.2 --upper 0.5
python3 python/article_calculator.py elasticity --sensitivity 46.3 --parameter 0.35 --output 99.2
python3 python/article_calculator.py robustness-classification --low-output 85.8 --high-output 99.7 --threshold 10
python3 python/article_calculator.py sweep-range --lower 0.2 --upper 0.5 --steps 7
python3 python/article_calculator.py sensitivity-warning --pattern robustness_domain
```

## R examples

```bash
Rscript r/article_calculator.R finite-difference 85.8 99.7 0.2 0.5
Rscript r/article_calculator.R robustness-classification 85.8 99.7 10
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
