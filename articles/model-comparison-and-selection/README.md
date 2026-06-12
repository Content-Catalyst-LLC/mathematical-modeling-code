# Model Comparison and Selection

Companion code and reproducible workflows for **“Model Comparison and Selection”** in the **Mathematical Modeling** knowledge series.

This folder treats model selection as a transparent evidence workflow: candidate model registers, baselines, calibration-vs-validation diagnostics, complexity penalties, overfit-gap checks, interpretability review, robustness review, decision relevance, and selection audit cards.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model comparison, selection, validation, parsimony, robustness, interpretability, and decision-support scaffolding.

## Folder structure

```text
articles/model-comparison-and-selection/
├── python/      # Candidate scoring, selection register, audit card, tests
├── r/           # Model-selection review and comparison diagnostics
├── julia/       # Model comparison scoring workflow
├── sql/         # Model-selection schema and diagnostic queries
├── haskell/     # Typed model selection records
├── rust/        # Strongly typed selection component CLI
├── go/          # Lightweight model comparison example
├── cpp/         # Engineering-style selection scoring
├── fortran/     # Scientific-computing comparison summary
├── c/           # Low-level model comparison score example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Selection, baselines, overfitting, and ethics guides
├── data/        # Candidate models, selection register, criteria
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for model candidates and selection records
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
python3 python/model_comparison_and_selection/cli.py --output-dir outputs
```

## Modeling themes

- model selection as structured judgment about purpose;
- baselines and competing alternatives;
- calibration error versus validation error;
- complexity penalties, parsimony, and overfit gaps;
- uncertainty, robustness, interpretability, and decision relevance;
- preserving alternatives instead of erasing structural uncertainty.
