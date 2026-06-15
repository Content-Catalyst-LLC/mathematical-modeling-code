# Article Calculators

Reusable calculator layer for **Vector-Valued Functions and Motion**.

## Python examples

```bash
python3 python/article_calculator.py position --t 1
python3 python/article_calculator.py velocity --t 1
python3 python/article_calculator.py acceleration --t 1
python3 python/article_calculator.py speed --t 1
python3 python/article_calculator.py distance --x1 0 --y1 0 --x2 3 --y2 4
python3 python/article_calculator.py displacement --start 0 --stop 6.283185307
python3 python/article_calculator.py arc-length-approx --step 0.25
python3 python/article_calculator.py path-efficiency --step 0.25
python3 python/article_calculator.py finite-difference-velocity --t 1 --dt 0.01
python3 python/article_calculator.py trajectory-audit --step 0.25
```

## R examples

```bash
Rscript r/article_calculator.R position 1
Rscript r/article_calculator.R speed 1
Rscript r/article_calculator.R distance 0 0 3 4
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
