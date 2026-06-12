# What Is Mathematical Modeling?

Companion code and reproducible workflows for **“What Is Mathematical Modeling?”** in the **Mathematical Modeling** knowledge series.

This folder treats mathematical modeling as a professional workflow rather than a single equation. It includes examples for mathematicians, engineers, statisticians, scientific programmers, and decision-support analysts.

## Quality standard

This folder is designed to meet or exceed the companion-code quality baseline used in the Mathematical Thinking repository:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, and sensitivity scaffolding.

## Repository contents

```text
articles/what-is-mathematical-modeling/
├── python/      # Core reproducible modeling package, CLI, and tests
├── r/           # Scenario diagnostics and visualization workflow
├── julia/       # Numerical modeling and parameter sweep workflow
├── sql/         # Modeling metadata, scenario, validation, and run schema
├── c/           # Low-level deterministic simulation example
├── cpp/         # Engineering-style model class and diagnostics
├── fortran/     # Scientific-computing style numerical simulation
├── rust/        # Strongly typed modeling workflow
├── go/          # Scenario workflow
├── haskell/     # Typed mathematical-modeling records
├── notebooks/   # Notebook-ready computational demonstrations
├── docs/        # Assumptions, V&V, UQ, engineering/statistical notes
├── data/        # Synthetic parameters, observations, scenarios
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for inputs and outputs
```

## Modeling coverage

- continuous-time and discrete-time logistic modeling;
- Euler and RK4 numerical integration;
- scenario comparison;
- calibration against synthetic observations;
- residual diagnostics;
- one-at-a-time sensitivity analysis;
- Monte Carlo uncertainty propagation;
- validation and adequacy reporting;
- typed model-governance records with Haskell;
- SQL tables for model governance and reproducibility;
- multi-language implementations for engineering and scientific-computing contexts.

## Run everything available

```bash
make all
```

## Run selected targets

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

## Minimal run

```bash
python3 python/what_is_mathematical_modeling/cli.py --output-dir outputs
```

## Professional extension paths

This scaffold can be extended with:

- dimensional analysis;
- nondimensionalization;
- solver convergence tests;
- Bayesian calibration;
- global sensitivity analysis;
- stochastic process models;
- model comparison and selection;
- formal validation reports;
- engineering review logs;
- model governance dashboards.
