# Article Calculators

Reusable calculator layer for **Ordinary Differential Equation Solver Workflows**.

## Python examples

```bash
python3 python/article_calculator.py rk4-solver-step --t 0 --y 100 --h 0.5 --decay-rate 0.35
python3 python/article_calculator.py solver-benchmark --y0 100 --decay-rate 0.35 --h 0.5 --stop-time 20
python3 python/article_calculator.py step-size-comparison --y0 100 --decay-rate 0.35 --stop-time 20
python3 python/article_calculator.py tolerance-threshold --atol 1e-8 --rtol 1e-6 --state 100
python3 python/article_calculator.py stiffness-indicator --fast-rate 100 --slow-rate 1
python3 python/article_calculator.py solver-config-record --method fixed_step_rk4 --h 0.5 --atol 1e-8 --rtol 1e-6
```

## R examples

```bash
Rscript r/article_calculator.R rk4-solver-step 0 100 0.5 0.35
Rscript r/article_calculator.R tolerance-threshold 1e-8 1e-6 100
Rscript r/article_calculator.R stiffness-indicator 100 1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
