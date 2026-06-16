# Predator-Prey Systems Calculators

Reusable calculator layer for **Case Study: Predator-Prey Systems**.

## Python examples

```bash
python3 python/article_calculator.py lotka-volterra-step --x 40 --y 9 --alpha 0.6 --beta 0.02 --gamma 0.5 --delta 0.01 --dt 0.02
python3 python/article_calculator.py coexistence --alpha 0.6 --beta 0.02 --gamma 0.5 --delta 0.01
python3 python/article_calculator.py jacobian --x 50 --y 30 --alpha 0.6 --beta 0.02 --gamma 0.5 --delta 0.01
python3 python/article_calculator.py simulate --x0 40 --y0 9 --steps 4000
python3 python/article_calculator.py type-ii-response --x 50 --a 0.04 --h 0.08
python3 python/article_calculator.py harvesting-risk --hx 1 --hy 0.05
python3 python/article_calculator.py interaction-warning --pattern mass_action
```

## R examples

```bash
Rscript r/article_calculator.R coexistence 0.6 0.02 0.5 0.01
Rscript r/article_calculator.R type-ii-response 50 0.04 0.08
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
