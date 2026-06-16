# Climate Feedback Models Calculators

Reusable calculator layer for **Case Study: Climate Feedback Models**.

## Python examples

```bash
python3 python/article_calculator.py co2-forcing --concentration 560 --baseline 280
python3 python/article_calculator.py one-box --forcing 3.7 --feedback 1.2 --heat-capacity 8 --time 80
python3 python/article_calculator.py ecs --forcing 3.7 --feedback 1.2
python3 python/article_calculator.py feedback-sensitivity --forcing 3.7 --feedback 1.2
python3 python/article_calculator.py two-box --forcing 3.7 --feedback 1.2 --surface-capacity 8 --deep-capacity 100 --exchange 0.7 --time 80
python3 python/article_calculator.py carbon-feedback --forcing 3.7 --temperature 3 --beta-carbon 0.15
python3 python/article_calculator.py sign-warning --convention restoring_positive
```

## R examples

```bash
Rscript r/article_calculator.R co2-forcing 560 280
Rscript r/article_calculator.R one-box 3.7 1.2 8 80
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
