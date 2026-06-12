# Differential Equations and Dynamic Models

Companion code and reproducible workflows for **“Differential Equations and Dynamic Models”** in the **Mathematical Modeling** knowledge series.

This folder treats differential equations, dynamic state variables, rate equations, initial conditions, boundaries, numerical time steps, trajectory diagnostics, stability review, and validation as explicit model design objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and dynamic-model review scaffolding.

## Folder structure

```text
articles/differential-equations-and-dynamic-models/
├── python/      # Dynamic model register, Euler simulation, CLI, tests
├── r/           # Dynamic review and time-series diagnostics
├── julia/       # Numerical dynamic-model scenario workflow
├── sql/         # Dynamic-model governance schema and diagnostic queries
├── haskell/     # Typed dynamic model records
├── rust/        # Strongly typed dynamic component CLI
├── go/          # Lightweight dynamic resource model
├── cpp/         # Engineering-style dynamic simulation
├── fortran/     # Scientific-computing dynamic simulation
├── c/           # Low-level deterministic dynamic simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Dynamic model design, solvers, validation, ethics
├── data/        # Dynamic model register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for dynamic model records and scenarios
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
python3 python/differential_equations_dynamic_models/cli.py --output-dir outputs
```

## Modeling themes

- differential equations as structured claims about change;
- states, rates, flows, initial conditions, and boundaries;
- ODE-style dynamic simulation;
- numerical integration and time-step review;
- trajectories, stress behavior, and domain constraints;
- validation, sensitivity, and uncertainty for dynamic models.
