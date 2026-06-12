# Probabilistic and Stochastic Models

Companion code and reproducible workflows for **“Probabilistic and Stochastic Models”** in the **Mathematical Modeling** knowledge series.

This folder treats random variables, distributions, stochastic processes, probability model registers, Monte Carlo simulation, uncertainty propagation, risk diagnostics, tail measures, dependence assumptions, and validation under uncertainty as explicit model design objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and probability-model review scaffolding.

## Folder structure

```text
articles/probabilistic-and-stochastic-models/
├── python/      # Probability register, Monte Carlo simulation, CLI, tests
├── r/           # Distribution review and uncertainty diagnostics
├── julia/       # Monte Carlo risk scenario workflow
├── sql/         # Probability-governance schema and diagnostic queries
├── haskell/     # Typed probability model records
├── rust/        # Strongly typed probability component CLI
├── go/          # Lightweight Monte Carlo risk model
├── cpp/         # Engineering-style probabilistic simulation
├── fortran/     # Scientific-computing Monte Carlo simulation
├── c/           # Low-level deterministic pseudo-random simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Distribution review, Monte Carlo, validation, ethics
├── data/        # Probability model register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for probability records and risk scenarios
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
python3 python/probabilistic_stochastic_models/cli.py --output-dir outputs
```

## Modeling themes

- uncertainty as model structure;
- random variables, distributions, and stochastic outputs;
- Monte Carlo simulation and uncertainty propagation;
- risk probability, severity, quantiles, and tail behavior;
- distribution review, dependence assumptions, and calibration;
- validation and responsible communication under uncertainty.
