# Article Calculators

Reusable calculator layer for **Flux, Circulation, and Spatial Flow**.

## Python examples

```bash
python3 python/article_calculator.py vector-field --x 1 --y 0
python3 python/article_calculator.py normal-alignment --x 1 --y 0
python3 python/article_calculator.py tangent-alignment --x 1 --y 0
python3 python/article_calculator.py flux-segment --radius 1 --segments 64 --index 0
python3 python/article_calculator.py circulation-segment --radius 1 --segments 64 --index 0
python3 python/article_calculator.py circle-flux --radius 1 --segments 64
python3 python/article_calculator.py circle-circulation --radius 1 --segments 64
python3 python/article_calculator.py flow-audit --radius 1 --segments 64
```

## R examples

```bash
Rscript r/article_calculator.R vector-field 1 0
Rscript r/article_calculator.R circle-circulation 1 64
Rscript r/article_calculator.R circle-flux 1 64
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
