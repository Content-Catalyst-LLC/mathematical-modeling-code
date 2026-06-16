# Article Calculators

Reusable calculator layer for **Initial Conditions, Boundary Conditions, and Model Scope**.

## Python examples

```bash
python3 python/article_calculator.py logistic-final --initial-stock 10 --growth-rate 0.35 --carrying-capacity 100 --horizon 20
python3 python/article_calculator.py initial-condition-effect --low 5 --baseline 10 --high 20
python3 python/article_calculator.py scope-check --value 0.35 --lower 0.1 --upper 0.6
python3 python/article_calculator.py boundary-warning --boundary-type no_flux
python3 python/article_calculator.py horizon-warning --horizon 20 --maximum-supported 20
python3 python/article_calculator.py condition-scope-warning --pattern claim_boundary
```

## R examples

```bash
Rscript r/article_calculator.R logistic-final 10 0.35 100 20
Rscript r/article_calculator.R scope-check 0.35 0.1 0.6
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
