# Model Repositories, Data, and Reproducible Research

Companion code and reproducible workflows for **“Model Repositories, Data, and Reproducible Research”** in the **Mathematical Modeling** knowledge series.

This folder treats a model repository as an evidence system: structured files, data provenance, metadata, schemas, reproducibility manifests, output indexes, model cards, tests, validation records, licensing notes, and governance artifacts.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional repository governance, data provenance, validation, reproducibility, and decision-support scaffolding.

## Folder structure

```text
articles/model-repositories-data-and-reproducible-research/
├── python/      # Repository audit, artifact inventory, manifest, tests
├── r/           # Repository review and data diagnostics
├── julia/       # Repository inventory workflow
├── sql/         # Repository-governance schema and diagnostic queries
├── haskell/     # Typed repository records
├── rust/        # Strongly typed repository component CLI
├── go/          # Lightweight repository inventory summary
├── cpp/         # Engineering-style repository inventory check
├── fortran/     # Scientific-computing inventory summary
├── c/           # Low-level repository inventory example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Repository, provenance, licensing, and ethics guides
├── data/        # Repository registers, expected artifacts, data dictionaries
├── outputs/     # Generated results, figures, JSON, logs, backups, archives
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for repository records and artifact inventory
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
python3 python/model_repositories_reproducible_research/cli.py --output-dir outputs
```

## Modeling themes

- repository structure as modeling infrastructure;
- data provenance, raw/processed/synthetic data boundaries;
- reproducibility manifests and output hashes;
- model cards, audit registers, license/citation notes;
- repository validation and long-term research accountability.
