# Article Calculators

Reusable calculator layer for **Green's Theorem and Planar Systems**.

## Python examples

```bash
python3 python/article_calculator.py rotation-field --x 1 --y 1
python3 python/article_calculator.py expansion-field --x 1 --y 1
python3 python/article_calculator.py planar-curl --x 1 --y 1
python3 python/article_calculator.py planar-divergence --x 1 --y 1
python3 python/article_calculator.py boundary-circulation --segments 32
python3 python/article_calculator.py interior-curl --step 0.25
python3 python/article_calculator.py boundary-flux --segments 32
python3 python/article_calculator.py interior-divergence --step 0.25
python3 python/article_calculator.py greens-audit --segments 32 --step 0.25
```

## R examples

```bash
Rscript r/article_calculator.R boundary-circulation 32
Rscript r/article_calculator.R interior-curl 0.25
Rscript r/article_calculator.R greens-audit 32 0.25
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
