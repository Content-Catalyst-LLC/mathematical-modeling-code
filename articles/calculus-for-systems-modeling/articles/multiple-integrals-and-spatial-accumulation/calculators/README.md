# Article Calculators

Reusable calculator layer for **Multiple Integrals and Spatial Accumulation**.

## Python examples

```bash
python3 python/article_calculator.py rectangle-total --density 12 --width 4 --height 3
python3 python/article_calculator.py volume-total --density 5 --length 4 --width 3 --height 2
python3 python/article_calculator.py polar-area --radius 3
python3 python/article_calculator.py polar-density-total --density 2 --radius 3
python3 python/article_calculator.py grid-total --step 0.5
python3 python/article_calculator.py area-average --step 0.5
python3 python/article_calculator.py population-weighted --step 0.5
python3 python/article_calculator.py cell-sum --values 1 2 3 4 --cell-area 0.25
python3 python/article_calculator.py weighted-average --values 10 20 30 --weights 1 2 3
python3 python/article_calculator.py resolution-scan --steps 1.0 0.5 0.25
```

## R examples

```bash
Rscript r/article_calculator.R rectangle-total 12 4 3
Rscript r/article_calculator.R grid-total 0.5
Rscript r/article_calculator.R population-weighted 0.5
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
