# Calibration, Estimation, and Parameter Fitting

Companion code and reproducible workflows for **“Calibration, Estimation, and Parameter Fitting”** in the **Mathematical Modeling** knowledge series.

This folder treats calibration as accountable modeling evidence: parameter registers, calibration observations, objective functions, candidate scoring, best-fit records, residual diagnostics, uncertainty notes, validation planning, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional calibration, estimation, validation, uncertainty, optimization, and decision-support scaffolding.

## Folder structure

```text
articles/calibration-estimation-and-parameter-fitting/
├── python/      # Calibration register, candidate scoring, residual diagnostics, tests
├── r/           # Calibration review and residual diagnostics
├── julia/       # Grid-search calibration workflow
├── sql/         # Calibration-governance schema and diagnostic queries
├── haskell/     # Typed calibration records
├── rust/        # Strongly typed calibration component CLI
├── go/          # Lightweight parameter fitting example
├── cpp/         # Engineering-style candidate scoring
├── fortran/     # Scientific-computing calibration summary
├── c/           # Low-level calibration score example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Calibration, identifiability, residual, and ethics guides
├── data/        # Observations, parameter grid, calibration register
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for calibration records and observations
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
python3 python/calibration_estimation_parameter_fitting/cli.py --output-dir outputs
```

## Modeling themes

- calibration as evidence-constrained optimization;
- parameter meaning, bounds, identifiability, and uncertainty;
- objective functions, residual diagnostics, and validation planning;
- reproducible parameter fitting with reviewable outputs;
- avoiding false authority from best-fit values alone.
