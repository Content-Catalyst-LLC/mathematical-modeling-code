# Article Calculators

Reusable calculator layer for **Phase Lines, Phase Planes, and Phase Portraits**.

## Python examples

```bash
python3 python/article_calculator.py predator-prey-vector --x 40 --y 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5
python3 python/article_calculator.py phase-speed --dxdt 3 --dydt 4
python3 python/article_calculator.py coexistence-equilibrium --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5
python3 python/article_calculator.py grid-summary --x-max 60 --y-max 30 --x-step 5 --y-step 3
```

## R examples

```bash
Rscript r/article_calculator.R predator-prey-vector 40 9 0.7 0.05 0.02 0.5
Rscript r/article_calculator.R phase-speed 3 4
Rscript r/article_calculator.R coexistence-equilibrium 0.7 0.05 0.02 0.5
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
