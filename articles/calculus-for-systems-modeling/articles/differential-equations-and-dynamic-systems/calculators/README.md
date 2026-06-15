# Article Calculators

Reusable calculator layer for **Differential Equations and Dynamic Systems**.

## Python examples

```bash
python3 python/article_calculator.py exponential-rate --state 10 --growth-rate 0.35
python3 python/article_calculator.py logistic-rate --state 10 --growth-rate 0.35 --capacity 100
python3 python/article_calculator.py euler-step --state 10 --rate 3.5 --dt 0.1
python3 python/article_calculator.py simulate-exponential --state 10 --growth-rate 0.35 --dt 0.1 --steps 20
python3 python/article_calculator.py simulate-logistic --state 10 --growth-rate 0.35 --capacity 100 --dt 0.1 --steps 20
```

## R examples

```bash
Rscript r/article_calculator.R exponential-rate 10 0.35
Rscript r/article_calculator.R logistic-rate 10 0.35 100
Rscript r/article_calculator.R euler-step 10 3.5 0.1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
