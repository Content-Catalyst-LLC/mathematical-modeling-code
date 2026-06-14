# Mathematical Modeling in Engineering

Companion code and reproducible workflows for **“Mathematical Modeling in Engineering”** in the **Mathematical Modeling** knowledge series.

This folder treats engineering modeling as design evidence: engineering model registers, design constraints, beam design review, stress-margin analysis, safety-factor summaries, optimization tradeoff notes, validation records, typed engineering model records, and responsible engineering interpretation artifacts.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional engineering model registration, design review, stress-margin analysis, safety review, uncertainty communication, and reproducibility scaffolding.

## Folder structure

```text
articles/mathematical-modeling-in-engineering/
├── python/      # Engineering model register, beam design review, evidence card, tests
├── r/           # Design alternative summary and safety review
├── julia/       # Beam design safety-factor summary
├── sql/         # Engineering modeling governance schema and queries
├── haskell/     # Typed engineering model records
├── rust/        # Strongly typed engineering model record CLI
├── go/          # Lightweight engineering design summary
├── cpp/         # Engineering-style beam design summary
├── fortran/     # Scientific-computing beam design model
├── c/           # Low-level beam design example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Design, safety, validation, uncertainty, ethics
├── data/        # Engineering model register, beam designs, domain guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for engineering model records and beam designs
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
python3 python/mathematical_modeling_in_engineering/cli.py --output-dir outputs
```

## Modeling themes

- engineering models as design-constrained representations;
- requirements, constraints, safety margins, and tolerances;
- stress, load, resistance, failure modes, and reliability;
- simulation, optimization, control, and lifecycle modeling;
- verification, validation, testing, and responsible engineering governance;
- reproducible design review and explicit use limits.
