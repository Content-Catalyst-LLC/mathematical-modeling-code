# Article Calculators

Reusable calculator layer for **Symbolic Calculus and Model Inspection**.

## Python examples

```bash
python3 python/article_calculator.py logistic-derivative
python3 python/article_calculator.py logistic-equilibria
python3 python/article_calculator.py capacity-limit
python3 python/article_calculator.py jacobian-record
python3 python/article_calculator.py domain-warning --expression "r*x*(1 - x/K)"
python3 python/article_calculator.py symbolic-inspection-report
```

## R examples

```bash
Rscript r/article_calculator.R logistic-derivative
Rscript r/article_calculator.R logistic-equilibria
Rscript r/article_calculator.R capacity-limit
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
