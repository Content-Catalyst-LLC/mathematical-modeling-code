# Calibration, Estimation, and Parameter Fitting

Companion code and reproducible workflows for **“Calibration, Estimation, and Parameter Fitting”** in the **Mathematical Modeling** knowledge series.

This folder treats calibration as accountable modeling evidence: parameter registers, calibration observations, objective functions, candidate scoring, best-fit records, residual diagnostics, uncertainty notes, validation planning, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional calibration, estimation, validation, uncertainty, optimization, and decision-support scaffolding.

## Folder structure

```text
articles/calibration-estimation-and-parameter-fitting/
├── python/      # Calibration register, candidate scoring, residual diagnostics, tests
├── r/           # Calibration review and residual diagnostics
├── julia/       # Grid-search calibration workflow
├── sql/         # Calibration-governance schema and diagnostic queries
├── haskell/     # Typed calibration records
├── rust/        # Strongly typed calibration component CLI
├── go/          # Lightweight parameter fitting example
├── cpp/         # Engineering-style candidate scoring
├── fortran/     # Scientific-computing calibration summary
├── c/           # Low-level calibration score example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Calibration, identifiability, residual, and ethics guides
├── data/        # Observations, parameter grid, calibration register
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for calibration records and observations
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
python3 python/calibration_estimation_parameter_fitting/cli.py --output-dir outputs
```

## Modeling themes

- calibration as evidence-constrained optimization;
- parameter meaning, bounds, identifiability, and uncertainty;
- objective functions, residual diagnostics, and validation planning;
- reproducible parameter fitting with reviewable outputs;
- avoiding false authority from best-fit values alone.

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
