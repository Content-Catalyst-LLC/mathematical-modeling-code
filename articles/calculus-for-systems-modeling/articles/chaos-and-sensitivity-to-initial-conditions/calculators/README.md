# Article Calculators

Reusable calculator layer for **Chaos and Sensitivity to Initial Conditions**.

## Python examples

```bash
python3 python/article_calculator.py logistic-next --x 0.2 --r 3.9
python3 python/article_calculator.py trajectory-divergence --x0 0.2 --perturbation 1e-8 --r 3.9 --steps 30
python3 python/article_calculator.py lyapunov-estimate --x0 0.2 --r 3.9 --burn-in 100 --sample-steps 1000
python3 python/article_calculator.py forecast-horizon --initial-uncertainty 1e-8 --acceptable-error 1e-2 --lyapunov 0.5
```

## R examples

```bash
Rscript r/article_calculator.R logistic-next 0.2 3.9
Rscript r/article_calculator.R trajectory-divergence 0.2 1e-8 3.9 30
Rscript r/article_calculator.R forecast-horizon 1e-8 1e-2 0.5
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
