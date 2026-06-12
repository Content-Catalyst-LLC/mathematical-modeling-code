# Model Boundaries, Scale, and Scope

Companion code and reproducible workflows for **“Model Boundaries, Scale, and Scope”** in the **Mathematical Modeling** knowledge series.

This folder treats model boundaries, scale, and scope as explicit design decisions. It supports boundary registers, scale audits, scope statements, resource stock-flow scenarios, boundary-expansion tests, validation planning, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and boundary-review scaffolding.

## Folder structure

```text
articles/model-boundaries-scale-and-scope/
├── python/      # Boundary/scale/scope audit package, CLI, tests
├── r/           # Boundary review and scenario diagnostic workflow
├── julia/       # Numerical boundary-scenario workflow
├── sql/         # Boundary governance schema and diagnostic queries
├── haskell/     # Typed boundary and scope records
├── rust/        # Strongly typed boundary-review CLI
├── go/          # Lightweight boundary scenario workflow
├── cpp/         # Engineering-style boundary scenario model
├── fortran/     # Scientific-computing stock-flow simulation
├── c/           # Low-level deterministic simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Boundaries, scale, scope, validation, ethics
├── data/        # Boundary register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for boundary and scenario inputs
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
python3 python/boundary_scale_scope/cli.py --output-dir outputs
```

## Modeling themes

- model boundaries as domain restrictions;
- spatial, temporal, population, mechanism, data, and decision boundaries;
- scale mismatch and false resolution;
- scope statements and prohibited uses;
- boundary sensitivity testing;
- aggregation and distributional visibility;
- validation by purpose, boundary, and scale;
- typed model governance;
- reproducible computational workflows.
