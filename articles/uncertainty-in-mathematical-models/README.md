# Uncertainty in Mathematical Models

Companion code and reproducible workflows for **“Uncertainty in Mathematical Models”** in the **Mathematical Modeling** knowledge series.

This folder treats uncertainty as a first-class modeling artifact: uncertainty registers, uncertain-parameter tables, propagation runs, probabilistic output summaries, threshold risk, interval review, structural uncertainty notes, typed uncertainty records, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional uncertainty quantification, propagation, probabilistic summaries, threshold risk, structural uncertainty, and decision-support scaffolding.

## Folder structure

```text
articles/uncertainty-in-mathematical-models/
├── python/      # Uncertainty register, propagation workflow, tests
├── r/           # Interval review and uncertainty distribution plots
├── julia/       # Uncertainty propagation summary
├── sql/         # Uncertainty-governance schema and queries
├── haskell/     # Typed uncertainty records
├── rust/        # Strongly typed uncertainty component CLI
├── go/          # Lightweight uncertainty propagation example
├── cpp/         # Engineering-style uncertainty summary
├── fortran/     # Scientific-computing uncertainty summary
├── c/           # Low-level uncertainty metric example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Uncertainty taxonomy, intervals, propagation, ethics
├── data/        # Uncertain parameters, register, component guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for uncertainty parameters and records
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
python3 python/uncertainty_in_mathematical_models/cli.py --output-dir outputs
```

## Modeling themes

- aleatory, epistemic, structural, scenario, and decision uncertainty;
- uncertainty registers and use-limit statements;
- uncertainty propagation and threshold probability;
- interval review and probabilistic output summaries;
- Monte Carlo-style sampling with dependency-light code;
- structural uncertainty as an unresolved modeling obligation.
