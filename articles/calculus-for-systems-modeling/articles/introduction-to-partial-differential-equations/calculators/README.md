# Article Calculators

Reusable calculator layer for **Introduction to Partial Differential Equations**.

## Python examples

```bash
python3 python/article_calculator.py stability-ratio --diffusivity 0.1 --dt 0.25 --dx 1
python3 python/article_calculator.py diffusion-step --left 0 --center 1 --right 0 --stability-ratio 0.025
python3 python/article_calculator.py explicit-diffusion --grid-points 51 --diffusivity 0.1 --dx 1 --dt 0.25 --steps 100
python3 python/article_calculator.py boundary-condition-note --kind dirichlet
```

## R examples

```bash
Rscript r/article_calculator.R stability-ratio 0.1 0.25 1
Rscript r/article_calculator.R diffusion-step 0 1 0 0.025
Rscript r/article_calculator.R explicit-diffusion 51 0.1 1 0.25 100
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
