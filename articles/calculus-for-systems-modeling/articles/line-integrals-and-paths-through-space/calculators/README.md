# Article Calculators

Reusable calculator layer for **Line Integrals and Paths Through Space**.

## Python examples

```bash
python3 python/article_calculator.py path-point --t 1
python3 python/article_calculator.py scalar-field --x 1 --y 2
python3 python/article_calculator.py vector-field --x 1 --y 2
python3 python/article_calculator.py segment-length --x1 0 --y1 0 --x2 3 --y2 4
python3 python/article_calculator.py scalar-segment --x 1 --y 2 --segment-length 0.5
python3 python/article_calculator.py vector-segment --x 1 --y 2 --dx 0.25 --dy 0.1
python3 python/article_calculator.py line-audit --step 0.25
python3 python/article_calculator.py path-length --step 0.25
python3 python/article_calculator.py scalar-line-approx --step 0.25
python3 python/article_calculator.py vector-line-approx --step 0.25
```

## R examples

```bash
Rscript r/article_calculator.R path-point 1
Rscript r/article_calculator.R segment-length 0 0 3 4
Rscript r/article_calculator.R scalar-field 1 2
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
