# Article Calculators

Reusable calculator layer for **Vectors, Fields, and Continuous Space**.

## Python examples

```bash
python3 python/article_calculator.py vector-magnitude --vx 3 --vy 4
python3 python/article_calculator.py vector-components --magnitude 5 --angle-degrees 53.130102354
python3 python/article_calculator.py dot-product --ax 1 --ay 2 --bx 3 --by 4
python3 python/article_calculator.py scalar-field --x 1 --y 2
python3 python/article_calculator.py vector-field --x 1 --y 2
python3 python/article_calculator.py field-magnitude --x 1 --y 2
python3 python/article_calculator.py grid-audit --step 0.5
python3 python/article_calculator.py resolution-scan --steps 1.0 0.5 0.25
python3 python/article_calculator.py unit-vector --vx 3 --vy 4
python3 python/article_calculator.py projection --ax 3 --ay 4 --bx 1 --by 0
```

## R examples

```bash
Rscript r/article_calculator.R vector-magnitude 3 4
Rscript r/article_calculator.R scalar-field 1 2
Rscript r/article_calculator.R vector-field 1 2
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
