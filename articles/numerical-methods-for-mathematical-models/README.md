# Numerical Methods for Mathematical Models

Companion code and reproducible workflows for **“Numerical Methods for Mathematical Models”** in the **Mathematical Modeling** knowledge series.

This folder treats numerical approximation, discretization, solver settings, convergence, stability, step-size sensitivity, numerical diagnostics, and computational validation as explicit mathematical modeling objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, numerical diagnostics, reproducibility, and decision-support scaffolding.

## Folder structure

```text
articles/numerical-methods-for-mathematical-models/
├── python/      # Numerical register, Euler solver diagnostics, tests
├── r/           # Numerical review and convergence diagnostics
├── julia/       # Euler step-size workflow
├── sql/         # Numerical-governance schema and diagnostic queries
├── haskell/     # Typed numerical method records
├── rust/        # Strongly typed numerical component CLI
├── go/          # Lightweight Euler approximation
├── cpp/         # Engineering-style Euler approximation
├── fortran/     # Scientific-computing numerical trajectory
├── c/           # Low-level numerical trajectory
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Numerical method, convergence, and validation guides
├── data/        # Numerical register and solver scenarios
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for numerical records and solver scenarios
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
python3 python/numerical_methods_for_mathematical_models/cli.py --output-dir outputs
```

## Modeling themes

- numerical methods as accountable approximations;
- step size, tolerance, discretization, and convergence;
- Euler approximation for resource dynamics;
- numerical diagnostics and solver review;
- implementation verification and model validation;
- reproducible computational workflows for decision support.
