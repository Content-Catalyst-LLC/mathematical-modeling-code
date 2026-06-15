# Robustness, Fragility, and Model Dependence

Companion code and reproducible workflows for **“Robustness, Fragility, and Model Dependence”** in the **Mathematical Modeling** knowledge series.

This folder treats robustness as a reviewable modeling artifact: robustness matrices, fragility rankings, dependence registers, scenario stress tests, threshold reversal checks, structural-dependence notes, typed robustness records, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional robustness assessment, fragility analysis, model dependence, stress testing, and decision-support scaffolding.

## Folder structure

```text
articles/robustness-fragility-and-model-dependence/
├── python/      # Robustness matrix, fragility classes, dependence registers, tests
├── r/           # Robustness summaries and fragility plots
├── julia/       # Robustness spread and threshold disagreement summary
├── sql/         # Robustness/dependence governance schema and queries
├── haskell/     # Typed robustness records
├── rust/        # Strongly typed dependence-layer CLI
├── go/          # Lightweight robustness matrix example
├── cpp/         # Engineering-style robustness summary
├── fortran/     # Scientific-computing robustness summary
├── c/           # Low-level robustness matrix example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Robustness, fragility, dependence, thresholds, ethics
├── data/        # Scenario matrix, robustness register, component guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for robustness scenarios and records
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
python3 python/robustness_fragility_and_model_dependence/cli.py --output-dir outputs
```

## Modeling themes

- robustness as stability across plausible disturbance;
- fragility as reversal under modest changes;
- model dependence as reliance on one representation or decision rule;
- threshold fragility and decision reversal;
- data, scenario, parameter, model-form, and metric dependence;
- robust decision support and use-limit communication.

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
