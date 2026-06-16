# Coupled Human-Natural Systems Calculators

Reusable calculator layer for **Coupled Human-Natural Systems**.

## Python examples

```bash
python3 python/article_calculator.py regeneration --stock 80 --growth-rate 0.08 --carrying-capacity 100
python3 python/article_calculator.py extraction --efficiency 0.003 --effort 12 --stock 80
python3 python/article_calculator.py stock-step --stock 80 --growth-rate 0.08 --carrying-capacity 100 --harvest 2.88 --stress 0.25 --dt 0.25
python3 python/article_calculator.py adaptive-effort-step --effort 12 --scarcity 0.2 --governance-strength 0.6 --adjustment-rate 0.2 --dt 0.25
python3 python/article_calculator.py distributional-burden --exposure 0.6 --vulnerability 1.4 --adaptation 0.2
python3 python/article_calculator.py threshold-warning --stock 25 --threshold 30
python3 python/article_calculator.py governance-warning --context equity
```

## R examples

```bash
Rscript r/article_calculator.R regeneration 80 0.08 100
Rscript r/article_calculator.R extraction 0.003 12 80
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
