# Mathematical Modeling in Public Health and Epidemiology

Companion code and reproducible workflows for **“Mathematical Modeling in Public Health and Epidemiology”** in the **Mathematical Modeling** knowledge series.

This folder treats epidemiological modeling as public health evidence infrastructure: public health model registers, SIR intervention scenarios, infectious-curve simulation, hospital capacity review, surveillance interpretation, equity diagnostics, communication notes, governance artifacts, typed public health model records, and responsible public health decision-support workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional public health model registration, SIR simulation, intervention review, hospital capacity diagnostics, surveillance/equity/governance scaffolding, and reproducible decision-support artifacts.

## Folder structure

```text
articles/mathematical-modeling-in-public-health-and-epidemiology/
├── python/      # Public health model register, SIR scenarios, review card, tests
├── r/           # Epidemic scenario summary and capacity review
├── julia/       # SIR scenario summary
├── sql/         # Public health modeling governance schema and queries
├── haskell/     # Typed public health model records
├── rust/        # Strongly typed public health model record CLI
├── go/          # Lightweight epidemic scenario summary
├── cpp/         # SIR scenario review
├── fortran/     # Scientific-computing epidemic model
├── c/           # Low-level SIR scenario example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Transmission, surveillance, capacity, equity, communication, ethics
├── data/        # Public health model register, epidemic scenarios, domain guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for public health model records and epidemic scenarios
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
python3 python/mathematical_modeling_in_public_health_and_epidemiology/cli.py --output-dir outputs
```

## Modeling themes

- epidemiological models as population-state representations;
- transmission dynamics, reproduction numbers, intervention scenarios, and capacity demand;
- surveillance bias, reporting delay, uncertainty, and model validation;
- health equity, public trust, and responsible communication;
- governance, use limits, and public health decision accountability.
