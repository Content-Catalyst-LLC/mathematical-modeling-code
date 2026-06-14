# Model Governance and Accountability

Companion code and reproducible workflows for **“Model Governance and Accountability”** in the **Mathematical Modeling** knowledge series.

This folder treats model governance as a full lifecycle process: purpose definition, ownership, validation status, use-limit tracking, monitoring status, governance-risk scoring, incident escalation, revision triggers, retirement criteria, and accountable decision ownership.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance registration, validation review, use-limit tracking, monitoring review, governance-risk scoring, escalation, and lifecycle accountability artifacts.

## Folder structure

```text
articles/model-governance-and-accountability/
├── python/      # Governance register, risk scoring, governance card, tests
├── r/           # Governance summary and risk review
├── julia/       # Governance-risk scoring summary
├── sql/         # Model governance schema and queries
├── haskell/     # Typed governance records
├── rust/        # Strongly typed governance record CLI
├── go/          # Lightweight governance-risk summary
├── cpp/         # Governance-risk scoring example
├── fortran/     # Scientific-computing governance scoring
├── c/           # Low-level governance-risk scoring
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Model governance, ownership, validation, use limits, monitoring
├── data/        # Governance register, risk cases, lifecycle checklist
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for governance records and risk cases
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
python3 python/model_governance_and_accountability/cli.py --output-dir outputs
```

## Modeling themes

- model ownership and decision ownership;
- validation, review, and approval;
- use limits and approved domains;
- monitoring, drift, incidents, revision, and retirement;
- model risk, uncertainty, scope misuse, and accountability gaps;
- governance as lifecycle control rather than paperwork.
