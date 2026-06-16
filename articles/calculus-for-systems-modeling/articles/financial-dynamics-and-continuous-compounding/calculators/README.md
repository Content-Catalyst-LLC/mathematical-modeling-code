# Financial Dynamics and Continuous Compounding Calculators

Reusable calculator layer for **Financial Dynamics and Continuous Compounding**.

## Python examples

```bash
python3 python/article_calculator.py continuous-future-value --v0 1000 --r 0.05 --t 30
python3 python/article_calculator.py continuous-present-value --fv 5000 --r 0.05 --t 30
python3 python/article_calculator.py discrete-compound-value --v0 1000 --r 0.05 --n 12 --t 30
python3 python/article_calculator.py real-rate --nominal-rate 0.06 --inflation-rate 0.025
python3 python/article_calculator.py npv --discount-rate 0.045 --cash-flows "0:-1000,5:300,10:500,15:900,20:1200"
python3 python/article_calculator.py debt-step --balance 2000 --rate 0.07 --payment 120
python3 python/article_calculator.py geometric-return --returns "0.08,-0.12,0.15,0.04,-0.05,0.11"
python3 python/article_calculator.py governance-warning --context expected_return
```

## R examples

```bash
Rscript r/article_calculator.R continuous-future-value 1000 0.05 30
Rscript r/article_calculator.R continuous-present-value 5000 0.05 30
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
