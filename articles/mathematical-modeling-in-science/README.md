# Mathematical Modeling in Science

Companion code and reproducible workflows for **“Mathematical Modeling in Science”** in the **Mathematical Modeling** knowledge series.

This folder treats scientific modeling as evidence infrastructure: scientific model registers, mechanism records, population-growth simulation, scenario summaries, validation and uncertainty notes, model-family documentation, typed scientific model records, and responsible scientific interpretation artifacts.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional scientific model registration, evidence review, population simulation, scenario comparison, uncertainty communication, and reproducibility scaffolding.

## Folder structure

```text
articles/mathematical-modeling-in-science/
├── python/      # Scientific model register, population simulation, evidence card, tests
├── r/           # Model evidence summary and diagnostic review
├── julia/       # Logistic population scenario summary
├── sql/         # Scientific modeling governance schema and queries
├── haskell/     # Typed scientific model records
├── rust/        # Strongly typed scientific model record CLI
├── go/          # Lightweight scientific scenario summary
├── cpp/         # Engineering-style scientific simulation summary
├── fortran/     # Scientific-computing population model
├── c/           # Low-level population simulation example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Scientific modeling, validation, measurement, uncertainty, ethics
├── data/        # Model register, scenarios, disciplinary guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for scientific model records and scenarios
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
python3 python/mathematical_modeling_in_science/cli.py --output-dir outputs
```

## Modeling themes

- scientific models as bridges between theory and observation;
- mechanism modeling, prediction, simulation, and inference;
- calibration, validation, and domain of validity;
- measurement error, uncertainty, and sensitivity;
- model comparison and scientific evidence review;
- reproducible scientific computation and responsible interpretation.

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
