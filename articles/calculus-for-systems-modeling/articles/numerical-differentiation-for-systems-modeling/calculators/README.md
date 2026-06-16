# Article Calculators

Reusable calculator layer for **Numerical Differentiation for Systems Modeling**.

## Python examples

```bash
python3 python/article_calculator.py forward-difference --f-current 1 --f-next 1.12 --h 0.1
python3 python/article_calculator.py backward-difference --f-previous 0.89 --f-current 1 --h 0.1
python3 python/article_calculator.py central-difference --f-previous 0.89 --f-next 1.12 --h 0.1
python3 python/article_calculator.py second-central-difference --f-previous 0.89 --f-current 1 --f-next 1.12 --h 0.1
python3 python/article_calculator.py benchmark-audit --start 0 --stop 10 --h 0.1
```

## R examples

```bash
Rscript r/article_calculator.R forward-difference 1 1.12 0.1
Rscript r/article_calculator.R central-difference 0.89 1.12 0.1
Rscript r/article_calculator.R second-central-difference 0.89 1 1.12 0.1
Rscript r/article_calculator.R benchmark-audit 0 10 0.1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
