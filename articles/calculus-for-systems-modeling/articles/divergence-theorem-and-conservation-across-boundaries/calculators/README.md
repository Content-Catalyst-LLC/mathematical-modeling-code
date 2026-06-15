# Article Calculators

Reusable calculator layer for **The Divergence Theorem and Conservation Across Boundaries**.

## Python examples

```bash
python3 python/article_calculator.py vector-field --x 1 --y 2 --z 3
python3 python/article_calculator.py divergence --x 1 --y 2 --z 3
python3 python/article_calculator.py boundary-flux --grid-steps 16
python3 python/article_calculator.py volume-divergence --grid-steps 16
python3 python/article_calculator.py conservation-audit --grid-steps 16
```

## R examples

```bash
Rscript r/article_calculator.R boundary-flux 16
Rscript r/article_calculator.R volume-divergence 16
Rscript r/article_calculator.R conservation-audit 16
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
