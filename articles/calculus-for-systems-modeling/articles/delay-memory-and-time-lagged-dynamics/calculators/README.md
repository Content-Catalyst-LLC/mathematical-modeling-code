# Article Calculators

Reusable calculator layer for **Delay, Memory, and Time-Lagged Dynamics**.

## Python examples

```bash
python3 python/article_calculator.py delay-steps --delay 5 --dt 0.1
python3 python/article_calculator.py delayed-lookup --initial-state 80 --delay-steps 50 --step 10
python3 python/article_calculator.py memory-kernel --age 3 --decay-rate 0.4
python3 python/article_calculator.py delayed-adjustment --initial-state 80 --target 100 --adjustment-rate 0.2 --delay 5 --dt 0.1 --steps 300
```

## R examples

```bash
Rscript r/article_calculator.R delay-steps 5 0.1
Rscript r/article_calculator.R memory-kernel 3 0.4
Rscript r/article_calculator.R delayed-adjustment 80 100 0.2 5 0.1 300
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
