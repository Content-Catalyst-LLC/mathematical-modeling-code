# Abstraction and Representation in Mathematical Models

Companion code and reproducible workflows for **“Abstraction and Representation in Mathematical Models”** in the **Mathematical Modeling** knowledge series.

This folder treats abstraction and representation as professional modeling decisions rather than informal preliminaries. It supports abstraction audits, representation-choice review, omitted-detail registers, stock-flow scenario modeling, typed representation records, validation planning, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and representation-review scaffolding.

## Folder structure

```text
articles/abstraction-and-representation-in-mathematical-models/
├── python/      # Abstraction/representation audit package, CLI, tests
├── r/           # Scenario review and visualization workflow
├── julia/       # Numerical stock-flow representation workflow
├── sql/         # Representation governance schema and diagnostics
├── haskell/     # Typed representation records
├── rust/        # Strongly typed representation-review CLI
├── go/          # Lightweight scenario-summary workflow
├── cpp/         # Engineering-style representation model
├── fortran/     # Scientific-computing stock-flow simulation
├── c/           # Low-level deterministic simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Assumptions, model-target relation, validation, ethics
├── data/        # Scenario definitions and representation audit inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for representation inputs and outputs
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
python3 python/abstraction_representation/cli.py --output-dir outputs
```

## Modeling themes

- abstraction as selective structure preservation;
- representation as formal encoding;
- model-target relationships;
- omitted-detail registers;
- aggregation, idealization, and distortion;
- stock-flow representations;
- scenario comparison;
- validation and representational adequacy;
- typed representation governance;
- reproducible computational workflows.
