# Validation and Model Assessment

Companion code and reproducible workflows for **“Validation and Model Assessment”** in the **Mathematical Modeling** knowledge series.

This folder treats validation as evidence organization: conceptual validity, implementation verification, data validation, residual diagnostics, out-of-sample assessment, benchmark comparison, uncertainty review, fitness-for-purpose classification, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional validation, verification, uncertainty, diagnostics, robustness, and decision-support scaffolding.

## Folder structure

```text
articles/validation-and-model-assessment/
├── python/      # Validation register, error metrics, assessment card, tests
├── r/           # Validation review and residual diagnostics
├── julia/       # Validation metric workflow
├── sql/         # Validation-governance schema and diagnostic queries
├── haskell/     # Typed validation records
├── rust/        # Strongly typed validation component CLI
├── go/          # Lightweight validation metrics example
├── cpp/         # Engineering-style validation diagnostics
├── fortran/     # Scientific-computing validation summary
├── c/           # Low-level validation score example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Validation, verification, uncertainty, and ethics guides
├── data/        # Validation observations, register, component guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for validation records and observations
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
python3 python/validation_and_model_assessment/cli.py --output-dir outputs
```

## Modeling themes

- validation as conditional trust, not certainty;
- verification, calibration review, and validation as distinct practices;
- residual diagnostics, out-of-sample assessment, and benchmark comparison;
- uncertainty, sensitivity, robustness, and fitness-for-purpose review;
- decision-support governance and use-limit statements.

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
