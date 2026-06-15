# Power Series and Functional Representation

Companion code and reproducible workflows for **Power Series and Functional Representation** in the **Calculus for Systems Modeling** series.

## Themes

- power series as functional representation;
- centers of expansion;
- coefficient interpretation;
- radius and interval of convergence;
- geometric series as the basic model;
- analytic functions;
- polynomial truncation;
- approximation error;
- local versus global validity;
- full multilanguage reproducible workflows;
- website-ready calculator scaffolding.

## Run

```bash
make smoke
make all
make calculators
make advanced
```

## Languages included

```text
python/
r/
julia/
sql/
haskell/
c/
cpp/
fortran/
rust/
go/
notebooks/
docs/
data/
outputs/
schemas/
canvas/
advanced/
calculators/
```

## Self-contained calculators

This article includes a reusable `calculators/` layer. These calculators are command-line runnable and designed to provide the computational source layer for future website widgets.

```bash
cd calculators
bash run_calculator_smoke_tests.sh

python3 python/article_calculator.py power-series --x 0.75 --terms 20
python3 python/article_calculator.py taylor-exp --x 1 --terms 12
python3 python/article_calculator.py taylor-sin --x 1 --terms 12
python3 python/article_calculator.py radius-check --x 1.25 --center 0 --radius 1
python3 python/article_calculator.py truncation-sweep --x 0.75 --max-terms 20
python3 python/article_calculator.py derivative --x 2 --h 0.0001
python3 python/article_calculator.py integral --a 0 --b 1 --steps 1000
python3 python/article_calculator.py euler --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py rk4 --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py logistic --initial 10 --carrying-capacity 100 --rate 0.25 --steps 20
python3 python/article_calculator.py finite-diff --values 1,2,4,7,11
python3 python/article_calculator.py sensitivity --parameter-min 0.1 --parameter-max 1.0 --samples 10
```

The calculators write CSV and JSON outputs to `calculators/outputs/`.
