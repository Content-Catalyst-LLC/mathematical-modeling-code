# Article Calculators

Reusable calculator layer for **Typed Model Records and Functional Workflows in Haskell**.

## Python examples

```bash
python3 python/article_calculator.py validate-parameter --name growth_rate --value 0.35 --minimum 0
python3 python/article_calculator.py logistic-step --stock 10 --growth-rate 0.35 --carrying-capacity 100 --time-step 0.25
python3 python/article_calculator.py simulate-final --growth-rate 0.35 --carrying-capacity 100
python3 python/article_calculator.py diagnostic-status --review-required false
python3 python/article_calculator.py record-completeness --present 7 --required 7
python3 python/article_calculator.py type-safety-warning --pattern empirical_validity
```

## R examples

```bash
Rscript r/article_calculator.R validate-parameter growth_rate 0.35 0
Rscript r/article_calculator.R logistic-step 10 0.35 100 0.25
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
