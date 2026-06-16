# Carbon Accumulation and Emissions Pathways Calculators

Reusable calculator layer for **Case Study: Carbon Accumulation and Emissions Pathways**.

## Python examples

```bash
python3 python/article_calculator.py cumulative-linear --e0 40 --years 30
python3 python/article_calculator.py cumulative-exponential --e0 40 --rate 0.08 --years 30
python3 python/article_calculator.py atmospheric-burden --cumulative 600 --airborne-fraction 0.45
python3 python/article_calculator.py budget-check --cumulative 600 --budget 500
python3 python/article_calculator.py overshoot --e0 40 --decline-years 30 --negative-years 20 --removal-rate 5
python3 python/article_calculator.py impulse-burden --e0 40 --years 30 --pathway linear
python3 python/article_calculator.py removal-warning --gross 10 --removal 10
python3 python/article_calculator.py accounting-warning --boundary global_co2
```

## R examples

```bash
Rscript r/article_calculator.R cumulative-linear 40 30
Rscript r/article_calculator.R budget-check 600 500
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
