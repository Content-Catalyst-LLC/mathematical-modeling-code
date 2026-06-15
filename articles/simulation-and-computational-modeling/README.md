# Simulation and Computational Modeling

Companion code and reproducible workflows for **“Simulation and Computational Modeling”** in the **Mathematical Modeling** knowledge series.

This folder treats simulation design, computational implementation, numerical approximation, scenario experiments, stochastic ensembles, verification, validation, reproducibility, and model governance as explicit mathematical modeling objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and reproducibility scaffolding.

## Folder structure

```text
articles/simulation-and-computational-modeling/
├── python/      # Simulation register, resource scenarios, ensemble diagnostics, tests
├── r/           # Simulation review and ensemble diagnostics
├── julia/       # Resource simulation workflow
├── sql/         # Simulation-governance schema and diagnostic queries
├── haskell/     # Typed simulation model records
├── rust/        # Strongly typed simulation component CLI
├── go/          # Lightweight resource simulation
├── cpp/         # Engineering-style resource simulation
├── fortran/     # Scientific-computing simulation summary
├── c/           # Low-level simulation trajectory
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Simulation design, verification, validation, ethics
├── data/        # Simulation register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for simulation records and scenarios
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
python3 python/simulation_computational_modeling/cli.py --output-dir outputs
```

## Modeling themes

- simulation as executable mathematical reasoning;
- state variables, update rules, parameters, scenarios, and outputs;
- deterministic and stochastic simulation;
- numerical approximation, convergence, verification, and validation;
- reproducibility, run logs, seeds, and versioned outputs;
- responsible decision support from computational experiments.

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
