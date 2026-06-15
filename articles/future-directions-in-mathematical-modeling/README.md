# Future Directions in Mathematical Modeling

Companion code and reproducible workflows for **“Future Directions in Mathematical Modeling”** in the **Mathematical Modeling** knowledge series.

This folder treats future modeling as a strategic, governed portfolio: hybrid models, model ensembles, AI-assisted modeling, digital twins, uncertainty-aware workflows, causal-ML integration, participatory modeling, reproducible infrastructure, model governance, human judgment, lifecycle monitoring, and responsible future modeling strategy.

## Run

```bash
make all
```

or:

```bash
make smoke
python3 python/future_directions_in_mathematical_modeling/cli.py --output-dir outputs
```

## Structure

```text
python/      # Future direction register, priority scoring, governance card, tests
r/           # Future modeling priority review
julia/       # Future direction priority summary
sql/         # Future modeling strategy schema and queries
haskell/     # Typed future direction records
rust/        # Strongly typed future direction records
go/          # Lightweight future direction summary
cpp/         # Future priority scoring example
fortran/     # Scientific-computing future priority scoring
c/           # Low-level future priority scoring
notebooks/   # Notebook-ready walkthrough
docs/        # Hybrid modeling, AI assistance, digital twins, uncertainty, governance
data/        # Direction register, domain guide, lifecycle guide
outputs/     # Generated results, figures, JSON, logs, backups
canvas/      # Catalyst Canvas companion metadata
schemas/     # JSON schemas for future direction records
```

## Self-contained calculators

This article folder includes a reusable calculator layer in `calculators/` for quick command-line exploration of derivatives, definite integrals, finite differences, ODE solvers, logistic dynamics, and parameter sensitivity. The scripts are intentionally self-contained so they can be run without installing article-specific dependencies.

Example commands:

```bash
cd calculators
python3 python/model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
python3 python/model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 10 --method simpson
python3 python/model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50
bash run_calculator_smoke_tests.sh
```
