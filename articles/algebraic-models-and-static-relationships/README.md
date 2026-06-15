# Algebraic Models and Static Relationships

Companion code and reproducible workflows for **“Algebraic Models and Static Relationships”** in the **Mathematical Modeling** knowledge series.

This folder treats algebraic relationships, static models, identities, balances, ratios, constraints, feasible regions, objectives, and scenario comparisons as explicit model design objects. It supports relationship registers, static allocation scenarios, feasibility diagnostics, constraint review, typed relationship records, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and static-relationship review scaffolding.

## Folder structure

```text
articles/algebraic-models-and-static-relationships/
├── python/      # Relationship register, static allocation model, CLI, tests
├── r/           # Static relationship diagnostics and review workflow
├── julia/       # Numerical algebraic scenario workflow
├── sql/         # Algebraic-governance schema and diagnostic queries
├── haskell/     # Typed algebraic relationships
├── rust/        # Strongly typed relationship-review CLI
├── go/          # Lightweight static allocation workflow
├── cpp/         # Engineering-style algebraic allocation model
├── fortran/     # Scientific-computing static allocation model
├── c/           # Low-level deterministic static allocation model
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Relationship registers, feasibility, ethics, validation
├── data/        # Algebraic relationships and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for relationships and scenarios
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
python3 python/algebraic_models_static_relationships/cli.py --output-dir outputs
```

## Modeling themes

- algebraic models as disciplined static representations;
- identities, balances, ratios, objectives, and constraints;
- feasible regions and static optimization;
- linear and nonlinear relationship review;
- relationship domains, units, assumptions, and interpretation;
- scenario comparison and constraint diagnostics.

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
