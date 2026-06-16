# Continuous-Time Epidemiological Models Calculators

Reusable calculator layer for **Continuous-Time Epidemiological Models**.

## Python examples

```bash
python3 python/article_calculator.py r0 --beta 0.32 --gamma 0.10
python3 python/article_calculator.py rt --beta 0.32 --gamma 0.10 --susceptible 85000 --population 100000
python3 python/article_calculator.py doubling-time --growth-rate 0.22
python3 python/article_calculator.py herd-threshold --r0 3.2
python3 python/article_calculator.py force-of-infection --beta 0.32 --infectious 100 --population 100000
python3 python/article_calculator.py incidence --beta 0.32 --susceptible 99900 --infectious 100 --population 100000
python3 python/article_calculator.py sir-step --susceptible 99900 --infectious 100 --recovered 0 --beta 0.32 --gamma 0.10 --population 100000
python3 python/article_calculator.py governance-warning --context reported_cases
```

## R examples

```bash
Rscript r/article_calculator.R r0 0.32 0.10
Rscript r/article_calculator.R doubling-time 0.22
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```

This layer is for educational and reproducible modeling support. It is not medical advice or public-health guidance.
