# Taylor and Maclaurin Series in Modeling

Companion code and reproducible workflows for **Taylor and Maclaurin Series in Modeling** in the **Calculus for Systems Modeling** series.

## Themes

- Taylor series and derivative-based coefficients;
- Maclaurin series as Taylor series centered at zero;
- first-order approximation and linearization;
- second-order approximation and curvature;
- higher-order nonlinear structure;
- remainder and truncation error;
- convergence versus useful approximation;
- local validity and modeling judgment;
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

```bash
cd calculators
bash run_calculator_smoke_tests.sh

python3 python/article_calculator.py taylor-exp --x 1 --order 10
python3 python/article_calculator.py taylor-sin --x 1 --order 10
python3 python/article_calculator.py taylor-cos --x 1 --order 10
python3 python/article_calculator.py linearization --x 1.1 --center 1
python3 python/article_calculator.py second-order --x 1.1 --center 1
python3 python/article_calculator.py truncation-sweep --x 1 --max-order 12
python3 python/article_calculator.py derivative --x 2 --h 0.0001
python3 python/article_calculator.py integral --a 0 --b 1 --steps 1000
python3 python/article_calculator.py euler --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py rk4 --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py logistic --initial 10 --carrying-capacity 100 --rate 0.25 --steps 20
python3 python/article_calculator.py finite-diff --values 1,2,4,7,11
python3 python/article_calculator.py sensitivity --parameter-min 0.1 --parameter-max 1.0 --samples 10
```

The calculators write CSV and JSON outputs to `calculators/outputs/`.
