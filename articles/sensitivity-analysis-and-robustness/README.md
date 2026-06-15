# Sensitivity Analysis and Robustness

Companion code and reproducible workflows for **“Sensitivity Analysis and Robustness”** in the **Mathematical Modeling** knowledge series.

This folder treats sensitivity and robustness as evidence workflows: parameter ranges, baseline outputs, one-at-a-time sweeps, scenario stress checks, threshold fragility, sensitivity rankings, robustness assessment cards, typed review records, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional sensitivity analysis, robustness, scenario testing, uncertainty propagation, structural sensitivity, and decision-support scaffolding.

## Folder structure

```text
articles/sensitivity-analysis-and-robustness/
├── python/      # Parameter sweeps, robustness cards, sensitivity register, tests
├── r/           # Sensitivity rankings and tornado-style plots
├── julia/       # Sensitivity scoring workflow
├── sql/         # Sensitivity-governance schema and queries
├── haskell/     # Typed sensitivity records
├── rust/        # Strongly typed sensitivity component CLI
├── go/          # Lightweight sensitivity example
├── cpp/         # Engineering-style robustness scoring
├── fortran/     # Scientific-computing sensitivity summary
├── c/           # Low-level sensitivity metric example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Parameter ranges, thresholds, scenarios, ethics
├── data/        # Parameters, sensitivity register, component guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for sensitivity parameters and records
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
python3 python/sensitivity_analysis_and_robustness/cli.py --output-dir outputs
```

## Modeling themes

- local sensitivity and parameter sweeps;
- sensitivity ranking and output range width;
- uncertainty propagation thinking;
- threshold fragility and decision reversal;
- scenario stress testing;
- structural sensitivity and model-form dependence;
- robustness as decision stability under plausible change.

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
