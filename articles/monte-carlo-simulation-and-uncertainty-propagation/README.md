# Monte Carlo Simulation and Uncertainty Propagation

Companion code and reproducible workflows for **“Monte Carlo Simulation and Uncertainty Propagation”** in the **Mathematical Modeling** knowledge series.

This folder treats uncertainty propagation, sampled ensembles, input distributions, pseudo-random seeds, threshold probabilities, quantiles, convergence diagnostics, sensitivity review, validation, and reproducibility as explicit mathematical modeling objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, convergence, reproducibility, and decision-support scaffolding.

## Folder structure

```text
articles/monte-carlo-simulation-and-uncertainty-propagation/
├── python/      # Monte Carlo register, sampled ensembles, risk diagnostics, tests
├── r/           # Uncertainty review and quantile diagnostics
├── julia/       # Monte Carlo resource-risk workflow
├── sql/         # Uncertainty-governance schema and diagnostic queries
├── haskell/     # Typed Monte Carlo model records
├── rust/        # Strongly typed uncertainty component CLI
├── go/          # Lightweight Monte Carlo sampling
├── cpp/         # Engineering-style Monte Carlo sampling
├── fortran/     # Scientific-computing Monte Carlo summary
├── c/           # Low-level Monte Carlo sample generator
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Sampling, convergence, validation, and ethics guides
├── data/        # Monte Carlo register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for uncertainty records and scenarios
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
python3 python/monte_carlo_uncertainty_propagation/cli.py --output-dir outputs
```

## Modeling themes

- Monte Carlo simulation as uncertainty propagation;
- input distributions, sampled ensembles, seeds, and replications;
- output distributions, quantiles, and threshold probabilities;
- convergence and replication diagnostics;
- sensitivity and uncertainty attribution;
- reproducible uncertainty workflows for decision support.
