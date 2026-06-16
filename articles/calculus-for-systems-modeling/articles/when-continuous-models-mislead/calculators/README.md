# Article Calculators

Reusable calculator layer for **When Continuous Models Mislead**.

## Python examples

```bash
python3 python/article_calculator.py smoothness-risk --breaks 1 --thresholds 1 --heterogeneity 1 --solver-warnings 0
python3 python/article_calculator.py threshold-warning --value 0.92 --critical 1.0 --margin 0.1
python3 python/article_calculator.py equilibrium-bias --has-equilibrium 1 --path-analyzed 0 --stability-tested 0
python3 python/article_calculator.py aggregation-risk --mean 50 --maximum 95 --threshold 80
python3 python/article_calculator.py solver-risk --step-check 0 --convergence-flag 1 --stiffness-warning 1
python3 python/article_calculator.py continuous-model-warning --pattern false_smoothness
```

## R examples

```bash
Rscript r/article_calculator.R smoothness-risk 1 1 1 0
Rscript r/article_calculator.R aggregation-risk 50 95 80
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
