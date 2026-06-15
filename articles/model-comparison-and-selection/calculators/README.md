# Calculator layer for model-comparison-and-selection

This folder contains self-contained calculator scripts for article companion workflows.
They are designed to run from the command line without project-specific packages.

## Python examples

```bash
python3 python/model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
python3 python/model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 10 --method simpson --n 1000
python3 python/model_calculator.py euler --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50 --out outputs/euler.csv
python3 python/model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50 --out outputs/rk4.csv
python3 python/model_calculator.py logistic --r 0.2 --k 100 --y0 10 --dt 0.1 --steps 50 --out outputs/logistic.csv
python3 python/model_calculator.py finite-difference --values "1,1.4,2.1,3.2" --h 0.5 --out outputs/finite_difference.csv
python3 python/model_calculator.py sensitivity --expr "r*x*(1-x/k)" --param r --min 0.05 --max 0.5 --count 10 --x 25 --params "k=100" --out outputs/sensitivity.csv
```

## R examples

```bash
Rscript r/model_calculator.R derivative --expr "sin(x)*exp(-x)" --x 1.5
Rscript r/model_calculator.R integral --expr "x^2 + sin(x)" --a 0 --b 10 --method simpson --n 1000
Rscript r/model_calculator.R logistic --r 0.2 --k 100 --y0 10 --dt 0.1 --steps 50 --out outputs/logistic_r.csv
```

## Smoke checks

```bash
bash run_calculator_smoke_tests.sh
```

## Included calculator modes

- numerical derivative estimates
- definite integral estimates
- Euler ODE stepping
- fourth-order Runge--Kutta ODE stepping
- logistic growth simulation
- finite difference tables
- one-parameter sensitivity sweeps
