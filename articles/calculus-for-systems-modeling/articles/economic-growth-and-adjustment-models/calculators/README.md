# Economic Growth and Adjustment Models Calculators

Reusable calculator layer for **Economic Growth and Adjustment Models**.

## Python examples

```bash
python3 python/article_calculator.py exponential-growth --y0 100 --g 0.025 --years 40
python3 python/article_calculator.py doubling-time --g 0.025
python3 python/article_calculator.py logistic-growth --y0 100 --r 0.06 --k 240 --years 40
python3 python/article_calculator.py capital-step --capital 300 --output 100 --savings-rate 0.22 --depreciation 0.05
python3 python/article_calculator.py cobb-douglas --a 1.2 --k 450 --l 180 --alpha 0.35
python3 python/article_calculator.py growth-accounting --a-growth 0.01 --k-growth 0.03 --l-growth 0.02 --alpha 0.35
python3 python/article_calculator.py adjustment-step --x 100 --target 160 --lambda-rate 0.35
python3 python/article_calculator.py governance-warning --context output_welfare
```

## R examples

```bash
Rscript r/article_calculator.R exponential-growth 100 0.025 40
Rscript r/article_calculator.R doubling-time 0.025
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
