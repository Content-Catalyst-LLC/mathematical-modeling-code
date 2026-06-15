# Convergence Tests and the Discipline of Infinite Approximation

Companion code and reproducible workflows for **Convergence Tests and the Discipline of Infinite Approximation** in the **Calculus for Systems Modeling** series.

## Themes

- term test and necessary conditions;
- geometric series and p-series benchmarks;
- comparison and limit-comparison tests;
- ratio and root tests;
- integral-test tail bounds;
- alternating-series error estimates;
- absolute and conditional convergence;
- finite partial sums versus infinite claims;
- stopping rules and remainder estimates;
- website-ready calculator scaffolding.

## Run

```bash
make smoke
make calculators
make advanced
```

## Self-contained calculators

This article includes a reusable `calculators/` layer. These calculators are command-line runnable and designed to provide the computational source layer for future website widgets.

```bash
cd calculators
bash run_calculator_smoke_tests.sh

python3 python/article_calculator.py geometric --a 10 --r 0.6 --terms 25
python3 python/article_calculator.py pseries --p 1.25 --terms 10000
python3 python/article_calculator.py alternating --terms 10000
python3 python/article_calculator.py derivative --x 2 --h 0.0001
python3 python/article_calculator.py integral --a 0 --b 1 --steps 1000
python3 python/article_calculator.py euler --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py rk4 --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py logistic --initial 10 --carrying-capacity 100 --rate 0.25 --steps 20
python3 python/article_calculator.py finite-diff --values 1,2,4,7,11
python3 python/article_calculator.py sensitivity --parameter-min 0.1 --parameter-max 1.0 --samples 10
```

The calculators write CSV and JSON outputs to `calculators/outputs/`.
