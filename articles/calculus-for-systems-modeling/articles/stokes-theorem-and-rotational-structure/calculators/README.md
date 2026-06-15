# Article Calculators

Reusable calculator layer for **Stokes' Theorem and Rotational Structure**.

## Python examples

```bash
python3 python/article_calculator.py vector-field --x 1 --y 0 --z 0
python3 python/article_calculator.py curl-field --x 1 --y 0 --z 0
python3 python/article_calculator.py boundary-circulation --radius 1 --segments 128
python3 python/article_calculator.py surface-curl-flux --radius 1 --radial-steps 32
python3 python/article_calculator.py stokes-audit --radius 1 --segments 128 --radial-steps 32
```

## R examples

```bash
Rscript r/article_calculator.R boundary-circulation 1 128
Rscript r/article_calculator.R surface-curl-flux 1 32
Rscript r/article_calculator.R stokes-audit 1 128 32
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
