# Assumptions, Simplification, and Model Design

Companion code and reproducible workflows for **“Assumptions, Simplification, and Model Design”** in the **Mathematical Modeling** knowledge series.

This folder treats assumptions and simplifications as explicit design objects. It supports assumption registers, simplification logs, scenario analysis, sensitivity review, model-design governance, validation planning, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and assumption-review scaffolding.

## Folder structure

```text
articles/assumptions-simplification-and-model-design/
├── python/      # Assumption-aware model design package, CLI, tests
├── r/           # Assumption review and scenario diagnostic workflow
├── julia/       # Numerical resource-model scenario workflow
├── sql/         # Assumption governance schema and diagnostic queries
├── haskell/     # Typed assumption and model-design records
├── rust/        # Strongly typed assumption-review CLI
├── go/          # Lightweight scenario-summary workflow
├── cpp/         # Engineering-style resource model
├── fortran/     # Scientific-computing stock-flow simulation
├── c/           # Low-level deterministic simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Assumptions, simplification, V&V, uncertainty, ethics
├── data/        # Scenario definitions and assumption register inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for assumptions and scenario inputs
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
python3 python/assumptions_model_design/cli.py --output-dir outputs
```

## Modeling themes

- assumptions as load-bearing model architecture;
- simplification, idealization, approximation, and distortion;
- boundary, scale, and scope assumptions;
- parameterization and hidden complexity;
- sensitivity tests and revision triggers;
- validation and representational adequacy;
- typed model-design governance;
- reproducible computational workflows.
