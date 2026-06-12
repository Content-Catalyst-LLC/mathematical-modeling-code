# Dimensional Analysis, Units, and Scale

Companion code and reproducible workflows for **“Dimensional Analysis, Units, and Scale”** in the **Mathematical Modeling** knowledge series.

This folder treats units, dimensions, rates, time steps, nondimensionalization, and scale as explicit model design objects. It supports unit registers, dimensional audits, conversion checks, scale scenarios, dimensionless ratios, time-step diagnostics, magnitude checks, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and unit/scale-review scaffolding.

## Folder structure

```text
articles/dimensional-analysis-units-and-scale/
├── python/      # Unit register, dimensional audit, scale diagnostics, CLI, tests
├── r/           # Unit and scale review workflow
├── julia/       # Numerical unit/scale scenario workflow
├── sql/         # Unit-governance schema and diagnostic queries
├── haskell/     # Typed units and dimensions
├── rust/        # Strongly typed unit-review CLI
├── go/          # Lightweight unit/scale scenario workflow
├── cpp/         # Engineering-style unit-consistent resource model
├── fortran/     # Scientific-computing unit-consistent simulation
├── c/           # Low-level deterministic unit-consistent simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Unit registers, dimensional analysis, scaling, ethics
├── data/        # Unit registers and scale-scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for units and scale scenarios
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
python3 python/dimensional_analysis_units_scale/cli.py --output-dir outputs
```

## Modeling themes

- units as formal meaning, not labels;
- dimensions and dimensional homogeneity;
- rate and time-step consistency;
- nondimensionalization and storage fractions;
- scale scenarios and aggregation warnings;
- magnitude checks and numerical scale;
- typed unit governance and reproducibility.
