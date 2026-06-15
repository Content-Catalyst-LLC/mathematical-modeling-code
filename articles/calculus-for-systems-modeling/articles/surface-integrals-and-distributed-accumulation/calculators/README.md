# Article Calculators

Reusable calculator layer for **Surface Integrals and Distributed Accumulation**.

## Python examples

```bash
python3 python/article_calculator.py height --x 1 --y 1
python3 python/article_calculator.py scalar-field --x 1 --y 1
python3 python/article_calculator.py vector-field --x 1 --y 1
python3 python/article_calculator.py normal-area-vector --x 1 --y 1 --step 0.25
python3 python/article_calculator.py patch-area --x 1 --y 1 --step 0.25
python3 python/article_calculator.py scalar-patch --x 1 --y 1 --step 0.25
python3 python/article_calculator.py flux-patch --x 1 --y 1 --step 0.25
python3 python/article_calculator.py surface-audit --step 0.25
python3 python/article_calculator.py surface-area --step 0.25
python3 python/article_calculator.py flux-approx --step 0.25
```

## R examples

```bash
Rscript r/article_calculator.R height 1 1
Rscript r/article_calculator.R patch-area 1 1 0.25
Rscript r/article_calculator.R scalar-field 1 1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
