# Article Calculators

Reusable calculator layer for **Diffusion, Transport, and Spatial Dynamics**.

## Python examples

```bash
python3 python/article_calculator.py diffusion-ratio --diffusivity 0.08 --dt 0.2 --dx 1
python3 python/article_calculator.py transport-ratio --velocity 0.4 --dt 0.2 --dx 1
python3 python/article_calculator.py advection-diffusion-step --left 0 --center 1 --right 0 --diffusion-ratio 0.016 --transport-ratio 0.08
python3 python/article_calculator.py advection-diffusion-simulation --grid-points 61 --diffusivity 0.08 --velocity 0.4 --dx 1 --dt 0.2 --steps 120
```

## R examples

```bash
Rscript r/article_calculator.R diffusion-ratio 0.08 0.2 1
Rscript r/article_calculator.R transport-ratio 0.4 0.2 1
Rscript r/article_calculator.R advection-diffusion-step 0 1 0 0.016 0.08
Rscript r/article_calculator.R advection-diffusion-simulation 61 0.08 0.4 1 0.2 120
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
