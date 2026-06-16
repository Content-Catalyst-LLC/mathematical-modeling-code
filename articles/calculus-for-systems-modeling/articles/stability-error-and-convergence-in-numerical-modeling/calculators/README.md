# Article Calculators

Reusable calculator layer for **Stability, Error, and Convergence in Numerical Modeling**.

## Python examples

```bash
python3 python/article_calculator.py absolute-error --numeric 0.912 --exact 0.9119
python3 python/article_calculator.py relative-error --numeric 0.912 --exact 0.9119
python3 python/article_calculator.py euler-stability-factor --step-size 0.1 --eigenvalue -1
python3 python/article_calculator.py convergence-ratio --previous-error 0.01 --current-error 0.000625
python3 python/article_calculator.py rk4-final-error --step-size 0.5
python3 python/article_calculator.py refinement-table
```

## R examples

```bash
Rscript r/article_calculator.R absolute-error 0.912 0.9119
Rscript r/article_calculator.R convergence-ratio 0.01 0.000625
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
