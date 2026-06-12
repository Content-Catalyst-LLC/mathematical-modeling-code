# Optimization Models and Objective Functions

Companion code and reproducible workflows for **“Optimization Models and Objective Functions”** in the **Mathematical Modeling** knowledge series.

This folder treats decision variables, objective functions, constraints, feasible regions, scenario comparison, tradeoff review, solver interpretation, and optimization ethics as explicit model design objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and optimization-model review scaffolding.

## Folder structure

```text
articles/optimization-models-and-objective-functions/
├── python/      # Optimization register, feasible-choice enumeration, CLI, tests
├── r/           # Objective review and scenario diagnostics
├── julia/       # Resource allocation optimization workflow
├── sql/         # Optimization-governance schema and diagnostic queries
├── haskell/     # Typed optimization model records
├── rust/        # Strongly typed optimization component CLI
├── go/          # Lightweight allocation optimizer
├── cpp/         # Engineering-style optimization enumeration
├── fortran/     # Scientific-computing allocation enumeration
├── c/           # Low-level exhaustive feasible-choice search
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Objective review, constraints, validation, ethics
├── data/        # Optimization model register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for optimization records and scenarios
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
python3 python/optimization_models_objective_functions/cli.py --output-dir outputs
```

## Modeling themes

- optimization as constrained decision support;
- objective functions as formalized goals;
- decision variables, constraints, feasible regions, and parameters;
- feasible-choice audits and near-optimal alternatives;
- sensitivity to objective, budget, weights, and constraints;
- solver interpretation, validation, and ethical review.
