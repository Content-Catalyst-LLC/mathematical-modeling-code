# Communicating Model Uncertainty

Companion code and reproducible workflows for **“Communicating Model Uncertainty”** in the **Mathematical Modeling** knowledge series.

This folder treats uncertainty communication as a governed modeling artifact: communication cards, uncertainty messages, audience-specific summaries, plain-language statements, threshold-risk explanations, use-limit statements, review queues, typed communication records, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional uncertainty communication, audience review, risk explanation, threshold communication, and use-limit scaffolding.

## Folder structure

```text
articles/communicating-model-uncertainty/
├── python/      # Communication card, uncertainty messages, review queues, tests
├── r/           # Audience summary and communication-priority plot
├── julia/       # Communication-priority summary
├── sql/         # Communication-governance schema and queries
├── haskell/     # Typed communication records
├── rust/        # Strongly typed communication-layer CLI
├── go/          # Lightweight audience communication summary
├── cpp/         # Engineering-style communication table
├── fortran/     # Scientific-computing communication summary
├── c/           # Low-level communication-priority example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Communication guidance, intervals, thresholds, ethics
├── data/        # Communication records, uncertainty messages, audience guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for communication records and messages
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
python3 python/communicating_model_uncertainty/cli.py --output-dir outputs
```

## Modeling themes

- uncertainty communication as part of evidence;
- intervals, ranges, scenarios, and probability statements;
- threshold-risk and decision-reversal communication;
- structural uncertainty disclosure;
- plain-language framing without oversimplification;
- audience-specific communication and use-limit statements.
