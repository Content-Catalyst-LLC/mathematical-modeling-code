# Functional Relationships and Mathematical Structure

Companion code and reproducible workflows for **“Functional Relationships and Mathematical Structure”** in the **Mathematical Modeling** knowledge series.

This folder treats functional relationships and mathematical structure as explicit, reviewable model design choices. It supports relationship registers, functional-form comparison, linear and nonlinear updates, bounded dynamics, feedback rules, stochastic scenario analysis, structural validation, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and structural-review scaffolding.

## Folder structure

```text
articles/functional-relationships-and-mathematical-structure/
├── python/      # Relationship register, structural diagnostics, CLI, tests
├── r/           # Functional-form comparison and review workflow
├── julia/       # Numerical structural scenario workflow
├── sql/         # Relationship governance schema and diagnostic queries
├── haskell/     # Typed relationship structures
├── rust/        # Strongly typed structural-review CLI
├── go/          # Lightweight structure scenario workflow
├── cpp/         # Engineering-style structural model
├── fortran/     # Scientific-computing structural simulation
├── c/           # Low-level deterministic structural simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Relationship types, structure, validation, ethics
├── data/        # Relationship registers and scenario inputs
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
python3 python/functional_relationships_structure/cli.py --output-dir outputs
```

## Modeling themes

- functional relationships as claims about dependence;
- mathematical structure as a mapping from variables, parameters, assumptions, and constraints to outputs;
- linear, nonlinear, static, dynamic, deterministic, stochastic, networked, and constrained structures;
- feedback, interaction, thresholds, and regime changes;
- relationship registers and structural validation;
- structural sensitivity and failure diagnostics;
- typed model governance and reproducibility.

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
