# Article Calculators

Reusable calculator layer for **Directional Derivatives and Gradients**.

## Python examples

```bash
python3 python/article_calculator.py evaluate --x 4 --y 3
python3 python/article_calculator.py gradient --x 4 --y 3
python3 python/article_calculator.py gradient-norm --x 4 --y 3
python3 python/article_calculator.py normalize --vx 2 --vy -1
python3 python/article_calculator.py directional-derivative --x 4 --y 3 --vx 1 --vy 1
python3 python/article_calculator.py estimated-change --x 4 --y 3 --vx 1 --vy 1 --step 0.25
python3 python/article_calculator.py feasible-direction --x 8 --y 1 --vx 1 --vy 1 --step 1 --budget 10
python3 python/article_calculator.py gradient-ascent-step --x 4 --y 3 --step 0.25
python3 python/article_calculator.py gradient-descent-step --x 4 --y 3 --step 0.25
python3 python/article_calculator.py compare-directions --x 4 --y 3
python3 python/article_calculator.py contour-tangent --x 4 --y 3
```

## R examples

```bash
Rscript r/article_calculator.R gradient 4 3
Rscript r/article_calculator.R directional-derivative 4 3 1 1
Rscript r/article_calculator.R estimated-change 4 3 1 1 0.25
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
