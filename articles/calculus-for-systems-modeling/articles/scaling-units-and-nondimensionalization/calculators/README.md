# Article Calculators

Reusable calculator layer for **Scaling, Units, and Nondimensionalization**.

## Python examples

```bash
python3 python/article_calculator.py scale-value --value 40 --scale 100
python3 python/article_calculator.py unscale-value --dimensionless 0.4 --scale 100
python3 python/article_calculator.py rate-conversion --rate 0.01 --from-unit day --to-unit year
python3 python/article_calculator.py logistic-nondimensional --stock 40 --capacity 100 --time 20 --growth-rate 0.35
python3 python/article_calculator.py conditioning-ratio --largest 1000000 --smallest 0.001
python3 python/article_calculator.py scaling-warning --pattern empirical_validity
```

## R examples

```bash
Rscript r/article_calculator.R scale-value 40 100
Rscript r/article_calculator.R logistic-nondimensional 40 100 20 0.35
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
