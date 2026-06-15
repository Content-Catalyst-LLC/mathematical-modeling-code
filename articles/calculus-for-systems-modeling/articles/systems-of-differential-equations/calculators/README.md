# Article Calculators

Reusable calculator layer for **Systems of Differential Equations**.

## Python examples

```bash
python3 python/article_calculator.py predator-prey-rates --prey 40 --predator 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5
python3 python/article_calculator.py coexistence-equilibrium --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5
python3 python/article_calculator.py euler-step --prey 40 --predator 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 --dt 0.01
python3 python/article_calculator.py simulate-predator-prey --prey 40 --predator 9 --alpha 0.7 --beta 0.05 --delta 0.02 --gamma 0.5 --dt 0.01 --steps 100
```

## R examples

```bash
Rscript r/article_calculator.R predator-prey-rates 40 9 0.7 0.05 0.02 0.5
Rscript r/article_calculator.R coexistence-equilibrium 0.7 0.05 0.02 0.5
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
