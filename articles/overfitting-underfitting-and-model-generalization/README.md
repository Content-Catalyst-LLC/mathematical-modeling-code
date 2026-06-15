# Overfitting, Underfitting, and Model Generalization

Companion code and reproducible workflows for **“Overfitting, Underfitting, and Model Generalization”** in the **Mathematical Modeling** knowledge series.

This folder treats generalization as an evidence workflow: training-versus-validation diagnostics, overfit gaps, underfit flags, complexity review, interpretability review, distribution-shift notes, decision-threshold review, and generalization assessment cards.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional overfitting, underfitting, generalization, validation, regularization, robustness, and decision-support scaffolding.

## Folder structure

```text
articles/overfitting-underfitting-and-model-generalization/
├── python/      # Generalization diagnostics, register, assessment card, tests
├── r/           # Training-vs-validation review and plots
├── julia/       # Generalization scoring workflow
├── sql/         # Generalization-governance schema and diagnostic queries
├── haskell/     # Typed generalization records
├── rust/        # Strongly typed generalization component CLI
├── go/          # Lightweight overfit/underfit example
├── cpp/         # Engineering-style generalization scoring
├── fortran/     # Scientific-computing generalization summary
├── c/           # Low-level generalization score example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Generalization, cross-validation, regularization, ethics
├── data/        # Candidate models, generalization register, criteria
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for generalization models and records
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
python3 python/overfitting_underfitting_generalization/cli.py --output-dir outputs
```

## Modeling themes

- overfitting as memorization of noise or accidental pattern;
- underfitting as missing structure;
- training error versus validation error;
- overfit gaps, underfit flags, and model complexity;
- regularization, constraints, and simpler models;
- distribution shift, external validity, and decision-support limits.

## Self-contained calculators

This article folder includes a reusable calculator layer in `calculators/` for quick command-line exploration of derivatives, definite integrals, finite differences, ODE solvers, logistic dynamics, and parameter sensitivity. The scripts are intentionally self-contained so they can be run without installing article-specific dependencies.

Example commands:

```bash
cd calculators
python3 python/model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
python3 python/model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 10 --method simpson
python3 python/model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50
bash run_calculator_smoke_tests.sh
```
