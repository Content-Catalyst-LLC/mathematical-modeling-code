# Discrete Models and Recurrence Relations

Companion code and reproducible workflows for **“Discrete Models and Recurrence Relations”** in the **Mathematical Modeling** knowledge series.

This folder treats recurrence relations, discrete-time state variables, step definitions, update rules, difference equations, boundary events, adaptive demand, threshold behavior, trajectory diagnostics, and validation as explicit model design objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and recurrence-model review scaffolding.

## Folder structure

```text
articles/discrete-models-and-recurrence-relations/
├── python/      # Recurrence register, discrete simulation, CLI, tests
├── r/           # Recurrence review and stepwise diagnostics
├── julia/       # Numerical recurrence scenario workflow
├── sql/         # Recurrence-governance schema and diagnostic queries
├── haskell/     # Typed recurrence records
├── rust/        # Strongly typed recurrence component CLI
├── go/          # Lightweight recurrence resource model
├── cpp/         # Engineering-style recurrence simulation
├── fortran/     # Scientific-computing recurrence simulation
├── c/           # Low-level deterministic recurrence simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Recurrence design, update order, validation, ethics
├── data/        # Recurrence model register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for recurrence records and scenarios
```

## Run everything available

```bash
make all
```

## Dependency-light smoke test

```bash
make smoke
```

## Selected targets

```bash
make python
make test
make r
make sql
make julia
make haskell
make rust
make go
make cpp
make fortran
make c
```

## Minimal Python run

```bash
python3 python/discrete_models_recurrence_relations/cli.py --output-dir outputs
```

## Modeling themes

- recurrence relations as structured stepwise update rules;
- state variables, time steps, update order, boundaries, and outputs;
- linear and nonlinear discrete-time dynamics;
- boundary-event reporting and adaptive demand;
- trajectory diagnostics and fixed-point review;
- validation, sensitivity, and uncertainty for discrete models.

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
