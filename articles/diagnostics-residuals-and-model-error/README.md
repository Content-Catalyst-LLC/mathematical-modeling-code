# Diagnostics, Residuals, and Model Error

Companion code and reproducible workflows for **“Diagnostics, Residuals, and Model Error”** in the **Mathematical Modeling** knowledge series.

This folder treats residuals as diagnostic evidence: residual tables, error metrics, bias review, subgroup diagnostics, threshold error, outlier flags, structural-error review, uncertainty notes, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional diagnostics, residual analysis, model error, uncertainty, structural-error, and decision-support scaffolding.

## Folder structure

```text
articles/diagnostics-residuals-and-model-error/
├── python/      # Residual diagnostics, register, assessment card, tests
├── r/           # Residual review and diagnostic plots
├── julia/       # Diagnostic metric workflow
├── sql/         # Diagnostic-governance schema and queries
├── haskell/     # Typed diagnostic records
├── rust/        # Strongly typed diagnostic component CLI
├── go/          # Lightweight residual diagnostic example
├── cpp/         # Engineering-style diagnostic scoring
├── fortran/     # Scientific-computing diagnostic summary
├── c/           # Low-level diagnostic metric example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Residuals, error metrics, thresholds, ethics
├── data/        # Observations, diagnostic register, component guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for diagnostic observations and records
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
python3 python/diagnostics_residuals_model_error/cli.py --output-dir outputs
```

## Modeling themes

- residuals as diagnostic evidence rather than leftover noise;
- model error as bias, variance, tail error, subgroup error, or structural error;
- decision-threshold diagnostics;
- outlier and stress-case review;
- error metrics plus context-specific interpretation;
- model-error communication and accountable use limits.
